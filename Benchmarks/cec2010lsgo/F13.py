from cec2010lsgo_torch.Benchmarks import Benchmarks
import numpy as np
import torch

class F13(Benchmarks):
	def __init__(self, device, output_format):
		super().__init__(device, output_format)
		self.device = device
		self.ID = 13
		self.Ovector = self.readOvector().to(self.device)
		self.Pvector = self.readPermVector().to(self.device)
		self.minX = -100.0
		self.maxX = 100.0

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
		
		# z = x - o
		self.anotherz = x - self.Ovector
		# t = P(z) - 使用Benchmarks中的置换函数
		t = super().permute_vector(self.anotherz, self.Pvector)
		
		# 分组参数 m = 50
		m = 50
		D = self.dimension
		num_groups = D // (2 * m)
		
		result = torch.zeros(x.shape[0], dtype=torch.float64, device=self.device)
		
		# Σ rosenbrock(t_{(k-1)*m+1},..,t_{k*m}) for k=1,..,D/2m
		for k in range(num_groups):
			start_idx = k * m
			end_idx = (k + 1) * m
			group = t[:, start_idx:end_idx]
			result += super().rosenbrock(group)
		
		# sphere(t_{D/2+1},..,t_{D})
		remaining_start = D // 2
		remaining_group = t[:, remaining_start:]
		result += super().sphere(remaining_group)
		
		if self.output_format == 'numpy':
			return result.cpu().numpy()
		return result
