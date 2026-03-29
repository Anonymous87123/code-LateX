import sys
import numpy as np
import time
import torch
import torch.nn as nn


class MLP(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_layer_num):
        super(MLP, self).__init__()
        self.networks = nn.ModuleList()
        # self.in_layer = nn.Sequential(nn.Linear(state_dim,32),nn.Tanh())
        self.networks.append(nn.Sequential(nn.Linear(state_dim, 32), nn.Tanh()))
        # self.hidden_layers = []
        for _ in range(hidden_layer_num):
            self.networks.append(nn.Sequential(nn.Linear(32, 32), nn.Tanh()))
        # self.out_layer = nn.Linear(32,action_dim)
        self.networks.append(nn.Linear(32, action_dim))

    def forward(self, state):
        # h = self.in_layer(state)
        for layer in self.networks:
            state = layer(state)
        return torch.tanh(state)


envs = {
    'ant': {'state_dim': 27, 'action_dim': 8, },  # https://github.com/google/brax/blob/main/brax/envs/ant.py
    'halfcheetah': {'state_dim': 17, 'action_dim': 6, },  # https://github.com/google/brax/blob/main/brax/envs/half_cheetah.py
    'hopper': {'state_dim': 11, 'action_dim': 3, },  # https://github.com/google/brax/blob/main/brax/envs/hopper.py
    'humanoid': {'state_dim': 244, 'action_dim': 17, },  # https://github.com/google/brax/blob/main/brax/envs/humanoid.py
    'humanoidstandup': {'state_dim': 244, 'action_dim': 17, },  # https://github.com/google/brax/blob/main/brax/envs/humanoidstandup.py
    'inverted_pendulum': {'state_dim': 4, 'action_dim': 1, },  # https://github.com/google/brax/blob/main/brax/envs/inverted_pendulum.py
    'inverted_double_pendulum': {'state_dim': 8, 'action_dim': 1, },  # https://github.com/google/brax/blob/main/brax/envs/inverted_double_pendulum.py
    'pusher': {'state_dim': 23, 'action_dim': 7, },  # https://github.com/google/brax/blob/main/brax/envs/pusher.py
    'reacher': {'state_dim': 11, 'action_dim': 2, },  # https://github.com/google/brax/blob/main/brax/envs/reacher.py
    'swimmer': {'state_dim': 8, 'action_dim': 2, },  # https://github.com/google/brax/blob/main/brax/envs/swimmer.py
    'walker2d': {'state_dim': 17, 'action_dim': 6, },  # https://github.com/google/brax/blob/main/brax/envs/walker2d.py
}   # FIXME: humanoid and humanoidstandup should have 376 state_dim in brax on github, but only 244 in experiments.

model_depth = [
    0,
    1,
    2,
    3,
    4,
    5
]


class NE_Problem:
    """
    # Introduction
    `NE_Problem` sets up a neural network-based optimization problem for a given Brax environment. It initializes the environment, neural network model, and evaluation mechanism, and provides a function to evaluate batches of neural network parameters.
    # Args:
    - env_name (str): The name of the Brax environment to solve.
    - model_depth (int): The number of layers (depth) for the neural network policy.
    - seed (int): Random seed for reproducibility.
    # Attributes:
    - env_state_dim (int): Dimension of the environment's state space.
    - env_action_dim (int): Dimension of the environment's action space.
    - nn_model (MLP): The neural network policy model.
    - dim (int): Total number of parameters in the neural network.
    - ub (float): Upper bound for parameter values.
    - lb (float): Lower bound for parameter values.
    - pop_size (int): Population size for evolutionary algorithms.
    - adapter (ParamsAndVector): Adapter for converting between parameter vectors and model parameters.
    - evaluator (BraxProblem): Evaluator for running policy rollouts in the environment.
    # Methods:
    ## func(x)
    Evaluates a batch of neural network parameter vectors by running them in the environment and returning their rewards.
    ### Args:
    - x (np.ndarray): Batch of neural network parameters with shape (batch_size, num_params).
    ### Returns:
    - torch.Tensor: Rewards for each parameter vector in the batch.
    ### Raises:
    - AssertionError: If the input parameter dimension does not match the expected dimension.
    """

    def __init__(self, env_name, model_depth, seed):
        self.env_state_dim = envs[env_name]['state_dim']
        self.env_action_dim = envs[env_name]['action_dim']
        self.nn_model = MLP(self.env_state_dim, self.env_action_dim, model_depth)
        self.dim = sum(p.numel() for p in self.nn_model.parameters())
        self.ub = 0.2
        self.lb = -0.2
        self.seed = seed
        self.env_name = env_name
        self.model_depth = model_depth
        self.optimum = None
        self.init = False

    def reset(self):
        from evox.utils import ParamsAndVector
        self.nn_model.to("cpu")
        self.adapter = ParamsAndVector(dummy_model = self.nn_model)
        self.evaluator = None
        self.T1 = 0

    def __str__(self):
        return f"{self.env_name}-{self.model_depth}"

    def info(self):
        info = {'dimension': self.dim, 'lower': self.lb, 'upper': self.ub} #, 'best': None, 'threshold': None, }
        return info

    def func(self, x):  # x is a batch of neural network parameters: bs * num_params, type: numpy.array
        # x_cuda = torch.from_numpy(x).double().to(torch.get_default_device())
        # x_cuda = torch.from_numpy(x)
        # print(1)
        from evox.problems.neuroevolution.brax import BraxProblem
        # print(torch.cuda.is_available())
        torch.set_default_device("cpu")
        torch.set_float32_matmul_precision('high')

        if self.init:
            pop_size = x.shape[0]
            if pop_size != self.evaluator.pop_size:
                self.evaluator = BraxProblem(
                    policy = self.nn_model,
                    env_name = self.env_name,
                    max_episode_length = 200,
                    num_episodes = 10,
                    pop_size = pop_size,
                    reduce_fn = torch.mean,
                )

        if self.evaluator == None:
            pop_size = x.shape[0]
            self.evaluator = BraxProblem(
                policy = self.nn_model,
                env_name = self.env_name,
                max_episode_length = 200,
                num_episodes = 10,
                pop_size = pop_size,
                seed = self.seed,
                reduce_fn = torch.mean,
            )
            self.init = True

        # 检查输入维度是否匹配模型参数数量
        if x.shape[-1] == self.dim:
            pass  # 一切正常
        elif x.shape[0] == self.dim:
            # 说明用户可能传的是转置的矩阵，需要修正
            x = x.T
            print(f"[Warning] Input x was transposed automatically: new shape = {x.shape}")
        else:
            raise ValueError(
                f"[Dimension Error] Input x has shape {x.shape}, but expected one dimension to match model parameter count = {self.dim}.\n"
                f" - If x.shape[1] == {self.dim}, it should be (batch_size, {self.dim})\n"
                f" - If x.shape[0] == {self.dim}, it will be transposed automatically.\n"
                f"Please check your input data formatting."
            )
        x = torch.tensor(x, device = torch.get_default_device()).float()
        nn_population = self.adapter.batched_to_params(x)
        # for key in nn_population.keys():
        #     print(nn_population[key].shape)
        rewards = self.evaluator.evaluate(nn_population)

        rewards[torch.isnan(rewards)] = -5 * 200
        rewards[torch.isinf(rewards)] = -5 * 200

        torch.set_default_device("cpu")

        rewards = rewards.cpu().numpy()
        rewards = 1e5 - rewards

        return rewards


