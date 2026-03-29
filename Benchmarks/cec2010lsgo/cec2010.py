from cec2010lsgo_torch.F1 import F1 as f1
from cec2010lsgo_torch.F2 import F2 as f2
from cec2010lsgo_torch.F3 import F3 as f3
from cec2010lsgo_torch.F4 import F4 as f4
from cec2010lsgo_torch.F5 import F5 as f5
from cec2010lsgo_torch.F6 import F6 as f6
from cec2010lsgo_torch.F7 import F7 as f7
from cec2010lsgo_torch.F8 import F8 as f8
from cec2010lsgo_torch.F9 import F9 as f9
from cec2010lsgo_torch.F10 import F10 as f10
from cec2010lsgo_torch.F11 import F11 as f11
from cec2010lsgo_torch.F12 import F12 as f12
from cec2010lsgo_torch.F13 import F13 as f13
from cec2010lsgo_torch.F14 import F14 as f14
from cec2010lsgo_torch.F15 import F15 as f15
from cec2010lsgo_torch.F16 import F16 as f16
from cec2010lsgo_torch.F17 import F17 as f17
from cec2010lsgo_torch.F18 import F18 as f18
from cec2010lsgo_torch.F19 import F19 as f19
from cec2010lsgo_torch.F20 import F20 as f20

class Benchmark():
	def __init__(self, device, output_format):
		self.device = device # 接收设备CPU或GPU
		self.output_format = output_format # F(x)函数值的输出格式，比如以Numpy数组形式输出

    # 传入参数，获取对应函数类的实例
	def get_function(self, func_id):
		if func_id == 1:
			return f1(self.device, self.output_format)
		elif func_id == 2:
			return f2(self.device, self.output_format)
		elif func_id == 3:
			return f3(self.device, self.output_format)
		elif func_id == 4:
			return f4(self.device, self.output_format)
		elif func_id == 5:
			return f5(self.device, self.output_format)
		elif func_id == 6:
			return f6(self.device, self.output_format)
		elif func_id == 7:
			return f7(self.device, self.output_format)
		elif func_id == 8:
			return f8(self.device, self.output_format)
		elif func_id == 9:
			return f9(self.device, self.output_format)
		elif func_id == 10:
			return f10(self.device, self.output_format)
		elif func_id == 11:
			return f11(self.device, self.output_format)
		elif func_id == 12:
			return f12(self.device, self.output_format)
		elif func_id == 13:
			return f13(self.device, self.output_format)
		elif func_id == 14:
			return f14(self.device, self.output_format)
		elif func_id == 15:
			return f15(self.device, self.output_format)
		elif func_id == 16:
			return f16(self.device, self.output_format)
		elif func_id == 17:
			return f17(self.device, self.output_format)
		elif func_id == 18:
			return f18(self.device, self.output_format)
		elif func_id == 19:
			return f19(self.device, self.output_format)
		elif func_id == 20:
			return f20(self.device, self.output_format)
		else:
			raise ValueError(f"Unknown function id: {func_id}")

	def get_info(self, func_id):
		if func_id == 1:
			f1_ = f1(self.device, self.output_format)
			return f1_.info()
		elif func_id == 2:
			f2_ = f2(self.device, self.output_format)
			return f2_.info()
		elif func_id == 3:
			f3_ = f3(self.device, self.output_format)
			return f3_.info()
		elif func_id == 4:
			f4_ = f4(self.device, self.output_format)
			return f4_.info()
		elif func_id == 5:
			f5_ = f5(self.device, self.output_format)
			return f5_.info()
		elif func_id == 6:
			f6_ = f6(self.device, self.output_format)
			return f6_.info()
		elif func_id == 7:
			f7_ = f7(self.device, self.output_format)
			return f7_.info()
		elif func_id == 8:
			f8_ = f8(self.device, self.output_format)
			return f8_.info()
		elif func_id == 9:
			f9_ = f9(self.device, self.output_format)
			return f9_.info()
		elif func_id == 10:
			f10_ = f10(self.device, self.output_format)
			return f10_.info()
		elif func_id == 11:
			f11_ = f11(self.device, self.output_format)
			return f11_.info()
		elif func_id == 12:
			f12_ = f12(self.device, self.output_format)
			return f12_.info()
		elif func_id == 13:
			f13_ = f13(self.device, self.output_format)
			return f13_.info()
		elif func_id == 14:
			f14_ = f14(self.device, self.output_format)
			return f14_.info()
		elif func_id == 15:
			f15_ = f15(self.device, self.output_format)
			return f15_.info()
		elif func_id == 16:
			f16_ = f16(self.device, self.output_format)
			return f16_.info()
		elif func_id == 17:
			f17_ = f17(self.device, self.output_format)
			return f17_.info()
		elif func_id == 18:
			f18_ = f18(self.device, self.output_format)
			return f18_.info()
		elif func_id == 19:
			f19_ = f19(self.device, self.output_format)
			return f19_.info()
		elif func_id == 20:
			f20_ = f20(self.device, self.output_format)
			return f20_.info()
		else:
			raise ValueError(f"Unknown function id: {func_id}")

	def get_num_functions(self):
		return 20
