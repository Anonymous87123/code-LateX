from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT / "cet 6" / "_analysis_output" / "section_b_texts"
MANUAL_PATH = ROOT / "tools" / "manual_full_texts_real.py"


def load_manual_texts() -> dict[str, str]:
    spec = importlib.util.spec_from_file_location("manual_full_texts_real", MANUAL_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.MANUAL_FULL_TEXTS_REAL


def extract_title(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 3:
        raise ValueError("manual text missing title line")
    return lines[2]


def main() -> None:
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    manual_texts = load_manual_texts()
    title_to_text = {extract_title(text): text if text.endswith("\n") else text + "\n" for text in manual_texts.values()}

    written = 0
    missing: list[str] = []
    for path in sorted(TEXT_DIR.glob("*.txt")):
        if not path.name.startswith(("2016", "2017", "2018", "2019", "2020", "2021")):
            continue

        current = path.read_text(encoding="utf-8", errors="ignore")
        if "Placeholder paragraph" not in current and "Placeholder statement" not in current:
            continue

        lines = [line.strip() for line in current.splitlines() if line.strip()]
        title = lines[2] if len(lines) > 2 else ""
        if title in title_to_text:
            path.write_text(title_to_text[title], encoding="utf-8")
            written += 1
        else:
            missing.append(path.name)

    print(f"written={written}")
    if missing:
        print("missing:")
        for name in missing:
            print(name)


if __name__ == "__main__":
    main()
