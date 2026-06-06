import csv
import os
from collections import defaultdict, Counter
import statistics
import math
from itertools import combinations

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(DATA_DIR, "manual_truth_records.csv")
OUT_PATH = os.path.join(DATA_DIR, "deep_analysis_round2.md")

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

# ─────────────────────────────────────────────
# 1. 标准化段落位置偏好
# ─────────────────────────────────────────────
def analysis_normalized_letter_preference(rows, by_title):
    out = []
    out.append("## 1. 标准化段落位置偏好\n")
    out.append("P/Q/R 少是因为多数文章不到 16 段 — 不是偏好信号。")
    out.append("标准化：将每个段落转化为相对位置（第 k/N），分 10% 桶统计选中率 vs 期望率。\n")

    bin_labels = [f"{b}-{b+10}%" for b in range(0, 100, 10)]
    bin_selected = defaultdict(int)
    bin_total = defaultdict(int)

    for title, qs in by_title.items():
        pc = qs[0]["pcount"]
        used_letters = set(q["letter"] for q in qs)
        for i in range(pc):
            letter = chr(ord('A') + i)
            pos_pct = (i + 0.5) / pc * 100
            bin_idx = min(int(pos_pct / 10), 9)
            bin_key = bin_labels[bin_idx]
            bin_total[bin_key] += 1
            if letter in used_letters:
                bin_selected[bin_key] += 1

    total_p = sum(bin_total.values())
    total_s = sum(bin_selected.values())
    overall_rate = total_s / total_p

    out.append("| 位置桶 | 可选段落 | 被选中 | 选中率 | 期望率 | 偏差 |")
    out.append("|--------|---------|--------|--------|--------|------|")

    rates = {}
    for label in bin_labels:
        t = bin_total.get(label, 0)
        s = bin_selected.get(label, 0)
        if t > 0:
            actual = s / t * 100
            expected = overall_rate * 100
            deviation = actual - expected
            rates[label] = actual
            out.append(f"| {label} | {t} | {s} | {actual:.1f}% | {expected:.1f}% | {deviation:+.1f}% |")

    max_bin = max(rates, key=rates.get)
    min_bin = min(rates, key=rates.get)
    out.append(f"\n- 总体选中率：{total_s}/{total_p} = {overall_rate*100:.1f}%")
    out.append(f"- 最高选中率：**{max_bin}**（{rates[max_bin]:.1f}%）")
    out.append(f"- 最低选中率：**{min_bin}**（{rates[min_bin]:.1f}%）")
    out.append(f"- 极差：{rates[max_bin]-rates[min_bin]:.1f}%")

    return "\n".join(out)

# ─────────────────────────────────────────────
# 2. 题号的段落排序
# ─────────────────────────────────────────────
def analysis_rank_order(rows, by_title):
    out = []
    out.append("## 2. 题号的段落排序（答案在10个答案中排第几）\n")
    out.append("用相对排序消除段落数差异。\n")

    rank_by_q = defaultdict(list)
    for title, qs in by_title.items():
        sorted_by_pos = sorted(qs, key=lambda x: x["pct"])
        for rank_idx, q in enumerate(sorted_by_pos):
            rank_by_q[q["qnum"]].append(rank_idx + 1)

    out.append("| 题号 | 中位排名 | 均值 | σ | 排第1 | 排第10 |")
    out.append("|------|---------|------|---|------|--------|")

    for q in range(36, 46):
        ranks = rank_by_q[q]
        med = statistics.median(ranks)
        avg = statistics.mean(ranks)
        sd = statistics.stdev(ranks) if len(ranks) > 1 else 0
        first = ranks.count(1)
        last = ranks.count(10)
        out.append(f"| Q{q} | {med:.1f} | {avg:.1f} | {sd:.1f} | {first} | {last} |")

    sds = {q: statistics.stdev(rank_by_q[q]) for q in range(36, 46)}
    most_stable = min(sds, key=sds.get)
    most_volatile = max(sds, key=sds.get)
    out.append(f"\n- 排名最稳定：Q{most_stable}（σ={sds[most_stable]:.1f}）")
    out.append(f"- 排名最不稳定：Q{most_volatile}（σ={sds[most_volatile]:.1f}）")

    out.append(f"\n### 2.2 相邻题排名差\n")
    out.append("| 题对 | 平均排名差 | 排名差=1占比 | 排名差≤2占比 |")
    out.append("|------|----------|------------|-------------|")

    for qi in range(36, 45):
        diffs = []
        close1 = 0
        close2 = 0
        for title, qs in by_title.items():
            sorted_by_pos = sorted(qs, key=lambda x: x["pct"])
            rank_map = {q["qnum"]: idx+1 for idx, q in enumerate(sorted_by_pos)}
            d = abs(rank_map[qi] - rank_map[qi+1])
            diffs.append(d)
            if d == 1: close1 += 1
            if d <= 2: close2 += 1
        avg_d = statistics.mean(diffs)
        out.append(f"| Q{qi}/Q{qi+1} | {avg_d:.1f} | {close1}/{len(diffs)} ({close1/len(diffs)*100:.0f}%) | {close2}/{len(diffs)} ({close2/len(diffs)*100:.0f}%) |")

    return "\n".join(out)

