import argparse
import os
import sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cec2013lsgo.cec2013 import Benchmark

from Algorithms.CC.VI_based_Dec.ERDG.erdg import ERDG
from Algorithms.CC.CBCC.CCFR2_AEPD.ccfr2_aepd import CCFR2_AEPD


def get_groups_with_erdg(fun, info, max_fe_for_erdg=100000, verbose=False):
    """
    使用ERDG获取变量分组
    
    Parameters
    ----------
    fun : callable
        目标函数
    info : dict
        问题信息
    max_fe_for_erdg : int
        ERDG最大评估次数
    verbose : bool
        是否打印详细信息
        
    Returns
    -------
    groups : list of lists
        变量分组列表
    decomp_fes : int
        ERDG消耗的评估次数
    """
    # 配置ERDG
    erdg_cfg = {
        'maxFEs': max_fe_for_erdg,
        'verbose': False
    }
    
    # 运行ERDG分解
    erdg = ERDG(fun, info, erdg_cfg)
    subspaces = erdg.decompose()
    decomp_fes = erdg.counter
    
    # 转换分组格式：从ERDG格式到CCFR2-AEPD格式
    # ERDG返回: {'seps': [i1, i2, ...], 'nonseps': [[...], [...]]}
    # CCFR2-AEPD需要: [[...], [...], [i1], [i2], ...]
    groups = []
    
    # 添加非可分离组
    for group in subspaces['nonseps']:
        groups.append(group)
    
    # 添加可分离变量（每个变量单独成组）
    for var_idx in subspaces['seps']:
        groups.append([var_idx])
    
    if verbose:
        print(f"  ✓ ERDG: {len(groups)} groups, {decomp_fes} FEs")
        print(f"    - Non-separable groups: {len(subspaces['nonseps'])}")
        print(f"    - Separable variables: {len(subspaces['seps'])}")
    
    return groups, decomp_fes


def run_single_function(fnum, maxFEs=3e6, use_erdg=True, verbose=False):
    """
    在单个函数上运行CCFR2-AEPD
    
    Returns
    -------
    dict
        包含完整结果和统计信息
    """
    # 初始化benchmark
    bench = Benchmark()
    info = bench.get_info(fnum)
    fun = bench.get_function(fnum)
    info['fNum'] = fnum
    
    # 获取分组
    if use_erdg:
        try:
            groups, decomp_fes = get_groups_with_erdg(
                fun, info, max_fe_for_erdg=min(100000, int(maxFEs*0.05)), verbose=verbose
            )
        except Exception as e:
            print(f"  ✗ ERDG failed on F{fnum}: {e}")
            print("  → Falling back to default grouping")
            use_erdg = False
    
    # 默认分组（每50维一组）
    if not use_erdg:
        D = info['dimension']
        group_size = 50
        groups = [list(range(i, min(i + group_size, D))) for i in range(0, D, group_size)]
        decomp_fes = 0
    
    # 将分组添加到info（CCFR2-AEPD从info读取groups）
    info['groups'] = groups
    
    # 配置CCFR2-AEPD
    cfg = {
        'maxFEs': int(maxFEs),
        'initial_fEvalNum': decomp_fes,  # 继承ERDG消耗的FEs
        'optimizer': 'CMAES',
        'verbose': verbose
    }
    
    # 实例化并运行
    optimizer = CCFR2_AEPD(fun=fun, info=info, cfg=cfg)
    
    # 设置必须记录的FEs点
    record_points = [int(3e5), int(1e6), int(3e6)]
    optimizer.alg['mustOutputPoints'] = np.asarray(record_points, dtype=int)

    
    # 运行优化
    optimizer.run()
    
    # 提取结果
    output_values = optimizer.alg['outputValues']
    final_fes = int(output_values[-1, 0])
    best_fitness = float(output_values[-1, 1])
    
    # 在目标FEs点获取结果
    target_results = {}
    for target_fes in record_points:
        if target_fes <= final_fes:
            # 找到最接近的记录点
            idx = np.abs(output_values[:, 0] - target_fes).argmin()
            actual_fes = int(output_values[idx, 0])
            fitness = float(output_values[idx, 1])
            target_results[target_fes] = {
                'actual_fes': actual_fes,
                'fitness': fitness,
                'reached': True
            }
        else:
            # 未达到目标FEs
            target_results[target_fes] = {
                'actual_fes': final_fes,
                'fitness': best_fitness,
                'reached': False
            }
    
    return {
        'fnum': fnum,
        'best_fitness': best_fitness,
        'final_fes': final_fes,
        'decomp_fes': decomp_fes,
        'opt_fes': final_fes - decomp_fes,
        'target_results': target_results,
        'output_values': output_values,
        'groups': groups
    }


