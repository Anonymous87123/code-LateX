from cec2010lsgo_torch.Benchmarks import Benchmarks
import numpy as np
import torch

class F6(Benchmarks):
	def __init__(self, device, output_format):
		super().__init__(device, output_format)
		self.device = device
		self.ID = 6
		self.Ovector = self.readOvector().to(self.device)
		self.Pvector = self.readPermVector().to(self.device)
		self.Rmatrix = self.readR(50).to(self.device)
		self.minX = -100.0
		self.maxX = 100.0
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
		
		# F6：z=x-o, t=P(z)
		self.anotherz = x - self.Ovector
		t = super().permute_vector(self.anotherz, self.Pvector)
		
		# 分组处理：m=50
		m = 50
		batch_size = x.shape[0]
		
		# 前m个变量：rot_ackley(t1,..,t_m) * 10^6
		t_m = t[:, :m]
		rotated_t_m = self.rotate_vector(t_m, self.Rmatrix)
		result_m = super().ackley(rotated_t_m) * 1e6
		
		# 剩余变量：ackley(t_m+1,..,t_D)
		t_rest = t[:, m:]
		result_rest = super().ackley(t_rest)
		
		# 合并结果
		result = result_m + result_rest
		
		if self.output_format == 'numpy':
			return result.cpu().numpy()
		return result
