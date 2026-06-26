# -*- coding: utf-8 -*-
"""Audit display math width across elegantbook2.tex.

The estimator is adapted from the user-provided Gemini sketch, with two
practical changes:
- parse nested brace arguments for common width-bearing commands;
- classify structural displays separately from simple formulas that may be
  candidates for inline conversion.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX_PATH = ROOT / "elegantbook2.tex"
OUT_CSV = ROOT / "solution_quality_audit" / "display_width_audit.csv"
OUT_MD = ROOT / "solution_quality_audit" / "display_width_audit.md"
OUT_JSON = ROOT / "solution_quality_audit" / "display_width_summary.json"

TEXTWIDTH_UNITS = 70.0
LOW_RATIO = 0.50

DISPLAY_ENVS = (
    "equation",
    "equation*",
    "align",
    "align*",
    "gather",
    "gather*",
    "multline",
    "multline*",
)

STRUCTURAL_MARKERS = (
    r"\begin{cases}",
    r"\begin{matrix}",
    r"\begin{pmatrix}",
    r"\begin{bmatrix}",
    r"\begin{vmatrix}",
    r"\begin{Vmatrix}",
    r"\begin{array}",
    r"\begin{aligned}",
    r"\begin{gathered}",
    r"\begin{split}",
    r"\begin{tikzpicture}",
)


@dataclass
class DisplayBlock:
    index: int
    kind: str
    start_line: int
    end_line: int
    content: str
    ratio: float
    units: float
    low_width: bool
    structural: bool
    simple_inline_candidate: bool
    context: str
    preview: str


def read_lines() -> list[str]:
    return TEX_PATH.read_text(encoding="utf-8", errors="replace").splitlines()


def find_matching_brace(text: str, open_index: int) -> int:
    depth = 0
    escaped = False
    for pos in range(open_index, len(text)):
        ch = text[pos]
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return pos
    return -1


def consume_braced(text: str, start: int) -> tuple[str, int] | None:
    pos = start
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos >= len(text) or text[pos] != "{":
        return None
    end = find_matching_brace(text, pos)
    if end == -1:
        return None
    return text[pos + 1 : end], end + 1


def strip_outer_display(latex: str) -> str:
    latex = latex.strip()
    if latex.startswith(r"\[") and latex.endswith(r"\]"):
        latex = latex[2:-2].strip()
    return latex


def estimate_units(latex_str: str) -> float:
    latex = strip_outer_display(latex_str)
    total = 0.0

    # Remove comments and spacing-only commands that do not draw glyphs.
    latex = re.sub(r"(?<!\\)%.*", "", latex)
    latex = re.sub(r"\\(?:left|right|bigl|bigr|Bigl|Bigr|big|Big|bigg|Bigg)\b", "", latex)
    latex = re.sub(r"\\(?:displaystyle|textstyle|scriptstyle|scriptscriptstyle)\b", "", latex)
    latex = re.sub(r"\\(?:mathrm|mathbf|mathit|mathbb|mathcal|mathscr|operatorname)\s*\{([^{}]*)\}", r"\1", latex)

    # Nested common wrappers.
    changed = True
    while changed:
        changed = False
        for cmd, overhead in ((r"\sqrt", 2.0),):
            idx = latex.find(cmd)
            if idx == -1:
                continue
            opt_end = idx + len(cmd)
            if opt_end < len(latex) and latex[opt_end] == "[":
                close = latex.find("]", opt_end + 1)
                if close != -1:
                    opt_end = close + 1
            consumed = consume_braced(latex, opt_end)
            if not consumed:
                continue
            body, end = consumed
            total += estimate_units(body) + overhead
            latex = latex[:idx] + latex[end:]
            changed = True
            break

    # Fractions: horizontal footprint is mostly max(numerator, denominator).
    frac_commands = (r"\frac", r"\dfrac", r"\tfrac", r"\binom")
    changed = True
    while changed:
        changed = False
        for cmd in frac_commands:
            idx = latex.find(cmd)
            if idx == -1:
                continue
            first = consume_braced(latex, idx + len(cmd))
            if not first:
                continue
            numerator, pos = first
            second = consume_braced(latex, pos)
            if not second:
                continue
            denominator, end = second
            total += max(estimate_units(numerator), estimate_units(denominator)) + 1.0
            latex = latex[:idx] + latex[end:]
            changed = True
            break

    command_weights = {
        r"\le": 3,
        r"\ge": 3,
        r"\neq": 3,
        r"\approx": 3,
        r"\sim": 2,
        r"\to": 3,
        r"\rightarrow": 3,
        r"\leftarrow": 3,
        r"\cdot": 2,
        r"\times": 2,
        r"\pm": 2,
        r"\mp": 2,
        r"\sum": 4,
        r"\prod": 4,
        r"\int": 4,
        r"\iint": 5,
        r"\iiint": 6,
        r"\oint": 5,
        r"\lim": 3,
        r"\max": 3,
        r"\min": 3,
        r"\ln": 2,
        r"\sin": 2,
        r"\cos": 2,
        r"\tan": 2,
        r"\arctan": 3,
        r"\quad": 6,
        r"\qquad": 12,
        r"\,": 1,
        r"\;": 2,
        r"\:": 2,
        r"\!": -1,
    }
    for cmd, weight in sorted(command_weights.items(), key=lambda item: -len(item[0])):
        count = latex.count(cmd)
        if count:
            total += count * weight
            latex = latex.replace(cmd, "")

    # Relation/operator characters with math spacing.
    char_weights = {
        "=": 3,
        "+": 2,
        "-": 2,
        "<": 2,
        ">": 2,
        ":": 1,
        ",": 1,
        ";": 1,
        "(": 1,
        ")": 1,
        "[": 1,
        "]": 1,
        "|": 1,
    }
    for ch, weight in char_weights.items():
        total += latex.count(ch) * weight
        latex = latex.replace(ch, "")

    # Sub/superscript markers are not full glyphs, but their contents count.
    latex = latex.replace("^", "").replace("_", "")
    latex = latex.replace("{", "").replace("}", "")

    remaining_commands = re.findall(r"\\[a-zA-Z]+", latex)
    total += len(remaining_commands)
    latex = re.sub(r"\\[a-zA-Z]+", "", latex)

    total += len(re.findall(r"[a-zA-Z0-9\u0391-\u03ff]", latex))
    return max(total, 0.0)


def estimate_ratio(latex_str: str) -> float:
    return round(estimate_units(latex_str) / TEXTWIDTH_UNITS, 2)


def current_context(line: str, current: dict[str, str]) -> None:
    for kind in ("chapter", "section", "subsection"):
        match = re.match(rf"\\{kind}\{{(.+)\}}", line)
        if match:
            current[kind] = match.group(1)
            if kind == "chapter":
                current["section"] = ""
                current["subsection"] = ""
            elif kind == "section":
                current["subsection"] = ""


def context_label(current: dict[str, str]) -> str:
    return " / ".join(part for part in [current["chapter"], current["section"], current["subsection"]] if part)


def collect_blocks(lines: list[str]) -> list[DisplayBlock]:
    blocks: list[DisplayBlock] = []
    current = {"chapter": "", "section": "", "subsection": ""}
    index = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        current_context(line, current)
        stripped = line.strip()

        if stripped == r"\[":
            start = i
            buf: list[str] = []
            i += 1
            while i < len(lines) and lines[i].strip() != r"\]":
                buf.append(lines[i])
                i += 1
            if i < len(lines):
                index += 1
                content = "\n".join(buf).strip()
                blocks.append(make_block(index, "bracket", start + 1, i + 1, content, context_label(current)))
            i += 1
            continue

        env_match = re.match(r"\\begin\{([^{}]+)\}", stripped)
        if env_match and env_match.group(1) in DISPLAY_ENVS:
            env = env_match.group(1)
            start = i
            buf = []
            i += 1
            end_pat = rf"\end{{{env}}}"
            while i < len(lines) and end_pat not in lines[i]:
                buf.append(lines[i])
                i += 1
            if i < len(lines):
                index += 1
                content = "\n".join(buf).strip()
                blocks.append(make_block(index, env, start + 1, i + 1, content, context_label(current)))
            i += 1
            continue

        i += 1

    return blocks


def is_structural(content: str, kind: str) -> bool:
    if kind != "bracket":
        return True
    if any(marker in content for marker in STRUCTURAL_MARKERS):
        return True
    if r"\\" in content or "&" in content:
        return True
    if len([line for line in content.splitlines() if line.strip()]) > 3:
        return True
    return False


def make_block(index: int, kind: str, start_line: int, end_line: int, content: str, context: str) -> DisplayBlock:
    units = round(estimate_units(content), 2)
    ratio = round(units / TEXTWIDTH_UNITS, 2)
    structural = is_structural(content, kind)
    preview = " ".join(content.split())[:220]
    return DisplayBlock(
        index=index,
        kind=kind,
        start_line=start_line,
        end_line=end_line,
        content=content,
        ratio=ratio,
        units=units,
        low_width=ratio < LOW_RATIO,
        structural=structural,
        simple_inline_candidate=ratio < LOW_RATIO and not structural,
        context=context,
        preview=preview,
    )


def write_outputs(blocks: list[DisplayBlock]) -> None:
    fields = [
        "index",
        "kind",
        "start_line",
        "end_line",
        "ratio",
        "units",
        "low_width",
        "structural",
        "simple_inline_candidate",
        "context",
        "preview",
    ]
    summary = {
        "total_display_blocks": len(blocks),
        "low_width_lt_0_5": sum(1 for block in blocks if block.low_width),
        "simple_inline_candidates": sum(1 for block in blocks if block.simple_inline_candidate),
        "structural_low_width": sum(1 for block in blocks if block.low_width and block.structural),
        "threshold_ratio": LOW_RATIO,
        "textwidth_units": TEXTWIDTH_UNITS,
    }

    md: list[str] = []
    md.append("# Display Width Audit\n\n")
    md.append("Estimator: adapted from the user-provided Gemini heuristic; full line is 70 units.\n\n")
    md.append("## Summary\n\n")
    for key, value in summary.items():
        md.append(f"- `{key}`: {value}\n")
    md.append("\n## Low-Width Simple Inline Candidates\n\n")
    md.append("| # | lines | ratio | context | preview |\n")
    md.append("|---:|---:|---:|---|---|\n")
    for block in blocks:
        if block.simple_inline_candidate:
            preview = block.preview.replace("|", r"\|")
            context = block.context.replace("|", r"\|")
            md.append(f"| {block.index} | {block.start_line}-{block.end_line} | {block.ratio:.2f} | {context} | `{preview}` |\n")
    md.append("\n## Low-Width But Structural Or Non-Bracket\n\n")
    md.append("| # | kind | lines | ratio | context | preview |\n")
    md.append("|---:|---|---:|---:|---|---|\n")
    for block in blocks:
        if block.low_width and not block.simple_inline_candidate:
            preview = block.preview.replace("|", r"\|")
            context = block.context.replace("|", r"\|")
            md.append(f"| {block.index} | {block.kind} | {block.start_line}-{block.end_line} | {block.ratio:.2f} | {context} | `{preview}` |\n")
    try:
        with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for block in blocks:
                writer.writerow({field: getattr(block, field) for field in fields})
        OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        OUT_MD.write_text("".join(md), encoding="utf-8")
    except PermissionError as exc:
        summary["write_warning"] = str(exc)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("\nLOW_WIDTH_SIMPLE_INLINE_CANDIDATES_HEAD")
    for block in [item for item in blocks if item.simple_inline_candidate][:120]:
        print(
            f"{block.index}\t{block.start_line}-{block.end_line}\t"
            f"{block.ratio:.2f}\t{block.context}\t{block.preview}"
        )


def main() -> None:
    write_outputs(collect_blocks(read_lines()))


if __name__ == "__main__":
    main()
