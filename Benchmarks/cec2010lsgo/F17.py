
from cec2010lsgo_torch.Benchmarks import Benchmarks
import numpy as np
import torch

class F17(Benchmarks):
	def __init__(self, device, output_format):
		super().__init__(device, output_format)
		self.device = device
		self.ID = 17
		self.s_size = 20
		self.Ovector = self.readOvector().to(self.device)
		self.Pvector = self.readPermVector().to(self.device)
		self.s = self.readS(self.s_size)
		self.w = self.readW(self.s_size).to(self.device)
		self.minX = -100.0
		self.maxX = 100.0
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
		
		# z = x - o
		self.anotherz = x - self.Ovector
		# t = P(z)
		t = super().permute_vector(self.anotherz, self.Pvector)
		
		# m = 50
		m = 50
		D = self.dimension
		num_groups = D // m
		
		result = torch.zeros(x.shape[0], dtype=torch.float64, device=self.device)
		
		# Σschwefel(t_{(k-1)*m+1},..,t_{k*m}) for k=1,..,D/m
		for k in range(num_groups):
			start_idx = k * m
			end_idx = (k + 1) * m
			group = t[:, start_idx:end_idx]
			result += super().schwefel(group)
		
		if self.output_format == 'numpy':
			return result.cpu().numpy()
		return result

