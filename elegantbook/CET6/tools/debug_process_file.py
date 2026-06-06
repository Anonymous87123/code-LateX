from pathlib import Path

from extract_cet6_paragraph_matching import process_file, BASE_DIR


for pdf_path in sorted(BASE_DIR.glob("*.pdf")):
    try:
        recs = process_file(pdf_path.name)
        print(
            ("OK " if recs else "BAD"),
            len(recs),
            pdf_path.stem.encode("unicode_escape").decode(),
        )
    except Exception as exc:
        print("ERR", type(exc).__name__, str(exc), pdf_path.stem.encode("unicode_escape").decode())
