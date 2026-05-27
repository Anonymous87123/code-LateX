#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
QC + progress tracker for word.tex.

Outputs:
- tmp/qc_word_report.csv: one row per word entry, in file order
- tmp/qc_word_report.md: quick summary + top offenders
- tmp/qc_progress.json: persistent progress state keyed by entry index + headword

Rule set matches the user's agreed plan:
- exactly one \wordbreakdown{...}
- at least one \wordfamily{...} and "cognate count" >= 3 (heuristic split by ；/; ,)
- at least one \wordsense{...}; every sense must start with a POS prefix (n./vt./vi./a./ad./prep./conj./pron./interj.)
- for each \wordsense: before next \wordsense or \end{word}, must have >=1 \wordphrase and >=1 \wordexample
- no OCR junk markers: <!--, book p, PDF p, ## LECTURE, replacement char �
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEX = ROOT / "word.tex"
OUT_DIR = ROOT / "tmp"
OUT_CSV = OUT_DIR / "qc_word_report.csv"
OUT_MD = OUT_DIR / "qc_word_report.md"
OUT_PROGRESS = OUT_DIR / "qc_progress.json"


POS_PREFIX_RE = re.compile(
    r"^\s*(?:n|v|vt|vi|a|ad|adv|prep|conj|pron|interj)\.\s*",
    re.IGNORECASE,
)

BEGIN_WORD_RE = re.compile(r"^\\begin\{word\}(?:\[[^\]]*\])?\{(?P<head>[^}]*)\}\{(?P<ipa>[^}]*)\}\s*$")
END_WORD_RE = re.compile(r"^\\end\{word\}\s*$")

CMD_RE = {
    "breakdown": re.compile(r"\\wordbreakdown\{"),
    "sense": re.compile(r"\\wordsense\{"),
    "family": re.compile(r"\\wordfamily\{"),
    "phrase": re.compile(r"\\wordphrase\{"),
    "example": re.compile(r"\\wordexample\{"),
}

JUNK_MARKERS = [
    "<!--",
    "book p",
    "PDF p",
    "## LECTURE",
    "�",
]


@dataclass
class WordEntry:
    idx: int
    headword: str
    ipa: str
    start_line: int
    end_line: int
    lines: List[str]


