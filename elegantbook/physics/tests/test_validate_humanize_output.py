import importlib.util
import html
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(
    os.environ.get(
        "HUMANIZE_SKILL_DIR",
        Path.home() / ".codex" / "skills" / "humanize-academic-chinese",
    )
)
SCRIPT = SKILL / "scripts" / "validate_humanize_output.py"
FORWARD_FIXTURES = Path(__file__).parent / "fixtures" / "humanize_forward_v3"
FORWARD_V4_FIXTURES = Path(__file__).parent / "fixtures" / "humanize_forward_v4"
GOLD_FIXTURES = Path(__file__).parent / "fixtures" / "humanize_gold"
FORWARD_V5_FIXTURES = Path(__file__).parent / "fixtures" / "humanize_forward_v5"
FORWARD_V10_FIXTURES = Path(__file__).parent / "fixtures" / "humanize_forward_v10"
SPEC = importlib.util.spec_from_file_location("validate_humanize_output", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class HumanizeOutputValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def pair(self, before: str, after: str, suffix: str = ".md") -> tuple[Path, Path]:
        before_path = self.root / f"before{suffix}"
        after_path = self.root / f"after{suffix}"
        before_path.write_text(before, encoding="utf-8")
        after_path.write_text(after, encoding="utf-8")
        return before_path, after_path

    def report_scope(self, source: Path, selections: list[str]) -> Path:
        source_text = source.read_bytes().decode("utf-8-sig")
        for selection in selections:
            self.assertEqual(1, source_text.count(selection))
        report = self.root / "report.html"
        report.write_text(
            '<!doctype html><html><meta charset="utf-8"><body>'
            + "".join(f"<mark>{html.escape(selection)}</mark>" for selection in selections)
            + "</body></html>",
            encoding="utf-8",
        )
        payload = validator.detector_scope.analyze_report(report, source)
        self.assertEqual("PASS", payload["status"])
        path = self.root / "report-scope.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def assert_paired_quality_review(
        self,
        payload: dict,
        *,
        decision: str,
        changes: int | None = None,
    ) -> dict:
        self.assertEqual("REVIEW", payload["status"])
        self.assertEqual(2, payload["exit_code"])
        self.assertEqual("PASS", payload["candidate_assembly_status"])
        self.assertEqual("PASS", payload["mechanical_validation_status"])
        self.assertEqual("REVIEW", payload["delivery_gate_status"])
        self.assertEqual("PENDING_EXTERNAL_REVIEW", payload["paired_quality_review_status"])
        self.assertFalse(payload["paired_quality_clearance_granted"])
        self.assertFalse(payload["humanize_quality_claim_allowed"])
        self.assertIn("paired_quality_not_evaluated", payload["review_reasons"])
        request = payload["paired_quality_review_request"]
        self.assertEqual("humanize-paired-quality-review-request/v1", request["schema"])
        self.assertEqual(decision, request["validation_context"]["decision"])
        self.assertRegex(request["request_sha256"], r"^[0-9a-f]{64}$")
        if changes is not None:
            self.assertEqual(changes, len(request["changes"]))
        return request

    def test_safe_rewrite_passes_with_hash_evidence(self) -> None:
        before, after = self.pair("值得注意的是，峰值出现在高温组。", "峰值出现在高温组。")
        payload = validator.validate(before, after, scene="RESEARCH")
        self.assert_paired_quality_review(payload, decision="REWRITE", changes=1)
        self.assertEqual("PASS", payload["hard_invariant_layer_status"])
        self.assertEqual("PASS", payload["speech_act_layer_status"])
        self.assertEqual("PASS", payload["style_signal_layer_status"])
        self.assertEqual("NOT_EVALUATED", payload["academic_correctness"])
        self.assertTrue(payload["evidence"]["checker_executed"])
        self.assertRegex(payload["evidence"]["before_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual("NOT_PROVIDED", payload["evidence"]["protected_terms"]["status"])
        self.assertEqual("DOCUMENT", payload["evidence"]["document_scope"])

    def test_v24_unseen_collocation_cannot_receive_false_delivery_pass(self) -> None:
        before, after = self.pair(
            "这类题看上去在测长度，其实真正要写的是厚度怎样增长。",
            "这类题测的是长度，但求解先要确定厚度怎样增长。",
        )

        payload = validator.validate(before, after, scene="COURSE")
        request = self.assert_paired_quality_review(
            payload, decision="REWRITE", changes=1
        )

        self.assertEqual("PASS", payload["hard_invariant_layer_status"])
        self.assertEqual("PASS", payload["speech_act_layer_status"])
        self.assertEqual("PASS", payload["style_signal_layer_status"])
        self.assertEqual(1, len(request["changes"]))
        self.assertFalse(
            request["review_contract"]["validator_pass_is_quality_clearance"]
        )

    def test_no_change_is_bound_for_external_quality_review(self) -> None:
        before, after = self.pair("该段表面自然，但仍可能存在未识别病灶。", "该段表面自然，但仍可能存在未识别病灶。")

        first = validator.validate(before, after, scene="GENERAL")
        second = validator.validate(before, after, scene="GENERAL")
        first_request = self.assert_paired_quality_review(
            first, decision="NO_CHANGE", changes=0
        )
        second_request = self.assert_paired_quality_review(
            second, decision="NO_CHANGE", changes=0
        )

        self.assertEqual(
            first_request["request_sha256"], second_request["request_sha256"]
        )
        self.assertIn(
            "no_change_is_best_available_decision",
            first_request["review_contract"]["required_dimensions"],
        )

    def test_paired_quality_hunks_preserve_eol_only_changes(self) -> None:
        before, after = self.pair("第一行。\r\n第二行。\r\n", "第一行。\n第二行。\n")
        before.write_bytes("第一行。\r\n第二行。\r\n".encode("utf-8"))
        after.write_bytes("第一行。\n第二行。\n".encode("utf-8"))

        payload = validator.validate(before, after, scene="GENERAL")
        request = self.assert_paired_quality_review(
            payload, decision="REWRITE", changes=1
        )

        change = request["changes"][0]
        self.assertEqual("REPLACE", change["operation"])
        self.assertNotEqual(
            change["before"]["sha256"], change["after"]["sha256"]
        )

    def test_paired_quality_hunks_preserve_bom_only_changes(self) -> None:
        before, after = self.pair("同一正文。", "同一正文。")
        before.write_bytes(b"\xef\xbb\xbf" + "同一正文。".encode("utf-8"))
        after.write_bytes("同一正文。".encode("utf-8"))

        payload = validator.validate(before, after, scene="GENERAL")
        request = self.assert_paired_quality_review(
            payload, decision="REWRITE", changes=1
        )

        self.assertNotEqual(
            request["artifact"]["before_sha256"],
            request["artifact"]["after_sha256"],
        )

    def test_paired_quality_hunks_preserve_trailing_newline_changes(self) -> None:
        before, after = self.pair("同一正文。\n", "同一正文。")
        before.write_bytes("同一正文。\n".encode("utf-8"))
        after.write_bytes("同一正文。".encode("utf-8"))

        payload = validator.validate(before, after, scene="GENERAL")
        request = self.assert_paired_quality_review(
            payload, decision="REWRITE", changes=1
        )

        self.assertEqual("REPLACE", request["changes"][0]["operation"])

    def test_paired_quality_request_binds_policy_hashes(self) -> None:
        before, after = self.pair("原句表述稍长。", "原句较长。")
        baseline = validator.validate(before, after, scene="GENERAL")
        baseline_request = baseline["paired_quality_review_request"]
        with mock.patch.object(
            validator,
            "_policy_hashes",
            return_value={
                "validator_sha256": "1" * 64,
                "invariant_checker_sha256": "2" * 64,
                "scanner_sha256": "3" * 64,
                "lexicon_sha256": "4" * 64,
            },
        ):
            drifted = validator.validate(before, after, scene="GENERAL")

        self.assertNotEqual(
            baseline_request["request_sha256"],
            drifted["paired_quality_review_request"]["request_sha256"],
        )

    def test_mechanical_failure_blocks_quality_review_instead_of_masking_failure(self) -> None:
        before, after = self.pair("公式为 $x=1$。", "公式为 $x=2$。", suffix=".tex")

        payload = validator.validate(before, after, scene="GENERAL")

        self.assertEqual("FAIL", payload["status"])
        self.assertEqual("FAIL", payload["mechanical_validation_status"])
        self.assertEqual("BLOCKED_BY_MECHANICAL_GATE", payload["paired_quality_review_status"])
        self.assertEqual(
            "BLOCKED_BY_MECHANICAL_GATE",
            payload["paired_quality_review_request"]["status"],
        )

    def test_fragment_scope_is_explicit_and_does_not_hide_structure_drift(self) -> None:
        before, after = self.pair(
            "\\begin{document}\n值得注意的是，结论保持不变。\n",
            "\\begin{document}\n结论保持不变。\n",
            suffix=".tex",
        )
        payload = validator.validate(
            before,
            after,
            scene="RESEARCH",
            fragment_mode=True,
        )
        self.assert_paired_quality_review(payload, decision="REWRITE", changes=1)
        self.assertEqual("FRAGMENT", payload["evidence"]["document_scope"])
        self.assertEqual("FRAGMENT", payload["invariants"]["evidence"]["document_scope"])

        after.write_text("结论保持不变。\n", encoding="utf-8")
        drifted = validator.validate(
            before,
            after,
            scene="RESEARCH",
            fragment_mode=True,
        )
        self.assertEqual("FAIL", drifted["status"])
        self.assertEqual("FAIL", drifted["hard_invariant_layer_status"])

        with self.assertRaisesRegex(ValueError, "only valid for REWRITE"):
            validator.validate(before, after, mode="DRAFT", fragment_mode=True)

    def test_draft_mode_uses_supply_surface_gate_and_never_claims_semantic_pass(self) -> None:
        supplied, draft = self.pair(
            "# 写作要点\n\n- 2025 年共三组数据。\n- 材料没有提供原因。\n",
            "2025 年共三组数据。\n",
        )

        payload = validator.validate(supplied, draft, mode="DRAFT", scene="GENERAL")

        self.assertEqual("DRAFT", payload["mode"])
        self.assertEqual("PASS", payload["hard_invariant_layer_status"])
        self.assertEqual("PASS", payload["draft_surface_source_check"]["status"])
        self.assertEqual("NOT_EVALUATED", payload["semantic_source_check"])
        self.assertEqual("REVIEW", payload["status"])
        self.assertIn("semantic_source_not_evaluated", payload["review_reasons"])
        self.assertFalse(
            any(
                item["code"] == "SPEECH_ACT_NEGATION_CHANGED"
                for item in payload["unaccepted_warnings"]
            )
        )

    def test_draft_mode_rejects_number_not_present_in_supplied_content(self) -> None:
        supplied, draft = self.pair(
            "材料记录了三组数据，共 3 组。\n",
            "材料记录了四组数据，共 4 组。\n",
        )

        payload = validator.validate(supplied, draft, mode="DRAFT", scene="GENERAL")

        self.assertEqual("FAIL", payload["status"])
        self.assertEqual("FAIL", payload["hard_invariant_layer_status"])
        self.assertEqual("FAIL", payload["draft_surface_source_check"]["status"])
        self.assertIn(
            "DRAFT_NUMBER_OR_UNIT_NOT_SUPPLIED",
            {item["code"] for item in payload["invariants"]["errors"]},
        )

    def test_draft_mode_rejects_new_attribution_shell(self) -> None:
        supplied, draft = self.pair(
            "材料记录了三组数据，共 3 组。\n",
            "已有研究表明，材料记录了三组数据，共 3 组。\n",
        )

        payload = validator.validate(supplied, draft, mode="DRAFT", scene="GENERAL")

        self.assertEqual("FAIL", payload["status"])
        self.assertIn(
            "DRAFT_ATTRIBUTION_NOT_SUPPLIED",
            {item["code"] for item in payload["invariants"]["errors"]},
        )

    def test_draft_mode_reuses_supplied_surface_values_without_occurrence_budget(self) -> None:
        cases = (
            ("code", "材料给出 `alpha()`。", "先运行 `alpha()`，再核对 `alpha()`。", ".md", ()),
            ("math", r"材料给出 \(x=y\)。", r"先使用 \(x=y\)，再由 \(x=y\) 展开。", ".tex", ()),
            (
                "formal",
                "\\begin{theorem}\n命题甲成立。\n\\end{theorem}\n",
                "\\begin{theorem}\n命题甲成立。\n\\end{theorem}\n\n"
                "\\begin{theorem}\n命题甲成立。\n\\end{theorem}\n",
                ".tex",
                (),
            ),
            (
                "command",
                r"材料引用 \cite{sourceA}。",
                r"依据 \cite{sourceA}，并参见 \cite{sourceA}。",
                ".tex",
                (),
            ),
            (
                "quotation",
                "材料原句为“边界保持不变”。",
                "“边界保持不变”；换言之，仍是“边界保持不变”。",
                ".md",
                (),
            ),
            ("garbled", "OCR： �字 。", "记录为 �字 。再次记录为 �字 。", ".md", ()),
            (
                "term",
                "本文采用有限元法。",
                "有限元法用于求解；有限元法保持不变。",
                ".md",
                ("有限元法", "谱方法"),
            ),
        )
        for name, supplied_text, draft_text, suffix, terms in cases:
            with self.subTest(name=name):
                supplied, draft = self.pair(supplied_text, draft_text, suffix=suffix)
                payload = validator.validate(
                    supplied,
                    draft,
                    mode="DRAFT",
                    scene="GENERAL",
                    protected_terms=terms,
                )
                self.assertEqual("PASS", payload["draft_surface_source_check"]["status"])
                self.assertEqual("PASS", payload["hard_invariant_layer_status"])
                self.assertEqual("NOT_EVALUATED", payload["semantic_source_check"])
                self.assertEqual("REVIEW", payload["status"])
                self.assertEqual(2, payload["exit_code"])

    def test_draft_mode_still_rejects_new_surface_values(self) -> None:
        cases = (
            ("code", "材料给出 `alpha()`。", "材料给出 `beta()`。", ".md", (), "DRAFT_CODE_NOT_SUPPLIED"),
            ("math", r"材料给出 \(x=y\)。", r"材料给出 \(x=z\)。", ".tex", (), "DRAFT_MATH_NOT_SUPPLIED"),
            (
                "formal",
                "\\begin{theorem}\n命题甲成立。\n\\end{theorem}\n",
                "\\begin{theorem}\n命题乙成立。\n\\end{theorem}\n",
                ".tex",
                (),
                "DRAFT_FORMAL_STATEMENT_NOT_SUPPLIED",
            ),
            (
                "command",
                r"材料引用 \cite{sourceA}。",
                r"材料引用 \cite{sourceB}。",
                ".tex",
                (),
                "DRAFT_CRITICAL_COMMAND_NOT_SUPPLIED",
            ),
            (
                "quotation",
                "材料原句为“边界保持不变”。",
                "材料原句为“边界已经改变”。",
                ".md",
                (),
                "DRAFT_QUOTATION_NOT_SUPPLIED",
            ),
            ("garbled", "OCR： �字 。", "记录为 �词 。", ".md", (), "DRAFT_GARBLED_TEXT_NOT_SUPPLIED"),
            (
                "term",
                "本文采用有限元法。",
                "本文采用谱方法。",
                ".md",
                ("有限元法", "谱方法"),
                "DRAFT_PROTECTED_TERM_NOT_SUPPLIED",
            ),
        )
        for name, supplied_text, draft_text, suffix, terms, error_code in cases:
            with self.subTest(name=name):
                supplied, draft = self.pair(supplied_text, draft_text, suffix=suffix)
                payload = validator.validate(
                    supplied,
                    draft,
                    mode="DRAFT",
                    scene="GENERAL",
                    protected_terms=terms,
                )
                self.assertEqual("FAIL", payload["status"])
                self.assertEqual(1, payload["exit_code"])
                self.assertIn(error_code, {item["code"] for item in payload["invariants"]["errors"]})

    def test_draft_mode_realistic_result_and_discussion_can_reuse_math(self) -> None:
        supplied, draft = self.pair(
            "将人工放流项置为 \\(R_S=0\\) 时，长江鲟末值为 0.519。\n",
            "将人工放流项置为 \\(R_S=0\\) 时，长江鲟末值为 0.519。\n\n"
            "讨论中，\\(R_S=0\\) 对照用于拆分人工放流补偿效应。\n",
            suffix=".tex",
        )
        payload = validator.validate(supplied, draft, mode="DRAFT", scene="MODELING")
        self.assertEqual("PASS", payload["draft_surface_source_check"]["status"])
        self.assertEqual("REVIEW", payload["status"])
        self.assertNotIn(
            "DRAFT_MATH_NOT_SUPPLIED",
            {item["code"] for item in payload["invariants"]["errors"]},
        )

    def test_rewrite_math_occurrence_protection_is_unchanged(self) -> None:
        before, after = self.pair(
            "模型使用 \\(x=y\\)。",
            "模型使用 \\(x=y\\)，并再次使用 \\(x=y\\)。",
            suffix=".tex",
        )
        payload = validator.validate(before, after, mode="REWRITE", scene="GENERAL")
        self.assertEqual("FAIL", payload["status"])
        self.assertIn(
            "PROTECTED_MATH_CHANGED",
            {item["code"] for item in payload["invariants"]["errors"]},
        )

    def test_report_scope_binds_rewrite_to_unique_selection_ranges(self) -> None:
        before, after = self.pair(
            "开头保持。\n\n标注一表述生硬。\n\n中间保持。\n\n标注二表述冗长。\n\n结尾保持。\n",
            "开头保持。\n\n标注一表述自然。\n\n中间保持。\n\n标注二更加简洁。\n\n结尾保持。\n",
        )
        scope = self.report_scope(before, ["标注一表述生硬。", "标注二表述冗长。"])
        payload = validator.validate(before, after, scene="GENERAL", report_scope_path=scope)
        self.assert_paired_quality_review(payload, decision="REWRITE", changes=2)
        self.assertEqual("PASS", payload["report_scope_check"]["status"])
        self.assertTrue(payload["report_scope_check"]["outside_selection_unchanged"])
        self.assertTrue(payload["report_scope_check"]["extractor_replay_match"])
        self.assertEqual(2, payload["report_scope_check"]["editable_range_count"])
        self.assertEqual("REPORT_SELECTION", payload["evidence"]["document_scope"])

    def test_report_scope_rejects_change_outside_selection_even_when_other_gates_pass(self) -> None:
        before, after = self.pair(
            "开头保持。\n\n标注段表述生硬。\n\n结尾保持。\n",
            "开头内容改变。\n\n标注段表述自然。\n\n结尾保持。\n",
        )
        scope = self.report_scope(before, ["标注段表述生硬。"])
        payload = validator.validate(before, after, scene="GENERAL", report_scope_path=scope)
        self.assertEqual("FAIL", payload["status"])
        self.assertEqual("FAIL", payload["report_scope_check"]["status"])
        self.assertFalse(payload["report_scope_check"]["outside_selection_unchanged"])
        self.assertIn(
            "REPORT_SCOPE_OUTSIDE_SELECTION_CHANGED",
            {item["code"] for item in payload["invariants"]["errors"]},
        )

    def test_report_scope_rejects_stale_source_hash(self) -> None:
        before, after = self.pair("标注段需要改写。", "标注段改得自然。")
        scope = self.report_scope(before, ["标注段需要改写。"])
        scope_payload = json.loads(scope.read_text(encoding="utf-8"))
        scope_payload["source_sha256"] = "0" * 64
        scope.write_text(json.dumps(scope_payload), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "source_sha256"):
            validator.validate(before, after, scene="GENERAL", report_scope_path=scope)

    def test_report_scope_rejects_forged_ranges_that_do_not_replay_from_report(self) -> None:
        before, after = self.pair(
            "开头保持。\n\n标注段表述生硬。\n\n结尾保持。\n",
            "开头保持。\n\n标注段表述自然。\n\n结尾保持。\n",
        )
        scope = self.report_scope(before, ["标注段表述生硬。"])
        scope_payload = json.loads(scope.read_text(encoding="utf-8"))
        scope_payload["fragments"][0]["source_start"] = 0
        scope_payload["fragments"][0]["source_end"] = len(before.read_text(encoding="utf-8"))
        scope.write_text(json.dumps(scope_payload, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "extractor replay"):
            validator.validate(before, after, scene="GENERAL", report_scope_path=scope)

    def test_unexplained_high_signal_requires_review(self) -> None:
        before, after = self.pair("这张表必须牢记。", "这张表必须牢记。")
        payload = validator.validate(before, after, scene="COURSE")
        self.assertEqual("REVIEW", payload["status"])
        self.assertEqual(2, payload["exit_code"])
        self.assertEqual("PASS", payload["hard_invariant_layer_status"])
        self.assertEqual("PASS", payload["speech_act_layer_status"])
        self.assertEqual("REVIEW", payload["style_signal_layer_status"])
        self.assertEqual("REVIEW", payload["delivery_gate_status"])
        self.assertEqual(1, payload["lexical_summary"]["unexplained_high_candidates"])

    def test_v19_closed_loop_and_abstract_path_shell_cannot_silently_pass(self) -> None:
        cases = (
            (
                "本问按参数设定、校准和反事实对照的实证闭环收紧。",
                "RESEARCH",
            ),
            (
                "问题二的证据关系由禁渔和食源恢复出发，经通道与污染修正，最终落到种群变化。",
                "MODELING",
            ),
        )
        for text, scene in cases:
            with self.subTest(scene=scene):
                before, after = self.pair(text, text)
                payload = validator.validate(before, after, scene=scene)
                ids = {item["signal_id"] for item in payload["unexplained_high_findings"]}
                self.assertEqual("REVIEW", payload["delivery_gate_status"])
                self.assertEqual(2, payload["delivery_gate_exit_code"])
                self.assertIn("LEX-MGMT-01", ids)

    def test_explicit_keep_reason_can_clear_a_surface_hit(self) -> None:
        before, after = self.pair("这张表必须牢记。", "这张表必须牢记。")
        payload = validator.validate(
            before,
            after,
            scene="COURSE",
            keep_reasons={"LEX-COACH-01": "用户锁定的课程原句"},
        )
        self.assert_paired_quality_review(payload, decision="NO_CHANGE", changes=0)
        self.assertEqual(1, len(payload["accepted_findings"]))
        self.assertRegex(payload["accepted_findings"][0]["finding_hash"], r"^[0-9a-f]{64}$")

    def test_introduced_repair_template_requires_review(self) -> None:
        before, after = self.pair(
            "峰值用于比较。误差用于比较。",
            "这里只看峰值。这里只比较误差。",
        )
        payload = validator.validate(before, after, scene="GENERAL")
        ids = {item["signal_id"] for item in payload["introduced_findings"]}
        self.assertEqual("REVIEW", payload["status"])
        self.assertIn("LEX-REPAIR-01", ids)

    def test_speech_act_warning_requires_review(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        payload = validator.validate(before, after, scene="GENERAL")
        self.assertEqual("REVIEW", payload["status"])
        self.assertEqual("PASS", payload["hard_invariant_layer_status"])
        self.assertEqual("REVIEW", payload["speech_act_layer_status"])
        self.assertEqual("PASS", payload["style_signal_layer_status"])
        self.assertEqual("REVIEW", payload["delivery_gate_status"])
        self.assertIn("speech_act_warning", payload["review_reasons"])
        request = payload["warning_review_request"]
        self.assertIsNotNone(request)
        self.assertRegex(request["request_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(1, len(request["warnings"]))
        self.assertRegex(
            request["warnings"][0]["warning_fingerprint"],
            r"^[0-9a-f]{64}$",
        )
        self.assertEqual(payload["evidence"]["before_sha256"], request["artifact"]["before_sha256"])
        self.assertEqual(payload["evidence"]["after_sha256"], request["artifact"]["after_sha256"])
        self.assertEqual("GENERAL", request["validation_context"]["scene"])
        self.assertEqual("markdown", request["validation_context"]["document_format"])
        self.assertEqual(
            payload["evidence"]["protected_terms"],
            request["validation_context"]["protected_terms"],
        )
        self.assertEqual(
            {
                "validator_sha256",
                "invariant_checker_sha256",
                "scanner_sha256",
                "lexicon_sha256",
                "report_extractor_sha256",
                "runtime_contract_sha256",
            },
            set(request["policy_hashes"]),
        )
        for policy_hash in request["policy_hashes"].values():
            self.assertRegex(policy_hash, r"^[0-9a-f]{64}$")

    def test_v19_focus_scope_loss_requires_review(self) -> None:
        before, after = self.pair(
            "本问的重点不是比较两个物种的绝对值，而是考察政策收益的保留程度。",
            "本问不比较两个物种的绝对值，而是考察政策收益的保留程度。",
        )
        payload = validator.validate(before, after, scene="MODELING")

        self.assertEqual("REVIEW", payload["delivery_gate_status"])
        self.assertIn(
            "SPEECH_ACT_FOCUS_SCOPE_CHANGED",
            {item["code"] for item in payload["unaccepted_warnings"]},
        )

    def test_v7_modeling_false_pass_is_blocked_by_transition_and_outlook_gates(self) -> None:
        before, after = self.pair(
            "本文构建模型。表格的作用在于统一实验口径，正文里要保留 20 ℃、25 ℃ 和 30 ℃ 三组数据。"
            "该模型形成了从数据到决策的完整闭环，为工程应用提供有力支撑。"
            "模型可能在一定程度上或许仍会受到传感器漂移影响，因此后续工作可以进一步拓展应用场景。",
            "本文构建模型。表格列出 20 ℃、25 ℃ 和 30 ℃ 三组数据，以统一实验口径。"
            "该模型将参数扫描结果用于工程决策，为工程应用提供依据。"
            "传感器漂移可能影响模型，影响程度或许有限。应用场景可以进一步拓展。",
        )
        payload = validator.validate(before, after, scene="MODELING")
        warning_codes = {item["code"] for item in payload["unaccepted_warnings"]}

        self.assertEqual("REVIEW", payload["delivery_gate_status"])
        self.assertIn("SPEECH_ACT_DIRECTIVE_TO_COMPLETION", warning_codes)
        self.assertIn("SPEECH_ACT_SUPPORT_TO_ACTUAL_USE", warning_codes)
        self.assertIn("SPEECH_ACT_MODALITY_TO_DEGREE", warning_codes)
        self.assertIn(
            "LEX-FUTURE-01",
            {item["signal_id"] for item in payload["introduced_findings"]},
        )

    def test_v7_course_coaching_synonym_cannot_pass(self) -> None:
        before, after = self.pair(
            "遇到这类题目时必须牢记公式。",
            "遇到这类题目，公式必须记清楚。",
        )
        payload = validator.validate(before, after, scene="COURSE")

        self.assertEqual("REVIEW", payload["delivery_gate_status"])
        self.assertIn(
            "LEX-COACH-01",
            {item["signal_id"] for item in payload["unexplained_high_findings"]},
        )

    def test_v8_memory_synonym_and_editor_note_cannot_pass(self) -> None:
        course_before, course_after = self.pair(
            "遇到这类题目时必须牢记公式。",
            "遇到这类题，公式需要记住。",
        )
        course = validator.validate(course_before, course_after, scene="COURSE")
        self.assertEqual("REVIEW", course["delivery_gate_status"])
        self.assertIn(
            "LEX-COACH-01",
            {item["signal_id"] for item in course["unexplained_high_findings"]},
        )

        modeling_before, modeling_after = self.pair(
            "正文里要保留 20 ℃、25 ℃ 和 30 ℃ 三组数据。",
            "20 ℃、25 ℃ 和 30 ℃ 三组数据仍需在正文中保留。",
        )
        modeling = validator.validate(modeling_before, modeling_after, scene="MODELING")
        self.assertEqual("REVIEW", modeling["delivery_gate_status"])
        self.assertIn(
            "LEX-META-01",
            {item["signal_id"] for item in modeling["unexplained_high_findings"]},
        )

    def test_v10_course_real_forward_deletes_coaching_shell_without_false_pass(self) -> None:
        payload = validator.validate(
            FORWARD_V10_FIXTURES / "course_before.tex",
            FORWARD_V10_FIXTURES / "course_after.tex",
            scene="COURSE",
        )
        self.assertEqual("REVIEW", payload["delivery_gate_status"])
        self.assertEqual("PASS", payload["hard_invariant_layer_status"])
        self.assertEqual("PASS", payload["style_signal_layer_status"])
        self.assertEqual(0, payload["lexical_summary"]["after_candidates"])
        self.assertIn(
            "SPEECH_ACT_MODALITY_SCOPE_CHANGED",
            {item["code"] for item in payload["unaccepted_warnings"]},
        )

    def test_v10_modeling_real_forward_recovers_payload_without_predicate_upgrade(self) -> None:
        payload = validator.validate(
            FORWARD_V10_FIXTURES / "modeling_before.md",
            FORWARD_V10_FIXTURES / "modeling_after.md",
            scene="MODELING",
        )
        warning_codes = {item["code"] for item in payload["unaccepted_warnings"]}
        self.assertEqual("REVIEW", payload["delivery_gate_status"])
        self.assertEqual("PASS", payload["hard_invariant_layer_status"])
        self.assertEqual("PASS", payload["style_signal_layer_status"])
        self.assertEqual(0, payload["lexical_summary"]["after_candidates"])
        self.assertIn("SPEECH_ACT_MODALITY_SCOPE_CHANGED", warning_codes)
        self.assertFalse(
            {
                "SPEECH_ACT_DIRECTIVE_TO_COMPLETION",
                "SPEECH_ACT_SUPPORT_TO_ACTUAL_USE",
                "SPEECH_ACT_MODALITY_TO_DEGREE",
            }
            & warning_codes
        )

    def test_v10_research_real_forward_passes_all_three_layers(self) -> None:
        payload = validator.validate(
            FORWARD_V10_FIXTURES / "research_before.md",
            FORWARD_V10_FIXTURES / "research_after.md",
            scene="RESEARCH",
        )
        self.assert_paired_quality_review(payload, decision="REWRITE")
        self.assertEqual("PASS", payload["hard_invariant_layer_status"])
        self.assertEqual("PASS", payload["speech_act_layer_status"])
        self.assertEqual("PASS", payload["style_signal_layer_status"])
        self.assertEqual(0, payload["lexical_summary"]["after_candidates"])

    def test_warning_review_request_and_fingerprints_are_deterministic(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        first = validator.validate(before, after, scene="GENERAL", protected_terms=["结果"])
        second = validator.validate(before, after, scene="GENERAL", protected_terms=["结果"])

        self.assertEqual(
            first["warning_review_request"]["request_sha256"],
            second["warning_review_request"]["request_sha256"],
        )
        self.assertEqual(
            first["warning_review_request"]["warnings"],
            second["warning_review_request"]["warnings"],
        )

    def test_attribution_source_upgrade_cannot_silently_pass(self) -> None:
        before, after = self.pair(
            "专家认为，该方法在低频组更稳定。",
            "本文证实，该方法在低频组更稳定。",
        )
        payload = validator.validate(before, after, scene="RESEARCH")
        warning_codes = {item["code"] for item in payload["unaccepted_warnings"]}
        self.assertEqual("REVIEW", payload["status"])
        self.assertEqual(2, payload["exit_code"])
        self.assertIn("SPEECH_ACT_ATTRIBUTION_SOURCE_CHANGED", warning_codes)

    def test_new_literature_background_cannot_silently_pass(self) -> None:
        before, after = self.pair(
            "本文结合问题背景和实验现象讨论可能机制。",
            "本文结合问题背景、实验现象和已有研究讨论可能机制。",
        )
        payload = validator.validate(before, after, scene="RESEARCH")
        warning_codes = {item["code"] for item in payload["unaccepted_warnings"]}

        self.assertEqual("REVIEW", payload["status"])
        self.assertEqual(2, payload["exit_code"])
        self.assertIn("SPEECH_ACT_ATTRIBUTION_SOURCE_CHANGED", warning_codes)

    def test_unverified_caller_proposal_never_clears_warning(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        first = validator.validate(before, after, scene="GENERAL")
        request = first["warning_review_request"]
        fingerprint = request["warnings"][0]["warning_fingerprint"]
        payload = validator.validate(
            before,
            after,
            scene="GENERAL",
            warning_resolutions={
                fingerprint: "调用方建议恢复原句中的模态范围以保留结论强度",
            },
            warning_review_request_sha256=request["request_sha256"],
        )
        self.assertEqual("REVIEW", payload["status"])
        self.assertEqual(2, payload["exit_code"])
        self.assertEqual("REVIEW", payload["speech_act_layer_status"])
        self.assertEqual([], payload["accepted_warnings"])
        self.assertEqual(1, len(payload["unaccepted_warnings"]))
        self.assertEqual(1, len(payload["proposed_warning_resolutions"]))
        self.assertEqual(1, len(payload["pending_warnings"]))
        self.assertEqual([], payload["warnings_without_resolution_proposal"])
        self.assertFalse(payload["proposed_warning_resolutions"][0]["review_clearance_granted"])
        proposal = payload["warning_proposal_state"]
        self.assertEqual("UNVERIFIED_CALLER_PROPOSAL", proposal["proposal_source"])
        self.assertFalse(proposal["reviewer_identifier_collected"])
        self.assertFalse(proposal["identity_verified"])
        self.assertFalse(proposal["review_clearance_granted"])
        self.assertEqual(
            "NOT_APPLICABLE",
            proposal["attestation_status"],
        )
        self.assertNotIn("warning_review", payload)

    def test_retired_accepted_warnings_are_explicitly_rejected(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        with self.assertRaisesRegex(ValueError, "accepted_warnings/--accept-warning is retired"):
            validator.validate(
                before,
                after,
                accepted_warnings={
                    "SPEECH_ACT_MODALITY_SCOPE_CHANGED": "人工确认该模态变化不影响原句表达功能",
                },
                warning_reviewer_kind="HUMAN",
                warning_reviewer_id="external-reviewer",
            )

    def test_reviewer_identity_metadata_is_retired(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        first = validator.validate(before, after)
        request = first["warning_review_request"]
        fingerprint = request["warnings"][0]["warning_fingerprint"]
        with self.assertRaisesRegex(ValueError, "identity metadata is retired"):
            validator.validate(
                before,
                after,
                warning_resolutions={
                    fingerprint: "模型建议恢复原句中的模态范围以保留表达功能",
                },
                warning_review_request_sha256=request["request_sha256"],
                warning_reviewer_kind="AGENT",
                warning_reviewer_id="forward-agent",
            )

    def test_retired_identity_or_request_without_proposal_is_rejected(self) -> None:
        before, after = self.pair("结果保持稳定。", "结果保持稳定。")
        with self.assertRaisesRegex(ValueError, "identity metadata is retired"):
            validator.validate(
                before,
                after,
                warning_reviewer_kind="HUMAN",
                warning_reviewer_id="external-reviewer",
            )
        with self.assertRaisesRegex(ValueError, "hash is only valid with warning_resolutions"):
            validator.validate(
                before,
                after,
                warning_review_request_sha256="0" * 64,
            )

    def test_all_warning_reviewer_labels_are_rejected_without_inspection(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        first = validator.validate(before, after)
        request = first["warning_review_request"]
        fingerprint = request["warnings"][0]["warning_fingerprint"]
        for reviewer_id in ("ab", "x" * 129, "human\nreviewer"):
            with self.subTest(reviewer_id=repr(reviewer_id)):
                with self.assertRaisesRegex(ValueError, "identity metadata is retired"):
                    validator.validate(
                        before,
                        after,
                        warning_resolutions={
                            fingerprint: "人工建议恢复原句中的模态范围以保留表达功能",
                        },
                        warning_review_request_sha256=request["request_sha256"],
                        warning_reviewer_kind="HUMAN",
                        warning_reviewer_id=reviewer_id,
                    )

    def test_cli_proposal_preserves_review_and_real_exit_code(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        first = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(before),
                str(after),
                "--format",
                "json",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        self.assertEqual(2, first.returncode, first.stderr)
        initial = json.loads(first.stdout)
        request = initial["warning_review_request"]
        fingerprint = request["warnings"][0]["warning_fingerprint"]
        command = [
            sys.executable,
            str(SCRIPT),
            str(before),
            str(after),
            "--format",
            "json",
            "--propose-warning-resolution",
            f"{fingerprint}=人工建议恢复原句中的模态范围以保留表达功能",
            "--warning-review-request-sha256",
            request["request_sha256"],
        ]

        proposed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        self.assertEqual(2, proposed.returncode, proposed.stderr)
        payload = json.loads(proposed.stdout)
        self.assertEqual("REVIEW", payload["delivery_gate_status"])
        proposal = payload["warning_proposal_state"]
        self.assertEqual("UNVERIFIED_CALLER_PROPOSAL", proposal["proposal_source"])
        self.assertFalse(proposal["reviewer_identifier_collected"])
        self.assertFalse(proposal["identity_verified"])
        self.assertFalse(proposal["review_clearance_granted"])

        retired = subprocess.run(
            command + [
                "--warning-reviewer-kind",
                "HUMAN",
                "--warning-reviewer-id",
                "external-reviewer-label",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        self.assertEqual(2, retired.returncode)
        self.assertIn("identity metadata is retired", retired.stderr)
        self.assertNotIn("external-reviewer-label", retired.stderr)

    def test_cli_retired_accept_warning_is_rejected_even_with_human_label(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(before),
                str(after),
                "--format",
                "json",
                "--accept-warning",
                "SPEECH_ACT_MODALITY_SCOPE_CHANGED=人工确认该模态变化不影响原句表达功能",
                "--warning-reviewer-kind",
                "HUMAN",
                "--warning-reviewer-id",
                "external-reviewer-label",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        self.assertEqual(2, completed.returncode)
        self.assertIn("--accept-warning is retired", completed.stderr)

    def test_unknown_or_vague_warning_resolution_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validator._parse_reason_pairs(
                ["SPEECH_ACT_MODALITY_SCOPE_CHANGED=接受"],
                "--propose-warning-resolution",
            )
        with self.assertRaises(ValueError):
            validator._parse_reason_pairs(
                ["SPEECH_ACT_MODALITY_SCOPE_CHANGED=人工确认"],
                "--propose-warning-resolution",
            )
        with self.assertRaises(ValueError):
            validator._parse_reason_pairs(
                ["SPEECH_ACT_MODALITY_SCOPE_CHANGED=这是一个具体理由"],
                "--propose-warning-resolution",
            )
        with self.assertRaisesRegex(ValueError, "重复提交 CODE"):
            validator._parse_reason_pairs(
                [
                    "f" * 64 + "=人工建议恢复原句模态以保留表达功能",
                    "f" * 64 + "=人工建议保留原句模态所限定的结论范围",
                ],
                "--propose-warning-resolution",
            )

    def test_review_request_cannot_be_replayed_across_artifacts(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        first = validator.validate(before, after, scene="GENERAL")
        request = first["warning_review_request"]
        fingerprint = request["warnings"][0]["warning_fingerprint"]
        after.write_text("结果发生改变。", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "does not match the current artifact"):
            validator.validate(
                before,
                after,
                scene="GENERAL",
                warning_resolutions={
                    fingerprint: "人工建议恢复原句中的模态范围以保留表达功能",
                },
                warning_review_request_sha256=request["request_sha256"],
            )

    def test_review_request_rejects_policy_hash_drift(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        first = validator.validate(before, after, scene="GENERAL")
        request = first["warning_review_request"]
        fingerprint = request["warnings"][0]["warning_fingerprint"]
        changed_policy = dict(request["policy_hashes"])
        changed_policy["validator_sha256"] = "0" * 64

        with mock.patch.object(validator, "_policy_hashes", return_value=changed_policy):
            with self.assertRaisesRegex(ValueError, "policy hashes"):
                validator.validate(
                    before,
                    after,
                    scene="GENERAL",
                    warning_resolutions={
                        fingerprint: "人工建议恢复原句中的模态范围以保留表达功能",
                    },
                    warning_review_request_sha256=request["request_sha256"],
                )

    def test_review_request_cannot_be_replayed_across_validation_context(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        first = validator.validate(before, after, scene="GENERAL")
        request = first["warning_review_request"]
        fingerprint = request["warnings"][0]["warning_fingerprint"]

        for changed_context in (
            {"scene": "RESEARCH"},
            {"scene": "GENERAL", "protected_terms": ["结果"]},
        ):
            with self.subTest(changed_context=changed_context):
                with self.assertRaisesRegex(ValueError, "does not match the current artifact"):
                    validator.validate(
                        before,
                        after,
                        warning_resolutions={
                            fingerprint: "人工建议恢复原句中的模态范围以保留表达功能",
                        },
                        warning_review_request_sha256=request["request_sha256"],
                        **changed_context,
                    )

    def test_resolution_fingerprint_must_exist_in_current_request(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        first = validator.validate(before, after, scene="GENERAL")
        request = first["warning_review_request"]

        with self.assertRaisesRegex(ValueError, "fingerprint not present"):
            validator.validate(
                before,
                after,
                scene="GENERAL",
                warning_resolutions={
                    "f" * 64: "人工建议恢复原句中的模态范围以保留表达功能",
                },
                warning_review_request_sha256=request["request_sha256"],
            )

    def test_pass_requires_revised_draft_to_eliminate_warning(self) -> None:
        before, warned = self.pair("结果可能变化。", "结果发生变化。")
        first = validator.validate(before, warned, scene="GENERAL")
        self.assertEqual("REVIEW", first["status"])
        warned.write_text("结果可能发生变化。", encoding="utf-8")

        revised = validator.validate(before, warned, scene="GENERAL")
        self.assert_paired_quality_review(revised, decision="REWRITE")
        self.assertEqual([], revised["unaccepted_warnings"])
        self.assertIsNone(revised["warning_review_request"])
        self.assertEqual(
            "NOT_PROVIDED",
            revised["warning_proposal_state"]["attestation_status"],
        )

    def test_hard_invariant_change_fails(self) -> None:
        before, after = self.pair("公式为 $x=1$。", "公式为 $x=2$。", suffix=".tex")
        payload = validator.validate(before, after, scene="GENERAL")
        self.assertEqual("FAIL", payload["status"])
        self.assertEqual(1, payload["exit_code"])
        self.assertEqual("FAIL", payload["hard_invariant_layer_status"])
        self.assertEqual("FAIL", payload["delivery_gate_status"])
        self.assertTrue(payload["invariants"]["hard_failure"])

    def test_text_output_names_layer_statuses_and_non_evaluated_scope(self) -> None:
        before, after = self.pair("结果可能变化。", "结果发生变化。")
        payload = validator.validate(before, after, scene="GENERAL")
        rendered = validator._text_output(payload)

        self.assertIn("delivery_gate_status: REVIEW", rendered)
        self.assertIn("hard_invariant_layer_status: PASS", rendered)
        self.assertIn("speech_act_layer_status: REVIEW", rendered)
        self.assertIn("style_signal_layer_status: PASS", rendered)
        self.assertIn("academic_correctness: NOT_EVALUATED", rendered)
        self.assertIn("warning_proposal_attestation_status: NOT_PROVIDED", rendered)
        self.assertIn("warning_proposal_identity_verified: FALSE", rendered)
        self.assertIn("warning_proposal_clearance_granted: FALSE", rendered)
        self.assertIn("warning_reviewer_identifier_collected: FALSE", rendered)
        self.assertNotIn("reviewer_id_sha256", rendered)
        self.assertRegex(rendered, r"warning_review_request_sha256: [0-9a-f]{64}")
        self.assertIn(
            "warning: SPEECH_ACT_MODALITY_SCOPE_CHANGED [warning]",
            rendered,
        )

    def test_extended_protected_content_and_garbled_text_fail(self) -> None:
        cases = (
            (
                "\\begin{alignat}{2}\nx &= y\n\\end{alignat}\n",
                "\\begin{alignat}{2}\nx &= z\n\\end{alignat}\n",
                ".tex",
            ),
            (
                "\\begin{exercise}\n求函数的极值。\n\\end{exercise}\n",
                "\\begin{exercise}\n计算函数的极值。\n\\end{exercise}\n",
                ".tex",
            ),
            ("```text\ntoken=alpha\n````\n", "```text\ntoken=beta\n````\n", ".md"),
            ("样本分为三组。", "样本分为四组。", ".md"),
            ("OCR：\ufffd字。", "OCR：清字。", ".md"),
        )
        for before_text, after_text, suffix in cases:
            with self.subTest(before=before_text):
                before, after = self.pair(before_text, after_text, suffix=suffix)
                payload = validator.validate(before, after)
                self.assertEqual("FAIL", payload["status"])
                self.assertEqual(1, payload["exit_code"])

    def test_repeated_term_cli_hard_fails_and_records_glossary_evidence(self) -> None:
        before, after = self.pair(
            "采用有限元法求解，材料为 Q235钢。",
            "采用谱方法求解，材料为 Q345钢。",
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(before),
                str(after),
                "--format",
                "json",
                "--term",
                "有限元法",
                "--term",
                "Q235钢",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(1, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual("FAIL", payload["status"])
        self.assertEqual("CHECKED", payload["evidence"]["protected_terms"]["status"])
        self.assertEqual(2, payload["evidence"]["protected_terms"]["count"])
        self.assertRegex(payload["evidence"]["protected_terms"]["sha256"], r"^[0-9a-f]{64}$")
        error_codes = {item["code"] for item in payload["invariants"]["errors"]}
        self.assertIn("PROTECTED_TERM_CHANGED", error_codes)

    def test_cli_json_status_and_exit_code(self) -> None:
        before, after = self.pair("这张表必须牢记。", "这张表必须牢记。")
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(before),
                str(after),
                "--scene",
                "course",
                "--format",
                "json",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(2, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual("REVIEW", payload["status"])
        self.assertRegex(payload["evidence"]["after_sha256"], r"^[0-9a-f]{64}$")
        self.assertNotIn("score", payload)

    def test_cli_evidence_dir_persists_result_request_and_manifest_atomically(self) -> None:
        before, after = self.pair("值得注意的是，结果为 1。", "结果为 1。")
        evidence_dir = self.root / "direct-evidence"
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(before),
                str(after),
                "--format",
                "json",
                "--evidence-dir",
                str(evidence_dir),
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        self.assertEqual(2, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual("PERSISTED", payload["evidence_bundle"]["status"])
        result_path = evidence_dir / "validation-result.json"
        request_path = evidence_dir / "paired-quality-review-request.json"
        invocation_path = evidence_dir / "invocation-request.json"
        execution_path = evidence_dir / "execution-record.json"
        stdout_path = evidence_dir / "rendered-output.txt"
        stderr_path = evidence_dir / "stderr.txt"
        manifest_path = evidence_dir / "evidence-manifest.json"
        before_archive = evidence_dir / "inputs" / "before.bin"
        after_archive = evidence_dir / "inputs" / "after.bin"
        self.assertTrue(result_path.is_file())
        self.assertTrue(request_path.is_file())
        self.assertTrue(invocation_path.is_file())
        self.assertTrue(execution_path.is_file())
        self.assertTrue(stdout_path.is_file())
        self.assertTrue(stderr_path.is_file())
        self.assertTrue(manifest_path.is_file())
        self.assertEqual(before.read_bytes(), before_archive.read_bytes())
        self.assertEqual(after.read_bytes(), after_archive.read_bytes())
        self.assertEqual(completed.stdout.encode("utf-8"), stdout_path.read_bytes())
        self.assertEqual(b"", stderr_path.read_bytes())
        self.assertEqual(payload, json.loads(result_path.read_text(encoding="utf-8")))
        self.assertEqual(
            payload["paired_quality_review_request"],
            json.loads(request_path.read_text(encoding="utf-8")),
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual("humanize-direct-validation-evidence/v3", manifest["schema"])
        self.assertEqual("SELF_CONSISTENCY_ONLY", manifest["integrity_scope"])
        self.assertEqual(payload["evidence_bundle"]["run_id"], manifest["run_id"])
        invocation = json.loads(invocation_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["run_id"], invocation["run_id"])
        self.assertEqual("SUPPORTED", invocation["reexecution"]["status"])
        self.assertFalse(invocation["privacy"]["reviewer_identifier_collected"])
        self.assertFalse(invocation["privacy"]["stable_reviewer_pseudonym_archived"])
        self.assertFalse(invocation["privacy"]["source_locator_archived"])
        self.assertEqual(payload["exit_code"], manifest["exit_code"])
        self.assertEqual(
            payload["paired_quality_review_request"]["request_sha256"],
            manifest["paired_quality_review_request_sha256"],
        )
        manifest_hash = manifest.pop("manifest_sha256")
        self.assertEqual(
            validator._sha256(validator._canonical_json_bytes(manifest)),
            manifest_hash,
        )
        before_hash = validator._sha256(before.read_bytes())
        self.assertEqual(before_hash, manifest["source_bindings"]["before"]["sha256"])

        rerun = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(before),
                str(after),
                "--format",
                "json",
                "--evidence-dir",
                str(evidence_dir),
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        self.assertEqual(2, rerun.returncode)
        rerun_payload = json.loads(rerun.stdout)
        self.assertEqual(payload, rerun_payload)
        self.assertEqual(manifest_hash, json.loads(manifest_path.read_text(encoding="utf-8"))["manifest_sha256"])

    def test_evidence_bundle_failure_leaves_no_staging_or_published_directory(self) -> None:
        before, after = self.pair("值得注意的是，结果为 1。", "结果为 1。")
        payload = validator.validate(before, after)
        payload["evidence_bundle"] = validator._evidence_bundle_record(payload)
        evidence_dir = self.root / "atomic-evidence"
        original = validator._write_exclusive
        calls = {"count": 0}

        def fail_on_second(path: Path, raw: bytes) -> None:
            calls["count"] += 1
            if calls["count"] == 2:
                raise OSError("injected evidence write failure")
            original(path, raw)

        with mock.patch.object(validator, "_write_exclusive", side_effect=fail_on_second):
            with self.assertRaisesRegex(OSError, "injected evidence write failure"):
                validator._persist_evidence_bundle(
                    payload,
                    before=before,
                    after=after,
                    output_dir=evidence_dir,
                )
        self.assertFalse(evidence_dir.exists())
        self.assertEqual([], list(self.root.glob(".atomic-evidence.staging-*")))

    def test_evidence_bundle_every_write_failure_rolls_back_completely(self) -> None:
        before, after = self.pair("值得注意的是，结果为 1。", "结果为 1。")
        payload = validator.validate(before, after)
        invocation = validator._build_invocation_request(
            payload,
            before=before,
            after=after,
        )
        payload["evidence_bundle"] = validator._evidence_bundle_record(
            payload,
            run_id=invocation["run_id"],
        )
        rendered = validator._pretty_json_bytes(payload)
        baseline = self.root / "write-count-baseline"
        validator._persist_evidence_bundle(
            payload,
            before=before,
            after=after,
            output_dir=baseline,
            invocation_request=invocation,
            rendered_output=rendered,
        )
        write_count = len(json.loads(
            (baseline / "evidence-manifest.json").read_text(encoding="utf-8")
        )["artifacts"]) + 1

        original = validator._write_exclusive
        for fail_at in range(1, write_count + 1):
            with self.subTest(fail_at=fail_at):
                target = self.root / f"write-failure-{fail_at}"
                calls = {"count": 0}

                def fail_selected(path: Path, raw: bytes) -> None:
                    calls["count"] += 1
                    if calls["count"] == fail_at:
                        raise OSError(f"injected write failure {fail_at}")
                    original(path, raw)

                with mock.patch.object(
                    validator,
                    "_write_exclusive",
                    side_effect=fail_selected,
                ):
                    with self.assertRaisesRegex(OSError, "injected write failure"):
                        validator._persist_evidence_bundle(
                            payload,
                            before=before,
                            after=after,
                            output_dir=target,
                            invocation_request=invocation,
                            rendered_output=rendered,
                        )
                self.assertFalse(target.exists())
                self.assertEqual(
                    [],
                    list(self.root.glob(f".{target.name}.staging-*")),
                )
                self.assertFalse(
                    target.with_name(f".{target.name}.publish.lock").exists()
                )

    def test_evidence_rename_failure_and_late_source_drift_roll_back(self) -> None:
        before, after = self.pair("值得注意的是，结果为 1。", "结果为 1。")
        payload = validator.validate(before, after)
        invocation = validator._build_invocation_request(
            payload,
            before=before,
            after=after,
        )
        payload["evidence_bundle"] = validator._evidence_bundle_record(
            payload,
            run_id=invocation["run_id"],
        )
        rendered = validator._pretty_json_bytes(payload)
        rename_target = self.root / "rename-failure"
        with mock.patch.object(Path, "rename", side_effect=OSError("rename failed")):
            with self.assertRaisesRegex(OSError, "rename failed"):
                validator._persist_evidence_bundle(
                    payload,
                    before=before,
                    after=after,
                    output_dir=rename_target,
                    invocation_request=invocation,
                    rendered_output=rendered,
                )
        self.assertFalse(rename_target.exists())
        self.assertEqual([], list(self.root.glob(".rename-failure.staging-*")))
        self.assertFalse((self.root / ".rename-failure.publish.lock").exists())

        drift_target = self.root / "source-drift"
        original_write = validator._write_exclusive

        def drift_after_manifest(path: Path, raw: bytes) -> None:
            original_write(path, raw)
            if path.name == "evidence-manifest.json":
                before.write_text("来源在提交前被替换。", encoding="utf-8")

        with mock.patch.object(
            validator,
            "_write_exclusive",
            side_effect=drift_after_manifest,
        ):
            with self.assertRaisesRegex(ValueError, "changed before evidence publication"):
                validator._persist_evidence_bundle(
                    payload,
                    before=before,
                    after=after,
                    output_dir=drift_target,
                    invocation_request=invocation,
                    rendered_output=rendered,
                )
        self.assertFalse(drift_target.exists())
        self.assertEqual([], list(self.root.glob(".source-drift.staging-*")))
        self.assertFalse((self.root / ".source-drift.publish.lock").exists())

    def test_keep_reason_requires_specific_chinese_reason(self) -> None:
        valid = {"LEX-COACH-01"}
        with self.assertRaises(ValueError):
            validator._parse_keep_reasons(["LEX-COACH-01=保留"], valid)
        with self.assertRaises(ValueError):
            validator._parse_keep_reasons(["LEX-COACH-01=确认保留"], valid)
        with self.assertRaises(ValueError):
            validator._parse_keep_reasons(["LEX-COACH-01=这是一个具体理由"], valid)
        before, after = self.pair("这张表必须牢记。", "这张表必须牢记。")
        with self.assertRaises(ValueError):
            validator.validate(
                before,
                after,
                scene="COURSE",
                keep_reasons={"LEX-COACH-01": "保留"},
            )
        with self.assertRaises(ValueError):
            validator.validate(
                before,
                after,
                scene="COURSE",
                keep_reasons={"NOT_A_SIGNAL": "这是一个不存在的信号"},
            )

    def test_multiple_keep_findings_require_location_and_emit_acceptance_ledger(self) -> None:
        before, after = self.pair("必须牢记。\n必须牢记。", "必须牢记。\n必须牢记。")
        with self.assertRaises(ValueError):
            validator.validate(
                before,
                after,
                scene="COURSE",
                keep_reasons={"LEX-COACH-01": "用户明确锁定这处课程原句"},
            )
        partial = validator.validate(
            before,
            after,
            scene="COURSE",
            keep_reasons={"LEX-COACH-01@1:1": "首处是用户明确锁定的课程原句"},
        )
        self.assertEqual("REVIEW", partial["status"])
        self.assertEqual(1, len(partial["accepted_findings"]))
        self.assertEqual(1, partial["accepted_findings"][0]["line"])
        complete = validator.validate(
            before,
            after,
            scene="COURSE",
            keep_reasons={
                "LEX-COACH-01@1:1": "首处是用户明确锁定的课程原句",
                "LEX-COACH-01@2:1": "次处是题面要求保留的课程原句",
            },
        )
        self.assert_paired_quality_review(complete, decision="NO_CHANGE", changes=0)
        self.assertEqual(2, len(complete["accepted_findings"]))

    def test_blind_forward_failures_are_machine_detectable(self) -> None:
        expected = {
            "course": "LEX-COACH-01",
            "modeling": "LEX-MARKET-01",
            "research": "LEX-FOUNDATION-01",
        }
        scenes = {"course": "COURSE", "modeling": "MODELING", "research": "RESEARCH"}
        for name, signal_id in expected.items():
            with self.subTest(scene=name):
                payload = validator.validate(
                    FORWARD_FIXTURES / f"{name}_before.md",
                    FORWARD_FIXTURES / f"{name}_after.md",
                    scene=scenes[name],
                )
                ids = {item["signal_id"] for item in payload["unexplained_high_findings"]}
                self.assertEqual("REVIEW", payload["status"])
                self.assertIn(signal_id, ids)

    def test_second_blind_pass_exposes_residual_and_synonym_dodges(self) -> None:
        expected = {
            "course": {"LEX-COACH-01", "LEX-FOUNDATION-01"},
            "modeling": {"LEX-MGMT-01", "LEX-MARKET-01"},
            "research": {"LEX-MARKET-01", "LEX-FOUNDATION-01"},
        }
        scenes = {"course": "COURSE", "modeling": "MODELING", "research": "RESEARCH"}
        for name, expected_ids in expected.items():
            with self.subTest(scene=name):
                payload = validator.validate(
                    FORWARD_FIXTURES / f"{name}_before.md",
                    FORWARD_V4_FIXTURES / f"{name}_after.md",
                    scene=scenes[name],
                )
                ids = {item["signal_id"] for item in payload["unexplained_high_findings"]}
                self.assertEqual("REVIEW", payload["status"])
                self.assertFalse(expected_ids - ids)

    def test_caller_asserted_proposals_cannot_close_gold_scenes(self) -> None:
        scenes = {"course": "COURSE", "modeling": "MODELING", "research": "RESEARCH"}
        for name, scene in scenes.items():
            with self.subTest(scene=name):
                first = validator.validate(
                    FORWARD_FIXTURES / f"{name}_before.md",
                    GOLD_FIXTURES / f"{name}_after.md",
                    scene=scene,
                )
                self.assertFalse(first["invariants"]["hard_failure"])
                self.assertEqual(0, first["lexical_summary"]["unexplained_high_candidates"])
                self.assertEqual(0, first["lexical_summary"]["introduced_candidates"])
                request = first["warning_review_request"]
                resolutions = {
                    item["warning_fingerprint"]: (
                        "人工建议恢复相应模态或写作命令以保留原句表达功能"
                    )
                    for item in request["warnings"]
                }
                second = validator.validate(
                    FORWARD_FIXTURES / f"{name}_before.md",
                    GOLD_FIXTURES / f"{name}_after.md",
                    scene=scene,
                    warning_resolutions=resolutions,
                    warning_review_request_sha256=request["request_sha256"],
                )
                self.assertEqual("REVIEW", second["status"])
                self.assertEqual(2, second["exit_code"])
                self.assertEqual([], second["accepted_warnings"])
                self.assertFalse(
                    second["warning_proposal_state"]["review_clearance_granted"]
                )

    def test_third_blind_pass_is_honest_but_still_requires_review(self) -> None:
        expected = {
            "course": "LEX-COACH-01",
            "modeling": "LEX-FUTURE-01",
            "research": "LEX-FOUNDATION-01",
        }
        scenes = {"course": "COURSE", "modeling": "MODELING", "research": "RESEARCH"}
        for name, signal_id in expected.items():
            with self.subTest(scene=name):
                payload = validator.validate(
                    FORWARD_FIXTURES / f"{name}_before.md",
                    FORWARD_V5_FIXTURES / f"{name}_after.md",
                    scene=scenes[name],
                )
                high_ids = {item["signal_id"] for item in payload["unexplained_high_findings"]}
                introduced_ids = {item["signal_id"] for item in payload["introduced_findings"]}
                self.assertEqual("REVIEW", payload["status"])
                self.assertIn(signal_id, high_ids | introduced_ids)

    def test_usability_red_blue_research_bridge_is_detected(self) -> None:
        fixture_root = ROOT / "tests" / "fixtures" / "humanize_usability_red_blue"
        payload = validator.validate(
            fixture_root / "research_before.md",
            fixture_root / "research_blue_body.md",
            scene="RESEARCH",
        )
        introduced_ids = {item["signal_id"] for item in payload["introduced_findings"]}
        self.assertEqual("REVIEW", payload["status"])
        self.assertIn("LEX-FOUNDATION-01", introduced_ids)

    def test_fresh_forward_foundation_synonym_cannot_receive_false_pass(self) -> None:
        before, after = self.pair(
            "已有研究表明，参数 $\\alpha=0.35$ 时，该方法可能在一定程度上显著提升系统稳定性。"
            "值得注意的是，这一结果不仅深刻揭示了控制机制，而且为后续研究奠定了坚实基础。",
            "已有研究表明，参数 $\\alpha=0.35$ 时，该方法可能在一定程度上显著提升系统稳定性。"
            "这一结果不仅揭示了控制机制，而且是后续研究的出发点。",
        )

        payload = validator.validate(before, after, scene="RESEARCH")
        high_ids = {item["signal_id"] for item in payload["unexplained_high_findings"]}

        self.assertEqual("REVIEW", payload["status"])
        self.assertEqual(2, payload["exit_code"])
        self.assertIn("LEX-FOUNDATION-01", high_ids)

    def test_fresh_course_synonym_repairs_cannot_receive_false_pass(self) -> None:
        before, after = self.pair(
            "\\begin{solution}必须牢记，遇到这类题千万不要直接套公式。"
            "值得注意的是，当 $x>0$ 时，由 $f'(x)=2x$ 可知函数递增。"
            "因此，我们可以很容易地得出最终结论。\\end{solution}",
            "\\begin{solution}遇到这类题，必须注意，不要直接套公式。"
            "当 $x>0$ 时，由 $f'(x)=2x$ 可知函数递增，由此可以得出结论。\\end{solution}",
            suffix=".tex",
        )

        payload = validator.validate(before, after, scene="COURSE")
        high_ids = {item["signal_id"] for item in payload["unexplained_high_findings"]}
        introduced_ids = {item["signal_id"] for item in payload["introduced_findings"]}

        self.assertEqual("REVIEW", payload["status"])
        self.assertEqual(2, payload["exit_code"])
        self.assertIn("LEX-COACH-01", high_ids)
        self.assertIn("LEX-CONCLUDE-01", introduced_ids)


if __name__ == "__main__":
    unittest.main()
