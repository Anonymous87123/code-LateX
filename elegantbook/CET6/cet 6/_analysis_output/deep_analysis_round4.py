import csv
import os
import re
from collections import defaultdict, Counter
import statistics
import math

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(DATA_DIR, "manual_truth_records.csv")
OUT_PATH = os.path.join(DATA_DIR, "deep_analysis_round4.md")

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
                    r["letter_idx"] = ord(r["answer_letter"]) - ord('A')
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

def extract_year(filename):
    m = re.search(r"(20\d{2})", filename)
    return int(m.group(1)) if m else None

def band_20(pct):
    if pct < 20: return "0-20"
    if pct < 40: return "20-40"
    if pct < 60: return "40-60"
    if pct < 80: return "60-80"
    return "80-100"

def analysis_year_trend(rows, by_title):
    out = []
    out.append("## 1. 年度趋势分析\n")
    year_data = defaultdict(lambda: {"pcts": defaultdict(list), "pcounts": [], "titles": []})
    for title, qs in by_title.items():
        yr = extract_year(qs[0]["file"])
        if yr is None:
            continue
        year_data[yr]["titles"].append(title)
        year_data[yr]["pcounts"].append(qs[0]["pcount"])
        for q in qs:
            year_data[yr]["pcts"][q["qnum"]].append(q["pct"])

    out.append("### 1.1 段落数趋势\n")
    out.append("| 年份 | 篇数 | 平均段落 | 最小 | 最大 |")
    out.append("|------|------|---------|------|------|")
    for yr in sorted(year_data.keys()):
        d = year_data[yr]
        pcs = d["pcounts"]
        out.append(f"| {yr} | {len(pcs)} | {statistics.mean(pcs):.1f} | {min(pcs)} | {max(pcs)} |")

    out.append("\n### 1.2 位置分散度趋势（全题平均σ）\n")
    out.append("| 年份 | 平均σ | Q36σ | Q41σ | Q45σ |")
    out.append("|------|------|------|------|------|")
    for yr in sorted(year_data.keys()):
        d = year_data[yr]
        sds = []
        q36sd = q41sd = q45sd = "-"
        for q in range(36, 46):
            vals = d["pcts"][q]
            if len(vals) >= 2:
                sd = statistics.stdev(vals)
                sds.append(sd)
                if q == 36: q36sd = f"{sd:.1f}"
                if q == 41: q41sd = f"{sd:.1f}"
                if q == 45: q45sd = f"{sd:.1f}"
        avg_sd = statistics.mean(sds) if sds else 0
        out.append(f"| {yr} | {avg_sd:.1f} | {q36sd} | {q41sd} | {q45sd} |")

    out.append("\n### 1.3 前后期对比（2016-2019 vs 2020-2025）\n")
    early = []
    late = []
    for title, qs in by_title.items():
        yr = extract_year(qs[0]["file"])
        if yr is None: continue
        vec = {q["qnum"]: q["pct"] for q in qs}
        if yr <= 2019:
            early.append(vec)
        else:
            late.append(vec)

    out.append("| 题号 | 前期中位 | 后期中位 | 差值 | 前期σ | 后期σ |")
    out.append("|------|---------|---------|------|------|------|")
    for q in range(36, 46):
        ev = [v[q] for v in early if q in v]
        lv = [v[q] for v in late if q in v]
        if ev and lv:
            em = statistics.median(ev)
            lm = statistics.median(lv)
            esd = statistics.stdev(ev) if len(ev) > 1 else 0
            lsd = statistics.stdev(lv) if len(lv) > 1 else 0
            out.append(f"| Q{q} | {em:.1f}% | {lm:.1f}% | {lm-em:+.1f}% | {esd:.1f} | {lsd:.1f} |")

    return "\n".join(out)

