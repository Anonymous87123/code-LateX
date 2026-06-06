import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "cet 6"
OUT = BASE / "_analysis_output"
TEXT_DIR = OUT / "section_b_texts"
POSITION_BINS = [0, 20, 40, 60, 80, 100]
POSITION_BAND_LABELS = ["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"]
HEATMAP_BINS = list(range(0, 101, 10))
HEATMAP_BAND_LABELS = [f"{start}-{start + 10}%" for start in range(0, 100, 10)]


MANUAL_ANSWERS = {
    "Can Societies Be Rich and Green?": ["I", "C", "L", "D", "K", "E", "G", "A", "N", "J"],
    "Reform and Medical Costs": ["F", "J", "A", "G", "L", "H", "C", "I", "P", "K"],
    "The Changing Generation": ["I", "B", "F", "D", "C", "K", "A", "L", "E", "J"],
    "Are We in an Innovation Lull?": ["D", "K", "B", "L", "F", "A", "H", "E", "I", "C"],
    "Countries Rush for Upper Hand in Antarctica": ["J", "C", "E", "G", "D", "I", "B", "H", "Q", "L"],
    "The American Workplace Is Broken. Here's How We Can Start Fixing It.": ["F", "B", "M", "H", "E", "K", "C", "J", "D", "B"],
    "Rich Children and Poor Ones Are Raised Very Differently": ["G", "F", "M", "D", "G", "O", "K", "H", "B", "P"],
    "Elite Math Competitions Struggle to Diversify Their Talent Pool": ["F", "A", "I", "G", "L", "E", "J", "B", "M", "H"],
    "The Price of Oil and the Price of Carbon": ["D", "L", "J", "E", "H", "A", "G", "F", "O", "B"],
    "Apple's Stance Highlights a More Confrontational Tech Industry": ["E", "M", "C", "H", "B", "J", "G", "P", "I", "D"],
    "Data sharing: An open mind on open data": ["M", "G", "D", "A", "P", "L", "B", "O", "I", "F"],
    "Who's Really Addicting You to Technology?": ["E", "L", "I", "O", "B", "J", "F", "D", "L", "G"],
    "Peer Pressure Has a Positive Side": ["H", "C", "L", "J", "G", "A", "I", "F", "K", "D"],
    "Grow Plants Without Water": ["C", "H", "A", "K", "E", "I", "G", "B", "F", "D"],
    "In the real world, nobody cares that you went to an Ivy League school": ["J", "G", "C", "K", "B", "H", "N", "A", "E", "I"],
    "Resilience Is About How You Recharge, Not How You Endure": ["D", "J", "L", "A", "E", "K", "I", "B", "G", "C"],
    "A Pioneering Woman of Science Re-Emerges after 300 Years": ["K", "I", "E", "M", "G", "O", "C", "L", "F", "D"],
    "Do Parents Invade Children's Privacy When They Post Photos Online?": ["H", "M", "N", "E", "B", "A", "J", "L", "G", "D"],
    "The Best Retailers Combine Bricks and Clicks": ["M", "G", "D", "I", "C", "H", "F", "O", "A", "K"],
    "Companies Are Working with Consumers to Reduce Waste": ["F", "C", "M", "E", "G", "N", "H", "B", "J", "D"],
    "The future of personal satellite technology is here-are we ready for it?": ["I", "C", "B", "E", "K", "F", "L", "G", "D", "J"],
    "Why More Farmers Are Making The Switch to Grass-Fed Meat and Dairy": ["F", "C", "J", "D", "G", "A", "I", "E", "B", "K"],
    "How Much Protein Do You Really Need?": ["C", "E", "A", "F", "M", "G", "B", "H", "D", "L"],
    "Increased Screen Time and Wellbeing Decline in Youth": ["G", "C", "H", "D", "B", "E", "J", "F", "I", "A"],
    "Six Potential Brain Benefits of Bilingual Education": ["H", "C", "J", "D", "M", "E", "B", "P", "G", "N"],
    "How Telemedicine Is Transforming Healthcare": ["D", "H", "E", "B", "K", "O", "G", "F", "I", "N"],
    "Why lifelong learning is the international passport to success": ["H", "E", "B", "K", "I", "C", "J", "N", "F", "M"],
    "Slow Hope": ["E", "I", "C", "K", "D", "G", "A", "F", "I", "B"],
    "The Challenges for Artificial Intelligence in Agriculture": ["D", "L", "E", "N", "F", "Q", "H", "C", "K", "M"],
    "What Are the Ethics of CGI Actors-And Will They Replace Real Ones?": ["G", "C", "J", "A", "F", "L", "B", "H", "E", "I"],
    "France's beloved cathedral only minutes away from complete destruction": ["I", "C", "K", "F", "B", "H", "A", "J", "D", "G"],
    "How Marconi Gave Us the Wireless World": ["F", "I", "D", "J", "C", "E", "K", "G", "B", "H"],
    "Why facts don't change our minds": ["D", "G", "M", "F", "N", "E", "I", "C", "O", "H"],
    "Do music lessons really make children smarter?": ["E", "N", "C", "G", "O", "H", "D", "J", "F", "I"],
    "No one in fashion is surprised that Burberry burnt 28 million of stock": ["G", "B", "K", "E", "L", "D", "F", "J", "A", "H"],
    "The Doctor Will Skype You Now": ["E", "B", "J", "D", "K", "F", "C", "G", "A", "H"],
    "Saving Our Planet": ["F", "B", "H", "D", "K", "C", "G", "A", "J", "E"],
    "Is computer coding a foreign language?": ["L", "E", "K", "G", "D", "H", "B", "J", "C", "N"],
    "This man is running 7 marathons on 7 continents in 7 days": ["E", "I", "D", "A", "F", "K", "H", "I", "C", "G"],
    "Fear of Nature: An Emerging Threat to Conservation": ["F", "A", "J", "C", "G", "P", "E", "M", "D", "N"],
    "San Francisco Has Become One Huge Metaphor for Economic Inequality in America": ["E", "J", "B", "G", "D", "M", "H", "C", "K", "F"],
    "The lifesaving power of gratitude": ["C", "G", "A", "I", "F", "K", "D", "M", "B", "H"],
    "The problem with being perfect": ["E", "A", "F", "C", "H", "B", "I", "E", "K", "G"],
    "African countries must get smarter with their agriculture": ["E", "H", "B", "G", "C", "F", "I", "A", "D", "J"],
    "Treasure Fever": ["F", "B", "I", "D", "G", "L", "C", "J", "E", "K"],
    "Why we need tiny colleges": ["G", "D", "J", "H", "B", "I", "C", "L", "E", "N"],
    "Classical music aims to evolve, build audiences without alienating old guard": ["E", "L", "A", "M", "D", "H", "B", "O", "K", "N"],
    "Are Forgotten Crops the Future of Food?": ["F", "C", "G", "J", "H", "O", "D", "I", "E", "K"],
    "What Is a Super Blood Wolf Moon?": ["E", "K", "G", "B", "H", "M", "F", "N", "D", "J"],
    "The Free-Trade Paradox": ["G", "C", "I", "D", "M", "J", "E", "H", "A", "L"],
    "These are the habits to avoid if you want to make a behavior change": ["D", "I", "A", "K", "H", "F", "J", "L", "G", "K"],
    "Blame your worthless workdays on meeting recovery syndrome": ["D", "H", "N", "F", "B", "K", "E", "I", "C", "L"],
    "The Curious Case of the Tree That Owns Itself": ["C", "H", "B", "K", "I", "D", "N", "J", "E", "O"],
    "The Benefits of Solitude": ["C", "H", "B", "I", "M", "E", "O", "L", "G", "N"],
    "Why Your Library Is the Most Important Place in Town": ["G", "C", "I", "D", "A", "L", "F", "H", "B", "K"],
    "Yes, eating meat affects the environment, but cows are not killing the climate": ["E", "K", "H", "A", "I", "M", "D", "L", "C", "J"],
    "Restaurants are now employing robots-should chefs be worried?": ["C", "H", "D", "L", "A", "F", "M", "J", "O", "G"],
    "Do You Know When to Quit Wisely?": ["F", "K", "J", "E", "M", "I", "O", "C", "N", "H"],
    "The History and Meaning of Colored Traffic Lights": ["Q", "I", "A", "J", "R", "L", "F", "K", "B", "N"],
}


