import csv
import os
from collections import defaultdict, Counter
import statistics
import math
from itertools import combinations

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(DATA_DIR, "manual_truth_records.csv")
OUT_PATH = os.path.join(DATA_DIR, "deep_analysis_round3.md")

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

def analysis_collision_audit(rows, by_title):
    out = []
    out.append("## 1. 同段重复清单\n")
    for title, qs in by_title.items():
        letters = [q["letter"] for q in qs]
        if len(set(letters)) < 10:
            out.append(f"### {title}\n")
            out.append(f"- 文件：{qs[0]['file']}")
            out.append(f"- 段落数：{qs[0]['pcount']}")
            out.append(f"- 可用字母：A ~ {chr(ord('A') + qs[0]['pcount'] - 1)}\n")
            sorted_qs = sorted(qs, key=lambda x: x["qnum"])
            out.append("| 题号 | 答案 | 位置% |")
            out.append("|------|------|-------|")
            for q in sorted_qs:
                flag = " **重复**" if letters.count(q["letter"]) > 1 else ""
                out.append(f"| Q{q['qnum']} | {q['letter']} | {q['pct']:.1f}%{flag} |")
            all_possible = set(chr(ord('A') + i) for i in range(qs[0]["pcount"]))
            used = set(letters)
            missing = sorted(all_possible - used)
            dup_letters = [l for l in set(letters) if letters.count(l) > 1]
            out.append(f"\n- 重复：{dup_letters}  缺失：{missing}")
            out.append(f"- **诊断**：某题答案可能应为 {missing} 中的一个\n")
    return "\n".join(out)

def analysis_pairwise_gap(rows, by_title):
    out = []
    out.append("## 2. 题对位置差分布\n")
    q_pcts = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_pcts[title][q["qnum"]] = q["pct"]
    titles = [t for t, d in q_pcts.items() if len(d) == 10]
    out.append("### 2.1 相邻题位置差（绝对值）\n")
    out.append("| 题对 | 中位差 | 均值 | <20% | >40% |")
    out.append("|------|-------|------|------|------|")
    for qi in range(36, 45):
        diffs = [abs(q_pcts[t][qi] - q_pcts[t][qi+1]) for t in titles]
        med = statistics.median(diffs)
        avg = statistics.mean(diffs)
        close = sum(1 for d in diffs if d < 20) / len(diffs) * 100
        far = sum(1 for d in diffs if d > 40) / len(diffs) * 100
        out.append(f"| Q{qi}/Q{qi+1} | {med:.1f}% | {avg:.1f}% | {close:.0f}% | {far:.0f}% |")
    out.append("\n### 2.2 关键非相邻题对\n")
    out.append("| 题对 | 中位差 | <20% | >40% |")
    out.append("|------|-------|------|------|")
    for qi, qj in [(36,38),(36,44),(37,39),(38,40),(38,42),(40,42),(41,45),(43,45)]:
        diffs = [abs(q_pcts[t][qi] - q_pcts[t][qj]) for t in titles]
        med = statistics.median(diffs)
        close = sum(1 for d in diffs if d < 20) / len(diffs) * 100
        far = sum(1 for d in diffs if d > 40) / len(diffs) * 100
        out.append(f"| Q{qi}/Q{qj} | {med:.1f}% | {close:.0f}% | {far:.0f}% |")
    return "\n".join(out)

def analysis_conditional_windows(rows, by_title):
    out = []
    out.append("## 3. 条件搜索窗口（80%覆盖）\n")
    q_pcts = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_pcts[title][q["qnum"]] = q["pct"]
    titles = [t for t, d in q_pcts.items() if len(d) == 10]
    bands = ["0-20", "20-40", "40-60", "60-80", "80-100"]
    for anchor in [36, 38, 40, 42, 44]:
        out.append(f"\n### 锚点 Q{anchor}\n")
        out.append(f"| Q{anchor}带 | 目标 | 80%窗口 | 宽度 | n |")
        out.append("|---------|------|--------|------|---|")
        for band in bands:
            bt = [t for t in titles if band_20(q_pcts[t][anchor]) == band]
            if len(bt) < 4: continue
            for tgt in range(36, 46):
                if tgt == anchor: continue
                tp = sorted(q_pcts[t][tgt] for t in bt)
                n = len(tp)
                lo = tp[max(0, int(n * 0.1))]
                hi = tp[min(n-1, int(n * 0.9))]
                w = hi - lo
                if w <= 50:
                    out.append(f"| {band}% | Q{tgt} | {lo:.0f}-{hi:.0f}% | {w:.0f} | {n} |")
    return "\n".join(out)

