from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parent.parent / "cet 6"
targets = [
    "2024.12六级真题第1套.pdf",
    "2025.06六级真题第1套.pdf",
    "2025.12六级真题第1套.pdf",
]

for name in targets:
    path = ROOT / name
    print("=" * 20, name, "=" * 20)
    with pdfplumber.open(path) as pdf:
        text = "\n".join((p.extract_text() or "") for p in pdf.pages)
        idx = text.find("Part III")
        if idx < 0:
            idx = text.find("Section A")
        snippet = text[idx : idx + 9000] if idx >= 0 else text[:9000]
        print(snippet.encode("gbk", "ignore").decode("gbk"))