def analysis_letter_preference(rows, by_title):
    out = []
    out.append("## 2. 每题答案字母偏好\n")
    out.append("显示每题最常选中的字母及频率。\n")

    q_letters = defaultdict(list)
    for r in rows:
        q_letters[r["qnum"]].append(r["letter"])

    out.append("| 题号 | Top1 | Top2 | Top3 | 唯一字母数 | 最大占比 |")
    out.append("|------|------|------|------|----------|---------|")
    for q in range(36, 46):
        c = Counter(q_letters[q])
        top3 = c.most_common(3)
        total = sum(c.values())
        unique = len(c)
        cells = []
        for letter, cnt in top3:
            cells.append(f"{letter}({cnt}/{total}={cnt/total*100:.0f}%)")
        while len(cells) < 3:
            cells.append("-")
        max_pct = top3[0][1] / total * 100
        out.append(f"| Q{q} | {cells[0]} | {cells[1]} | {cells[2]} | {unique} | {max_pct:.0f}% |")

    out.append("\n### 2.2 字母使用热图（Q×Letter计数）\n")
    all_letters = sorted(set(r["letter"] for r in rows))
    header = "| 题号 | " + " | ".join(all_letters) + " |"
    sep = "|------" + "|---" * len(all_letters) + "|"
    out.append(header)
    out.append(sep)
    for q in range(36, 46):
        c = Counter(q_letters[q])
        cells = [str(c.get(l, 0)) for l in all_letters]
        out.append(f"| Q{q} | " + " | ".join(cells) + " |")

    return "\n".join(out)

def analysis_letter_gap(rows, by_title):
    out = []
    out.append("## 3. 相邻题答案字母间距\n")
    out.append("字母间距 = |letter_idx(Qi+1) - letter_idx(Qi)|。反映答案在段落上的跳跃幅度。\n")

    q_idx = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_idx[title][q["qnum"]] = q["letter_idx"]

    titles = [t for t, d in q_idx.items() if len(d) == 10]

    out.append("| 题对 | 中位间距 | 均值 | 间距=0 | 间距=1 | 间距≥5 |")
    out.append("|------|---------|------|--------|--------|--------|")
    for qi in range(36, 45):
        gaps = [abs(q_idx[t][qi+1] - q_idx[t][qi]) for t in titles]
        med = statistics.median(gaps)
        avg = statistics.mean(gaps)
        z = sum(1 for g in gaps if g == 0) / len(gaps) * 100
        one = sum(1 for g in gaps if g == 1) / len(gaps) * 100
        big = sum(1 for g in gaps if g >= 5) / len(gaps) * 100
        out.append(f"| Q{qi}/Q{qi+1} | {med:.0f} | {avg:.1f} | {z:.0f}% | {one:.0f}% | {big:.0f}% |")

    out.append("\n### 3.2 总体字母间距分布\n")
    all_gaps = []
    for t in titles:
        for qi in range(36, 45):
            all_gaps.append(abs(q_idx[t][qi+1] - q_idx[t][qi]))
    gc = Counter(all_gaps)
    out.append("| 间距 | 次数 | 占比 |")
    out.append("|------|------|------|")
    for g in sorted(gc.keys()):
        out.append(f"| {g} | {gc[g]} | {gc[g]/len(all_gaps)*100:.1f}% |")

    return "\n".join(out)

def analysis_cross_conditional(rows, by_title):
    out = []
    out.append("## 4. 交叉条件概率（Q_i带→Q_j带）\n")
    out.append("给定Q_i所在20%带，Q_j最可能在哪个带。仅显示条件概率≥35%的强关联。\n")

    q_bands = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_bands[title][q["qnum"]] = band_20(q["pct"])
    titles = [t for t, d in q_bands.items() if len(d) == 10]
    bands = ["0-20", "20-40", "40-60", "60-80", "80-100"]

    strong_rules = []
    for qi in range(36, 46):
        for qj in range(36, 46):
            if qi == qj: continue
            for band in bands:
                bt = [t for t in titles if q_bands[t][qi] == band]
                if len(bt) < 5: continue
                tc = Counter(q_bands[t][qj] for t in bt)
                top = tc.most_common(1)[0]
                pct = top[1] / len(bt) * 100
                if pct >= 35:
                    strong_rules.append((qi, band, qj, top[0], pct, len(bt)))

    strong_rules.sort(key=lambda x: -x[4])
    out.append("| 条件 | 目标 | 最可能带 | 概率 | n |")
    out.append("|------|------|---------|------|---|")
    for qi, band, qj, tband, pct, n in strong_rules[:40]:
        out.append(f"| Q{qi}∈{band}% | Q{qj} | {tband}% | {pct:.0f}% | {n} |")

    out.append(f"\n- 总强规则数（≥35%）：{len(strong_rules)}")
    if strong_rules:
        out.append(f"- 最强规则：Q{strong_rules[0][0]}∈{strong_rules[0][1]}% → Q{strong_rules[0][2]}∈{strong_rules[0][3]}% ({strong_rules[0][4]:.0f}%)")

    return "\n".join(out)

