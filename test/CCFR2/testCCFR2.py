import argparse
import os
import sys
import numpy as np
import time

# 添加项目根目录到路径，确保能引用到 Algorithms 和 cec2013lsgo
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cec2013lsgo.cec2013 import Benchmark
from Algorithms.CC.CBCC.CCFR2.ccfr2 import CCFR2
from Algorithms.CC.VI_based_Dec.DG2.dg2 import DG2

def get_groups_with_dg2(fun, info, verbose=False):
    """
    使用 DG2 获取变量分组。
    
    1. 运行 DG2 获取邻接矩阵/列表
    2. 使用连通分量算法(Connected Components)将邻接关系转换为分组
    """
    if DG2 is None:
        raise ImportError("DG2 class not found. Cannot run decomposition.")

    D = info['dimension']
    
    # 1. 实例化并运行 DG2
    # ----------------------------------------------------
    # 基于你提供的 snippet
    dg2 = DG2(fun, info)
    
    # 获取 Interaction Structure Matrix (ISM) 和所需的评估次数
    # 注意：dg2.ism() 返回的具体参数根据你的实现可能略有不同，这里遵循你的描述
    # 假设返回: (structure_matrix, evaluations_count, lambda_threshold)
    _, evaluations, lambda_,decomp_fes = dg2.ism()
    
    # 获取 Dependency Structure Matrix (DSM) / Theta
    theta = dg2.dsm(evaluations, lambda_)
    
    
    # 2. 构建邻接表 (Adjacency List)
    # ----------------------------------------------------
    adjacency = []
    for i in range(D):
        # theta[i, j] == 1 表示 i 和 j 相互作用
        neighbors = [
        j for j in range(D)
        if j != i and (theta[i, j] == 1 or theta[j, i] == 1)
        ]
        adjacency.append(set(neighbors))
        
    # 3. 寻找连通分量 (Connected Components) 形成分组
    # ----------------------------------------------------
    groups = []
    visited = set()
    
    for i in range(D):
        if i not in visited:
            # 开始一个新的组 (BFS/DFS)
            current_group = []
            queue = [i]
            visited.add(i)
            
            while queue:
                node = queue.pop(0)
                current_group.append(node)
                
                # 遍历邻居
                for neighbor in adjacency[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            # 排序后加入结果，保持确定性
            current_group.sort()
            groups.append(current_group)

    # 统计信息
    # 分离出可分离变量（大小为1的组）和不可分离变量
    seps = [g[0] for g in groups if len(g) == 1]
    nonseps = [g for g in groups if len(g) > 1]

    if verbose:
        print(f"  ✓ DG2: {len(groups)} groups found, {decomp_fes} FEs consumed")
        print(f"    - Non-separable groups: {len(nonseps)} (Max size: {max([len(g) for g in nonseps]) if nonseps else 0})")
        print(f"    - Separable variables: {len(seps)}")

    return groups, decomp_fes

def run_single_function(fnum, maxFEs=3e6, use_dg2=True, verbose=False):
    """
    在单个函数上运行 CCFR2 (使用 DG2 分组)
    """
    # 初始化 benchmark
    bench = Benchmark()
    info = bench.get_info(fnum)
    fun = bench.get_function(fnum)
    info['fNum'] = fnum

    
    # 1. 获取分组 (Decomposition)
    decomp_fes = 0
    groups = []
    
    if use_dg2:
        try:
            start_time = time.time()
            groups, decomp_fes = get_groups_with_dg2(fun, info, verbose=verbose)
            if verbose:
                print(f"  Time for DG2: {time.time() - start_time:.2f}s")
        except Exception as e:
            print(f"  ✗ DG2 failed on F{fnum}: {e}")
            print("  → Falling back to default grouping (50-dim chunks)")
            use_dg2 = False

    # Fallback: 默认分组 (每50维一组)
    if not use_dg2 or not groups:
        D = info['dimension']
        group_size = 50
        groups = [list(range(i, min(i + group_size, D))) for i in range(0, D, group_size)]
        # 如果是 fallback，decomp_fes 设为 0 或者保持之前的错误消耗？通常设为0
        decomp_fes = 0
    
    # 2. 配置 CCFR2
    # 将分组存入 info，这是 CCFR2 读取的标准位置
    info['groups'] = groups
    
    cfg = {
        'maxFEs': int(maxFEs),
        'initial_fEvalNum': decomp_fes,  # 继承 DG2 消耗的 FEs
        'optimizer': 'CMAES',            # CCFR2 内部默认使用 CMAES
        'w': 0.1,                        # CCFR2 权重参数
        'GEs': 100,                      # CCFR2 每一轮进化的代数
        'verbose': verbose
    }
    
    # 3. 实例化并运行优化器
    optimizer = CCFR2(fun=fun, info=info, cfg=cfg)
    
    # 设置必须记录的 FEs 点 (用于统计表格)
    record_points = [int(1.2e5), int(6e5), int(3e6)] 
    # 注意: CEC2013标准通常看 1.2e5, 6.0e5, 3.0e6
    # 但你也用了 3e5, 1e6, 3e6。这里兼容你的 3e5, 1e6, 3e6 设置
    user_record_points = [int(3e5), int(1e6), int(3e6)]
    optimizer.alg['mustOutputPoints'] = np.asarray(user_record_points, dtype=int)
    
    optimizer.run()
    
    # 4. 提取结果
    output_values = optimizer.alg['outputValues']
    final_fes = int(output_values[-1, 0]) if output_values.shape[0] > 0 else decomp_fes
    best_fitness = float(optimizer.alg['bestGlobal']['f'])
    
    # 在目标 FEs 点获取结果
    target_results = {}
    for target_fes in user_record_points:
        if output_values is not None and len(output_values) > 0:
            # 找到 <= target_fes 的最近点，或者直接找最接近的点
            # 通常 outputValues 包含 exact points 如果我们在 mustOutputPoints 里设置了
            idx = np.abs(output_values[:, 0] - target_fes).argmin()
            
            # 简单检查：如果还没有运行到这个FE，取当前的
            curr_fes = output_values[idx, 0]
            if curr_fes > target_fes and idx > 0:
                 # 如果最近点比目标大，且有前一个点，取前一个? 
                 # 实际上 outputValues 是稀疏记录的。
                 pass
            
            fitness = float(output_values[idx, 1])
            actual_fes = int(output_values[idx, 0])
            
            # 如果还没运行到 target (例如 Early Stop), 使用最终结果填充
            if final_fes < target_fes:
                 fitness = best_fitness
                 actual_fes = final_fes
                 
            target_results[target_fes] = {
                'actual_fes': actual_fes,
                'fitness': fitness
            }
        else:
            target_results[target_fes] = {'actual_fes': final_fes, 'fitness': best_fitness}

    return {
        'fnum': fnum,
        'best_fitness': best_fitness,
        'final_fes': final_fes,
        'decomp_fes': decomp_fes,
        'opt_fes': final_fes - decomp_fes,
        'target_results': target_results,
        'groups_count': len(groups)
    }

def main():
    parser = argparse.ArgumentParser(
        description="CCFR2 with DG2 on CEC2013 LSGO Benchmark",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--func_id', type=int, default=None, help='Function ID (1-15). Run all if None.')
    parser.add_argument('--maxFEs', type=float, default=3e6, help='Maximum function evaluations')
    parser.add_argument('--no_dg2', action='store_true', help='Disable DG2 grouping (use default fixed grouping)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')
    parser.add_argument('--out_dir', type=str, default='./results_ccfr2_dg2', help='Output directory')
    
    args = parser.parse_args()
    
    if args.seed is not None:
        np.random.seed(args.seed)
        
    os.makedirs(args.out_dir, exist_ok=True)
    
    if args.func_id is not None:
        func_ids = [args.func_id]
        mode_str = f"F{args.func_id}"
    else:
        func_ids = list(range(1, 16))
        mode_str = "F1-F15"

    print("\n" + "="*80)
    print(f"CCFR2 with DG2 Decomposition - CEC2013 LSGO")
    print(f"Functions: {mode_str} | MaxFEs: {int(args.maxFEs):,}")
    print(f"Decomposition: {'DG2' if not args.no_dg2 else 'Fixed(50)'}")
    print("="*80)

    results_summary = []

    for fnum in func_ids:
        print(f"\n[{fnum}/15] Testing Function F{fnum}...")
        
        try:
            res = run_single_function(
                fnum=fnum,
                maxFEs=args.maxFEs,
                use_dg2=not args.no_dg2,
                verbose=args.verbose
            )
            
            tr = res['target_results']
            print(f"  ✓ Finished. Total FEs: {res['final_fes']:,} (Decomp: {res['decomp_fes']:,})")
            print(f"  → Best: {res['best_fitness']:.2e}")
            print(f"    3e5:  {tr[300000]['fitness']:.2e}")
            print(f"    1e6:  {tr[1000000]['fitness']:.2e}")
            print(f"    3e6:  {tr[3000000]['fitness']:.2e}")
            
            results_summary.append(res)
            
        except KeyboardInterrupt:
            print("\n  ! Interrupted by user.")
            break
        except Exception as e:
            print(f"  ✗ Critical Error on F{fnum}: {e}")
            import traceback
            traceback.print_exc()

    # --- Summary Table ---
    print("\n" + "="*95)
    print(f"{'Func':<5} {'DecompFEs':<10} {'Groups':<7} {'3e5':<12} {'1e6':<12} {'3e6 (Best)':<12}")
    print("-" * 95)
    
    summary_path = os.path.join(args.out_dir, f'summary_{mode_str}.txt')
    
    with open(summary_path, 'w') as f:
        f.write(f"CCFR2 + DG2 Results ({time.strftime('%Y-%m-%d %H:%M:%S')})\n")
        f.write("-" * 95 + "\n")
        f.write(f"{'Func':<5} {'DecompFEs':<10} {'Groups':<7} {'3e5':<12} {'1e6':<12} {'3e6':<12}\n")
        f.write("-" * 95 + "\n")
        
        for res in results_summary:
            tr = res['target_results']
            line = (f"F{res['fnum']:<4} "
                    f"{res['decomp_fes']:<10} "
                    f"{res['groups_count']:<7} "
                    f"{tr[300000]['fitness']:<12.2e} "
                    f"{tr[1000000]['fitness']:<12.2e} "
                    f"{tr[3000000]['fitness']:<12.2e}")
            
            print(line)
            f.write(line + "\n")

    print("="*95)
    print(f"Summary saved to: {summary_path}")

if __name__ == '__main__':
    main()