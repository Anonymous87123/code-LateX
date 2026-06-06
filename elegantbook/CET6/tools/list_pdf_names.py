from pathlib import Path


for i, path in enumerate(sorted((Path(__file__).resolve().parent.parent / "cet 6").glob("*.pdf")), 1):
    print(f"{i:02d} {path.name}")
