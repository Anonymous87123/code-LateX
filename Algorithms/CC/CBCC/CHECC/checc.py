import numpy as np
from scipy.linalg import eigh

# ==========================================
# 工具函数
# ==========================================

def SetPopSizeForGroups(groups):
    return np.array([len(g) + 25 for g in groups], dtype=int)

def Selection_Probability(pher, HI, group_num, alpha, beta):
    temp = (pher ** alpha) * (HI ** beta)
    return temp / (np.sum(temp) + 1e-100)

def Roulette_Selection(probability, group_num):
    cumulative_prob = np.cumsum(probability)
    return min(np.searchsorted(cumulative_prob, np.random.rand()), group_num - 1)

# ==========================================
# 核心演化逻辑 (Algorithm 1)
# ==========================================

def Subproblem_Optimization(group_index, groups, prob, alg, optimizer_func):
    """子问题优化逻辑：包含停止准则与贡献度计算"""
    f_start = alg['bestval'][0]
    fes_start = alg['FEs']
    
    # 记录初始贡献度
    prebestval = alg['bestval'][0]
    optimizer_func(group_index) # 演化第一代
    bestval_new = alg['bestval'][0]
    
    delta_C_pre = (prebestval - bestval_new) / (abs(prebestval) + 1e-100)
    prebestval = bestval_new
    count = 0

    while alg['FEs'] < alg['MaxFEs']:
        optimizer_func(group_index) # 演化下一代
        bestval_new = alg['bestval'][0]
        
        delta_C_current = (prebestval - bestval_new) / (abs(prebestval) + 1e-100)
        
        # 论文停止条件：效率下降或长时间无改进
        if delta_C_pre > delta_C_current: break
        if delta_C_current <= 0: count += 1
        else: count = 0
            
        if count >= prob['count_num']: break
            
        delta_C_pre = delta_C_current
        prebestval = bestval_new

    fes_used = alg['FEs'] - fes_start
    if fes_used <= 0: return 0
    
    # 核心公式 (Eq. 11): 归一化改进量
    deltaFitFinal = (f_start - alg['bestval'][0]) / (abs(f_start) * fes_used + 1e-100)
    return max(0, deltaFitFinal)

# ==========================================
# CHECC 类：集成带记忆的 CMA-ES
# ==========================================

