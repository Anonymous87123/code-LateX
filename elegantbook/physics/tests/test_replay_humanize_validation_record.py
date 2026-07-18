import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SKILL = Path.home() / ".codex" / "skills" / "humanize-academic-chinese"
VALIDATOR_PATH = SKILL / "scripts" / "validate_humanize_output.py"
REPLAY_PATH = SKILL / "scripts" / "replay_humanize_validation_record.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validator = load_module("humanize_validator_v29_tests", VALIDATOR_PATH)
replayer = load_module("humanize_replayer_v29_tests", REPLAY_PATH)


class HumanizeValidationReplayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.before = self.root / "before.md"
        self.after = self.root / "after.md"
        self.before.write_text("值得注意的是，峰值出现在高温组。", encoding="utf-8")
        self.after.write_text("峰值出现在高温组。", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def publish(
        self,
        evidence_dir: Path,
        *,
        before: Path | None = None,
        after: Path | None = None,
        extra: list[str] | None = None,
        expected_exit: int = 2,
    ) -> tuple[subprocess.CompletedProcess[str], dict]:
        command = [
            sys.executable,
            str(VALIDATOR_PATH),
            str(before or self.before),
            str(after or self.after),
            "--scene",
            "RESEARCH",
            "--format",
            "json",
            "--evidence-dir",
            str(evidence_dir),
        ]
        command.extend(extra or [])
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        self.assertEqual(expected_exit, completed.returncode, completed.stderr)
        return completed, json.loads(completed.stdout)

    def replay_cli(self, evidence_dir: Path, *extra: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        completed = subprocess.run(
            [
                sys.executable,
                str(REPLAY_PATH),
                str(evidence_dir),
                "--format",
                "json",
                *extra,
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        return completed, json.loads(completed.stdout)

    @staticmethod
    def tree_hashes(root: Path) -> dict[str, str]:
        return {
            path.relative_to(root).as_posix(): validator._sha256(path.read_bytes())
            for path in root.rglob("*")
            if path.is_file()
        }

    @staticmethod
    def refresh_manifest(root: Path, changed_path: str) -> None:
        manifest_path = root / "evidence-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        raw = (root / changed_path).read_bytes()
        manifest["artifacts"][changed_path] = {
            "sha256": validator._sha256(raw),
            "size": len(raw),
        }
        identity = {
            "schema": manifest["schema"],
            "run_id": manifest["run_id"],
            "artifacts": manifest["artifacts"],
        }
        manifest["record_sha256"] = validator._sha256(
            validator._canonical_json_bytes(identity)
        )
        body = dict(manifest)
        body.pop("manifest_sha256", None)
        manifest["manifest_sha256"] = validator._sha256(
            validator._canonical_json_bytes(body)
        )
        manifest_path.write_bytes(validator._pretty_json_bytes(manifest))

    def test_supported_record_replays_from_archived_inputs(self) -> None:
        evidence = self.root / "evidence"
        _, original = self.publish(evidence)
        completed, payload = self.replay_cli(evidence)
        self.assertEqual(
            0,
            completed.returncode,
            json.dumps(payload, ensure_ascii=False, indent=2),
        )
        self.assertEqual("PASS", payload["status"])
        self.assertEqual("PASS", payload["record_integrity_status"])
        self.assertEqual("PASS", payload["reexecution_status"])
        self.assertEqual(original["evidence_bundle"]["run_id"], payload["run_id"])
        self.assertEqual("NOT_EVALUATED", payload["academic_correctness"])
        self.assertFalse(payload["paired_quality_clearance_granted"])
        self.assertFalse(payload["humanize_quality_claim_allowed"])

    def test_text_record_with_finding_replays_without_absolute_path_drift(self) -> None:
        before = self.root / "research_before.md"
        after = self.root / "research_after.md"
        before.write_text("本段讨论已有结果。", encoding="utf-8")
        after.write_text("本段为后续研究提供了基础。", encoding="utf-8")
        evidence = self.root / "text-evidence"
        completed = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR_PATH),
                str(before),
                str(after),
                "--scene",
                "RESEARCH",
                "--format",
                "text",
                "--evidence-dir",
                str(evidence),
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        self.assertEqual(2, completed.returncode, completed.stderr)
        self.assertIn("after:", completed.stdout)
        self.assertNotIn(str(self.root), completed.stdout)
        replayed, payload = self.replay_cli(evidence)
        self.assertEqual(0, replayed.returncode, json.dumps(payload, ensure_ascii=False))
        self.assertEqual("PASS", payload["reexecution_status"])

    def test_identical_publication_is_idempotent_and_byte_preserving(self) -> None:
        evidence = self.root / "evidence"
        _, first = self.publish(evidence)
        before_hashes = self.tree_hashes(evidence)
        _, second = self.publish(evidence)
        self.assertEqual(first, second)
        self.assertEqual(before_hashes, self.tree_hashes(evidence))

    def test_same_invocation_has_same_run_id_and_config_change_has_new_id(self) -> None:
        _, first = self.publish(self.root / "evidence-a")
        _, second = self.publish(self.root / "evidence-b")
        self.assertEqual(
            first["evidence_bundle"]["run_id"],
            second["evidence_bundle"]["run_id"],
        )
        _, changed = self.publish(
            self.root / "evidence-c",
            extra=["--scene", "COURSE"],
        )
        self.assertNotEqual(
            first["evidence_bundle"]["run_id"],
            changed["evidence_bundle"]["run_id"],
        )

    def test_existing_directory_with_different_invocation_is_conflict(self) -> None:
        evidence = self.root / "evidence"
        self.publish(evidence)
        initial = self.tree_hashes(evidence)
        completed, payload = self.publish(
            evidence,
            extra=["--scene", "COURSE"],
            expected_exit=1,
        )
        self.assertEqual("FAIL", payload["status"])
        self.assertEqual("EVIDENCE_PERSISTENCE_FAILED", payload["error_code"])
        self.assertIn("conflict", payload["error"])
        self.assertEqual(initial, self.tree_hashes(evidence))
        self.assertEqual("", completed.stderr)

    def test_each_bound_artifact_tamper_fails_before_reexecution(self) -> None:
        source = self.root / "source-evidence"
        self.publish(source)
        paths = [
            "inputs/before.bin",
            "inputs/after.bin",
            "invocation-request.json",
            "validation-result.json",
            "paired-quality-review-request.json",
            "rendered-output.txt",
            "stderr.txt",
            "execution-record.json",
            "evidence-manifest.json",
        ]
        for index, relative in enumerate(paths):
            with self.subTest(relative=relative):
                tampered = self.root / f"tampered-{index}"
                shutil.copytree(source, tampered)
                path = tampered / relative
                path.write_bytes(path.read_bytes() + b"X")
                completed, payload = self.replay_cli(tampered)
                self.assertEqual(1, completed.returncode)
                self.assertEqual("FAIL", payload["status"])
                self.assertEqual("NOT_RUN", payload["reexecution_status"])

    def test_rehashed_result_tamper_still_fails_cross_artifact_binding(self) -> None:
        evidence = self.root / "evidence"
        self.publish(evidence)
        result_path = evidence / "validation-result.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result["delivery_gate_status"] = "PASS"
        result_path.write_bytes(validator._pretty_json_bytes(result))
        self.refresh_manifest(evidence, "validation-result.json")
        completed, payload = self.replay_cli(evidence)
        self.assertEqual(1, completed.returncode)
        self.assertEqual("RESULT_STATUS_MISMATCH", payload["error_code"])

    def test_rehashed_stdout_tamper_still_fails_result_consistency(self) -> None:
        evidence = self.root / "evidence"
        self.publish(evidence)
        output = evidence / "rendered-output.txt"
        output.write_bytes(output.read_bytes().replace(b'"status": "REVIEW"', b'"status": "PASS__"'))
        self.refresh_manifest(evidence, "rendered-output.txt")
        completed, payload = self.replay_cli(evidence)
        self.assertEqual(1, completed.returncode)
        self.assertEqual("STDOUT_RESULT_MISMATCH", payload["error_code"])

    def test_extra_file_is_rejected(self) -> None:
        evidence = self.root / "evidence"
        self.publish(evidence)
        (evidence / "unbound.txt").write_text("extra", encoding="utf-8")
        completed, payload = self.replay_cli(evidence)
        self.assertEqual(1, completed.returncode)
        self.assertEqual("RECORD_INVENTORY_MISMATCH", payload["error_code"])

    def test_hardlinked_record_file_is_rejected(self) -> None:
        evidence = self.root / "evidence"
        self.publish(evidence)
        try:
            os.link(
                evidence / "validation-result.json",
                self.root / "result-hardlink.json",
            )
        except OSError as error:
            self.skipTest(f"hard links unavailable: {error}")
        completed, payload = self.replay_cli(evidence)
        self.assertEqual(1, completed.returncode)
        self.assertEqual("HARDLINK_REJECTED", payload["error_code"])

    def test_policy_drift_is_review_not_false_replay_pass(self) -> None:
        evidence = self.root / "evidence"
        self.publish(evidence)
        manifest, artifacts = replayer._load_record(evidence)
        invocation = replayer._validate_invocation(manifest, artifacts)
        changed = dict(invocation["policy_hashes"])
        changed["validator_sha256"] = "0" * 64
        with mock.patch.object(replayer, "_current_policy_hashes", return_value=changed):
            payload, exit_code = replayer.replay_record(evidence)
        self.assertEqual(2, exit_code)
        self.assertEqual("REVIEW", payload["status"])
        self.assertEqual("PASS", payload["record_integrity_status"])
        self.assertEqual("NOT_RUN", payload["reexecution_status"])
        self.assertEqual(["POLICY_DRIFT"], payload["reexecution_reasons"])

    def test_rehashed_invocation_unknown_field_and_path_injection_are_rejected(self) -> None:
        evidence = self.root / "evidence"
        self.publish(evidence)
        manifest, artifacts = replayer._load_record(evidence)
        baseline = json.loads(artifacts["invocation-request.json"].decode("utf-8"))
        cases = (
            ("unknown", lambda item: item["arguments"].update({"hidden_override": True}), "INVALID_SCHEMA"),
            (
                "path",
                lambda item: item["inputs"]["before"].update(
                    {"archive_path": "../inputs/before.bin"}
                ),
                "UNSAFE_ARTIFACT_PATH",
            ),
            (
                "suffix",
                lambda item: item["inputs"]["before"].update(
                    {"original_suffix": ".md/../../escape"}
                ),
                "INVALID_INPUT_SUFFIX",
            ),
        )
        for name, mutate, expected_code in cases:
            with self.subTest(name=name):
                invocation = json.loads(json.dumps(baseline))
                mutate(invocation)
                body = dict(invocation)
                body.pop("invocation_sha256")
                body.pop("run_id")
                invocation_sha = validator._sha256(
                    validator._canonical_json_bytes(body)
                )
                invocation["invocation_sha256"] = invocation_sha
                invocation["run_id"] = f"hvr2-{invocation_sha}"
                forged_manifest = dict(manifest)
                forged_manifest["run_id"] = invocation["run_id"]
                forged_manifest["invocation_request_sha256"] = invocation_sha
                forged_artifacts = dict(artifacts)
                forged_artifacts["invocation-request.json"] = validator._pretty_json_bytes(
                    invocation
                )
                with self.assertRaises(replayer.ReplayError) as raised:
                    replayer._validate_invocation(forged_manifest, forged_artifacts)
                self.assertEqual(expected_code, raised.exception.code)

    def test_live_source_drift_does_not_change_archive_but_can_be_required(self) -> None:
        evidence = self.root / "evidence"
        self.publish(evidence)
        self.before.write_text("来源已在记录之后改变。", encoding="utf-8")
        payload, exit_code = replayer.replay_record(
            evidence,
            live_before=self.before,
            live_after=self.after,
        )
        self.assertEqual(0, exit_code)
        self.assertEqual("NOT_CURRENT", payload["live_source_status"]["status"])
        strict_payload, strict_exit = replayer.replay_record(
            evidence,
            require_live_source_match=True,
            live_before=self.before,
            live_after=self.after,
        )
        self.assertEqual(2, strict_exit)
        self.assertEqual("REVIEW", strict_payload["status"])
        self.assertEqual("PASS", strict_payload["reexecution_status"])

    def test_report_scope_and_report_are_archived_for_offline_replay(self) -> None:
        before = self.root / "report-before.md"
        after = self.root / "report-after.md"
        before.write_text("前文不动。值得注意的是，结果为 1。后文不动。", encoding="utf-8")
        after.write_text("前文不动。结果为 1。后文不动。", encoding="utf-8")
        report = self.root / "report.html"
        report.write_text(
            '<!doctype html><html><meta charset="utf-8"><body>'
            "<mark>值得注意的是，结果为 1。</mark></body></html>",
            encoding="utf-8",
        )
        scope_payload = validator.detector_scope.analyze_report(report, before)
        scope = self.root / "report-scope.json"
        scope.write_bytes(validator._pretty_json_bytes(scope_payload))
        evidence = self.root / "report-evidence"
        _, payload = self.publish(
            evidence,
            before=before,
            after=after,
            extra=["--report-scope", str(scope)],
        )
        request = payload["paired_quality_review_request"]
        self.assertEqual("REPORT_SELECTION", request["validation_context"]["document_scope"])
        self.assertIn("report_scope_binding", request["validation_context"])
        self.assertTrue((evidence / "inputs" / "report-scope.json").is_file())
        self.assertTrue((evidence / "inputs" / "report.bin").is_file())
        before.unlink()
        after.unlink()
        report.unlink()
        scope.unlink()
        completed, replayed = self.replay_cli(evidence)
        self.assertEqual(
            0,
            completed.returncode,
            json.dumps(replayed, ensure_ascii=False, indent=2),
        )
        self.assertEqual("PASS", replayed["reexecution_status"])
        self.assertEqual("NOT_REQUESTED", replayed["live_source_status"]["status"])

    def test_identity_free_proposal_is_replayable_but_never_clears_review(self) -> None:
        before = self.root / "warning-before.md"
        after = self.root / "warning-after.md"
        before.write_text("结果可能变化。", encoding="utf-8")
        after.write_text("结果发生变化。", encoding="utf-8")
        first = validator.validate(before, after, scene="GENERAL")
        request = first["warning_review_request"]
        fingerprint = request["warnings"][0]["warning_fingerprint"]
        evidence = self.root / "warning-evidence"
        self.publish(
            evidence,
            before=before,
            after=after,
            extra=[
                "--scene",
                "GENERAL",
                "--propose-warning-resolution",
                f"{fingerprint}=人工建议恢复原句中的模态范围以保留表达功能",
                "--warning-review-request-sha256",
                request["request_sha256"],
            ],
        )
        invocation = json.loads(
            (evidence / "invocation-request.json").read_text(encoding="utf-8")
        )
        self.assertEqual("SUPPORTED", invocation["reexecution"]["status"])
        self.assertFalse(invocation["privacy"]["reviewer_identifier_collected"])
        self.assertFalse(invocation["privacy"]["stable_reviewer_pseudonym_archived"])
        completed, replayed = self.replay_cli(evidence)
        self.assertEqual(0, completed.returncode)
        self.assertEqual("PASS", replayed["status"])
        self.assertEqual("PASS", replayed["record_integrity_status"])
        self.assertEqual("PASS", replayed["reexecution_status"])
        self.assertFalse(replayed["humanize_quality_claim_allowed"])

    def test_draft_terms_and_fragment_configuration_are_replayable(self) -> None:
        supplied = self.root / "supplied.md"
        draft = self.root / "draft.md"
        supplied.write_text("材料 A 的结果为 1。", encoding="utf-8")
        draft.write_text("材料 A 的结果为 1。", encoding="utf-8")
        draft_evidence = self.root / "draft-evidence"
        self.publish(
            draft_evidence,
            before=supplied,
            after=draft,
            extra=["--mode", "DRAFT", "--term", "材料 A"],
            expected_exit=0,
        )
        completed, payload = self.replay_cli(draft_evidence)
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("PASS", payload["reexecution_status"])

        fragment_before = self.root / "fragment-before.tex"
        fragment_after = self.root / "fragment-after.tex"
        fragment_before.write_text("值得注意的是，结果为 1。\\end{solution}", encoding="utf-8")
        fragment_after.write_text("结果为 1。\\end{solution}", encoding="utf-8")
        fragment_evidence = self.root / "fragment-evidence"
        self.publish(
            fragment_evidence,
            before=fragment_before,
            after=fragment_after,
            extra=["--fragment", "--strict-speech-acts"],
        )
        completed, payload = self.replay_cli(fragment_evidence)
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("PASS", payload["reexecution_status"])


if __name__ == "__main__":
    unittest.main()
