import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simpson
import time
from PIL import Image
import pandas as pd

'''
此库为AOB的小工具库:
1、calculate_DA: 计算分解准确性
2、EvaluatorLogger: 评估记录器, 用于在评估过程中记录一些信息
3、remove_overlapping_groups: 去除重叠组
4、make_monotonic_decreasing: 使数组单调递减
5、combine: 用于CC中将子空间映射回全空间
6、evaluation_record: 评估记录
7、plot_evaluation_curve: 绘制评估曲线
8、plot_evaluation_curve_best_so_far: 绘制最佳评估曲线
9、plot_time_consumption: 绘制时间消耗曲线
10、plot_target_based_ecdf: 绘制基于目标的ECDF曲线
11、plot_eaf_based_ecdf: 绘制基于EAF的ECDF曲线
'''

def calculate_DA(true_subcomps, predicted_subcomps):
    """
    计算分解准确性 (DA)。

    Args:
        true_subcomps (list of sets): 真实的子组件集合，每个子组件是一个集合。
        predicted_subcomps (list of sets): 算法生成的子组件集合，每个子组件是一个集合。

    Returns:
        float: DA 的值。
    """
    # 初始化变量
    numerator = 0
    denominator = 0

    # 遍历每个真实的子组件
    for true_comp in true_subcomps:
        true_set = set(true_comp)
        # 计算与每个预测子组件的交集大小
        intersections = [len(true_set & set(pred_comp)) for pred_comp in predicted_subcomps]
        # 取最大交集
        numerator += max(intersections)
        # 累加真实子组件的大小
        denominator += len(true_comp)

    # 计算 DA
    da = numerator / denominator if denominator > 0 else 0
    return da

class EvaluatorLogger:
    def __init__(self, fun, interval=50000):
        """
        初始化记录器。

        参数：
        - fun: 目标函数，支持批量输入。
        - interval: 每隔多少次评估记录一次时间，默认为 50000。
        """
        self.fun = fun  # 原始目标函数
        self.interval = interval  # 记录间隔
        self.count = 0  # 总评估次数
        self.times = []  # 存储时间的列表
        self.last_record_time = time.time()  # 上一次记录的时间

    def __call__(self, x_batch):
        """
        批量评估函数的包装器。

        参数：
        - x_batch: 输入样本矩阵，每一行是一个样本。
        - *args, **kwargs: 目标函数的其他参数。

        返回：
        - y_batch: 目标函数的评估结果。
        """
        # 评估目标函数
        y_batch = self.fun(x_batch)

        # 更新计数器
        self.count += len(x_batch)

        # 检查是否需要记录时间
        if self.count // self.interval > len(self.times):
            current_time = time.time()
            elapsed_time = current_time - self.last_record_time
            self.times.append(elapsed_time)
            self.last_record_time = current_time  # 更新上一次记录时间

        return y_batch

    def get_times(self):
        """
        获取记录的时间列表。

        返回：
        - times: 每隔 interval 次评估记录的时间列表。
        """
        return self.times
    
def remove_overlapping_groups(grouping_result):
    seen = set()  # 用来跟踪已经处理过的元素
    unique_groups = []  # 存储最终去重后的组
    duplicates = []  # 存储所有重复的元素
    overlap_groups = []  # 存储相邻组之间的重复元素
    grouping_result_ = grouping_result.copy()  # 避免直接修改原数组

    # 先处理所有组，将重复项提取出来
    for group in grouping_result:
        for item in group:
            if item in seen:
                duplicates.append(item)  # 找到重复项并记录
            else:
                seen.add(item)  # 标记为已处理

    # 遍历所有组并删除重复项，计算相邻组之间的重复项
    for i in range(len(grouping_result) - 1):
        group1 = grouping_result[i]
        group2 = grouping_result[i + 1]

        group1_ = grouping_result_[i]
        group2_ = grouping_result_[i + 1]

        # 找出group1和group2之间的重复元素
        overlap = set(group1) & set(group2)
        overlap_groups.append(list(overlap))  # 将重复元素作为一个子列表加入overlap_groups
        
        # 过滤掉重复元素
        unique_group1 = [item for item in group1_ if item not in overlap]
        unique_group2 = [item for item in group2_ if item not in overlap]
        
        unique_groups.append(unique_group1)

        # 更新第二组，但不直接修改原数组中的 `grouping_result`，避免错位
        grouping_result_[i + 1] = unique_group2

    # 最后加入处理后的最后一组
    unique_groups.append(list(set(grouping_result[-1])-set(overlap_groups[-1])))

    duplicates = list(set(duplicates))  # 去重
    return unique_groups, duplicates, overlap_groups

def make_monotonic_decreasing(arr):
    for i in range(len(arr) - 1):
        if arr[i] < arr[i + 1]:  # 如果前面的元素小于后面的元素
            arr[i + 1] = arr[i]  # 修改后面的元素，使其不大于当前元素
    return arr

def combine(small_vec, background_vec, location):
    if location is None:
        return small_vec
    else:
        combination = np.tile(background_vec, (len(small_vec), 1))
        combination[:, location] = small_vec
        return combination

