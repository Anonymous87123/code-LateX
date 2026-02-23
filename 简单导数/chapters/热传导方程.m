% 求解一维热传导方程的 MATLAB 示例
function solve_heat_equation()
    m = 0; % 空间坐标几何对称性 (0表示一维平板)
    x = linspace(0, 1, 100); % 空间网格
    t = linspace(0, 5, 100); % 时间网格
    
    sol = pdepe(m, @pdefun, @icfun, @bcfun, x, t);
    u = sol(:,:,1);
    
    surf(x, t, u);
    title('一维热传导方程数值解');
    xlabel('空间 x');
    ylabel('时间 t');
    zlabel('温度 u');
end

% 定义方程: c*du/dt = x^-m * d/dx(x^m * f) + s
function [c, f, s] = pdefun(x, t, u, dudx)
    c = 1;
    f = dudx; % a^2 设为 1
    s = 0;
end

% 初始条件
function u0 = icfun(x)
    u0 = sin(pi*x); % 假设初始温度分布为正弦
end

% 边界条件
function [pl, ql, pr, qr] = bcfun(xl, ul, xr, ur, t)
    pl = ul; % 左端点温度保持为 0
    ql = 0;
    pr = ur; % 右端点温度保持为 0
    qr = 0;
end