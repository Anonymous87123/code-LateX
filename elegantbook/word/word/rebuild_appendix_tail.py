from __future__ import annotations

import re
import statistics
from dataclasses import dataclass, field
from pathlib import Path

from generate_word_tex import collapse_spaces, escape_tex, is_comment


BASE_DIR = Path(__file__).resolve().parent
OCR_PATH = BASE_DIR / "ocr.md"
WORD_TEX_PATH = BASE_DIR / "word.tex"

TAIL_START_COMMENT = "<!-- PDF p421 | book p402 -->"
BROKEN_START_MARKERS = {
    r"\subsection{aur(= gold ) 9. basil( = king, royal)}",
    r"\subsection{aur(= gold)}",
}

WORD_RE = re.compile(
    r"""
    ^
    (?P<lemma>[A-Za-z][A-Za-z0-9' .,/()\-]*?)
    \s*
    (?P<stars>[+*]*)
    \s*
    [\[\［【]
    (?P<phonetic>[^\]\］】]*)
    [\]\］】]
    \s*
    (?P<meaning>.*)
    $
    """,
    re.VERBOSE,
)
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


@dataclass
class AppendixWord:
    lemma: str
    stars: str = ""
    phonetic: str = ""
    meaning: str = ""


@dataclass
class RootBlock:
    root: str
    section: str
    row: int
    column: int
    words: list[AppendixWord] = field(default_factory=list)


def smart_join(left: str, right: str) -> str:
    left = collapse_spaces(left)
    right = collapse_spaces(right)
    if not left:
        return right
    if not right:
        return left
    if re.search(r"[A-Za-z0-9]$", left) and re.match(r"^[A-Za-z0-9]", right):
        return f"{left} {right}"
    return f"{left}{right}"


def clean_root(text: str) -> str:
    text = collapse_spaces(text)
    text = text.replace(" .", ".")
    text = re.sub(r"\(\s*-\s*", "(= ", text)
    text = re.sub(r"\(\s*=\s*", "(= ", text)
    text = re.sub(r"\s+\)", ")", text)
    text = text.strip(" ?@")
    return text


def section_from_root(root: str) -> str:
    match = re.search(r"[A-Za-z]", root)
    return match.group(0).upper() if match else "?"


def clean_lemma(text: str) -> str:
    text = collapse_spaces(text)
    text = text.rstrip("\"“”‘’`.;:·")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_phonetic(text: str) -> str:
    text = (
        text.replace("［", "[")
        .replace("］", "]")
        .replace("【", "[")
        .replace("】", "]")
        .replace("「", "[")
        .replace("」", "]")
        .replace("『", "[")
        .replace("』", "]")
        .replace("（", "(")
        .replace("）", ")")
        .replace("‘", "'")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
    )
    text = collapse_spaces(text)
    text = re.sub(r"^[EI](?=['\"])", "", text)
    text = text.lstrip('["[] ')
    text = text.rstrip('] ')
    return text.strip()


def clean_meaning(text: str) -> str:
    text = text.replace("（", "(").replace("）", ")")
    return collapse_spaces(text)


def parse_word_line(text: str) -> AppendixWord | None:
    text = collapse_spaces(text)
    match = WORD_RE.match(text)
    if not match:
        cjk_match = CJK_RE.search(text)
        if cjk_match is None:
            return None
        head = text[: cjk_match.start()].strip()
        meaning = text[cjk_match.start() :].strip()
        if not re.match(r"^[A-Za-z]", head):
            return None
        head_for_match = head.rstrip("]】］")
        star_phonetic_match = re.match(
            r"^(?P<lemma>[A-Za-z][A-Za-z0-9 .,/()\-]*?)(?P<stars>[+*]+)(?P<phonetic>['`,.!:;A-Za-z0-9()\-]+)$",
            head_for_match,
        )
        sep_match = re.search(r"[\[\]［］【】「」『』\"“”‘’`']", head_for_match)
        if star_phonetic_match:
            lemma = star_phonetic_match.group("lemma")
            stars = star_phonetic_match.group("stars")
            phonetic = star_phonetic_match.group("phonetic")
        elif sep_match:
            prefix = head_for_match[: sep_match.start()].rstrip()
            phonetic = head_for_match[sep_match.start() :].strip()
            star_match = re.search(r"([+*]+)$", prefix)
            if star_match:
                stars = star_match.group(1)
                lemma = prefix[: star_match.start()].rstrip()
            else:
                odd_tail_match = re.search(r"([+*]+)([A-Za-z])$", prefix)
                if odd_tail_match:
                    stars = odd_tail_match.group(1)
                    lemma = prefix[: odd_tail_match.start(1)].rstrip()
                    phonetic = odd_tail_match.group(2) + phonetic
                else:
                    stars = ""
                    lemma = prefix
        else:
            tail_star_match = re.search(r"([+*]+)$", head_for_match)
            if tail_star_match:
                stars = tail_star_match.group(1)
                lemma = head_for_match[: tail_star_match.start()].rstrip()
            else:
                stars = ""
                lemma = head_for_match
            phonetic = ""
    else:
        lemma = match.group("lemma")
        stars = match.group("stars").strip()
        phonetic = match.group("phonetic")
        meaning = match.group("meaning")
    lemma = clean_lemma(lemma)
    phonetic = clean_phonetic(phonetic)
    meaning = clean_meaning(meaning)
    if not lemma:
        return None
    return AppendixWord(lemma=lemma, stars=stars, phonetic=phonetic, meaning=meaning)


