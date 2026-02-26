% 作业2：利用 ode45 求解微分方程组的数值解

% 设定基础参数 (对应图片中未加入e的基础参数)
r1 = 1; lambda1 = 0.1;   % 食物鱼的自然增长率与被捕食率
r2 = 0.5; lambda2 = 0.02; % 鲨鱼的死亡率与捕食增长率

% 定义微分方程组，x(1)为食物鱼，x(2)为鲨鱼
% 注意：odefun 必须接受 (t, x) 两个参数，即使方程是自治的（不显含t）
odefun = @(t, x) [x(1) * (r1 - lambda1 * x(2)); 
                  x(2) * (-r2 + lambda2 * x(1))];

tspan = [0 50]; % 设定求解时间区间
x0 = [25; 2];   % 设定初始种群数量 x1(0)=25, x2(0)=2

% 求解数值解
[t, x] = ode45(odefun, tspan, x0);

% 绘制时间序列图
figure;
plot(t, x(:,1), 'b-', 'LineWidth', 1.5); hold on;
plot(t, x(:,2), 'r-', 'LineWidth', 1.5);
title('Volterra 模型数值解时间序列');
xlabel('时间 t'); ylabel('种群数量');
legend('食用鱼 (x_1)', '鲨鱼 (x_2)');
grid on;