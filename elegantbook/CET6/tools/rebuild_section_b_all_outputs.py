from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


COMMANDS = [
    [sys.executable, "tools/add_ocr_manuals_to_section_b_texts.py"],
    [sys.executable, "tools/build_manual_truth_and_charts.py"],
    [sys.executable, "tools/analyze_section_b_relations.py"],
    [sys.executable, "tools/analyze_section_b_deeper_patterns.py"],
    [sys.executable, "tools/convert_section_b_md_to_tex.py"],
]


def run(cmd: list[str]) -> None:
    print("RUN", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    for cmd in COMMANDS:
        run(cmd)


if __name__ == "__main__":
    main()
