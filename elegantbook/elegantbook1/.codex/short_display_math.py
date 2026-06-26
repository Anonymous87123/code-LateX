# -*- coding: utf-8 -*-
"""Audit and inline short LaTeX display math blocks.

The width estimator is intentionally heuristic.  It is adapted from the
user-provided sketch, with nested braces and common math commands handled so
the report is stable enough to guide mechanical edits.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


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

SKIP_ACTIVE_ENVS = {
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
    "multicols",
    "pmatrix",
    "shortexenum",
    "shorttrienum",
    "split",
    "tabular",
    "tabularx",
    "vmatrix",
}

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

INLINE_UNSAFE = re.compile(
    r"\\(?:begin|end|label|tag|nonumber|notag|displaybreak|intertext)\b|&|\\\\"
)


@dataclass
class DisplayBlock:
    index: int
    kind: str
    start: int
    end: int
    content_start: int
    content_end: int
    line: int
    end_line: int
    ratio: float
    units: float
    low_width: bool
    structural: bool
    active_envs: str
    inline_safe: bool
    skip_reason: str
    preview: str


def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def strip_comments(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        cut = len(line)
        search = 0
        while True:
            pos = line.find("%", search)
            if pos < 0:
                break
            if pos == 0 or line[pos - 1] != "\\":
                cut = pos
                break
            search = pos + 1
        out.append(line[:cut])
    return "\n".join(out)


def read_braced(text: str, start: int) -> tuple[str, int] | None:
    pos = start
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos >= len(text) or text[pos] != "{":
        return None
    depth = 0
    escaped = False
    for idx in range(pos, len(text)):
        ch = text[idx]
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
                return text[pos + 1 : idx], idx + 1
    return None


def estimate_units(expr: str) -> float:
    """Return an approximate rendered width in average text characters."""
    s = strip_comments(expr)
    s = re.sub(r"\\begin\{[^{}]+\}|\\end\{[^{}]+\}", " ", s)
    s = s.replace(r"\\", "\n")
    parts = [part for part in re.split(r"\n|&", s) if part.strip()]
    if len(parts) > 1:
        return max(estimate_units(part) for part in parts)
    s = s.strip()

    total = 0.0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch.isspace() or ch in "{}":
            i += 1
            continue
        if ch == "\\":
            match = re.match(r"\\[a-zA-Z]+[*]?", s[i:])
            if not match:
                cmd = s[i : i + 2]
                total += {
                    r"\,": 0.5,
                    r"\!": -0.5,
                    r"\;": 1.0,
                    r"\:": 1.0,
                    r"\ ": 1.0,
                    r"\{": 1.0,
                    r"\}": 1.0,
                }.get(cmd, 1.0)
                i += 2
                continue

            cmd = match.group(0)
            i += len(cmd)

            if cmd in (
                r"\left",
                r"\right",
                r"\middle",
                r"\big",
                r"\Big",
                r"\bigg",
                r"\Bigg",
                r"\bigl",
                r"\bigr",
                r"\Bigl",
                r"\Bigr",
                r"\displaystyle",
                r"\textstyle",
                r"\scriptstyle",
                r"\scriptscriptstyle",
            ):
                continue
            if cmd == r"\quad":
                total += 4.0
                continue
            if cmd == r"\qquad":
                total += 8.0
                continue
            if cmd in (r"\sum", r"\int", r"\prod"):
                total += 3.5
                continue
            if cmd in (r"\iint", r"\iiint", r"\oint"):
                total += 4.5
                continue
            if cmd in (r"\cdot", r"\times", r"\le", r"\leq", r"\leqslant", r"\ge", r"\geq", r"\geqslant", r"\neq", r"\approx", r"\sim"):
                total += 2.5
                continue
            if cmd in (r"\to", r"\rightarrow", r"\Rightarrow", r"\implies", r"\Longrightarrow"):
                total += 3.0
                continue
            if cmd in (r"\lim", r"\max", r"\min"):
                total += 3.0
                continue
            if cmd in (r"\ln", r"\sin", r"\cos", r"\tan", r"\exp"):
                total += 2.0
                continue
            if cmd in (r"\arctan", r"\arcsin", r"\arccos"):
                total += 3.0
                continue
            if cmd in (r"\frac", r"\dfrac", r"\tfrac", r"\binom"):
                first = read_braced(s, i)
                if first:
                    second = read_braced(s, first[1])
                    if second:
                        total += max(estimate_units(first[0]), estimate_units(second[0])) + 1.5
                        i = second[1]
                        continue
                total += 4.0
                continue
            if cmd in (
                r"\sqrt",
                r"\abs",
                r"\qty",
                r"\vb",
                r"\vec",
                r"\overline",
                r"\bar",
                r"\hat",
                r"\tilde",
                r"\boxed",
            ):
                if i < len(s) and s[i] == "[":
                    end_opt = s.find("]", i + 1)
                    if end_opt >= 0:
                        i = end_opt + 1
                arg = read_braced(s, i)
                if arg:
                    total += estimate_units(arg[0]) + (2.0 if cmd in (r"\sqrt", r"\boxed") else 1.0)
                    i = arg[1]
                    continue
                total += 2.0
                continue
            if cmd in (r"\text", r"\mathrm", r"\mathbf", r"\mathit", r"\mathbb", r"\mathcal", r"\mathscr", r"\operatorname"):
                arg = read_braced(s, i)
                if arg:
                    visible = re.sub(r"\\[a-zA-Z]+", "", arg[0]).strip()
                    total += max(1.0, len(visible))
                    i = arg[1]
                    continue
                total += 1.0
                continue

            total += 1.0
            continue

        if ch in "=+-":
            total += 2.0
        elif ch in "<>":
            total += 1.5
        elif ch in "(),.[]|;:":
            total += 0.8
        elif "\u4e00" <= ch <= "\u9fff":
            total += 2.0
        else:
            total += 1.0
        i += 1
    return max(total, 0.0)


def estimate_ratio(expr: str) -> float:
    return round(estimate_units(expr) / TEXTWIDTH_UNITS, 2)


def find_token(text: str, token: str, start: int) -> int:
    pos = start
    while True:
        found = text.find(token, pos)
        if found < 0:
            return -1
        if found == 0 or text[found - 1] != "\\":
            return found
        pos = found + 1


def find_displays(text: str) -> list[tuple[str, int, int, int, int]]:
    starts: list[tuple[int, str, str, str]] = []

    search = 0
    while True:
        start = find_token(text, r"\[", search)
        if start < 0:
            break
        starts.append((start, "bracket", r"\[", r"\]"))
        search = start + 2

    search = 0
    while True:
        start = text.find("$$", search)
        if start < 0:
            break
        if start == 0 or text[start - 1] != "\\":
            starts.append((start, "dollar", "$$", "$$"))
        search = start + 2

    for env in DISPLAY_ENVS:
        pattern = re.compile(r"\\begin\{" + re.escape(env) + r"\}")
        for match in pattern.finditer(text):
            starts.append((match.start(), f"env:{env}", match.group(0), r"\end{" + env + "}"))

    starts.sort(key=lambda item: item[0])
    blocks: list[tuple[str, int, int, int, int]] = []
    occupied_until = -1
    for start, kind, start_token, end_token in starts:
        if start < occupied_until:
            continue
        content_start = start + len(start_token)
        end = find_token(text, end_token, content_start) if kind == "bracket" else text.find(end_token, content_start)
        if end < 0:
            continue
        full_end = end + len(end_token)
        blocks.append((kind, start, full_end, content_start, end))
        occupied_until = full_end
    return blocks


def env_stack_at_offsets(text: str, offsets: list[int]) -> dict[int, set[str]]:
    env_pat = re.compile(r"\\(begin|end)\{([^{}]+)\}")
    wanted = sorted(offsets)
    stacks: dict[int, set[str]] = {}
    stack: list[str] = []
    cursor = 0

    for match in env_pat.finditer(text):
        while cursor < len(wanted) and wanted[cursor] <= match.start():
            stacks[wanted[cursor]] = set(stack)
            cursor += 1
        kind, env = match.groups()
        if kind == "begin":
            stack.append(env)
        else:
            for pos in range(len(stack) - 1, -1, -1):
                if stack[pos] == env:
                    del stack[pos:]
                    break
    while cursor < len(wanted):
        stacks[wanted[cursor]] = set(stack)
        cursor += 1
    return stacks


def is_structural(kind: str, content: str) -> bool:
    if kind != "bracket":
        return True
    clean = strip_comments(content)
    if any(marker in clean for marker in STRUCTURAL_MARKERS):
        return True
    if r"\\" in clean or "&" in clean:
        return True
    if len([line for line in clean.splitlines() if line.strip()]) > 3:
        return True
    return False


def normalize_inline(content: str) -> str:
    clean = strip_comments(content).strip()
    clean = re.sub(r"\s+", " ", clean)
    clean = clean.replace(r"\displaystyle", "")
    clean = clean.replace(r"\dfrac", r"\frac")
    clean = re.sub(r"\s+", " ", clean)
    return clean.strip()


def line_bounds(text: str, pos: int) -> tuple[int, int]:
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    if end < 0:
        end = len(text)
    return start, end


def neighbor_lines(text: str, start: int, end: int) -> tuple[str, str]:
    prev_end = text.rfind("\n", 0, start)
    if prev_end < 0:
        prev_line = ""
    else:
        prev_start = text.rfind("\n", 0, prev_end) + 1
        prev_line = text[prev_start:prev_end]
    next_start = text.find("\n", end)
    if next_start < 0:
        next_line = ""
    else:
        next_end = text.find("\n", next_start + 1)
        if next_end < 0:
            next_end = len(text)
        next_line = text[next_start + 1 : next_end]
    return prev_line, next_line


def decide_inline_safe(text: str, kind: str, start: int, end: int, content: str, ratio: float, active_envs: set[str]) -> tuple[bool, str]:
    clean = strip_comments(content).strip()
    if ratio >= LOW_RATIO:
        return False, "wide"
    if kind != "bracket":
        return False, "display_environment"
    if not clean:
        return False, "empty"
    if INLINE_UNSAFE.search(clean):
        return False, "inline_unsafe_marker"
    if clean.count(r"\left") != clean.count(r"\right"):
        return False, "unbalanced_left_right"
    skipped_envs = sorted(active_envs & SKIP_ACTIVE_ENVS)
    if skipped_envs:
        return False, "inside_" + ",".join(skipped_envs)
    prev_line, next_line = neighbor_lines(text, start, end)
    if not prev_line.strip() and not next_line.strip():
        return False, "isolated_by_blank_lines"
    if "\n\n" in clean:
        return False, "paragraph_break"
    if estimate_ratio(normalize_inline(content)) >= LOW_RATIO:
        return False, "normalized_width_not_low"
    return True, "inline_safe"


def analyze(path: Path) -> tuple[str, list[DisplayBlock]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    raw = find_displays(text)
    stacks = env_stack_at_offsets(text, [start for _, start, _, _, _ in raw])
    blocks: list[DisplayBlock] = []
    for idx, (kind, start, end, content_start, content_end) in enumerate(raw, start=1):
        content = text[content_start:content_end]
        units = round(estimate_units(content), 2)
        ratio = round(units / TEXTWIDTH_UNITS, 2)
        structural = is_structural(kind, content)
        active_envs = stacks.get(start, set())
        safe, reason = decide_inline_safe(text, kind, start, end, content, ratio, active_envs)
        if structural and safe:
            safe, reason = False, "structural"
        preview = re.sub(r"\s+", " ", content.strip())
        if len(preview) > 180:
            preview = preview[:177] + "..."
        blocks.append(
            DisplayBlock(
                index=idx,
                kind=kind,
                start=start,
                end=end,
                content_start=content_start,
                content_end=content_end,
                line=line_no(text, start),
                end_line=line_no(text, end),
                ratio=ratio,
                units=units,
                low_width=ratio < LOW_RATIO,
                structural=structural,
                active_envs=",".join(sorted(active_envs)),
                inline_safe=safe,
                skip_reason=reason,
                preview=preview,
            )
        )
    return text, blocks


def replacement_for(text: str, block: DisplayBlock) -> str:
    body = normalize_inline(text[block.content_start : block.content_end])
    replacement = rf"\({body}\)"
    before = text[block.start - 1] if block.start > 0 else ""
    after = text[block.end] if block.end < len(text) else ""
    if before and not before.isspace() and before not in "([{":
        replacement = " " + replacement
    if after and not after.isspace() and after not in ".,;:，。；：、)]}":
        replacement += " "
    return replacement


def has_same_line_text(text: str, block: DisplayBlock) -> bool:
    line_start, _ = line_bounds(text, block.start)
    _, line_end = line_bounds(text, block.end)
    before = text[line_start:block.start].strip()
    after = text[block.end:line_end].strip()
    return bool(before or after)


def has_close_sentence_context(text: str, block: DisplayBlock) -> bool:
    prev_line, next_line = neighbor_lines(text, block.start, block.end)
    prev = prev_line.strip()
    next_ = next_line.strip()
    if not prev and not next_:
        return False
    if prev.startswith("\\") or next_.startswith("\\"):
        return False
    return True


def select_inline_candidates(
    text: str,
    blocks: list[DisplayBlock],
    max_ratio: float,
    context_mode: str,
    exclude: set[int],
) -> list[DisplayBlock]:
    chosen: list[DisplayBlock] = []
    for block in blocks:
        if not block.inline_safe or block.index in exclude or block.ratio > max_ratio:
            continue
        same_line = has_same_line_text(text, block)
        close_sentence = has_close_sentence_context(text, block)
        if context_mode == "all":
            chosen.append(block)
        elif context_mode == "embedded" and same_line:
            chosen.append(block)
        elif context_mode == "sentence" and (same_line or close_sentence):
            chosen.append(block)
        elif context_mode == "short-standalone" and (same_line or block.ratio <= 0.25):
            chosen.append(block)
    return chosen


def apply_inline(
    path: Path,
    output: Path | None = None,
    limit: int | None = None,
    exclude: set[int] | None = None,
    max_ratio: float = LOW_RATIO,
    context_mode: str = "all",
) -> list[DisplayBlock]:
    text, blocks = analyze(path)
    exclude = exclude or set()
    chosen = select_inline_candidates(text, blocks, max_ratio, context_mode, exclude)
    if limit is not None:
        chosen = chosen[:limit]
    out = text
    for block in reversed(chosen):
        out = out[: block.start] + replacement_for(text, block) + out[block.end :]
    target = output or path
    target.write_text(out, encoding="utf-8", newline="\n")
    return chosen


def write_reports(blocks: list[DisplayBlock], report_prefix: Path) -> dict[str, object]:
    report_prefix.parent.mkdir(parents=True, exist_ok=True)
    low = [block for block in blocks if block.low_width]
    safe = [block for block in low if block.inline_safe]
    by_status: dict[str, int] = {}
    for block in low:
        status = "inline_safe" if block.inline_safe else block.skip_reason
        by_status[status] = by_status.get(status, 0) + 1
    summary = {
        "total_display_blocks": len(blocks),
        "low_width_lt_0_5": len(low),
        "inline_safe": len(safe),
        "threshold_ratio": LOW_RATIO,
        "textwidth_units": TEXTWIDTH_UNITS,
        "low_width_by_status": dict(sorted(by_status.items())),
    }
    payload = {"summary": summary, "blocks": [asdict(block) for block in blocks]}
    report_prefix.with_suffix(".json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    with report_prefix.with_suffix(".csv").open("w", encoding="utf-8-sig", newline="") as fh:
        fields = list(asdict(blocks[0]).keys()) if blocks else list(DisplayBlock.__dataclass_fields__)
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for block in blocks:
            writer.writerow(asdict(block))

    lines = [
        "# Short Display Math Audit",
        "",
        f"- total display blocks: {summary['total_display_blocks']}",
        f"- ratio < 0.5: {summary['low_width_lt_0_5']}",
        f"- inline-safe candidates: {summary['inline_safe']}",
        "",
        "## Low-Width Blocks",
        "",
        "| index | lines | ratio | status | kind | preview |",
        "|---:|---:|---:|---|---|---|",
    ]
    for block in low:
        status = "inline_safe" if block.inline_safe else block.skip_reason
        preview = block.preview.replace("|", r"\|")
        lines.append(f"| {block.index} | {block.line}-{block.end_line} | {block.ratio:.2f} | {status} | {block.kind} | `{preview}` |")
    report_prefix.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def parse_exclude(path: Path | None) -> set[int]:
    if path is None or not path.exists():
        return set()
    raw = path.read_text(encoding="utf-8").strip()
    return {int(part) for part in re.split(r"[\s,]+", raw) if part}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tex", type=Path)
    parser.add_argument("--report-prefix", type=Path, default=Path(".codex/short_display_math_report"))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--exclude-index-file", type=Path)
    parser.add_argument("--max-ratio", type=float, default=LOW_RATIO)
    parser.add_argument(
        "--context-mode",
        choices=("all", "embedded", "sentence", "short-standalone"),
        default="all",
        help="extra selection rule used only with --apply",
    )
    args = parser.parse_args()

    if args.apply:
        chosen = apply_inline(
            args.tex,
            args.output,
            args.limit,
            parse_exclude(args.exclude_index_file),
            args.max_ratio,
            args.context_mode,
        )
        print(json.dumps({"applied": len(chosen), "output": str(args.output or args.tex)}, ensure_ascii=False, indent=2))

    _, blocks = analyze(args.output or args.tex)
    summary = write_reports(blocks, args.report_prefix)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
