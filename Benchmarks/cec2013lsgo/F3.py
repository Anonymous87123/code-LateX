from Benchmarks.cec2013lsgo.benchmark import Benchmarks
import numpy as np
import torch


class F3(Benchmarks):
    def __init__(self,device,output_format):
        super().__init__(device,output_format)
        self.device = device
        self.ID = 3
        self.Ovector = self.readOvector().to(self.device)
        self.minX = -32.0
        self.maxX = 32.0
        self.anotherz = torch.zeros(self.dimension).to(self.device)

    def __call__(self, x):
        return self.compute(x)
    
    def info(self):
        info = {'best': 0.0, 'dimension': self.dimension, 'lower': self.minX, 'threshold': 0, 'upper': self.maxX}
        return info

    def compute(self, x):
        # if x is numpy, transform numpy to tensor
        if isinstance(x, np.ndarray):
            x = torch.tensor(x, dtype=torch.float64,device=self.device)
        x = x.clone().detach() # Convert to tensor

        x.to(self.device)

        if x.ndim == 1:
            x = x.view(1, -1)
        result = torch.zeros(x.shape[0])
        
        self.anotherz = x - self.Ovector
        self.anotherz = self.transform_osz(self.anotherz)
        self.anotherz = self.transform_asy(self.anotherz, 0.2)
        self.anotherz = self.Lambda(self.anotherz, 10)
        result = self.ackley(self.anotherz)
        
        if self.output_format == 'numpy':
            return result.cpu().numpy()
        else:
            return result

