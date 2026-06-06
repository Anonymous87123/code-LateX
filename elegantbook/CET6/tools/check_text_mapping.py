from pathlib import Path


base = Path(__file__).resolve().parent.parent / "cet 6"
pdfs = sorted(p.stem for p in base.glob("*.pdf"))
txts = {p.stem for p in (base / "_analysis_output" / "section_b_texts").glob("*.txt")}

print("pdf", len(pdfs), "txt", len(txts))
for stem in pdfs:
    print(("Y" if stem in txts else "N"), stem.encode("unicode_escape").decode())
