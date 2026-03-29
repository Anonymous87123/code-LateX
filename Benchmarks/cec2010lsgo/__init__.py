"""
cec2010lsgo_torch - CEC 2010 Large Scale Global Optimization Benchmark Functions

This package provides implementations of the CEC 2010 benchmark functions
for large-scale global optimization problems.
"""

__version__ = "1.0.0"
__author__ = "CEC 2010 LSGO Benchmark"

# Import key modules to make them available at package level
from cec2010lsgo_torch.Benchmarks import Benchmarks
from cec2010lsgo_torch.cec2010 import Benchmark

# Import all function classes
from cec2010lsgo_torch.F1 import F1
from cec2010lsgo_torch.F2 import F2
from cec2010lsgo_torch.F3 import F3
from cec2010lsgo_torch.F4 import F4
from cec2010lsgo_torch.F5 import F5
from cec2010lsgo_torch.F6 import F6
from cec2010lsgo_torch.F7 import F7
from cec2010lsgo_torch.F8 import F8
from cec2010lsgo_torch.F9 import F9
from cec2010lsgo_torch.F10 import F10
from cec2010lsgo_torch.F11 import F11
from cec2010lsgo_torch.F12 import F12
from cec2010lsgo_torch.F13 import F13
from cec2010lsgo_torch.F14 import F14
from cec2010lsgo_torch.F15 import F15
from cec2010lsgo_torch.F16 import F16
from cec2010lsgo_torch.F17 import F17
from cec2010lsgo_torch.F18 import F18
from cec2010lsgo_torch.F19 import F19
from cec2010lsgo_torch.F20 import F20

# List of available functions
__all__ = [
    'Benchmarks',
    'Benchmark',
    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
    'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20'
]