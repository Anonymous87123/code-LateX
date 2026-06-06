from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cet 6" / "_analysis_output" / "section_b_texts"
PACKETS = ROOT / "cet 6" / "_analysis_output" / "recheck_packets"


SPECS = [
    (
        "The_Curious_Case_of_the_Tree_That_Owns_Itself.md",
        "2024年6月六级第一套原题.txt",
    ),
    (
        "These_are_the_habits_to_avoid_if_you_want_to_make_a_behavior_change.md",
        "2024年6月六级第二套原题.txt",
    ),
    (
        "Blame_your_worthless_workdays_on_meeting_recovery_syndrome.md",
        "2024年6月六级第三套原题.txt",
    ),
]

INTRO = (
    "Section B\n"
    "Directions: In this section, you are going to read a passage with ten statements attached to it. "
    "Each statement contains information given in one of the paragraphs. Identify the paragraph from which "
    "the information is derived. You may choose a paragraph more than once. Each paragraph is marked with a "
    "letter. Answer the questions by making the corresponding letter on Answer Sheet 2.\n"
)


def normalize_body(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def parse_packet(path: Path) -> tuple[str, list[tuple[str, str]], list[tuple[int, str]]]:
    text = normalize_body(path.read_text(encoding="utf-8"))
    lines = text.splitlines()
    if not lines:
        raise ValueError(f"empty packet: {path}")

    title = lines[0].strip()

    para_match = re.search(
        r"(?ms)^Paragraphs\s*\n(?P<body>.+)$",
        text,
    )
    if not para_match:
        raise ValueError(f"missing paragraphs block: {path}")
    para_block = para_match.group("body")
    paragraphs = re.findall(r"(?ms)^([A-R])\)\s*(.+?)(?=^\s*[A-R]\)\s*|\Z)", para_block)
    paragraphs = [(letter, normalize_body(body)) for letter, body in paragraphs]

    stmt_match = re.search(
        r"(?ms)^Statements\s*\n(?P<body>.+?)^\s*Paragraphs\s*$",
        text,
    )
    if not stmt_match:
        raise ValueError(f"missing statements block: {path}")
    stmt_block = stmt_match.group("body")
    questions = re.findall(r"(?ms)^\s*(3[6-9]|4[0-5])\.\s*(.+?)(?=^\s*(?:3[6-9]|4[0-5])\.\s*|\Z)", stmt_block)
    questions = [(int(num), normalize_body(body)) for num, body in questions]

    return title, paragraphs, questions


def build_text(title: str, paragraphs: list[tuple[str, str]], questions: list[tuple[int, str]]) -> str:
    lines = [INTRO.rstrip("\n"), title]
    for letter, body in paragraphs:
        lines.append(f"{letter}) {body}")
    for num, body in questions:
        lines.append(f"{num}. {body}")
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for packet_name, out_name in SPECS:
        title, paragraphs, questions = parse_packet(PACKETS / packet_name)
        out_path = OUT / out_name
        out_path.write_text(build_text(title, paragraphs, questions), encoding="utf-8")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
