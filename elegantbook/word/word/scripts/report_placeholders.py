from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


PLACEHOLDER_PATTERNS = {
    "example_placeholder": re.compile(r"This entry shows a common use of"),
    "collocation_placeholder": re.compile(r"A common collocation is|常见搭配："),
}


def build_report(tex_path: Path) -> list[tuple[str, dict[str, int]]]:
    chapter = "UNASSIGNED"
    counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "word_count": 0,
            "example_placeholder": 0,
            "collocation_placeholder": 0,
        }
    )

    for line in tex_path.read_text(encoding="utf-8").splitlines():
        chapter_match = re.match(r"\\chapter\{(.+)\}", line)
        if chapter_match:
            chapter = chapter_match.group(1)
        if r"\begin{word}" in line:
            counts[chapter]["word_count"] += 1
        for key, pattern in PLACEHOLDER_PATTERNS.items():
            if pattern.search(line):
                counts[chapter][key] += 1

    return sorted(
        counts.items(),
        key=lambda item: (
            item[1]["example_placeholder"] + item[1]["collocation_placeholder"],
            item[1]["word_count"],
        ),
        reverse=True,
    )


def render_markdown(rows: list[tuple[str, dict[str, int]]]) -> str:
    lines = [
        "# Placeholder Density by Chapter",
        "",
        "| Rank | Chapter | Words | Example placeholders | Collocation placeholders | Total |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    rank = 1
    for chapter, stats in rows:
        total = stats["example_placeholder"] + stats["collocation_placeholder"]
        if total == 0:
            continue
        lines.append(
            f"| {rank} | {chapter} | {stats['word_count']} | "
            f"{stats['example_placeholder']} | {stats['collocation_placeholder']} | {total} |"
        )
        rank += 1
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tex", default="word.tex")
    parser.add_argument("--out", default="tmp/polish_chapter_rank.md")
    args = parser.parse_args()

    rows = build_report(Path(args.tex))
    output = render_markdown(rows)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
