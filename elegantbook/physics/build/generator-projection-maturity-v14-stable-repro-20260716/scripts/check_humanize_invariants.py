#!/usr/bin/env python3
"""Compare a source document with its humanized rewrite.

This checker deliberately audits preservation, not academic correctness.  It
protects deterministic Markdown/LaTeX spans and reports changes to Chinese
speech-act markers that can silently alter an author's claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Sequence


MATH_ENVIRONMENTS = {
    "align",
    "align*",
    "alignat",
    "alignat*",
    "aligned",
    "alignedat",
    "array",
    "cases",
    "displaymath",
    "equation",
    "equation*",
    "gather",
    "gather*",
    "math",
    "matrix",
    "multline",
    "multline*",
    "pmatrix",
    "smallmatrix",
    "split",
    "vmatrix",
    "Vmatrix",
}
QUOTE_ENVIRONMENTS = {"quote", "quotation"}
CODE_ENVIRONMENTS = {"Verbatim", "lstlisting", "minted", "verbatim", "verbatim*"}
FORMAL_STATEMENT_ENVIRONMENTS = {
    f"{name}{suffix}"
    for name in (
        "corollary",
        "definition",
        "example",
        "exercise",
        "lemma",
        "problem",
        "proposition",
        "question",
        "theorem",
    )
    for suffix in ("", "*")
}
CRITICAL_COMMANDS = {
    "autoref",
    "cite",
    "citealp",
    "citeauthor",
    "citep",
    "citeyear",
    "citet",
    "cref",
    "Cref",
    "eqref",
    "includegraphics",
    "label",
    "pageref",
    "ref",
    "url",
}

SPEECH_ACT_MARKERS: dict[str, tuple[str, ...]] = {
    "negation": (
        "并不意味着",
        "并非",
        "不能",
        "不再",
        "未曾",
        "没有",
        "不",
        "未",
        "无",
        "非",
    ),
    "modality_scope": (
        "不一定",
        "有必要",
        "必须",
        "应当",
        "需要",
        "可能",
        "或许",
        "可以",
        "仅仅",
        "仅",
        "只",
        "可",
        "应",
    ),
    "definition_naming": (
        "以下简称",
        "称之为",
        "定义为",
        "记作",
        "记为",
        "称为",
        "简称",
        "所谓",
        "定义",
        "意味着",
    ),
    "assumption": ("不妨设", "假定", "假设", "设"),
    "reporting_observation": (
        "研究结果表明",
        "实验结果表明",
        "结果表明",
        "结果显示",
        "可以观察到",
        "可以看到",
        "观察到",
        "我们发现",
        "表明",
        "显示",
        "发现",
    ),
    "attribution_source": (
        "已有研究",
        "既有研究",
        "相关研究",
        "已有文献",
        "既有文献",
        "相关文献",
        "业内普遍认为",
        "一些学者指出",
        "有观点认为",
        "研究者认为",
        "研究者指出",
        "专家认为",
        "专家指出",
        "学者认为",
        "学者指出",
        "文献认为",
        "文献指出",
        "本研究证实",
        "本研究证明",
        "本研究表明",
        "本文证实",
        "本文证明",
        "本文表明",
    ),
    "condition": ("当且仅当", "只有当", "除非", "仅当", "只要", "如果", "若", "当"),
}

# Single-character Chinese markers require lexical exclusions.  Without these,
# a useful signal such as "应" also fires inside technical words such as
# "响应" and "对应".  Keep this list deliberately narrow and auditable.
SINGLE_MARKER_EXCLUSIONS: dict[str, tuple[str, ...]] = {
    "不": ("不仅", "不但"),
    "仅": ("不仅",),
    "应": ("对应", "响应", "反应", "效应", "适应", "应用", "应力", "应变", "应答"),
    "设": ("设备", "设施", "建设", "设计"),
    "若": ("若干",),
    "当": ("相当", "恰当", "适当", "当量", "当代"),
    "可": ("可靠", "许可", "认可", "可视化"),
}

# These checks cover a narrow class of source-to-rewrite transitions that a
# token inventory cannot see.  They are intentionally conservative: a warning
# is emitted only when the risky predicate is absent from the source and the
# source contains the corresponding directive or support shell.
SEMANTIC_TRANSITION_RULES: tuple[
    tuple[str, str, tuple[str, ...], tuple[str, ...]], ...
] = (
    (
        "SPEECH_ACT_DIRECTIVE_TO_COMPLETION",
        "An editing directive or artifact purpose was rewritten as a completed artifact assertion.",
        (
            r"表格的作用(?:是|在于)",
            r"正文(?:里|中)?(?:要|需要|应当|应该)",
            r"如果放到图上",
            r"图上应当",
        ),
        (
            r"表格[^。！？\n]{0,16}(?:列出|展示|包含|给出)",
            r"图(?:中|上)[^。！？\n]{0,16}(?:标出|展示|包含|给出)",
        ),
    ),
    (
        "SPEECH_ACT_SUPPORT_TO_ACTUAL_USE",
        "A support, value, or closure claim was rewritten as actual engineering use or a completed decision.",
        (
            r"为工程应用提供[^。！？\n]{0,12}(?:支撑|依据|参考)",
            r"从数据到决策[^。！？\n]{0,16}闭环",
            r"形成[^。！？\n]{0,16}闭环",
        ),
        (
            r"(?:用于|用来|服务于|指导|影响)[^。！？\n]{0,16}(?:工程决策|方案选择)",
            r"(?:工程决策|方案选择)[^。！？\n]{0,12}(?:已经|已被|完成|落地)",
        ),
    ),
)

HEDGE_MARKERS = ("可能", "或许", "在一定程度上")
DEGREE_CLAIM_PATTERN = re.compile(
    r"(?:影响程度[^。！？\n]{0,8}(?:有限|较小|轻微|显著|较大)|"
    r"影响[^。！？\n]{0,5}(?:有限|较小|轻微|显著|较大))"
)


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: str
    message: str
    details: dict[str, object] = field(default_factory=dict)


@dataclass
class CheckResult:
    errors: list[Diagnostic] = field(default_factory=list)
    warnings: list[Diagnostic] = field(default_factory=list)
    evidence: dict[str, object] = field(default_factory=dict)

    @property
    def hard_failure(self) -> bool:
        return bool(self.errors)

    @property
    def status(self) -> str:
        return "fail" if self.hard_failure else "pass"

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "hard_failure": self.hard_failure,
            "summary": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
            },
            "errors": [asdict(item) for item in self.errors],
            "warnings": [asdict(item) for item in self.warnings],
            "evidence": self.evidence,
        }


def _is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def strip_tex_comments(text: str) -> str:
    """Remove unescaped TeX comments while preserving line boundaries."""
    output: list[str] = []
    for line in text.splitlines(keepends=True):
        cut = None
        for index, char in enumerate(line):
            if char == "%" and not _is_escaped(line, index):
                cut = index
                break
        if cut is None:
            output.append(line)
            continue
        prefix = line[:cut]
        if prefix.endswith("\r"):
            prefix = prefix[:-1]
        # TeX comments consume the physical newline as well.  Removing both
        # makes comment-only line insertion invisible while retaining any
        # intentional space before the percent sign.
        output.append(prefix)
    return "".join(output)


def _tex_comment_spans(text: str) -> list[str]:
    """Return unescaped TeX comments exactly, including a bare continuation percent."""
    comments: list[str] = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").splitlines():
        for index, char in enumerate(line):
            if char == "%" and not _is_escaped(line, index):
                comments.append(line[index:])
                break
    return comments


def _canonical_span(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.strip().split("\n"))


def _mask_ranges(text: str, ranges: Iterable[tuple[int, int]]) -> str:
    chars = list(text)
    for start, end in ranges:
        chars[start:end] = " " * (end - start)
    return "".join(chars)


def _markdown_fence_spans(
    text: str,
    excluded_ranges: Sequence[tuple[int, int]] = (),
) -> list[tuple[int, int, str]]:
    """Return CommonMark fences, whose closer may be longer than the opener."""
    masked = _mask_ranges(text, excluded_ranges)
    opening_re = re.compile(
        r"(?m)^[ \t]{0,3}(?P<fence>`{3,}|~{3,})[^\n]*(?:\n|$)"
    )
    spans: list[tuple[int, int, str]] = []
    cursor = 0
    while cursor < len(masked):
        opening = opening_re.search(masked, cursor)
        if opening is None:
            break
        fence = opening.group("fence")
        closing_re = re.compile(
            rf"(?m)^[ \t]{{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*(?:\n|$)"
        )
        closing = closing_re.search(masked, opening.end())
        end = closing.end() if closing is not None else len(masked)
        spans.append((opening.start(), end, _canonical_span(text[opening.start():end])))
        cursor = end
    return spans


def _code_spans(text: str) -> tuple[list[str], list[tuple[int, int]]]:
    items: list[tuple[int, int, str]] = []
    occupied: list[tuple[int, int]] = []
    alternatives = "|".join(
        sorted((re.escape(name) for name in CODE_ENVIRONMENTS), key=len, reverse=True)
    )
    tex_env_re = re.compile(
        rf"(?s)\\begin\s*\{{(?P<name>{alternatives})\}}.*?"
        rf"\\end\s*\{{(?P=name)\}}"
    )
    for match in tex_env_re.finditer(text):
        items.append((match.start(), match.end(), _canonical_span(match.group(0))))
        occupied.append((match.start(), match.end()))

    for start, end, canonical in _markdown_fence_spans(text, occupied):
        items.append((start, end, canonical))
        occupied.append((start, end))

    masked = _mask_ranges(text, occupied)
    verb_re = re.compile(r"\\(?:verb|lstinline)\*?(?P<delimiter>[^\w\s]).*?(?P=delimiter)")
    for match in verb_re.finditer(masked):
        items.append((match.start(), match.end(), _canonical_span(match.group(0))))
        occupied.append((match.start(), match.end()))
    masked = _mask_ranges(text, occupied)

    index = 0
    while index < len(masked):
        if masked[index] != "`":
            index += 1
            continue
        end_ticks = index
        while end_ticks < len(masked) and masked[end_ticks] == "`":
            end_ticks += 1
        delimiter = masked[index:end_ticks]
        closing = masked.find(delimiter, end_ticks)
        if closing < 0 or "\n" in masked[end_ticks:closing]:
            index = end_ticks
            continue
        end = closing + len(delimiter)
        items.append((index, end, _canonical_span(text[index:end])))
        occupied.append((index, end))
        index = end

    items.sort(key=lambda item: item[0])
    occupied.sort()
    return [item[2] for item in items], occupied


def _extract_environment_spans(text: str, names: set[str]) -> list[str]:
    if not names:
        return []
    alternatives = "|".join(sorted((re.escape(name) for name in names), key=len, reverse=True))
    pattern = re.compile(
        rf"(?s)\\begin\s*\{{(?P<name>{alternatives})\}}.*?"
        rf"\\end\s*\{{(?P=name)\}}"
    )
    return [_canonical_span(match.group(0)) for match in pattern.finditer(text)]


def _math_spans(text: str, excluded_ranges: Sequence[tuple[int, int]]) -> list[str]:
    masked = _mask_ranges(text, excluded_ranges)
    spans: list[tuple[int, int, str]] = []
    occupied = list(excluded_ranges)

    alternatives = "|".join(
        sorted((re.escape(name) for name in MATH_ENVIRONMENTS), key=len, reverse=True)
    )
    env_re = re.compile(
        rf"(?s)\\begin\s*\{{(?P<name>{alternatives})\}}.*?"
        rf"\\end\s*\{{(?P=name)\}}"
    )
    for match in env_re.finditer(masked):
        spans.append((match.start(), match.end(), _canonical_span(text[match.start():match.end()])))
        occupied.append((match.start(), match.end()))

    masked = _mask_ranges(masked, occupied)
    for pattern in (re.compile(r"(?s)\\\[.*?\\\]"), re.compile(r"(?s)\\\(.*?\\\)")):
        matches = list(pattern.finditer(masked))
        for match in matches:
            spans.append((match.start(), match.end(), _canonical_span(text[match.start():match.end()])))
            occupied.append((match.start(), match.end()))
        masked = _mask_ranges(masked, [(match.start(), match.end()) for match in matches])

    index = 0
    while index < len(masked):
        if masked[index] != "$" or _is_escaped(masked, index):
            index += 1
            continue
        delimiter = "$$" if masked.startswith("$$", index) else "$"
        search = index + len(delimiter)
        closing = -1
        while search < len(masked):
            candidate = masked.find(delimiter, search)
            if candidate < 0:
                break
            if not _is_escaped(masked, candidate):
                closing = candidate
                break
            search = candidate + len(delimiter)
        if closing < 0:
            index += len(delimiter)
            continue
        end = closing + len(delimiter)
        spans.append((index, end, _canonical_span(text[index:end])))
        index = end

    spans.sort(key=lambda item: item[0])
    return [item[2] for item in spans]


def _quotation_spans(text: str, excluded_ranges: Sequence[tuple[int, int]]) -> list[str]:
    masked = _mask_ranges(text, excluded_ranges)
    spans: list[tuple[int, str]] = []
    patterns = (
        re.compile(r"“[^”\n]*”"),
        re.compile(r"‘[^’\n]*’"),
        re.compile(r"「[^」\n]*」"),
        re.compile(r"『[^』\n]*』"),
        re.compile(r'"[^"\n]+"'),
        re.compile(r"(?<!`)``[^\n]*?''"),
        re.compile(r"(?m)^(?:[ \t]*>[^\n]*(?:\n|$))+"),
    )
    for pattern in patterns:
        for match in pattern.finditer(masked):
            spans.append((match.start(), _canonical_span(text[match.start():match.end()])))

    command_quote_re = re.compile(r"\\(?:enquote|textquote)\s*(?P<brace>\{)")
    for match in command_quote_re.finditer(masked):
        parsed = _balanced_group(text, match.start("brace"), "{", "}")
        if parsed is None:
            continue
        _, end = parsed
        spans.append((match.start(), _canonical_span(text[match.start():end])))

    quote_env_re = re.compile(
        r"(?s)\\begin\s*\{(?P<name>quote|quotation)\}.*?"
        r"\\end\s*\{(?P=name)\}"
    )
    for match in quote_env_re.finditer(masked):
        spans.append((match.start(), _canonical_span(text[match.start():match.end()])))
    spans.sort(key=lambda item: item[0])
    return [item[1] for item in spans]


def _balanced_group(text: str, start: int, opening: str, closing: str) -> tuple[str, int] | None:
    if start >= len(text) or text[start] != opening:
        return None
    depth = 0
    index = start
    while index < len(text):
        char = text[index]
        if char == opening and not _is_escaped(text, index):
            depth += 1
        elif char == closing and not _is_escaped(text, index):
            depth -= 1
            if depth == 0:
                return text[start:index + 1], index + 1
        index += 1
    return None


def _critical_commands(text: str, excluded_ranges: Sequence[tuple[int, int]]) -> list[str]:
    masked = _mask_ranges(text, excluded_ranges)
    output: list[tuple[int, str]] = []
    command_re = re.compile(r"\\(?P<name>[A-Za-z@]+)(?P<star>\*)?")
    for match in command_re.finditer(masked):
        name = match.group("name")
        if name not in CRITICAL_COMMANDS and not _is_citation_command(name):
            continue
        index = match.end()
        groups: list[str] = []
        while True:
            while index < len(masked) and masked[index].isspace():
                index += 1
            if index < len(masked) and masked[index] == "[":
                parsed = _balanced_group(masked, index, "[", "]")
                if parsed is None:
                    break
                group, index = parsed
                groups.append(_canonical_span(group))
                continue
            break
        while index < len(masked) and masked[index].isspace():
            index += 1
        parsed_arg = _balanced_group(masked, index, "{", "}")
        if parsed_arg is None:
            canonical = f"\\{name}{match.group('star') or ''}<MISSING_ARGUMENT>"
        else:
            argument, _ = parsed_arg
            groups.append(_canonical_span(argument))
            canonical = f"\\{name}{match.group('star') or ''}" + "".join(groups)
        output.append((match.start(), canonical))
    output.sort(key=lambda item: item[0])
    return [item[1] for item in output]


def _is_citation_command(name: str) -> bool:
    return bool(
        re.fullmatch(
            r"(?:cite(?:alp|alt|author|p|t|year|yearpar)?|"
            r"(?:auto|foot|full|no|paren|smart|super|text)cite)",
            name,
        )
    )


NUMBER_UNIT_RE = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][-+]?\d+)?"
    r"(?:\s*(?:~|～|–|—|至)\s*[-+]?(?:\d+(?:\.\d+)?))?"
    r"\s*(?:\\%|%|‰|℃|°[CF]|"
    r"(?:[kMGTmunμ]?(?:m|s|g|A|K|mol|Hz|Pa|J|W|V|N|L|l|B|bps))"
    r"(?:\^?\{?-?\d+\}?|[²³])?(?:/[A-Za-zμ]+(?:\^?\{?-?\d+\}?|[²³])?)?|"
    r"年|月|日|小时|分钟|秒|千米|公里|厘米|毫米|微米|纳米|米|千克|公斤|克|毫克|人|次|项|组|倍)?"
)
CHINESE_NUMBER_RE = re.compile(
    r"(?:"
    r"第[零〇一二两三四五六七八九十百千万亿廿卅]+"
    r"(?:位|名|篇|章|节|级|轮|次|项|组|倍)?"
    r"|[零〇一二两三四五六七八九十百千万亿廿卅]+"
    r"(?:年|月|日|小时|分钟|秒|千米|公里|厘米|毫米|微米|纳米|米|千克|公斤|克|毫克|"
    r"人|位|名|篇|章|节|级|轮|次|项|组|倍)"
    r")"
)
GARBLED_MARKER_RE = re.compile(
    r"(?:\ufffd|[\ue000-\uf8ff]|锛岋|銆俾|鈥濃|â(?:€|€™|€œ|€“|€”))"
)
GARBLED_SPAN_RE = re.compile(
    rf"[^，。！？；;\s]*(?:{GARBLED_MARKER_RE.pattern})[^，。！？；;\s]*"
)


def _numbers_and_units(text: str, excluded_ranges: Sequence[tuple[int, int]]) -> list[str]:
    masked = _mask_ranges(text, excluded_ranges)
    output: list[tuple[int, str]] = []
    for match in NUMBER_UNIT_RE.finditer(masked):
        token = re.sub(r"\s+", "", match.group(0)).replace("\\%", "%")
        output.append((match.start(), token))
    output.extend((match.start(), match.group(0)) for match in CHINESE_NUMBER_RE.finditer(masked))
    return [token for _, token in sorted(output)]


def _garbled_spans(text: str) -> list[str]:
    return [_canonical_span(match.group(0)) for match in GARBLED_SPAN_RE.finditer(text)]


def _environment_events(text: str, excluded_ranges: Sequence[tuple[int, int]]) -> list[tuple[str, str]]:
    masked = _mask_ranges(text, excluded_ranges)
    pattern = re.compile(r"\\(?P<kind>begin|end)\s*\{(?P<name>[^{}\s]+)\}")
    return [(match.group("kind"), match.group("name")) for match in pattern.finditer(masked)]


def _validate_environment_nesting(events: Sequence[tuple[str, str]]) -> list[str]:
    stack: list[str] = []
    problems: list[str] = []
    for kind, name in events:
        if kind == "begin":
            stack.append(name)
        elif not stack:
            problems.append(f"end{{{name}}} has no matching begin")
        elif stack[-1] != name:
            problems.append(f"end{{{name}}} closes begin{{{stack[-1]}}}")
            stack.pop()
        else:
            stack.pop()
    problems.extend(f"begin{{{name}}} has no matching end" for name in reversed(stack))
    return problems


def _brace_problems(text: str, excluded_ranges: Sequence[tuple[int, int]]) -> list[str]:
    masked = _mask_ranges(text, excluded_ranges)
    stack: list[int] = []
    problems: list[str] = []
    for index, char in enumerate(masked):
        if char == "{" and not _is_escaped(masked, index):
            stack.append(index)
        elif char == "}" and not _is_escaped(masked, index):
            if stack:
                stack.pop()
            else:
                problems.append(f"unmatched closing brace at offset {index}")
    problems.extend(f"unmatched opening brace at offset {index}" for index in stack[:10])
    if len(stack) > 10:
        problems.append(f"{len(stack) - 10} additional unmatched opening braces")
    return problems


def _marker_counts(text: str) -> dict[str, Counter[str]]:
    result: dict[str, Counter[str]] = {}
    for category, markers in SPEECH_ACT_MARKERS.items():
        ordered = sorted(markers, key=len, reverse=True)
        pattern = re.compile("|".join(re.escape(marker) for marker in ordered))
        counts: Counter[str] = Counter()
        for match in pattern.finditer(text):
            marker = match.group(0)
            if len(marker) == 1 and _inside_excluded_word(text, match.start(), marker):
                continue
            counts[marker] += 1
        result[category] = counts
    return result


def _matched_patterns(text: str, patterns: Sequence[str]) -> list[str]:
    matches: list[str] = []
    for raw_pattern in patterns:
        match = re.search(raw_pattern, text)
        if match:
            matches.append(match.group(0)[:240])
    return matches


def _semantic_transition_diagnostics(
    before: str,
    after: str,
    *,
    severity: str,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for code, message, before_patterns, after_patterns in SEMANTIC_TRANSITION_RULES:
        before_trigger = _matched_patterns(before, before_patterns)
        after_predicate = _matched_patterns(after, after_patterns)
        source_predicate = _matched_patterns(before, after_patterns)
        if not before_trigger or not after_predicate or source_predicate:
            continue
        diagnostics.append(
            Diagnostic(
                code=code,
                severity=severity,
                message=message,
                details={
                    "source_triggers": before_trigger,
                    "rewrite_predicates": after_predicate,
                    "source_contains_rewrite_predicate": False,
                },
            )
        )

    hedge_count = sum(marker in before for marker in HEDGE_MARKERS)
    source_degree_claims = [match.group(0) for match in DEGREE_CLAIM_PATTERN.finditer(before)]
    rewrite_degree_claims = [match.group(0) for match in DEGREE_CLAIM_PATTERN.finditer(after)]
    if hedge_count >= 2 and rewrite_degree_claims and not source_degree_claims:
        diagnostics.append(
            Diagnostic(
                code="SPEECH_ACT_MODALITY_TO_DEGREE",
                severity=severity,
                message="Stacked uncertainty markers were rewritten as a new degree claim.",
                details={
                    "source_hedges": [marker for marker in HEDGE_MARKERS if marker in before],
                    "rewrite_degree_claims": rewrite_degree_claims[:8],
                    "source_degree_claims": [],
                },
            )
        )
    return diagnostics


def _inside_excluded_word(text: str, index: int, marker: str) -> bool:
    for word in SINGLE_MARKER_EXCLUSIONS.get(marker, ()):
        search_start = max(0, index - len(word) + 1)
        position = text.find(word, search_start, min(len(text), index + len(word)))
        if position >= 0 and position <= index < position + len(word):
            return True
    return False


def _sequence_details(before: Sequence[str], after: Sequence[str]) -> dict[str, object]:
    before_counter = Counter(before)
    after_counter = Counter(after)
    first_difference = None
    for index, pair in enumerate(zip(before, after)):
        if pair[0] != pair[1]:
            first_difference = index
            break
    if first_difference is None and len(before) != len(after):
        first_difference = min(len(before), len(after))

    def limited(counter: Counter[str]) -> list[dict[str, object]]:
        return [
            {"value": value[:240], "count": count}
            for value, count in counter.most_common(8)
            if count > 0
        ]

    return {
        "before_count": len(before),
        "after_count": len(after),
        "first_difference": first_difference,
        "removed": limited(before_counter - after_counter),
        "added": limited(after_counter - before_counter),
    }


def normalize_protected_terms(terms: Sequence[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in terms:
        term = raw.strip()
        if not term:
            raise ValueError("protected term must not be empty")
        if term not in seen:
            seen.add(term)
            normalized.append(term)
    return normalized


def _term_evidence(terms: Sequence[str]) -> dict[str, object]:
    raw = json.dumps(list(terms), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return {
        "status": "CHECKED" if terms else "NOT_PROVIDED",
        "count": len(terms),
        "sha256": hashlib.sha256(raw).hexdigest() if terms else None,
    }


def _term_occurrences(text: str, terms: Sequence[str]) -> list[str]:
    occurrences: list[tuple[int, str]] = []
    for term in terms:
        cursor = 0
        while True:
            position = text.find(term, cursor)
            if position < 0:
                break
            occurrences.append((position, term))
            cursor = position + len(term)
    return [term for _, term in sorted(occurrences)]


def _compare_sequence(
    result: CheckResult,
    code: str,
    label: str,
    before: Sequence[str],
    after: Sequence[str],
) -> None:
    if list(before) == list(after):
        return
    result.errors.append(
        Diagnostic(
            code=code,
            severity="error",
            message=f"{label} changed in count, content, or order.",
            details=_sequence_details(before, after),
        )
    )


def _prepare(text: str, document_format: str) -> tuple[str, list[str], list[tuple[int, int]]]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if document_format == "tex":
        normalized = strip_tex_comments(normalized)
    code, ranges = _code_spans(normalized)
    return normalized, code, ranges


def check_documents(
    before: str,
    after: str,
    *,
    document_format: str = "markdown",
    protect_quotes: bool = True,
    strict_speech_acts: bool = False,
    protected_terms: Sequence[str] = (),
    fragment_mode: bool = False,
) -> CheckResult:
    """Check deterministic preservation invariants for a style-only rewrite."""
    if document_format not in {"markdown", "tex"}:
        raise ValueError("document_format must be 'markdown' or 'tex'")

    terms = normalize_protected_terms(protected_terms)
    result = CheckResult(
        evidence={
            "protected_terms": _term_evidence(terms),
            "document_scope": "FRAGMENT" if fragment_mode else "DOCUMENT",
        }
    )
    if terms:
        _compare_sequence(
            result,
            "PROTECTED_TERM_CHANGED",
            "Explicitly supplied protected terms",
            _term_occurrences(before, terms),
            _term_occurrences(after, terms),
        )
    _compare_sequence(
        result,
        "GARBLED_TEXT_CHANGED",
        "Replacement characters or obvious mojibake spans",
        _garbled_spans(before),
        _garbled_spans(after),
    )
    if document_format == "tex":
        _compare_sequence(
            result,
            "TEX_COMMENT_CHANGED",
            "TeX comments or line-continuation percent markers",
            _tex_comment_spans(before),
            _tex_comment_spans(after),
        )
    before_text, before_code, before_code_ranges = _prepare(before, document_format)
    after_text, after_code, after_code_ranges = _prepare(after, document_format)

    _compare_sequence(result, "PROTECTED_CODE_CHANGED", "Code spans or fences", before_code, after_code)

    before_formal = _extract_environment_spans(before_text, FORMAL_STATEMENT_ENVIRONMENTS)
    after_formal = _extract_environment_spans(after_text, FORMAL_STATEMENT_ENVIRONMENTS)
    _compare_sequence(
        result,
        "PROTECTED_FORMAL_STATEMENT_CHANGED",
        "Exam prompts or formal statement environments",
        before_formal,
        after_formal,
    )

    before_math = _math_spans(before_text, before_code_ranges)
    after_math = _math_spans(after_text, after_code_ranges)
    _compare_sequence(result, "PROTECTED_MATH_CHANGED", "Math spans or environments", before_math, after_math)

    before_math_ranges = _locate_exact_spans(before_text, before_math)
    after_math_ranges = _locate_exact_spans(after_text, after_math)
    before_excluded = sorted(before_code_ranges + before_math_ranges)
    after_excluded = sorted(after_code_ranges + after_math_ranges)

    before_commands = _critical_commands(before_text, before_code_ranges)
    after_commands = _critical_commands(after_text, after_code_ranges)
    _compare_sequence(
        result,
        "CRITICAL_LATEX_COMMAND_CHANGED",
        "Critical LaTeX commands or arguments",
        before_commands,
        after_commands,
    )

    if protect_quotes:
        before_quotes = _quotation_spans(before_text, before_excluded)
        after_quotes = _quotation_spans(after_text, after_excluded)
        _compare_sequence(
            result,
            "DIRECT_QUOTATION_CHANGED",
            "Direct quotations",
            before_quotes,
            after_quotes,
        )

    before_numbers = _numbers_and_units(before_text, before_code_ranges)
    after_numbers = _numbers_and_units(after_text, after_code_ranges)
    _compare_sequence(
        result,
        "NUMBER_OR_UNIT_CHANGED",
        "Numbers or units",
        before_numbers,
        after_numbers,
    )

    before_events = _environment_events(before_text, before_code_ranges)
    after_events = _environment_events(after_text, after_code_ranges)
    if before_events != after_events:
        result.errors.append(
            Diagnostic(
                code="LATEX_ENVIRONMENT_ORDER_CHANGED",
                severity="error",
                message="LaTeX environment names or order changed.",
                details=_sequence_details(
                    [f"{kind}:{name}" for kind, name in before_events],
                    [f"{kind}:{name}" for kind, name in after_events],
                ),
            )
        )
    before_environment_problems = _validate_environment_nesting(before_events)
    after_environment_problems = _validate_environment_nesting(after_events)
    if fragment_mode:
        if before_environment_problems != after_environment_problems:
            result.errors.append(
                Diagnostic(
                    code="LATEX_ENVIRONMENT_FRAGMENT_BALANCE_CHANGED",
                    severity="error",
                    message="LaTeX fragment boundary balance changed.",
                    details={
                        "before": before_environment_problems[:20],
                        "after": after_environment_problems[:20],
                    },
                )
            )
    else:
        for side, problems in (
            ("before", before_environment_problems),
            ("after", after_environment_problems),
        ):
            if problems:
                result.errors.append(
                    Diagnostic(
                        code="LATEX_ENVIRONMENT_UNBALANCED",
                        severity="error",
                        message=f"LaTeX environments are unbalanced in {side} document.",
                        details={"side": side, "problems": problems[:20]},
                    )
                )

    before_brace_problems = _brace_problems(before_text, before_code_ranges)
    after_brace_problems = _brace_problems(after_text, after_code_ranges)
    if fragment_mode:
        if before_brace_problems != after_brace_problems:
            result.errors.append(
                Diagnostic(
                    code="LATEX_BRACE_FRAGMENT_BALANCE_CHANGED",
                    severity="error",
                    message="LaTeX fragment brace balance changed.",
                    details={
                        "before": before_brace_problems[:20],
                        "after": after_brace_problems[:20],
                    },
                )
            )
    else:
        for side, problems in (
            ("before", before_brace_problems),
            ("after", after_brace_problems),
        ):
            if problems:
                result.errors.append(
                    Diagnostic(
                        code="LATEX_BRACES_UNBALANCED",
                        severity="error",
                        message=f"Unescaped braces are unbalanced in {side} document.",
                        details={"side": side, "problems": problems[:20]},
                    )
                )

    before_speech_text = _mask_ranges(before_text, before_excluded)
    after_speech_text = _mask_ranges(after_text, after_excluded)
    before_markers = _marker_counts(before_speech_text)
    after_markers = _marker_counts(after_speech_text)
    for category in SPEECH_ACT_MARKERS:
        if before_markers[category] == after_markers[category]:
            continue
        severity = "error" if strict_speech_acts else "warning"
        diagnostic = Diagnostic(
            code=f"SPEECH_ACT_{category.upper()}_CHANGED",
            severity=severity,
            message=f"Speech-act markers changed in category '{category}'; review semantic force manually.",
            details={
                "before": dict(sorted(before_markers[category].items())),
                "after": dict(sorted(after_markers[category].items())),
            },
        )
        (result.errors if strict_speech_acts else result.warnings).append(diagnostic)

    transition_severity = "error" if strict_speech_acts else "warning"
    for diagnostic in _semantic_transition_diagnostics(
        before_speech_text,
        after_speech_text,
        severity=transition_severity,
    ):
        (result.errors if strict_speech_acts else result.warnings).append(diagnostic)

    return result


def _locate_exact_spans(text: str, spans: Sequence[str]) -> list[tuple[int, int]]:
    """Best-effort locations for already canonicalized spans, used only for masking."""
    ranges: list[tuple[int, int]] = []
    cursor = 0
    for span in spans:
        position = text.find(span, cursor)
        if position < 0:
            # Canonicalization may have removed outer/trailing whitespace.  Searching
            # from the start still masks the meaningful span in ordinary documents.
            position = text.find(span)
        if position >= 0:
            ranges.append((position, position + len(span)))
            cursor = position + len(span)
    return ranges


def _infer_format(path: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    return "tex" if path.suffix.lower() in {".tex", ".ltx"} else "markdown"


def _text_output(result: CheckResult) -> str:
    term_evidence = result.evidence.get("protected_terms", {})
    lines = [
        f"status: {result.status}",
        f"hard errors: {len(result.errors)}",
        f"warnings: {len(result.warnings)}",
        f"protected terms: {term_evidence.get('status', 'NOT_PROVIDED')}",
        f"protected term count: {term_evidence.get('count', 0)}",
        f"protected term sha256: {term_evidence.get('sha256') or 'NONE'}",
    ]
    for diagnostic in [*result.errors, *result.warnings]:
        lines.append(f"[{diagnostic.severity.upper()}] {diagnostic.code}: {diagnostic.message}")
        if diagnostic.details:
            lines.append("  " + json.dumps(diagnostic.details, ensure_ascii=False, sort_keys=True))
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check preservation invariants between original and humanized Markdown/TeX."
    )
    parser.add_argument("before", type=Path, help="Original UTF-8 Markdown or TeX file")
    parser.add_argument("after", type=Path, help="Humanized UTF-8 Markdown or TeX file")
    parser.add_argument("--format", choices=("auto", "markdown", "tex"), default="auto")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument(
        "--allow-quote-edits",
        action="store_true",
        help="Do not protect direct quotations (off by default)",
    )
    parser.add_argument(
        "--strict-speech-acts",
        action="store_true",
        help="Treat changes to negation/modality/definition/reporting markers as hard errors",
    )
    parser.add_argument(
        "--fragment",
        action="store_true",
        help=(
            "Validate a document fragment: unchanged boundary imbalance is allowed, "
            "but any environment or brace-balance drift still fails"
        ),
    )
    parser.add_argument(
        "--term",
        action="append",
        default=[],
        metavar="TERM",
        help="Protect an exact method, material, or glossary term; repeat for multiple terms",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        before = args.before.read_text(encoding="utf-8-sig")
        after = args.after.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2

    result = check_documents(
        before,
        after,
        document_format=_infer_format(args.before, args.format),
        protect_quotes=not args.allow_quote_edits,
        strict_speech_acts=args.strict_speech_acts,
        protected_terms=args.term,
        fragment_mode=args.fragment,
    )
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(_text_output(result))
    return 1 if result.hard_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
