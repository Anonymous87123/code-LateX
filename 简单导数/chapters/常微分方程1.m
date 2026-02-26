% 作业1：利用 dsolve 求解 Malthus 和 Logistic 模型的精确解

% 定义符号变量 P(t)代表种群数量, t代表时间, r为增长率, K为环境容量, P0为初始数量
syms P(t) r K P0 

%% 1. 求解 Malthus 模型
eqn_m = diff(P, t) == r * P;     % 定义微分方程
cond_m = P(0) == P0;             % 定义初始条件
P_malthus = dsolve(eqn_m, cond_m); % 求精确解

fprintf('Malthus 模型的精确解为:\n');
disp(P_malthus);

%% 2. 求解 Logistic 模型
eqn_l = diff(P, t) == r * P * (1 - P/K); 
cond_l = P(0) == P0;
P_logistic = dsolve(eqn_l, cond_l);

fprintf('\nLogistic 模型的精确解为:\n');
disp(P_logistic);