def analysis_paper_clustering(rows, by_title):
    out = []
    out.append("## 5. 试卷位置向量聚类\n")
    out.append("用10维位置向量（Q36-Q45的pct）做两两欧氏距离，找最相似/最不同的试卷对。\n")

    vecs = {}
    for title, qs in by_title.items():
        d = {q["qnum"]: q["pct"] for q in qs}
        if len(d) == 10:
            vecs[title] = [d[q] for q in range(36, 46)]

    titles = list(vecs.keys())
    dists = []
    for i in range(len(titles)):
        for j in range(i+1, len(titles)):
            d = math.sqrt(sum((a-b)**2 for a, b in zip(vecs[titles[i]], vecs[titles[j]])))
            dists.append((titles[i], titles[j], d))

    dists.sort(key=lambda x: x[2])

    out.append("### 5.1 最相似试卷对（Top 10）\n")
    out.append("| 排名 | 试卷A | 试卷B | 距离 |")
    out.append("|------|-------|-------|------|")
    for i, (a, b, d) in enumerate(dists[:10]):
        out.append(f"| {i+1} | {a[:30]} | {b[:30]} | {d:.1f} |")

    out.append("\n### 5.2 最不同试卷对（Top 5）\n")
    out.append("| 排名 | 试卷A | 试卷B | 距离 |")
    out.append("|------|-------|-------|------|")
    for i, (a, b, d) in enumerate(dists[-5:]):
        out.append(f"| {len(dists)-4+i} | {a[:30]} | {b[:30]} | {d:.1f} |")

    avg_d = statistics.mean([x[2] for x in dists])
    med_d = statistics.median([x[2] for x in dists])
    out.append(f"\n- 平均距离：{avg_d:.1f}")
    out.append(f"- 中位距离：{med_d:.1f}")
    out.append(f"- 距离范围：{dists[0][2]:.1f} ~ {dists[-1][2]:.1f}")

    return "\n".join(out)

def analysis_answer_diversity(rows, by_title):
    out = []
    out.append("## 6. 答案字母多样性\n")

    diversity_data = []
    for title, qs in by_title.items():
        letters = [q["letter"] for q in qs]
        unique = len(set(letters))
        pc = qs[0]["pcount"]
        coverage = unique / pc * 100
        indices = sorted(ord(l) - ord('A') for l in set(letters))
        span = indices[-1] - indices[0] + 1 if indices else 0
        diversity_data.append({
            "title": title, "unique": unique, "pc": pc,
            "coverage": coverage, "span": span, "file": qs[0]["file"]
        })

    out.append("### 6.1 唯一字母数分布\n")
    uc = Counter(d["unique"] for d in diversity_data)
    out.append("| 唯一字母数 | 篇数 | 占比 |")
    out.append("|----------|------|------|")
    for u in sorted(uc.keys()):
        out.append(f"| {u} | {uc[u]} | {uc[u]/len(diversity_data)*100:.1f}% |")

    out.append(f"\n- 常见唯一数=10（多数试卷每题不同段），实际中位={statistics.median([d['unique'] for d in diversity_data]):.0f}")

    out.append("\n### 6.2 覆盖率（唯一字母/段落数）\n")
    coverages = [d["coverage"] for d in diversity_data]
    out.append(f"- 平均覆盖率：{statistics.mean(coverages):.1f}%")
    out.append(f"- 最低覆盖率：{min(coverages):.1f}%")
    out.append(f"- 最高覆盖率：{max(coverages):.1f}%")

    out.append("\n### 6.3 按段落数分组的覆盖率\n")
    out.append("| 段落数 | 篇数 | 平均覆盖率 | 同段重复篇数 |")
    out.append("|--------|------|----------|---------|")
    pc_groups = defaultdict(list)
    for d in diversity_data:
        pc_groups[d["pc"]].append(d)
    for pc in sorted(pc_groups.keys()):
        items = pc_groups[pc]
        avg_cov = statistics.mean([d["coverage"] for d in items])
        collisions = sum(1 for d in items if d["unique"] < 10)
        out.append(f"| {pc} | {len(items)} | {avg_cov:.1f}% | {collisions} |")

    return "\n".join(out)