def analysis_bayesian_simulation(rows, by_title):
    out = []
    out.append("## 4. 贪心信息增益序列\n")
    q_bands = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_bands[title][q["qnum"]] = band_20(q["pct"])
    titles = [t for t, d in q_bands.items() if len(d) == 10]
    bands = ["0-20", "20-40", "40-60", "60-80", "80-100"]

    def entropy_of(question, subset):
        bc = Counter(q_bands[t][question] for t in subset if question in q_bands[t])
        total = sum(bc.values())
        if total == 0: return math.log2(5)
        return -sum((c/total) * math.log2(c/total) for c in bc.values() if c > 0)

    unc = {q: entropy_of(q, titles) for q in range(36, 46)}
    remaining = list(range(36, 46))
    order = []
    gains = []

    while remaining:
        best_q = None
        best_gain = -1
        for cand in remaining:
            gain = 0
            others = [q for q in remaining if q != cand]
            for band in bands:
                bt = [t for t in titles if q_bands[t].get(cand) == band]
                if not bt: continue
                p = len(bt) / len(titles)
                for oq in others:
                    gain += p * (unc.get(oq, 0) - entropy_of(oq, bt))
            if gain > best_gain:
                best_gain = gain
                best_q = cand
        remaining.remove(best_q)
        order.append(best_q)
        gains.append(best_gain)
        for q in remaining:
            ch = []
            for band in bands:
                bt = [t for t in titles if q_bands[t].get(best_q) == band]
                if bt: ch.append((len(bt)/len(titles), entropy_of(q, bt)))
            if ch: unc[q] = sum(p*h for p, h in ch)

    out.append("| 步骤 | 做题 | 信息增益 | 角色 |")
    out.append("|------|------|---------|------|")
    for i, (q, g) in enumerate(zip(order, gains)):
        role = ""
        if i == 0: role = "信息增益最大"
        elif i <= 2: role = "高信息量"
        elif i >= 7: role = "弱排除"
        out.append(f"| {i+1} | Q{q} | {g:.3f} | {role} |")
    out.append(f"\n**贪心最优序列：{'→'.join(f'Q{q}' for q in order)}**")
    return "\n".join(out)

def analysis_strategy_simulation(rows, by_title):
    out = []
    out.append("## 5. 策略搜索效率对比\n")
    q_pcts = defaultdict(dict)
    q_bands = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_pcts[title][q["qnum"]] = q["pct"]
            q_bands[title][q["qnum"]] = band_20(q["pct"])
    titles = [t for t, d in q_pcts.items() if len(d) == 10]
    strategies = {
        "顺序(36→45)": list(range(36, 46)),
        "锚链(36→38→40→42→44→37→39→41→43→45)": [36,38,40,42,44,37,39,41,43,45],
    }
    for sname, sorder in strategies.items():
        out.append(f"\n### {sname}\n")
        out.append("| 步骤 | 做题 | 剩余题平均候选带 |")
        out.append("|------|------|----------------|")
        for step in range(min(6, len(sorder))):
            done = sorder[:step+1]
            rest = [q for q in range(36, 46) if q not in done]
            if not rest: break
            total_bands = 0
            count = 0
            for t in titles:
                key = tuple(q_bands[t][q] for q in done)
                for rq in rest:
                    matching = [t2 for t2 in titles if tuple(q_bands[t2][q] for q in done) == key]
                    total_bands += len(set(q_bands[t2][rq] for t2 in matching))
                    count += 1
            out.append(f"| {step+1} | Q{sorder[step]} | {total_bands/count:.2f} |")
    return "\n".join(out)

def analysis_directional_gap(rows, by_title):
    out = []
    out.append("## 6. 题对有向位置差\n")
    out.append("正=目标在锚点后面。\n")
    q_pcts = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_pcts[title][q["qnum"]] = q["pct"]
    titles = [t for t, d in q_pcts.items() if len(d) == 10]
    out.append("### 从 Q36 看\n")
    out.append("| 目标 | 中位差 | 在后面% | 中位距离 |")
    out.append("|------|-------|--------|---------|")
    for tgt in range(37, 46):
        diffs = [q_pcts[t][tgt] - q_pcts[t][36] for t in titles]
        med = statistics.median(diffs)
        behind = sum(1 for d in diffs if d > 0) / len(diffs) * 100
        med_abs = statistics.median([abs(d) for d in diffs])
        out.append(f"| Q{tgt} | {med:+.1f}% | {behind:.0f}% | {med_abs:.1f}% |")
    out.append("\n### 从 Q44 看\n")
    out.append("| 目标 | 中位差 | 在后面% | 中位距离 |")
    out.append("|------|-------|--------|---------|")
    for tgt in [36,37,38,39,40,41,42,43,45]:
        diffs = [q_pcts[t][tgt] - q_pcts[t][44] for t in titles]
        med = statistics.median(diffs)
        behind = sum(1 for d in diffs if d > 0) / len(diffs) * 100
        med_abs = statistics.median([abs(d) for d in diffs])
        out.append(f"| Q{tgt} | {med:+.1f}% | {behind:.0f}% | {med_abs:.1f}% |")
    return "\n".join(out)

