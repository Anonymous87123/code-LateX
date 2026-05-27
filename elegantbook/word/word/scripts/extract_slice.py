#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extract a slice of word.tex into tmp/slice.tex for faster compilation/visual review.

Modes:
- by index range: --start-idx N --end-idx M
- by chapter title (exact match on \chapter{...}): --chapter "HOM, HUM"

Output:
- tmp/slice.tex (standalone document)

Notes:
- Keeps the same documentclass and preamble from the original word.tex
  up to \begin{document}, then injects minimal frontmatter.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEX = ROOT / "word.tex"
OUT_DIR = ROOT / "tmp"
OUT_TEX = OUT_DIR / "slice.tex"

BEGIN_DOC_RE = re.compile(r"^\\begin\{document\}\s*$")
BEGIN_WORD_RE = re.compile(r"^\\begin\{word\}(?:\[[^\]]*\])?\{(?P<head>[^}]*)\}\{(?P<ipa>[^}]*)\}\s*$")
END_WORD_RE = re.compile(r"^\\end\{word\}\s*$")
CHAPTER_RE = re.compile(r"^\\chapter\{(?P<title>[^}]*)\}\s*$")


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def find_preamble(lines: list[str]) -> tuple[list[str], int]:
    for i, ln in enumerate(lines):
        if BEGIN_DOC_RE.match(ln):
            return lines[: i + 1], i
    raise RuntimeError("missing \\begin{document}")


def iter_word_blocks(lines: list[str], start_line0: int = 0):
    i = start_line0
    idx = 0
    while i < len(lines):
        m = BEGIN_WORD_RE.match(lines[i])
        if not m:
            i += 1
            continue
        idx += 1
        start = i
        i += 1
        while i < len(lines) and not END_WORD_RE.match(lines[i]):
            i += 1
        end = i if i < len(lines) else len(lines) - 1
        if i < len(lines):
            end = i
        yield idx, start, end, lines[start : end + 1]
        i += 1


def slice_by_idx(lines: list[str], start_idx: int, end_idx: int) -> list[str]:
    out: list[str] = []
    for idx, _s, _e, block in iter_word_blocks(lines):
        if idx < start_idx:
            continue
        if idx > end_idx:
            break
        out.extend(block)
        out.append("")
    return out


def slice_by_chapter(lines: list[str], chapter: str) -> list[str]:
    # include the chapter heading + following until next chapter heading
    out: list[str] = []
    in_ch = False
    for ln in lines:
        m = CHAPTER_RE.match(ln)
        if m:
            title = m.group("title")
            if in_ch:
                break
            if title == chapter:
                in_ch = True
        if in_ch:
            out.append(ln)
    if not out:
        raise RuntimeError(f"chapter not found: {chapter}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", type=str, default=str(DEFAULT_TEX))
    ap.add_argument("--start-idx", type=int, default=0)
    ap.add_argument("--end-idx", type=int, default=0)
    ap.add_argument("--chapter", type=str, default="")
    args = ap.parse_args()

    tex_path = Path(args.tex)
    lines = read_lines(tex_path)
    preamble, doc_i = find_preamble(lines)

    if args.chapter:
        body = slice_by_chapter(lines[doc_i + 1 :], args.chapter)
    else:
        if not (args.start_idx and args.end_idx and args.start_idx <= args.end_idx):
            raise SystemExit("must provide --chapter or --start-idx/--end-idx")
        body = slice_by_idx(lines[doc_i + 1 :], args.start_idx, args.end_idx)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_lines: list[str] = []
    out_lines.extend(preamble)
    out_lines.append("\\frontmatter")
    out_lines.append("\\chapter{Slice}")
    out_lines.append("\\mainmatter")
    out_lines.append("")
    out_lines.extend(body)
    out_lines.append("")
    out_lines.append("\\end{document}")
    OUT_TEX.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_TEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

