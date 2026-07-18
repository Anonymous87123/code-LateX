import hashlib
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
SCRIPT = SKILL / "scripts" / "build_humanize_generator_projection.py"
SPEC = importlib.util.spec_from_file_location("build_humanize_generator_projection", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
builder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class HumanizeGeneratorProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.skill = self.root / "humanize-academic-chinese"
        shutil.copytree(
            SKILL,
            self.skill,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        self.counter = 0

    def tearDown(self) -> None:
        self.temp.cleanup()

    def build(self, *, real_quick_validate: bool = False) -> tuple[dict, Path, Path]:
        self.counter += 1
        output = self.root / f"projection-{self.counter}"
        manifest = self.root / f"manifest-{self.counter}.json"
        if real_quick_validate:
            result = builder.build_projection(self.skill, output, manifest)
        else:
            with mock.patch.object(builder, "_quick_validate", return_value="PASS"):
                result = builder.build_projection(self.skill, output, manifest)
        return result, output, manifest

    def policy_payload(self) -> dict:
        path = self.skill / "references" / "generator-projection-policy.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def write_policy(self, payload: dict) -> None:
        path = self.skill / "references" / "generator-projection-policy.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def test_baseline_projection_has_exact_capability_surface(self) -> None:
        result, output, manifest = self.build(real_quick_validate=True)
        files = sorted(
            path.relative_to(output).as_posix()
            for path in output.rglob("*")
            if path.is_file()
        )
        expected = sorted([*builder.EXPECTED_INCLUDE, *builder.EXPECTED_TRANSFORM])
        self.assertEqual(expected, files)
        self.assertEqual(30, len(files))
        self.assertIn("references/structural-rewrite-contract.md", files)
        self.assertFalse((output / manifest.name).exists())
        self.assertEqual("PASS", result["audits"]["skill_quick_validate"])
        self.assertFalse(result["audits"]["read_only_marking_is_isolation_proof"])

    def test_rebuild_is_byte_deterministic(self) -> None:
        first, _first_output, first_manifest = self.build()
        second, _second_output, second_manifest = self.build()
        self.assertEqual(first["projection_tree_sha256"], second["projection_tree_sha256"])
        self.assertEqual(first_manifest.read_bytes(), second_manifest.read_bytes())
        self.assertEqual(first["manifest_sha256"], second["manifest_sha256"])

    def test_manifest_binds_hidden_evaluation_surface_without_entering_projection(self) -> None:
        result, output, _manifest = self.build()
        excluded = {item["path"] for item in result["excluded"]}
        self.assertIn("references/generation-qualification-oracles.json", excluded)
        self.assertIn("references/generation-qualification-trust.json", excluded)
        self.assertIn("scripts/audit_humanize_generation_qualification.py", excluded)
        self.assertIn("scripts/replay_humanize_validation_record.py", excluded)
        self.assertIn("scripts/replay_humanize_long_fixture.py", excluded)
        self.assertFalse(
            (output / "scripts" / "replay_humanize_validation_record.py").exists()
        )
        self.assertFalse((output / "scripts" / "replay_humanize_long_fixture.py").exists())
        self.assertRegex(result["source"]["evaluation_surface_sha256"], r"^[0-9a-f]{64}$")
        self.assertFalse(any("qualification" in path.name for path in output.rglob("*")))

    def test_second_pass_control_plane_is_hidden_from_fresh_generator(self) -> None:
        result, output, _manifest = self.build()
        excluded = {item["path"] for item in result["excluded"]}
        self.assertIn("scripts/prepare_humanize_second_pass.py", excluded)
        self.assertIn("scripts/verify_humanize_second_pass.py", excluded)
        self.assertFalse((output / "scripts" / "prepare_humanize_second_pass.py").exists())
        self.assertFalse((output / "scripts" / "verify_humanize_second_pass.py").exists())
        projected_finalizer = (
            output / "scripts" / "finalize_humanize_long_document.py"
        ).read_text(encoding="utf-8")
        for leaked_control in (
            "all_units_no_change",
            "second_output_equals_first",
            "verify_humanize_second_pass.py",
            "expected_outcome_exposed",
        ):
            self.assertNotIn(leaked_control, projected_finalizer)

    def test_long_replay_and_transaction_qualification_controls_do_not_leak(self) -> None:
        _result, output, _manifest = self.build()
        projected_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in output.rglob("*")
            if path.is_file() and path.suffix.lower() in {".md", ".json", ".py", ".yaml"}
        )
        self.assertNotIn("replay_humanize_long_fixture.py", projected_text)
        for control_id in (
            "LONG-20",
            "LONG-21",
            "LONG-22",
            "LONG-23",
            "LONG-24",
            "LONG-25",
            "LONG-26",
            "LONG-27",
            "DEC-09",
        ):
            self.assertNotIn(control_id, projected_text)
        for hidden_outcome in (
            "structural_review_request_binding_status",
            "transaction_non_downgrade_status",
        ):
            self.assertNotIn(hidden_outcome, projected_text)

    def test_skill_transform_removes_only_fixed_control_spans(self) -> None:
        raw = (self.skill / "SKILL.md").read_bytes()
        projected, removed = builder._transform_skill(raw)
        self.assertEqual(5, len(removed))
        labels = {item["label"] for item in removed}
        self.assertEqual(
            {
                "route-row:来源动作候选审计",
                "route-row:验证 Skill",
                "route-row:生成资格审计",
                "sections:生成资格与来源候选审计",
                "control:SECOND_PASS",
            },
            labels,
        )
        text = projected.decode("utf-8")
        self.assertNotIn("## 生成资格采集边界", text)
        self.assertNotIn("## 来源锚定的改写候选", text)
        self.assertIn("## 来源信任边界", text)
        self.assertIn("| 长 MD/TEX |", text)
        self.assertNotIn("validate_humanize_candidate_queue.py", text)

    def test_long_workflow_transform_removes_convergence_answer_surface(self) -> None:
        raw = (self.skill / "references" / "long-document-workflow.md").read_bytes()
        projected, removed = builder._transform_long_workflow(raw)
        text = projected.decode("utf-8")
        self.assertEqual(2, len(removed))
        self.assertIn("## 16. 独立复读", text)
        self.assertNotIn("prepare_humanize_second_pass.py", text)
        self.assertNotIn("verify_humanize_second_pass.py", text)
        self.assertNotIn("全部 fresh 决策为 `NO_CHANGE`", text)

    def test_corpus_transform_emits_strict_detector_only_registry(self) -> None:
        raw = (self.skill / "references" / "corpus-action-sources.json").read_bytes()
        original = json.loads(raw.decode("utf-8"))

        projected_raw, removed = builder._transform_corpus_action_sources(raw)
        projected = json.loads(projected_raw.decode("utf-8"))

        self.assertEqual(4, len(removed))
        self.assertEqual(17, removed[0]["count"])
        self.assertEqual(
            {
                "schema_version": "humanize-negative-guard-registry/v1",
                "registry_id": "humanize-academic-chinese/corpus-negative-guards/v1",
            },
            {key: projected[key] for key in ("schema_version", "registry_id")},
        )
        self.assertEqual({"schema_version", "registry_id", "guards"}, set(projected))
        self.assertEqual(4, len(projected["guards"]))
        self.assertTrue(
            all(set(guard) == {"id", "scene", "detector"} for guard in projected["guards"])
        )
        source_origins = {
            source["id"]: source["origin_class"] for source in original["sources"]
        }
        runtime_origins = {"MODEL_GENERATED", "MODEL_ORIGIN_UNRESOLVED"}
        expected = {
            card["id"]: {"scene": card["scene"], "detector": card["detector"]}
            for card in original["action_cards"]
            if card["kind"] == "negative_guard"
            and all(
                source_origins[ref["source_id"]] in runtime_origins
                for ref in card["source_refs"]
            )
        }
        actual = {
            guard["id"]: {"scene": guard["scene"], "detector": guard["detector"]}
            for guard in projected["guards"]
        }
        self.assertEqual(expected, actual)
        self.assertEqual(6, removed[2]["count"])
        serialized = projected_raw.decode("utf-8")
        self.assertNotIn("COURSE-DECISION-01", serialized)
        self.assertNotIn("MODELING-METRIC-ROLE-01", serialized)
        for forbidden in (
            "sources",
            "source_refs",
            "origin_class",
            "source_tier",
            "path",
            "action",
            "requires",
            "forbids",
            "use_limit",
        ):
            self.assertNotIn(forbidden, serialized)

    def test_projection_contains_loader_but_not_full_action_builder(self) -> None:
        _result, output, _manifest = self.build()
        self.assertTrue((output / "scripts" / "load_humanize_negative_guards.py").is_file())
        self.assertFalse((output / "scripts" / "build_humanize_action_profile.py").exists())

    def test_corpus_transform_rejects_local_negative_permission_widening(self) -> None:
        raw = (self.skill / "references" / "corpus-action-sources.json").read_bytes()
        trust_path = self.skill / "references" / "source-provenance-trust.json"
        trust = json.loads(trust_path.read_text(encoding="utf-8"))
        trust["origin_decisions"]["THIRD_PARTY"]["allowed_uses"].append(
            "NEGATIVE_GUARD"
        )
        with self.assertRaisesRegex(builder.ProjectionError, "decision matrix drifted"):
            builder._transform_corpus_action_sources(
                raw, json.dumps(trust, ensure_ascii=False).encode("utf-8")
            )

    def test_candidate_queue_control_is_absent_from_generator_projection(self) -> None:
        _result, output, _manifest = self.build()
        for relative in (
            "scripts/prepare_humanize_candidate_revision.py",
            "scripts/validate_humanize_candidate_queue.py",
        ):
            self.assertFalse((output / relative).exists())

    def test_missing_or_duplicate_transform_anchor_fails_closed(self) -> None:
        skill_path = self.skill / "SKILL.md"
        original = skill_path.read_text(encoding="utf-8")
        for name, changed in (
            ("missing", original.replace("## 生成资格采集边界", "## 资格边界", 1)),
            (
                "duplicate",
                original.replace(
                    "| 验证 Skill |",
                    "| 验证 Skill | duplicate |\n| 验证 Skill |",
                    1,
                ),
            ),
        ):
            with self.subTest(name=name):
                with self.assertRaises(builder.ProjectionError):
                    builder._transform_skill(changed.encode("utf-8"))

    def test_invalid_utf8_skill_fails(self) -> None:
        with self.assertRaisesRegex(builder.ProjectionError, "strict UTF-8"):
            builder._transform_skill(b"---\nname: x\ndescription: x\n---\n\xff")

    def test_unknown_source_file_fails_instead_of_auto_including(self) -> None:
        (self.skill / "references" / "new-helpful-rule.md").write_text(
            "看似生产规则", encoding="utf-8"
        )
        with self.assertRaisesRegex(builder.ProjectionError, "unclassified source file"):
            self.build()

    def test_unknown_oracle_like_file_also_fails(self) -> None:
        (self.skill / "references" / "oracle-copy.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(builder.ProjectionError, "unclassified source file"):
            self.build()

    def test_policy_cannot_widen_include_set(self) -> None:
        payload = self.policy_payload()
        payload["include_exact"].append("references/evaluation-contract.md")
        payload["exclude_exact"].remove("references/evaluation-contract.md")
        self.write_policy(payload)
        with self.assertRaisesRegex(builder.ProjectionError, "include_exact drifted"):
            self.build()

    def test_policy_cannot_drop_trust_or_oracle_exclusion(self) -> None:
        for path in (
            "references/generation-qualification-trust.json",
            "references/generation-qualification-oracles.json",
            "scripts/replay_humanize_validation_record.py",
        ):
            with self.subTest(path=path):
                payload = self.policy_payload()
                payload["exclude_exact"].remove(path)
                self.write_policy(payload)
                with self.assertRaisesRegex(builder.ProjectionError, "exclude_exact drifted"):
                    self.build()
                shutil.copyfile(SKILL / "references" / "generator-projection-policy.json", self.skill / "references" / "generator-projection-policy.json")

    def test_duplicate_policy_key_is_rejected(self) -> None:
        path = self.skill / "references" / "generator-projection-policy.json"
        raw = path.read_text(encoding="utf-8")
        path.write_text(raw[:-2] + ',"policy_id":"duplicate"}\n', encoding="utf-8")
        with self.assertRaisesRegex(builder.ProjectionError, "duplicate JSON key"):
            self.build()

    def test_missing_policy_path_is_rejected(self) -> None:
        (self.skill / "references" / "course-notes.md").unlink()
        with self.assertRaisesRegex(builder.ProjectionError, "policy paths are absent"):
            self.build()

    def test_forbidden_basename_leak_in_production_file_is_rejected(self) -> None:
        path = self.skill / "references" / "course-notes.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n参见 generation-qualification-oracles.json。\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(builder.ProjectionError, "forbidden evaluation basename"):
            self.build()

    def test_control_id_leak_in_production_file_is_rejected(self) -> None:
        path = self.skill / "references" / "course-notes.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n执行 PATH-05。\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(builder.ProjectionError, "hidden catalog identifier leaked"):
            self.build()

    def test_non_numeric_global_control_id_leak_is_rejected(self) -> None:
        path = self.skill / "references" / "course-notes.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n执行 PROTECTED/hash-zero。\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(builder.ProjectionError, "control ID leaked"):
            self.build()

    def test_benign_capability_content_drift_requires_policy_approval(self) -> None:
        path = self.skill / "references" / "course-notes.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n这是一条没有控制词的新增规则。\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(builder.ProjectionError, "source hash is not approved"):
            self.build()

    def test_missing_local_reference_is_rejected(self) -> None:
        path = self.skill / "references" / "course-notes.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n参见 [缺失](references/not-present.md)。\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(builder.ProjectionError, "reference closure failed"):
            self.build()

    def test_manifest_inside_projection_is_rejected(self) -> None:
        output = self.root / "projection"
        with self.assertRaisesRegex(builder.ProjectionError, "manifest must remain outside"):
            builder.build_projection(self.skill, output, output / "manifest.json")

    def test_manifest_inside_source_skill_is_rejected(self) -> None:
        with self.assertRaisesRegex(builder.ProjectionError, "outside the source Skill"):
            builder.build_projection(
                self.skill,
                self.root / "projection",
                self.skill / "build" / "projection-manifest.json",
            )

    def test_source_and_output_containment_is_rejected(self) -> None:
        with self.assertRaisesRegex(builder.ProjectionError, "must not contain each other"):
            builder.build_projection(
                self.skill,
                self.skill / "projection",
                self.root / "manifest.json",
            )

    def test_manifest_publish_failure_rolls_back_projection(self) -> None:
        output = self.root / "projection"
        manifest = self.root / "manifest.json"
        with (
            mock.patch.object(builder, "_quick_validate", return_value="PASS"),
            mock.patch.object(builder.os, "replace", side_effect=OSError("publish failed")),
            self.assertRaisesRegex(OSError, "publish failed"),
        ):
            builder.build_projection(self.skill, output, manifest)
        self.assertFalse(output.exists())
        self.assertFalse(manifest.exists())

    def test_qualification_section_cannot_swallow_an_inserted_h2(self) -> None:
        raw = (self.skill / "SKILL.md").read_text(encoding="utf-8")
        changed = raw.replace(
            "## 来源锚定的改写候选",
            "## 新增生产规则\n\n这段内容不得被静默删除。\n\n## 来源锚定的改写候选",
            1,
        )
        with self.assertRaisesRegex(builder.ProjectionError, "immediate next H2"):
            builder._transform_skill(changed.encode("utf-8"))

    def test_qualification_heading_inside_code_fence_is_not_an_anchor(self) -> None:
        raw = (self.skill / "SKILL.md").read_text(encoding="utf-8")
        changed = raw.replace(
            "## 生成资格采集边界",
            "```text\n## 生成资格采集边界\n```",
            1,
        )
        with self.assertRaisesRegex(builder.ProjectionError, "unfenced heading"):
            builder._transform_skill(changed.encode("utf-8"))

    def test_existing_output_or_manifest_is_rejected(self) -> None:
        output = self.root / "projection"
        output.mkdir()
        with self.assertRaisesRegex(builder.ProjectionError, "must not already exist"):
            builder.build_projection(self.skill, output, self.root / "manifest.json")
        output.rmdir()
        manifest = self.root / "manifest.json"
        manifest.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(builder.ProjectionError, "must not already exist"):
            builder.build_projection(self.skill, output, manifest)

    def test_symlink_or_reparse_source_is_rejected(self) -> None:
        link = self.skill / "references" / "linked.md"
        try:
            link.symlink_to(self.skill / "references" / "course-notes.md")
        except OSError as error:
            self.skipTest(f"symlink creation is unavailable: {error}")
        with self.assertRaisesRegex(builder.ProjectionError, "symlink or reparse point"):
            self.build()

    def test_hardlinked_capability_files_are_rejected(self) -> None:
        first = self.skill / "references" / "course-notes.md"
        second = self.skill / "references" / "workflow.md"
        second.unlink()
        try:
            os.link(first, second)
        except OSError as error:
            self.skipTest(f"hard-link creation is unavailable: {error}")
        with self.assertRaisesRegex(builder.ProjectionError, "hard-link identity"):
            self.build()

    def test_projected_tree_hash_recomputes_from_retained_bytes(self) -> None:
        result, output, _manifest = self.build()
        files = {
            path.relative_to(output).as_posix(): path.read_bytes()
            for path in output.rglob("*")
            if path.is_file()
        }
        self.assertEqual(result["projection_tree_sha256"], builder._tree_hash(files))
        files["SKILL.md"] += b"\n"
        self.assertNotEqual(result["projection_tree_sha256"], builder._tree_hash(files))

    def test_projection_verifier_rejects_unexpected_empty_directory(self) -> None:
        result, output, _manifest = self.build()
        (output / "unexpected-empty").mkdir()
        with self.assertRaisesRegex(builder.ProjectionError, "unexpected directory"):
            builder.verify_projection(output, result)

    def test_projection_verifier_rejects_root_symlink_or_junction(self) -> None:
        result, output, _manifest = self.build()
        alias = self.root / "projection-root-alias"
        if os.name == "nt":
            created = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(alias), str(output)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
                shell=False,
            )
            if created.returncode != 0:
                self.skipTest("Windows junction creation is unavailable")
        else:
            alias.symlink_to(output, target_is_directory=True)
        try:
            with self.assertRaisesRegex(
                builder.ProjectionError, "regular non-reparse directory"
            ):
                builder.verify_projection(alias, result)
        finally:
            alias.rmdir()

    def test_external_source_paths_are_inventory_only(self) -> None:
        result, output, _manifest = self.build()
        refs = result["declared_external_capability_refs"]
        self.assertEqual([], refs)
        original = json.loads(
            (self.skill / "references" / "corpus-action-sources.json").read_text(encoding="utf-8")
        )
        provisional_paths = {
            source["path"]
            for source in original["sources"]
            if source.get("role") == "positive_action_reference"
            and source.get("origin_class") == "UNKNOWN"
        }
        self.assertTrue(provisional_paths)
        self.assertTrue(set(refs).isdisjoint(provisional_paths))


if __name__ == "__main__":
    unittest.main()