def split_page_rows(page_lines: list[str]) -> list[tuple[str, str]]:
    split_pattern = re.compile(r"^(?P<left>\s*\S.*?)\s{3,}(?P<right>\S.*)$")
    right_starts: list[int] = []

    for raw in page_lines:
        if not raw.strip() or is_comment(raw):
            continue
        match = split_pattern.match(raw.rstrip())
        if match:
            right_starts.append(raw.index(match.group("right")))

    boundary = int(statistics.median(right_starts)) if right_starts else 40
    rows: list[tuple[str, str]] = []

    for raw in page_lines:
        if is_comment(raw):
            continue
        if not raw.strip():
            rows.append(("", ""))
            continue
        match = split_pattern.match(raw.rstrip())
        if match:
            rows.append((match.group("left").strip(), match.group("right").strip()))
            continue
        stripped = raw.strip()
        first_nonspace = len(raw) - len(raw.lstrip())
        if right_starts and first_nonspace >= boundary - 5:
            rows.append(("", stripped))
        else:
            rows.append((stripped, ""))
    return rows


def flush_word(block: RootBlock | None, current_word: AppendixWord | None) -> None:
    if block is not None and current_word is not None:
        block.words.append(current_word)


def parse_column_rows(rows: list[tuple[int, str]], column: int) -> list[RootBlock]:
    blocks: list[RootBlock] = []
    current_block: RootBlock | None = None
    current_word: AppendixWord | None = None

    def flush_block() -> None:
        nonlocal current_block, current_word
        flush_word(current_block, current_word)
        current_word = None
        if current_block is not None and current_block.root:
            blocks.append(current_block)
        current_block = None

    for row, raw in rows:
        text = collapse_spaces(raw)
        if not text or text in {"?", "@", "?", "@"}:
            continue
        if re.fullmatch(r"[A-Z]", text):
            continue
        root_match = re.match(r"^\d+\.\s*(.+)$", text)
        if root_match:
            flush_block()
            root = clean_root(root_match.group(1))
            current_block = RootBlock(
                root=root,
                section=section_from_root(root),
                row=row,
                column=column,
            )
            continue
        if current_block is None:
            continue
        parsed_word = parse_word_line(text)
        if parsed_word is not None:
            flush_word(current_block, current_word)
            current_word = parsed_word
            continue
        if current_word is not None:
            current_word.meaning = smart_join(current_word.meaning, text)
        elif current_block.words:
            current_block.words[-1].meaning = smart_join(current_block.words[-1].meaning, text)

    flush_block()
    return blocks


def build_tail_blocks(source_lines: list[str]) -> list[RootBlock]:
    pages: list[list[str]] = []
    current: list[str] = []
    for line in source_lines:
        if is_comment(line):
            if current:
                pages.append(current)
            current = [line]
            continue
        current.append(line)
    if current:
        pages.append(current)

    all_blocks: list[RootBlock] = []
    for page in pages:
        rows = split_page_rows(page)
        left_rows = [(idx, left) for idx, (left, _right) in enumerate(rows) if left]
        right_rows = [(idx, right) for idx, (_left, right) in enumerate(rows) if right]
        merged = parse_column_rows(left_rows, 0) + parse_column_rows(right_rows, 1)
        merged.sort(key=lambda block: (block.row, block.column))

        section_order: list[str] = []
        for block in merged:
            if block.section not in section_order:
                section_order.append(block.section)
        for section in section_order:
            all_blocks.extend(block for block in merged if block.section == section)
    return all_blocks


def render_tail(blocks: list[RootBlock], initial_section: str = "A") -> list[str]:
    output: list[str] = []
    current_section = initial_section

    for block in blocks:
        if block.section != current_section:
            output.extend([rf"\section{{{block.section}}}", ""])
            current_section = block.section
        if not block.words:
            continue
        output.extend([rf"\subsection{{{escape_tex(block.root)}}}", ""])
        for word in block.words:
            stars = f"[{escape_tex(word.stars)}]" if word.stars else ""
            lemma = escape_tex(word.lemma)
            breakdown = escape_tex(word.phonetic or "词根待复核")
            meaning = escape_tex(word.meaning or "词义待复核")
            output.append(rf"\begin{{word}}{stars}{{{lemma}}}{{[]}}")
            output.append(rf"  \wordbreakdown{{{breakdown}}}")
            output.append(rf"  \wordsense{{{meaning}}}")
            output.append(r"\end{word}")
            output.append("")
    return output


def rebuild_word_tex() -> None:
    ocr_lines = OCR_PATH.read_text(encoding="utf-8").splitlines()
    tail_start = next(i for i, line in enumerate(ocr_lines) if line.strip() == TAIL_START_COMMENT)
    tail_end = next(i for i, line in enumerate(ocr_lines) if line.strip() == "# 索引")
    tail_blocks = build_tail_blocks(ocr_lines[tail_start:tail_end])
    rendered_tail = render_tail(tail_blocks)

    word_lines = WORD_TEX_PATH.read_text(encoding="utf-8").splitlines()
    broken_start = next(i for i, line in enumerate(word_lines) if line.strip() in BROKEN_START_MARKERS)
    backmatter = next(i for i, line in enumerate(word_lines) if line.strip() == r"\backmatter")

    new_lines = word_lines[:broken_start] + rendered_tail + word_lines[backmatter:]
    WORD_TEX_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    rebuild_word_tex()
