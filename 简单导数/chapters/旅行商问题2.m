% 作业2：AR9152 (阿根廷9152城市) TSP求解 (贪心/最近邻算法)

clear; clc;

% 1. 读取 TSPLIB 数据 (假设数据文件名为 ar9152.tsp)
% 【注意】：由于不能直接提供文件，这里用生成9152个点的代码模拟读取过程
% 实际应用中你应该写文件读取代码，例如 textscan 或 fscanf
N = 9152;
disp(['正在加载 ', num2str(N), ' 个城市的数据...']);
% 模拟坐标数据 (实际应从 ar9152.tsp 中读取 NODE_COORD_SECTION 的X,Y)
rng(42); 
coords = rand(N, 2) * 1000; 

% 为了避免 9152x9152 (约 630MB) 的距离矩阵占用过大内存，
% 我们将在贪心算法中动态计算距离

% 2. 最近邻算法 (Nearest Neighbor) 初始化路线
disp('正在使用最近邻算法计算初始路线...');
visited = false(1, N);
tour = zeros(1, N);

current_city = 1; % 从城市1开始
tour(1) = current_city;
visited(current_city) = true;
total_dist = 0;

for step = 2:N
    if mod(step, 1000) == 0
        disp(['已规划 ', num2str(step), ' 个城市...']);
    end
    
    % 计算当前城市到所有未访问城市的距离
    unvisited_idx = find(~visited);
    
    % 矢量化计算距离 (欧氏距离)
    % 如果是地理坐标(LAT/LONG)，需要换成 Haversine 公式
    diffs = coords(unvisited_idx, :) - coords(current_city, :);
    dists = sum(diffs.^2, 2); % 使用距离平方比较，提高计算速度
    
    % 找到最近的未访问城市
    [~, min_idx] = min(dists);
    next_city = unvisited_idx(min_idx);
    
    % 更新路线和状态
    tour(step) = next_city;
    visited(next_city) = true;
    total_dist = total_dist + sqrt(dists(min_idx));
    current_city = next_city;
end
% 加上回到起点的距离
total_dist = total_dist + norm(coords(tour(end), :) - coords(tour(1), :));

disp(['最近邻算法完成！初步路线总距离: ', num2str(total_dist)]);

% 3. 可视化阿根廷TSP路线
figure;
% 为了画图不卡顿，可以直接绘制线段
plot(coords(tour, 1), coords(tour, 2), 'k-', 'LineWidth', 0.5);
hold on;
plot([coords(tour(end), 1), coords(tour(1), 1)], ...
     [coords(tour(end), 2), coords(tour(1), 2)], 'r-', 'LineWidth', 0.5); % 回起点的红线
title(sprintf('AR9152 启发式路径规划 (总距离: %.2f)', total_dist));
xlabel('X Coordinate'); ylabel('Y Coordinate');
axis equal;