def _read_lines(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def parse_entries(lines: List[str]) -> List[WordEntry]:
    entries: List[WordEntry] = []
    i = 0
    idx = 0
    while i < len(lines):
        m = BEGIN_WORD_RE.match(lines[i])
        if not m:
            i += 1
            continue
        head = m.group("head").strip()
        ipa = m.group("ipa").strip()
        start_line = i + 1  # 1-based
        buf = [lines[i]]
        i += 1
        while i < len(lines):
            buf.append(lines[i])
            if END_WORD_RE.match(lines[i]):
                end_line = i + 1
                idx += 1
                entries.append(
                    WordEntry(
                        idx=idx,
                        headword=head,
                        ipa=ipa,
                        start_line=start_line,
                        end_line=end_line,
                        lines=buf,
                    )
                )
                break
            i += 1
        i += 1
    return entries


def _count_cmd(entry: WordEntry, cmd: str) -> int:
    pat = CMD_RE[cmd]
    return sum(1 for ln in entry.lines if pat.search(ln))


def _has_junk(entry: WordEntry) -> List[str]:
    hits: List[str] = []
    joined = "\n".join(entry.lines)
    for mk in JUNK_MARKERS:
        if mk in joined:
            hits.append(mk)
    return hits


def _cognate_items_from_family(entry: WordEntry) -> List[str]:
    # Extract content inside \wordfamily{...} on the same line (best-effort).
    # If braces span multiple lines, we just count as 1 item to avoid false precision.
    items: List[str] = []
    for ln in entry.lines:
        if "\\wordfamily{" not in ln:
            continue
        # Try to get one-line brace payload.
        m = re.search(r"\\wordfamily\{(.*)\}\s*$", ln)
        if not m:
            items.append("__multiline__")
            continue
        payload = m.group(1).strip()
        if not payload:
            continue
        # Split by common separators
        parts = re.split(r"[；;，,]\s*", payload)
        parts = [p.strip() for p in parts if p.strip()]
        if parts:
            items.extend(parts)
    return items


def _extract_sense_blocks(entry: WordEntry) -> List[Tuple[int, List[str]]]:
    """
    Return list of (sense_line_no_within_entry, block_lines_including_sense_line)
    where each block spans from its \wordsense line up to before next \wordsense or \end{word}.
    """
    sense_line_idxs = [j for j, ln in enumerate(entry.lines) if "\\wordsense{" in ln]
    blocks: List[Tuple[int, List[str]]] = []
    for k, j in enumerate(sense_line_idxs):
        j2 = sense_line_idxs[k + 1] if k + 1 < len(sense_line_idxs) else len(entry.lines) - 1
        # include up to line before next sense; keep \end{word} as boundary, excluded
        block = entry.lines[j:j2]
        blocks.append((j, block))
    return blocks


def qc_entry(entry: WordEntry) -> dict:
    breakdown_count = _count_cmd(entry, "breakdown")
    family_count = _count_cmd(entry, "family")
    sense_count = _count_cmd(entry, "sense")

    family_items = _cognate_items_from_family(entry) if family_count > 0 else []
    cognate_count = len([x for x in family_items if x and x != "__multiline__"])
    if family_count > 0 and cognate_count == 0:
        # Only multiline families; treat as 1 item minimum
        cognate_count = 1

    junk_hits = _has_junk(entry)

    sense_blocks = _extract_sense_blocks(entry)
    bad_pos = 0
    missing_phrase = 0
    missing_example = 0
    for j, block in sense_blocks:
        # Get first sense line payload (best effort)
        sense_ln = block[0]
        payload_m = re.search(r"\\wordsense\{(.*)\}\s*$", sense_ln)
        payload = (payload_m.group(1) if payload_m else sense_ln).strip()
        if not POS_PREFIX_RE.match(payload):
            bad_pos += 1
        # phrase/example presence in this block
        if not any("\\wordphrase{" in ln for ln in block):
            missing_phrase += 1
        if not any("\\wordexample{" in ln for ln in block):
            missing_example += 1

    ok_breakdown = breakdown_count == 1
    ok_family = family_count >= 1 and cognate_count >= 3
    ok_sense = sense_count >= 1 and bad_pos == 0
    ok_per_sense = (sense_count >= 1) and (missing_phrase == 0) and (missing_example == 0)
    ok_no_junk = len(junk_hits) == 0

    ok_all = ok_breakdown and ok_family and ok_sense and ok_per_sense and ok_no_junk

    return {
        "idx": entry.idx,
        "headword": entry.headword,
        "ipa": entry.ipa,
        "start_line": entry.start_line,
        "end_line": entry.end_line,
        "breakdown_count": breakdown_count,
        "family_count": family_count,
        "cognate_count": cognate_count,
        "sense_count": sense_count,
        "bad_pos_count": bad_pos,
        "sense_missing_phrase": missing_phrase,
        "sense_missing_example": missing_example,
        "junk_hits": "|".join(junk_hits),
        "ok_breakdown": int(ok_breakdown),
        "ok_family": int(ok_family),
        "ok_sense": int(ok_sense),
        "ok_per_sense": int(ok_per_sense),
        "ok_no_junk": int(ok_no_junk),
        "ok_all": int(ok_all),
    }


def load_progress() -> dict:
    if not OUT_PROGRESS.exists():
        return {"version": 1, "updated_at": None, "done": {}}
    try:
        return json.loads(OUT_PROGRESS.read_text(encoding="utf-8"))
    except Exception:
        return {"version": 1, "updated_at": None, "done": {}}


def save_progress(progress: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    progress["updated_at"] = datetime.now().isoformat(timespec="seconds")
    OUT_PROGRESS.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def mark_done(progress: dict, entry: WordEntry) -> None:
    key = f"{entry.idx}:{entry.headword}"
    progress.setdefault("done", {})
    progress["done"][key] = {"idx": entry.idx, "headword": entry.headword, "marked_at": datetime.now().isoformat(timespec="seconds")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", type=str, default=str(DEFAULT_TEX))
    ap.add_argument("--write", action="store_true", help="write CSV/MD/progress")
    ap.add_argument("--mark-done-idx", type=int, default=0, help="mark this entry index as done in progress file")
    ap.add_argument("--max-rows", type=int, default=0, help="limit rows (for quick debug)")
    args = ap.parse_args()

    tex_path = Path(args.tex)
    lines = _read_lines(tex_path)
    entries = parse_entries(lines)

    if args.mark_done_idx:
        progress = load_progress()
        hit = next((e for e in entries if e.idx == args.mark_done_idx), None)
        if not hit:
            print(f"idx {args.mark_done_idx} not found", file=sys.stderr)
            return 2
        mark_done(progress, hit)
        if args.write:
            save_progress(progress)
        print(f"marked done: {hit.idx} {hit.headword} ({hit.start_line}-{hit.end_line})")
        return 0

    rows = [qc_entry(e) for e in entries]
    if args.max_rows and args.max_rows > 0:
        rows = rows[: args.max_rows]

    if args.write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

        total = len(rows)
        ok = sum(r["ok_all"] for r in rows)
        bad = total - ok
        offenders = sorted(
            [r for r in rows if not r["ok_all"]],
            key=lambda r: (
                r["ok_breakdown"],
                r["ok_family"],
                r["ok_sense"],
                r["ok_per_sense"],
                r["ok_no_junk"],
                -r["sense_count"],
            ),
        )
        top = offenders[:50]
        md = []
        md.append(f"# QC Report for {tex_path.name}")
        md.append("")
        md.append(f"- Total entries: {total}")
        md.append(f"- OK: {ok}")
        md.append(f"- Not OK: {bad}")
        md.append("")
        md.append("## Top Offenders (first 50)")
        md.append("")
        md.append("| idx | headword | lines | breakdown | cognates | senses | bad_pos | miss_phrase | miss_example | junk |")
        md.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|---|")
        for r in top:
            md.append(
                f"| {r['idx']} | {r['headword']} | {r['start_line']}-{r['end_line']} | {r['breakdown_count']} | {r['cognate_count']} | {r['sense_count']} | {r['bad_pos_count']} | {r['sense_missing_phrase']} | {r['sense_missing_example']} | {r['junk_hits']} |"
            )
        OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

        progress = load_progress()
        save_progress(progress)

        print(f"Wrote {OUT_CSV}")
        print(f"Wrote {OUT_MD}")
        print(f"Wrote {OUT_PROGRESS}")
    else:
        total = len(rows)
        ok = sum(r["ok_all"] for r in rows)
        print(f"entries={total} ok={ok} bad={total-ok}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

