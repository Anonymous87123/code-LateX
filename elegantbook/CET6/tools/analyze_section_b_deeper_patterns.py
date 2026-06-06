from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cet 6" / "_analysis_output"
QUESTION_NUMS = list(range(36, 46))


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


def to_half(pct: float) -> str:
    return "前半区" if pct <= 50 else "后半区"


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


def build_wide_tables() -> pd.DataFrame:
    df = pd.read_csv(OUT / "manual_truth_records.csv")
    df = df[df["paragraph_position_pct"].notna()].copy()

    pct_wide = df.pivot(index="title", columns="question_number", values="paragraph_position_pct")
    letter_wide = df.pivot(index="title", columns="question_number", values="answer_letter")
    para_count = df.groupby("title")["paragraph_count"].first()

    wide = pd.DataFrame(index=sorted(df["title"].unique()))
    for q in QUESTION_NUMS:
        wide[f"pct_{q}"] = pct_wide[q]
        wide[f"band20_{q}"] = pct_wide[q].map(to_band_20)
        wide[f"half_{q}"] = pct_wide[q].map(to_half)
        wide[f"letter_{q}"] = letter_wide[q]
    wide["paragraph_count"] = para_count
    return wide


def analyze_order_profiles(wide: pd.DataFrame) -> pd.DataFrame:
    pct_cols = [f"pct_{q}" for q in QUESTION_NUMS]
    ranks = wide[pct_cols].rank(axis=1, method="min")
    rows = []
    for q in QUESTION_NUMS:
        s = ranks[f"pct_{q}"]
        vc = s.value_counts(normalize=True).sort_index() * 100
        top = vc.sort_values(ascending=False).head(3)
        rows.append(
            {
                "question_number": q,
                "count": int(s.notna().sum()),
                "earliest_pct": round((s == 1).mean() * 100, 2),
                "top2_earliest_pct": round((s <= 2).mean() * 100, 2),
                "top3_earliest_pct": round((s <= 3).mean() * 100, 2),
                "latest_pct": round((s == 10).mean() * 100, 2),
                "top2_latest_pct": round((s >= 9).mean() * 100, 2),
                "top3_latest_pct": round((s >= 8).mean() * 100, 2),
                "median_rank": round(float(s.median()), 2),
                "mean_rank": round(float(s.mean()), 2),
                "most_common_rank": int(top.index[0]),
                "most_common_rank_pct": round(float(top.iloc[0]), 2),
                "second_common_rank": int(top.index[1]),
                "second_common_rank_pct": round(float(top.iloc[1]), 2),
                "third_common_rank": int(top.index[2]),
                "third_common_rank_pct": round(float(top.iloc[2]), 2),
            }
        )
    order_df = pd.DataFrame(rows).sort_values("question_number")
    order_df.to_csv(OUT / "question_order_profile.csv", index=False, encoding="utf-8-sig")
    return order_df


