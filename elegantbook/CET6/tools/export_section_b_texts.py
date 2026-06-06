import json
import re
from pathlib import Path

import pdfplumber


ROOT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = ROOT_DIR / "cet 6"
OUT_DIR = BASE_DIR / "_analysis_output"
TEXT_DIR = OUT_DIR / "section_b_texts"


SECTION_B_RE = re.compile(
    r"Reading Comprehension.*?Section B(.*?)(?:Section C|Passage One|Part IV Translation|Translation \(30 minutes\)|Translation \(30 Minutes\))",
    re.S,
)


def normalize(text: str) -> str:
    text = text.replace("\x00", " ")
    text = text.replace("\u2014", "-")
    text = text.replace("\u2013", "-")
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def extract_all_text(pdf_path: Path) -> str:
    parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return normalize("\n".join(parts))


def main():
    OUT_DIR.mkdir(exist_ok=True)
    TEXT_DIR.mkdir(exist_ok=True)
    for old_file in TEXT_DIR.glob("*.txt"):
        old_file.unlink()

    report = []
    for pdf_path in sorted(BASE_DIR.glob("*.pdf")):
        text = extract_all_text(pdf_path)
        has_section_b = "Section B" in text and "36." in text
        duplicate_hint = None
        for line in text.splitlines()[:12]:
            if "相同" in line or "一致" in line or "重复给出" in line or "不再重复列出" in line:
                duplicate_hint = line
                break

        section_text = None
        if has_section_b:
            m = SECTION_B_RE.search(text)
            if m:
                section_text = normalize("Section B\n" + m.group(1))
                safe_name = pdf_path.stem.replace("/", "_").replace("\\", "_")
                (TEXT_DIR / f"{safe_name}.txt").write_text(section_text, encoding="utf-8")

        report.append(
            {
                "file": pdf_path.name,
                "has_section_b": has_section_b,
                "duplicate_hint": duplicate_hint,
                "pages": len(pdfplumber.open(pdf_path).pages),
                "section_text_file": f"{pdf_path.stem}.txt" if section_text else None,
            }
        )

    (OUT_DIR / "section_b_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"exported={sum(1 for x in report if x['section_text_file'])} total={len(report)}")


if __name__ == "__main__":
    main()
