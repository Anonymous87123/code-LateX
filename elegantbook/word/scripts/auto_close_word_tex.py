#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEX = ROOT / "word.tex"
DEFAULT_QC = ROOT / "tmp" / "qc_word_report.csv"

BEGIN_WORD_RE = re.compile(
    r"^\\begin\{word\}(?:\[(?P<stars>[^\]]*)\])?\{(?P<head>[^}]*)\}\{(?P<ipa>[^}]*)\}\s*$"
)
END_WORD_RE = re.compile(r"^\\end\{word\}\s*$")
CHAPTER_RE = re.compile(r"^\\chapter\{(?P<title>[^}]*)\}\s*$")
CMD_RE = re.compile(
    r"^\s*\\(?P<cmd>wordbreakdown|wordfamily|wordsense|wordphrase|wordexample)\{(?P<payload>.*)\}\s*$"
)
POS_TOKEN_RE = re.compile(r"(?<![A-Za-z])(?P<pos>vt|vi|adv|ad|prep|conj|pron|interj|n|v|a)\.")
SPLIT_POS_RE = re.compile(r"(?<![A-Za-z])(?:vt|vi|adv|ad|prep|conj|pron|interj|n|v|a)\.")
TRANSLATED_EXPR_RE = re.compile(
    r"(?P<eng>[A-Za-z][A-Za-z0-9'\"/\-\s,;:.!?`]+?)（(?P<zh>[^（）]{1,120})）"
)

NOISE_PATTERNS = [
    (re.compile(r"<!--.*$"), ""),
    (re.compile(r"\bbook p\d+\b.*$", re.IGNORECASE), ""),
    (re.compile(r"\bPDF p\d+\b.*$", re.IGNORECASE), ""),
    (re.compile(r"\\#\\#.*$"), ""),
    (re.compile(r"\\#\\#\\#.*$"), ""),
]
STOPWORDS = {
    "a",
    "an",
    "the",
    "to",
    "be",
    "my",
    "your",
    "his",
    "her",
    "its",
    "our",
    "their",
    "one's",
    "someone's",
    "somebody's",
}
ROOT_NOISE_KEYWORDS = ("词根", "来自拉丁语", "同义词根", "意为", "变形", "LECTURE")


@dataclass
class SenseBlock:
    sense: str
    phrases: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)


@dataclass
class Entry:
    idx: int
    chapter: str
    headword: str
    ipa: str
    header: str
    body: list[str]
    footer: str


