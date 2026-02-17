from math import exp, sin
from numpy import min, max, array, argmax, ndarray


def step(x, y):
    # 这里是二阶混沌系统，实际计算时只取y作为混沌序列的元素
    a = sin(2*x)
    b = sin(3/2*y)
    return a+b, a


def pre_run():
    # 预载波
    y = x = exp(-1)
    i = 0
    while i < 16384:
        x, y = step(x, y)
        i = i + 1
    return x, y


def run(x, y, n):
    # 正式的载波，这里第一次载波与第二次载波共用一个格式
    ly = []
    i = 0
    while i < n:
        x, y = step(x, y)
        i = i + 1
        ly.append(y)
    return x, y, ly


def get(arr, a, b):
    # 将变量转换为[a,b]内的数
    if type(arr) is ndarray:
        arr = (arr - min(arr)) / (max(arr) - min(arr))
        arr = arr * (b - a) + a
    return arr


def maximum(fun, arr):
    # 得到最大点和最大值
    lst = []
    for x in arr:
        lst.append(fun(x))
    arr1 = array(lst)
    r = max(arr1)
    p = arr[argmax(arr1)]
    return p, r


def chaotic_opt():
    # 定义的问题
    def f(u):
        v = exp(-u ** 2) + sin(10 * u)
        return v
    # 区间，载波的采样数和细搜索步长
    A = -3
    B = 3
    n = 1024
    alpha = 1e-1

    # 粗搜索（第一次载波）
    x, y = pre_run()
    x, y, ly = run(x, y, n)
    arry = array(ly)
    points = get(arry, A, B)
    bp, br = maximum(f, points)
    print(bp, br)
    # 细搜索（第二次载波）
    x, y, ly = run(x, y, n)
    arry = array(ly)
    points = get(arry, bp - alpha, bp + alpha)
    bp, br = maximum(f, points)

    print(bp, br)


chaotic_opt()






















