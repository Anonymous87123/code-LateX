import numpy as np

# 输入需要整数对称矩阵
class rddsm():
    def __init__(self, Matrix):
        self.Matrix = Matrix
        self.sub_space = []

    # 将列表中的单个元素与其他列表合并
    def combine(self, list_of_lists):
        single_element_combined = []
        remaining_lists = []

        for sublist in list_of_lists:
            if len(sublist) == 1:
                single_element_combined.extend(sublist)
            else:
                remaining_lists.append(sublist)
                
        # if len(single_element_combined) > 0:
        #     new_list = remaining_lists + [single_element_combined]
        # else:
        #     new_list = remaining_lists
        subspaces = {'seps': single_element_combined, 'nonseps': remaining_lists} # seps：list of indices; nonseps: list of lists of indices 
        return subspaces
    
    # 按位求并函数
    def bitwise_or(self, list1, list2):
        return [a | b for a, b in zip(list1, list2)]
    
    def find_sum_element(self, lst):
        # 创建一个字典，用于存储所有可能的 bitwise_or 结果
        bitwise_or_dict = {}
        
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                result = tuple(self.bitwise_or(lst[i], lst[j]))
                bitwise_or_dict[result] = (lst[i], lst[j])
        
        # 查找是否存在一个元素是字典中的键
        for element in lst:
            if tuple(element) in bitwise_or_dict:
                return element
        return None
    
    def find_paradigm(self, sub_Matrix):
        # 字典用于存储每个元素及其索引
        element_indices = {}

        # 遍历列表，记录每个元素出现的索引
        for index, element in enumerate(sub_Matrix):
            element_tuple = tuple(element)  # 将列表转换为元组以便作为字典键
            if element_tuple in element_indices:
                element_indices[element_tuple].append(index)
            else:
                element_indices[element_tuple] = [index]

        keys = list(element_indices.keys())
        if len(keys) == 1:
            return [set(element_indices[keys[0]])]
        else:
            union_elements = self.find_sum_element(keys)
            overlap = element_indices[union_elements]
            del element_indices[union_elements]

            for key in element_indices:
                element_indices[key].extend(overlap)
            
            Paradigm_list = []
            for value in element_indices.values():
                Paradigm_list.append(set(value))
            return Paradigm_list
    
    def decomposition(self):
        for i in range(len(self.Matrix[0])):
            sub_Matrix = []
            non_zero_index = np.where(self.Matrix[:,i] != 0)[0]
            non_zero_index = non_zero_index[non_zero_index != i]
            if len(non_zero_index) == 0:
                self.sub_space.append({i})
                continue
            else:
                sub_Matrix = self.Matrix[np.ix_(non_zero_index, non_zero_index)]

                # 寻找范式
                Paradigm_list = self.find_paradigm(sub_Matrix)
                for paradigm in Paradigm_list:
                    paradigm_list = list(paradigm)
                    non_zero_index_add_i= non_zero_index[paradigm_list]
                    non_zero_index_add_i = np.append(non_zero_index_add_i, i)
                    non_zero_index_add_i.sort()
                    self.sub_space.append(set(non_zero_index_add_i))
                    
        # 将每个集合转换为元组，并使用集合移除重复项
        self.sub_space = {tuple(s) for s in self.sub_space}

        # 如果需要将结果转换回列表中的集合
        self.sub_space = [set(t) for t in self.sub_space]

        # 合并单个元素
        self.sub_space = [list(s) for s in self.sub_space]
        self.sub_space = self.combine(self.sub_space)

        return self.sub_space