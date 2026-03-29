from cec2010lsgo_torch.Benchmarks import Benchmarks
import numpy as np
import torch

class F20(Benchmarks):
	def __init__(self, device, output_format):
		super().__init__(device, output_format)
		self.device = device
		self.ID = 20
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
		
		# rosenbrock(z)
		result = super().rosenbrock(self.anotherz)
		
		if self.output_format == 'numpy':
			return result.cpu().numpy()
		return result