DUPLICATE_MAP = {
    "2022.06六级真题第3套【可复制可搜索，打印首选】.pdf": "2022.06六级真题第2套【可复制可搜索，打印首选】.pdf",
    "2022.09英语六级真题第2套【可复制可搜索，打印首选】.pdf": "2022.09英语六级真题第1套【可复制可搜索，打印首选】.pdf",
    "2022.09英语六级真题第3套【可复制可搜索，打印首选】.pdf": "2022.09英语六级真题第1套【可复制可搜索，打印首选】.pdf",
    "2023.03英语六级真题第2套.pdf": "2023.03英语六级真题第1套.pdf",
    "2023.03英语六级真题第3套.pdf": "2023.03英语六级真题第1套.pdf",
}


OCR_TITLES = {
    "2024年6月六级第一套原题.pdf": "The Curious Case of the Tree That Owns Itself",
    "2024年6月六级第二套原题.pdf": "These are the habits to avoid if you want to make a behavior change",
    "2024年6月六级第三套原题.pdf": "Blame your worthless workdays on meeting recovery syndrome",
}

FILE_TITLE_OVERRIDES = {
    "2025.06六级真题第1套.pdf": "Why Your Library Is the Most Important Place in Town",
    "2025.06六级真题第2套.pdf": "Yes, eating meat affects the environment, but cows are not killing the climate",
    "2025.06六级真题第1套.txt": "Why Your Library Is the Most Important Place in Town",
    "2025.06六级真题第2套.txt": "Yes, eating meat affects the environment, but cows are not killing the climate",
}