def main():
    parser = argparse.ArgumentParser(
        description="CCFR2-AEPD with ERDG on CEC2013 LSGO Benchmark",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--func_id', type=int, default=None,
        help='Function ID (1-15). If not specified, runs all functions.'
    )
    parser.add_argument(
        '--maxFEs', type=float, default=3e6,
        help='Maximum function evaluations'
    )
    parser.add_argument(
        '--no_erdg', action='store_true',
        help='Disable ERDG grouping (use default grouping)'
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='Enable verbose output during optimization'
    )
    parser.add_argument(
        '--out_dir', type=str, default='./results_ccfr2_aepd',
        help='Output directory for results'
    )
    parser.add_argument(
        '--seed', type=int, default=None,
        help='Random seed for reproducibility'
    )
    
    args = parser.parse_args()
    
    if args.seed is not None:
        np.random.seed(args.seed)
    
    os.makedirs(args.out_dir, exist_ok=True)
    
    if args.func_id is not None:
        if not 1 <= args.func_id <= 15:
            raise ValueError("func_id must be between 1 and 15")
        func_ids = [args.func_id]
        mode = f"F{args.func_id}"
    else:
        func_ids = list(range(1, 16))
        mode = "F1-F15"
    
    all_results = {}
    
    print("\n" + "="*80)
    print(f"CCFR2-AEPD with ERDG on CEC2013 LSGO")
    print(f"Mode: {mode} | MaxFEs: {int(args.maxFEs)} | ERDG: {'Enabled' if not args.no_erdg else 'Disabled'}")
    if args.seed is not None:
        print(f"Random seed: {args.seed}")
    print("="*80)
    
    for idx, fnum in enumerate(func_ids, 1):
        print(f"\n[{idx:2d}/{len(func_ids)}] Testing F{fnum}...")
        
        try:
            result = run_single_function(
                fnum=fnum,
                maxFEs=args.maxFEs,
                use_erdg=not args.no_erdg,
                verbose=args.verbose
            )
            
            all_results[fnum] = result
            
            # 显示简要结果
            tr = result['target_results']
            print(f"  ✓ Total FEs: {result['final_fes']:,} "
                  f"(Decomp: {result['decomp_fes']:,}, Opt: {result['opt_fes']:,})")
            print(f"  → Best: {result['best_fitness']:.6e}")
            print(f"    3e5:  {tr[300000]['fitness']:.6e} (FEs: {tr[300000]['actual_fes']:,})")
            print(f"    1e6:  {tr[1000000]['fitness']:.6e} (FEs: {tr[1000000]['actual_fes']:,})")
            print(f"    3e6:  {tr[3000000]['fitness']:.6e} (FEs: {tr[3000000]['actual_fes']:,})")
            
        except Exception as e:
            print(f"  ✗ ERROR on F{fnum}: {e}")
            import traceback
            traceback.print_exc()
            all_results[fnum] = {'error': str(e)}
    
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    
    header = f"{'Func':<6} {'DecompFEs':<10} {'TotalFEs':<10} {'3e5':<14} {'1e6':<14} {'3e6':<14}"
    print(header)
    print("-"*80)
    
    summary_content = [
        "CCFR2-AEPD on CEC2013 LSGO Summary\n",
        "="*80 + "\n",
        f"Config: MaxFEs={int(args.maxFEs)}, ERDG={'Enabled' if not args.no_erdg else 'Disabled'}, Seed={args.seed}\n",
        "-"*80 + "\n",
        header + "\n",
        "-"*80 + "\n"
    ]
    
    for fnum in func_ids:
        result = all_results.get(fnum, {})
        
        if 'error' in result:
            line = f"F{fnum:<4} {'ERROR':<10} {'ERROR':<10} {'N/A':<14} {'N/A':<14} {'N/A':<14}"
        else:
            tr = result['target_results']
            line = (f"F{fnum:<4} {result['decomp_fes']:<10} {result['final_fes']:<10} "
                    f"{tr[300000]['fitness']:<14.6e} "
                    f"{tr[1000000]['fitness']:<14.6e} "
                    f"{tr[3000000]['fitness']:<14.6e}")
        
        print(line)
        summary_content.append(line + "\n")
    
    summary_file = os.path.join(args.out_dir, f"summary_{mode}.txt")
    with open(summary_file, 'w') as f:
        f.writelines(summary_content)
    print(f"\n✓ Text summary saved to: {summary_file}")
    
    try:
        detail_file = os.path.join(args.out_dir, f"detail_{mode}.npz")
        save_dict = {}
        for fnum, result in all_results.items():
            if 'error' not in result:
                save_dict[f'F{fnum}_output'] = result['output_values']
                save_dict[f'F{fnum}_best_fitness'] = result['best_fitness']
                save_dict[f'F{fnum}_final_fes'] = result['final_fes']
                save_dict[f'F{fnum}_decomp_fes'] = result['decomp_fes']
                save_dict[f'F{fnum}_groups'] = result['groups']
        if save_dict:
            np.savez_compressed(detail_file, **save_dict)
            print(f"✓ Detailed results saved to: {detail_file}")
    except Exception as e:
        print(f"⚠️  Failed to save detailed results: {e}")
    
    print("\n" + "="*80)
    print("Testing completed!")
    print("="*80)


if __name__ == '__main__':
    main()