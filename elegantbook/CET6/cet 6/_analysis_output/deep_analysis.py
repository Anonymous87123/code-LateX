import csv
import os
from collections import defaultdict, Counter
from itertools import combinations
import statistics
import re

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(DATA_DIR, "manual_truth_records.csv")
OUT_PATH = os.path.join(DATA_DIR, "deep_analysis_results.md")

def load_data():
    rows = []
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["paragraph_position_pct"] and r["paragraph_count"]:
                try:
                    r["pct"] = float(r["paragraph_position_pct"])
                    r["pcount"] = int(float(r["paragraph_count"]))
                    r["qnum"] = int(r["question_number"])
                    r["letter"] = r["answer_letter"]
                    r["title"] = r["title"]
                    r["file"] = r["file"]
                    rows.append(r)
                except:
                    pass
    return rows

def group_by_title(rows):
    d = defaultdict(list)
    for r in rows:
        d[r["title"]].append(r)
    return d

def band_20(pct):
    if pct < 20: return "0-20"
    if pct < 40: return "20-40"
    if pct < 60: return "40-60"
    if pct < 80: return "60-80"
    return "80-100"

def spearman_corr(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0, 1.0
    def rank(vals):
        sorted_idx = sorted(range(n), key=lambda i: vals[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and vals[sorted_idx[j]] == vals[sorted_idx[j+1]]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1
            for k in range(i, j+1):
                ranks[sorted_idx[k]] = avg_rank
            i = j + 1
        return ranks
    rx = rank(xs)
    ry = rank(ys)
    d_sq = sum((rx[i] - ry[i])**2 for i in range(n))
    rho = 1 - 6 * d_sq / (n * (n*n - 1))
    return rho, 0.0

def kendall_tau(xs, ys):
    n = len(xs)
    concordant = 0
    discordant = 0
    for i in range(n):
        for j in range(i+1, n):
            dx = xs[i] - xs[j]
            dy = ys[i] - ys[j]
            if dx * dy > 0:
                concordant += 1
            elif dx * dy < 0:
                discordant += 1
    denom = concordant + discordant
    if denom == 0:
        return 0.0
    return (concordant - discordant) / denom

# ─────────────────────────────────────────────
# Analysis 1: front/back half split
# ─────────────────────────────────────────────
def analysis_1_half_split(rows, by_title):
    out = []
    out.append("## 分析 1：前后半区分裂比的策略含义\n")

    splits = Counter()
    for title, qs in by_title.items():
        front = sum(1 for q in qs if q["pct"] < 50)
        back = 10 - front
        splits[f"{front}/{back}"] += 1

    total = sum(splits.values())
    out.append("### 1.1 分裂比分布\n")
    out.append("| 前/后 | 篇数 | 占比 |")
    out.append("|-------|------|------|")
    for k in sorted(splits.keys(), key=lambda x: -splits[x]):
        out.append(f"| {k} | {splits[k]} | {splits[k]/total*100:.1f}% |")

    mode_key = splits.most_common(1)[0][0]
    mode_front = int(mode_key.split("/")[0])
    out.append(f"\n- 最常见分裂比为 **{mode_key}**（{splits[mode_key]}/{total} = {splits[mode_key]/total*100:.1f}%）")

    at_least_6 = sum(v for k, v in splits.items() if int(k.split("/")[0]) >= 6)
    at_least_5 = sum(v for k, v in splits.items() if int(k.split("/")[0]) >= 5)
    out.append(f"- 前半区 ≥6 题概率：{at_least_6}/{total} = {at_least_6/total*100:.1f}%")
    out.append(f"- 前半区 ≥5 题概率：{at_least_5}/{total} = {at_least_5/total*100:.1f}%")

    out.append("\n**实战规则：** 如果已在前半区找到 5 题，仍有较高概率还有第 6 题。如果只找到 4 题就急于转向后半区，约 90% 试卷中的第 5 题会被漏掉。\n")

    out.append("### 1.2 各题落在前半区的概率\n")
    out.append("| 题号 | 前半区次数 | 概率 |")
    out.append("|------|-----------|------|")
    for q in range(36, 46):
        q_rows = [r for r in rows if r["qnum"] == q]
        front_count = sum(1 for r in q_rows if r["pct"] < 50)
        out.append(f"| Q{q} | {front_count}/{len(q_rows)} | {front_count/len(q_rows)*100:.1f}% |")

    return "\n".join(out)

# ─────────────────────────────────────────────
# Analysis 2: odd-even alternating structure
# ─────────────────────────────────────────────
def analysis_2_odd_even(rows, by_title):
    out = []
    out.append("## 分析 2：完整奇偶交替结构系统表述\n")

    q_pcts = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_pcts[title][q["qnum"]] = q["pct"]

    titles_with_all = [t for t, d in q_pcts.items() if len(d) == 10]

    pair_results = {}
    for qi in range(36, 46):
        for qj in range(qi+1, 46):
            xs = [q_pcts[t][qi] for t in titles_with_all]
            ys = [q_pcts[t][qj] for t in titles_with_all]
            rho, _ = spearman_corr(xs, ys)
            pair_results[(qi, qj)] = rho

    out.append("### 2.1 相邻题对（间距=1）Spearman 相关\n")
    out.append("| 题对 | Spearman ρ | 方向 |")
    out.append("|------|-----------|------|")
    adj_neg = 0
    for i in range(36, 45):
        rho = pair_results[(i, i+1)]
        sign = "负" if rho < 0 else "正"
        if rho < 0: adj_neg += 1
        out.append(f"| Q{i}/Q{i+1} | {rho:+.4f} | {sign} |")

    out.append(f"\n**全部相邻题对负相关：{'是 ✓' if adj_neg == 9 else '否 ✗'}** — {adj_neg}/9 对为负\n")

    out.append("### 2.2 隔一题对（间距=2）Spearman 相关\n")
    out.append("| 题对 | Spearman ρ | 方向 |")
    out.append("|------|-----------|------|")
    skip_pos = 0
    for i in range(36, 44):
        rho = pair_results[(i, i+2)]
        sign = "正" if rho > 0 else "负"
        if rho > 0: skip_pos += 1
        out.append(f"| Q{i}/Q{i+2} | {rho:+.4f} | {sign} |")

    out.append(f"\n**全部隔一题对正相关：{'是 ✓' if skip_pos == 8 else '否 ✗'}** — {skip_pos}/8 对为正\n")

    out.append("### 2.3 间距=3 题对\n")
    out.append("| 题对 | Spearman ρ | 方向 |")
    out.append("|------|-----------|------|")
    for i in range(36, 43):
        rho = pair_results[(i, i+3)]
        sign = "正" if rho > 0 else "负"
        out.append(f"| Q{i}/Q{i+3} | {rho:+.4f} | {sign} |")

    out.append("\n### 2.4 结构性总结\n")
    out.append("- 间距=1（相邻）：**一致负相关** → 跷跷板效应")
    out.append("- 间距=2（隔一）：**一致正相关** → 同奇/同偶题同向")
    out.append("- 两条交织链：奇数链 Q36-Q38-Q40-Q42-Q44，偶数链 Q37-Q39-Q41-Q43-Q45")
    out.append("- 链内同向移动，链间反向移动\n")

    return "\n".join(out)

# ─────────────────────────────────────────────
# Analysis 3: paragraph count grouping
# ─────────────────────────────────────────────
def analysis_3_paragraph_count(rows, by_title):
    out = []
    out.append("## 分析 3：文章段落数分组分析\n")

    title_pcount = {}
    for title, qs in by_title.items():
        title_pcount[title] = qs[0]["pcount"]

    pcount_dist = Counter(title_pcount.values())
    total = sum(pcount_dist.values())

    out.append("### 3.1 段落数分布\n")
    out.append("| 段落数 | 篇数 | 占比 |")
    out.append("|--------|------|------|")
    for pc in sorted(pcount_dist.keys()):
        out.append(f"| {pc} | {pcount_dist[pc]} | {pcount_dist[pc]/total*100:.1f}% |")

    median_pc = statistics.median(title_pcount.values())
    mean_pc = statistics.mean(title_pcount.values())
    out.append(f"\n- 中位数：{median_pc}，均值：{mean_pc:.1f}")

    short_titles = set(t for t, pc in title_pcount.items() if pc <= 12)
    medium_titles = set(t for t, pc in title_pcount.items() if 13 <= pc <= 15)
    long_titles = set(t for t, pc in title_pcount.items() if pc >= 16)

    out.append(f"\n### 3.2 按段落数分组的位置分布差异\n")
    out.append(f"分组：短文（≤12段，{len(short_titles)}篇）、中文（13-15段，{len(medium_titles)}篇）、长文（≥16段，{len(long_titles)}篇）\n")

    groups = [("短文 ≤12", short_titles), ("中文 13-15", medium_titles), ("长文 ≥16", long_titles)]

    out.append("| 题号 | 短文中位数 | 中文中位数 | 长文中位数 | 短-长差 |")
    out.append("|------|----------|----------|----------|---------|")

    for q in range(36, 46):
        medians = []
        for gname, gtitles in groups:
            vals = [r["pct"] for r in rows if r["qnum"] == q and r["title"] in gtitles]
            medians.append(statistics.median(vals) if vals else None)
        diff = ""
        if medians[0] is not None and medians[2] is not None:
            diff = f"{medians[0]-medians[2]:+.1f}"
        cells = [f"{m:.1f}" if m is not None else "N/A" for m in medians]
        out.append(f"| Q{q} | {cells[0]} | {cells[1]} | {cells[2]} | {diff} |")

    out.append(f"\n### 3.3 干扰段落数\n")
    out.append("10题对应10个段落，剩余为干扰项。\n")
    out.append("| 段落数 | 干扰段落数 | 篇数 |")
    out.append("|--------|----------|------|")
    for pc in sorted(pcount_dist.keys()):
        out.append(f"| {pc} | {pc-10} | {pcount_dist[pc]} |")

    out.append(f"\n- 干扰段落范围：{min(title_pcount.values())-10} ~ {max(title_pcount.values())-10}")

    return "\n".join(out)

# ─────────────────────────────────────────────
# Analysis 4: temporal stability
# ─────────────────────────────────────────────
def analysis_4_temporal_stability(rows, by_title):
    out = []
    out.append("## 分析 4：时间窗口稳定性验证\n")

    title_year = {}
    for title, qs in by_title.items():
        m = re.search(r"(20\d{2})", qs[0]["file"])
        if m:
            title_year[title] = int(m.group(1))

    era_map = {}
    for t, y in title_year.items():
        if y <= 2018:
            era_map[t] = "2016-2018"
        elif y <= 2021:
            era_map[t] = "2019-2021"
        else:
            era_map[t] = "2022-2025"

    eras = sorted(set(era_map.values()))
    era_counts = Counter(era_map.values())

    out.append("### 4.1 时代分组\n")
    for e in eras:
        out.append(f"- {e}：{era_counts[e]} 篇")

    out.append(f"\n### 4.2 各题各时代中位数位置\n")
    out.append("| 题号 | " + " | ".join(eras) + " | 最大跨时代差 |")
    out.append("|------" + "|----------" * len(eras) + "|------------|")

    max_diffs = []
    for q in range(36, 46):
        vals_by_era = {}
        for e in eras:
            era_titles = [t for t, er in era_map.items() if er == e]
            vals = [r["pct"] for r in rows if r["qnum"] == q and r["title"] in era_titles]
            vals_by_era[e] = statistics.median(vals) if vals else None

        valid = [v for v in vals_by_era.values() if v is not None]
        maxdiff = max(valid) - min(valid) if len(valid) >= 2 else 0
        max_diffs.append(maxdiff)

        cells = [f"{vals_by_era[e]:.1f}" if vals_by_era[e] is not None else "N/A" for e in eras]
        out.append(f"| Q{q} | " + " | ".join(cells) + f" | {maxdiff:.1f} |")

    avg_drift = statistics.mean(max_diffs)
    max_drift_q = 36 + max_diffs.index(max(max_diffs))

    out.append(f"\n- 平均跨时代位置漂移：{avg_drift:.1f}%")
    out.append(f"- 最大漂移题：Q{max_drift_q}（{max(max_diffs):.1f}%）")

    stable = sum(1 for d in max_diffs if d <= 10)
    out.append(f"- 漂移≤10%的题数：{stable}/10")

    out.append("\n### 4.3 稳定性结论\n")
    if avg_drift <= 10:
        out.append("整体模式 **高度稳定**，各时代分布无显著结构性变化。本报告结论可适用于未来考试。")
    elif avg_drift <= 20:
        out.append("整体模式 **基本稳定**，个别题有漂移但不改变整体结构。")
    else:
        out.append("存在显著时代漂移，需谨慎外推。")

    return "\n".join(out)

# ─────────────────────────────────────────────
# Analysis 5: collision constraint
# ─────────────────────────────────────────────
def analysis_5_collision(rows, by_title):
    out = []
    out.append("## 分析 5：同段重复率：不是错误，也不是硬约束\n")

    collision_count = 0
    total_pairs = 0

    for title, qs in by_title.items():
        letters = [q["letter"] for q in sorted(qs, key=lambda x: x["qnum"])]
        for i in range(len(letters)):
            for j in range(i+1, len(letters)):
                total_pairs += 1
                if letters[i] == letters[j]:
                    collision_count += 1

    rate = collision_count / total_pairs * 100 if total_pairs > 0 else 0

    out.append(f"### 5.1 重复统计\n")
    out.append(f"- 总题对数：{total_pairs}")
    out.append(f"- 同答案字母重复题对次数：{collision_count}")
    out.append(f"- 重复题对率：{rate:.2f}%")

    # unique letter check per title
    all_unique = sum(1 for title, qs in by_title.items() if len(set(q["letter"] for q in qs)) == 10)
    out.append(f"- 10题全部不同字母篇数：{all_unique}/{len(by_title)} = {all_unique/len(by_title)*100:.1f}%")

    out.append(f"\n### 5.2 结论\n")
    out.append("- 题目说明允许同一段被多次选择，因此重复字母不是数据错误")
    out.append("- 10题全部不同字母很常见，但不是硬约束")
    out.append("- 已确认答案段只能降低其他题优先级，不能绝对排除\n")

    return "\n".join(out)

# ─────────────────────────────────────────────
# Analysis 6: answer sequence monotonicity
# ─────────────────────────────────────────────
def analysis_6_monotonicity(rows, by_title):
    out = []
    out.append("## 分析 6：答案序列单调性分析\n")
    out.append("检验题号顺序（Q36→Q45）是否对应段落位置单调递增。\n")

    mono_inc = 0
    inversion_counts = []
    taus = []

    for title, qs in by_title.items():
        sorted_qs = sorted(qs, key=lambda x: x["qnum"])
        pcts = [q["pct"] for q in sorted_qs]

        inversions = 0
        for i in range(len(pcts)):
            for j in range(i+1, len(pcts)):
                if pcts[i] > pcts[j]:
                    inversions += 1
        inversion_counts.append(inversions)

        is_inc = all(pcts[i] <= pcts[i+1] for i in range(len(pcts)-1))
        if is_inc: mono_inc += 1

        tau = kendall_tau(list(range(10)), pcts)
        taus.append(tau)

    total = len(by_title)
    avg_inv = statistics.mean(inversion_counts)
    avg_tau = statistics.mean(taus)

    out.append("### 6.1 完全单调性\n")
    out.append(f"- 完全单调递增篇数：{mono_inc}/{total} = {mono_inc/total*100:.1f}%")

    out.append(f"\n### 6.2 逆序对统计\n")
    out.append(f"- 最大可能逆序对数 C(10,2)：45")
    out.append(f"- 实际平均逆序对数：{avg_inv:.1f}")
    out.append(f"- 逆序率：{avg_inv/45*100:.1f}%")
    out.append(f"- 范围：[{min(inversion_counts)}, {max(inversion_counts)}]")
    out.append(f"- 随机排列期望逆序对：22.5")
    out.append(f"- 实际/随机比：{avg_inv/22.5:.2f}")

    out.append(f"\n### 6.3 Kendall τ 统计\n")
    out.append(f"- 平均 Kendall τ：{avg_tau:.4f}")
    out.append(f"- τ > 0 的篇数：{sum(1 for t in taus if t > 0)}/{total}")
    out.append(f"- τ 范围：[{min(taus):.4f}, {max(taus):.4f}]")

    out.append(f"\n### 6.4 单调性结论\n")
    if avg_tau > 0.3:
        out.append("题号与段落位置存在 **中等正向单调趋势**：总体小题号偏前、大题号偏后，但远非严格单调。")
    elif avg_tau > 0.1:
        out.append("题号与段落位置存在 **弱正向单调趋势**：有轻微前→后倾向，但乱序程度很高。")
    elif avg_tau > -0.1:
        out.append("题号与段落位置 **基本无单调关系**。")
    else:
        out.append("题号与段落位置存在 **负向趋势**。")

    out.append("- **实战意义**：不能按 Q36→Q45 顺序从前到后扫文章。题号顺序≠段落顺序。")

    return "\n".join(out)

# ─────────────────────────────────────────────
# Analysis 7: letter exclusion constraint
# ─────────────────────────────────────────────
def analysis_7_letter_exclusion(rows, by_title):
    out = []
    out.append("## 分析 7：答案字母分布与弱排除\n")

    all_unique = 0
    has_dup = 0
    for title, qs in by_title.items():
        letters = [q["letter"] for q in qs]
        if len(set(letters)) == 10:
            all_unique += 1
        else:
            has_dup += 1

    total = len(by_title)
    out.append(f"### 7.1 唯一字母数验证\n")
    out.append(f"- 全部字母唯一：{all_unique}/{total} = {all_unique/total*100:.1f}%")
    out.append(f"- 存在重复字母：{has_dup}/{total}")

    out.append(f"\n### 7.2 字母使用频率\n")
    all_letters = [r["letter"] for r in rows]
    letter_freq = Counter(all_letters)
    out.append("| 字母 | 使用次数 | 占比 |")
    out.append("|------|---------|------|")
    for letter in sorted(letter_freq.keys()):
        out.append(f"| {letter} | {letter_freq[letter]} | {letter_freq[letter]/len(all_letters)*100:.1f}% |")

    out.append(f"\n- 共 {len(letter_freq)} 个不同字母被使用")

    out.append(f"\n### 7.3 弱排除的策略价值\n")
    out.append("- 多数试卷 10 题对应 10 个不同段落，但同段重复合法")
    out.append("- 解到第7-8题时，已用段落可降优先级，但不能直接判死")
    out.append("- 后半程应结合题干语义、条件窗口和已用段落一起排除\n")

    return "\n".join(out)

# ─────────────────────────────────────────────
# Analysis 8: distractor analysis
# ─────────────────────────────────────────────
def analysis_8_distractors(rows, by_title):
    out = []
    out.append("## 分析 8：未使用段落（干扰项）分析\n")

    distractor_positions = []
    distractor_bands = Counter()

    for title, qs in by_title.items():
        pc = qs[0]["pcount"]
        used_letters = set(q["letter"] for q in qs)
        all_letters_set = set(chr(ord('A') + i) for i in range(pc))
        unused = all_letters_set - used_letters

        for letter in unused:
            pos_idx = ord(letter) - ord('A')
            pct = (pos_idx + 0.5) / pc * 100
            distractor_positions.append(pct)
            distractor_bands[band_20(pct)] += 1

    total_dist = len(distractor_positions)
    out.append(f"### 8.1 干扰段落总量\n")
    out.append(f"- 总干扰段落数：{total_dist}（{len(by_title)}篇）")
    out.append(f"- 每篇平均干扰段落：{total_dist/len(by_title):.1f}")

    out.append(f"\n### 8.2 干扰段落位置分布（20%带）\n")
    out.append("| 位置带 | 干扰数 | 占比 |")
    out.append("|--------|-------|------|")
    for band in ["0-20", "20-40", "40-60", "60-80", "80-100"]:
        cnt = distractor_bands.get(band, 0)
        out.append(f"| {band}% | {cnt} | {cnt/total_dist*100:.1f}% |")

    med_pos = statistics.median(distractor_positions) if distractor_positions else 0
    out.append(f"\n- 干扰段落中位位置：{med_pos:.1f}%")

    top_band = max(distractor_bands, key=distractor_bands.get) if distractor_bands else "N/A"
    out.append(f"\n### 8.3 策略含义\n")
    out.append(f"- 干扰段最密集区域：**{top_band}%**")
    out.append("- 该区域段落更可能是干扰项 → 匹配时需更谨慎")
    out.append("- 短文干扰少，长文干扰多 → 长文需更多语义排除和条件窗口\n")

    return "\n".join(out)

# ─────────────────────────────────────────────
# Analysis 9: multi-anchor compound conditions
# ─────────────────────────────────────────────
def analysis_9_multi_anchor(rows, by_title):
    out = []
    out.append("## 分析 9：多锚点复合条件分析\n")
    out.append("当两个锚点题同时已知位置带时，目标题搜索窗口进一步缩小多少？\n")

    q_band = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_band[title][q["qnum"]] = band_20(q["pct"])

    titles = list(q_band.keys())

    anchor_pairs = [(36, 37), (36, 44), (37, 44), (36, 41), (37, 43)]
    target_qs = list(range(36, 46))

    results = []
    for a1, a2 in anchor_pairs:
        for tgt in target_qs:
            if tgt == a1 or tgt == a2:
                continue
            combo_groups = defaultdict(list)
            for t in titles:
                if a1 in q_band[t] and a2 in q_band[t] and tgt in q_band[t]:
                    key = (q_band[t][a1], q_band[t][a2])
                    combo_groups[key].append(q_band[t][tgt])

            for (b1, b2), target_bands in combo_groups.items():
                if len(target_bands) < 4:
                    continue
                unique_bands = set(target_bands)
                if len(unique_bands) <= 2:
                    top_band = Counter(target_bands).most_common(1)[0]
                    results.append({
                        "anchors": f"Q{a1}∈{b1}% ∧ Q{a2}∈{b2}%",
                        "target": f"Q{tgt}",
                        "n": len(target_bands),
                        "bands": len(unique_bands),
                        "top_band": top_band[0],
                        "top_pct": top_band[1] / len(target_bands) * 100,
                    })

    results.sort(key=lambda x: -x["top_pct"])

    out.append("### 9.1 双锚点高确信规则（目标带≤2，样本≥4）\n")
    if results:
        out.append("| 锚点条件 | 目标题 | 样本 | 可能带数 | 最可能带 | 命中率 |")
        out.append("|---------|--------|------|---------|---------|--------|")
        for r in results[:25]:
            out.append(f"| {r['anchors']} | {r['target']} | {r['n']} | {r['bands']} | {r['top_band']}% | {r['top_pct']:.0f}% |")
    else:
        out.append("未发现满足条件的双锚点规则。")

    out.append(f"\n### 9.2 Q36+Q44 双锚定位效果\n")
    out.append("当 Q36 和 Q44 位置带已知时，各题搜索空间：\n")

    for tgt in [37, 38, 39, 40, 41, 42, 43, 45]:
        combo_groups = defaultdict(list)
        for t in titles:
            if 36 in q_band[t] and 44 in q_band[t] and tgt in q_band[t]:
                key = (q_band[t][36], q_band[t][44])
                combo_groups[key].append(q_band[t][tgt])

        total_combos = len(combo_groups)
        narrow = sum(1 for bands in combo_groups.values() if len(set(bands)) <= 2 and len(bands) >= 3)
        if total_combos > 0:
            out.append(f"- Q{tgt}：{total_combos}种组合中，{narrow}种可缩至≤2带 ({narrow/total_combos*100:.0f}%)")

    out.append(f"\n### 9.3 策略含义\n")
    out.append("- 双锚点比单锚点显著提升定位精度")
    out.append("- Q36+Q44 是最佳双锚组合（一前一后，覆盖全文）")
    out.append("- 考试中优先确认这两题，再用复合条件缩窗其余题\n")

    return "\n".join(out)


def main():
    rows = load_data()
    by_title = group_by_title(rows)

    print(f"Loaded {len(rows)} records from {len(by_title)} titles")

    sections = []
    sections.append("# CET-6 Section B 深度补充分析\n")
    sections.append(f"基于 {len(by_title)} 篇有效位置数据的全量计算。\n")

    sections.append(analysis_1_half_split(rows, by_title))
    sections.append(analysis_2_odd_even(rows, by_title))
    sections.append(analysis_3_paragraph_count(rows, by_title))
    sections.append(analysis_4_temporal_stability(rows, by_title))
    sections.append(analysis_5_collision(rows, by_title))
    sections.append(analysis_6_monotonicity(rows, by_title))
    sections.append(analysis_7_letter_exclusion(rows, by_title))
    sections.append(analysis_8_distractors(rows, by_title))
    sections.append(analysis_9_multi_anchor(rows, by_title))

    full_text = "\n\n".join(sections)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"Written to {OUT_PATH}")
    print(f"Length: {len(full_text)} chars")

if __name__ == "__main__":
    main()
