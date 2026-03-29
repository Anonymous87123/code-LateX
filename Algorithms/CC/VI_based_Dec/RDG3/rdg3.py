import numpy as np

class RDG3():
    def __init__(self, fun, info, cfg):
        self.fun = fun
        self.info = info
        self.counter = 0
        self.epsilon = 0
        self.y1 = None
        self.rdg_3_epsilon_n = 50
        self.rdg_3_epsilon_s = 100
    
    def combine(self, list_of_lists):
        single_element_combined = []
        remaining_lists = []

        for sublist in list_of_lists:
            if len(sublist) == 1:
                single_element_combined.extend(sublist)
            else:
                remaining_lists.append(sublist)
                
        subspaces = {'seps': single_element_combined, 'nonseps': remaining_lists} # seps：list of indices; nonseps: list of lists of indices 
        return subspaces

    def gamma(self, d):
        muM = np.finfo(float).eps / 2
        return (d * muM) / (1 - d * muM)
    
    def intersect(self, sub_1, sub_2):
        p2 = np.ones(self.info['dimension'])*self.info['lower'] # x_ll
        p2[sub_1] = self.info['upper'] # x_ul
        y2 = self.fun(p2)
        self.counter += 1
        d1 = self.y1 - y2 # f(x_ll) - f(x_ul)

        p3 = np.ones(self.info['dimension'])*self.info['lower']
        p4 = p2.copy()
        p3[sub_2] = (self.info['upper']+self.info['lower'])/2 # x_lm
        p4[sub_2] = (self.info['upper']+self.info['lower'])/2 # x_um
        y3 = self.fun(p3)
        y4 = self.fun(p4)
        self.counter += 2
        d2 = y3 - y4 # f(x_lm) - f(x_um)

        self.epsilon = self.gamma((self.info['dimension']**0.5) + 2) * (abs(self.y1) + abs(y2) + abs(y3) + abs(y4))
        if abs(d1 - d2) > self.epsilon:
            if len(sub_2) == 1:
                sub_1.append(sub_2[0])
                return sub_1, []  # x_remain is empty
            else:
                k = len(sub_2) // 2
                sub_2_1 = sub_2[:k]  # G1
                sub_2_2 = sub_2[k:]  # G2

                sub_1_1, x_remain_1 = self.intersect(sub_1.copy(), sub_2_1.copy())
                sub_1_2, x_remain_2 = self.intersect(sub_1.copy(), sub_2_2.copy())

                sub_1_combined = list(set(sub_1_1 + sub_1_2))  
                x_remain_combined = list(set(x_remain_1 + x_remain_2))  

                return sub_1_combined, x_remain_combined
        else:
            return sub_1, sub_2  # sub_2 is x_remain

    def decompose(self):
        sub_problems = []
        self.y1 = self.fun(np.ones(self.info['dimension'])*self.info['lower'])
        self.counter += 1
        sub_1 = []
        sub_2 = []
        x_remain = []
        sub_1.append(0)
        x_remain.append(0)
        sub_2.extend(range(1, self.info['dimension']))
        x_remain.extend(range(1, self.info['dimension']))
        while len(x_remain) > 0:
            x_remain.clear()
            result = self.intersect(sub_1.copy(), sub_2.copy())
            sub_1_a = result[0]
            x_remain = result[1]
            if len(sub_1_a) != len(sub_1) and len(sub_1_a)<self.rdg_3_epsilon_n:
                sub_1 = sub_1_a
                sub_2 = x_remain.copy()
                if len(x_remain) == 0:
                    sub_problems.append(sub_1.copy())
                    break
            else:
                sub_problems.append(sub_1_a.copy())
                if len(x_remain) > 1:
                    sub_1.clear()
                    key = x_remain[0]
                    sub_1.append(key)
                    x_remain.remove(key)
                    sub_2.clear()
                    sub_2.extend(x_remain)
                elif len(x_remain) == 1:
                    sub_problems.append(x_remain.copy())
                    break
            
        return self.combine(sub_problems)