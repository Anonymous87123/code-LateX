
from cec2010lsgo_torch.Benchmarks import Benchmarks
import numpy as np
import torch

class F10(Benchmarks):
	def __init__(self, device, output_format):
		super().__init__(device, output_format)
		self.device = device
		self.ID = 10
		self.s_size = 20
		self.Ovector = self.readOvector().to(self.device)
		self.Pvector = self.readPermVector().to(self.device)
		self.Rmatrix = self.readR(50).to(self.device)
		self.minX = -32.0
		self.maxX = 32.0
		self.r_min_dim = 25
		self.r_med_dim = 50
		self.r_max_dim = 100
		self.anotherz = torch.zeros(self.dimension).to(self.device)

	def __call__(self, x):
		return self.compute(x)

	def info(self):
		info = {'best': 0.0, 'dimension': self.dimension, 'lower': self.minX, 'threshold': 0, 'upper': self.maxX}
		return info

	def compute(self, x):
		if isinstance(x, np.ndarray):
			x = torch.tensor(x, dtype=torch.float64, device=self.device)
		x = x.clone().detach()
		x = x.to(self.device)
		if x.ndim == 1:
			x = x.view(1, -1)
		
		# F10：z=x-o, t=P(z)
		self.anotherz = x - self.Ovector
		t = super().permute_vector(self.anotherz, self.Pvector)
		
		# 分组处理：m=50
		m = 50
		batch_size = x.shape[0]
		dim = x.shape[1]
		
		# 计算组数：k=1,..,D/2m
		num_groups = dim // (2 * m)
		
		# 第一部分：Σrot_rastrigin(t_{(k-1)*m+1},..,t_{k*m}) (k=1,..,D/2m)
		sum_rot_rastrigin = torch.zeros(batch_size, device=self.device, dtype=torch.float64)
		
		for k in range(1, num_groups + 1):
			# 计算当前组的起始和结束索引
			start_idx = (k - 1) * m
			end_idx = k * m
			
			# 获取当前组的变量
			t_group = t[:, start_idx:end_idx]
			
			
			# 对当前组进行旋转
			rotated_group = self.rotate_vector(t_group, self.Rmatrix)
			
			# 计算旋转后的rastrigin函数值并累加
			group_result = super().rastrigin(rotated_group)
			sum_rot_rastrigin += group_result
		
		# 第二部分：rastrigin(t_{D/2+1},..,t_{D})
		start_idx_rest = dim // 2
		t_rest = t[:, start_idx_rest:]
		rastrigin_rest = super().rastrigin(t_rest)
		
		# 合并结果
		result = sum_rot_rastrigin + rastrigin_rest
		
		if self.output_format == 'numpy':
			return result.cpu().numpy()
		return result