def analysis_position_symmetry(rows, by_title):
    out = []
    out.append("## 7. 前后半对称性\n")
    out.append("每题答案落在文章前半(0-50%) vs 后半(50-100%)的比例。\n")

    out.append("| 题号 | 前半 | 后半 | 前半% | 偏向 |")
    out.append("|------|------|------|-------|------|")
    for q in range(36, 46):
        qr = [r for r in rows if r["qnum"] == q]
        front = sum(1 for r in qr if r["pct"] < 50)
        back = len(qr) - front
        fp = front / len(qr) * 100
        bias = "前半" if fp > 55 else ("后半" if fp < 45 else "均衡")
        out.append(f"| Q{q} | {front} | {back} | {fp:.1f}% | {bias} |")

    out.append("\n### 7.2 题号与前后半关联\n")
    out.append("Q36-Q39倾向前半还是后半？Q41-Q45呢？\n")
    for group_name, group_range in [("Q36-Q39", range(36, 40)), ("Q40-Q42", range(40, 43)), ("Q43-Q45", range(43, 46))]:
        qr = [r for r in rows if r["qnum"] in group_range]
        front = sum(1 for r in qr if r["pct"] < 50)
        fp = front / len(qr) * 100
        out.append(f"- {group_name}：前半 {fp:.1f}%")

    return "\n".join(out)

def analysis_paragraph_reuse(rows, by_title):
    out = []
    out.append("## 8. 段落位置重用频率\n")
    out.append("哪些相对位置（10%桶）被不同题号反复命中？\n")

    bin_q = defaultdict(lambda: defaultdict(int))
    for r in rows:
        b = int(r["pct"] / 10) * 10
        bin_key = f"{b}-{b+10}%"
        bin_q[bin_key][r["qnum"]] += 1

    bins = sorted(bin_q.keys(), key=lambda x: int(x.split("-")[0]))
    out.append("| 位置桶 | 总命中 | 命中题号数 | 最频题号 |")
    out.append("|--------|--------|----------|---------|")
    for b in bins:
        total = sum(bin_q[b].values())
        unique_q = len(bin_q[b])
        top_q = max(bin_q[b], key=bin_q[b].get)
        out.append(f"| {b} | {total} | {unique_q} | Q{top_q}({bin_q[b][top_q]}) |")

    out.append("\n### 8.2 竞争最激烈的位置桶\n")
    out.append("多题号共享同一位置桶 = 考试时该区域容易混淆。\n")
    competition = []
    for b in bins:
        counts = list(bin_q[b].values())
        if len(counts) >= 2:
            entropy = -sum((c/sum(counts)) * math.log2(c/sum(counts)) for c in counts if c > 0)
            competition.append((b, sum(counts), entropy))
    competition.sort(key=lambda x: -x[2])
    out.append("| 位置桶 | 总命中 | 竞争熵 | 难度评估 |")
    out.append("|--------|--------|--------|---------|")
    for b, total, h in competition:
        level = "高竞争" if h > 3.0 else ("中等" if h > 2.5 else "低竞争")
        out.append(f"| {b} | {total} | {h:.2f} | {level} |")

    return "\n".join(out)