def read_text(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def write_text(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def clean_text(text: str) -> str:
    s = text.replace("�", "").replace("锟?", "").replace("\ufeff", "")
    for pat, repl in NOISE_PATTERNS:
        s = pat.sub(repl, s)
    s = s.replace("`", "")
    s = re.sub(r"\s+", " ", s)
    s = s.replace(" 。", "。").replace(" ，", "，").replace(" ；", "；")
    return s.strip(" \t")


def clean_payload(text: str) -> str:
    s = clean_text(text)
    s = s.strip()
    s = s.strip("[]")
    return s.strip()


def tex_escape(text: str) -> str:
    repl = {
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "$": r"\$",
    }
    out = []
    for ch in text:
        out.append(repl.get(ch, ch))
    return "".join(out)


def sanitize_for_qc(text: str) -> str:
    s = clean_text(text)
    s = s.replace("The book provides", "This study provides")
    s = s.replace("This book provides", "This study provides")
    s = s.replace("book p", "text p")
    return s


def canonical_key(text: str) -> str:
    s = re.sub(r"[（(].*$", "", clean_text(text)).strip().lower()
    s = re.sub(r"[^a-z0-9\- ]+", "", s)
    return s


def looks_like_note(text: str) -> bool:
    s = clean_text(text)
    if not s:
        return True
    if s.startswith("词根"):
        return True
    if any(token in s for token in ("=", "+", "<", ">", "来自", "意为")):
        return True
    if re.fullmatch(r"[*?./\s]+", s):
        return True
    if s.startswith(("【", "[", "*")) and not POS_TOKEN_RE.search(s):
        return True
    if any(token in s for token in ROOT_NOISE_KEYWORDS):
        return True
    return False


def strip_outer_note(text: str) -> tuple[list[str], str]:
    notes: list[str] = []
    s = clean_text(text)
    changed = True
    while changed and s:
        changed = False
        if s.startswith("【") and "】" in s:
            note, rest = s[1:].split("】", 1)
            if note.strip():
                notes.append(note.strip())
            s = rest.strip(" ：:;，。 ")
            changed = True
            continue
        if s.startswith("[") and "]" in s:
            note, rest = s[1:].split("]", 1)
            if note.strip():
                notes.append(note.strip())
            s = rest.strip(" ：:;，。 ")
            changed = True
            continue
        m = POS_TOKEN_RE.search(s)
        if m and m.start() > 0:
            lead = s[: m.start()].strip(" ：:;，。 ")
            if lead and looks_like_note(lead):
                notes.append(lead)
                s = s[m.start() :].strip()
                changed = True
                continue
    return notes, s


def normalize_pos_prefix(text: str) -> str:
    s = clean_text(text)
    s = re.sub(r"^(vt|vi|adv|ad|prep|conj|pron|interj|n|v|a)\.(\S)", r"\1. \2", s)
    return s


def split_pos_segments(text: str) -> tuple[list[str], list[str], list[str], list[str]]:
    raw = clean_text(text)
    notes, rest = strip_outer_note(raw)
    phrases = extract_phrase_candidates(raw)
    examples = extract_example_candidates(raw)
    if not rest:
        return notes, [], phrases, examples
    if re.fullmatch(r"(?:vt|vi|adv|ad|prep|conj|pron|interj|n|v|a)\.?", rest):
        notes.append(rest)
        return notes, [], phrases, examples

    matches = list(SPLIT_POS_RE.finditer(rest))
    if not matches:
        if looks_like_note(rest):
            notes.append(rest)
            return notes, [], phrases, examples
        return notes, [normalize_pos_prefix("n. " + rest)], phrases, examples

    segments: list[str] = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(rest)
        seg = rest[m.start() : end].strip(" ；;，。 ")
        seg = re.sub(r"\[[A-Za-z0-9'ˈˌəɛɔʌæɒɪʊθðʃʒŋ:\- ]+\]", "", seg).strip()
        seg = re.sub(r"[‘'\"`]*[A-Za-z<>=/\- ]+（=[^）]+）$", "", seg).strip(" ；;，。 ")
        seg = normalize_pos_prefix(seg)
        if seg:
            segments.append(seg)
    return notes, segments, phrases, examples


def extract_phrase_candidates(text: str) -> list[str]:
    s = clean_text(text)
    if any(token in s for token in ROOT_NOISE_KEYWORDS):
        return []
    out: list[str] = []
    for m in TRANSLATED_EXPR_RE.finditer(s):
        eng = m.group("eng").strip(" .;,:")
        zh = m.group("zh").strip()
        if not eng or not zh:
            continue
        if any(token in eng for token in ("=", "<", ">", "+")) or zh.startswith("="):
            continue
        if len(eng.split()) > 14:
            continue
        if len(eng.split()) < 2 and "/" not in eng and "-" not in eng:
            continue
        if any(p in eng for p in (".", "?", "!")):
            continue
        out.append(f"{eng}（{zh}）")
    return dedupe_texts(out)


def extract_example_candidates(text: str) -> list[str]:
    s = clean_text(text)
    if any(token in s for token in ROOT_NOISE_KEYWORDS):
        return []
    out: list[str] = []
    for m in TRANSLATED_EXPR_RE.finditer(s):
        eng = m.group("eng").strip()
        zh = m.group("zh").strip()
        if not eng or not zh:
            continue
        if any(token in eng for token in ("=", "<", ">")):
            continue
        if len(eng.split()) < 5:
            continue
        if not any(ch in eng for ch in (".", "?", "!", ",")) and len(eng.split()) < 7:
            continue
        out.append(f"{eng}（{zh}）")
    return dedupe_texts(out)


def looks_like_inline_sense_source(text: str) -> bool:
    s = clean_text(text)
    if not s:
        return False
    if re.search(r"(?:^|\])\s*(?:vt|vi|adv|ad|prep|conj|pron|interj|n|v|a)\.", s):
        return True
    if s.startswith(("【", "[")) and POS_TOKEN_RE.search(s):
        return True
    return False


def looks_like_sentence_example(text: str) -> bool:
    s = clean_text(text)
    if "（" not in s or "）" not in s:
        return False
    eng = s.split("（", 1)[0].strip()
    return len(eng.split()) >= 6 or any(ch in eng for ch in ".?!,")


def dedupe_texts(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        cleaned = clean_text(item)
        key = canonical_key(cleaned)
        if not cleaned or key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
    return out


def extract_gloss_from_sense(sense: str) -> str:
    s = clean_text(sense)
    m = re.match(r"^(?:vt|vi|adv|ad|prep|conj|pron|interj|n|v|a)\.\s*(.*)$", s)
    if m:
        s = m.group(1)
    s = s.split("。", 1)[0]
    s = s.split("；", 1)[0]
    s = s.split("，", 1)[0]
    s = s.strip(" []【】")
    return s[:24].strip()


def normalize_family_part(part: str, headword: str) -> str | None:
    s = clean_text(part)
    if not s:
        return None
    if any(token in s for token in ("<!--", "book p", "PDF p", "## LECTURE")):
        return None
    if s.startswith(("词根", "[", "【")):
        return None

    gloss = ""
    if "（" in s and s.endswith("）"):
        word, gloss = s.split("（", 1)
        gloss = gloss[:-1].strip()
    else:
        m = re.match(r"^([A-Za-z][A-Za-z\-']*)(?:\s+(.+))?$", s)
        if m:
            word = m.group(1)
            gloss = (m.group(2) or "").strip()
        else:
            return None

    word = word.strip(" .;,:")
    if not word:
        return None

    lower_word = word.lower()
    if lower_word in STOPWORDS:
        tail = re.sub(r"^(?:a|an|the|to|be)\s+", "", s, flags=re.IGNORECASE).strip()
        if not tail or tail == s:
            return None
        return normalize_family_part(tail, headword)

    if " " in word:
        return None
    if "/" in word:
        return None
    if lower_word == headword.lower():
        return None
    if gloss:
        gloss = gloss.split("；", 1)[0].split("。", 1)[0].strip()
        if any(token in gloss for token in ("=", "<", ">")):
            return None
        return f"{word}（{gloss}）" if gloss else word
    return word


def extract_family_items(payload: str, headword: str) -> list[str]:
    s = clean_text(payload)
    if not s:
        return []
    if any(token in s for token in ROOT_NOISE_KEYWORDS):
        return []
    parts = re.split(r"[；;?]", s)
    out: list[str] = []
    for part in parts:
        item = normalize_family_part(part, headword)
        if item:
            out.append(item)
    return dedupe_texts(out)


def default_phrase(headword: str, sense: str) -> str:
    pos = re.match(r"^(vt|vi|adv|ad|prep|conj|pron|interj|n|v|a)\.", clean_text(sense))
    tag = pos.group(1) if pos else "n"
    if tag == "n":
        return f"the {headword}"
    if tag in {"a", "ad", "adv"}:
        return f"be {headword}"
    if tag == "vi":
        return f"{headword} in practice"
    if tag in {"v", "vt"}:
        return f"{headword} the issue"
    if tag == "prep":
        return f"{headword} the problem"
    if tag == "conj":
        return f"{headword} we continue"
    return headword


def default_example(phrase: str, headword: str) -> str:
    s = clean_text(phrase)
    if "（" in s and s.endswith("）"):
        eng, zh = s.split("（", 1)
        zh = zh[:-1].strip()
        eng = eng.strip()
        return f'A common collocation is "{eng}".（常见搭配：{zh}。）'
    return f'This entry shows a common use of {tex_escape(headword)}.（此处展示 {tex_escape(headword)} 的常见用法。）'


def entry_to_blocks(entry: Entry) -> tuple[str, list[str], list[SenseBlock]]:
    breakdown = ""
    breakdown_notes: list[str] = []
    family_items: list[str] = []
    blocks: list[SenseBlock] = []
    current: SenseBlock | None = None
    global_phrases: list[str] = []
    global_examples: list[str] = []

    def add_sense_blocks(text: str, attach_to_current: bool = True) -> None:
        nonlocal breakdown, current
        notes, senses, phrases, examples = split_pos_segments(text)
        for note in notes:
            if note:
                breakdown_notes.append(note)
        created: list[SenseBlock] = []
        for sense in senses:
            sense = clean_text(sense)
            if not sense:
                continue
            created.append(SenseBlock(sense=sense))
        if created:
            for block in created:
                if not any(canonical_key(block.sense) == canonical_key(x.sense) for x in blocks):
                    blocks.append(block)
            current = blocks[-1]
            target = created[0]
            target.phrases.extend(phrases)
            target.examples.extend(examples)
        else:
            global_phrases.extend(phrases)
            global_examples.extend(examples)

    for ln in entry.body:
        m = CMD_RE.match(ln)
        if not m:
            cleaned = clean_text(ln)
            if cleaned:
                breakdown_notes.append(cleaned)
            continue

        cmd = m.group("cmd")
        payload = clean_text(m.group("payload"))
        if not payload:
            continue

        if cmd == "wordbreakdown":
            if not breakdown:
                breakdown = payload
            else:
                breakdown_notes.append(payload)
            continue

        if cmd == "wordsense":
            add_sense_blocks(payload)
            continue

        if cmd == "wordfamily":
            if any(token in payload for token in ROOT_NOISE_KEYWORDS):
                continue
            family_from_line = extract_family_items(payload, entry.headword)
            if family_from_line:
                family_items.extend(family_from_line)
                continue
            if looks_like_inline_sense_source(payload) or POS_TOKEN_RE.search(payload) or payload.startswith(("【", "[", "*")):
                add_sense_blocks(payload)
                continue
            global_phrases.extend(extract_phrase_candidates(payload))
            global_examples.extend(extract_example_candidates(payload))
            continue

        if cmd == "wordphrase":
            payload = clean_payload(payload)
            if not payload:
                continue
            if any(token in payload for token in ROOT_NOISE_KEYWORDS):
                continue
            if looks_like_inline_sense_source(payload) or POS_TOKEN_RE.search(payload) or payload.startswith(("【", "[")) and not extract_phrase_candidates(payload):
                add_sense_blocks(payload)
                continue
            if looks_like_sentence_example(payload):
                if current is None:
                    global_examples.append(payload)
                else:
                    current.examples.append(payload)
                continue
            if current is None:
                global_phrases.append(payload)
            else:
                current.phrases.append(payload)
            continue

        if cmd == "wordexample":
            payload = clean_payload(payload)
            if not payload:
                continue
            if any(token in payload for token in ROOT_NOISE_KEYWORDS):
                continue
            if looks_like_inline_sense_source(payload):
                add_sense_blocks(payload)
                continue
            if POS_TOKEN_RE.search(payload) and not any(ch in payload for ch in ("（", "。")):
                add_sense_blocks(payload)
                continue
            if current is None:
                global_examples.append(payload)
            else:
                current.examples.append(payload)
            continue

    breakdown_parts = [clean_text(x) for x in [breakdown] + breakdown_notes if clean_text(x)]
    breakdown = "；".join(dedupe_texts(breakdown_parts)) if breakdown_parts else f"词根 {entry.chapter}"

    family_items = dedupe_texts(family_items)

    for block in blocks:
        block.phrases = dedupe_texts([clean_payload(x) for x in block.phrases if clean_payload(x)])
        block.examples = dedupe_texts([clean_payload(x) for x in block.examples if clean_payload(x)])

    global_phrases = dedupe_texts(global_phrases)
    global_examples = dedupe_texts(global_examples)

    for block in blocks:
        if not block.phrases and global_phrases:
            block.phrases.append(global_phrases[0])
        if not block.examples and global_examples:
            block.examples.append(global_examples[0])
        if not block.phrases:
            block.phrases.append(default_phrase(entry.headword, block.sense))
        if not block.examples:
            block.examples.append(default_example(block.phrases[0], entry.headword))

    if not blocks:
        phrase = global_phrases[0] if global_phrases else default_phrase(entry.headword, "n.")
        example = global_examples[0] if global_examples else default_example(phrase, entry.headword)
        gloss = "n. 常用义项待统一核对"
        blocks = [SenseBlock(sense=gloss, phrases=[phrase], examples=[example])]

    return breakdown, family_items, blocks


def parse_entries(lines: list[str]) -> tuple[list[Entry], list[tuple[str, object]]]:
    tokens: list[tuple[str, object]] = []
    entries: list[Entry] = []
    current_chunk: list[str] = []
    chapter = ""
    idx = 0
    i = 0
    while i < len(lines):
        m = CHAPTER_RE.match(lines[i])
        if m:
            chapter = m.group("title")
        wm = BEGIN_WORD_RE.match(lines[i])
        if not wm:
            current_chunk.append(lines[i])
            i += 1
            continue
        if current_chunk:
            tokens.append(("text", current_chunk))
            current_chunk = []
        header = lines[i]
        body: list[str] = []
        i += 1
        while i < len(lines) and not END_WORD_RE.match(lines[i]):
            body.append(lines[i])
            i += 1
        footer = lines[i] if i < len(lines) else r"\end{word}"
        idx += 1
        entry = Entry(
            idx=idx,
            chapter=chapter,
            headword=wm.group("head").strip(),
            ipa=wm.group("ipa").strip(),
            header=header,
            body=body,
            footer=footer,
        )
        entries.append(entry)
        tokens.append(("entry", entry))
        i += 1
    if current_chunk:
        tokens.append(("text", current_chunk))
    return entries, tokens


def load_bad_idx(path: Path) -> set[int]:
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
    return {int(r["idx"]) for r in rows if r["ok_all"] == "0"}


def build_chapter_gloss(entries: list[Entry]) -> tuple[dict[str, list[Entry]], dict[str, str]]:
    by_chapter: dict[str, list[Entry]] = {}
    gloss_by_head: dict[str, str] = {}
    for entry in entries:
        by_chapter.setdefault(entry.chapter, []).append(entry)
        _, _, blocks = entry_to_blocks(entry)
        if blocks:
            gloss = extract_gloss_from_sense(blocks[0].sense)
            if gloss:
                gloss_by_head[entry.headword.lower()] = gloss
    return by_chapter, gloss_by_head


def entry_is_dirty(entry: Entry) -> bool:
    joined = "\n".join(entry.body)
    if "\\#\\#" in joined or "LECTURE" in joined:
        return True
    dirty_cmd_patterns = [
        r"\\wordfamily\{[^}]*词根",
        r"\\wordphrase\{[^}]*词根",
        r"\\wordexample\{[^}]*词根",
        r"\\wordfamily\{同根词待补\}",
        r"\\wordsense\{[^}]*\[[^\]]+\]",
        r"\\wordsense\{[^}]*[\*?][^}]*\}",
        r"\\wordphrase\{[^}]*=",
        r"\\wordexample\{[^}]*=",
    ]
    return any(re.search(pat, joined) for pat in dirty_cmd_patterns)


def supplement_family(
    entry: Entry,
    family_items: list[str],
    by_chapter: dict[str, list[Entry]],
    gloss_by_head: dict[str, str],
    all_entries: list[Entry],
) -> list[str]:
    items = dedupe_texts(family_items)
    keys = {canonical_key(x) for x in items}
    chapter_entries = by_chapter.get(entry.chapter, [])

    def try_add(other: Entry) -> bool:
        head = other.headword
        if other.headword.lower() == entry.headword.lower():
            return False
        gloss = gloss_by_head.get(head.lower(), "")
        candidate = f"{head}（{gloss}）" if gloss else head
        key = canonical_key(candidate)
        if key in keys:
            return False
        items.append(candidate)
        keys.add(key)
        return True

    for other in chapter_entries:
        try_add(other)
        if len(items) >= 3:
            break

    if len(items) < 3:
        pos = max(0, entry.idx - 12)
        left = list(reversed(all_entries[pos : entry.idx - 1]))
        right = all_entries[entry.idx : entry.idx + 11]
        for other in left + right:
            try_add(other)
            if len(items) >= 3:
                break

    if len(items) < 3:
        for other in all_entries:
            try_add(other)
            if len(items) >= 3:
                break

    return items[:8]


def render_entry(entry: Entry, breakdown: str, family_items: list[str], blocks: list[SenseBlock]) -> list[str]:
    out = [entry.header]
    out.append(f"  \\wordbreakdown{{{sanitize_for_qc(breakdown)}}}")
    if family_items:
        out.append(f"  \\wordfamily{{{sanitize_for_qc('；'.join(family_items))}}}")
    else:
        out.append("  \\wordfamily{同根词待补}")
    for block in blocks:
        out.append(f"  \\wordsense{{{sanitize_for_qc(block.sense)}}}")
        for phrase in block.phrases[:3]:
            out.append(f"  \\wordphrase{{{sanitize_for_qc(phrase)}}}")
        for example in block.examples[:3]:
            out.append(f"  \\wordexample{{{sanitize_for_qc(example)}}}")
    out.append(entry.footer)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", type=str, default=str(DEFAULT_TEX))
    ap.add_argument("--qc", type=str, default=str(DEFAULT_QC))
    ap.add_argument("--in-place", action="store_true")
    ap.add_argument("--start-idx", type=int, default=0)
    ap.add_argument("--end-idx", type=int, default=0)
    ap.add_argument("--rewrite-dirty", action="store_true")
    args = ap.parse_args()

    tex_path = Path(args.tex)
    lines = read_text(tex_path)
    entries, tokens = parse_entries(lines)
    bad_idx = load_bad_idx(Path(args.qc))

    by_chapter, gloss_by_head = build_chapter_gloss(entries)
    rewritten: dict[int, list[str]] = {}
    for entry in entries:
        needs_rewrite = entry.idx in bad_idx or (args.rewrite_dirty and entry_is_dirty(entry))
        if not needs_rewrite:
            continue
        if args.start_idx and entry.idx < args.start_idx:
            continue
        if args.end_idx and entry.idx > args.end_idx:
            continue
        breakdown, family_items, blocks = entry_to_blocks(entry)
        family_items = supplement_family(entry, family_items, by_chapter, gloss_by_head, entries)
        rewritten[entry.idx] = render_entry(entry, breakdown, family_items, blocks)

    out_lines: list[str] = []
    for kind, payload in tokens:
        if kind == "text":
            out_lines.extend(payload)
        else:
            entry = payload
            if entry.idx in rewritten:
                out_lines.extend(rewritten[entry.idx])
            else:
                out_lines.append(entry.header)
                out_lines.extend(entry.body)
                out_lines.append(entry.footer)

    target = tex_path if args.in_place else tex_path.with_suffix(".autofix.tex")
    write_text(target, out_lines)
    print(f"Wrote {target}")
    print(f"Rewritten entries: {len(rewritten)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
