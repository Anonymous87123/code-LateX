import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent / "cet 6"
TEXT_DIR = ROOT / "_analysis_output" / "section_b_texts"

QUESTION_RE = re.compile(r"\b(3[6-9]|4[0-5])\.\s*(.+?)(?=(?:\b(?:3[6-9]|4[0-5])\.)|$)", re.S)
PARAGRAPH_RE = re.compile(r"([A-K])\)\s*(.+?)(?=(?:\b[A-K]\))|(?:\b(?:3[6-9]|4[0-5])\.)|$)", re.S)

for path in sorted(TEXT_DIR.glob("*.txt")):
    text = path.read_text(encoding="utf-8")
    paragraphs = PARAGRAPH_RE.findall(text)
    questions = QUESTION_RE.findall(text)
    status = "OK" if len(paragraphs) >= 8 and len(questions) == 10 else "BAD"
    print(f"{status} | paras={len(paragraphs):02d} questions={len(questions):02d} | {path.name}")
