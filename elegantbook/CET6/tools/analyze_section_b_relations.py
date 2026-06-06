from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cet 6" / "_analysis_output"


QUESTION_NUMS = list(range(36, 46))


def reconstruct_paragraph_index(position_pct: float, paragraph_count: float) -> int:
    return int(round((position_pct * paragraph_count / 100.0) - 0.5)) + 1


def to_band_20(pct: float) -> str:
    if pct <= 20:
        return "0-20%"
    if pct <= 40:
        return "20-40%"
    if pct <= 60:
        return "40-60%"
    if pct <= 80:
        return "60-80%"
    return "80-100%"


def to_band_10(pct: float) -> str:
    start = min(int((pct - 1e-9) // 10) * 10, 90)
    if pct <= 0:
        start = 0
    return f"{start}-{start + 10}%"


def contiguous_window_coverages(pcts: pd.Series, step: int, window_count: int) -> tuple[str, float]:
    labels = []
    buckets = []
    start = 0
    while start < 100:
        end = start + step
        labels.append(f"{start}-{end}%")
        buckets.append(((pcts > start) if start > 0 else (pcts >= 0)) & (pcts <= end))
        start += step

    best_label = ""
    best_pct = -1.0
    for i in range(len(labels) - window_count + 1):
        mask = pd.Series(False, index=pcts.index)
        for j in range(window_count):
            mask = mask | buckets[i + j]
        pct = round(mask.mean() * 100, 2)
        if pct > best_pct:
            best_pct = pct
            best_label = f"{labels[i].split('-')[0]}-{labels[i + window_count - 1].split('-')[1]}"
    return best_label, best_pct


def build_base_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(OUT / "manual_truth_records.csv")
    df_pos = df[df["paragraph_position_pct"].notna()].copy()
    df_pos["paragraph_index"] = [
        reconstruct_paragraph_index(pct, cnt)
        for pct, cnt in zip(df_pos["paragraph_position_pct"], df_pos["paragraph_count"])
    ]
    df_pos["band_20"] = df_pos["paragraph_position_pct"].map(to_band_20)
    df_pos["band_10"] = df_pos["paragraph_position_pct"].map(to_band_10)

    pos_wide = df_pos.pivot(index="title", columns="question_number", values="paragraph_index")
    pct_wide = df_pos.pivot(index="title", columns="question_number", values="paragraph_position_pct")
    letter_wide = df.pivot(index="title", columns="question_number", values="answer_letter")

    merged = pd.DataFrame(index=sorted(set(df["title"])))
    for q in QUESTION_NUMS:
        if q in pos_wide:
            merged[f"idx_{q}"] = pos_wide[q]
        if q in pct_wide:
            merged[f"pct_{q}"] = pct_wide[q]
        if q in letter_wide:
            merged[f"letter_{q}"] = letter_wide[q]
    return df_pos, merged


def analyze_pairs(df_pos: pd.DataFrame, merged: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for q1 in QUESTION_NUMS:
        for q2 in QUESTION_NUMS:
            if q1 >= q2:
                continue
            a = merged[[f"idx_{q1}", f"idx_{q2}", f"pct_{q1}", f"pct_{q2}"]].dropna()
            if a.empty:
                continue
            gap = a[f"idx_{q2}"] - a[f"idx_{q1}"]
            pct_gap = a[f"pct_{q2}"] - a[f"pct_{q1}"]
            rows.append(
                {
                    "q1": q1,
                    "q2": q2,
                    "count": len(a),
                    "pearson_pct": round(a[f"pct_{q1}"].corr(a[f"pct_{q2}"], method="pearson"), 4),
                    "spearman_pct": round(a[f"pct_{q1}"].corr(a[f"pct_{q2}"], method="spearman"), 4),
                    "q1_before_q2_pct": round((gap > 0).mean() * 100, 2),
                    "same_paragraph_pct": round((gap == 0).mean() * 100, 2),
                    "within_1_paragraph_pct": round((gap.abs() <= 1).mean() * 100, 2),
                    "within_2_paragraph_pct": round((gap.abs() <= 2).mean() * 100, 2),
                    "within_3_paragraph_pct": round((gap.abs() <= 3).mean() * 100, 2),
                    "same_20_band_pct": round(
                        (
                            a[f"pct_{q1}"].map(to_band_20)
                            == a[f"pct_{q2}"].map(to_band_20)
                        ).mean()
                        * 100,
                        2,
                    ),
                    "same_half_pct": round(
                        (((a[f"pct_{q1}"] <= 50) & (a[f"pct_{q2}"] <= 50)) | ((a[f"pct_{q1}"] > 50) & (a[f"pct_{q2}"] > 50))).mean()
                        * 100,
                        2,
                    ),
                    "median_gap_paragraphs": round(gap.median(), 2),
                    "mean_gap_paragraphs": round(gap.mean(), 2),
                    "std_gap_paragraphs": round(gap.std(ddof=1), 2),
                    "median_gap_pct": round(pct_gap.median(), 2),
                }
            )
    pair_df = pd.DataFrame(rows).sort_values(["q1", "q2"])
    pair_df.to_csv(OUT / "question_pair_relation_stats.csv", index=False, encoding="utf-8-sig")
    return pair_df


def analyze_adjacent_pairs(merged: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for q in range(36, 45):
        a = merged[[f"idx_{q}", f"idx_{q+1}", f"pct_{q}", f"pct_{q+1}", f"letter_{q}", f"letter_{q+1}"]].dropna()
        if a.empty:
            continue
        gap = a[f"idx_{q+1}"] - a[f"idx_{q}"]
        letter_gap = (
            a[f"letter_{q+1}"].map(lambda x: ord(x) - ord("A") + 1)
            - a[f"letter_{q}"].map(lambda x: ord(x) - ord("A") + 1)
        )
        gap_counts = gap.value_counts().sort_values(ascending=False)
        top_gap = int(gap_counts.index[0])
        top_gap_pct = round(gap_counts.iloc[0] * 100 / len(gap), 2)
        second_gap = int(gap_counts.index[1]) if len(gap_counts) > 1 else None
        second_gap_pct = round(gap_counts.iloc[1] * 100 / len(gap), 2) if len(gap_counts) > 1 else None
        rows.append(
            {
                "q1": q,
                "q2": q + 1,
                "count": len(a),
                "q1_before_q2_pct": round((gap > 0).mean() * 100, 2),
                "within_1_paragraph_pct": round((gap.abs() <= 1).mean() * 100, 2),
                "within_2_paragraph_pct": round((gap.abs() <= 2).mean() * 100, 2),
                "within_3_paragraph_pct": round((gap.abs() <= 3).mean() * 100, 2),
                "same_20_band_pct": round(
                    (
                        a[f"pct_{q}"].map(to_band_20)
                        == a[f"pct_{q+1}"].map(to_band_20)
                    ).mean()
                    * 100,
                    2,
                ),
                "median_gap_paragraphs": round(gap.median(), 2),
                "mean_gap_paragraphs": round(gap.mean(), 2),
                "top_gap_paragraphs": top_gap,
                "top_gap_pct": top_gap_pct,
                "second_gap_paragraphs": second_gap,
                "second_gap_pct": second_gap_pct,
                "within_2_letters_pct": round((letter_gap.abs() <= 2).mean() * 100, 2),
                "within_4_letters_pct": round((letter_gap.abs() <= 4).mean() * 100, 2),
                "median_letter_gap": round(letter_gap.median(), 2),
            }
        )
    adj_df = pd.DataFrame(rows).sort_values(["q1", "q2"])
    adj_df.to_csv(OUT / "adjacent_question_relation_stats.csv", index=False, encoding="utf-8-sig")
    return adj_df


def analyze_question_features(df_pos: pd.DataFrame, pair_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for q in QUESTION_NUMS:
        q_df = df_pos[df_pos["question_number"] == q].copy()
        if q_df.empty:
            continue
        contig40_label, contig40_pct = contiguous_window_coverages(q_df["paragraph_position_pct"], step=20, window_count=2)
        contig60_label, contig60_pct = contiguous_window_coverages(q_df["paragraph_position_pct"], step=20, window_count=3)
        contig30_label, contig30_pct = contiguous_window_coverages(q_df["paragraph_position_pct"], step=10, window_count=3)
        contig50_label, contig50_pct = contiguous_window_coverages(q_df["paragraph_position_pct"], step=10, window_count=5)

        neighbor_pairs = pair_df[(pair_df["q1"] == q - 1) & (pair_df["q2"] == q)].copy()
        neighbor_pairs = pd.concat(
            [
                neighbor_pairs,
                pair_df[(pair_df["q1"] == q) & (pair_df["q2"] == q + 1)],
            ],
            ignore_index=True,
        )

        avg_neighbor_spearman = round(neighbor_pairs["spearman_pct"].mean(), 4) if not neighbor_pairs.empty else None
        avg_neighbor_within2 = round(neighbor_pairs["within_2_paragraph_pct"].mean(), 2) if not neighbor_pairs.empty else None
        avg_neighbor_order = round(neighbor_pairs["q1_before_q2_pct"].mean(), 2) if not neighbor_pairs.empty else None

        rows.append(
            {
                "question_number": q,
                "count": len(q_df),
                "top2_20_band_coverage_pct": round(
                    q_df["band_20"].value_counts(normalize=True).sort_values(ascending=False).head(2).sum() * 100,
                    2,
                ),
                "best_contiguous_40_window": contig40_label,
                "best_contiguous_40_coverage_pct": contig40_pct,
                "best_contiguous_60_window": contig60_label,
                "best_contiguous_60_coverage_pct": contig60_pct,
                "best_contiguous_30_window": contig30_label,
                "best_contiguous_30_coverage_pct": contig30_pct,
                "best_contiguous_50_window": contig50_label,
                "best_contiguous_50_coverage_pct": contig50_pct,
                "avg_neighbor_spearman": avg_neighbor_spearman,
                "avg_neighbor_within_2_paragraph_pct": avg_neighbor_within2,
                "avg_neighbor_order_metric": avg_neighbor_order,
            }
        )
    feat_df = pd.DataFrame(rows).sort_values("question_number")
    feat_df.to_csv(OUT / "question_strategy_features.csv", index=False, encoding="utf-8-sig")
    return feat_df


def main() -> None:
    df_pos, merged = build_base_tables()
    pair_df = analyze_pairs(df_pos, merged)
    analyze_adjacent_pairs(merged)
    analyze_question_features(df_pos, pair_df)
    print("wrote: question_pair_relation_stats.csv, adjacent_question_relation_stats.csv, question_strategy_features.csv")


if __name__ == "__main__":
    main()