def analysis_paragraph_type(rows, by_title):
    out = []
    out.append("## 7. 段落类型偏好\n")
    first = second = penult = last = 0
    for title, qs in by_title.items():
        pc = qs[0]["pcount"]
        used = set(q["letter"] for q in qs)
        if 'A' in used: first += 1
        if chr(ord('A')+pc-1) in used: last += 1
        if 'B' in used: second += 1
        if chr(ord('A')+pc-2) in used: penult += 1
    total = len(by_title)
    pcounts = [qs[0]["pcount"] for qs in by_title.values()]
    exp = 10 / statistics.mean(pcounts) * 100
    out.append("| 类型 | 选为答案 | 选率 | 期望 | 偏差 |")
    out.append("|------|---------|------|------|------|")
    out.append(f"| 首段A | {first}/{total} | {first/total*100:.1f}% | {exp:.0f}% | {first/total*100-exp:+.1f}% |")
    out.append(f"| 第二段B | {second}/{total} | {second/total*100:.1f}% | {exp:.0f}% | {second/total*100-exp:+.1f}% |")
    out.append(f"| 倒数第二 | {penult}/{total} | {penult/total*100:.1f}% | {exp:.0f}% | {penult/total*100-exp:+.1f}% |")
    out.append(f"| 末段 | {last}/{total} | {last/total*100:.1f}% | {exp:.0f}% | {last/total*100-exp:+.1f}% |")
    return "\n".join(out)

def analysis_decision_tree(rows, by_title):
    out = []
    out.append("## 8. 机械化做题决策树\n")
    q_bands = defaultdict(dict)
    for title, qs in by_title.items():
        for q in qs:
            q_bands[title][q["qnum"]] = band_20(q["pct"])
    titles = [t for t, d in q_bands.items() if len(d) == 10]
    bands = ["0-20", "20-40", "40-60", "60-80", "80-100"]
    out.append("### Step 1: Q36 定位后的推断\n")
    out.append("```")
    for band in bands:
        bt = [t for t in titles if q_bands[t][36] == band]
        if len(bt) < 3: continue
        out.append(f"\nQ36 ∈ {band}%  (n={len(bt)}):")
        for tgt in [38,40,42,37,39,41,43,44,45]:
            tc = Counter(q_bands[t][tgt] for t in bt)
            top = tc.most_common(1)[0]
            pct = top[1]/len(bt)*100
            if pct >= 35:
                runner = tc.most_common(2)
                r2 = f", 次={runner[1][0]}%({runner[1][1]/len(bt)*100:.0f}%)" if len(runner) > 1 else ""
                out.append(f"  Q{tgt} → {top[0]}% ({pct:.0f}%){r2}")
    out.append("```")
    out.append("\n### Step 2: Q36+Q38 双锚推断\n")
    out.append("```")
    for b36 in ["20-40", "40-60"]:
        for b38 in bands:
            bt = [t for t in titles if q_bands[t][36] == b36 and q_bands[t][38] == b38]
            if len(bt) < 3: continue
            out.append(f"\nQ36∈{b36}% + Q38∈{b38}%  (n={len(bt)}):")
            for tgt in [40,42,37,39,41,43,44,45]:
                tc = Counter(q_bands[t][tgt] for t in bt)
                top = tc.most_common(1)[0]
                pct = top[1]/len(bt)*100
                if pct >= 45:
                    out.append(f"  Q{tgt} → {top[0]}% ({pct:.0f}%)")
    out.append("```")
    return "\n".join(out)


def main():
    rows = load_data()
    by_title = group_by_title(rows)
    print(f"Loaded {len(rows)} records from {len(by_title)} titles")
    sections = []
    sections.append("# CET-6 Section B 深度分析 Round 3\n")
    sections.append(f"基于 {len(by_title)} 篇。同段重复清单 + 条件窗口 + 贝叶斯 + 策略模拟 + 决策树。\n")
    sections.append(analysis_collision_audit(rows, by_title))
    sections.append(analysis_pairwise_gap(rows, by_title))
    sections.append(analysis_conditional_windows(rows, by_title))
    sections.append(analysis_bayesian_simulation(rows, by_title))
    sections.append(analysis_strategy_simulation(rows, by_title))
    sections.append(analysis_directional_gap(rows, by_title))
    sections.append(analysis_paragraph_type(rows, by_title))
    sections.append(analysis_decision_tree(rows, by_title))
    full_text = "\n\n".join(sections)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Written to {OUT_PATH}")
    print(f"Length: {len(full_text)} chars")

if __name__ == "__main__":
    main()