def evaluation_record(data, output_path, record_FEs_list):
    """
    记录算法的评估值（包括特定评估点和最终点），以及运行时间。

    Args:
        data (dict): 包含算法运行结果及运行时间的字典。
        output_path (str): 输出路径。
        record_FEs_list (list): 特定的评估点列表。
    """
    # Convert the record points to integers
    record_FEs_list = [int(x) for x in record_FEs_list]
    
    # Initialize a dictionary to hold the average fitness values for each algorithm
    algorithm_avg_fitness = {}

    for algorithm, runs in data.items():
        if "_time" in algorithm:  # 跳过时间记录的键
            continue

        runs = [make_monotonic_decreasing(run.copy()) for run in runs]
        # 获取当前算法的所有运行数据
        max_length = max(len(run) for run in runs)  # 获取所有运行中最长的评估值列表长度
        avg_fitness = []  # 存储每个评估次数的均值
        variances = []  # 存储每个评估次数的方差

        # 遍历每个评估次数
        for i in range(max_length):
            values_at_i = [run[i] for run in runs if i < len(run)]  # 获取所有运行中第 i 次评估的值
            if values_at_i:  # 如果有运行达到了当前评估次数
                avg_fitness.append(sum(values_at_i) / len(values_at_i))  # 计算均值
                variances.append(np.std(values_at_i)) # 计算方差
            else:
                avg_fitness.append(None)  # 如果没有值，填充 None
                variances.append(None)  # 方差也填充 None
        
        # Store the computed average fitness for the current algorithm
        algorithm_avg_fitness[algorithm] = {'avg_fitness': avg_fitness, 'variances': variances}
    
    # Save the record points and their corresponding fitness values to a txt file
    output_file_path = f"{output_path}evaluation_record.txt"
    with open(output_file_path, 'w') as f:
        # Write a well-formatted header with a line separator
        f.write(f"{'Algorithm':<20}{'Record Point':<25}{'Fitness Value':<30}{'Scientific Notation':<25}{'Variance':<30}{'Scientific Notation':<25}\n")
        f.write("-" * 155 + "\n")  # Separator line
        
        # Write each record point for every algorithm
        for algorithm, avg_fitness in algorithm_avg_fitness.items():
            f.write(f"Algorithm: {algorithm}\n")  # Write the algorithm name
            
            # 获取该算法的运行时间
            time_key = f"{algorithm}_time"
            if time_key in data:
                run_time = data[time_key][0]  # 取出运行时间（假设运行时间是单个数值）
            else:
                run_time = None  # 如果没有时间记录，设为 None
            
            for record_FEs in record_FEs_list:
                if record_FEs < len(algorithm_avg_fitness[algorithm]['avg_fitness']):
                    fitness_value = algorithm_avg_fitness[algorithm]['avg_fitness'][record_FEs]
                    variance_value = algorithm_avg_fitness[algorithm]['variances'][record_FEs]
                    if fitness_value is not None:
                        # Format both decimal and scientific notation
                        f.write(f"{'':<20}{record_FEs:<25.3e}{fitness_value:<30.6f}{fitness_value:<25.6e}{variance_value:<30.6f}{variance_value:<25.6e}\n")
                else:
                    print(f"Warning: Record point {record_FEs} exceeds the available evaluations for {algorithm}.")
            
            # 记录最终点
            final_value = algorithm_avg_fitness[algorithm]['avg_fitness'][-1] if algorithm_avg_fitness[algorithm]['avg_fitness'][-1] is not None else "N/A"
            final_variance = algorithm_avg_fitness[algorithm]['variances'][-1] if algorithm_avg_fitness[algorithm]['variances'][-1] is not None else "N/A"
            inner_value = f"Fin:{len(algorithm_avg_fitness[algorithm]['avg_fitness']):.3e}"
            f.write(f"{'':<20}{inner_value:<25}{final_value:<30.6f}{final_value:<25.6e}{final_variance:<30.6f}{final_variance:<25.6e}\n")
            
            # 添加运行时间记录
            if run_time is not None:
                f.write(f"{'':<20}{'Run Time:':<25}{run_time:<30.6f}\n")
            
            # Add a separator between algorithms
            f.write("-" * 155 + "\n")
    
    print(f"Evaluation records have been saved to '{output_file_path}'.")

def save_to_excel(data, output_path, num_groups=1000):
    """
    将所有评估值保存在一个 Excel 表格中，其中首行表示评估次数，第一列是算法名称，
    每个运行数据占一行，按照给定的组数划分，记录每组的代表性列。

    Args:
        data (dict): 包含算法运行结果及运行时间的字典，格式为 {"Algorithm1": [[list1], [list2], ...], ...}
        output_path (str): 输出路径。
        num_groups (int): 需要划分的组数，默认是 1000 组。
    """
    # Initialize a list to hold all rows of the output
    all_rows = []
    

    for algorithm, runs in data.items():
        if "_time" in algorithm:  # 跳过时间记录的键
            continue
        
        runs = [make_monotonic_decreasing(run.copy()) for run in runs]
        # 获取最大列数，作为标准
        max_length = max(len(run) for run in runs)  # 获取最长行的列数
        step = max_length // num_groups + 1 # 计算每组的列数
        columns = ["Algorithm", "Run #"] + [f"{(i+1)*num_groups:.3e}" for i in range(step)]  # 科学计数法表示的评估次数

        # 处理每次独立运行
        for run_idx, run in enumerate(runs):
            if isinstance(run, float):
                run = [run]  # 将单个浮动值转换为列表
            # 选择每隔 step 列的数据
            row = [algorithm, run_idx + 1] + run[::num_groups]  # 每次运行的数据，选择每隔 step 列的数据
            all_rows.append(row)
        
        # 计算并添加均值行
        avg_fitness = [sum(values) / len(values) for values in zip(*runs)]  # 计算每个评估点的均值
        avg_row = [algorithm, "Avg"] + avg_fitness[::num_groups]  # 均值行，选择每隔 step 列的数据
        all_rows.append(avg_row)

        # 在每个算法之间加入空行
        all_rows.append([None] * len(columns))  # 用空行分隔不同算法

    # 创建 DataFrame
    df = pd.DataFrame(all_rows, columns=columns)  # 根据列数切割

    # 输出到 Excel
    output_file_path = f"{output_path}evaluation_record.xlsx"
    df.to_excel(output_file_path, index=False)

    print(f"Evaluation records have been saved to '{output_file_path}'.")