def extract_title_map():
    mapping = {}
    for p in sorted(TEXT_DIR.glob("*.txt")):
        override_title = FILE_TITLE_OVERRIDES.get(p.name)
        if override_title:
            mapping[p.stem + ".pdf"] = override_title
            continue
        lines = [line.strip() for line in p.read_text(encoding="utf-8", errors="ignore").splitlines()]
        title = ""
        for i, line in enumerate(lines):
            if re.match(r"^[A-R]\)", line):
                j = i - 1
                while j >= 0:
                    cand = lines[j].strip()
                    if cand and not cand.startswith("Directions") and not cand.startswith("Section B") and "paragraph" not in cand.lower():
                        title = cand
                        break
                    j -= 1
                break
        mapping[p.stem + ".pdf"] = title
    return mapping


def parse_paragraph_blocks(text: str):
    matches = list(re.finditer(r"(?m)^([A-R])\)\s*", text))
    paragraphs = []
    for i, match in enumerate(matches):
        letter = match.group(1)
        start = match.end()
        end = len(text)
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        stmt_match = re.search(r"(?m)^\s*36\.\s*", text[start:end])
        if stmt_match:
            end = start + stmt_match.start()
        body = re.sub(r"\s+", " ", text[start:end]).strip()
        paragraphs.append((letter, body))
    return paragraphs


