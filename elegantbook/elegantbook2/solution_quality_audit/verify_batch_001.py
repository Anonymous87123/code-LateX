# -*- coding: utf-8 -*-
"""Local verification for batch 001 (global solution 1-10).

This script is intentionally small and read-only. It checks:
- solution index still maps global 1-10 to the first exercise batch;
- no very long formula-heavy source lines remain inside the batch range;
- the ten final partial-fraction decompositions are symbolically equivalent.
"""

from __future__ import annotations

import csv
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
TEX_PATH = ROOT / "elegantbook2.tex"
INDEX_PATH = ROOT / "solution_quality_audit" / "solution_index.csv"


def main() -> None:
    lines = TEX_PATH.read_text(encoding="utf-8").splitlines()
    with INDEX_PATH.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    first_batch = rows[:10]
    assert [int(row["global_no"]) for row in first_batch] == list(range(1, 11))
    assert all(row["subsection"] == "第一节习题：模法与多项式逆元" for row in first_batch)

    start = min(int(row["solution_start"]) for row in first_batch)
    end = max(int(row["solution_end"]) for row in first_batch)
    long_formula_lines: list[tuple[int, int, str]] = []
    for line_no, text in enumerate(lines[start - 1 : end], start=start):
        if len(text) >= 170 and ("\\" in text or "$" in text):
            long_formula_lines.append((line_no, len(text), text[:180]))
    assert not long_formula_lines, long_formula_lines

    x = sp.symbols("x")
    originals = [
        (x**3 + 2) / ((x - 1) ** 2 * (x**2 + 1)),
        (x + 2) / ((x**2 + 2 * x + 2) * (x**2 + 1)),
        (x**3 + 3 * x) / (x**2 + 1) ** 2,
        1 / ((x - 1) ** 2 * (x**2 + 1) ** 2),
        (2 * x**2 + 3) / ((x - 1) * (x**2 + x + 1)),
        x**5 / (x**2 + 1) ** 3,
        x / ((x - 1) ** 2 * (x + 1) ** 2),
        x**2 / ((x**2 + 1) ** 2 * (x**2 + x + 1)),
        1 / (x * (x - 1) * (x**2 + 1)),
        x**3 / ((x - 1) * (x + 1) * (x**2 + x + 1)),
    ]
    rewritten = [
        3 / (2 * (x - 1) ** 2) + (2 * x + 1) / (2 * (x**2 + 1)),
        (3 * x + 2) / (5 * (x**2 + 2 * x + 2)) + (4 - 3 * x) / (5 * (x**2 + 1)),
        x / (x**2 + 1) + 2 * x / (x**2 + 1) ** 2,
        -1 / (2 * (x - 1))
        + 1 / (4 * (x - 1) ** 2)
        + (2 * x + 1) / (4 * (x**2 + 1))
        + x / (2 * (x**2 + 1) ** 2),
        5 / (3 * (x - 1)) + (x - 4) / (3 * (x**2 + x + 1)),
        x / (x**2 + 1) - 2 * x / (x**2 + 1) ** 2 + x / (x**2 + 1) ** 3,
        1 / (4 * (x - 1) ** 2) - 1 / (4 * (x + 1) ** 2),
        1 / (x**2 + x + 1) - 1 / (x**2 + 1) + x / (x**2 + 1) ** 2,
        -1 / x + 1 / (2 * (x - 1)) + (x - 1) / (2 * (x**2 + 1)),
        1 / (6 * (x - 1)) + 1 / (2 * (x + 1)) + (x - 1) / (3 * (x**2 + x + 1)),
    ]

    failures: list[int] = []
    for index, (original, answer) in enumerate(zip(originals, rewritten), start=1):
        if sp.simplify(original - answer) != 0:
            failures.append(index)
    assert not failures, failures

    print(
        "batch_001 verification passed: "
        f"solutions=1-10, source_lines={start}-{end}, math_equivalence=10/10"
    )


if __name__ == "__main__":
    main()
