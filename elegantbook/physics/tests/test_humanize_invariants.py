import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "humanize_invariants"
SCRIPT = Path(
    os.environ.get(
        "HUMANIZE_SKILL_DIR",
        Path.home() / ".codex" / "skills" / "humanize-academic-chinese",
    )
) / "scripts" / "check_humanize_invariants.py"

SPEC = importlib.util.spec_from_file_location("check_humanize_invariants", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
invariants = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = invariants
SPEC.loader.exec_module(invariants)


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def codes(result: object, field: str) -> set[str]:
    return {item.code for item in getattr(result, field)}


class HumanizeInvariantTests(unittest.TestCase):
    def test_safe_style_rewrite_passes_without_warning(self) -> None:
        result = invariants.check_documents(
            fixture("safe_before.md"),
            fixture("safe_after.md"),
            document_format="markdown",
        )
        self.assertEqual("pass", result.status)
        self.assertFalse(result.errors)
        self.assertFalse(result.warnings)
        self.assertEqual("NOT_PROVIDED", result.evidence["protected_terms"]["status"])
        self.assertIsNone(result.evidence["protected_terms"]["sha256"])
        self.assertEqual("DOCUMENT", result.evidence["document_scope"])

    def test_explicit_method_and_material_terms_are_hard_invariants(self) -> None:
        result = invariants.check_documents(
            "采用有限元法求解，材料为 Q235钢。有限元法保持不变。",
            "采用谱方法求解，材料为 Q345钢。",
            protected_terms=["有限元法", "Q235钢"],
        )
        self.assertIn("PROTECTED_TERM_CHANGED", codes(result, "errors"))
        evidence = result.evidence["protected_terms"]
        self.assertEqual("CHECKED", evidence["status"])
        self.assertEqual(2, evidence["count"])
        self.assertRegex(str(evidence["sha256"]), r"^[0-9a-f]{64}$")

    def test_changed_formula_is_a_hard_failure(self) -> None:
        result = invariants.check_documents(
            fixture("changed_formula_before.tex"),
            fixture("changed_formula_after.tex"),
            document_format="tex",
        )
        self.assertTrue(result.hard_failure)
        self.assertIn("PROTECTED_MATH_CHANGED", codes(result, "errors"))

    def test_alignat_formula_is_protected(self) -> None:
        result = invariants.check_documents(
            "\\begin{alignat}{2}\nx &= y\n\\end{alignat}\n",
            "\\begin{alignat}{2}\nx &= z\n\\end{alignat}\n",
            document_format="tex",
        )
        self.assertIn("PROTECTED_MATH_CHANGED", codes(result, "errors"))

    def test_exam_and_formal_statement_environments_are_protected(self) -> None:
        result = invariants.check_documents(
            "\\begin{exercise}\n求函数的极值。\n\\end{exercise}\n",
            "\\begin{exercise}\n计算函数的极值。\n\\end{exercise}\n",
            document_format="tex",
        )
        self.assertIn("PROTECTED_FORMAL_STATEMENT_CHANGED", codes(result, "errors"))

    def test_changed_direct_quote_is_a_hard_failure_by_default(self) -> None:
        before = fixture("changed_quote_before.md")
        after = fixture("changed_quote_after.md")
        protected = invariants.check_documents(before, after)
        allowed = invariants.check_documents(before, after, protect_quotes=False)
        self.assertIn("DIRECT_QUOTATION_CHANGED", codes(protected, "errors"))
        self.assertFalse(allowed.errors)

    def test_speech_act_drift_warns_and_strict_mode_fails(self) -> None:
        before = fixture("speech_act_drift_before.md")
        after = fixture("speech_act_drift_after.md")
        normal = invariants.check_documents(before, after)
        strict = invariants.check_documents(before, after, strict_speech_acts=True)
        self.assertFalse(normal.errors)
        self.assertIn("SPEECH_ACT_DEFINITION_NAMING_CHANGED", codes(normal, "warnings"))
        self.assertIn("SPEECH_ACT_MODALITY_SCOPE_CHANGED", codes(normal, "warnings"))
        self.assertIn("SPEECH_ACT_REPORTING_OBSERVATION_CHANGED", codes(normal, "warnings"))
        self.assertTrue(strict.hard_failure)
        self.assertFalse(strict.warnings)

    def test_attribution_source_drift_requires_review_and_strict_mode_fails(self) -> None:
        before = "专家认为，该方法在低频组更稳定。"
        after = "本文证实，该方法在低频组更稳定。"
        normal = invariants.check_documents(before, after)
        strict = invariants.check_documents(before, after, strict_speech_acts=True)
        code = "SPEECH_ACT_ATTRIBUTION_SOURCE_CHANGED"
        self.assertFalse(normal.errors)
        self.assertIn(code, codes(normal, "warnings"))
        self.assertIn(code, codes(strict, "errors"))
        self.assertTrue(strict.hard_failure)

    def test_unchanged_explicit_attribution_does_not_warn(self) -> None:
        before = "王明（2020）指出，该效应只在低频组出现。"
        after = "王明（2020）指出，该效应仅在低频组出现。"
        result = invariants.check_documents(before, after)
        self.assertNotIn("SPEECH_ACT_ATTRIBUTION_SOURCE_CHANGED", codes(result, "warnings"))

    def test_v19_focus_scope_cannot_be_absolutized_silently(self) -> None:
        normal = invariants.check_documents(
            "本问的重点不是比较两个物种的绝对值，而是考察政策收益的保留程度。",
            "本问不比较两个物种的绝对值，而是考察政策收益的保留程度。",
        )
        strict = invariants.check_documents(
            "本问的重点不是比较两个物种的绝对值，而是考察政策收益的保留程度。",
            "本问不比较两个物种的绝对值，而是考察政策收益的保留程度。",
            strict_speech_acts=True,
        )

        self.assertIn("SPEECH_ACT_FOCUS_SCOPE_CHANGED", codes(normal, "warnings"))
        self.assertIn("SPEECH_ACT_FOCUS_SCOPE_CHANGED", codes(strict, "errors"))

    def test_v7_directive_must_not_become_completed_artifact_assertion(self) -> None:
        result = invariants.check_documents(
            "表格的作用在于统一实验口径，正文里要保留 20 ℃、25 ℃ 和 30 ℃ 三组数据。",
            "表格列出 20 ℃、25 ℃ 和 30 ℃ 三组数据，以统一实验口径。",
        )
        self.assertIn("SPEECH_ACT_DIRECTIVE_TO_COMPLETION", codes(result, "warnings"))

    def test_v7_support_claim_must_not_become_actual_engineering_use(self) -> None:
        result = invariants.check_documents(
            "该模型形成了从数据到决策的完整闭环，为工程应用提供有力支撑。",
            "该模型将参数扫描结果用于工程决策，为工程应用提供依据。",
        )
        self.assertIn("SPEECH_ACT_SUPPORT_TO_ACTUAL_USE", codes(result, "warnings"))

    def test_v7_hedge_stack_must_not_become_new_degree_claim(self) -> None:
        result = invariants.check_documents(
            "模型可能在一定程度上或许仍会受到传感器漂移影响。",
            "传感器漂移可能影响模型，影响程度或许有限。",
        )
        self.assertIn("SPEECH_ACT_MODALITY_TO_DEGREE", codes(result, "warnings"))

    def test_v7_transition_checks_do_not_fire_when_source_already_states_result(self) -> None:
        result = invariants.check_documents(
            "表格列出三组数据。该结果已用于工程决策。传感器漂移的影响程度有限。",
            "表格给出三组数据。该结果用于工程决策。传感器漂移影响有限。",
        )
        transition_codes = {
            "SPEECH_ACT_DIRECTIVE_TO_COMPLETION",
            "SPEECH_ACT_SUPPORT_TO_ACTUAL_USE",
            "SPEECH_ACT_MODALITY_TO_DEGREE",
        }
        self.assertFalse(transition_codes & codes(result, "warnings"))

    def test_v7_transition_checks_respect_strict_mode(self) -> None:
        result = invariants.check_documents(
            "正文里要保留三组数据。该模型为工程应用提供支撑。",
            "表格列出三组数据。该模型用于工程决策。",
            strict_speech_acts=True,
        )
        self.assertIn("SPEECH_ACT_DIRECTIVE_TO_COMPLETION", codes(result, "errors"))
        self.assertIn("SPEECH_ACT_SUPPORT_TO_ACTUAL_USE", codes(result, "errors"))
        self.assertFalse(result.warnings)

    def test_v7_transition_checks_ignore_protected_code_and_math(self) -> None:
        markdown = invariants.check_documents(
            "```text\n正文里要保留三组数据。\n```",
            "```text\n表格列出三组数据。\n```",
        )
        tex = invariants.check_documents(
            "设 $x=\\text{正文里要保留}$。",
            "设 $x=\\text{表格列出}$。",
            document_format="tex",
        )
        self.assertNotIn("SPEECH_ACT_DIRECTIVE_TO_COMPLETION", codes(markdown, "warnings"))
        self.assertNotIn("SPEECH_ACT_DIRECTIVE_TO_COMPLETION", codes(tex, "warnings"))

    def test_v8_bujin_is_not_counted_as_negation_or_scope_marker(self) -> None:
        result = invariants.check_documents(
            "该模型不仅全面提升了预测性能，而且形成完整闭环。",
            "",
        )
        self.assertNotIn("SPEECH_ACT_NEGATION_CHANGED", codes(result, "warnings"))
        self.assertNotIn("SPEECH_ACT_MODALITY_SCOPE_CHANGED", codes(result, "warnings"))

    def test_v9_editor_payload_paraphrase_is_not_a_completion_upgrade(self) -> None:
        result = invariants.check_documents(
            "正文里要保留三组数据，温度分别为 20 ℃、25 ℃ 和 30 ℃。",
            "三组数据的温度分别为 20 ℃、25 ℃ 和 30 ℃。",
        )
        self.assertNotIn("SPEECH_ACT_DIRECTIVE_TO_COMPLETION", codes(result, "warnings"))

    def test_tex_comments_are_protected_by_default(self) -> None:
        result = invariants.check_documents(
            fixture("tex_comments_before.tex"),
            fixture("tex_comments_after.tex"),
            document_format="tex",
        )
        self.assertIn("TEX_COMMENT_CHANGED", codes(result, "errors"))

    def test_number_or_unit_change_is_a_hard_failure(self) -> None:
        result = invariants.check_documents(
            "样本在 25 ℃ 下保持 30 分钟。",
            "样本在 35 ℃ 下保持 30 分钟。",
        )
        self.assertIn("NUMBER_OR_UNIT_CHANGED", codes(result, "errors"))

    def test_chinese_number_change_is_a_hard_failure(self) -> None:
        result = invariants.check_documents("样本分为三组。", "样本分为四组。")
        self.assertIn("NUMBER_OR_UNIT_CHANGED", codes(result, "errors"))

    def test_replacement_character_or_mojibake_change_is_a_hard_failure(self) -> None:
        replacement = invariants.check_documents("OCR：\ufffd字。", "OCR：清字。")
        mojibake = invariants.check_documents("片段：绾腑。", "片段：正常。")
        self.assertIn("GARBLED_TEXT_CHANGED", codes(replacement, "errors"))
        self.assertIn("GARBLED_TEXT_CHANGED", codes(mojibake, "errors"))

    def test_critical_command_arguments_and_order_are_protected(self) -> None:
        result = invariants.check_documents(
            r"见式 \eqref{eq:a} 与文献 \citep[p. 3]{alpha,beta}。",
            r"见式 \eqref{eq:b} 与文献 \citep[p. 3]{alpha,beta}。",
            document_format="tex",
        )
        self.assertIn("CRITICAL_LATEX_COMMAND_CHANGED", codes(result, "errors"))

    def test_code_fences_and_inline_code_are_protected(self) -> None:
        before = "运行 `python app.py`：\n\n```python\nvalue = 1\n```\n"
        after = "执行 `python app.py`：\n\n```python\nvalue = 2\n```\n"
        result = invariants.check_documents(before, after)
        self.assertIn("PROTECTED_CODE_CHANGED", codes(result, "errors"))

    def test_commonmark_longer_closing_fence_is_protected(self) -> None:
        before = "```python\ntoken = alpha\n````\n"
        after = "```python\ntoken = beta\n````\n"
        result = invariants.check_documents(before, after)
        self.assertIn("PROTECTED_CODE_CHANGED", codes(result, "errors"))

    def test_tex_verbatim_code_is_protected_and_braces_inside_are_ignored(self) -> None:
        before = "\\verb|mapping = {'a': 1}|\n\\begin{lstlisting}\nx = {1: 2}\n\\end{lstlisting}\n"
        after = "\\verb|mapping = {'a': 1}|\n\\begin{lstlisting}\nx = {1: 3}\n\\end{lstlisting}\n"
        result = invariants.check_documents(before, after, document_format="tex")
        self.assertIn("PROTECTED_CODE_CHANGED", codes(result, "errors"))
        self.assertNotIn("LATEX_BRACES_UNBALANCED", codes(result, "errors"))

    def test_ascii_direct_quote_is_protected(self) -> None:
        result = invariants.check_documents(
            '作者使用 "local response" 指代该现象。',
            '作者使用 "regional response" 指代该现象。',
        )
        self.assertIn("DIRECT_QUOTATION_CHANGED", codes(result, "errors"))

    def test_nested_latex_quote_command_is_protected(self) -> None:
        result = invariants.check_documents(
            r"作者写道：\enquote{模型 \textbf{A} 保持稳定}。",
            r"作者写道：\enquote{模型 \textbf{B} 保持稳定}。",
            document_format="tex",
        )
        self.assertIn("DIRECT_QUOTATION_CHANGED", codes(result, "errors"))

    def test_common_citation_variants_are_protected(self) -> None:
        result = invariants.check_documents(
            r"参见 \parencite[12]{alpha}。",
            r"参见 \parencite[12]{beta}。",
            document_format="tex",
        )
        self.assertIn("CRITICAL_LATEX_COMMAND_CHANGED", codes(result, "errors"))

    def test_comment_only_line_inside_math_is_protected(self) -> None:
        before = "\\[\nx = 1\n% old note 20 and \\ref{fake}\n\\]\n"
        after = "\\[\nx = 1\n\\]\n"
        result = invariants.check_documents(before, after, document_format="tex")
        self.assertIn("TEX_COMMENT_CHANGED", codes(result, "errors"))

    def test_unchanged_comment_and_escaped_percent_pass(self) -> None:
        before = "% keep this layout comment\n比例为 50\\%，因此保留原式。\n"
        after = "% keep this layout comment\n比例为 50\\%，故保留原式。\n"
        result = invariants.check_documents(before, after, document_format="tex")
        self.assertNotIn("TEX_COMMENT_CHANGED", codes(result, "errors"))

    def test_environment_order_and_brace_balance_are_checked(self) -> None:
        before = "\\begin{itemize}\n\\item A\n\\end{itemize}\n"
        after = "\\begin{enumerate}\n\\item A}\n\\end{enumerate}\n"
        result = invariants.check_documents(before, after, document_format="tex")
        self.assertIn("LATEX_ENVIRONMENT_ORDER_CHANGED", codes(result, "errors"))
        self.assertIn("LATEX_BRACES_UNBALANCED", codes(result, "errors"))

    def test_fragment_mode_allows_only_unchanged_boundary_imbalance(self) -> None:
        before = "\\begin{document}\n值得注意的是，结论保持不变。\n"
        after = "\\begin{document}\n结论保持不变。\n"
        whole_document = invariants.check_documents(
            before, after, document_format="tex"
        )
        fragment = invariants.check_documents(
            before,
            after,
            document_format="tex",
            fragment_mode=True,
        )

        self.assertIn("LATEX_ENVIRONMENT_UNBALANCED", codes(whole_document, "errors"))
        self.assertNotIn("LATEX_ENVIRONMENT_UNBALANCED", codes(fragment, "errors"))
        self.assertFalse(fragment.errors)
        self.assertEqual("FRAGMENT", fragment.evidence["document_scope"])

        drifted = invariants.check_documents(
            before,
            "结论保持不变。\n",
            document_format="tex",
            fragment_mode=True,
        )
        self.assertIn("LATEX_ENVIRONMENT_ORDER_CHANGED", codes(drifted, "errors"))

    def test_cli_json_and_exit_codes(self) -> None:
        safe = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(FIXTURES / "safe_before.md"),
                str(FIXTURES / "safe_after.md"),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        changed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(FIXTURES / "changed_formula_before.tex"),
                str(FIXTURES / "changed_formula_after.tex"),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, safe.returncode, safe.stderr)
        self.assertEqual("pass", json.loads(safe.stdout)["status"])
        self.assertEqual(1, changed.returncode, changed.stderr)
        payload = json.loads(changed.stdout)
        self.assertEqual("fail", payload["status"])
        self.assertTrue(payload["hard_failure"])


if __name__ == "__main__":
    unittest.main()
