from pathlib import Path

import pandas as pd


base = Path(__file__).resolve().parent.parent / "cet 6" / "_analysis_output"
df = pd.read_csv(base / "manual_truth_records.csv")
df = df[df["paragraph_position_pct"].notna()].copy()

bins = [0, 20, 40, 60, 80, 100]
labels = ["0-20", "20-40", "40-60", "60-80", "80-100"]
df["bin"] = pd.cut(df["paragraph_position_pct"], bins=bins, labels=labels, include_lowest=True, right=True)

print("BINS_BY_QUESTION")
for q, g in df.groupby("question_number"):
    counts = g["bin"].value_counts().reindex(labels, fill_value=0)
    total = int(counts.sum())
    top = counts.sort_values(ascending=False)
    pieces = [f"{k}:{int(v)}({v/total:.0%})" for k, v in counts.items() if v]
    top2 = [f"{idx}:{int(val)}({val/total:.0%})" for idx, val in top.head(2).items()]
    print(f"Q{q}: " + ", ".join(pieces))
    print("  TOP2:", " / ".join(top2))

print("QUARTILES_BY_QUESTION")
for q, g in df.groupby("question_number"):
    print(
        f"Q{q}: median={g['paragraph_position_pct'].median():.1f}, "
        f"q1={g['paragraph_position_pct'].quantile(0.25):.1f}, "
        f"q3={g['paragraph_position_pct'].quantile(0.75):.1f}"
    )

print("POSITION_BY_LETTER")
for letter, g in df.groupby("answer_letter"):
    counts = g["question_number"].value_counts().sort_index()
    total = int(counts.sum())
    top = counts.sort_values(ascending=False)
    pieces = [f"Q{int(k)}:{int(v)}({v/total:.0%})" for k, v in counts.items()]
    top3 = [f"Q{int(idx)}:{int(val)}({val/total:.0%})" for idx, val in top.head(3).items()]
    print(f"{letter}: " + ", ".join(pieces))
    print("  TOP3:", " / ".join(top3))