# ─────────────────────────────────────────────
# 3. 标准化位置重标定
# ─────────────────────────────────────────────
def analysis_position_normalized(rows, by_title):
    out = []
    out.append("## 3. 段落数条件下的位置重标定\n")
    out.append("用 letter_index/(pcount-1) 替代 paragraph_position_pct。\n")

    q_normed = defaultdict(list)
    for r in rows:
        idx = ord(r["letter"]) - ord('A')
        normed = idx / (r["pcount"] - 1) if r["pcount"] > 1 else 0.5
        q_normed[r["qnum"]].append(normed * 100)

    out.append("| 题号 | 标准化中位 | 标准化均值 | σ | 原始中位 | 差值 |")
    out.append("|------|----------|----------|---|---------|------|")

    for q in range(36, 46):
        nv = q_normed[q]
        rv = [r["pct"] for r in rows if r["qnum"] == q]
        n_med = statistics.median(nv)
        n_avg = statistics.mean(nv)
        n_sd = statistics.stdev(nv) if len(nv) > 1 else 0
        r_med = statistics.median(rv)
        diff = n_med - r_med
        out.append(f"| Q{q} | {n_med:.1f}% | {n_avg:.1f}% | {n_sd:.1f} | {r_med:.1f}% | {diff:+.1f} |")

    return "\n".join(out)

# ─────────────────────────────────────────────
# 4. 连续段落覆盖与间隔分析
# ─────────────────────────────────────────────
def analysis_consecutive_coverage(rows, by_title):
    out = []
    out.append("## 4. 连续段落覆盖与间隔分析\n")

    gap_all = []
    max_gap_all = []
    max_consec_all = []
    coverage_span_all = []

    for title, qs in by_title.items():
        pc = qs[0]["pcount"]
        used_indices = sorted(ord(q["letter"]) - ord('A') for q in qs)
        gaps = [used_indices[i+1] - used_indices[i] - 1 for i in range(len(used_indices)-1)]
        gap_all.extend(gaps)
        max_gap_all.append(max(gaps) if gaps else 0)
        max_run = 1
        run = 1
        for i in range(1, len(used_indices)):
            if used_indices[i] == used_indices[i-1] + 1:
                run += 1
                max_run = max(max_run, run)
            else:
                run = 1
        max_consec_all.append(max_run)
        span = used_indices[-1] - used_indices[0] + 1
        coverage_span_all.append(span / pc * 100)

    out.append("### 4.1 答案间隔统计\n")
    out.append(f"- 平均相邻答案间隔：{statistics.mean(gap_all):.2f} 段")
    out.append(f"- 间隔=0（连续答案）占比：{gap_all.count(0)/len(gap_all)*100:.1f}%")

    gap_dist = Counter(gap_all)
    out.append(f"\n| 间隔(段) | 次数 | 占比 |")
    out.append("|---------|------|------|")
    for g in sorted(gap_dist.keys()):
        out.append(f"| {g} | {gap_dist[g]} | {gap_dist[g]/len(gap_all)*100:.1f}% |")

    out.append(f"\n### 4.2 最长连续答案段\n")
    consec_dist = Counter(max_consec_all)
    out.append(f"- 平均最长连续：{statistics.mean(max_consec_all):.1f}")
    out.append(f"| 最长连续 | 篇数 |")
    out.append("|---------|------|")
    for c in sorted(consec_dist.keys()):
        out.append(f"| {c} | {consec_dist[c]} |")

    out.append(f"\n### 4.3 覆盖跨度\n")
    out.append(f"- 平均覆盖：{statistics.mean(coverage_span_all):.1f}%")
    out.append(f"- 最小覆盖：{min(coverage_span_all):.1f}%")

    return "\n".join(out)