def plot_evaluation_curve(data, output_path, font_size, log_scale=False, show_variance=False):
    """
    绘制不同算法的评估值均值曲线，并可选添加方差带。

    Args:
        data (dict): 包含各算法评估值的字典，格式为
                     {"Algorithm1": [[list1], [list2], ...], "Algorithm2": [[list1], [list2], ...], ...}
        log_scale (bool): 是否对 y 轴使用对数坐标。
        show_variance (bool): 是否绘制方差带。
    """
    plt.figure(figsize=(9, 6))  # 设置图形大小

    for algorithm, runs in data.items():
        # 跳过时间记录字段
        if "_time" in algorithm:
            continue

        # 获取当前算法的所有运行数据
        max_length = max(len(run) for run in runs)  # 获取所有运行中最长的评估值列表长度
        avg_fitness = []  # 存储每个评估次数的均值
        std_fitness = []  # 存储每个评估次数的标准差

        # 遍历每个评估次数
        for i in range(max_length):
            values_at_i = [run[i] for run in runs if i < len(run)]  # 获取所有运行中第 i 次评估的值
            if values_at_i:  # 如果有运行达到了当前评估次数
                avg_fitness.append(np.mean(values_at_i))  # 计算均值
                std_fitness.append(np.std(values_at_i))   # 计算标准差
            else:
                avg_fitness.append(None)  # 如果没有值，填充 None
                std_fitness.append(None)  # 标准差也填充 None

        # 绘制曲线，跳过 None 值
        x = range(len(avg_fitness))
        y = [v for v in avg_fitness if v is not None]  # 过滤 None 值
        x = [i for i, v in enumerate(avg_fitness) if v is not None]  # 保留对应的 x 值
        std = [s for s in std_fitness if s is not None]  # 保留对应的标准差值

        # 绘制均值曲线
        line, = plt.plot(x, y, label=algorithm)

        # 绘制方差带（如果启用）
        if show_variance and std:
            plt.fill_between(x, np.array(y) - np.array(std), np.array(y) + np.array(std),
                             color=line.get_color(), alpha=0.2)

    # 设置对数坐标
    if log_scale:
        plt.yscale("log")

    # 设置字体大小
    plt.rcParams.update({'font.size': font_size})

    # 添加图例、标题和标签
    plt.xlabel("FEs", fontsize=font_size)
    plt.ylabel("Objective Value (log10)", fontsize=font_size)
    plt.title("Evaluation Curves for Different Algorithms", fontsize=font_size)
    plt.legend(fontsize=font_size)  # 显示图例并设置字体大小
    plt.grid(True)  # 添加网格线

    # 保存图像
    filename = "evaluation_curves.png"
    plt.savefig(f"{output_path}{filename}", bbox_inches='tight')
    print(f"Plot saved to '{output_path}{filename}'.")
    plt.close()

def _plot_evaluation_curve(data, output_path, glofes, font_size, log_scale=False, show_variance=False):
    """
    绘制不同算法的评估值均值曲线，并可选添加方差带。

    Args:
        data (dict): 包含各算法评估值的字典，格式为
                     {"Algorithm1": [[list1], [list2], ...], "Algorithm2": [[list1], [list2], ...], ...}
        glofes (dict): 每个算法对应的评估点数，格式为
                       {"Algorithm1": 500, "Algorithm2": 1000, ...}
        log_scale (bool): 是否对 y 轴使用对数坐标。
        show_variance (bool): 是否绘制方差带。
    """
    plt.figure(figsize=(6, 6))  # 设置图形大小

    # 为每个算法分配颜色
    colors = plt.cm.tab10(range(len(data)))  # 使用tab10颜色映射

    for j, (algorithm, runs) in enumerate(data.items()):
        # 跳过时间记录字段
        if "_time" in algorithm:
            continue

        # 获取当前算法的 GloFEs
        max_glofes = glofes.get(algorithm, 500)  # 默认值为 500

        # 对于 gloFEs 为 0 的情况，处理为全实线
        if max_glofes == 0:
            max_glofes = 0  # 如果 gloFEs 为 0，使用最大的评估点数


        # 获取当前算法的所有运行数据
        max_length = max(len(run) for run in runs)  # 获取所有运行中最长的评估值列表长度
        avg_fitness = []  # 存储每个评估次数的均值
        std_fitness = []  # 存储每个评估次数的标准差

        # 遍历每个评估次数
        for i in range(max_length):
            values_at_i = [run[i] for run in runs if i < len(run)]  # 获取所有运行中第 i 次评估的值
            if values_at_i:  # 如果有运行达到了当前评估次数
                avg_fitness.append(np.mean(values_at_i))  # 计算均值
                std_fitness.append(np.std(values_at_i))   # 计算标准差
            else:
                avg_fitness.append(None)  # 如果没有值，填充 None
                std_fitness.append(None)  # 标准差也填充 None

        # 绘制曲线，跳过 None 值
        x = range(len(avg_fitness))
        y = [v for v in avg_fitness if v is not None]  # 过滤 None 值
        x = [i for i, v in enumerate(avg_fitness) if v is not None]  # 保留对应的 x 值
        std = [s for s in std_fitness if s is not None]  # 保留对应的标准差值

        color = colors[j]  # 为当前算法分配一个颜色

        if max_glofes > 0:
            # 绘制虚线部分（评估点数之前）
            cutoff_idx = min(max_glofes, len(x))
            x1, y1 = x[:cutoff_idx], y[:cutoff_idx]
            plt.plot(x1, y1, label=algorithm, linestyle="--", color=color)

            # 绘制实线部分（评估点数之后）
            x2, y2 = x[cutoff_idx:], y[cutoff_idx:]
            plt.plot(x2, y2, linestyle="-", color=color)
        else:
            # 如果 GloFEs 为 0，全部绘制为实线
            plt.plot(x, y, label=algorithm, linestyle="-", color=color)

        # 绘制方差带（如果启用）
        if show_variance and std:
            plt.fill_between(x, np.array(y) - np.array(std), np.array(y) + np.array(std),
                             color=color, alpha=0.2)

    # 设置对数坐标
    if log_scale:
        plt.yscale("log")

    # 设置字体大小
    plt.rcParams.update({'font.size': font_size})

    # 添加图例、标题和标签
    plt.xlabel("FEs", fontsize=font_size)
    plt.ylabel("Objective Value (log10)", fontsize=font_size)
    plt.title("Evaluation Curves for Different Algorithms", fontsize=font_size)
    plt.legend(fontsize=font_size)  # 显示图例并设置字体大小
    plt.grid(True)  # 添加网格线

    # 保存图像
    filename = "evaluation_curves.png"
    plt.savefig(f"{output_path}{filename}", bbox_inches='tight')
    print(f"Plot saved to '{output_path}{filename}'.")
    plt.close()

