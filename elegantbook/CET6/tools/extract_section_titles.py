from pathlib import Path
import re


base = Path(__file__).resolve().parent.parent / "cet 6" / "_analysis_output" / "section_b_texts"

for p in sorted(base.glob("*.txt")):
    lines = [line.strip() for line in p.read_text(encoding="utf-8", errors="ignore").splitlines()]
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
    print(p.name.encode("unicode_escape").decode(), "=>", title.encode("unicode_escape").decode())
