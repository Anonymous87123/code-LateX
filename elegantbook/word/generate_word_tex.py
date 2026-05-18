from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OCR_PATH = BASE_DIR / "ocr.md"
OUTPUT_PATH = BASE_DIR / "word.tex"

SUPPORT_MARKERS = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
OUTPUT_CHAR_REPLACEMENTS = {
    "★": "*",
    "☆": "*",
    "△": "triangle",
}
CIRCLED_DIGIT_REPLACEMENTS = {
    "①": "(1)",
    "②": "(2)",
    "③": "(3)",
    "④": "(4)",
    "⑤": "(5)",
    "⑥": "(6)",
    "⑦": "(7)",
    "⑧": "(8)",
    "⑨": "(9)",
    "⑩": "(10)",
    "⑪": "(11)",
    "⑫": "(12)",
    "⑬": "(13)",
    "⑭": "(14)",
    "⑮": "(15)",
    "⑯": "(16)",
    "⑰": "(17)",
    "⑱": "(18)",
    "⑲": "(19)",
    "⑳": "(20)",
}
POS_PREFIXES = (
    "n.",
    "v.",
    "vi.",
    "vt.",
    "a.",
    "adj.",
    "ad.",
    "adv.",
    "prep.",
    "conj.",
    "pron.",
    "int.",
    "num.",
    "aux.",
    "phr.",
    "pl.",
    "pp.",
)

PART_TITLES = {
    "第一部分 利用前缀扩充词汇之词根篇",
    "第二部分 利用后缀扩充词汇之词根篇",
}


@dataclass
class WordEntry:
    word: str
    stars: str = ""
    phonetic: str = ""
    breakdown: str = ""
    senses: list[str] = field(default_factory=list)
    phrases: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def normalize_output_text(text: str) -> str:
    for old, new in OUTPUT_CHAR_REPLACEMENTS.items():
        text = text.replace(old, new)
    for old, new in CIRCLED_DIGIT_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def escape_tex(text: str) -> str:
    text = normalize_output_text(text)
    text = collapse_spaces(text)
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "#": r"\#",
        "_": r"\_",
        "%": r"\%",
        "^": r"\textasciicircum{}",
        "~": r"\textasciitilde{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def collapse_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u3000", " ")).strip()