# def plot_evaluation_curve_best_so_far(data, output_path, font_size, log_scale=False, show_variance=False):
#     """
#     绘制不同算法的评估值曲线 (best-so-far)，并可选添加方差带。

#     Args:
#         data (dict): 包含各算法评估值的字典，格式为
#                      {"Algorithm1": [[list1], [list2], ...], "Algorithm2": [[list1], [list2], ...], ...}
#         log_scale (bool): 是否对 y 轴使用对数坐标。
#         show_variance (bool): 是否绘制方差带。
#     """
#     plt.figure(figsize=(9, 6))  # 设置图形大小

#     for algorithm, runs in data.items():
#         # 跳过时间记录字段
#         if "_time" in algorithm:
#             continue

#         # 对每个运行的评估值列表进行单调递减处理
#         runs = [make_monotonic_decreasing(run.copy()) for run in runs]

#         # 获取当前算法的所有运行数据
#         max_length = max(len(run) for run in runs)  # 获取所有运行中最长的评估值列表长度
#         avg_fitness = []  # 存储每个评估次数的均值
#         std_fitness = []  # 存储每个评估次数的标准差

#         # 遍历每个评估次数
#         for i in range(max_length):
#             values_at_i = [run[i] for run in runs if i < len(run)]  # 获取所有运行中第 i 次评估的值
#             if values_at_i:  # 如果有运行达到了当前评估次数
#                 avg_fitness.append(np.mean(values_at_i))  # 计算均值
#                 std_fitness.append(np.std(values_at_i))   # 计算标准差
#             else:
#                 avg_fitness.append(None)  # 如果没有值，填充 None
#                 std_fitness.append(None)  # 标准差也填充 None

#         # 绘制曲线，跳过 None 值
#         x = range(len(avg_fitness))
#         y = [v for v in make_monotonic_decreasing(avg_fitness) if v is not None]  # 过滤 None 值
#         x = [i for i, v in enumerate(avg_fitness) if v is not None]  # 保留对应的 x 值
#         std = [s for s in std_fitness if s is not None]  # 保留对应的标准差值

#         # 绘制均值曲线
#         line, = plt.plot(x, y, label=algorithm)

#         # 绘制方差带（如果启用）
#         if show_variance and std:
#             plt.fill_between(x, np.array(y) - np.array(std), np.array(y) + np.array(std),
#                              color=line.get_color(), alpha=0.2)

#     # 设置对数坐标
#     if log_scale:
#         plt.yscale("log")

#     # 设置字体大小
#     plt.rcParams.update({'font.size': font_size})

#     # 添加图例、标题和标签
#     plt.xlabel("FEs", fontsize=font_size)
#     plt.ylabel("Objective Value (log10)", fontsize=font_size)
#     plt.title("Best-so-Far Evaluation Curves for Different Algorithms", fontsize=font_size)
#     plt.legend(fontsize=font_size)  # 显示图例并设置字体大小
#     plt.grid(True)  # 添加网格线

#     # 保存图像
#     filename = "evaluation_curves_best_so_far.png"
#     plt.savefig(f"{output_path}{filename}", bbox_inches='tight')
#     print(f"Plot saved to '{output_path}{filename}'.")
#     plt.close()

def plot_evaluation_curve_best_so_far(
    data, output_path, maxfes, font_size, log_scale=False, show_variance=False, eps=1e-12
):
    """
    中心曲线：算术均值（linear）
    方差带：在 log10 空间计算标准差，形成乘法对称带（/factor 与 *factor）
    """
    plt.figure(figsize=(9, 6))
    ax = plt.gca()

    for algorithm, runs in data.items():
        if "_time" in algorithm:
            continue

        # 每条 run 先做 best-so-far（单调不增）
        runs = [make_monotonic_decreasing(run.copy()) for run in runs]

        # 以最长 run 为准逐点统计
        max_length = int(maxfes)

        xs, centers, lows, highs = [], [], [], []
        for i in range(max_length):
            values_at_i = [run[i] for run in runs if i < len(run)]
            if not values_at_i:
                continue

            vals = np.asarray(values_at_i, dtype=float)
            vals = np.clip(vals, eps, None)  # 防止非正导致 log 失败

            # 中心：算术均值（不要再对聚合后的均值做单调化）
            c = vals.mean()
            xs.append(i)
            centers.append(c)

            # 方差带：log 空间 std -> 乘法因子
            if show_variance:
                std_log = np.log10(vals).std()
                factor = 10 ** std_log
                lows.append(c / factor)
                highs.append(c * factor)

        # 画均值
        line, = ax.plot(xs, centers, label=algorithm)

        # 画方差带
        if show_variance and len(xs) > 0:
            ax.fill_between(xs, lows, highs, color=line.get_color(), alpha=0.2)

    if log_scale:
        ax.set_yscale("log")

    plt.rcParams.update({'font.size': font_size})
    ax.set_xlabel("FEs", fontsize=font_size)
    ax.set_ylabel("Objective Value (log10)", fontsize=font_size)
    ax.set_title("Best-so-Far Evaluation Curves for Different Algorithms", fontsize=font_size)
    ax.legend(fontsize=font_size)
    ax.grid(True)

    filename = "evaluation_curves_best_so_far.png"
    plt.savefig(f"{output_path}{filename}", bbox_inches='tight')
    print(f"Plot saved to '{output_path}{filename}'.")
    plt.close()


