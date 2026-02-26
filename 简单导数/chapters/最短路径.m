% 作业1：求节点 A 到 G 的最短路径 (Dijkstra 算法)

clear; clc;

% 1. 定义节点数量 (A=1, B=2, C=3, D=4, E=5, F=6, G=7)
n = 7; 

% 2. 初始化邻接矩阵 W 为无穷大
W = inf(n, n);

% 对角线元素设为 0 (自己到自己的距离)
for i = 1:n
    W(i, i) = 0;
end

% -------------------------------------------------------------
% 请根据作业中的网络图(image1.jpeg)填入实际的边长(权重)。
% 下面是一个示例数据，你需要替换成图中的真实数字！
% 例如，如果 A(1) 到 B(2) 的距离是 4，则 W(1,2) = 4; W(2,1) = 4;
% -------------------------------------------------------------
% 【需要你在此处补充真实权重】
W(1, 2) = 4;  W(2, 1) = 4;  % A-B
W(1, 3) = 2;  W(3, 1) = 2;  % A-C
% ... 补充剩下的边 ...

% 3. 调用自定义的 Dijkstra 函数计算 A(1) 到 G(7) 的最短路径
start_node = 1; % A点
end_node = 7;   % G点
[min_cost, path] = dijkstra(W, start_node, end_node);

% 4. 打印结果
nodes_name = {'A', 'B', 'C', 'D', 'E', 'F', 'G'};
if min_cost == inf
    fprintf('无法从起点走到终点。\n');
else
    fprintf('最短距离（最省费用）为: %d\n', min_cost);
    path_str = strjoin(nodes_name(path), ' -> ');
    fprintf('最短路线为: %s\n', path_str);
end


% ==========================================================
% 自定义 Dijkstra 算法函数
% ==========================================================
function [dist, path] = dijkstra(W, start_node, end_node)
    num_nodes = size(W, 1);
    distances = inf(1, num_nodes);
    visited = false(1, num_nodes);
    prev = zeros(1, num_nodes); % 记录前驱节点以回溯路径
    
    distances(start_node) = 0;
    
    for i = 1:num_nodes
        % 寻找未访问节点中距离最小的节点
        min_dist = inf;
        u = -1;
        for j = 1:num_nodes
            if ~visited(j) && distances(j) < min_dist
                min_dist = distances(j);
                u = j;
            end
        end
        
        % 如果找不到连通节点或者已经到达终点，则停止
        if u == -1 || u == end_node
            break; 
        end
        
        visited(u) = true;
        
        % 更新相邻节点的距离
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
    
    % 回溯构建最短路径
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