def is_comment(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("<!--") and stripped.endswith("-->")


def next_non_comment(lines: list[str], start: int) -> str:
    for idx in range(start, len(lines)):
        stripped = lines[idx].strip()
        if stripped and not is_comment(stripped):
            return stripped
    return ""


def is_phonetic_line(line: str) -> bool:
    stripped = line.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        return False
    inner = stripped[1:-1]
    if re.search(r"[\u4e00-\u9fff]", inner):
        return False
    if any(token in inner for token in ("=", "（", "）")):
        return False
    return True


def looks_like_pos_line(line: str) -> bool:
    stripped = collapse_spaces(line).lower()
    return stripped.startswith(POS_PREFIXES)


def looks_like_example(text: str) -> bool:
    stripped = collapse_spaces(text)
    if not stripped:
        return False
    if "（" in stripped and "）" in stripped and re.search(r"[A-Za-z]", stripped):
        return True
    if re.search(r"[A-Za-z].*[.?!]", stripped):
        return True
    if stripped.startswith(
        (
            "The ",
            "A ",
            "An ",
            "He ",
            "She ",
            "It ",
            "They ",
            "We ",
            "I ",
            "In ",
            "Our ",
            "His ",
            "Her ",
            "Potatoes ",
        )
    ):
        return True
    return False


def split_support_chunks(text: str) -> list[str]:
    stripped = collapse_spaces(text)
    if not stripped:
        return []
    chunks: list[str] = []
    if any(marker in stripped for marker in SUPPORT_MARKERS):
        parts = re.split(rf"(?=[{SUPPORT_MARKERS}])", stripped)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            chunks.append(part.lstrip(SUPPORT_MARKERS).strip())
        return [chunk for chunk in chunks if chunk]
    if "@" in stripped:
        parts = re.split(r"\s*@+\s*", stripped)
        return [collapse_spaces(part) for part in parts if collapse_spaces(part)]
    return [stripped]


def split_inline_phonetic(text: str) -> tuple[str, str]:
    stripped = text.strip()
    match = re.match(r"^\[([^\]]+)\]\s*(.*)$", stripped)
    if not match:
        return "", stripped
    if not is_phonetic_line(match.group(0).strip()):
        return "", stripped
    return match.group(1).strip(), match.group(2).strip()


def is_main_word_start(lines: list[str], index: int) -> bool:
    stripped = lines[index].strip()
    if not stripped or is_comment(stripped):
        return False
    if stripped.startswith(("#", "-", "词根", "来自")):
        return False
    if looks_like_pos_line(stripped):
        return False
    if not re.match(r"^[A-Za-z]", stripped):
        return False
    if "*" in stripped:
        return True
    if re.match(r"^[A-Za-z][A-Za-z0-9' .,/()\-]*\[[^\]]+\]", stripped):
        return True
    lookahead = next_non_comment(lines, index + 1)
    if is_phonetic_line(lookahead):
        return True
    return bool(
        len(stripped) <= 32
        and re.fullmatch(r"[A-Za-z][A-Za-z0-9' .,/()\-]*", stripped)
    )


def parse_word_header(line: str) -> tuple[str, str, str, str]:
    stripped = collapse_spaces(line)
    match = re.match(
        r"^(?P<lemma>[A-Za-z][A-Za-z0-9' .,/()\-]*)(?P<stars>\*{1,3})(?:\s+(?P<rest>.*)|$)",
        stripped,
    )
    if not match:
        match = re.match(
            r"^(?P<lemma>[A-Za-z][A-Za-z0-9' .,/()\-]*)(?:\s+(?P<rest>.*)|$)",
            stripped,
        )
    if not match:
        return stripped, "", "", ""
    lemma = collapse_spaces(match.group("lemma"))
    groups = match.groupdict()
    stars = groups.get("stars") or ""
    rest = groups.get("rest") or ""
    phonetic, trailing = split_inline_phonetic(rest)
    return lemma, stars, phonetic, trailing


def append_to_last(items: list[str], fragment: str) -> None:
    fragment = collapse_spaces(fragment)
    if not fragment:
        return
    if items:
        items[-1] = collapse_spaces(f"{items[-1]} {fragment}")
    else:
        items.append(fragment)


def split_support_from_line(text: str) -> tuple[str, list[str]]:
    stripped = collapse_spaces(text)
    if not stripped:
        return "", []
    positions = [stripped.find(marker) for marker in SUPPORT_MARKERS if marker in stripped]
    at_pos = stripped.find("@")
    if positions:
        first_pos = min(pos for pos in positions if pos >= 0)
    elif at_pos >= 0:
        first_pos = at_pos
    else:
        return stripped, []
    head = collapse_spaces(stripped[:first_pos])
    tail = stripped[first_pos:]
    return head, split_support_chunks(tail)


def parse_word_block(block_lines: list[str], fallback_breakdown: str = "") -> WordEntry | None:
    cleaned = [line.strip() for line in block_lines if line.strip() and not is_comment(line)]
    if not cleaned:
        return None

    word, stars, phonetic, inline_rest = parse_word_header(cleaned[0])
    entry = WordEntry(word=word, stars=stars, phonetic=phonetic, breakdown=fallback_breakdown)

    if inline_rest and inline_rest.startswith("[") and not is_phonetic_line(inline_rest):
        breakdown_match = re.match(r"^\[([^\]]+)\]\s*(.*)$", inline_rest)
        if breakdown_match:
            entry.breakdown = breakdown_match.group(1).strip()
            inline_rest = breakdown_match.group(2).strip()

    cursor = 1
    if not entry.phonetic and cursor < len(cleaned) and is_phonetic_line(cleaned[cursor]):
        entry.phonetic = cleaned[cursor][1:-1].strip()
        cursor += 1

    if cursor < len(cleaned):
        maybe_breakdown = cleaned[cursor]
        if maybe_breakdown.startswith("[") and maybe_breakdown.endswith("]") and not is_phonetic_line(maybe_breakdown):
            entry.breakdown = maybe_breakdown[1:-1].strip()
            cursor += 1

    if inline_rest:
        cleaned.insert(cursor, inline_rest)

    current_mode = "sense"
    for line in cleaned[cursor:]:
        stripped = collapse_spaces(line)
        if not stripped:
            continue
        if stripped.startswith(tuple(SUPPORT_MARKERS)) or "@" in stripped:
            current_mode = "support"
            for chunk in split_support_chunks(stripped):
                if looks_like_example(chunk):
                    entry.examples.append(chunk)
                else:
                    entry.phrases.append(chunk)
            continue
        sense_head, support_chunks = split_support_from_line(stripped)
        if support_chunks:
            if sense_head:
                entry.senses.append(sense_head)
            for chunk in support_chunks:
                if looks_like_example(chunk):
                    entry.examples.append(chunk)
                else:
                    entry.phrases.append(chunk)
            current_mode = "support"
            continue
        if looks_like_pos_line(stripped) or not entry.senses:
            if current_mode == "sense":
                entry.senses.append(stripped)
            else:
                current_mode = "sense"
                entry.senses.append(stripped)
            continue
        if current_mode == "support":
            target = entry.examples if entry.examples else entry.phrases
            append_to_last(target, stripped)
        else:
            append_to_last(entry.senses, stripped)

    if not entry.breakdown:
        entry.breakdown = fallback_breakdown or "未单独标出拆解，沿用 OCR 原文释义。"
    if not entry.senses:
        entry.senses = ["OCR 原文未稳定拆分词性与释义，保留原始内容。"]
    if not entry.phonetic:
        entry.phonetic = "[]"
    return entry


def render_word_entry(entry: WordEntry) -> list[str]:
    lines: list[str] = []
    opt = f"[{escape_tex(entry.stars)}]" if entry.stars else ""
    lines.append(
        rf"\begin{{word}}{opt}{{{escape_tex(entry.word)}}}{{{escape_tex(entry.phonetic)}}}"
    )
    lines.append(rf"  \wordbreakdown{{{escape_tex(entry.breakdown)}}}")
    for sense in entry.senses:
        lines.append(rf"  \wordsense{{{escape_tex(sense)}}}")
    for phrase in entry.phrases:
        lines.append(rf"  \wordphrase{{{escape_tex(phrase)}}}")
    for example in entry.examples:
        lines.append(rf"  \wordexample{{{escape_tex(example)}}}")
    lines.append(r"\end{word}")
    lines.append("")
    return lines


def render_paragraph_block(lines: list[str]) -> list[str]:
    output: list[str] = []
    paragraph: list[str] = []
    bullet_mode = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(escape_tex(" ".join(paragraph)))
            output.append("")
            paragraph = []

    def end_bullets() -> None:
        nonlocal bullet_mode
        if bullet_mode:
            output.append(r"\end{itemize}")
            output.append("")
            bullet_mode = False

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            flush_paragraph()
            end_bullets()
            continue
        if is_comment(stripped):
            continue
        bullet_match = re.match(r"^-\s+(.*)$", stripped)
        if bullet_match:
            flush_paragraph()
            if not bullet_mode:
                output.append(r"\begin{itemize}")
                bullet_mode = True
            output.append(rf"  \item {escape_tex(bullet_match.group(1))}")
            continue
        end_bullets()
        paragraph.append(stripped)

    flush_paragraph()
    end_bullets()
    return output


def collect_until(lines: list[str], start: int, stop_patterns: tuple[str, ...]) -> tuple[list[str], int]:
    bucket: list[str] = []
    index = start
    while index < len(lines):
        stripped = lines[index].strip()
        if any(stripped.startswith(pattern) for pattern in stop_patterns):
            break
        bucket.append(lines[index])
        index += 1
    return bucket, index


def render_frontmatter(lines: list[str]) -> list[str]:
    output: list[str] = []
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped or is_comment(stripped):
            index += 1
            continue
        top_match = re.match(r"^#\s+(.+)$", stripped)
        sub_match = re.match(r"^##\s+(.+)$", stripped)
        if top_match:
            title = top_match.group(1).strip()
            output.append(rf"\chapter{{{escape_tex(title)}}}")
            output.append("")
            index += 1
            block, index = collect_until(lines, index, ("#", "##"))
            output.extend(render_paragraph_block(block))
            continue
        if sub_match:
            title = sub_match.group(1).strip()
            output.append(rf"\section{{{escape_tex(title)}}}")
            output.append("")
            index += 1
            block, index = collect_until(lines, index, ("#", "##"))
            output.extend(render_paragraph_block(block))
            continue
        output.extend(render_paragraph_block([lines[index]]))
        index += 1
    return output


def render_root_intro(lines: list[str]) -> list[str]:
    items = [collapse_spaces(line) for line in lines if collapse_spaces(line) and not is_comment(line)]
    if not items:
        return []
    output = [r"\begin{itemize}"]
    for item in items:
        output.append(rf"  \item {escape_tex(item)}")
    output.append(r"\end{itemize}")
    output.append("")
    return output


def render_mainmatter(lines: list[str]) -> list[str]:
    output: list[str] = []
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped or is_comment(stripped):
            index += 1
            continue
        if stripped in PART_TITLES:
            output.append(rf"\part{{{escape_tex(stripped)}}}")
            output.append("")
            index += 1
            continue
        if re.match(r"^#\s+(第[一二]部分.+)$", stripped):
            title = re.sub(r"^#\s+", "", stripped).strip()
            output.append(rf"\part{{{escape_tex(title)}}}")
            output.append("")
            index += 1
            continue
        if re.match(r"^##\s+LECTURE\s+\d+$", stripped):
            index += 1
            continue
        root_match = re.match(r"^###\s+词根\s+(.+)$", stripped)
        if root_match:
            chapter_title = root_match.group(1).strip()
            output.append(rf"\chapter{{{escape_tex(chapter_title)}}}")
            output.append("")
            index += 1
            intro_lines: list[str] = []
            while index < len(lines):
                current = lines[index].strip()
                if not current or is_comment(current):
                    index += 1
                    continue
                if re.match(r"^###\s+词根\s+(.+)$", current) or re.match(r"^##\s+LECTURE\s+\d+$", current) or current.startswith("# 附录 补充词根"):
                    break
                if is_main_word_start(lines, index):
                    break
                intro_lines.append(lines[index])
                index += 1
            output.extend(render_root_intro(intro_lines))
            while index < len(lines):
                current = lines[index].strip()
                if not current or is_comment(current):
                    index += 1
                    continue
                if re.match(r"^###\s+词根\s+(.+)$", current) or re.match(r"^##\s+LECTURE\s+\d+$", current) or current.startswith("# 附录 补充词根"):
                    break
                if not is_main_word_start(lines, index):
                    fallback = parse_word_block([current], fallback_breakdown=f"保留 OCR 原文：{chapter_title}")
                    if fallback is not None:
                        output.extend(render_word_entry(fallback))
                    index += 1
                    continue
                block = [lines[index]]
                index += 1
                while index < len(lines):
                    ahead = lines[index].strip()
                    if not ahead or is_comment(ahead):
                        block.append(lines[index])
                        index += 1
                        continue
                    if re.match(r"^###\s+词根\s+(.+)$", ahead) or re.match(r"^##\s+LECTURE\s+\d+$", ahead) or ahead.startswith("# 附录 补充词根"):
                        break
                    if is_main_word_start(lines, index):
                        break
                    block.append(lines[index])
                    index += 1
                entry = parse_word_block(block, fallback_breakdown=f"词根 {chapter_title}")
                if entry is not None:
                    output.extend(render_word_entry(entry))
            continue
        index += 1
    return output


def render_appendix(lines: list[str]) -> list[str]:
    output: list[str] = [r"\appendix", r"\chapter{补充词根}", ""]
    index = 0
    current_section = ""
    current_root = ""
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped or is_comment(stripped):
            index += 1
            continue
        if stripped in {"# 附录 补充词根", "Appendix", "附录 补充词根"}:
            index += 1
            continue
        if re.fullmatch(r"[A-Z]", stripped):
            current_section = stripped
            output.append(rf"\section{{{current_section}}}")
            output.append("")
            index += 1
            continue
        root_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if root_match:
            current_root = root_match.group(1).strip()
            output.append(rf"\subsection{{{escape_tex(current_root)}}}")
            output.append("")
            index += 1
            continue
        if is_main_word_start(lines, index):
            block = [lines[index]]
            index += 1
            while index < len(lines):
                ahead = lines[index].strip()
                if not ahead or is_comment(ahead):
                    index += 1
                    continue
                if re.fullmatch(r"[A-Z]", ahead) or re.match(r"^\d+\.\s+(.+)$", ahead) or ahead.startswith("# 索引"):
                    break
                if is_main_word_start(lines, index):
                    break
                block.append(lines[index])
                index += 1
            entry = parse_word_block(block, fallback_breakdown=current_root or "补充词根")
            if entry is not None:
                output.extend(render_word_entry(entry))
            continue
        output.extend(render_paragraph_block([lines[index]]))
        index += 1
    return output


def render_index_section(title: str, lines: list[str]) -> list[str]:
    output = [rf"\section{{{escape_tex(title)}}}", "", r"\begin{Verbatim}[fontsize=\small]"]
    for line in lines:
        stripped = line.rstrip()
        if stripped.startswith("<!--"):
            continue
        output.append(normalize_output_text(stripped))
    output.extend([r"\end{Verbatim}", ""])
    return output


def render_indexes(lines: list[str]) -> list[str]:
    output = [r"\backmatter", r"\chapter{索引}", ""]
    current_title = ""
    bucket: list[str] = []

    def flush() -> None:
        nonlocal bucket, current_title
        if current_title:
            output.extend(render_index_section(current_title, bucket))
        bucket = []
        current_title = ""

    for line in lines:
        stripped = line.strip()
        if stripped == "# 索引":
            continue
        heading = re.match(r"^##\s+(.+)$", stripped)
        if heading:
            flush()
            current_title = heading.group(1).strip()
            continue
        if current_title and stripped in {"Index", "索引", current_title}:
            continue
        if current_title:
            bucket.append(line)
    flush()
    return output


def build_document(front_lines: list[str], main_lines: list[str], appendix_lines: list[str], index_lines: list[str]) -> str:
    output: list[str] = [
        r"\documentclass[lang=cn,11pt]{elegantbook}",
        "",
        r"\title{英语词根词典}",
        r"\subtitle{OCR 结构化整理版}",
        r"\author{（韩）金正基 编著}",
        r"\date{\today}",
        r"\setcounter{tocdepth}{1}",
        r"\makeatletter",
        r"\@ifundefined{setmainfont}{}{%",
        r"  \IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{}%",
        r"  \IfFontExistsTF{Arial}{\setsansfont{Arial}}{}%",
        r"  \IfFontExistsTF{Consolas}{\setmonofont{Consolas}}{}%",
        r"}",
        r"\makeatother",
        "",
        r"\begin{document}",
        r"\frontmatter",
        r"\tableofcontents",
        "",
    ]
    output.extend(render_frontmatter(front_lines))
    output.append(r"\mainmatter")
    output.append("")
    output.extend(render_mainmatter(main_lines))
    output.extend(render_appendix(appendix_lines))
    output.extend(render_indexes(index_lines))
    output.append(r"\end{document}")
    output.append("")
    return "\n".join(output)


def split_source(lines: list[str]) -> tuple[list[str], list[str], list[str], list[str]]:
    first_part_index = next(
        idx for idx, line in enumerate(lines) if line.strip() == "# 第一部分 利用前缀扩充词汇之词根篇"
    )
    appendix_index = next(
        idx for idx, line in enumerate(lines) if line.strip() == "# 附录 补充词根"
    )
    index_index = next(
        idx for idx, line in enumerate(lines) if line.strip() == "# 索引"
    )
    front = lines[:first_part_index]
    main = lines[first_part_index:appendix_index]
    appendix = lines[appendix_index:index_index]
    indexes = lines[index_index:]
    return front, main, appendix, indexes


def main() -> None:
    lines = read_lines(OCR_PATH)
    front, main_lines, appendix, indexes = split_source(lines)
    document = build_document(front, main_lines, appendix, indexes)
    OUTPUT_PATH.write_text(document, encoding="utf-8")
    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
