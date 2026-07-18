import csv
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SKILL = Path(
    os.environ.get(
        "HUMANIZE_SKILL_DIR",
        Path.home() / ".codex" / "skills" / "humanize-academic-chinese",
    )
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


preparer = load_module(
    "prepare_humanize_long_document",
    SKILL / "scripts" / "prepare_humanize_long_document.py",
)
finalizer = load_module(
    "finalize_humanize_long_document",
    SKILL / "scripts" / "finalize_humanize_long_document.py",
)
voice = finalizer.voice_profiles


class HumanizeDocumentStyleGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def records(before: list[str], after: list[str], *, scene: str = "RESEARCH") -> list[dict]:
        assert len(before) == len(after)
        return [
            {
                "unit_id": f"U-{index:02d}",
                "scene": scene,
                "expected": True,
                "state": "NO_CHANGE" if old == new else "DONE",
                "style_validation": "PASS",
                "before_masked": old,
                "after_masked": new,
            }
            for index, (old, new) in enumerate(zip(before, after), 1)
        ]

    @staticmethod
    def personal_profile() -> dict:
        code = "TEXT_OR_OBJECT_SUBJECT"
        extractor = voice.FEATURE_EXTRACTORS[code]
        extractor_sha256 = voice._stable_hash(
            {
                "rule_id": extractor["rule_id"],
                "pattern": extractor["pattern"].pattern,
                "flags": extractor["pattern"].flags,
                "code": code,
            }
        )
        return {
            "profile_kind": "PERSONAL",
            "profile_sha256": "a" * 64,
            "features": [
                {
                    "feature_key": "syntax.subject_position.text_or_object_subject",
                    "value": {"code": code},
                    "scope": ["RESEARCH"],
                    "disposition": "PREFER",
                    "evidence": {
                        "support_ratio_ppm": 1_000_000,
                        "extractor_sha256": extractor_sha256,
                    },
                }
            ],
            "negative_controls": [],
            "defaults": {"personal_voice_claim_allowed": True},
        }

    def test_personal_profile_no_change_passes_registered_feature_gate(self) -> None:
        paragraphs = [f"本文说明第{index}项内容。" for index in range(1, 7)]
        result = finalizer._audit_voice_conformance(
            self.personal_profile(),
            self.records(paragraphs, paragraphs),
            scene_routing_status="PASS",
        )

        self.assertEqual("PASS", result["status"])
        self.assertEqual("PERSONAL_PROFILE_NON_REGRESSION", result["basis"])
        self.assertFalse(result["identity_verified"])
        self.assertEqual(6, result["feature_results"][0]["after_support"])

    def test_personal_profile_material_subject_regression_is_reviewed(self) -> None:
        before = [f"本文说明第{index}项内容。" for index in range(1, 7)]
        after = [f"结果说明第{index}项内容。" for index in range(1, 7)]
        result = finalizer._audit_voice_conformance(
            self.personal_profile(),
            self.records(before, after),
            scene_routing_status="PASS",
        )

        self.assertEqual("REVIEW", result["status"])
        self.assertIn(
            result["feature_results"][0]["reason"],
            {"MATERIAL_PREFERRED_FEATURE_REGRESSION", "SEVERE_PROFILE_FEATURE_GAP"},
        )

    def test_personal_profile_short_target_does_not_claim_conformance(self) -> None:
        paragraphs = ["本文说明甲项。", "本文说明乙项。"]
        result = finalizer._audit_voice_conformance(
            self.personal_profile(),
            self.records(paragraphs, paragraphs),
            scene_routing_status="PASS",
        )

        self.assertEqual("REVIEW", result["status"])
        self.assertIn("INSUFFICIENT_TARGET_BLOCKS", result["review_reasons"])

    def test_cross_unit_repair_family_blocks_only_introduced_units(self) -> None:
        before = ["本段比较峰值。", "本段讨论误差。"]
        after = ["这里只比较峰值。", "这里只讨论误差。"]
        result = finalizer._audit_cross_unit_repetition(self.records(before, after))

        self.assertEqual("REVIEW", result["status"])
        self.assertEqual(["U-01", "U-02"], result["blocking_unit_ids"])
        self.assertIn(
            "LEX-REPAIR-01",
            {item.get("signal_id") for item in result["findings"]},
        )
        replay = finalizer._audit_cross_unit_repetition(self.records(before, after))
        self.assertEqual(
            [item["finding_fingerprint"] for item in result["findings"]],
            [item["finding_fingerprint"] for item in replay["findings"]],
        )
        self.assertEqual(result["blocking_unit_ids"], replay["blocking_unit_ids"])

    def test_inherited_cross_unit_repair_family_is_audited_but_not_blocked(self) -> None:
        paragraphs = ["这里只比较峰值。", "这里只讨论误差。"]
        result = finalizer._audit_cross_unit_repetition(
            self.records(paragraphs, paragraphs)
        )

        self.assertEqual("PASS", result["status"])
        self.assertEqual([], result["blocking_unit_ids"])
        self.assertGreaterEqual(result["inherited_finding_count"], 1)

    def test_protected_payload_is_absent_and_zero_width_cannot_bypass_gate(self) -> None:
        protected = "[[PROTECTED:P-001:0123456789ab]]"
        protected_result = finalizer._audit_cross_unit_repetition(
            self.records([protected, protected], [protected, protected])
        )
        self.assertEqual("PASS", protected_result["status"])
        self.assertEqual(0, protected_result["finding_count"])

        before = ["本段比较峰值。", "本段讨论误差。"]
        after = ["这\u200b里只比较峰值。", "这\u2060里只讨论误差。"]
        bypass_result = finalizer._audit_cross_unit_repetition(
            self.records(before, after)
        )
        self.assertEqual("REVIEW", bypass_result["status"])
        self.assertEqual(["U-01", "U-02"], bypass_result["blocking_unit_ids"])

    def test_registered_corpus_negative_guard_runs_across_units(self) -> None:
        before = ["甲项用于表面比较。", "乙项用于机制说明。"]
        after = ["这不是甲项而是乙项。", "这不是表面差异而是机制变化。"]
        result = finalizer._audit_cross_unit_repetition(self.records(before, after))

        self.assertEqual("REVIEW", result["status"])
        guard_findings = [
            item for item in result["findings"] if item["kind"] == "CORPUS_NEGATIVE_GUARD"
        ]
        self.assertIn(
            "NEGATIVE-TEMPLATE-01", {item["card_id"] for item in guard_findings}
        )
        self.assertRegex(result["action_catalog_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(result["action_profile_sha256"], r"^[0-9a-f]{64}$")

    def test_partial_scope_and_unavailable_negative_guard_cannot_pass(self) -> None:
        partial = self.records(["本段保持原样。"], ["本段保持原样。"])
        partial[0]["state"] = "PENDING"
        partial[0]["after_masked"] = None
        partial_result = finalizer._audit_cross_unit_repetition(partial)
        self.assertEqual("REVIEW", partial_result["status"])
        self.assertEqual("PARTIAL", partial_result["evaluation_scope"])

        unavailable_registry = {
            "status": "REVIEW",
            "guards": [
                {
                    "id": "NEGATIVE-TEMPLATE-UNAVAILABLE",
                    "scene": "ALL",
                    "status": "UNAVAILABLE",
                    "detector": {
                        "minimum_groups": 1,
                        "pattern_groups": [
                            {
                                "id": "shell",
                                "regex": "这里只",
                                "minimum_occurrences": 1,
                            }
                        ],
                    },
                },
            ],
            "registry_sha256": "1" * 64,
            "source_sha256": "2" * 64,
            "source_format": "TEST",
        }
        with mock.patch.object(
            finalizer.negative_guards,
            "load_negative_guard_registry",
            return_value=unavailable_registry,
        ):
            result = finalizer._audit_cross_unit_repetition(
                self.records(
                    ["本段保持原样。", "另一段保持原样。"],
                    ["本段保持原样。", "另一段保持原样。"],
                )
            )
        self.assertEqual("REVIEW", result["status"])
        self.assertIn(
            "NEGATIVE_GUARD_UNAVAILABLE:NEGATIVE-TEMPLATE-UNAVAILABLE",
            result["review_reasons"],
        )

    def test_negative_guard_registry_failure_is_review_not_silent_pass(self) -> None:
        with mock.patch.object(
            finalizer.negative_guards,
            "load_negative_guard_registry",
            side_effect=finalizer.negative_guards.NegativeGuardRegistryError("broken"),
        ):
            result = finalizer._audit_cross_unit_repetition(
                self.records(
                    ["甲段保持原样。", "乙段保持原样。"],
                    ["甲段保持原样。", "乙段保持原样。"],
                )
            )
        self.assertEqual("REVIEW", result["status"])
        self.assertEqual([], result["blocking_unit_ids"])
        self.assertIn(
            "NEGATIVE_GUARD_REGISTRY_UNAVAILABLE:NegativeGuardRegistryError",
            result["review_reasons"],
        )
        self.assertEqual("NOT_AVAILABLE", result["negative_guard_registry_status"])

    def test_finalizer_rolls_back_locally_valid_cross_unit_repair_templates(self) -> None:
        source = self.root / "main.tex"
        source.write_text(
            "\\section{甲}\n本段只比较峰值。\n\n"
            "\\section{乙}\n本段只讨论误差。\n",
            encoding="utf-8",
        )
        run_dir = self.root / "run"
        preparer.prepare([source], run_dir, scene="COURSE", min_author_chars=0)
        chunks = sorted(
            (
                json.loads(path.read_text(encoding="utf-8"))
                for path in (run_dir / "chunks").glob("*.json")
                if json.loads(path.read_text(encoding="utf-8"))["status"] == "PENDING"
            ),
            key=lambda item: int(item["start"]),
        )
        self.assertEqual(2, len(chunks))
        rewrites = self.root / "rewrites"
        rewrites.mkdir()
        replacements = (
            ("本段只比较峰值。", "这里只比较峰值。"),
            ("本段只讨论误差。", "这里只讨论误差。"),
        )
        for unit, (old, new) in zip(chunks, replacements):
            payload = {
                "unit_id": unit["unit_id"],
                "chunk_binding_sha256": unit["chunk_binding_sha256"],
                "voice_profile_sha256": unit["voice_profile_sha256"],
                "decision": "REWRITE",
                "masked_text": unit["masked_text"].replace(old, new),
                "keep_reasons": {},
            }
            (rewrites / f"{unit['unit_id']}.json").write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )

        result = finalizer.finalize(run_dir, rewrites)
        with (run_dir / "coverage_ledger.final.csv").open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            ledger = list(csv.DictReader(handle))

        self.assertEqual("REVIEW", result["status"])
        self.assertEqual("REVIEW", result["cross_unit_repetition_status"])
        self.assertEqual(
            {"UNRESOLVED"},
            {row["status"] for row in ledger if row["unit_id"] in result["cross_unit_repetition"]["blocking_unit_ids"]},
        )
        self.assertFalse(result["coverage_completion_claim_allowed"])
        self.assertFalse(result["humanize_completion_claim_allowed"])
        rendered = next((run_dir / "rendered_partial").rglob("*.tex")).read_text(
            encoding="utf-8"
        )
        self.assertNotIn("这里只", rendered)
        self.assertTrue((run_dir / "validation" / "cross_unit_repetition.json").is_file())


if __name__ == "__main__":
    unittest.main()
