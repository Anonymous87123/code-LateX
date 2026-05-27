from __future__ import annotations

import re
import subprocess
from bisect import bisect_left
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEX_PATH = ROOT / "word.tex"
PDF_PATH = ROOT / "word.pdf"
ROOT_INDEX_PATH = ROOT / "generated-root-index.tex"
WORD_INDEX_PATH = ROOT / "generated-word-index.tex"


def run_text(command: list[str]) -> str:
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    return result.stdout


def tex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "#": r"\#",
        "$": r"\$",
        "%": r"\%",
        "&": r"\&",
        "_": r"\_",
        "^": r"\textasciicircum{}",
        "~": r"\textasciitilde{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


def collapse_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def sort_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def first_letter(text: str) -> str:
    match = re.search(r"[A-Za-z]", text)
    return match.group(0).upper() if match else "#"


def load_pdf_pages() -> list[str]:
    stdout = run_text(["pdftotext", "-layout", "-enc", "UTF-8", str(PDF_PATH), "-"])
    pages = stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def page_offset() -> int:
    dests = run_text(["pdfinfo", "-dests", str(PDF_PATH)])
    match = re.search(r'^\s*(\d+)\s+\[.*\]\s+"page\.1"', dests, re.M)
    if not match:
        return 12
    return int(match.group(1)) - 1


def body_block(tex: str) -> str:
    start = tex.index(r"\mainmatter")
    end = tex.index(r"\backmatter")
    return tex[start:end]


def parse_words(block: str) -> list[dict[str, object]]:
    words: list[dict[str, object]] = []
    pattern = re.compile(r"^\\begin\{word\}(?:\[(?P<stars>[^\]]*)\])?\{(?P<title>.+?)\}\{(?P<ipa>.+?)\}\s*$", re.M)
    for match in pattern.finditer(block):
        words.append(
            {
                "title": match.group("title").strip(),
                "stars": (match.group("stars") or "").strip(),
                "pos": match.start(),
            }
        )
    return words


def parse_root_headings(block: str) -> list[dict[str, object]]:
    appendix_pos = block.index(r"\appendix")
    headings: list[dict[str, object]] = []

    for match in re.finditer(r"^\\chapter\{(.+?)\}\s*$", block, re.M):
        headings.append({"title": match.group(1).strip(), "pos": match.start()})

    appendix_block = block[appendix_pos:]
    for match in re.finditer(r"^\\subsection\{(.+?)\}\s*$", appendix_block, re.M):
        headings.append({"title": match.group(1).strip(), "pos": appendix_pos + match.start()})

    headings.sort(key=lambda item: int(item["pos"]))
    return headings


def split_roots(title: str) -> list[str]:
    core = title.split("(", 1)[0].strip()
    expanded = core.replace("[", ",").replace("]", "").replace(".", ",")
    parts = [part.strip() for part in expanded.split(",")]
    return [part.lower() for part in parts if part.strip()]


