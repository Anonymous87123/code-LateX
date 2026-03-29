from Benchmarks.cec2013lsgo.F1 import F1 as f1
from Benchmarks.cec2013lsgo.F2 import F2 as f2
from Benchmarks.cec2013lsgo.F3 import F3 as f3
from Benchmarks.cec2013lsgo.F4 import F4 as f4
from Benchmarks.cec2013lsgo.F5 import F5 as f5
from Benchmarks.cec2013lsgo.F6 import F6 as f6
from Benchmarks.cec2013lsgo.F7 import F7 as f7
from Benchmarks.cec2013lsgo.F8 import F8 as f8
from Benchmarks.cec2013lsgo.F9 import F9 as f9
from Benchmarks.cec2013lsgo.F10 import F10 as f10
from Benchmarks.cec2013lsgo.F11 import F11 as f11
from Benchmarks.cec2013lsgo.F12 import F12 as f12
from Benchmarks.cec2013lsgo.F13 import F13 as f13
from Benchmarks.cec2013lsgo.F14 import F14 as f14
from Benchmarks.cec2013lsgo.F15 import F15 as f15

class Benchmark():
    def __init__(self, device,output_format):
        self.device = device
        self.output_format = output_format
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
        else:
            raise ValueError("Function id is out of range.")

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
        else:
            raise ValueError("Function id is out of range.")
    
    def get_num_functions(self):
        return 15



