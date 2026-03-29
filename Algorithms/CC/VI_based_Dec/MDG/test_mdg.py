import numpy as np
import time
from cec2013lsgo.cec2013 import Benchmark
from Algorithms.CC.VI_based_Dec.MDG.mdg import MDG

def test_mdg_on_cec2013():
    bench = Benchmark()
    func_ids = range(1, 16)
    
    header = f"{'Func':<5} {'Dim':<6} {'TotalFEs':<10} {'Seps':<6} {'NonSepGroups':<12} {'GroupSizes':<20} {'Time(s)':<8}"
    print("=" * 85)
    print("MDG Decomposition Test on CEC2013 LSGO")
    print("=" * 85)
    print(header)
    print("-" * 85)

    results = []

    for fnum in func_ids:
        info = bench.get_info(fnum)
        fun = bench.get_function(fnum)
        
        # --- 修正点：将 base 设为标量 ---
        # 报错是因为原代码试图将数组赋给 p2[i]
        # 根据你的 mdg.py 逻辑，这里传入 lb (float) 即可
        lb = info['lower']
        ub = info['upper']
        cfg = {
            'base': float(lb),  # 强制转换为 Python 标量浮点数
            'sigma': (ub - lb) * 1e-3 
        }

        start_time = time.time()
        mdg_engine = MDG(fun, info, cfg) 
        subspaces = mdg_engine.decompose() 
        elapsed = time.time() - start_time
        
        # --- 结果分析 ---
        seps = subspaces['seps']
        nonseps = subspaces['nonseps']
        # 修正属性名：使用 mdg.py 中定义的 self.FEs
        fes_used = mdg_engine.FEs 
        
        num_seps = len(seps)
        num_nonsep_groups = len(nonseps)
        
        if num_nonsep_groups > 0:
            sizes = [len(g) for g in nonseps]
            size_str = f"{min(sizes)}-{max(sizes)} (avg:{np.mean(sizes):.1f})"
        else:
            size_str = "N/A"

        # 打印结果
        print(f"F{fnum:<4} {info['dimension']:<6} {fes_used:<10} {num_seps:<6} {num_nonsep_groups:<12} {size_str:<20} {elapsed:<8.2f}")
        
        results.append({
            'fnum': fnum,
            'fes': fes_used,
            'seps': seps,
            'nonseps': nonseps,
            'group_cs': subspaces.get('group_cs', []),
            'elapsed': elapsed
        })

    print("-" * 85)
    return results

if __name__ == "__main__":
    all_results = test_mdg_on_cec2013()
    
    if all_results:
        f1_res = all_results[0]
        all_groups_for_checc = f1_res['nonseps'] + [[s] for s in f1_res['seps']]
        print(f"\n[Tips] 分解完成。F1 共有 {len(all_groups_for_checc)} 个组。")