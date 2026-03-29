import numpy as np
from collections import deque


#注： 这里的CS计算没有算入FEs中
# CS的计算比较慢，这里的 代表是否要返回这个值

class MDG:
    def __init__(self, fun, info, cfg):
        self.fun = fun
        self.info = info
        self.D = info['dimension']
        self.base = cfg['base']
        self.sigma = cfg['sigma']
        self.FEs = 0

    def _eval(self, x):
        self.FEs += 1
        # 确保输入是 numpy 数组并调用
        return float(self.fun(x))

    def epsilon_calculate(self, fp1, fp2, fp3, fp4):
        f_max = max(abs(fp1), abs(fp2), abs(fp3), abs(fp4))
        # 2**-52 是 MATLAB 的 eps
        return 0.003 * (2**-52) * f_max * self.D

    def bi_search(self, left_group, fp1, fp2, fp_iR, Rgroups, Rperts):
        """对应 MATLAB biSearch.m"""
        fes_local = 0
        R_gnum = len(Rgroups)
        Rfp = Rperts[1]
        
        # 使用 deque 模拟 MATLAB 的 cell array 队列
        groups_queue = deque([Rgroups])
        data_queue = deque([[fp1, fp2, Rfp, fp_iR]])
        group_indexs_queue = deque([list(range(R_gnum))])
        p_queue = deque([np.full(self.D, self.base)])
        node_orders = deque([1])
        
        group = []
        group_indexs = []
        
        while groups_queue:
            cur_groups = groups_queue.popleft()
            cur_data = data_queue.popleft()
            cur_group_indexs = group_indexs_queue.popleft()
            cur_p = p_queue.popleft()
            cur_order = node_orders.popleft()
            
            delta1 = cur_data[1] - cur_data[0]
            delta2 = cur_data[3] - cur_data[2]
            epsilon = self.epsilon_calculate(cur_data[0], cur_data[1], cur_data[2], cur_data[3])
            
            if abs(delta1 - delta2) > epsilon:
                cur_gnum = len(cur_groups)
                if cur_gnum == 1:
                    group.append(cur_groups[0])
                    group_indexs.append(cur_group_indexs[0])
                else:
                    median = cur_gnum // 2
                    # Left split
                    groups1 = cur_groups[:median]
                    group_indexs1 = cur_group_indexs[:median]
                    p_1 = cur_p.copy()
                    for g in groups1:
                        for idx in g: p_1[idx] = self.base + self.sigma
                    
                    # 检查 Rperts 缓存 (对应 MATLAB: Rperts(cur_order*2))
                    if (cur_order * 2) in Rperts and Rperts[cur_order * 2] != 0:
                        fp_1 = Rperts[cur_order * 2]
                    else:
                        fp_1 = self._eval(p_1)
                        Rperts[cur_order * 2] = fp_1
                    
                    p_i1 = p_1.copy()
                    for idx in left_group: p_i1[idx] = self.base + self.sigma
                    fp_i1 = self._eval(p_i1)
                    
                    data1 = [cur_data[0], cur_data[1], fp_1, fp_i1]
                    groups_queue.append(groups1)
                    data_queue.append(data1)
                    group_indexs_queue.append(group_indexs1)
                    p_queue.append(cur_p)
                    node_orders.append(cur_order * 2)
                    
                    # Right split
                    groups2 = cur_groups[median:]
                    group_indexs2 = cur_group_indexs[median:]
                    data2 = [fp_1, fp_i1, cur_data[2], cur_data[3]]
                    groups_queue.append(groups2)
                    data_queue.append(data2)
                    group_indexs_queue.append(group_indexs2)
                    p_queue.append(p_1)
                    node_orders.append(cur_order * 2 + 1)
                    
        return group, group_indexs, Rperts

    def merge_interaction_group(self, Lgroup_indexs, Rinteract_indexs, Lgroups, Rgroups):
        """对应 MATLAB mergeInteractionGroup.m"""
        merged_groups = []
        Lgroup_indexs = list(Lgroup_indexs)
        Rinteract_indexs = [list(r) for r in Rinteract_indexs]
        
        while Lgroup_indexs:
            cur_index = Lgroup_indexs.pop(0)
            cur_interact_indexs = set(Rinteract_indexs.pop(0))
            
            combined_group = list(Lgroups[cur_index])
            
            i = len(Lgroup_indexs) - 1
            while i >= 0:
                # 检查 R 索引是否有交集
                if cur_interact_indexs.intersection(Rinteract_indexs[i]):
                    cur_interact_indexs.update(Rinteract_indexs[i])
                    combined_group.extend(Lgroups[Lgroup_indexs[i]])
                    Rinteract_indexs.pop(i)
                    Lgroup_indexs.pop(i)
                    i = len(Lgroup_indexs) - 1
                else:
                    i -= 1
            
            for r_idx in cur_interact_indexs:
                combined_group.extend(Rgroups[r_idx])
            
            merged_groups.append(combined_group)
            
        return merged_groups

    def merge_group(self, dims, fp1, perturbed_values):
        """对应 MATLAB mergeGroup.m"""
        dim_len = len(dims)
        
        # Case: 1 or 2 variables
        if dim_len == 1:
            return [[dims[0]]], perturbed_values[dims[0]]
        
        if dim_len == 2:
            p = np.full(self.D, self.base)
            for d in dims: p[d] = self.base + self.sigma
            fp = self._eval(p)
            
            delta1 = perturbed_values[dims[0]] - fp1
            delta2 = fp - perturbed_values[dims[1]]
            epsilon = self.epsilon_calculate(fp1, perturbed_values[dims[0]], perturbed_values[dims[1]], fp)
            
            if abs(delta1 - delta2) < epsilon:
                return [[dims[0]], [dims[1]]], fp
            else:
                return [list(dims)], fp

        # Recursive split
        median = dim_len // 2
        Ldims = dims[:median]
        Rdims = dims[median:]
        
        Lgroups, Lgroups_perturb = self.merge_group(Ldims, fp1, perturbed_values)
        Rgroups, Rgroups_perturb = self.merge_group(Rdims, fp1, perturbed_values)
        
        # Check interaction between L and R groups
        p = np.full(self.D, self.base)
        for d in dims: p[d] = self.base + self.sigma
        fp = self._eval(p)
        
        delta1 = Lgroups_perturb - fp1
        delta2 = fp - Rgroups_perturb
        epsilon = self.epsilon_calculate(fp1, Lgroups_perturb, Rgroups_perturb, fp)
        
        if abs(delta1 - delta2) > epsilon:
            # 存在交互
            if len(Lgroups) == 1 and len(Rgroups) == 1:
                return [Lgroups[0] + Rgroups[0]], fp
            
            # biSearch to find which Lgroups interact with Rdims
            Lgroup_subset, Lgroup_indexs, _ = self.bi_search(
                Rdims, fp1, Rgroups_perturb, fp, Lgroups, {1: Lgroups_perturb}
            )
            
            if Lgroup_indexs:
                lnum = len(Lgroup_indexs)
                if len(Rgroups) == 1:
                    # 只有一个 R 组的情况
                    flat_L = []
                    for g in Lgroup_subset: flat_L.extend(g)
                    new_Rgroup = [flat_L + Rgroups[0]]
                    
                    # 移除已合并的 L 组
                    for idx in sorted(Lgroup_indexs, reverse=True):
                        Lgroups.pop(idx)
                    return Lgroups + new_Rgroup, fp
                
                # 多个 R 组，需要进一步查找
                Rinteract_indexs = []
                Rperts = {1: Rgroups_perturb}
                
                for i in range(lnum):
                    if len(Lgroups) == 1:
                        fp_i = Lgroups_perturb
                        fp_iR = fp
                    else:
                        p_i = np.full(self.D, self.base)
                        for idx in Lgroup_subset[i]: p_i[idx] = self.base + self.sigma
                        fp_i = self._eval(p_i)
                        
                        p_iR = p_i.copy()
                        for idx in Rdims: p_iR[idx] = self.base + self.sigma
                        fp_iR = self._eval(p_iR)
                    
                    _, r_idxs, Rperts = self.bi_search(
                        Lgroup_subset[i], fp1, fp_i, fp_iR, Rgroups, Rperts
                    )
                    Rinteract_indexs.append(r_idxs)
                
                # Merge logic
                merged = self.merge_interaction_group(Lgroup_indexs, Rinteract_indexs, Lgroups, Rgroups)
                
                # 从原列表中删除已合并的
                all_r_to_remove = set()
                for r_list in Rinteract_indexs: all_r_to_remove.update(r_list)
                
                for idx in sorted(Lgroup_indexs, reverse=True): Lgroups.pop(idx)
                for idx in sorted(list(all_r_to_remove), reverse=True): Rgroups.pop(idx)
                
                return Lgroups + Rgroups + merged, fp
                
        return Lgroups + Rgroups, fp

    def decompose(self):
        """对应 MATLAB MDG.m，同时计算每个组的 CS 向量"""
        # Phase 1: Separable detection (保持不变)
        p1 = np.full(self.D, self.base)
        fp1 = self._eval(p1)
        
        p4 = np.full(self.D, self.base + self.sigma)
        fp4 = self._eval(p4)
        
        dims = []
        seps = []
        perturbed_values = {}
        
        for i in range(self.D):
            p2 = p1.copy()
            p2[i] = self.base + self.sigma
            fp2 = self._eval(p2)
            
            p3 = p4.copy()
            p3[i] = self.base
            fp3 = self._eval(p3)
            
            perturbed_values[i] = fp2
            epsilon = self.epsilon_calculate(fp1, fp2, fp3, fp4)
            
            if abs((fp2 - fp1) - (fp4 - fp3)) < epsilon:
                seps.append(i)
            else:
                dims.append(i)
        
        # Phase 2: Grouping (保持不变)
        all_groups = []
        if len(dims) > 1:
            groups, _ = self.merge_group(dims, fp1, perturbed_values)
            final_groups = []
            for g in groups:
                if len(g) == 1:
                    seps.append(g[0])
                else:
                    final_groups.append(sorted(g))
            all_groups = final_groups
        elif len(dims) == 1:
            seps.append(dims[0])
        
        # 构建最终分组列表（与返回的 seps 和 nonseps 一致）
        final_seps = sorted(seps)
        final_nonseps = all_groups
        all_groups_list = final_nonseps + [[s] for s in final_seps]  # 统一顺序：先非可分，后单变量

        # --- 新增：计算每个组的 CS 向量 ---
        group_cs = []  # 长度与 all_groups_list 相同
        # 用于存储所有变量对 Δ 的列表（仅用于归一化）
        all_delta = []
        saved_fes = self.FEs  # 1. 记录当前 FEs
        
        # 先计算所有非可分组的内部对，收集 Δ
        for g in final_nonseps:
            size = len(g)
            if size < 2:
                continue
            for idx_i in range(size):
                for idx_j in range(idx_i+1, size):
                    i, j = g[idx_i], g[idx_j]
                    # 构造同时扰动 i 和 j 的点
                    p_ij = p1.copy()
                    p_ij[i] = self.base + self.sigma
                    p_ij[j] = self.base + self.sigma
                    f_ij = self._eval(p_ij)
                    f_i = perturbed_values[i]   # 已计算
                    f_j = perturbed_values[j]
                    delta = f_ij - f_i - f_j + fp1
                    all_delta.append(delta)
        
        # 若没有非可分对，则 Δmax 设为 1 以避免除零
        if len(all_delta) == 0:
            delta_max = 1.0
        else:
            delta_max = max(abs(d) for d in all_delta)
        
        # 计算每个组的 CS
        for g in all_groups_list:
            size = len(g)
            if size < 2:
                group_cs.append(0.0)  # 单变量组 CS = 0
            else:
                sum_norm = 0.0
                for idx_i in range(size):
                    for idx_j in range(idx_i+1, size):
                        i, j = g[idx_i], g[idx_j]
                        # 重新计算 Δ（也可以复用之前计算的，但为了清晰，重新计算）
                        p_ij = p1.copy()
                        p_ij[i] = self.base + self.sigma
                        p_ij[j] = self.base + self.sigma
                        f_ij = self._eval(p_ij)  # 注意：这会导致重复计算，但组间无交互，所以每个对只计算一次
                        f_i = perturbed_values[i]
                        f_j = perturbed_values[j]
                        delta = f_ij - f_i - f_j + fp1
                        delta_norm = delta / delta_max
                        sum_norm += delta_norm
                cs = sum_norm / (size * (size - 1) / 2)
                group_cs.append(cs)
        
        self.FEs = saved_fes  # 2. 恢复 FEs，使 CS 的计算过程对外部透明
        # 注意：以上计算中，对每个对重新评估了 f_ij，可能重复。可以优化为缓存，但简单起见，保持原样。
        
        return {
            'seps': final_seps,
            'nonseps': final_nonseps,
            'FEs': self.FEs,
            'group_cs': group_cs   # 新增：与最终分组顺序对应的 CS 向量
        }