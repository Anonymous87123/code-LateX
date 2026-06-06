from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parent.parent / "cet 6"
targets = [
    "2024年6月六级第一套原题.pdf",
    "2024年6月六级第二套原题.pdf",
    "2024年6月六级第三套原题.pdf",
]

for name in targets:
    path = ROOT / name
    print("=" * 20, name, "=" * 20)
    with pdfplumber.open(path) as pdf:
        print("pages", len(pdf.pages))
        for i, page in enumerate(pdf.pages[:3]):
            text = (page.extract_text() or "")[:2500]
            print("--- page", i + 1, "---")
            print(text)
