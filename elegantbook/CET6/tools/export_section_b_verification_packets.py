import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT / "cet 6" / "_analysis_output" / "section_b_texts"
OUT_DIR = ROOT / "cet 6" / "_analysis_output" / "verification_packets"

MANUAL_ANSWERS = {
    "The Doctor Will Skype You Now": ["E", "B", "J", "D", "K", "F", "C", "G", "A", "H"],
    "Saving Our Planet": ["F", "B", "H", "D", "K", "C", "G", "A", "J", "E"],
    "Is computer coding a foreign language?": ["L", "E", "K", "G", "D", "H", "B", "J", "C", "N"],
    "This man is running 7 marathons on 7 continents in 7 days": ["E", "I", "D", "A", "F", "K", "H", "I", "C", "G"],
    "Fear of Nature: An Emerging Threat to Conservation": ["F", "A", "J", "C", "G", "P", "E", "M", "D", "N"],
    "San Francisco Has Become One Huge Metaphor for Economic Inequality in America": ["E", "J", "B", "G", "D", "M", "H", "C", "K", "F"],
    "The lifesaving power of gratitude": ["C", "G", "A", "I", "F", "K", "D", "M", "B", "H"],
    "The problem with being perfect": ["E", "A", "F", "C", "H", "B", "I", "E", "K", "G"],
    "African countries must get smarter with their agriculture": ["E", "H", "B", "G", "C", "F", "I", "A", "D", "J"],
    "Treasure Fever": ["F", "B", "I", "D", "G", "L", "C", "J", "E", "K"],
    "Why we need tiny colleges": ["G", "D", "J", "H", "B", "I", "C", "L", "E", "N"],
    "Classical music aims to evolve, build audiences without alienating old guard": ["E", "L", "A", "M", "D", "H", "B", "O", "K", "N"],
    "Are Forgotten Crops the Future of Food?": ["F", "C", "G", "J", "H", "O", "D", "I", "E", "K"],
    "What Is a Super Blood Wolf Moon?": ["E", "K", "G", "B", "H", "M", "F", "N", "D", "J"],
    "The Free-Trade Paradox": ["G", "C", "I", "D", "M", "J", "E", "H", "A", "L"],
    "These are the habits to avoid if you want to make a behavior change": ["D", "I", "A", "K", "H", "F", "J", "L", "G", "K"],
    "Blame your worthless workdays on meeting recovery syndrome": ["D", "H", "N", "F", "B", "K", "E", "I", "C", "L"],
    "The Curious Case of the Tree That Owns Itself": ["C", "H", "B", "K", "I", "D", "N", "J", "E", "O"],
    "The Benefits of Solitude": ["C", "H", "B", "I", "M", "E", "O", "L", "G", "N"],
    "Why Your Library Is the Most Important Place in Town": ["G", "C", "I", "D", "A", "L", "F", "H", "B", "K"],
    "Yes, eating meat affects the environment, but cows are not killing the climate": ["E", "K", "H", "A", "I", "M", "D", "L", "C", "J"],
    "Restaurants are now employing robots-should chefs be worried?": ["C", "H", "D", "L", "A", "F", "M", "J", "O", "G"],
    "Do You Know When to Quit Wisely?": ["F", "K", "J", "E", "M", "I", "O", "C", "N", "H"],
    "The History and Meaning of Colored Traffic Lights": ["Q", "I", "A", "J", "R", "L", "F", "K", "B", "N"],
}


def extract_title_and_text(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = [line.strip() for line in text.splitlines()]
    title = ""
    for i, line in enumerate(lines):
        if re.match(r"^[A-R]\)", line):
            j = i - 1
            while j >= 0:
                cand = lines[j].strip()
                if cand and not cand.startswith("Directions") and not cand.startswith("Section B") and "paragraph" not in cand.lower():
                    title = cand
                    break
                j -= 1
            break
    return title, text


def parse_paragraphs(text: str):
    matches = list(re.finditer(r"(?m)^([A-R])\)\s*", text))
    paragraphs = {}
    for i, match in enumerate(matches):
        letter = match.group(1)
        start = match.end()
        end = len(text)
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        stmt_match = re.search(r"(?m)^\s*36\.\s*", text[start:end])
        if stmt_match:
            end = start + stmt_match.start()
        body = re.sub(r"\s+", " ", text[start:end]).strip()
        paragraphs[letter] = body
    return paragraphs


def parse_statements(text: str):
    statements = {}
    for q in range(36, 46):
        pattern = rf"^\s*{q}\.\s*(.+?)(?=^\s*{q + 1}\.|\Z)"
        match = re.search(pattern, text, re.S | re.M)
        if match:
            statements[q] = re.sub(r"\s+", " ", match.group(1)).strip()
    return statements


def slugify(title: str):
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    return slug[:80] or "untitled"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    title_map = {}
    for path in sorted(TEXT_DIR.glob("*.txt")):
        title, text = extract_title_and_text(path)
        if title in MANUAL_ANSWERS and title not in title_map:
            title_map[title] = (path, text)

    index_lines = ["title\tfile"]
    for title in sorted(MANUAL_ANSWERS):
        if title not in title_map:
            continue
        path, text = title_map[title]
        paragraphs = parse_paragraphs(text)
        statements = parse_statements(text)
        answers = MANUAL_ANSWERS[title]
        packet_lines = [title, ""]
        packet_lines.append("Current answers: " + " ".join(f"{36 + i}:{ans}" for i, ans in enumerate(answers)))
        packet_lines.append("")
        packet_lines.append("Statements")
        for q in range(36, 46):
            statement = statements.get(q, "")
            answer = answers[q - 36]
            para = paragraphs.get(answer, "")
            packet_lines.append(f"{q}. [{answer}] {statement}")
            packet_lines.append(f"   -> {answer}) {para}")
            packet_lines.append("")
        packet_lines.append("Paragraphs")
        for letter in sorted(paragraphs):
            packet_lines.append(f"{letter}) {paragraphs[letter]}")
            packet_lines.append("")
        out_path = OUT_DIR / f"{slugify(title)}.md"
        out_path.write_text("\n".join(packet_lines), encoding="utf-8")
        index_lines.append(f"{title}\t{path.name}")

    (OUT_DIR / "index.tsv").write_text("\n".join(index_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