class CHECC:
    def __init__(self, fun, info, cfg):
        self.fun = fun
        self.D = info['dimension']
        self.lb = np.full(self.D, info['lower'])
        self.ub = np.full(self.D, info['upper'])
        
        self.alg = {
            'FEs': int(cfg.get('initial_FEs', 0)),
            'MaxFEs': int(cfg.get('maxFEs', 3e6)),
            'bestval': [float('inf')],
            'bestIndividual': None
        }
        
        self.prob = {
            'D': self.D, 'groups': cfg['groups'], 
            'rho': cfg.get('rho', 0.8), 'Omega': cfg.get('Omega', 0.8),
            'alpha': cfg.get('alpha', 2), 'beta': cfg.get('beta', 1),
            'count_num': cfg.get('count_num', 20),
            'Deta': np.asarray(cfg['Deta'])
        }
        
        # 为每个 Group 初始化独立的 CMA-ES 状态 (对应 MATLAB 的 evolState_group)
        self.group_states = [self._init_cma_state(len(g), g) for g in self.prob['groups']]
        self.record_callback = None

    def _init_cma_state(self, n, dims):
        """初始化单组 CMA-ES 状态变量"""
        # 选择参数
        sublambda = 4 + int(3 * np.log(n))
        mu = sublambda // 2
        weights = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1))
        weights /= np.sum(weights)
        mueff = (np.sum(weights)**2) / np.sum(weights**2)
        
        # 适应参数
        cc = (4 + mueff/n) / (n + 4 + 2*mueff/n)
        cs = (mueff + 2) / (n + mueff + 5)
        c1 = 2 / ((n + 1.3)**2 + mueff)
        cmu = min(1 - c1, 2 * (mueff - 2 + 1/mueff) / ((n + 2)**2 + mueff))
        damps = 1 + 2 * max(0, np.sqrt((mueff - 1)/(n + 1)) - 1) + cs
        
        return {
            'first': True,
            'n': n, 'dims': dims,
            'sublambda': sublambda, 'mu': mu, 'weights': weights, 'mueff': mueff,
            'cc': cc, 'cs': cs, 'c1': c1, 'cmu': cmu, 'damps': damps,
            'xmean': (self.lb[dims] + self.ub[dims]) / 2.0,
            'sigma': 0.3 * (self.ub[dims] - self.lb[dims]),
            'pc': np.zeros(n), 'ps': np.zeros(n),
            'B': np.eye(n), 'D': np.ones(n), 'C': np.eye(n),
            'invsqrtC': np.eye(n), 'eigeneval': 0, 'counteval': 0,
            'chiN': n**0.5 * (1 - 1/(4*n) + 1/(21*n**2))
        }

    def _eval_wrapper(self, x_group, dims):
        """将子问题解拼接到全局最优解中进行评价"""
        if self.alg['FEs'] >= self.alg['MaxFEs']:
            return self.alg['bestval'][0]
        
        # 复制当前的全局最优解作为上下文
        full_x = self.alg['bestIndividual'].copy()
        full_x[dims] = x_group # 替换当前子问题的维度
        
        fit = float(self.fun(full_x))
        self.alg['FEs'] += 1
        
        if fit < self.alg['bestval'][0]:
            self.alg['bestval'][0] = fit
            self.alg['bestIndividual'] = full_x
            
        if self.record_callback:
            self.record_callback(self.alg['FEs'], self.alg['bestval'])
        return fit

    def _cmaes_step(self, group_idx):
        """执行指定 Group 的一代 CMA-ES 演化"""
        s = self.group_states[group_idx]
        n, dims = s['n'], s['dims']
        lb, ub = self.lb[dims], self.ub[dims]
        
        # 1. 生成并评价种群
        arx = np.zeros((s['sublambda'], n))
        arfitness = np.zeros(s['sublambda'])
        
        for k in range(s['sublambda']):
            # 抽样并边界约束 (对齐 MATLAB 逻辑)
            for _ in range(100): # 最多尝试 100 次以满足边界
                hz = np.random.randn(n)
                delta = s['sigma'] * (s['B'] @ (s['D'] * hz))
                x_k = s['xmean'] + delta
                if np.all(x_k >= lb) and np.all(x_k <= ub):
                    break
                x_k = np.clip(x_k, lb, ub)
            
            arx[k] = x_k
            arfitness[k] = self._eval_wrapper(x_k, dims)
        
        s['counteval'] += s['sublambda']
        
        # 2. 排序与更新均值
        arindex = np.argsort(arfitness)
        xold = s['xmean'].copy()
        s['xmean'] = weights_dot = s['weights'] @ arx[arindex[:s['mu']]]
        
        # 3. 更新演化路径 (ps, pc)
        y = (s['xmean'] - xold) / s['sigma']
        z = s['invsqrtC'] @ y
        s['ps'] = (1 - s['cs']) * s['ps'] + np.sqrt(s['cs']*(2 - s['cs']) * s['mueff']) * z
        
        hsig = (np.linalg.norm(s['ps']) / np.sqrt(1 - (1 - s['cs'])**(2 * s['counteval']/s['sublambda'])) / s['chiN'] 
                < 1.4 + 2/(n + 1))
        
        s['pc'] = (1 - s['cc']) * s['pc'] + hsig * np.sqrt(s['cc']*(2 - s['cc']) * s['mueff']) * y
        
        # 4. 更新协方差矩阵 C
        artmp = (arx[arindex[:s['mu']]] - xold) / s['sigma']
        s['C'] = ((1 - s['c1'] - s['cmu']) * s['C'] + 
                  s['c1'] * (np.outer(s['pc'], s['pc']) + (1 - hsig) * s['cc']*(2 - s['cc']) * s['C']) + 
                  s['cmu'] * (artmp.T @ np.diag(s['weights']) @ artmp))
        
        # 5. 更新步长 sigma
        s['sigma'] *= np.exp((s['cs'] / s['damps']) * (np.linalg.norm(s['ps']) / s['chiN'] - 1))
        
        # 6. 定期进行特征分解 (保持数值稳定)
        if s['counteval'] - s['eigeneval'] > s['sublambda'] / (s['c1'] + s['cmu']) / n / 10:
            s['eigeneval'] = s['counteval']
            s['C'] = np.triu(s['C']) + np.triu(s['C'], 1).T # 强制对称
            ev, s['B'] = eigh(s['C'])
            s['D'] = np.sqrt(np.maximum(1e-18, ev))
            s['invsqrtC'] = s['B'] @ np.diag(1.0 / s['D']) @ s['B'].T

    def run(self):
        groupN = len(self.prob['groups'])
        
        # 1. 初始全局最优解随机化
        self.alg['bestIndividual'] = np.random.uniform(self.lb, self.ub)
        # 评价一次初始解以获取初始 bestval
        fit_init = float(self.fun(self.alg['bestIndividual']))
        self.alg['bestval'][0] = fit_init
        self.alg['FEs'] = 1
        
        # 2. 计算启发式信息 HI (Eq. 10)
        dim_num = np.array([len(g) for g in self.prob['groups']])
        dim_rate = dim_num / self.D
        dim_rate /= (np.max(dim_rate) + 1e-100)
        HI = self.prob['Omega'] * self.prob['Deta'] + (1 - self.prob['Omega']) * dim_rate
        
        # 3. 初始轮次演化
        Contri = np.ones(groupN)
        for i in range(groupN):
            Contri[i] = self.prob['rho'] * Contri[i] + Subproblem_Optimization(
                i, self.prob['groups'], self.prob, self.alg, self._cmaes_step)
            if self.alg['FEs'] >= self.alg['MaxFEs']: break

        # 4. 主循环：基于贡献度的资源分配
        while self.alg['FEs'] < self.alg['MaxFEs']:
            pher = Contri / (np.max(Contri) + 1e-40)
            prob_sel = Selection_Probability(pher, HI, groupN, self.prob['alpha'], self.prob['beta'])
            idx = Roulette_Selection(prob_sel, groupN)
            
            deltaFit = Subproblem_Optimization(idx, self.prob['groups'], self.prob, self.alg, self._cmaes_step)
            Contri[idx] = self.prob['rho'] * Contri[idx] + deltaFit
            
            if self.alg['FEs'] % 5000 < 200:
                print(f"FEs: {self.alg['FEs']} | Best: {self.alg['bestval'][0]:.4e}")

        return self.alg['bestval']

    def set_record_callback(self, callback):
        self.record_callback = callback