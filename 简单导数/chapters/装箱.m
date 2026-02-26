% 装箱问题 - 平板车问题 (The Railroad Flatcar Problem)

% --- 1. 问题数据输入 ---
% C1 到 C7 的属性
t = [48.7; 52.0; 61.3; 72.0; 48.7; 52.0; 64.0]; % 厚度 (cm)
w = [2000; 3000; 1000; 500;  4000; 2000; 1000]; % 重量 (kg)
n = [8; 7; 9; 6; 6; 4; 8];                      % 可用数量

% 平板车限制条件 (转换为统一单位: cm, kg)
L_max = 10.2 * 100;   % 平板车最大长度 10.2m = 1020cm
W_max = 40 * 1000;    % 平板车最大载重 40t = 40000kg
S_max = 302.7;        % C5, C6, C7 特别厚度限制

% --- 2. 目标函数 ---
% 决策变量排布: X = [平板车1的C1~C7, 平板车2的C1~C7]' 
% 目标是最大化已装载的总厚度 = 最小化 (-总厚度)
f = -[t; t]; 

% --- 3. 约束条件 (A * X <= b) ---
% 总共有 13 个不等式约束
A = zeros(13, 14);
b = zeros(13, 1);

% 1-2: 长度约束 (平板车1 和 平板车2)
A(1, 1:7) = t'; b(1) = L_max;
A(2, 8:14) = t'; b(2) = L_max;

% 3-4: 重量约束 (平板车1 和 平板车2)
A(3, 1:7) = w'; b(3) = W_max;
A(4, 8:14) = w'; b(4) = W_max;

% 5-6: C5, C6, C7的特别厚度限制 (平板车1 和 平板车2)
A(5, 5:7) = t(5:7)'; b(5) = S_max;
A(6, 12:14) = t(5:7)'; b(6) = S_max;

% 7-13: 每种集装箱的总可用数量约束 (x_i1 + x_i2 <= n_i)
for i = 1:7
    A(6+i, i) = 1;     % 对应平板车1的箱子i
    A(6+i, i+7) = 1;   % 对应平板车2的箱子i
    b(6+i) = n(i);
end

% --- 4. 变量范围与整数约束 ---
lb = zeros(14, 1);     % 数量至少为 0
ub = [n; n];           % 理论上限为各集装箱的最大可用量
intcon = 1:14;         % 所有 14 个变量均为整数

% --- 5. 求解 ---
options = optimoptions('intlinprog', 'Display', 'off'); % 关闭迭代输出保持简洁
[x, fval, exitflag, output] = intlinprog(f, intcon, A, b, [], [], lb, ub, options);

% --- 6. 输出结果 ---
if exitflag > 0
    % 将一维结果转回 7x2 矩阵以便于查看
    % 第1列为平板车1，第2列为平板车2
    solution = reshape(round(x), 7, 2); 
    
    fprintf('======= 优化成功 =======\n');
    fprintf('最小浪费空间(每节车): %.2f cm\n', (2 * L_max - (-fval)) / 2); % 或者总浪费空间 (2040 - (-fval))
    fprintf('装载的总厚度: %.2f cm (总容量: 2040 cm)\n\n', -fval);
    
    disp('装载方案 (行=C1至C7集装箱, 列=平板车1和2):');
    disp(array2table(solution, 'VariableNames', {'Flatcar_1', 'Flatcar_2'}, ...
        'RowNames', {'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7'}));
        
    % 验证约束消耗
    len1 = sum(solution(:, 1) .* t);
    len2 = sum(solution(:, 2) .* t);
    wt1  = sum(solution(:, 1) .* w);
    wt2  = sum(solution(:, 2) .* w);
    spec1 = sum(solution(5:7, 1) .* t(5:7));
    spec2 = sum(solution(5:7, 2) .* t(5:7));
    
    fprintf('\n======= 资源消耗验证 =======\n');
    fprintf('平板车 1: 占用长度 %.2f cm (上限 1020), 重量 %d kg (上限 40000)\n', len1, wt1);
    fprintf('         特殊限制厚度 %.2f cm (上限 302.7)\n', spec1);
    fprintf('平板车 2: 占用长度 %.2f cm (上限 1020), 重量 %d kg (上限 40000)\n', len2, wt2);
    fprintf('         特殊限制厚度 %.2f cm (上限 302.7)\n', spec2);
else
    fprintf('求解失败，退出标志为 %d\n', exitflag);
end