def analysis_strategy_matrix(rows, by_title):
    out = []
    out.append("## 9. 综合做题策略矩阵\n")
    out.append("整合全部4轮分析，给出每题最优搜索策略。\n")

    q_data = {}
    for q in range(36, 46):
        qr = [r for r in rows if r["qnum"] == q]
        pcts = [r["pct"] for r in qr]
        med = statistics.median(pcts)
        sd = statistics.stdev(pcts)
        front = sum(1 for p in pcts if p < 50) / len(pcts) * 100
        bc = Counter(band_20(p) for p in pcts)
        top_band = bc.most_common(1)[0]
        top_pct = top_band[1] / len(pcts) * 100
        probs = [bc.get(b, 0)/len(pcts) for b in ["0-20","20-40","40-60","60-80","80-100"]]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        q_data[q] = {
            "med": med, "sd": sd, "front": front,
            "top_band": top_band[0], "top_pct": top_pct,
            "entropy": entropy
        }

    out.append("| 题号 | 中位位置 | σ | 最优带(概率) | 熵 | 前半% | 搜索建议 |")
    out.append("|------|---------|---|------------|-----|------|---------|")
    for q in range(36, 46):
        d = q_data[q]
        if d["sd"] < 22:
            advice = f"集中搜{d['top_band']}%"
        elif d["top_pct"] > 35:
            advice = f"优先{d['top_band']}%，兼顾邻带"
        else:
            advice = "均匀扫描"
        out.append(f"| Q{q} | {d['med']:.0f}% | {d['sd']:.0f} | {d['top_band']}%({d['top_pct']:.0f}%) | {d['entropy']:.2f} | {d['front']:.0f}% | {advice} |")

    out.append("\n### 9.2 最佳做题流程（全局推荐）\n")
    out.append("```")
    out.append("Phase 1 — 锚定（3题，~3分钟）")
    out.append("  1. Q38: 扫描全文中段偏前，确定位置带")
    out.append("  2. Q40: 扫描中段，与Q38形成双锚")
    out.append("  3. Q42: 扫描前段或中段，三锚定位")
    out.append("")
    out.append("Phase 2 — 信息题（4题，~4分钟）")
    out.append("  4. Q41: 偏后半（80-100%最集中），用三锚缩窗")
    out.append("  5. Q37: 偏前半（0-20%最集中），用已知排除")
    out.append("  6. Q44: 20-40%带最集中，位置稳定")
    out.append("  7. Q43: 40-60%带，用条件窗口和弱排除缩小")
    out.append("")
    out.append("Phase 3 — 收尾（3题，~2分钟）")
    out.append("  8. Q36: σ最小最稳定，20-40%集中")
    out.append("  9. Q45: 60-80%集中，弱排除价值较高")
    out.append("  10. Q39: 20-40%集中，最后排除定答案")
    out.append("```")

    return "\n".join(out)


def main():
    rows = load_data()
    by_title = group_by_title(rows)
    print(f"Loaded {len(rows)} records from {len(by_title)} titles")

    sections = []
    sections.append("# CET-6 Section B 深度分析 Round 4\n")
    sections.append(f"基于 {len(by_title)} 篇。年度趋势 + 字母偏好 + 字母间距 + 条件概率 + 聚类 + 多样性 + 对称性 + 段落重用 + 策略矩阵。\n")

    sections.append(analysis_year_trend(rows, by_title))
    sections.append(analysis_letter_preference(rows, by_title))
    sections.append(analysis_letter_gap(rows, by_title))
    sections.append(analysis_cross_conditional(rows, by_title))
    sections.append(analysis_paper_clustering(rows, by_title))
    sections.append(analysis_answer_diversity(rows, by_title))
    sections.append(analysis_position_symmetry(rows, by_title))
    sections.append(analysis_paragraph_reuse(rows, by_title))
    sections.append(analysis_strategy_matrix(rows, by_title))

    full_text = "\n\n".join(sections)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Written to {OUT_PATH}")
    print(f"Length: {len(full_text)} chars")

if __name__ == "__main__":
    main()