def _plot_evaluation_curve_best_so_far(data, output_path, glofes, font_size, log_scale=False, show_variance=False):
    """
    绘制不同算法的评估值曲线 (best-so-far)，并可选添加方差带。

    Args:
        data (dict): 包含各算法评估值的字典，格式为
                     {"Algorithm1": [[list1], [list2], ...], "Algorithm2": [[list1], [list2], ...], ...}
        glofes (dict): 每个算法对应的评估点数，格式为
                       {"Algorithm1": 500, "Algorithm2": 1000, ...}
        log_scale (bool): 是否对 y 轴使用对数坐标。
        show_variance (bool): 是否绘制方差带。
    """
    plt.figure(figsize=(6, 6))  # 设置图形大小

    # 为每个算法分配颜色
    colors = plt.cm.tab10(range(len(data)))  # 使用tab10颜色映射

    for j, (algorithm, runs) in enumerate(data.items()):
        # 跳过时间记录字段
        if "_time" in algorithm:
            continue

        # 获取当前算法的 GloFEs
        max_glofes = glofes.get(algorithm, 500)  # 默认值为 500

        # 对于 gloFEs 为 0 的情况，处理为全实线
        if max_glofes == 0:
            max_glofes = 0  # 如果 gloFEs 为 0，使用最大的评估点数

        # 对每个运行的评估值列表进行单调递减处理
        runs = [make_monotonic_decreasing(run.copy()) for run in runs]

        # 获取当前算法的所有运行数据
        max_length = max(len(run) for run in runs)  # 获取所有运行中最长的评估值列表长度
        avg_fitness = []  # 存储每个评估次数的均值
        std_fitness = []  # 存储每个评估次数的标准差

        # 遍历每个评估次数
        for i in range(max_length):
            values_at_i = [run[i] for run in runs if i < len(run)]  # 获取所有运行中第 i 次评估的值
            if values_at_i:  # 如果有运行达到了当前评估次数
                avg_fitness.append(np.mean(values_at_i))  # 计算均值
                std_fitness.append(np.std(values_at_i))   # 计算标准差
            else:
                avg_fitness.append(None)  # 如果没有值，填充 None
                std_fitness.append(None)  # 标准差也填充 None

        # 绘制曲线，跳过 None 值
        x = range(len(avg_fitness))
        y = [v for v in avg_fitness if v is not None]  # 过滤 None 值
        x = [i for i, v in enumerate(avg_fitness) if v is not None]  # 保留对应的 x 值
        std = [s for s in std_fitness if s is not None]  # 保留对应的标准差值

        color = colors[j]  # 为当前算法分配一个颜色

        if max_glofes > 0:
            # 绘制虚线部分（评估点数之前）
            cutoff_idx = min(max_glofes, len(x))
            x1, y1 = x[:cutoff_idx], y[:cutoff_idx]
            plt.plot(x1, y1, label=algorithm, linestyle="--", color=color)

            # 绘制实线部分（评估点数之后）
            x2, y2 = x[cutoff_idx:], y[cutoff_idx:]
            plt.plot(x2, y2, linestyle="-", color=color)
        else:
            # 如果 GloFEs 为 0，全部绘制为实线
            plt.plot(x, y, label=algorithm, linestyle="-", color=color)

        # 绘制方差带（如果启用）
        if show_variance and std:
            plt.fill_between(x, np.array(y) - np.array(std), np.array(y) + np.array(std),
                             color=color, alpha=0.2)

    # 设置对数坐标
    if log_scale:
        plt.yscale("log")

    # 设置字体大小
    plt.rcParams.update({'font.size': font_size})

    # 添加图例、标题和标签
    plt.xlabel("FEs", fontsize=font_size)
    plt.ylabel("Objective Value (log10)", fontsize=font_size)
    plt.title("Best-so-Far Evaluation Curves for Different Algorithms", fontsize=font_size)
    plt.legend(fontsize=font_size)  # 显示图例并设置字体大小
    plt.grid(True)  # 添加网格线

    # 保存图像
    filename = "evaluation_curves_best_so_far.png"
    plt.savefig(f"{output_path}{filename}", bbox_inches='tight')
    print(f"Plot saved to '{output_path}{filename}'.")
    plt.close()

