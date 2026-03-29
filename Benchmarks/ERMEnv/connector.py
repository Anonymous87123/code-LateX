import numpy as np
from .ERMPackage.example import ERMEnv as _ERMEnv  # MATLAB 编译生成的包


class ERMEnv:
    def __init__(self, no_evals=1e7, mapped_bound=100,verbose=False):
        """
        Initialize MATLAB engine and environment.
        """
        self.no_evals = no_evals
        self.verbose = verbose

        self.eng = _ERMEnv.initialize()
        if self.verbose:
            print("MATLAB engine 已启动")

        # Initialize MATLAB ERMEnv
        _, lowerB, upperB, dim = self.eng.ERMEnv([], self.no_evals, nargout=4)
        self.lowerB = np.array(lowerB).flatten()
        self.upperB = np.array(upperB).flatten()
        self.dim = int(dim)
        if self.verbose:
            print(f"ERMEnv MATLAB 环境初始化完成，维度: {self.dim}")

        # 映射到统一范围 [-mapped_bound, mapped_bound]
        self.mapped_bound = mapped_bound
        self.mapped_lowerB = -np.ones(self.dim) * mapped_bound
        self.mapped_upperB = np.ones(self.dim) * mapped_bound

        # 计算线性映射参数
        self._scale = (self.upperB - self.lowerB) / (2 * mapped_bound)
        self._shift = self.lowerB + (self.upperB - self.lowerB) / 2

    def _map_to_original(self, pop_mapped: np.ndarray):
        """Map [-mapped_bound, mapped_bound] -> original bounds."""
        return pop_mapped * self._scale + self._shift

    def evaluate(self, pop: np.ndarray):
        """
        Evaluate population in original bounds.
        Uses matlab.double (fast) but safe if using MAT loading.
        """
        pop = np.atleast_2d(pop)
        if pop.shape[1] != self.dim:
            pop = pop.T
        pop_matlab = pop
        S_val = self.eng.ERMEnv(pop_matlab, self.no_evals)
        return np.array(S_val).flatten()

    def evaluate_mapped(self, pop_mapped: np.ndarray):
        """Evaluate mapped population [-mapped_bound, mapped_bound]."""
        pop_orig = self._map_to_original(pop_mapped)
        return self.evaluate(pop_orig)

    def __del__(self):
        if hasattr(self, "eng"):
            self.eng.quit()
            if self.verbose:
                print("MATLAB engine 已关闭")

# ------------------------------
# Test
# ------------------------------

if __name__ == "__main__":
    # 初始化环境
    env = ERMEnv(no_evals=5000)
    dim = env.dim

    # 每个维度上下界
    lb = env.lowerB
    ub = env.upperB

    # 生成 13 个解：每个维度取 13 等分点（这里我们只取每个维度的第一个等分点，构造 13 个不同解）
    n_splits = 13
    X = np.zeros((n_splits, dim))

    for i in range(n_splits):
        fraction = i / (n_splits - 1)  # 0, 1/12, 2/12, ..., 12/12
        X[i, :] = lb + fraction * (ub - lb)

    # 调用 evaluate
    vals = env.evaluate(X)

    # 输出结果
    for i, val in enumerate(vals):
        print(f"Solution {i+1}: Value = {val}")


   