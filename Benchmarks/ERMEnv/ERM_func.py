from .connector import ERMEnv
import numpy as np

class ERM_fun:
    def __init__(self):
        self._erm_env = None

        self.reinitialize()

    def reinitialize(self, no_evals=int(1e7)):
        self.no_evals = no_evals
        self.lb, self.ub = self.get_bounds()
        self.dim = 13680
        self.used_evals = 0

        # Temp
        self.optimum = None

    def __str__(self):
        return "ERM_fun"

    def info(self):
        info = {'dimension': self.dim, 'lower': self.lb, 'upper': self.ub} #, 'best': None, 'threshold': None, }
        return info

    def get_bounds(self):
        if self._erm_env is None:
            self._erm_env = ERMEnv(no_evals=self.no_evals)
            ret = (self._erm_env.lowerB, self._erm_env.upperB)
            self._erm_env = None
        else:
            ret = (self._erm_env.lowerB, self._erm_env.upperB)
        return ret

    def func(self, x):
        # 检查是否已有 ERMEnv 实例
        if self._erm_env is None:
            self._erm_env = ERMEnv(no_evals=self.no_evals)
            print("已创建 ERMEnv 实例")

        result = self._erm_env.evaluate(x)
        return result[0] if x.ndim == 1 else result



class ERM_fun_mapped(ERM_fun):
    def __init__(self):
        super().__init__()

    def reinitialize(self, no_evals=int(1e7), boundary=100):
        super().reinitialize(no_evals=no_evals)
        self.ub = boundary * np.ones(self.dim)
        self.lb = -boundary * np.ones(self.dim)

    def __str__(self):
        return "ERM_fun_mapped"

    def func(self, x):
        # 检查是否已有 ERMEnv 实例
        if self._erm_env is None:
            self._erm_env = ERMEnv(no_evals=self.no_evals, mapped_bound=self.ub)
            print("已创建 ERMEnv 实例")

        result = self._erm_env.evaluate_mapped(x)
        return result[0] if x.ndim == 1 else result


if __name__ == "__main__":
    # 初始化环境
    if False:
        env = ERM_fun_mapped()
    else:
        env = ERM_fun()
    dim = env.dim

    # 每个维度上下界
    lb = env.lb
    ub = env.ub

    # 生成 13 个解：每个维度取 13 等分点（这里我们只取每个维度的第一个等分点，构造 13 个不同解）
    n_splits = 13
    X = np.zeros((n_splits, dim))

    for i in range(n_splits):
        fraction = i / (n_splits - 1)  # 0, 1/12, 2/12, ..., 12/12
        X[i, :] = lb + fraction * (ub - lb)

    # 调用 evaluate
    vals = env.func(X)

    # 输出结果
    for i, val in enumerate(vals):
        print(f"Solution {i+1}: Value = {val}")