def plot_time_consumption(data, output_path, interval=50000):
    """
    绘制时间消耗虚线，并确保每个点刚好对齐到 x 轴的刻度点。

    Args:
        data (dict): Time consumption data.
        output_path (str): Path to save the output plot.
        interval (int): Number of steps between time records.
    """
    plt.figure(figsize=(10, 6))

    max_evaluations = 0  # 用于记录最大评估值
    for algorithm, runs in data.items():
        if "_interval_times" not in algorithm:
            continue

        interval_times = data[algorithm]
        avg_times = [
            sum(t_list) / len(t_list) if t_list else None
            for t_list in zip(*interval_times)
        ]
        time_x = [interval * (i + 1) for i in range(len(avg_times)) if avg_times[i] is not None]
        time_y = [avg_times[i] for i in range(len(avg_times)) if avg_times[i] is not None]

        # 绘制虚线
        plt.plot(
            time_x, time_y, linestyle="--", label=algorithm.replace("_interval_times", "")
        )

        # 更新最大评估值
        if time_x:
            max_evaluations = max(max_evaluations, max(time_x))

    # 设置 x 轴刻度为每个 interval 的倍数
    x_ticks = list(range(interval, max_evaluations + interval, interval))
    plt.xticks(x_ticks)  # 设置 x 轴刻度

    # 设置 x 轴和 y 轴标签
    plt.xlabel("Number of Evaluations")
    plt.ylabel("Time (Seconds)")
    plt.title("Time Consumption per Interval")

    # 添加图例和网格线
    plt.legend()
    plt.grid(True)

    # 保存图片
    plt.savefig(f"{output_path}/time_consumption.png")
    plt.close()

def plot_target_based_ecdf(data, output_path, target_values, log_scale=False, calculate_auc=False, calculate_aocc=False):
    """
    绘制不同算法的 Target-Based ECDF 曲线，并根据需要计算 AUC 和 AOCC。
    
    Args:
        data (dict): 包含各算法评估值的字典，格式为
                     {"Algorithm1": [[list1], [list2], ...], "Algorithm2": [[list1], [list2], ...], ...}
        output_path (str): 图像保存路径。
        target_values (list): 目标值集合 Z，例如 [10, 20, 30]。
        log_scale (bool): 是否对 y 轴使用对数坐标。
        calculate_auc (bool): 是否计算每个算法的 AUC，并绘制柱状图。
        calculate_aocc (bool): 是否计算每个算法的 AOCC，并绘制柱状图。
        z_max (float): 用于 AOCC 计算的最大目标值，仅在 calculate_aocc=True 时有效。
    """
    plt.figure(figsize=(10, 6))  # 设置图形大小
    auc_results = {}  # 存储每个算法的 AUC 结果
    aocc_results = {}  # 存储每个算法的 AOCC 结果
    z_max = max(target_values)

    # 遍历每个算法的数据
    for algorithm, runs in data.items():
        # 跳过时间记录字段
        if "_time" in algorithm:
            continue
        runs = [make_monotonic_decreasing(run.copy()) for run in runs]
        max_length = max(len(run) for run in runs)  # 获取最长运行的评估值列表长度
        ecdf_values = []  # 存储每个评估次数的 ECDF 值

        # 遍历每个评估次数
        for t in range(max_length):
            success_counts = []  # 统计每个目标值的成功次数

            # 遍历目标值
            for target in target_values:
                count = 0
                # 遍历所有运行
                for run in runs:
                    if t < len(run) and run[t] <= target:  # 如果在第 t 次评估达到目标
                        count += 1
                success_counts.append(count / len(runs))  # 计算当前目标的成功率

            # 计算当前评估次数的 ECDF 值
            ecdf = sum(success_counts) / len(target_values)  # 目标值的平均成功率
            ecdf_values.append(ecdf)

        # 绘制曲线
        plt.plot(range(max_length), ecdf_values, label=algorithm)

        # 如果需要计算 AUC，使用 Simpson 数值积分法
        if calculate_auc:
            auc = simpson(ecdf_values, dx=1)  # 使用评估次数 (t) 作为步长 dx
            auc_results[algorithm] = auc

        # 如果需要计算 AOCC，计算每次运行的 AOCC 并取平均
        if calculate_aocc and z_max is not None:
            aocc = 0
            for run in runs:
                aocc += sum(max(0, z_max - value) for value in run)  # 矩形面积
            aocc_results[algorithm] = aocc / len(runs)  # 平均 AOCC

    # 设置对数坐标
    if log_scale:
        plt.yscale("log")

    # 添加图例、标题、标签和网格线
    plt.xlabel("Number of Evaluations")
    plt.ylabel("ECDF")
    plt.title("Target-Based ECDF for Different Algorithms")
    plt.legend(loc="best")  # 图例显示在最佳位置
    plt.grid(True)  # 添加网格线

    # 保存 ECDF 曲线图像
    filename = "target_based_ecdf.png"
    full_path = f"{output_path}{filename}"
    plt.savefig(full_path)
    print(f"Target-Based ECDF plot saved to '{full_path}'.")
    plt.close()

    # 如果需要计算 AUC，绘制 AUC 柱状图
    if calculate_auc:
        plt.figure(figsize=(10, 6))
        algorithms = list(auc_results.keys())
        auc_values = list(auc_results.values())
        
        # 绘制柱状图
        plt.bar(algorithms, auc_values, color="skyblue")
        plt.xlabel("Algorithms")
        plt.ylabel("AUC")
        plt.title("AUC of Target-Based ECDF for Different Algorithms")
        
        # 保存柱状图
        filename = "target_based_ecdf_auc.png"
        full_path = f"{output_path}{filename}"
        plt.savefig(full_path)
        print(f"AUC bar chart saved to '{full_path}'.")
        plt.close()

    # 如果需要计算 AOCC，绘制 AOCC 柱状图
    if calculate_aocc:
        plt.figure(figsize=(10, 6))
        algorithms = list(aocc_results.keys())
        aocc_values = list(aocc_results.values())
        
        # 绘制柱状图
        plt.bar(algorithms, aocc_values, color="lightgreen")
        plt.xlabel("Algorithms")
        plt.ylabel("AOCC")
        plt.title("AOCC of Target-Based ECDF for Different Algorithms")
        
        # 保存柱状图
        filename = "target_based_ecdf_aocc.png"
        full_path = f"{output_path}{filename}"
        plt.savefig(full_path)
        print(f"AOCC bar chart saved to '{full_path}'.")
        plt.close()