def analyze_conditional_windows(wide: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    base_rows = []
    for q in QUESTION_NUMS:
        pcts = wide[f"pct_{q}"].dropna()
        w40_label, w40_pct = contiguous_window_coverages(pcts, step=10, window_count=4)
        w30_label, w30_pct = contiguous_window_coverages(pcts, step=10, window_count=3)
        w50_label, w50_pct = contiguous_window_coverages(pcts, step=10, window_count=5)
        base_rows.append(
            {
                "question_number": q,
                "base_best_30_window": w30_label,
                "base_best_30_coverage_pct": w30_pct,
                "base_best_40_window": w40_label,
                "base_best_40_coverage_pct": w40_pct,
                "base_best_50_window": w50_label,
                "base_best_50_coverage_pct": w50_pct,
            }
        )
    base_df = pd.DataFrame(base_rows)
    base_map = base_df.set_index("question_number").to_dict(orient="index")

    rows = []
    for anchor in QUESTION_NUMS:
        band_col = f"band20_{anchor}"
        half_col = f"half_{anchor}"

        for condition_type, condition_values in (
            ("half", ["前半区", "后半区"]),
            ("band20", ["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"]),
        ):
            source_col = half_col if condition_type == "half" else band_col
            for condition_value in condition_values:
                subset = wide[wide[source_col] == condition_value].copy()
                support = len(subset)
                if support < 8:
                    continue
                support_pct = round(support * 100 / len(wide), 2)
                for target in QUESTION_NUMS:
                    if target == anchor:
                        continue
                    target_pcts = subset[f"pct_{target}"].dropna()
                    if len(target_pcts) < 8:
                        continue
                    cond40_label, cond40_pct = contiguous_window_coverages(target_pcts, step=10, window_count=4)
                    cond30_label, cond30_pct = contiguous_window_coverages(target_pcts, step=10, window_count=3)
                    cond50_label, cond50_pct = contiguous_window_coverages(target_pcts, step=10, window_count=5)
                    base_info = base_map[target]
                    rows.append(
                        {
                            "anchor_question": anchor,
                            "target_question": target,
                            "condition_type": condition_type,
                            "condition_value": condition_value,
                            "support_count": support,
                            "support_pct": support_pct,
                            "target_best_30_window": cond30_label,
                            "target_best_30_coverage_pct": cond30_pct,
                            "target_best_40_window": cond40_label,
                            "target_best_40_coverage_pct": cond40_pct,
                            "target_best_50_window": cond50_label,
                            "target_best_50_coverage_pct": cond50_pct,
                            "base_best_30_window": base_info["base_best_30_window"],
                            "base_best_30_coverage_pct": base_info["base_best_30_coverage_pct"],
                            "base_best_40_window": base_info["base_best_40_window"],
                            "base_best_40_coverage_pct": base_info["base_best_40_coverage_pct"],
                            "base_best_50_window": base_info["base_best_50_window"],
                            "base_best_50_coverage_pct": base_info["base_best_50_coverage_pct"],
                            "gain_30_pct": round(cond30_pct - float(base_info["base_best_30_coverage_pct"]), 2),
                            "gain_40_pct": round(cond40_pct - float(base_info["base_best_40_coverage_pct"]), 2),
                            "gain_50_pct": round(cond50_pct - float(base_info["base_best_50_coverage_pct"]), 2),
                            "target_median_pct": round(float(target_pcts.median()), 2),
                        }
                    )

    cond_df = pd.DataFrame(rows).sort_values(
        ["gain_40_pct", "gain_30_pct", "support_count", "anchor_question", "target_question"],
        ascending=[False, False, False, True, True],
    )
    cond_df.to_csv(OUT / "conditional_window_gain_stats.csv", index=False, encoding="utf-8-sig")

    leverage_rows = []
    for anchor in QUESTION_NUMS:
        a = cond_df[cond_df["anchor_question"] == anchor].copy()
        if a.empty:
            continue
        useful = a[(a["gain_40_pct"] >= 10) & (a["support_count"] >= 10)].copy()
        strong = a[(a["gain_40_pct"] >= 15) & (a["support_count"] >= 10)].copy()
        top3 = a.head(3)
        leverage_rows.append(
            {
                "anchor_question": anchor,
                "rule_count_gain10": int(len(useful)),
                "rule_count_gain15": int(len(strong)),
                "best_gain_40_pct": round(float(a["gain_40_pct"].max()), 2),
                "median_gain_40_pct": round(float(a["gain_40_pct"].median()), 2),
                "top3_avg_gain_40_pct": round(float(top3["gain_40_pct"].mean()), 2),
                "top_rule_target": int(a.iloc[0]["target_question"]),
                "top_rule_condition": f"{a.iloc[0]['condition_type']}={a.iloc[0]['condition_value']}",
                "top_rule_support_count": int(a.iloc[0]["support_count"]),
                "top_rule_target_window": a.iloc[0]["target_best_40_window"],
            }
        )
    leverage_df = pd.DataFrame(leverage_rows).sort_values(
        ["rule_count_gain15", "top3_avg_gain_40_pct", "best_gain_40_pct", "anchor_question"],
        ascending=[False, False, False, True],
    )
    leverage_df.to_csv(OUT / "anchor_leverage_summary.csv", index=False, encoding="utf-8-sig")
    return cond_df, leverage_df


def analyze_half_split_patterns(wide: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for title, row in wide.iterrows():
        front_count = 0
        back_count = 0
        for q in QUESTION_NUMS:
            if row[f"pct_{q}"] <= 50:
                front_count += 1
            else:
                back_count += 1
        rows.append(
            {
                "title": title,
                "front_half_count": front_count,
                "back_half_count": back_count,
            }
        )
    split_df = pd.DataFrame(rows)
    summary = (
        split_df.groupby(["front_half_count", "back_half_count"])
        .size()
        .reset_index(name="count")
        .sort_values(["count", "front_half_count"], ascending=[False, True])
    )
    summary.to_csv(OUT / "question_half_split_patterns.csv", index=False, encoding="utf-8-sig")
    return summary


def analyze_capacity_patterns(wide: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    per_title_rows = []
    for title, row in wide.iterrows():
        pcts = [float(row[f"pct_{q}"]) for q in QUESTION_NUMS]
        band_counts = {
            "0-20%": 0,
            "20-40%": 0,
            "40-60%": 0,
            "60-80%": 0,
            "80-100%": 0,
        }
        for pct in pcts:
            band_counts[to_band_20(pct)] += 1
        per_title_rows.append(
            {
                "title": title,
                "front_40_count": sum(1 for pct in pcts if pct <= 40),
                "front_50_count": sum(1 for pct in pcts if pct <= 50),
                "max_single_20_band_count": max(band_counts.values()),
                "band_0_20_count": band_counts["0-20%"],
                "band_20_40_count": band_counts["20-40%"],
                "band_40_60_count": band_counts["40-60%"],
                "band_60_80_count": band_counts["60-80%"],
                "band_80_100_count": band_counts["80-100%"],
            }
        )

    per_title_df = pd.DataFrame(per_title_rows)
    per_title_df.to_csv(OUT / "question_capacity_per_title.csv", index=False, encoding="utf-8-sig")

    summary_rows = []
    for column in ("front_40_count", "front_50_count", "max_single_20_band_count"):
        counts = per_title_df[column].value_counts().sort_index()
        for value, count in counts.items():
            summary_rows.append(
                {
                    "metric": column,
                    "value": int(value),
                    "count": int(count),
                    "pct": round(float(count) * 100 / len(per_title_df), 2),
                }
            )
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT / "question_capacity_summary.csv", index=False, encoding="utf-8-sig")
    return per_title_df, summary_df


def main() -> None:
    wide = build_wide_tables()
    analyze_order_profiles(wide)
    analyze_conditional_windows(wide)
    analyze_half_split_patterns(wide)
    analyze_capacity_patterns(wide)
    print(
        "wrote: question_order_profile.csv, conditional_window_gain_stats.csv, "
        "anchor_leverage_summary.csv, question_half_split_patterns.csv, "
        "question_capacity_per_title.csv, question_capacity_summary.csv"
    )


if __name__ == "__main__":
    main()
