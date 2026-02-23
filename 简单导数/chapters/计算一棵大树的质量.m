% 作业2: 估计校园内树木的质量范围

% 1. 输入实测参数 (假设我们在校园里测得以下数据)
C = 1.5;         % 树干胸径处的周长 (单位: 米)
H = 10.0;        % 树干的估计高度 (单位: 米)
f = 0.45;        % 树干形数 (Form factor，用于修正圆柱体体积带来的高估)

% 常见木材(含水)的密度范围 (单位: kg/m^3)
rho_min = 700;   % 松木/较干木材
rho_max = 950;   % 阔叶林/含水量高的木材

% 2. 数学计算
R = C / (2 * pi);           % 计算半径
V_cylinder = pi * R^2 * H;  % 理想圆柱体积
V_actual = V_cylinder * f;  % 修正后的实际预估体积

% 计算质量范围 (质量 = 密度 * 体积)
Mass_min = rho_min * V_actual;
Mass_max = rho_max * V_actual;

% 3. 结果输出
fprintf('--- 树木质量估计报告 ---\n');
fprintf('树干周长: %.2f m, 树高: %.2f m\n', C, H);
fprintf('预估树干体积: %.4f 立方米\n', V_actual);
fprintf('估计该树木的质量范围为: %.2f kg 到 %.2f kg\n', Mass_min, Mass_max);