def plot_eaf(data, output_path, target_value, max_alpha=0.8):
    """
    绘制优化曲线，并从目标点开始动态填充阴影，表示目标值达到的频率。

    Args:
        data (dict): 包含各算法评估值的字典，格式为
                     {"Algorithm1": [[list1], [list2], ...], "Algorithm2": [[list1], [list2], ...], ...}
        output_path (str): 图像保存路径。
        target_value (float): 给定的目标函数值。
        max_alpha (float): 最大透明度值(默认 1.0)。
    """
    for algorithm, runs in data.items():
        if "_time" in algorithm:
            continue
        runs = [make_monotonic_decreasing(run.copy()) for run in runs]
        max_length = max(len(run) for run in runs)  # 获取最长运行的评估值列表长度
        min_y = min(min(run) for run in runs)  # 动态设置 y 轴的最小值
        max_y = max(max(run) for run in runs)  # 动态设置 y 轴的最大值

        # 创建图像
        plt.figure(figsize=(10, 6))

        # 每次运行的灰度增量，根据总运行次数动态调整
        gray_increment = max_alpha / len(runs)

        # 创建一个矩阵来累加阴影值
        shading_matrix = np.zeros((max_length,))

        # 遍历每次运行，逐条更新阴影
        for run_idx, run in enumerate(runs):
            t_values = np.arange(len(run))  # 当前曲线的 t 值
            y_values = np.array(run)  # 当前曲线的 y 值

            # 找到从目标值开始的区域
            target_mask = y_values <= target_value  # 是否达到目标值
            if np.any(target_mask):  # 如果达到了目标值
                first_target_index = np.argmax(target_mask)  # 第一次达到目标值的索引

                # 更新阴影矩阵，目标点之后均填充灰度
                shading_matrix[first_target_index:] = np.clip(
                    shading_matrix[first_target_index:] + gray_increment, 0, max_alpha
                )

                # 从目标点到后续点逐步绘制阴影
                plt.fill_between(
                    t_values[first_target_index:],  # x 区间
                    y_values[first_target_index:],  # 下界
                    max_y,  # 上界
                    color="gray", alpha=shading_matrix[first_target_index], step="post"
                )

            # 绘制当前曲线
            plt.step(t_values, y_values, where="post", label=f"Run {run_idx+1}", alpha=0.7)

        # 添加目标值的水平线
        plt.axhline(target_value, color="red", linestyle="--", linewidth=1.5, label="Target Value")

        # 设置对数坐标
        plt.yscale("log")  # 对数化处理目标值

        # 图形设置
        plt.xlabel("Number of Evaluations (t)")
        plt.ylabel("Objective Value (log scale)")
        plt.title(f"EAF for {algorithm} (Target: {target_value})")
        plt.legend(loc="best")

        # 保存图像
        filename = f"{algorithm}_eaf.png"
        full_path = f"{output_path}{filename}"
        plt.savefig(full_path)
        print(f"EAF plot with shading saved to '{full_path}'.")
        plt.close()

def plot_eaf_based_ecdf(data, output_path, z_min, z_max, calculate_auc=False, calculate_aocc=False):
    """
    绘制不同算法的 EAF-Based ECDF 曲线，并在同一图中对比。
    根据需要计算每个算法的 AUC 和 AOCC，并保存柱状图。

    Args:
        data (dict): 包含多次运行结果的字典，每个算法包含其运行列表。例如：
                     {"Algorithm1": [[list1], [list2], ...], "Algorithm2": [[list1], [list2], ...]}。
        z_min (float): 目标值区间的下界。
        z_max (float): 目标值区间的上界。
        output_path (str): 图像保存路径。
        calculate_auc (bool): 是否计算每个算法的 AUC，并绘制柱状图。
        calculate_aocc (bool): 是否计算每个算法的 AOCC，并绘制柱状图。
    """
    target_values = np.linspace(z_min, z_max, 1000)  # 离散化目标值区间
    plt.figure(figsize=(10, 6))  # 设置图形大小
    auc_results = {}  # 存储每个算法的 AUC 结果
    aocc_results = {}  # 存储每个算法的 AOCC 结果

    # 遍历每个算法
    for algorithm_name, runs in data.items():
        # 跳过时间记录字段
        if "_time" in algorithm_name:
            continue
        runs = [make_monotonic_decreasing(run.copy()) for run in runs]
        t_max = max(len(run) for run in runs)  # 决定最大评估次数
        ecdf_values = []  # 存储每个评估次数 t 的 ECDF 值

        # 对每个评估次数 t，计算对应的 ECDF 值
        for t in range(t_max):
            # 对每个 t，计算 \hat{\alpha}(t, z) 并对目标值区间 [z_min, z_max] 积分
            alpha_tz = []
            for z in target_values:
                count = sum(1 for run in runs if t < len(run) and run[t] <= z)
                alpha_tz.append(count / len(runs))
            # 数值积分计算 F_{\hat{\alpha}}(t)
            ecdf_value = simpson(y=alpha_tz, x=target_values) / (z_max - z_min)
            ecdf_values.append(ecdf_value)

        # 绘制曲线
        plt.plot(range(t_max), ecdf_values, label=algorithm_name)

        # 如果需要计算 AUC，使用 Simpson 数值积分法
        if calculate_auc:
            auc = simpson(ecdf_values, dx=1)  # 使用评估次数 (t) 作为步长 dx
            auc_results[algorithm_name] = auc

        # 如果需要计算 AOCC，计算每次运行的 AOCC 并取平均
        if calculate_aocc:
            aocc = 0
            for run in runs:
                aocc += sum(max(0, z_max - value) for value in run[:t_max])  # 计算矩形面积
            aocc_results[algorithm_name] = aocc / len(runs)  # 平均 AOCC

    # 设置图形
    plt.xlabel("Number of Evaluations (t)")
    plt.ylabel("EAF-Based ECDF")
    plt.title("EAF-Based ECDF for Different Algorithms")
    plt.legend(loc="best")
    plt.grid(True)

    # 保存 EAF-Based ECDF 曲线图像
    filename = "eaf_based_ecdf.png"
    full_path = f"{output_path}{filename}"
    plt.savefig(full_path)
    print(f"EAF-Based ECDF plot saved to '{full_path}'.")
    plt.close()

    # 如果需要计算 AUC，绘制 AUC 柱状图
    if calculate_auc:
        plt.figure(figsize=(10, 6))
        algorithms = list(auc_results.keys())
        auc_values = list(auc_results.values())
        
        # 绘制柱状图
        plt.bar(algorithms, auc_values, color="skyblue")
        plt.xlabel("Algorithms")
        plt.ylabel("AUC")
        plt.title("AUC of EAF-Based ECDF for Different Algorithms")
        
        # 保存柱状图
        filename = "eaf_based_ecdf_auc.png"
        full_path = f"{output_path}{filename}"
        plt.savefig(full_path)
        print(f"AUC bar chart saved to '{full_path}'.")
        plt.close()

    # 如果需要计算 AOCC，绘制 AOCC 柱状图
    if calculate_aocc:
        plt.figure(figsize=(10, 6))
        algorithms = list(aocc_results.keys())
        aocc_values = list(aocc_results.values())
        
        # 绘制柱状图
        plt.bar(algorithms, aocc_values, color="lightgreen")
        plt.xlabel("Algorithms")
        plt.ylabel("AOCC")
        plt.title("AOCC of EAF-Based ECDF for Different Algorithms")
        
        # 保存柱状图
        filename = "eaf_based_ecdf_aocc.png"
        full_path = f"{output_path}{filename}"
        plt.savefig(full_path)
        print(f"AOCC bar chart saved to '{full_path}'.")
        plt.close()

