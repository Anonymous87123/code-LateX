from __future__ import annotations

import importlib.util
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT / "cet 6" / "_analysis_output" / "section_b_texts"
OUT_DIR = ROOT / "cet 6" / "_analysis_output" / "recheck_packets"
ANSWER_MODULE = ROOT / "tools" / "build_manual_truth_and_charts.py"
SAMPLE_PATH = ROOT / "cet 6" / "sample.txt"
SAMPLE_ONLY_TITLES = {
    "The Curious Case of the Tree That Owns Itself",
    "Blame your worthless workdays on meeting recovery syndrome",
    "These are the habits to avoid if you want to make a behavior change",
}


def load_manual_answers() -> dict[str, list[str]]:
    spec = importlib.util.spec_from_file_location("build_manual_truth_and_charts", ANSWER_MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.MANUAL_ANSWERS


def extract_title(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    for i, line in enumerate(lines):
        if re.match(r"^[A-R]\)", line):
            j = i - 1
            while j >= 0:
                cand = lines[j].strip()
                if cand and not cand.startswith("Directions") and not cand.startswith("Section B") and "paragraph" not in cand.lower():
                    return cand
                j -= 1
            break
    raise ValueError("title not found")


def parse_paragraphs(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^([A-R])\)\s*", text))
    paragraphs: dict[str, str] = {}
    for i, match in enumerate(matches):
        letter = match.group(1)
        start = match.end()
        end = len(text)
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        stmt_match = re.search(r"(?m)^\s*36\.\s*", text[start:end])
        if stmt_match:
            end = start + stmt_match.start()
        paragraphs[letter] = re.sub(r"\s+", " ", text[start:end]).strip()
    return paragraphs


def parse_statements(text: str) -> dict[int, str]:
    statements: dict[int, str] = {}
    for q in range(36, 46):
        pattern = rf"^\s*{q}\.\s*(.+?)(?=^\s*{q + 1}\.|\Z)"
        match = re.search(pattern, text, re.S | re.M)
        if match:
            statements[q] = re.sub(r"\s+", " ", match.group(1)).strip()
    return statements


def slugify(title: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    return slug[:100] or "untitled"


def extract_from_sample(sample_text: str, title: str) -> str | None:
    marker = f"{title}\n"
    start = sample_text.find(marker)
    if start < 0:
        return None
    after_title = start + len(marker)
    first_heading = sample_text.find("\n#### ", after_title)
    if first_heading < 0:
        return None
    second_heading = sample_text.find("\n#### ", first_heading + 1)
    if second_heading < 0:
        return None
    para_block = sample_text[after_title:first_heading].strip()
    question_block = sample_text[first_heading + 1:second_heading].strip()
    lines = ["Section B", "Directions:", title]
    lines.extend(line.rstrip() for line in para_block.splitlines() if line.strip())
    lines.extend(line.rstrip() for line in question_block.splitlines() if re.match(r"^\d{2}\.", line.strip()))
    return "\n".join(lines) + "\n"


def main() -> None:
    manual_answers = load_manual_answers()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    title_map: dict[str, tuple[str, str]] = {}
    for path in sorted(TEXT_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        try:
            title = extract_title(text)
        except ValueError:
            continue
        if title not in manual_answers:
            continue
        title_map[title] = (path.name, text)

    sample_text = SAMPLE_PATH.read_text(encoding="utf-8", errors="ignore")
    for title in SAMPLE_ONLY_TITLES:
        if title in title_map or title not in manual_answers:
            continue
        extracted = extract_from_sample(sample_text, title)
        if extracted:
            title_map[title] = (f"sample::{title}", extracted)

    index_lines = ["title\tfile\tpacket"]
    for title in sorted(title_map):
        file_name, text = title_map[title]
        paragraphs = parse_paragraphs(text)
        statements = parse_statements(text)
        answers = manual_answers[title]

        packet_lines = [title, ""]
        packet_lines.append("Current answers: " + " ".join(f"{36 + i}:{ans}" for i, ans in enumerate(answers)))
        packet_lines.append("")
        packet_lines.append("Statements")
        for q in range(36, 46):
            statement = statements.get(q, "")
            answer = answers[q - 36]
            packet_lines.append(f"{q}. [{answer}] {statement}")
            packet_lines.append("")
        packet_lines.append("Paragraphs")
        for letter in sorted(paragraphs):
            packet_lines.append(f"{letter}) {paragraphs[letter]}")
            packet_lines.append("")

        packet_name = f"{slugify(title)}.md"
        (OUT_DIR / packet_name).write_text("\n".join(packet_lines), encoding="utf-8")
        index_lines.append(f"{title}\t{file_name}\t{packet_name}")

    (OUT_DIR / "index.tsv").write_text("\n".join(index_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