if __name__ == "__main__":
    import numpy as np
    import time

    # 假设 hyde 已经定义好，和 NE_Problem 已导入
    # 参数
    no_evals = 5000
    NP = 10
    F_weight = 0.3
    F_CR = 0.5

    # 遍历指定环境
    for env_name in envs.keys():
        for depth in model_depth:
            print(f"\n=== Environment: {env_name}, Model Depth: {depth} ===")
            # 初始化 NE_Problem
            problem = NE_Problem(env_name=env_name, model_depth=depth, seed=42)
            problem.reset()

            # 设定边界
            lowerB = np.full(problem.dim, problem.lb)
            upperB = np.full(problem.dim, problem.ub)

            # 定义目标函数 wrapper
            def evaluate_nn_pop(pop):
                return problem.func(pop)

            # ------------------- HyDE-DF -------------------
            dim = problem.dim
            I_itermax = int(no_evals / NP)
            rng = np.random.default_rng()

            # 初始化种群
            pop = rng.uniform(low=lowerB, high=upperB, size=(NP, dim))
            F = np.full((NP, 3), F_weight)
            F_old = F.copy()
            CR = np.full(NP, F_CR)
            CR_old = CR.copy()
            fitness = evaluate_nn_pop(pop)

            best_idx = np.argmin(fitness)
            best_x = pop[best_idx].copy()
            best_f = fitness[best_idx]
            fit_curve = np.zeros(I_itermax)
            fit_curve[0] = best_f

            rot = np.arange(NP)

            start_time = time.time()
            for gen in range(1, I_itermax):
                a = (I_itermax - gen) / I_itermax

                # 更新 F 和 CR
                rand_vals = rng.random((NP, 3))
                ind1 = rand_vals < 0.1
                ind2 = rng.random(NP) < 0.1
                F[ind1] = 0.1 + rng.random(np.sum(ind1)) * 0.9
                F[~ind1] = F_old[~ind1]
                CR[ind2] = rng.random(np.sum(ind2))
                CR[~ind2] = CR_old[~ind2]

                # HyDE-DF trial generation
                idx1 = rng.permutation(NP)
                idx2 = np.roll(idx1, 1)
                idx3 = np.roll(idx2, 1)
                base = np.tile(best_x, (NP, 1))
                diff = pop[idx1] - pop[idx2]
                ginv = np.exp(1 - (1 / a**2))
                trial = pop + F[:, [2]] * diff + ginv * (F[:, [0]] * (base * (F[:, [1]] + rng.normal(size=(NP, dim))) - pop))

                # Binomial crossover
                mask = rng.random((NP, dim)) < CR[:, None]
                trial = np.where(mask, trial, pop)

                # 边界控制
                trial = np.clip(trial, lowerB, upperB)

                # 评估
                trial_fitness = evaluate_nn_pop(trial)

                # 精英选择
                replace = trial_fitness < fitness
                fitness[replace] = trial_fitness[replace]
                pop[replace] = trial[replace]

                # 更新最优
                best_idx = np.argmin(fitness)
                best_x = pop[best_idx].copy()
                best_f = fitness[best_idx]
                fit_curve[gen] = best_f

                # 更新 F_old 和 CR_old
                F_old[replace] = F[replace]
                CR_old[replace] = CR[replace]

                # 进度输出
                print(f"Gen {gen+1}/{I_itermax}, Best fitness: {best_f:.6f}", end='\r')

            elapsed_time = time.time() - start_time
            print(f"\nFinished Environment: {env_name}, Depth: {depth}")
            print(f"Best fitness: {best_f:.6f}, Time elapsed: {elapsed_time:.2f}s")
