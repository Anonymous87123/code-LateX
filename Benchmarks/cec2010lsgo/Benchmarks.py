
import torch
import numpy as np
import os

class Benchmarks:
	# 基础变量+数据文件夹路径
	def __init__(self, device, output_format):
		torch.set_default_dtype(torch.float64)
		# 数据文件夹路径（可根据实际情况调整）
		self.data_dir = r"E:\cec2010lsgo\cec2010lsgo_torch\cdatafiles"
		self.dimension = 1000  # 默认维度
		self.min_dim = 25
		self.med_dim = 50
		self.max_dim = 100
		self.device = device
		self.ID = None
		self.s_size = 20
		self.overlap = None
		self.minX = None
		self.maxX = None
		self.Ovector = None
		self.OvectorVec = None
		self.Pvector = None
		self.r_min_dim = None
		self.r_med_dim = None
		self.r_max_dim = None
		self.anotherz = torch.zeros(self.dimension)
		self.anotherz1 = None
		self.best = 0
		self.maxevals = 3000000
		self.numevals = 0
		self.output = ""
		self.output_dir = 'cec2010lsgo_py'
		self.output_format = output_format
     
	# 从F{self.ID}-xopt.txt读取移位向量o，适用于F1-F20
	def readOvector(self):
		o = torch.zeros(self.dimension) #不移位等价于o=O,所以初始化需要d为D维零向量
		file_path = os.path.join(self.data_dir, f"F{self.ID}-xopt.txt")
		try:
			with open(file_path, 'r') as file:
				c = 0
				for line in file:
					values = line.strip().split(',')
					for value in values:
						if c < self.dimension:
							o[c] = float(value)
							c += 1
		except FileNotFoundError:
			print(f"Cannot open the datafile '{file_path}'")
		return o

    # 从F{self.ID}-xopt.txt读取移位向量o，将o组织成相应的分块形式，适用于处理具有多个子组件或分块结构的复杂测试函数
	def readOvectorVec(self):
		o = [torch.zeros(self.s[i], device=self.device) for i in range(self.s_size)]
		file_path = os.path.join(self.data_dir, f"F{self.ID}-xopt.txt")
		try:
			with open(file_path, 'r') as file:
				c = 0
				i = -1
				up = 0
				for line in file:
					if c == up:
						i += 1
						up += self.s[i]
					values = line.strip().split(',')
					for value in values:
						if c < self.dimension:
							o[i][c - (up - self.s[i])] = float(value)
							c += 1
		except FileNotFoundError:
			print(f"Cannot open the datafile '{file_path}'")
		return o

    # 从F{self.ID}-p.txt读取置换向量P。
	def readPermVector(self):
		d = torch.zeros(self.dimension, dtype=torch.int64) # 不置换等价于P=0，也就是若后续代码识别到P=0，那么就按照原始x的顺序即可
		file_path = os.path.join(self.data_dir, f"F{self.ID}-p.txt")
		try:
			with open(file_path, 'r') as file:
				c = 0
				for line in file:
					values = line.strip().split(',')
					for value in values:
						if c < self.dimension:
							d[c] = int(float(value)) - 1  
							c += 1
		except FileNotFoundError:
			print(f"Cannot open the datafile '{file_path}'")
		return d

    # 从F{self.ID}-R{dim}.txt读取旋转矩阵R。
	def readR(self, dim):
		file_path = os.path.join(self.data_dir, f"F{self.ID}-R{dim}.txt")
		mat = torch.eye(dim) # 不旋转等价于R=E，单位阵
		try:
			with open(file_path, 'r') as file:
				i = 0
				for line in file:
					values = line.strip().split(',')
					for j, value in enumerate(values):
						if i < dim and j < dim:
							mat[i, j] = float(value)
					i += 1
		except FileNotFoundError:
			print(f"Cannot open the datafile '{file_path}'")
		return mat

    # 从F{self.ID}-s.txt读取分块向量s，s[i]代表第i个子空间的维度。
	def readS(self, s_size):
		file_path = os.path.join(self.data_dir, f"F{self.ID}-s.txt")
		s = []
		try:
			with open(file_path, 'r') as file:
				for line in file:
					values = line.strip().split(',')
					for value in values:
						if len(s) < s_size:
							s.append(int(value))
		except FileNotFoundError:
			print(f"Cannot open the datafile '{file_path}'")
		return s

    # 从F{self.ID}-w.txt读取分块权重向量w，w[i]代表第i个子空间的权重，衡量其贡献度。
	def readW(self, s_size):
		file_path = os.path.join(self.data_dir, f"F{self.ID}-w.txt")
		w = torch.ones(s_size)/s_size # 不指定权重等价于贡献一致
		try:
			with open(file_path, 'r') as file:
				c = 0
				for line in file:
					values = line.strip().split(',')
					for value in values:
						if c < s_size:
							w[c] = float(value)
							c += 1
		except FileNotFoundError:
			print(f"Cannot open the datafile '{file_path}'")
		return w
    
    # 旋转
	def rotate_vector(self, x, RMatrix):
		# 直接矩阵乘法得到旋转后的向量
		rotated = torch.zeros_like(x).to(self.device)
		for i in range(x.shape[0]):
			rotated[i] = x[i] @ RMatrix.T
		
		return rotated
    
	# 置换
	def permute_vector(self, x, p_vector=None):
		if p_vector is None:
			p_vector = self.Pvector
		permuted = torch.zeros_like(x).to(self.device)
		for i in range(x.shape[0]):
			permuted[i] = x[i, p_vector]
		return permuted

    # 基本函数
	def sphere(self, x):
		return torch.sum(x**2, dim=1)
	
	def elliptic(self, x):
		batch_size, dimension = x.shape
		i = torch.arange(dimension, device=self.device).float()
		weights = 10.0 ** (6.0 * i / (dimension - 1))
		return torch.sum(weights * x**2, dim=1)
	
	def rastrigin(self, x):
		term1 = x**2
		term2 = 10 * torch.cos(2 * torch.pi * x)
		return torch.sum(term1 - term2 + 10, dim=1)
	
	def ackley(self, x):
		batch_size, dimension = x.shape
		
		# 第一项: -20 * exp(-0.2 * sqrt(1/D * Σ(x_i^2)))
		sum_squares = torch.sum(x**2, dim=1)
		term1 = -20 * torch.exp(-0.2 * torch.sqrt(sum_squares / dimension))
		
		# 第二项: -exp(1/D * Σ(cos(2 * π * x_i)))
		sum_cos = torch.sum(torch.cos(2 * torch.pi * x), dim=1)
		term2 = -torch.exp(sum_cos / dimension)
		
		# 常数项: 20 + exp(1)
		term3 = 20 + torch.exp(torch.tensor(1.0, device=self.device))
		
		return term1 + term2 + term3
	
	def schwefel(self, x):
		batch_size, dimension = x.shape
		cumulative_sums = torch.cumsum(x, dim=1)
		return torch.sum(cumulative_sums**2, dim=1)
	
	def rosenbrock(self, x):
		batch_size, dimension = x.shape
		
		# 对于每个i从0到dimension-2
		x_i = x[:, :-1]  # x_1 到 x_{D-1}
		x_ip1 = x[:, 1:]  # x_2 到 x_D
		
		# 计算两项
		term1 = 100 * (x_i**2 - x_ip1)**2
		term2 = (x_i - 1)**2
		
		# 对最后一项单独处理 (x_D - 1)^2
		last_term = (x[:, -1] - 1)**2
		
		return torch.sum(term1 + term2, dim=1) + last_term