from __future__ import annotations

import re
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "cet 6"
OUT = BASE / "_analysis_output" / "section_b_texts"

SPECS = {
    "2016年12月英语六级真题(第2套).txt": {
        "title": "Countries Rush for Upper Hand in Antarctica",
        "letters": list("ABCDEFGHIJKLMNOPQ"),
    },
    "2016年12月英语六级真题(第3套).txt": {
        "title": "The American Workplace Is Broken. Here's How We Can Start Fixing It.",
        "letters": list("ABCDEFGHIJKLM"),
    },
    "2017年6月英语六级真题(第1套).txt": {
        "title": "The Price of Oil and the Price of Carbon",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2017年6月英语六级真题(第2套).txt": {
        "title": "Elite Math Competitions Struggle to Diversify Their Talent Pool",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2017年6月英语六级真题(第3套).txt": {
        "title": "Rich Children and Poor Ones Are Raised Very Differently",
        "letters": list("ABCDEFGHIJKLMNOPQ"),
    },
    "2017年12月英语六级真题(第1套).txt": {
        "title": "Who's Really Addicting You to Technology?",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2017年12月英语六级真题(第2套).txt": {
        "title": "Data sharing: An open mind on open data",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
    "2017年12月英语六级真题(第3套).txt": {
        "title": "Apple's Stance Highlights a More Confrontational Tech Industry",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
    "2018年6月英语六级真题(第1套).txt": {
        "title": "Peer Pressure Has a Positive Side",
        "letters": list("ABCDEFGHIJKL"),
    },
    "2018年6月英语六级真题(第2套).txt": {
        "title": "Grow Plants Without Water",
        "letters": list("ABCDEFGHIJK"),
    },
    "2018年6月英语六级真题(第3套).txt": {
        "title": "In the real world, nobody cares that you went to an Ivy League school",
        "letters": list("ABCDEFGHIJKLMN"),
    },
    "2018年12月英语六级真题(第1套).txt": {
        "title": "Do Parents Invade Children's Privacy When They Post Photos Online?",
        "letters": list("ABCDEFGHIJKLMN"),
    },
    "2018年12月英语六级真题(第2套).txt": {
        "title": "A Pioneering Woman of Science Re-Emerges after 300 Years",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
    "2018年12月英语六级真题(第3套).txt": {
        "title": "Resilience Is About How You Recharge, Not How You Endure",
        "letters": list("ABCDEFGHIJKLM"),
    },
    "2019年6月英语六级真题(第1套).txt": {
        "title": "The Best Retailers Combine Bricks and Clicks",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2019年6月英语六级真题(第2套).txt": {
        "title": "Companies Are Working with Consumers to Reduce Waste",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2019年6月英语六级真题(第3套).txt": {
        "title": "The future of personal satellite technology is here-are we ready for it?",
        "letters": list("ABCDEFGHIJKLM"),
    },
    "2019年12月英语六级真题(第1套).txt": {
        "title": "Increased Screen Time and Wellbeing Decline in Youth",
        "letters": list("ABCDEFGHIJ"),
    },
    "2019年12月英语六级真题(第2套).txt": {
        "title": "How Much Protein Do You Really Need?",
        "letters": list("ABCDEFGHIJKLMN"),
    },
    "2019年12月英语六级真题(第3套).txt": {
        "title": "Why More Farmers Are Making The Switch to Grass-Fed Meat and Dairy",
        "letters": list("ABCDEFGHIJKL"),
    },
    "2020年9月英语六级真题(第1套).txt": {
        "title": "Six Potential Brain Benefits of Bilingual Education",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
    "2020年9月英语六级真题(第2套).txt": {
        "title": "How Telemedicine Is Transforming Healthcare",
        "letters": list("ABCDEFGHIJKLMNO"),
    },
    "2020年12月英语六级真题(第1套).txt": {
        "title": "The Challenges for Artificial Intelligence in Agriculture",
        "letters": list("ABCDEFGHIJKLMNOPQR"),
    },
    "2020年12月英语六级真题(第2套).txt": {
        "title": "Slow Hope",
        "letters": list("ABCDEFGHIJK"),
    },
    "2020年12月英语六级真题(第3套).txt": {
        "title": "Why lifelong learning is the international passport to success",
        "letters": list("ABCDEFGHIJKLMNOP"),
    },
    "2021年6月英语六级真题(第2套).txt": {
        "title": "France's beloved cathedral only minutes away from complete destruction",
        "letters": list("ABCDEFGHIJK"),
    },
    "2021年6月英语六级真题(第3套).txt": {
        "title": "What Are the Ethics of CGI Actors-And Will They Replace Real Ones?",
        "letters": list("ABCDEFGHIJKL"),
    },
}


def normalize(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\r", "\n").replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text


def read_pdf(path: Path) -> str:
    parts: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return normalize("\n".join(parts))


def extract_block(text: str, title: str) -> str:
    start = text.find(title)
    if start < 0:
        raise ValueError(f"title not found: {title}")
    return text[start + len(title):]


def parse_paragraphs(block: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"(?ms)^\s*([A-R])\)\s*(.+?)(?=^\s*[A-R]\)\s*|^\s*36\.\s*|\Z)")
    return [(letter, re.sub(r"\s+", " ", body).strip()) for letter, body in pattern.findall(block)]


def parse_questions(block: str) -> list[tuple[int, str]]:
    pattern = re.compile(r"(?ms)^\s*(3[6-9]|4[0-5])\.\s*(.+?)(?=^\s*(?:3[6-9]|4[0-5])\.\s*|\Z)")
    return [(int(num), re.sub(r"\s+", " ", body).strip()) for num, body in pattern.findall(block)]


def build_text(title: str, paragraphs: list[tuple[str, str]], questions: list[tuple[int, str]]) -> str:
    lines = [
        "Section B",
        "Directions: In this section, you are going to read a passage with ten statements attached to it. Each statement contains information given in one of the paragraphs. Identify the paragraph from which the information is derived. You may choose a paragraph more than once. Each paragraph is marked with a letter. Answer the questions by marking the corresponding letter on Answer Sheet 2.",
        title,
    ]
    for letter, body in paragraphs:
        lines.append(f"{letter}) {body}")
    for num, body in questions:
        lines.append(f"{num}. {body}")
    return "\n".join(lines) + "\n"


def main() -> None:
    failures: list[str] = []
    for filename, spec in SPECS.items():
        pdf_path = BASE / filename.replace(".txt", ".pdf")
        if not pdf_path.exists():
            failures.append(f"{filename}: missing pdf")
            continue

        text = read_pdf(pdf_path)
        try:
            block = extract_block(text, spec["title"])
        except Exception as exc:
            failures.append(f"{filename}: {exc}")
            continue

        paragraphs = parse_paragraphs(block)
        questions = parse_questions(block)
        letters = [letter for letter, _ in paragraphs]

        if letters != spec["letters"]:
            failures.append(f"{filename}: letters {letters} != {spec['letters']}")
            continue
        if [num for num, _ in questions] != list(range(36, 46)):
            failures.append(f"{filename}: question numbers invalid")
            continue

        (OUT / filename).write_text(build_text(spec["title"], paragraphs, questions), encoding="utf-8")

    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
