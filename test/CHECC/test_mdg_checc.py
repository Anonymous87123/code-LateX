#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 CHECC 类（与 MDG 分解结合）在 CEC2013 LSGO 上的性能。
记录并输出在 3e5, 1e6, 3e6 次评价处的适应度值。
"""

import numpy as np
import os
import sys
import json
import argparse
import contextlib
import io

# 添加项目根目录到路径（根据实际结构调整）
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Benchmarks.cec2013lsgo.cec2013 import Benchmark
# from cec2013lsgo.cec2013 import Benchmark
from Algorithms.CC.VI_based_Dec.MDG.mdg import MDG
from Algorithms.CC.CBCC.CHECC.checc import CHECC   # 导入封装的 CHECC 类


# ============================================================================
# 工具函数：校验并修复分组
# ============================================================================
def validate_and_fix_groups(groups, D):
    """确保分组为0-based，覆盖所有维度，补全缺失维度。"""
    flat = [i for g in groups for i in g]
    if len(flat) == 0:
        raise ValueError("Groups is empty.")

    mn, mx = min(flat), max(flat)

    # 若为1-based，转换为0-based
    if mn == 1 and mx == D:
        groups = [[i - 1 for i in g] for g in groups]
        flat = [i for g in groups for i in g]
        mn, mx = min(flat), max(flat)

    if mn < 0 or mx >= D:
        raise ValueError(f"Group index out of range after fixing: min={mn}, max={mx}, D={D}")

    flat_set = set(flat)
    covered = len(flat_set)
    missing = set(range(D)) - flat_set
    duplicated = (len(flat) != len(flat_set))

    info = {
        "covered_dims": covered,
        "missing_dims": len(missing),
        "has_duplicate": duplicated
    }

    if missing:
        for i in sorted(missing):
            groups.append([i])

    return groups, info


# ============================================================================
# 使用 MDG 获取分组
# ============================================================================
def get_groups_with_mdg(fun, info, verbose=False):
    """调用 MDG 分解，返回分组列表、消耗的 FEs 和统计信息。"""
    lb = info['lower']
    ub = info['upper']
    base = (ub + lb) / 2.0 - (ub - lb) / 8.0
    sigma = (ub - lb) / 4.0
    cfg = {'base': base, 'sigma': sigma}

    mdg_engine = MDG(fun, info, cfg)

    output = mdg_engine.decompose()
    decomp_fes = output['FEs']

    print(f"MDG 分解消费 FEs: {output['FEs']}")

    groups = []
    for g in output.get('nonseps', []):
        groups.append(list(g))
    for idx in output.get('seps', []):
        groups.append([int(idx)])

    group_n = len(groups)
    nonsep_n = len(output.get('nonseps', []))
    sep_n = len(output.get('seps', []))

    # 获取 CS 向量（注意顺序：先 nonseps 后 seps，与 groups 一致）
    group_cs = output.get('group_cs', [])
    # 确保长度匹配
    if len(group_cs) != group_n:
        # 若 MDG 未提供，则用默认（全1）
        group_cs = np.ones(group_n)

    if verbose:
        print(f"  ✓ MDG done: groupN={group_n}, nonsep={nonsep_n}, seps={sep_n}, decompFEs={decomp_fes}")

    return groups, decomp_fes, group_cs, {"group_n": group_n, "nonsep_n": nonsep_n, "sep_n": sep_n}


# ============================================================================
# 单个函数运行包装器
# ============================================================================
def run_single_function(fnum, maxFEs=3e6, record_points=(300000, 1000000, 3000000),
                        verbose=False, save_groups_json_dir=None):
    """对单个函数执行 MDG 分解 + CHECC 优化，返回结果字典。"""
    maxFEs_int = int(maxFEs)
    record_points_int = [int(p) for p in record_points if int(p) <= maxFEs_int]

    bench = Benchmark()
    info = bench.get_info(fnum)
    fun = bench.get_function(fnum)

    D = int(info["dimension"])

    # --- 步骤1: MDG 分解 ---
    groups, decomp_fes, group_cs, group_stats = get_groups_with_mdg(fun, info, verbose)
    groups, vinfo = validate_and_fix_groups(groups, D)
    if verbose:
        print(f"  ✓ groups validated: covered={vinfo['covered_dims']}/{D}, missing={vinfo['missing_dims']}, dup={vinfo['has_duplicate']}")

    # 可选保存分组
    if save_groups_json_dir:
        os.makedirs(save_groups_json_dir, exist_ok=True)
        with open(os.path.join(save_groups_json_dir, f"F{fnum}_groups.json"), "w") as fp:
            json.dump(groups, fp)

    # --- 步骤2: 准备 CHECC 类实例 ---
    # 从 MDG 中获取 Deta（简化设为1，实际可根据分解结果计算）

    # 创建记录列表
    recorded = []   # 存储 (FEs, bestval)

    # 构建 cfg
    cfg = {
        'groups': groups,
        'maxFEs': maxFEs_int,
        'initial_FEs': decomp_fes,
        'Deta': group_cs,          # 向量形式
        'F': 0.5,
        'CR': 0.9,
        # 其他可选参数
    }

    def record_callback(current_fes, current_best):
        """记录指定 FEs 点的适应度"""
        # 确保 current_best 是标量（若为列表/数组则取第一个元素）
        if isinstance(current_best, (list, tuple, np.ndarray)):
            current_best = float(current_best[0])
        for target in record_points_int:
            if current_fes >= target and not any(rec[0] == target for rec in recorded):
                recorded.append([target, current_best])

    # 实例化 CHECC，传入分组、边界等
    checc = CHECC(fun=fun, info=info, cfg=cfg)
    checc.set_record_callback(record_callback)


    # print("run_single 开始优化")

    # --- 步骤3: 运行优化 ---
    final_best = checc.run()

    # print("run_single 优化完了")

    # 收集结果
    final_fes = checc.alg['FEs']
    best_fitness = checc.alg['bestval'][0]
    output_values = np.array(recorded) if recorded else np.empty((0, 2))

    # print("1")

    # 整理每个记录点的结果
    target_results = {}
    for target in record_points_int:
        mask = output_values[:, 0] == target
        if np.any(mask):
            idx = np.where(mask)[0][0]
            fit = output_values[idx, 1]
            target_results[target] = {
                'target_fes': target,
                'actual_fes': target,
                'fitness': fit,
                'reached': True
            }
        else:
            # 未精确记录，取最后一个小于等于目标的点
            valid = output_values[output_values[:, 0] <= target]
            if len(valid) > 0:
                last = valid[-1]
                target_results[target] = {
                    'target_fes': target,
                    'actual_fes': int(last[0]),
                    'fitness': last[1],
                    'reached': True
                }
            else:
                target_results[target] = {
                    'target_fes': target,
                    'actual_fes': target,
                    'fitness': best_fitness,
                    'reached': False
                }

    # print("2")

    return {
        'fnum': int(fnum),
        'group_n': len(groups),
        'nonsep_n': group_stats['nonsep_n'],
        'sep_n': group_stats['sep_n'],
        'decomp_fes': decomp_fes,
        'final_fes': final_fes,
        'best_fitness': best_fitness,
        'record_points': record_points_int,
        'target_results': target_results,
        'output_values': output_values.tolist()   # 转换为列表便于 JSON 序列化
    }


# ============================================================================
# 输出 CSV 汇总表
# ============================================================================
def write_summary_csv(path, rows, record_points):
    record_points = [int(p) for p in record_points]
    header = ["FuncID", "GroupN"] + [f"Best@FEs={p}" for p in record_points]
    with open(path, "w", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for r in rows:
            func = f"F{r['fnum']}"
            group_n = str(r['group_n'])
            vals = []
            for p in record_points:
                tr = r['target_results'].get(p, {})
                vals.append(f"{tr.get('fitness', np.nan):.12e}")
            f.write(",".join([func, group_n] + vals) + "\n")


# ============================================================================
# 主函数
# ============================================================================
def main():
    parser = argparse.ArgumentParser(description="CHECC + MDG on CEC2013 LSGO")
    parser.add_argument("--func_id", type=int, default=None,
                        help="Function ID (1-15). If omitted, run all.")
    parser.add_argument("--maxFEs", type=float, default=3e6,
                        help="Total max function evaluations (including decomposition).")
    parser.add_argument("--seed", type=int, default=None, help="Random seed.")
    parser.add_argument("--verbose", action="store_true", help="Verbose output.")
    parser.add_argument("--out_dir", type=str, default="./results_checc",
                        help="Output directory.")
    parser.add_argument("--save_groups", action="store_true",
                        help="Save groups as JSON per function.")
    args = parser.parse_args()

    if args.seed is not None:
        np.random.seed(args.seed)

    os.makedirs(args.out_dir, exist_ok=True)

    if args.func_id is not None:
        if not (1 <= args.func_id <= 15):
            raise ValueError("func_id must be in [1,15].")
        func_ids = [args.func_id]
        mode = f"F{args.func_id}"
    else:
        func_ids = list(range(1, 16))
        mode = "F1-F15"

    record_points = [300000, 1000000, 3000000]
    record_points = [p for p in record_points if p <= int(args.maxFEs)]

    print("\n" + "=" * 90)
    print(f"CHECC + MDG on CEC2013 LSGO | Mode={mode} | maxFEs={int(args.maxFEs)} | Seed={args.seed}")
    print(f"Record points: {record_points}")
    print("=" * 90)

    rows = []
    for i, fnum in enumerate(func_ids, 1):
        print(f"\n[{i:2d}/{len(func_ids)}] Running F{fnum} ...")
        try:
            r = run_single_function(
                fnum=fnum,
                maxFEs=args.maxFEs,
                record_points=record_points,
                verbose=args.verbose,
                save_groups_json_dir=os.path.join(args.out_dir, "groups") if args.save_groups else None
            )
            # print("优化完了")
            rows.append(r)
            # print("rows append")

            line = f"  ✓ F{fnum}: GroupN={r['group_n']}, FinalFEs={r['final_fes']}, Best={r['best_fitness']:.6e}"
            print(line)
            for p in record_points:
                tr = r['target_results'][p]
                print(f"    - FEs={p}: best={tr['fitness']:.6e} (actual={tr['actual_fes']}, reached={tr['reached']})")

        except Exception as e:
            print(f"  ✗ ERROR on F{fnum}: {e}")
            rows.append({
                'fnum': fnum,
                'group_n': -1,
                'target_results': {p: {'fitness': np.nan} for p in record_points}
            })

    print("开始写csv")
    # 写入 CSV 汇总
    summary_csv = os.path.join(args.out_dir, f"summary_{mode}.csv")
    write_summary_csv(summary_csv, rows, record_points)
    print("\n" + "=" * 90)
    print(f"Summary saved: {summary_csv}")
    print("=" * 90)

    # 控制台打印表格
    header = ["FuncID", "GroupN"] + [f"Best@{p}" for p in record_points]
    print("{:<6} {:<8} ".format(header[0], header[1]) + " ".join([f"{h:<18}" for h in header[2:]]))
    print("-" * 90)
    for r in rows:
        func = f"F{r['fnum']}"
        group_n = r.get("group_n", -1)
        vals = []
        for p in record_points:
            tr = r['target_results'].get(p, {})
            vals.append(f"{tr.get('fitness', np.nan):.6e}")
        print(f"{func:<6} {group_n:<8} " + " ".join([f"{v:<18}" for v in vals]))

    # 保存详细 JSON
    detail_json = os.path.join(args.out_dir, f"detail_{mode}.json")
    with open(detail_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"\nDetailed results saved: {detail_json}")
    print("=" * 90)


if __name__ == "__main__":
    main()