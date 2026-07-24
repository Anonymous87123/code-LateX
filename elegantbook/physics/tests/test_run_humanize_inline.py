import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(
    os.environ.get(
        "HUMANIZE_SKILL_DIR",
        Path.home() / ".codex" / "skills" / "humanize-academic-chinese",
    )
)
SCRIPT = SKILL / "scripts" / "run_humanize_inline.py"
SPEC = importlib.util.spec_from_file_location("run_humanize_inline", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
inline = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = inline
SPEC.loader.exec_module(inline)


class HumanizeInlineRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.output_root = self.root / "runs"
        self.before = self.root / "source.md"
        self.after = self.root / "candidate.md"
        self.before.write_text(
            "值得注意的是，峰值出现在高温组。\n", encoding="utf-8"
        )
        self.after.write_text("峰值出现在高温组。\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_candidate(self, *, visible_output: str = "BODY_WITH_SUMMARY"):
        return inline.run_inline(
            self.before,
            self.after,
            output_root=self.output_root,
            mode="REWRITE",
            scene="RESEARCH",
            document_format="markdown",
            visible_output=visible_output,
        )

    def test_run_materializes_unique_artifacts_and_preserves_top_level_review(self) -> None:
        first, first_dir = self.run_candidate()
        second, second_dir = self.run_candidate()

        self.assertNotEqual(first_dir, second_dir)
        self.assertEqual("INLINE_TEXT", first["source_kind"])
        self.assertEqual("VALIDATED", first["execution_status"])
        self.assertEqual("PASS", first["mechanical_validation_status"])
        self.assertEqual("REVIEW", first["delivery_gate_status"])
        self.assertEqual(2, first["exit_code"])
        self.assertFalse(first["completion_claim_allowed"])
        self.assertTrue(first["body_emission_allowed"])
        self.assertTrue((first_dir / "evidence" / "evidence-manifest.json").is_file())
        self.assertEqual(
            self.before.read_bytes(),
            (first_dir / first["artifacts"]["before"]["path"]).read_bytes(),
        )
        self.assertEqual(
            self.after.read_bytes(),
            (first_dir / first["artifacts"]["after"]["path"]).read_bytes(),
        )

    def test_body_only_hides_audit_display_but_still_creates_evidence(self) -> None:
        record, run_dir = self.run_candidate(visible_output="BODY_ONLY")

        self.assertEqual("BODY_ONLY", record["visible_output"])
        self.assertTrue(
            record["response_contract"][
                "body_only_hides_audit_display_not_audit_execution"
            ]
        )
        self.assertEqual("VALIDATED", record["execution_status"])
        self.assertTrue((run_dir / "validation.json").is_file())
        self.assertTrue((run_dir / "evidence" / "evidence-manifest.json").is_file())

    def test_emit_body_rechecks_and_returns_exact_validated_bytes(self) -> None:
        _record, run_dir = self.run_candidate(visible_output="BODY_ONLY")

        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "emit", str(run_dir), "--format", "body"],
            check=False,
            capture_output=True,
        )

        self.assertEqual(2, completed.returncode)
        self.assertEqual(self.after.read_bytes(), completed.stdout)
        self.assertEqual(b"", completed.stderr)
        self.assertNotIn(b"delivery_gate_status", completed.stdout)

    def test_post_validation_mutation_blocks_body_emission(self) -> None:
        record, run_dir = self.run_candidate(visible_output="BODY_ONLY")
        frozen_after = run_dir / record["artifacts"]["after"]["path"]
        frozen_after.write_text("峰值位置发生了变化。\n", encoding="utf-8")

        verification, body = inline.verify_run(run_dir)

        self.assertEqual("FAIL", verification["status"])
        self.assertEqual(1, verification["exit_code"])
        self.assertEqual("FAIL", verification["delivery_gate_status"])
        self.assertFalse(verification["body_emission_allowed"])
        self.assertIn("artifact_sha256_mismatch:after", verification["reason"])
        self.assertIsNone(body)

    def test_validator_not_started_is_honest_not_run_review(self) -> None:
        record, run_dir = inline.run_inline(
            self.before,
            self.after,
            output_root=self.output_root,
            mode="REWRITE",
            scene="RESEARCH",
            document_format="markdown",
            visible_output="BODY_ONLY",
            validator_path=self.root / "missing-validator.py",
        )

        self.assertEqual("NOT_RUN", record["execution_status"])
        self.assertEqual("NOT_RUN", record["mechanical_validation_status"])
        self.assertEqual("REVIEW", record["delivery_gate_status"])
        self.assertEqual(2, record["exit_code"])
        self.assertFalse(record["body_emission_allowed"])
        validation = json.loads((run_dir / "validation.json").read_text(encoding="utf-8"))
        self.assertFalse(validation["evidence"]["checker_executed"])
        self.assertFalse(
            (run_dir / record["artifacts"]["evidence_manifest"]["path"]).exists()
        )

    def test_tampered_validation_record_fails_closed(self) -> None:
        record, run_dir = self.run_candidate()
        validation_path = run_dir / record["artifacts"]["validation"]["path"]
        payload = json.loads(validation_path.read_text(encoding="utf-8"))
        payload["delivery_gate_status"] = "PASS"
        validation_path.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8"
        )

        verification, body = inline.verify_run(run_dir)

        self.assertEqual("FAIL", verification["status"])
        self.assertFalse(verification["body_emission_allowed"])
        self.assertIsNone(body)

    def test_tampered_invocation_record_fails_closed(self) -> None:
        record, run_dir = self.run_candidate()
        invocation_path = run_dir / record["artifacts"]["invocation"]["path"]
        payload = json.loads(invocation_path.read_text(encoding="utf-8"))
        payload["scene"] = "GENERAL"
        invocation_path.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8"
        )

        verification, body = inline.verify_run(run_dir)

        self.assertEqual("FAIL", verification["status"])
        self.assertIn("artifact_sha256_mismatch:invocation", verification["reason"])
        self.assertIsNone(body)

    def test_tampered_evidence_manifest_fails_closed(self) -> None:
        record, run_dir = self.run_candidate()
        manifest_path = run_dir / record["artifacts"]["evidence_manifest"]["path"]
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        payload["scene"] = "GENERAL"
        manifest_path.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8"
        )

        verification, body = inline.verify_run(run_dir)

        self.assertEqual("FAIL", verification["status"])
        self.assertIn("artifact_sha256_mismatch:evidence_manifest", verification["reason"])
        self.assertIsNone(body)

    def test_draft_can_emit_mechanically_clear_candidate_without_quality_claim(self) -> None:
        self.before.write_text(
            "低温组误差小于高温组。两组峰值位置接近。\n", encoding="utf-8"
        )
        self.after.write_text(
            "低温组误差小于高温组，两组峰值位置接近。\n", encoding="utf-8"
        )

        record, run_dir = inline.run_inline(
            self.before,
            self.after,
            output_root=self.output_root,
            mode="DRAFT",
            scene="RESEARCH",
            document_format="markdown",
            visible_output="BODY_ONLY",
        )
        verification, body = inline.verify_run(run_dir)

        self.assertEqual("PASS", record["mechanical_validation_status"])
        self.assertEqual("REVIEW", record["delivery_gate_status"])
        self.assertEqual(2, record["exit_code"])
        self.assertFalse(record["humanize_quality_claim_allowed"])
        self.assertTrue(record["body_emission_allowed"])
        self.assertEqual("PASS", verification["status"])
        self.assertEqual(self.after.read_bytes(), body)

    def test_tex_candidate_preserves_formula_and_emits_exact_bytes(self) -> None:
        self.before = self.root / "source.tex"
        self.after = self.root / "candidate.tex"
        self.before.write_text(
            "值得注意的是，关系为 \\(E=mc^2\\)。\n", encoding="utf-8"
        )
        self.after.write_text("关系为 \\(E=mc^2\\)。\n", encoding="utf-8")

        record, run_dir = inline.run_inline(
            self.before,
            self.after,
            output_root=self.output_root,
            mode="REWRITE",
            scene="RESEARCH",
            document_format="tex",
            visible_output="BODY_ONLY",
        )
        verification, body = inline.verify_run(run_dir)

        self.assertEqual("PASS", record["mechanical_validation_status"])
        self.assertEqual("REVIEW", record["delivery_gate_status"])
        self.assertEqual(self.after.read_bytes(), body)

    def test_cli_run_reports_run_directory_without_claiming_completion(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "run",
                str(self.before),
                str(self.after),
                "--output-root",
                str(self.output_root),
                "--mode",
                "REWRITE",
                "--scene",
                "RESEARCH",
                "--document-format",
                "markdown",
                "--visible-output",
                "BODY_ONLY",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(2, completed.returncode)
        self.assertEqual("PASS", payload["mechanical_validation_status"])
        self.assertEqual("REVIEW", payload["delivery_gate_status"])
        self.assertFalse(payload["completion_claim_allowed"])
        self.assertTrue(Path(payload["run_dir"]).is_dir())


if __name__ == "__main__":
    unittest.main()