def normalize_headword(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\*+", "", text)
    text = collapse_spaces(text)
    return text


def extract_headword_from_line(text: str) -> str | None:
    if not text or not text[0].isalpha():
        return None
    match = re.match(r"^([A-Za-z][A-Za-z0-9' ./,()\-]*?)(?:\s+\*{1,3})?(?:\s{2,}|$)", text)
    if not match:
        return None
    headword = collapse_spaces(match.group(1))
    if not headword or len(headword) > 40:
        return None
    return headword


def page_lines(pages: list[str]) -> list[list[str]]:
    prepared: list[list[str]] = []
    for page in pages:
        prepared.append([line.rstrip() for line in page.splitlines() if line.strip()])
    return prepared


def build_headword_page_map(pages: list[str]) -> dict[str, list[int]]:
    mapping: dict[str, list[int]] = defaultdict(list)
    for page_no, lines in enumerate(page_lines(pages), start=1):
        seen_on_page: set[str] = set()
        for line in lines:
            headword = extract_headword_from_line(line)
            if not headword:
                continue
            key = normalize_headword(headword)
            if not key or key in seen_on_page:
                continue
            mapping[key].append(page_no)
            seen_on_page.add(key)
    return dict(mapping)


def find_word_pages(
    words: list[dict[str, object]],
    pages: list[str],
    offset: int,
    start_page_no: int | None = None,
) -> tuple[dict[str, list[int]], list[int]]:
    headword_pages = build_headword_page_map(pages)
    current_page_no = start_page_no if start_page_no is not None else offset + 1
    entry_pages: dict[str, set[int]] = defaultdict(set)
    ordered_pages: list[int] = []

    for word in words:
        target = normalize_headword(str(word["title"]))
        pages_for_word = headword_pages.get(target, [])
        idx = bisect_left(pages_for_word, current_page_no)
        if idx < len(pages_for_word):
            found_page_no = pages_for_word[idx]
        elif pages_for_word:
            found_page_no = pages_for_word[-1]
        else:
            found_page_no = current_page_no

        current_page_no = found_page_no
        printed_page = found_page_no - offset
        entry_pages[str(word["title"])].add(printed_page)
        ordered_pages.append(printed_page)

    return {title: sorted(page_list) for title, page_list in entry_pages.items()}, ordered_pages


def build_root_entries(headings: list[dict[str, object]], words: list[dict[str, object]], word_pages: list[int]) -> dict[str, list[int]]:
    entries: dict[str, set[int]] = defaultdict(set)
    word_idx = 0

    for heading_idx, heading in enumerate(headings):
        start_pos = int(heading["pos"])
        end_pos = int(headings[heading_idx + 1]["pos"]) if heading_idx + 1 < len(headings) else 10**18

        while word_idx < len(words) and int(words[word_idx]["pos"]) < start_pos:
            word_idx += 1

        probe_idx = word_idx
        while probe_idx < len(words) and int(words[probe_idx]["pos"]) < end_pos:
            page = word_pages[probe_idx]
            for root in split_roots(str(heading["title"])):
                entries[root].add(page)
            break

    return {root: sorted(page_list) for root, page_list in entries.items()}


def format_index(note: str, entries: dict[str, list[int]], columns: int, size_command: str) -> str:
    lines = [
        rf"\noindent {note}\par",
        r"\medskip",
        r"\begingroup",
        size_command,
        rf"\begin{{multicols}}{{{columns}}}",
        r"\raggedcolumns",
    ]
    current_group = ""
    for key in sorted(entries, key=sort_key):
        group = first_letter(key)
        if group != current_group:
            lines.append(rf"\IndexGroup{{{tex_escape(group)}}}")
            current_group = group
        page_text = ", ".join(str(page) for page in entries[key])
        lines.append(rf"\IndexEntry{{{tex_escape(key)}}}{{{tex_escape(page_text)}}}")
    lines.extend([r"\end{multicols}", r"\endgroup", ""])
    return "\n".join(lines)


def main() -> None:
    tex = TEX_PATH.read_text(encoding="utf-8")
    block = body_block(tex)
    words = parse_words(block)
    headings = parse_root_headings(block)
    pages = load_pdf_pages()
    offset = page_offset()

    word_entries, ordered_word_pages = find_word_pages(words, pages, offset)
    root_entries = build_root_entries(headings, words, ordered_word_pages)

    ROOT_INDEX_PATH.write_text(
        format_index(
            "词根索引收录正文 200 个章节词根及附录补充词根，按字母顺序整理。",
            root_entries,
            columns=4,
            size_command=r"\footnotesize",
        ),
        encoding="utf-8",
    )
    WORD_INDEX_PATH.write_text(
        format_index(
            "单词索引按全书所有 \\texttt{word} 词条自动整理，正文与附录统一纳入。",
            word_entries,
            columns=4,
            size_command=r"\scriptsize",
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
