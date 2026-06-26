# -*- coding: utf-8 -*-
r"""Inline short display math blocks in elegantbook2.tex.

This is a conservative companion to audit_display_width.py.  It only rewrites
simple ``\[...\]`` displays whose estimated width is below 0.5 textwidth, and
leaves numbered/structural environments alone.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from audit_display_width import LOW_RATIO, TEX_PATH, collect_blocks, estimate_ratio, read_lines


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "tmp" / "inline_short_display_report.json"
REPORT_MD = ROOT / "tmp" / "inline_short_display_report.md"

SKIP_ENVS = {
    "align",
    "align*",
    "array",
    "bmatrix",
    "cases",
    "equation",
    "equation*",
    "gather",
    "gather*",
    "matrix",
    "minipage",
    "multicols",
    "pmatrix",
    "shortexenum",
    "shorttrienum",
    "split",
    "tabular",
    "tabularx",
    "tikzpicture",
    "vmatrix",
}

INLINE_UNSAFE_MARKERS = (
    r"\begin{",
    r"\end{",
    r"\tag",
    r"\label",
    r"\nonumber",
    r"\displaybreak",
)

STRUCTURAL_LINE = re.compile(
    r"^\s*\\(?:chapter|section|subsection|subsubsection|paragraph|begin|end|caption|includegraphics|input|include)\b"
)


@dataclass
class CandidateDecision:
    index: int
    start_line: int
    end_line: int
    ratio: float
    action: str
    reason: str
    preview: str


def read_text_preserve_newline(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    newline = "\r\n" if text.count("\r\n") > text.count("\n") - text.count("\r\n") else "\n"
    return text, newline


def env_stack_by_line(lines: list[str]) -> list[set[str]]:
    stack: list[str] = []
    stacks: list[set[str]] = []
    env_pat = re.compile(r"\\(begin|end)\{([^{}]+)\}")
    for line in lines:
        stacks.append(set(stack))
        for match in env_pat.finditer(line):
            kind, env = match.groups()
            if kind == "begin":
                stack.append(env)
            else:
                for pos in range(len(stack) - 1, -1, -1):
                    if stack[pos] == env:
                        del stack[pos:]
                        break
    return stacks


def normalize_inline_content(content: str) -> str:
    content = re.sub(r"(?<!\\)%.*", "", content)
    return " ".join(part.strip() for part in content.splitlines() if part.strip())


def line_is_structural(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if STRUCTURAL_LINE.match(stripped):
        return True
    return stripped in {r"\[", r"\]"}


def decide(block, lines: list[str], stacks: list[set[str]]) -> CandidateDecision:
    content = normalize_inline_content(block.content)
    preview = content[:180]
    if not block.simple_inline_candidate:
        return CandidateDecision(block.index, block.start_line, block.end_line, block.ratio, "skip", "not_simple_low_width", preview)
    if block.kind != "bracket":
        return CandidateDecision(block.index, block.start_line, block.end_line, block.ratio, "skip", "not_bracket_display", preview)
    if any(marker in content for marker in INLINE_UNSAFE_MARKERS):
        return CandidateDecision(block.index, block.start_line, block.end_line, block.ratio, "skip", "inline_unsafe_marker", preview)
    if r"\\" in content or "&" in content:
        return CandidateDecision(block.index, block.start_line, block.end_line, block.ratio, "skip", "alignment_marker", preview)
    active_envs = stacks[block.start_line - 1]
    skipped_envs = sorted(active_envs & SKIP_ENVS)
    if skipped_envs:
        return CandidateDecision(
            block.index,
            block.start_line,
            block.end_line,
            block.ratio,
            "skip",
            "inside_" + ",".join(skipped_envs),
            preview,
        )
    prev_line = lines[block.start_line - 2] if block.start_line >= 2 else ""
    next_line = lines[block.end_line] if block.end_line < len(lines) else ""
    if line_is_structural(prev_line) and line_is_structural(next_line):
        return CandidateDecision(block.index, block.start_line, block.end_line, block.ratio, "skip", "between_structural_lines", preview)
    if not prev_line.strip() and not next_line.strip():
        return CandidateDecision(block.index, block.start_line, block.end_line, block.ratio, "skip", "isolated_by_blank_lines", preview)
    if content.count(r"\left") != content.count(r"\right"):
        return CandidateDecision(block.index, block.start_line, block.end_line, block.ratio, "skip", "unbalanced_left_right", preview)
    # Re-check after whitespace normalization; a borderline block may grow if
    # hidden comments were removed or line breaks carried meaningful spacing.
    if estimate_ratio(content) >= LOW_RATIO:
        return CandidateDecision(block.index, block.start_line, block.end_line, block.ratio, "skip", "normalized_width_not_low", preview)
    return CandidateDecision(block.index, block.start_line, block.end_line, block.ratio, "inline", "simple_low_width", preview)


def apply_inline_rewrites(text: str, newline: str, decisions: list[CandidateDecision]) -> str:
    lines = text.splitlines()
    # Rebuild block content from current lines so the report and replacement stay
    # in lockstep even if another script changed whitespace before this runs.
    for item in sorted((d for d in decisions if d.action == "inline"), key=lambda d: d.start_line, reverse=True):
        start = item.start_line - 1
        end = item.end_line - 1
        body = normalize_inline_content("\n".join(lines[start + 1 : end]))
        lines[start : end + 1] = [rf"\({body}\)"]
    return newline.join(lines) + newline


def write_report(decisions: list[CandidateDecision]) -> None:
    summary = {
        "threshold_ratio": LOW_RATIO,
        "total_low_simple_seen": sum(1 for d in decisions if d.reason != "not_simple_low_width"),
        "inline": sum(1 for d in decisions if d.action == "inline"),
        "skip": sum(1 for d in decisions if d.action == "skip"),
        "reasons": dict(Counter(d.reason for d in decisions)),
    }
    REPORT_JSON.write_text(
        json.dumps({"summary": summary, "decisions": [asdict(d) for d in decisions]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    rows = [d for d in decisions if d.action == "inline"]
    skipped = [d for d in decisions if d.action == "skip" and d.reason != "not_simple_low_width"]
    md: list[str] = []
    md.append("# Inline Short Display Math Report\n\n")
    md.append("## Summary\n\n")
    for key, value in summary.items():
        md.append(f"- `{key}`: {value}\n")
    md.append("\n## Inlined\n\n")
    md.append("| # | lines | ratio | preview |\n")
    md.append("|---:|---:|---:|---|\n")
    for d in rows:
        md.append(f"| {d.index} | {d.start_line}-{d.end_line} | {d.ratio:.2f} | `{d.preview.replace('|', r'\|')}` |\n")
    md.append("\n## Skipped Low Simple Candidates\n\n")
    md.append("| # | lines | ratio | reason | preview |\n")
    md.append("|---:|---:|---:|---|---|\n")
    for d in skipped:
        md.append(
            f"| {d.index} | {d.start_line}-{d.end_line} | {d.ratio:.2f} | {d.reason} | `{d.preview.replace('|', r'\|')}` |\n"
        )
    REPORT_MD.write_text("".join(md), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="rewrite elegantbook2.tex in place")
    args = parser.parse_args()

    text, newline = read_text_preserve_newline(TEX_PATH)
    lines = text.splitlines()
    blocks = collect_blocks(read_lines())
    stacks = env_stack_by_line(lines)
    decisions = [decide(block, lines, stacks) for block in blocks]
    write_report(decisions)

    summary = {
        "inline": sum(1 for d in decisions if d.action == "inline"),
        "skipped_low_simple": sum(1 for d in decisions if d.action == "skip" and d.reason != "not_simple_low_width"),
        "report_json": str(REPORT_JSON.relative_to(ROOT)),
        "report_md": str(REPORT_MD.relative_to(ROOT)),
        "applied": args.apply,
    }
    if args.apply:
        TEX_PATH.write_text(apply_inline_rewrites(text, newline, decisions), encoding="utf-8", newline="")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
