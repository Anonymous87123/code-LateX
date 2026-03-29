import torch
import numpy as np
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

class Delta():
    delta1 = 0
    delta2 = 0

class Evaluations():
    base = 0
    F = 0
    fhat = 0

class DG2():
    def __init__(self, fun, info, cfg):
        self.fun = fun
        self.info = info
        self.device = cfg.device
        self.batch_size = cfg.batch_size

    def dg3(self):
        delta, evaluations, lambda_ = self.ism()
        subspaces, theta, epsilon = self.dsm(evaluations, lambda_)
        return subspaces, theta

    def ism(self):
        delta = Delta()
        evaluations = Evaluations()

        # 使用 torch 替代 numpy
        lower = torch.tensor(self.info['lower'], device=self.device)
        upper = torch.tensor(self.info['upper'], device=self.device)
        dimension = self.info['dimension']

        center = 0.5 * (lower + upper)
        f_archive = torch.full((dimension, dimension), torch.nan, device=self.device)  # record the [a_hat,b_hat,c,...] in the paper
        fhat_archive = torch.full((1 , dimension), torch.nan, device=self.device)  # record the [a,b_hat,c,...] in the paper
        delta1 = torch.full((dimension, dimension), torch.nan, device=self.device)
        delta2 = torch.full((dimension, dimension), torch.nan, device=self.device)
        lambda_ = torch.full((dimension, dimension), torch.nan, device=self.device)  # raw interaction structure matrix

        p1 = torch.ones(dimension, device=self.device) * lower
        fp1 = self.fun(p1)  # f_base

        # 创建一个矩阵，其中每一行是基向量 p1 的副本
        p2 = p1.unsqueeze(0).expand(dimension, -1).clone()
        indices = torch.arange(dimension, device=self.device)

        # 更新 p2 的 对角线 为 center 值
        p2[indices, indices] = center
        fp2 = self.fun(p2)
        fhat_archive = fp2
        
        # d1值，记录 i 位置的 fhat_archive 与 fp1 的差值
        d1 = fhat_archive - fp1

        # 生成一个上三角矩阵的索引
        i_indices, j_indices = torch.triu_indices(dimension, dimension, 1, device=self.device)

        for row in range(len(fhat_archive)):
            # 找到上三角矩阵中与当前行对应的列索引
            row_indices = (i_indices == row).nonzero(as_tuple=True)[0]
            # 更新 delta1 对应位置的值
            delta1[row, j_indices[row_indices]] = d1[row]
        
        # 批量处理 p4 和计算 delta1, delta2, lambda_
        num_batches = (i_indices.size(0) + self.batch_size - 1) // self.batch_size
        for batch_idx in tqdm(range(num_batches)):
            start_idx = batch_idx * self.batch_size
            end_idx = min((batch_idx + 1) * self.batch_size, i_indices.size(0))

            i_batch = i_indices[start_idx:end_idx]
            j_batch = j_indices[start_idx:end_idx]

            p4_batch = p1.unsqueeze(0).expand(i_batch.size(0), -1).clone()
            p4_batch[torch.arange(len(i_batch)), i_batch] = center
            p4_batch[torch.arange(len(j_batch)), j_batch] = center

            fp4_batch = self.fun(p4_batch)

            # 更新 f_achieved 对应位置的值
            for idx in range(len(i_batch)):
                f_archive[i_batch[idx], j_batch[idx]] = fp4_batch[idx]

        delta2 = f_archive.clone()
        # 遍历每一列 i，减去 A[i]，但只在上三角矩阵的相应部分执行减法
        for i in range(1,dimension):
            # 找到列 j == i 的行索引
            row_indices = (j_indices == i).nonzero(as_tuple=True)[0]
            delta2[i_indices[row_indices], i] -= fhat_archive[i]
        
        # 将f_archive转为对称矩阵
        f_archive = self.upper_to_symmetric_(f_archive)

        lambda_ = torch.abs(delta1 - delta2) # 关键是lamda_的计算

        # 将结果存储到 delta 和 evaluations 中
        delta.delta1 = delta1
        delta.delta2 = delta2
        evaluations.base = fp1
        evaluations.F = f_archive
        evaluations.fhat = fhat_archive

        return delta, evaluations, lambda_


    # DSM: Decomposition Structure Matrix
    def dsm(self, evaluation, lambda_):
        dimension = self.info['dimension']
        fhat_archive = evaluation.fhat.to(self.device)
        f_archive = evaluation.F.to(self.device)
        fp1 = evaluation.base

        F1 = torch.full((dimension, dimension), fp1.item(), device=self.device)
        F2 = torch.tile((fhat_archive.unsqueeze(1)).T, (dimension, 1))
        F3 = torch.tile(fhat_archive.unsqueeze(1), ( 1, dimension))
        F4 = f_archive
        FS = torch.stack((F1, F2, F3, F4), dim=2)
        Fmax = torch.amax(FS, dim=2)
        FS = torch.stack((F1 + F4, F2 + F3), dim=2)
        Fmax_inf = torch.amax(FS, dim=2)

        theta = torch.full((dimension, dimension), torch.nan, device=self.device)  # design structure matrix
        muM = torch.finfo(torch.float64).eps / 2
        gamma = lambda n: (n * muM) / (1 - n * muM)
        errlb = gamma(2) * Fmax_inf
        errub = gamma((dimension) ** 0.5) * Fmax

        I1 = lambda_ <= errlb
        theta[I1] = 0
        I2 = lambda_ >= errub
        theta[I2] = 1
        I0 = lambda_ == 0
        c0 = torch.sum(I0)
        count_seps = torch.sum(~I0 & I1)  # 0 < lambda_ <= errlb
        count_nonseps = torch.sum(I2)
        reliable_calcs = count_seps + count_nonseps
        w1 = (count_seps + c0) / (c0 + reliable_calcs)
        w2 = count_nonseps / (c0 + reliable_calcs)
        epsilon = w1 * errlb + w2 * errub

        AdjTemp = lambda_ > epsilon  # adjustment threshold
        idx = torch.isnan(theta)
        theta[idx] = AdjTemp[idx].to(dtype=torch.float64)  # Complete the values ​​in the range[errlb, errub]
        theta[torch.eye(dimension, device=self.device).bool()] = True
        theta = self.upper_to_symmetric(theta)
        theta = theta.int()

        return theta

    def upper_to_symmetric(self, upper_matrix):
        # 确保输入矩阵为方阵
        assert upper_matrix.shape[0] == upper_matrix.shape[1], "输入矩阵必须是方阵"

        # 将矩阵与其转置相加，并减去对角线的重复部分
        symmetric_matrix = upper_matrix + upper_matrix.T - torch.diag(upper_matrix.diagonal())

        return symmetric_matrix