def parse_paragraph_positions():
    positions = {}
    for p in sorted(TEXT_DIR.glob("*.txt")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        paras = parse_paragraph_blocks(text)
        count = len(paras)
        pos = {}
        for idx, (letter, _body) in enumerate(paras):
            pos[letter] = round(((idx + 0.5) / count) * 100, 2)
        positions[p.stem + ".pdf"] = {"count": count, "positions": pos}
    return positions


def normalized_entropy(values):
    values = [float(v) for v in values]
    total = sum(values)
    if total <= 0:
        return 0.0
    probs = [v / total for v in values if v > 0]
    if len(values) <= 1:
        return 0.0
    max_entropy = math.log2(len(values))
    if max_entropy == 0:
        return 0.0
    entropy = -sum(p * math.log2(p) for p in probs)
    return entropy / max_entropy


def build_records():
    title_map = extract_title_map()
    para_map = parse_paragraph_positions()
    records = []
    seen_titles = set()
    for text_path in sorted(TEXT_DIR.glob("*.txt")):
        fname = text_path.stem + ".pdf"
        title = FILE_TITLE_OVERRIDES.get(text_path.name) or title_map.get(fname)
        if not title or title not in MANUAL_ANSWERS or title in seen_titles:
            continue

        seen_titles.add(title)
        answers = MANUAL_ANSWERS[title]
        info = para_map.get(fname, {"count": None, "positions": {}})
        for idx, ans in enumerate(answers, start=36):
            if ans is None:
                continue
            records.append(
                {
                    "file": fname,
                    "title": title,
                    "question_number": idx,
                    "answer_letter": ans,
                    "paragraph_position_pct": info["positions"].get(ans),
                    "paragraph_count": info["count"],
                    "source_type": "manual",
                }
            )

    for fname, title in OCR_TITLES.items():
        if title not in MANUAL_ANSWERS or title in seen_titles:
            continue
        para_source = None
        for key, value in title_map.items():
            if value == title:
                para_source = key
                break
        info = para_map.get(para_source or fname, {"count": None, "positions": {}})
        answers = MANUAL_ANSWERS[title]
        for idx, ans in enumerate(answers, start=36):
            if ans is None:
                continue
            records.append(
                {
                    "file": fname,
                    "title": title,
                    "question_number": idx,
                    "answer_letter": ans,
                    "paragraph_position_pct": info["positions"].get(ans),
                    "paragraph_count": info["count"],
                    "source_type": "ocr_manual",
                }
            )
    return pd.DataFrame(records)


def make_charts(df: pd.DataFrame):
    question_nums = list(range(36, 46))

    q_dist = (
        df.groupby(["question_number", "answer_letter"])
        .size()
        .unstack(fill_value=0)
        .reindex(index=question_nums, columns=sorted(df["answer_letter"].unique()), fill_value=0)
    )
    q_dist.to_csv(OUT / "question_answer_distribution.csv", encoding="utf-8-sig")

    plt.figure(figsize=(14, 8))
    q_dist.plot(kind="bar", stacked=True, figsize=(14, 8), colormap="tab20")
    plt.title("各题号对应答案字母分布")
    plt.xlabel("题号")
    plt.ylabel("次数")
    plt.tight_layout()
    plt.savefig(OUT / "question_answer_distribution.png", dpi=180)
    plt.close()

    q_summary_rows = []
    for q in question_nums:
        row = q_dist.loc[q]
        total = int(row.sum())
        sorted_row = row.sort_values(ascending=False)
        top_letter = sorted_row.index[0]
        second_letter = sorted_row.index[1]
        q_summary_rows.append(
            {
                "question_number": q,
                "top_letter": top_letter,
                "top_count": int(sorted_row.iloc[0]),
                "top_pct": round(float(sorted_row.iloc[0]) * 100 / total, 2),
                "second_letter": second_letter,
                "second_count": int(sorted_row.iloc[1]),
                "second_pct": round(float(sorted_row.iloc[1]) * 100 / total, 2),
                "top_gap_pct": round((float(sorted_row.iloc[0]) - float(sorted_row.iloc[1])) * 100 / total, 2),
                "answer_entropy": round(normalized_entropy(row.values), 4),
            }
        )
    pd.DataFrame(q_summary_rows).to_csv(OUT / "question_answer_summary.csv", index=False, encoding="utf-8-sig")

    pos_df = df[df["paragraph_position_pct"].notna()].copy()
    pos_df["position_band"] = pd.cut(
        pos_df["paragraph_position_pct"],
        bins=POSITION_BINS,
        labels=POSITION_BAND_LABELS,
        include_lowest=True,
        right=True,
    )

    pos_stats = (
        pos_df.groupby("question_number")["paragraph_position_pct"]
        .agg(
            min="min",
            q1=lambda s: s.quantile(0.25),
            median="median",
            q3=lambda s: s.quantile(0.75),
            iqr=lambda s: s.quantile(0.75) - s.quantile(0.25),
            variance="var",
            std="std",
            max="max",
            count="count",
        )
        .reset_index()
    )

    band_counts = (
        pos_df.groupby(["question_number", "position_band"], observed=False)
        .size()
        .unstack(fill_value=0)
        .reindex(index=question_nums, columns=POSITION_BAND_LABELS, fill_value=0)
    )
    band_counts.to_csv(OUT / "question_position_band_counts.csv", encoding="utf-8-sig")

    band_pct = band_counts.div(band_counts.sum(axis=1), axis=0).fillna(0)
    band_pct.to_csv(OUT / "question_position_band_distribution.csv", encoding="utf-8-sig")

    band_peaks = []
    for q in question_nums:
        sorted_row = band_counts.loc[q].sort_values(ascending=False)
        dominant_band = sorted_row.index[0]
        secondary_band = sorted_row.index[1]
        row_counts = band_counts.loc[q]
        band_peaks.append(
            {
                "question_number": q,
                "dominant_band": dominant_band,
                "dominant_band_count": int(sorted_row.iloc[0]),
                "dominant_band_pct": round(float(band_pct.loc[q, dominant_band]) * 100, 2),
                "secondary_band": secondary_band,
                "secondary_band_count": int(sorted_row.iloc[1]),
                "secondary_band_pct": round(float(band_pct.loc[q, secondary_band]) * 100, 2),
                "dominant_gap_pct": round((float(sorted_row.iloc[0]) - float(sorted_row.iloc[1])) * 100 / float(row_counts.sum()), 2),
                "band_entropy_20": round(normalized_entropy(row_counts.values), 4),
            }
        )

    pos_stats = pos_stats.merge(pd.DataFrame(band_peaks), on="question_number", how="left")

    boxplot_data = [
        pos_df.loc[pos_df["question_number"] == q, "paragraph_position_pct"].tolist()
        for q in question_nums
    ]
    fig, ax = plt.subplots(figsize=(12, 6))
    box = ax.boxplot(boxplot_data, patch_artist=True, tick_labels=question_nums)
    for patch in box["boxes"]:
        patch.set(facecolor="#d8e8f3", edgecolor="#2f5d62", linewidth=1.2)
    for median in box["medians"]:
        median.set(color="#c84b31", linewidth=2.0)
    for whisker in box["whiskers"]:
        whisker.set(color="#2f5d62", linewidth=1.0)
    for cap in box["caps"]:
        cap.set(color="#2f5d62", linewidth=1.0)
    for flier in box["fliers"]:
        flier.set(marker="o", markersize=4, markerfacecolor="#4f8a8b", markeredgecolor="#4f8a8b", alpha=0.7)
    ax.set_ylim(0, 100)
    ax.set_xlabel("题号")
    ax.set_ylabel("段落位置百分位")
    ax.set_title("各题号对应段落位置分布（中位数 / 四分位距）")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUT / "question_position_curve.png", dpi=180)
    fig.savefig(OUT / "question_position_boxplot.png", dpi=180)
    plt.close(fig)

    band_colors = ["#f4d35e", "#ee964b", "#f95738", "#0d3b66", "#4f6d7a"]
    ax = (band_pct * 100).plot(
        kind="bar",
        stacked=True,
        figsize=(12, 6),
        color=band_colors,
        width=0.75,
    )
    ax.set_xlabel("题号")
    ax.set_ylabel("命中占比（%）")
    ax.set_title("各题号对应段落位置分段分布")
    ax.legend(title="位置分段", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.set_ylim(0, 100)
    plt.tight_layout()
    plt.savefig(OUT / "question_position_band_distribution.png", dpi=180)
    plt.close()

    pos_df["heatmap_band"] = pd.cut(
        pos_df["paragraph_position_pct"],
        bins=HEATMAP_BINS,
        labels=HEATMAP_BAND_LABELS,
        include_lowest=True,
        right=True,
    )
    heatmap_pct = (
        pos_df.groupby(["question_number", "heatmap_band"], observed=False)
        .size()
        .unstack(fill_value=0)
        .reindex(index=question_nums, columns=HEATMAP_BAND_LABELS, fill_value=0)
    )
    heatmap_pct = heatmap_pct.div(heatmap_pct.sum(axis=1), axis=0).fillna(0)
    heatmap_pct.to_csv(OUT / "question_position_heatmap_distribution.csv", encoding="utf-8-sig")

    fine_rows = []
    heatmap_counts = (
        pos_df.groupby(["question_number", "heatmap_band"], observed=False)
        .size()
        .unstack(fill_value=0)
        .reindex(index=question_nums, columns=HEATMAP_BAND_LABELS, fill_value=0)
    )
    for q in question_nums:
        row = heatmap_counts.loc[q]
        sorted_row = row.sort_values(ascending=False)
        dominant_10 = sorted_row.index[0]
        secondary_10 = sorted_row.index[1]
        fine_rows.append(
            {
                "question_number": q,
                "dominant_10_band": dominant_10,
                "dominant_10_band_pct": round(float(heatmap_pct.loc[q, dominant_10]) * 100, 2),
                "secondary_10_band": secondary_10,
                "secondary_10_band_pct": round(float(heatmap_pct.loc[q, secondary_10]) * 100, 2),
                "dominant_gap_10_pct": round((float(sorted_row.iloc[0]) - float(sorted_row.iloc[1])) * 100 / float(row.sum()), 2),
                "band_entropy_10": round(normalized_entropy(row.values), 4),
            }
        )
    fine_stats = pd.DataFrame(fine_rows)
    fine_stats.to_csv(OUT / "question_position_fine_stats.csv", index=False, encoding="utf-8-sig")

    pos_stats = pos_stats.merge(fine_stats, on="question_number", how="left")
    pos_stats.to_csv(OUT / "question_position_stats.csv", index=False, encoding="utf-8-sig")

    fig, ax = plt.subplots(figsize=(10, 5))
    heatmap_values = (heatmap_pct * 100).T.values
    image = ax.imshow(heatmap_values, aspect="auto", cmap="YlGnBu", vmin=0, vmax=max(25, heatmap_values.max()))
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("命中占比（%）")
    ax.set_xticks(range(len(question_nums)))
    ax.set_xticklabels(question_nums)
    ax.set_yticks(range(len(HEATMAP_BAND_LABELS)))
    ax.set_yticklabels(HEATMAP_BAND_LABELS)
    ax.set_xlabel("题号")
    ax.set_ylabel("位置分段")
    ax.set_title("各题号最常落入的 10% 位置区间")
    text_threshold = max(12, heatmap_values.max() * 0.55)
    for y in range(len(HEATMAP_BAND_LABELS)):
        for x in range(len(question_nums)):
            value = heatmap_values[y, x]
            if value > 0:
                text_color = "white" if value >= text_threshold else "black"
                ax.text(x, y, f"{value:.0f}%", ha="center", va="center", color=text_color, fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "question_position_band_heatmap.png", dpi=180)
    plt.close(fig)

    letter_q = (
        df.groupby(["answer_letter", "question_number"])
        .size()
        .unstack(fill_value=0)
        .reindex(index=sorted(df["answer_letter"].unique()), columns=question_nums, fill_value=0)
    )
    letter_q.to_csv(OUT / "letter_to_question_distribution.csv", encoding="utf-8-sig")

    letter_summary_rows = []
    for letter in letter_q.index:
        row = letter_q.loc[letter]
        total = int(row.sum())
        sorted_row = row.sort_values(ascending=False)
        top_q = int(sorted_row.index[0])
        second_q = int(sorted_row.index[1])
        letter_summary_rows.append(
            {
                "answer_letter": letter,
                "top_question": top_q,
                "top_count": int(sorted_row.iloc[0]),
                "top_pct": round(float(sorted_row.iloc[0]) * 100 / total, 2),
                "second_question": second_q,
                "second_count": int(sorted_row.iloc[1]),
                "second_pct": round(float(sorted_row.iloc[1]) * 100 / total, 2),
                "top_gap_pct": round((float(sorted_row.iloc[0]) - float(sorted_row.iloc[1])) * 100 / total, 2),
                "reverse_entropy": round(normalized_entropy(row.values), 4),
            }
        )
    pd.DataFrame(letter_summary_rows).to_csv(OUT / "letter_to_question_summary.csv", index=False, encoding="utf-8-sig")

    plt.figure(figsize=(12, 8))
    plt.imshow(letter_q.values, aspect="auto", cmap="YlOrRd")
    plt.colorbar(label="次数")
    plt.xticks(range(len(question_nums)), question_nums)
    plt.yticks(range(len(letter_q.index)), letter_q.index)
    plt.xlabel("题号")
    plt.ylabel("答案字母")
    plt.title("各答案字母更常对应哪些题号")
    plt.tight_layout()
    plt.savefig(OUT / "letter_to_question_heatmap.png", dpi=180)
    plt.close()


def main():
    df = build_records()
    df.to_csv(OUT / "manual_truth_records.csv", index=False, encoding="utf-8-sig")
    make_charts(df)

    summary = {
        "files_count": int(df["file"].nunique()),
        "records_count": int(len(df)),
        "titles_count": int(df["title"].nunique()),
        "source_type_counts": {k: int(v) for k, v in Counter(df["source_type"]).items()},
    }
    (OUT / "manual_truth_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