# ─────────────────────────────────────────────
# 5. 信息熵细分
# ─────────────────────────────────────────────
def analysis_positional_entropy(rows, by_title):
    out = []
    out.append("## 5. 各题段落位置信息熵\n")

    bands = ["0-20", "20-40", "40-60", "60-80", "80-100"]

    out.append("| 题号 | 0-20% | 20-40% | 40-60% | 60-80% | 80-100% | 熵 | 最集中带 |")
    out.append("|------|-------|--------|--------|--------|---------|-----|---------|")

    for q in range(36, 46):
        q_rows = [r for r in rows if r["qnum"] == q]
        band_counts = Counter(band_20(r["pct"]) for r in q_rows)
        total = len(q_rows)
        probs = []
        cells = []
        for b in bands:
            c = band_counts.get(b, 0)
            p = c / total if total > 0 else 0
            probs.append(p)
            cells.append(f"{c}({p*100:.0f}%)")
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        top_band = bands[probs.index(max(probs))]
        out.append(f"| Q{q} | " + " | ".join(cells) + f" | {entropy:.3f} | {top_band}% |")

    out.append(f"\n- 最大熵（均匀5带）= {math.log2(5):.3f}")

    return "\n".join(out)

# ─────────────────────────────────────────────
# 6. 排除法加速曲线
# ─────────────────────────────────────────────
def analysis_elimination_speed(rows, by_title):
    out = []
    out.append("## 6. 排除法加速曲线\n")

    pcounts = [qs[0]["pcount"] for qs in by_title.values()]
    avg_pc = statistics.mean(pcounts)

    out.append("| 已做对 | 平均候选段落 | 缩减比 |")
    out.append("|--------|-----------|--------|")

    for k in range(11):
        remaining = [max(pc - k, 1) for pc in pcounts]
        avg_r = statistics.mean(remaining)
        red = (1 - avg_r / avg_pc) * 100 if k > 0 else 0
        out.append(f"| {k} | {avg_r:.1f} | {red:.1f}% |")

    for k in range(11):
        if statistics.mean([max(pc - k, 1) for pc in pcounts]) < 5:
            out.append(f"\n- 做对 {k} 题 → 平均候选<5，弱排除更高效")
            break
    for k in range(11):
        if statistics.mean([max(pc - k, 1) for pc in pcounts]) < 3:
            out.append(f"- 做对 {k} 题 → 平均候选<3，但仍需用语义确认，不能只按已用字母定答案")
            break

    return "\n".join(out)

