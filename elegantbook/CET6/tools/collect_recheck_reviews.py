from __future__ import annotations

import csv
import importlib.util
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REVIEWS_DIR = ROOT / "cet 6" / "_analysis_output" / "recheck_reviews"
OUT_DIR = ROOT / "cet 6" / "_analysis_output"
ANSWER_MODULE = ROOT / "tools" / "build_manual_truth_and_charts.py"


def load_manual_answers() -> dict[str, list[str]]:
    spec = importlib.util.spec_from_file_location("build_manual_truth_and_charts", ANSWER_MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.MANUAL_ANSWERS


def parse_review(path: Path) -> list[tuple[str, list[str]]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    sections = re.split(r"(?m)^##\s+", text)
    results: list[tuple[str, list[str]]] = []
    for section in sections:
        section = section.strip()
        if not section:
            continue
        lines = section.splitlines()
        title = lines[0].strip()
        m = re.search(r"Final answers:\s*(.+)", section)
        if not m:
            continue
        parts = re.findall(r"(3[6-9]|4[0-5]):([A-R])", m.group(1))
        if len(parts) != 10:
            continue
        answers = [ans for _q, ans in sorted(((int(q), ans) for q, ans in parts), key=lambda x: x[0])]
        results.append((title, answers))
    return results


def main() -> None:
    current = load_manual_answers()
    rows = []
    for path in sorted(REVIEWS_DIR.glob("batch*_review.md")):
        for title, verified in parse_review(path):
            current_answers = current.get(title, [])
            changed = current_answers != verified
            rows.append(
                {
                    "title": title,
                    "review_file": path.name,
                    "current_answers": " ".join(f"{36 + i}:{ans}" for i, ans in enumerate(current_answers)),
                    "verified_answers": " ".join(f"{36 + i}:{ans}" for i, ans in enumerate(verified)),
                    "changed": "yes" if changed else "no",
                }
            )

    out_path = OUT_DIR / "recheck_review_summary.csv"
    with out_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["title", "review_file", "current_answers", "verified_answers", "changed"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"reviews={len(rows)} out={out_path.name}")


if __name__ == "__main__":
    main()
