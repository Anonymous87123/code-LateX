% 作业2：设备更新五年计划最优解 (Dijkstra 算法)

clear; clc;

% 1. 输入数据参数
% 各年年初的购买费用 (第1年到第5年)
P = [11, 11, 12, 12, 13]; 
% 设备按使用年龄的每年维修费用 (第1年, 第2年, 第3年, 第4年)
% (基于表格中的数据: 0-1年为5, 1-2年为8, 2-3年为11, 3-4年为18)
M = [5, 8, 11, 18]; 

% 节点 1~6 分别代表第1, 2, 3, 4, 5年年初，以及第6年年初(五年计划结束)
n = 6; 
W = inf(n, n);

% 2. 构建有向无环图的距离矩阵 (权重即为期间的总支出)
for i = 1:n-1
    for j = i+1:n
        years_used = j - i; % 设备使用的年数
        
        % 因为维修费用只给到了第4年，所以设备最多用4年
        if years_used <= length(M)
            % 权重 = 在第 i 年买新设备的费用 + 累计使用年限的维修费
            W(i, j) = P(i) + sum(M(1:years_used));
        end
    end
end

% 3. 使用 Dijkstra 算法求从节点1到节点6的最短路径
[min_cost, path] = dijkstra(W, 1, 6);

% 4. 打印结果
fprintf('=== 设备五年更新计划最优解 ===\n');
fprintf('五年总支出最少为: %d 万元\n', min_cost);

fprintf('\n最优更新策略为: \n');
for k = 1:length(path)-1
    buy_year = path(k);
    replace_year = path(k+1);
    fprintf(' - 在第 %d 年年初购买新设备，使用 %d 年 (用到第 %d 年年初)。\n', ...
            buy_year, replace_year - buy_year, replace_year);
end


% ==========================================================
% 自定义 Dijkstra 算法函数 (同第一题，可复用)
% ==========================================================
function [dist, path] = dijkstra(W, start_node, end_node)
    num_nodes = size(W, 1);
    distances = inf(1, num_nodes);
    visited = false(1, num_nodes);
    prev = zeros(1, num_nodes); 
    
    distances(start_node) = 0;
    
    for i = 1:num_nodes
        min_dist = inf;
        u = -1;
        for j = 1:num_nodes
            if ~visited(j) && distances(j) < min_dist
                min_dist = distances(j);
                u = j;
            end
        end
        
        if u == -1 || u == end_node
            break; 
        end
        visited(u) = true;
        
        for v = 1:num_nodes
            if ~visited(v) && W(u, v) ~= inf
                alt = distances(u) + W(u, v);
                if alt < distances(v)
                    distances(v) = alt;
                    prev(v) = u;
                end
            end
        end
    end
    
    dist = distances(end_node);
    path = [];
    if dist ~= inf
        curr = end_node;
        while curr ~= 0
            path = [curr, path];
            curr = prev(curr);
        end
    end
end