# ─────────────────────────────────────────────
# 7. 难度代理指标
# ─────────────────────────────────────────────
def analysis_difficulty_proxy(rows, by_title):
    out = []
    out.append("## 7. 题目难度代理指标\n")

    bands = ["0-20", "20-40", "40-60", "60-80", "80-100"]
    q_stats = {}

    for q in range(36, 46):
        q_rows = [r for r in rows if r["qnum"] == q]
        pcts = [r["pct"] for r in q_rows]
        sd = statistics.stdev(pcts)
        band_counts = Counter(band_20(p) for p in pcts)
        total = len(q_rows)
        probs = [band_counts.get(b, 0) / total for b in bands]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        dominant_band = band_counts.most_common(1)[0][0]

        dist_in_band = 0
        total_in_band = 0
        for title, qs in by_title.items():
            pc = qs[0]["pcount"]
            used = set(q2["letter"] for q2 in qs)
            for i in range(pc):
                pos = (i + 0.5) / pc * 100
                if band_20(pos) == dominant_band:
                    total_in_band += 1
                    if chr(ord('A') + i) not in used:
                        dist_in_band += 1
        dist_density = dist_in_band / total_in_band * 100 if total_in_band > 0 else 0
        difficulty = sd * 0.4 + entropy * 10 * 0.3 + dist_density * 0.3
        q_stats[q] = {"sd": sd, "entropy": entropy, "dist_density": dist_density, "difficulty": difficulty}

    sorted_qs = sorted(q_stats.items(), key=lambda x: -x[1]["difficulty"])
    rank_map = {q: i+1 for i, (q, _) in enumerate(sorted_qs)}

    out.append("| 题号 | 位置σ | 熵 | 主带干扰密度 | 综合难度 | 排名 |")
    out.append("|------|------|-----|-----------|---------|------|")
    for q in range(36, 46):
        s = q_stats[q]
        out.append(f"| Q{q} | {s['sd']:.1f} | {s['entropy']:.3f} | {s['dist_density']:.1f}% | {s['difficulty']:.1f} | {rank_map[q]} |")

    hardest = sorted_qs[0][0]
    easiest = sorted_qs[-1][0]
    out.append(f"\n- 最难：Q{hardest}  |  最易：Q{easiest}")

    return "\n".join(out)

# ─────────────────────────────────────────────
# 8. 密度热区
# ─────────────────────────────────────────────
def analysis_density_hotzone(rows, by_title):
    out = []
    out.append("## 8. 答案密度热区（每题最佳扫描窗口）\n")

    out.append("| 题号 | 最佳40%窗口 | 覆盖率 | 次佳40%窗口 | 覆盖率 |")
    out.append("|------|-----------|--------|-----------|--------|")

    for q in range(36, 46):
        pcts = [r["pct"] for r in rows if r["qnum"] == q]
        total = len(pcts)
        best_window = None
        best_count = 0
        second_window = None
        second_count = 0
        for start in range(0, 61):
            end = start + 40
            count = sum(1 for p in pcts if start <= p < end)
            if count > best_count:
                second_window = best_window
                second_count = best_count
                best_count = count
                best_window = f"{start}-{end}%"
            elif count > second_count:
                second_count = count
                second_window = f"{start}-{end}%"
        pct1 = best_count / total * 100
        pct2 = second_count / total * 100
        out.append(f"| Q{q} | {best_window} | {pct1:.1f}% | {second_window} | {pct2:.1f}% |")

    return "\n".join(out)

