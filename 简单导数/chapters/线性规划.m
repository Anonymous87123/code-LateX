% 饮食问题的整数线性规划求解 (Diet Problem with intlinprog)

% 1. 定义目标函数系数 (Price $/portion)
% 分别对应: Oats, Chicken, Eggs, Milk, Kuchen, Beans
f = [30; 240; 130; 90; 200; 60];

% 2. 定义整数变量的索引
% 问题中的 6 个变量 (份数) 都被要求为整数
intcon = 1:6;

% 3. 定义不等式约束 (A * x <= b)
% 营养要求是 >= (至少)，所以将系数矩阵和常数向量乘以 -1
% 行1: Energy (Kcal) >= 2000
% 行2: Proteins (grams) >= 55
% 行3: Calcium (mg) >= 800
A = - [110, 205, 160, 160, 420, 260;
       4,   32,  13,  8,   4,   14;
       2,   12,  54,  285, 22,  80];

b = - [2000; 
       55; 
       800];

% 4. 定义等式约束 (如果没有等式约束则设为空)
Aeq = [];
beq = [];

% 5. 定义变量的下限和上限 (Lower Bounds and Upper Bounds)
lb = zeros(6, 1); % 食物份数不能为负数
% 对应: Oats, Chicken, Eggs, Milk, Kuchen, Beans 的每日份数上限
ub = [4; 3; 2; 8; 2; 2]; 

% 6. 使用 intlinprog 函数求解
options = optimoptions('intlinprog','Display','iter'); % 显示迭代过程
[x, fval, exitflag, output] = intlinprog(f, intcon, A, b, Aeq, beq, lb, ub, options);

% 7. 打印结果
if exitflag > 0
    fprintf('\n========== 优化成功 ==========\n');
    fprintf('最低饮食成本为: $%.2f\n', fval);
    fprintf('\n推荐的每日食物份数搭配如下：\n');
    fprintf('燕麦 (Oats)   : %d 份\n', x(1));
    fprintf('鸡肉 (Chicken): %d 份\n', x(2));
    fprintf('鸡蛋 (Eggs)   : %d 份\n', x(3));
    fprintf('牛奶 (Milk)   : %d 份\n', x(4));
    fprintf('糕点 (Kuchen) : %d 份\n', x(5));
    fprintf('豆类 (Beans)  : %d 份\n', x(6));
else
    fprintf('\n优化失败，退出标志为: %d\n', exitflag);
    disp(output);
end