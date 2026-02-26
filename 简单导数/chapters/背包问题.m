% 钢管切割问题的 MATLAB 求解代码

% 1. 定义目标函数系数 (对应7种模式的余料长度)
f = [3; 1; 3; 3; 1; 1; 3];

% 2. 定义不等式约束矩阵 A 和向量 b (形式为 A*x <= b)
% 由于我们的需求约束是 >=，需要等式两边同乘 -1 转化为 <=
% 约束顺序依次为：4米钢管、6米钢管、8米钢管
A = -[4, 3, 2, 1, 1, 0, 0;
      0, 1, 0, 2, 1, 3, 0;
      0, 0, 1, 0, 1, 0, 2];
b = -[50; 20; 15];

% 3. 定义整数变量索引 (所有7个决策变量都必须是整数)
intcon = 1:7;

% 4. 定义变量下界 (不能切割负数根)
lb = zeros(7, 1);
% 变量没有明确的上界，设为空
ub = []; 

% 5. 求解整数规划问题
% 屏蔽迭代过程的冗长输出以保持控制台整洁
options = optimoptions('intlinprog', 'Display', 'off');
[x, fval, exitflag] = intlinprog(f, intcon, A, b, [], [], lb, ub, options);

% 6. 输出结果
if exitflag > 0
    disp('--- 寻找到最优切割方案 ---');
    for i = 1:7
        if x(i) > 0
            fprintf('采用 模式 %d: %d 根\n', i, round(x(i)));
        end
    end
    fprintf('--------------------------\n');
    fprintf('最少余料总长度: %d 米\n', round(fval));
    
    % 验证实际产出数量
    produce_4m = 4*x(1) + 3*x(2) + 2*x(3) + x(4) + x(5);
    produce_6m = x(2) + 2*x(4) + x(5) + 3*x(6);
    produce_8m = x(3) + x(5) + 2*x(7);
    fprintf('\n--- 实际产出核对 ---\n');
    fprintf('4米钢管: 生产 %d 根 (需求 50)\n', round(produce_4m));
    fprintf('6米钢管: 生产 %d 根 (需求 20)\n', round(produce_6m));
    fprintf('8米钢管: 生产 %d 根 (需求 15)\n', round(produce_8m));
else
    disp('未找到可行解，请检查约束条件。');
end