# ─────────────────────────────────────────────
# 9. 锚链效应（最佳三题组合）
# ─────────────────────────────────────────────
def analysis_anchor_chain(rows, by_title):
    out = []
    out.append("## 9. 锚链效应：最佳做题顺序链\n")

    q_bands = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_bands[title][q["qnum"]] = band_20(q["pct"])

    titles = list(q_bands.keys())
    all_qs = list(range(36, 46))
    best_combos = []

    for combo in combinations(all_qs, 3):
        a1, a2, a3 = combo
        remaining = [q for q in all_qs if q not in combo]
        total_entropy = 0
        for tgt in remaining:
            groups = defaultdict(list)
            for t in titles:
                if all(q in q_bands[t] for q in [a1, a2, a3, tgt]):
                    key = (q_bands[t][a1], q_bands[t][a2], q_bands[t][a3])
                    groups[key].append(q_bands[t][tgt])
            weighted_h = 0
            total_n = sum(len(v) for v in groups.values())
            for target_bands in groups.values():
                n = len(target_bands)
                if n < 2: continue
                bc = Counter(target_bands)
                probs = [c/n for c in bc.values()]
                h = -sum(p * math.log2(p) for p in probs if p > 0)
                weighted_h += h * n / total_n
            total_entropy += weighted_h
        best_combos.append((combo, total_entropy / len(remaining)))

    best_combos.sort(key=lambda x: x[1])

    out.append("### 9.1 最强三题锚组合（残余熵最低）\n")
    out.append("| 排名 | 锚点组合 | 残余熵 |")
    out.append("|------|---------|--------|")
    for i, (combo, h) in enumerate(best_combos[:10]):
        out.append(f"| {i+1} | Q{combo[0]}+Q{combo[1]}+Q{combo[2]} | {h:.3f} |")

    out.append(f"\n### 9.2 最弱三题组合\n")
    out.append("| 排名 | 锚点组合 | 残余熵 |")
    out.append("|------|---------|--------|")
    for i, (combo, h) in enumerate(best_combos[-5:]):
        out.append(f"| {len(best_combos)-4+i} | Q{combo[0]}+Q{combo[1]}+Q{combo[2]} | {h:.3f} |")

    best = best_combos[0]
    out.append(f"\n**信息互补性最强的三题组合：Q{best[0][0]}+Q{best[0][1]}+Q{best[0][2]}**")
    out.append(f"- 残余熵 {best[1]:.3f} bits ≈ 每题在 {2**best[1]:.1f} 个带中搜索")

    return "\n".join(out)

# ─────────────────────────────────────────────
# 10. 同段重复详情
# ─────────────────────────────────────────────
def analysis_collision_detail(rows, by_title):
    out = []
    out.append("## 10. 同段重复详情\n")

    dup_titles = []
    for title, qs in by_title.items():
        letters = [q["letter"] for q in qs]
        if len(set(letters)) < 10:
            q_map = defaultdict(list)
            for q in qs:
                q_map[q["letter"]].append(q["qnum"])
            dups = [l for l in set(letters) if letters.count(l) > 1]
            info = [f"{d}→Q{',Q'.join(str(x) for x in q_map[d])}" for d in dups]
            dup_titles.append((title, info, qs[0]["pcount"]))

    if dup_titles:
        out.append("| 文章 | 段落数 | 同段重复详情 |")
        out.append("|------|--------|---------|")
        for title, info, pc in dup_titles:
            short = title[:40] + ("..." if len(title) > 40 else "")
            out.append(f"| {short} | {pc} | {'; '.join(info)} |")
        out.append(f"\n- 同段重复篇数：{len(dup_titles)}/56")
        out.append("- 说明：Section B 允许同一段被多次选择，重复本身不能判为数据错误")
    else:
        out.append("全部 56 篇均无同段重复。")

    return "\n".join(out)


def main():
    rows = load_data()
    by_title = group_by_title(rows)
    print(f"Loaded {len(rows)} records from {len(by_title)} titles")

    sections = []
    sections.append("# CET-6 Section B 深度分析 Round 2\n")
    sections.append(f"基于 {len(by_title)} 篇，消除段落数差异后的标准化分析。\n")

    sections.append(analysis_normalized_letter_preference(rows, by_title))
    sections.append(analysis_rank_order(rows, by_title))
    sections.append(analysis_position_normalized(rows, by_title))
    sections.append(analysis_consecutive_coverage(rows, by_title))
    sections.append(analysis_positional_entropy(rows, by_title))
    sections.append(analysis_elimination_speed(rows, by_title))
    sections.append(analysis_difficulty_proxy(rows, by_title))
    sections.append(analysis_density_hotzone(rows, by_title))
    sections.append(analysis_anchor_chain(rows, by_title))
    sections.append(analysis_collision_detail(rows, by_title))

    full_text = "\n\n".join(sections)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Written to {OUT_PATH}")
    print(f"Length: {len(full_text)} chars")

if __name__ == "__main__":
    main()
