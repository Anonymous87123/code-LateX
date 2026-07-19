#!/usr/bin/env python3
"""Locate reviewable Chinese academic-style signals without classifying authorship."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from bisect import bisect_right
from pathlib import Path
from typing import Any, Iterable, Sequence


DEFAULT_LEXICON = Path(__file__).resolve().parents[1] / "references" / "lexical-signals.json"
DEFAULT_EXTENSIONS = {".md", ".markdown", ".tex", ".txt"}
SENTENCE_BREAKS = "。！？!?；;\n"
SCENE_CHOICES = ("ALL", "AUTO", "GENERAL", "COURSE", "MODELING", "RESEARCH")
COURSE_FORMULA_CAPTION_MATCHER = "course-short-caption-formula-run-v1"


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> Any:
    raise ValueError(f"non-finite JSON number: {value}")


def load_lexicon(path: str | Path = DEFAULT_LEXICON) -> dict[str, Any]:
    """Load and minimally validate the lexical signal contract."""
    lexicon_path = Path(path)
    with lexicon_path.open("r", encoding="utf-8") as handle:
        data = json.load(
            handle,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonfinite,
        )

    if not isinstance(data.get("signals"), list) or not data["signals"]:
        raise ValueError("lexicon must contain a non-empty signals list")

    seen: set[str] = set()
    required = {
        "id",
        "category",
        "label",
        "variants",
        "regex",
        "scenes",
        "severity",
        "threshold",
        "exclusions",
        "action",
        "rationale",
        "positive_examples",
        "negative_examples",
        "provenance",
    }
    for signal in data["signals"]:
        missing = required - signal.keys()
        if missing:
            raise ValueError(f"{signal.get('id', '<unknown>')} missing fields: {sorted(missing)}")
        signal_id = signal["id"]
        if signal_id in seen:
            raise ValueError(f"duplicate signal id: {signal_id}")
        seen.add(signal_id)
        if signal["action"] not in {"KEEP", "DELETE", "REWRITE", "REVIEW"}:
            raise ValueError(f"invalid action for {signal_id}: {signal['action']}")
        threshold = signal["threshold"]
        if threshold.get("window") not in {"document", "paragraph", "sentence", "line"}:
            raise ValueError(f"invalid threshold window for {signal_id}")
        if int(threshold.get("min_occurrences", 0)) < 1:
            raise ValueError(f"invalid min_occurrences for {signal_id}")
        for pattern in signal["regex"]:
            re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        structural_matcher = signal.get("structural_matcher")
        if structural_matcher is not None:
            if not isinstance(structural_matcher, dict):
                raise ValueError(f"invalid structural_matcher for {signal_id}")
            required_matcher = {
                "kind",
                "min_pairs",
                "max_caption_hanzi",
                "max_blank_lines_before_formula",
                "caption_regex",
                "caption_exclusion_regex",
                "formula_environments",
            }
            if set(structural_matcher) != required_matcher:
                raise ValueError(f"invalid structural_matcher contract for {signal_id}")
            if structural_matcher["kind"] != COURSE_FORMULA_CAPTION_MATCHER:
                raise ValueError(f"unsupported structural matcher for {signal_id}")
            if int(structural_matcher["min_pairs"]) < 2:
                raise ValueError(f"invalid structural min_pairs for {signal_id}")
            if int(structural_matcher["max_caption_hanzi"]) < 2:
                raise ValueError(f"invalid max_caption_hanzi for {signal_id}")
            if int(structural_matcher["max_blank_lines_before_formula"]) < 0:
                raise ValueError(f"invalid formula adjacency for {signal_id}")
            re.compile(structural_matcher["caption_regex"])
            re.compile(structural_matcher["caption_exclusion_regex"])
            environments = structural_matcher["formula_environments"]
            if not isinstance(environments, list) or not environments:
                raise ValueError(f"invalid formula_environments for {signal_id}")
            if any(not isinstance(item, str) or not item for item in environments):
                raise ValueError(f"invalid formula environment for {signal_id}")
        for exclusion in signal["exclusions"]:
            if set(exclusion) != {"scope", "regex", "reason"}:
                raise ValueError(f"invalid exclusion contract for {signal_id}")
            re.compile(exclusion["regex"], re.IGNORECASE | re.MULTILINE)
    return data


def _markdown_fence_spans(text: str) -> list[tuple[int, int, str]]:
    opening_re = re.compile(
        r"(?m)^[ \t]{0,3}(?P<fence>`{3,}|~{3,})[^\n]*(?:\n|$)"
    )
    spans: list[tuple[int, int, str]] = []
    cursor = 0
    while cursor < len(text):
        opening = opening_re.search(text, cursor)
        if opening is None:
            break
        fence = opening.group("fence")
        closing_re = re.compile(
            rf"(?m)^[ \t]{{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*(?:\n|$)"
        )
        closing = closing_re.search(text, opening.end())
        end = closing.end() if closing is not None else len(text)
        spans.append((opening.start(), end, "markdown-fence"))
        cursor = end
    return spans


def _raw_protected_spans(
    text: str,
    document_format: str = "markdown",
) -> list[tuple[int, int, str]]:
    if document_format not in {"markdown", "tex"}:
        raise ValueError("document_format must be 'markdown' or 'tex'")
    patterns = [
        (
            "latex-verbatim-or-math-environment",
            re.compile(
                r"(?is)\\begin\{(equation\*?|align\*?|alignat\*?|alignedat|gather\*?|multline\*?|"
                r"displaymath|math|verbatim\*?|lstlisting|minted)\}.*?\\end\{\1\}"
            ),
        ),
        (
            "latex-exam-or-formal-statement-environment",
            re.compile(
                r"(?is)\\begin\{(example\*?|exercise\*?|problem\*?|question\*?|"
                r"theorem\*?|lemma\*?|proposition\*?|corollary\*?|definition\*?)\}"
                r".*?\\end\{\1\}"
            ),
        ),
        ("display-math", re.compile(r"(?s)(?<!\\)\$\$.*?(?<!\\)\$\$|\\\[.*?\\\]")),
        ("inline-math", re.compile(r"(?s)\\\(.*?\\\)|(?<!\\)\$(?!\$)(?:\\.|[^$\n])+?(?<!\\)\$")),
        ("inline-code", re.compile(r"(?<!`)`[^`\n]+`(?!`)")),
        ("markdown-quote", re.compile(r"(?m)^\s*>[^\n]*")),
        ("chinese-double-quote", re.compile(r"“[^”\n]*”|「[^」\n]*」|『[^』\n]*』")),
        ("chinese-single-quote", re.compile(r"‘[^’\n]*’")),
        (
            "latex-quote",
            re.compile(
                r"``[^\n]*?''|\\(?:enquote|textquote)\{(?:[^{}\n]|\{[^{}\n]*\})*\}"
            ),
        ),
        ("ascii-quote", re.compile(r'(?<!\\)"[^"\n]*?(?<!\\)"')),
    ]
    if document_format == "tex":
        patterns.append(("latex-comment", re.compile(r"(?m)(?<!\\)%[^\n]*")))
    spans = _markdown_fence_spans(text)
    for reason, pattern in patterns:
        spans.extend((match.start(), match.end(), reason) for match in pattern.finditer(text))
    return spans


def _merge_spans(spans: Iterable[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    merged: list[list[Any]] = []
    for start, end, reason in sorted(spans, key=lambda item: (item[0], item[1])):
        if not merged or start >= merged[-1][1]:
            merged.append([start, end, {reason}])
            continue
        merged[-1][1] = max(merged[-1][1], end)
        merged[-1][2].add(reason)
    return [(start, end, "+".join(sorted(reasons))) for start, end, reasons in merged]


class ProtectedIndex:
    """Find whether an offset falls inside code, math, comments, or quotations."""

    def __init__(self, text: str, document_format: str = "markdown") -> None:
        self.spans = _merge_spans(_raw_protected_spans(text, document_format))
        self.starts = [span[0] for span in self.spans]

    def reason_at(self, offset: int) -> str | None:
        index = bisect_right(self.starts, offset) - 1
        if index >= 0:
            start, end, reason = self.spans[index]
            if start <= offset < end:
                return reason
        return None

    def reason_for_span(self, start: int, end: int) -> str | None:
        index = bisect_right(self.starts, start) - 1
        if index >= 0:
            protected_start, protected_end, reason = self.spans[index]
            if protected_start <= start and end <= protected_end:
                return reason
        return None


def _signal_patterns(signal: dict[str, Any]) -> list[re.Pattern[str]]:
    patterns: list[re.Pattern[str]] = []
    if signal["variants"]:
        variants = sorted(set(signal["variants"]), key=len, reverse=True)
        patterns.append(re.compile("|".join(re.escape(item) for item in variants), re.IGNORECASE))
    patterns.extend(
        re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        for pattern in signal["regex"]
    )
    return patterns


def _deduplicate_matches(matches: Iterable[re.Match[str]]) -> list[tuple[int, int, str]]:
    raw = sorted(
        ((match.start(), match.end(), match.group(0)) for match in matches),
        key=lambda item: (item[0], -(item[1] - item[0])),
    )
    kept: list[tuple[int, int, str]] = []
    for candidate in raw:
        start, end, _ = candidate
        if any(start < old_end and end > old_start for old_start, old_end, _ in kept):
            continue
        kept.append(candidate)
    return sorted(kept)


def _physical_lines(text: str) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    offset = 0
    for raw in text.splitlines(keepends=True):
        content = raw.rstrip("\r\n")
        lines.append(
            {
                "start": offset,
                "content_end": offset + len(content),
                "end": offset + len(raw),
                "content": content,
            }
        )
        offset += len(raw)
    if offset < len(text) or (text and not lines):
        lines.append(
            {
                "start": offset,
                "content_end": len(text),
                "end": len(text),
                "content": text[offset:],
            }
        )
    return lines


def _standalone_formula_end(
    lines: Sequence[dict[str, Any]],
    start_index: int,
    environments: set[str],
) -> int | None:
    stripped = str(lines[start_index]["content"]).strip()
    if stripped.startswith(r"\("):
        closing_at = stripped.find(r"\)", 2)
        if closing_at > 2 and not stripped[closing_at + 2 :].strip():
            return start_index
        return None
    if re.fullmatch(r"\$(?!\$)(?:\\.|[^$])+\$", stripped):
        return start_index

    delimiters = (("$$", "$$"), (r"\[", r"\]"))
    for opening, closing in delimiters:
        if not stripped.startswith(opening):
            continue
        remainder = stripped[len(opening):]
        closing_at = remainder.find(closing)
        if closing_at >= 0:
            if not remainder[closing_at + len(closing) :].strip():
                return start_index
            return None
        for index in range(start_index + 1, len(lines)):
            content = str(lines[index]["content"]).strip()
            closing_at = content.find(closing)
            if closing_at < 0:
                continue
            if not content[closing_at + len(closing) :].strip():
                return index
            return None
        return None

    opening = re.fullmatch(r"\\begin\{([A-Za-z*]+)\}", stripped)
    if opening is None or opening.group(1) not in environments:
        return None
    closing = rf"\end{{{opening.group(1)}}}"
    for index in range(start_index + 1, len(lines)):
        if str(lines[index]["content"]).strip() == closing:
            return index
    return None


def _course_formula_caption_occurrences(
    text: str,
    matcher: dict[str, Any],
) -> list[tuple[int, int, str]]:
    lines = _physical_lines(text)
    caption_pattern = re.compile(str(matcher["caption_regex"]))
    exclusion_pattern = re.compile(str(matcher["caption_exclusion_regex"]))
    max_hanzi = int(matcher["max_caption_hanzi"])
    max_blanks = int(matcher["max_blank_lines_before_formula"])
    environments = {str(item) for item in matcher["formula_environments"]}
    pairs: list[dict[str, Any]] = []

    for index, line in enumerate(lines):
        content = str(line["content"])
        caption = content.strip()
        if not caption_pattern.fullmatch(caption):
            continue
        hanzi_count = len(re.findall(r"[\u3400-\u9fff]", caption))
        if hanzi_count < 2 or hanzi_count > max_hanzi:
            continue
        if exclusion_pattern.search(caption):
            continue

        formula_index = index + 1
        blank_count = 0
        while formula_index < len(lines) and not str(lines[formula_index]["content"]).strip():
            blank_count += 1
            formula_index += 1
        if blank_count > max_blanks or formula_index >= len(lines):
            continue
        formula_end_index = _standalone_formula_end(lines, formula_index, environments)
        if formula_end_index is None:
            continue

        leading = len(content) - len(content.lstrip())
        trailing = len(content.rstrip())
        start = int(line["start"]) + leading
        end = int(line["start"]) + trailing
        pairs.append(
            {
                "start": start,
                "end": end,
                "matched": text[start:end],
                "formula_end": int(lines[formula_end_index]["end"]),
            }
        )

    runs: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for pair in pairs:
        if not current:
            current = [pair]
            continue
        between = text[int(current[-1]["formula_end"]):int(pair["start"])]
        if not between.strip():
            current.append(pair)
        else:
            runs.append(current)
            current = [pair]
    if current:
        runs.append(current)

    minimum = int(matcher["min_pairs"])
    return [
        (int(pair["start"]), int(pair["end"]), str(pair["matched"]))
        for run in runs
        if len(run) >= minimum
        for pair in run
    ]


def _structural_matches(
    text: str,
    matcher: dict[str, Any],
) -> list[tuple[int, int, str]]:
    if matcher["kind"] == COURSE_FORMULA_CAPTION_MATCHER:
        return _course_formula_caption_occurrences(text, matcher)
    raise ValueError(f"unsupported structural matcher: {matcher['kind']}")


def _bounded_span(text: str, offset: int, separators: str) -> tuple[int, int]:
    left = max((text.rfind(char, 0, offset) for char in separators), default=-1) + 1
    right_candidates = [text.find(char, offset) for char in separators]
    right_candidates = [position for position in right_candidates if position >= 0]
    right = min(right_candidates) + 1 if right_candidates else len(text)
    return left, right


def _paragraph_span(text: str, offset: int) -> tuple[int, int]:
    separators = list(re.finditer(r"(?:\r?\n\s*){2,}", text))
    start = 0
    end = len(text)
    for separator in separators:
        if separator.end() <= offset:
            start = separator.end()
        elif separator.start() >= offset:
            end = separator.start()
            break
    return start, end


def _scope_span(text: str, offset: int, scope: str) -> tuple[int, int]:
    if scope == "document":
        return 0, len(text)
    if scope == "paragraph":
        return _paragraph_span(text, offset)
    if scope == "sentence":
        return _bounded_span(text, offset, SENTENCE_BREAKS)
    if scope == "line":
        return _bounded_span(text, offset, "\n")
    raise ValueError(f"unsupported scope: {scope}")


def _scope_bounds(text: str, start: int, end: int, scope: str) -> tuple[int, int]:
    if scope == "match":
        return start, end
    if scope == "context":
        return max(0, start - 100), min(len(text), end + 100)
    return _scope_span(text, start, scope)


def _exclusion_reason(
    text: str,
    start: int,
    end: int,
    signal: dict[str, Any],
) -> str | None:
    for exclusion in signal["exclusions"]:
        scope_start, scope_end = _scope_bounds(text, start, end, exclusion["scope"])
        scoped = text[scope_start:scope_end]
        for match in re.finditer(exclusion["regex"], scoped, re.IGNORECASE | re.MULTILINE):
            absolute_start = scope_start + match.start()
            absolute_end = scope_start + match.end()
            if absolute_start < end and absolute_end > start:
                return exclusion["reason"]
    return None


def _line_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    last_break = text.rfind("\n", 0, offset)
    column = offset - last_break
    return line, column


def _context(text: str, start: int, end: int, radius: int = 70) -> str:
    snippet = text[max(0, start - radius):min(len(text), end + radius)]
    return re.sub(r"\s+", " ", snippet).strip()


def _window_key(text: str, offset: int, scope: str) -> tuple[int, int]:
    return _scope_span(text, offset, scope)


def _qualifying_counts(
    text: str,
    occurrences: Sequence[dict[str, Any]],
    threshold: dict[str, Any],
) -> list[int]:
    scope = threshold["window"]
    max_chars = int(threshold.get("window_chars", 0) or 0)
    distinct_scope = threshold.get("count_distinct_by")
    if distinct_scope not in {None, "paragraph", "sentence", "line"}:
        raise ValueError(f"unsupported count_distinct_by: {distinct_scope}")
    keys = [_window_key(text, item["start"], scope) for item in occurrences]
    counts: list[int] = []
    for index, occurrence in enumerate(occurrences):
        key = keys[index]
        neighbors = [
            item
            for other_index, item in enumerate(occurrences)
            if keys[other_index] == key
            and (not max_chars or abs(item["start"] - occurrence["start"]) <= max_chars)
        ]
        if distinct_scope:
            counts.append(
                len({_window_key(text, item["start"], distinct_scope) for item in neighbors})
            )
        else:
            counts.append(len(neighbors))
    return counts


def _finding(
    *,
    text: str,
    file: str,
    scene: str,
    signal: dict[str, Any],
    occurrence: dict[str, Any],
    count: int,
    protected: bool,
    protection: str | None,
    excluded: bool = False,
    exclusion: str | None = None,
) -> dict[str, Any]:
    line, column = _line_column(text, occurrence["start"])
    return {
        "start_char": occurrence["start"],
        "end_char": occurrence["end"],
        "file": file,
        "line": line,
        "column": column,
        "matched": occurrence["matched"],
        "context": _context(text, occurrence["start"], occurrence["end"]),
        "count": count,
        "action": "KEEP" if protected or excluded else signal["action"],
        "signal_id": signal["id"],
        "category": signal["category"],
        "label": signal["label"],
        "scene": scene,
        "severity": signal["severity"],
        "candidate": not protected and not excluded,
        "protected": protected,
        "protection": protection,
        "excluded": excluded,
        "exclusion": exclusion,
        "rationale": signal["rationale"],
    }


def scan_text_with_offsets(
    text: str,
    *,
    file: str = "<memory>",
    scene: str = "ALL",
    lexicon: dict[str, Any] | None = None,
    include_protected: bool = False,
    include_excluded: bool = False,
) -> list[dict[str, Any]]:
    """Return candidates with exact internal character offsets."""
    scene = scene.upper()
    if scene not in SCENE_CHOICES:
        raise ValueError(f"unsupported scene: {scene}")
    lexicon = lexicon or load_lexicon()
    suffix = Path(file).suffix.lower() if file and file != "<memory>" else ""
    document_format = "tex" if suffix in {".tex", ".ltx"} else "markdown"
    protected_index = ProtectedIndex(text, document_format=document_format)
    findings: list[dict[str, Any]] = []

    for signal in lexicon["signals"]:
        if (
            scene not in {"ALL", "AUTO"}
            and "ALL" not in signal["scenes"]
            and scene not in signal["scenes"]
        ):
            continue
        structural_matcher = signal.get("structural_matcher")
        if structural_matcher is not None:
            matches = _structural_matches(text, structural_matcher)
        else:
            raw_matches: list[re.Match[str]] = []
            for pattern in _signal_patterns(signal):
                raw_matches.extend(pattern.finditer(text))
            matches = _deduplicate_matches(raw_matches)

        candidates: list[dict[str, Any]] = []
        protected_hits: list[tuple[dict[str, Any], str]] = []
        excluded_hits: list[tuple[dict[str, Any], str]] = []
        for start, end, matched in matches:
            occurrence = {"start": start, "end": end, "matched": matched}
            protection = protected_index.reason_for_span(start, end)
            if protection:
                protected_hits.append((occurrence, protection))
                continue
            exclusion = _exclusion_reason(text, start, end, signal)
            if exclusion:
                excluded_hits.append((occurrence, exclusion))
                continue
            candidates.append(occurrence)

        counts = _qualifying_counts(text, candidates, signal["threshold"])
        minimum = int(signal["threshold"]["min_occurrences"])
        for occurrence, count in zip(candidates, counts):
            if count >= minimum:
                findings.append(
                    _finding(
                        text=text,
                        file=file,
                        scene=scene,
                        signal=signal,
                        occurrence=occurrence,
                        count=count,
                        protected=False,
                        protection=None,
                    )
                )
        if include_protected:
            for occurrence, protection in protected_hits:
                findings.append(
                    _finding(
                        text=text,
                        file=file,
                        scene=scene,
                        signal=signal,
                        occurrence=occurrence,
                        count=1,
                        protected=True,
                        protection=protection,
                    )
                )
        if include_excluded:
            for occurrence, exclusion in excluded_hits:
                findings.append(
                    _finding(
                        text=text,
                        file=file,
                        scene=scene,
                        signal=signal,
                        occurrence=occurrence,
                        count=1,
                        protected=False,
                        protection=None,
                        excluded=True,
                        exclusion=exclusion,
                    )
                )

    return sorted(findings, key=lambda item: (item["file"], item["line"], item["column"], item["signal_id"]))


def scan_text(
    text: str,
    *,
    file: str = "<memory>",
    scene: str = "ALL",
    lexicon: dict[str, Any] | None = None,
    include_protected: bool = False,
    include_excluded: bool = False,
) -> list[dict[str, Any]]:
    """Return the stable public finding view without internal offsets."""
    findings = scan_text_with_offsets(
        text,
        file=file,
        scene=scene,
        lexicon=lexicon,
        include_protected=include_protected,
        include_excluded=include_excluded,
    )
    return [
        {key: value for key, value in finding.items() if key not in {"start_char", "end_char"}}
        for finding in findings
    ]


def scan_file(
    path: str | Path,
    *,
    scene: str = "ALL",
    lexicon: dict[str, Any] | None = None,
    include_protected: bool = False,
    include_excluded: bool = False,
) -> list[dict[str, Any]]:
    source = Path(path)
    text = source.read_text(encoding="utf-8-sig")
    return scan_text(
        text,
        file=str(source),
        scene=scene,
        lexicon=lexicon,
        include_protected=include_protected,
        include_excluded=include_excluded,
    )


def collect_paths(paths: Sequence[str], extensions: set[str] | None = None) -> list[Path]:
    extensions = extensions or DEFAULT_EXTENSIONS
    collected: set[Path] = set()
    for raw in paths:
        path = Path(raw)
        if path.is_file():
            collected.add(path.resolve())
        elif path.is_dir():
            collected.update(
                item.resolve()
                for item in path.rglob("*")
                if item.is_file() and item.suffix.lower() in extensions
            )
        else:
            raise FileNotFoundError(raw)
    return sorted(collected, key=lambda item: str(item).lower())


OUTPUT_FIELDS = (
    "file",
    "line",
    "column",
    "matched",
    "context",
    "count",
    "action",
    "signal_id",
    "category",
    "label",
    "scene",
    "severity",
    "candidate",
    "protected",
    "protection",
    "excluded",
    "exclusion",
    "rationale",
)


def render_output(
    findings: Sequence[dict[str, Any]],
    *,
    output_format: str,
    notice: str,
    coverage: dict[str, Any] | None = None,
) -> str:
    if output_format == "json":
        payload = {
            "notice": notice,
            "finding_count": len(findings),
            "candidate_count": sum(bool(item["candidate"]) for item in findings),
            "findings": list(findings),
            "coverage": coverage
            or {
                "status": "NOT_REPORTED",
                "requested_count": 0,
                "scanned_count": 0,
                "skipped_count": 0,
                "requested_files": [],
                "scanned_files": [],
                "skipped_files": [],
            },
        }
        return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if output_format == "csv":
        buffer = io.StringIO(newline="")
        writer = csv.DictWriter(buffer, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(findings)
        return buffer.getvalue()
    if output_format == "text":
        lines = [f"说明：{notice}"]
        for item in findings:
            state = "受保护" if item["protected"] else "已豁免" if item["excluded"] else "候选"
            lines.append(
                f"{item['file']}:{item['line']}:{item['column']} "
                f"[{item['signal_id']}/{item['severity']}/{item['action']}/{state}] "
                f"{item['matched']} | count={item['count']} | {item['context']}"
            )
        return "\n".join(lines) + "\n"
    raise ValueError(f"unsupported output format: {output_format}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="定位中文学术文本中的模板词和句壳候选；不判断作者身份。"
    )
    parser.add_argument("paths", nargs="+", help="UTF-8 文本文件或目录")
    parser.add_argument(
        "--scene",
        type=str.upper,
        choices=SCENE_CHOICES,
        default="ALL",
        help="大小写不敏感；AUTO 扫描全部场景信号，GENERAL 只扫描通用信号",
    )
    parser.add_argument("--format", choices=("json", "csv", "text"), default="text", dest="output_format")
    parser.add_argument("--output", help="输出文件；省略时写到标准输出")
    parser.add_argument("--lexicon", default=str(DEFAULT_LEXICON), help="lexical-signals.json 路径")
    parser.add_argument("--include-protected", action="store_true", help="显示代码、数学、注释和引文中的受保护命中")
    parser.add_argument("--include-excluded", action="store_true", help="显示因技术上下文而豁免的命中")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        lexicon = load_lexicon(args.lexicon)
        paths = collect_paths(args.paths)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))

    findings: list[dict[str, Any]] = []
    scanned: list[str] = []
    skipped: list[str] = []
    for path in paths:
        try:
            findings.extend(
                scan_file(
                    path,
                    scene=args.scene,
                    lexicon=lexicon,
                    include_protected=args.include_protected,
                    include_excluded=args.include_excluded,
                )
            )
            scanned.append(str(path))
        except UnicodeDecodeError:
            skipped.append(str(path))

    coverage = {
        "status": "REVIEW" if skipped else "PASS",
        "requested_count": len(paths),
        "scanned_count": len(scanned),
        "skipped_count": len(skipped),
        "requested_files": [str(path) for path in paths],
        "scanned_files": scanned,
        "skipped_files": skipped,
    }
    rendered = render_output(
        findings,
        output_format=args.output_format,
        notice=lexicon["output_policy"],
        coverage=coverage,
    )
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8", newline="")
    else:
        sys.stdout.write(rendered)
    for path in skipped:
        print(f"跳过非 UTF-8 或乱码文件：{path}", file=sys.stderr)
    return 2 if skipped else 0


if __name__ == "__main__":
    raise SystemExit(main())