def plot_bar_chart(categories, values, title="Bar Chart", xlabel="Categories", ylabel="Values", bar_colors=None, output_path=None, rotate_x_labels=False):
    """
    绘制柱状图，并支持设置每个柱子的颜色和 X 轴标签是否倾斜。

    Args:
        categories (list): 类别名称列表。
        values (list): 每个类别对应的值。
        title (str): 图表标题。
        xlabel (str): x 轴标签。
        ylabel (str): y 轴标签。
        bar_colors (list): 每个柱子的颜色列表，长度需与 values 相同。
        output_path (str): 如果提供路径，则保存图片到该路径。
        rotate_x_labels (bool): 是否旋转 X 轴标签。
    """
    # 检查输入数据是否一致
    if len(categories) != len(values):
        raise ValueError("Categories and values must have the same length.")
    if bar_colors and len(bar_colors) != len(values):
        raise ValueError("bar_colors must have the same length as values if provided.")

    # 设置柱状图
    x = np.arange(len(categories))  # x 轴位置
    plt.figure(figsize=(6, 6))     # 设置图形大小

    # 使用颜色列表绘制柱状图
    if bar_colors:
        plt.bar(x, values, color=bar_colors, alpha=0.8)  # 设置每个柱子的颜色
    else:
        plt.bar(x, values, color='skyblue', alpha=0.8)   # 默认颜色

    # 添加标签和标题
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=12)

    # 设置 X 轴标签是否旋转
    if rotate_x_labels:
        plt.xticks(x, categories, rotation=45, fontsize=10)  # 倾斜 45 度
    else:
        plt.xticks(x, categories, rotation=0, fontsize=10)   # 不旋转

    # 显示网格
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 保存或显示图像
    if output_path:
        plt.savefig(output_path, bbox_inches='tight')
        print(f"Bar chart saved to {output_path}")
    else:
        plt.show()

def create_image_grid(image_paths, output_path, rows, cols, figsize=(15, 10), titles=None):
    """
    生成组图，将多张图片按指定行列布局拼接。

    Args:
        image_paths (list): 图片路径列表，按顺序提供。
        output_path (str): 输出组图的保存路径。
        rows (int): 组图的行数。
        cols (int): 组图的列数。
        figsize (tuple): 图像整体大小，默认为 (15, 10)。
        titles (list): 每张图片的标题，默认为 None。

    Raises:
        ValueError: 如果图片数量与行列布局不匹配，抛出错误。
    """
    # 检查图片数量是否匹配行列布局
    if len(image_paths) > rows * cols:
        raise ValueError("Number of images exceeds grid capacity (rows * cols).")

    # 创建图形对象
    fig, axes = plt.subplots(rows, cols, figsize=figsize)

    # 确保 axes 是二维数组
    axes = axes.ravel() if rows * cols > 1 else [axes]

    # 加载图片并绘制
    for i, img_path in enumerate(image_paths):
        img = Image.open(img_path)  # 打开图片
        axes[i].imshow(img)
        axes[i].axis('off')  # 去掉坐标轴

        # 添加标题
        if titles and i < len(titles):
            axes[i].set_title(titles[i], fontsize=12)

    # 隐藏多余的子图
    for j in range(len(image_paths), rows * cols):
        axes[j].axis('off')

    # 调整布局并保存
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    print(f"Image grid saved to {output_path}")
    plt.close()