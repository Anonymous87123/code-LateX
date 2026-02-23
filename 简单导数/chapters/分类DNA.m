% ---------------------------------------------------------
% 数学建模：基于 3-mer 频率特征与质心距离的 DNA 序列分类模型
% ---------------------------------------------------------

% 1. 载入题目提供的 40 条序列数据 (简化为数组，请在此处补充完整)
% 1-10 为 A类，11-20 为 B类，21-40 为待分类
dna_sequences = {
    'tgacctcttgtcctgtatagcaacctatttggtaatgattccagcactcacagaaaagct' % 1 (A类)
    'tgcacacatacacacacaccccacccctccccactaacaaatgcaagttggtaaacaaat' % 2 (A类)
    % ... 省略部分输入，实际运行时请将 40 条序列完整粘贴至此
    'ggtccttttctatgctgtggaaggtctgttctttcactcttcacaataaatcttgtgctc' % 39 (待分类)
    'actctttggggccgtgccacctttaagagctataacactcactgcaagggtctgtggctt' % 40 (待分类)
};

% 为了代码可运行性，这里生成一个包含 40 条随机序列的 mock 数组（假设你还没有填入完整数据）
% 实际使用时请直接用上面的 dna_sequences 替换这段 mock 逻辑
if length(dna_sequences) < 40
    warning('未检测到完整的 40 条序列，正在自动补全 mock 数据用于算法逻辑验证...');
    bases = ['a', 'c', 'g', 't'];
    for i = length(dna_sequences)+1 : 40
        dna_sequences{i} = bases(randi([1, 4], 1, 60)); % 题目序列长度均为60
    end
end

N_seq = length(dna_sequences);
k = 3; % 定义 K-mer 窗口大小为 3

% 2. 构建 64 维特征空间 (4^3 = 64 种 3-mer 组合)
alphabet = {'a', 'c', 'g', 't'};
[B1, B2, B3] = ndgrid(1:4, 1:4, 1:4);
kmers = cell(64, 1);
for i = 1:64
    kmers{i} = [alphabet{B1(i)}, alphabet{B2(i)}, alphabet{B3(i)}];
end

% 3. 特征提取 (映射到 R^64 空间)
% 特征矩阵：行代表序列，列代表 64 种 3-mer 的频率
feature_matrix = zeros(N_seq, 64);

for i = 1:N_seq
    seq = lower(dna_sequences{i}); % 统一转换为小写确保严谨
    L = length(seq);
    
    % 滑动窗口统计 3-mer 频数
    for j = 1:(L - k + 1)
        current_kmer = seq(j : j+k-1);
        % 寻找该 kmer 在特征字典中的索引
        idx = find(strcmp(kmers, current_kmer));
        if ~isempty(idx)
            feature_matrix(i, idx) = feature_matrix(i, idx) + 1;
        end
    end
    
    % 频率归一化：除以窗口滑动总次数 (L - k + 1)
    feature_matrix(i, :) = feature_matrix(i, :) / (L - k + 1);
end

% 4. 提取训练集并计算质心 (Centroid)
% 根据题意：1-10 为 A类，11-20 为 B类
train_A = feature_matrix(1:10, :);
train_B = feature_matrix(11:20, :);

centroid_A = mean(train_A, 1);
centroid_B = mean(train_B, 1);

% 5. 距离计算与分类判别 (针对 21-40)
% 提取测试集 (21-40)
test_data = feature_matrix(21:40, :);
num_test = size(test_data, 1);
predictions = cell(num_test, 1);

fprintf('=== DNA 序列分类结果 ===\n');
for i = 1:num_test
    % 计算待分类样本到 A 类和 B 类质心的欧氏距离
    dist_A = norm(test_data(i, :) - centroid_A);
    dist_B = norm(test_data(i, :) - centroid_B);
    
    % 严谨的闭环判别法则
    if dist_A < dist_B
        predictions{i} = 'A';
    elseif dist_B < dist_A
        predictions{i} = 'B';
    else
        predictions{i} = '边界模糊 (等距)'; % 极其罕见，但数学上必须闭环防范
    end
    
    % 输出详细的推导比对过程
    fprintf('序列 %2d (原题编号 %2d): 到 A 距离 = %.4f, 到 B 距离 = %.4f --> 判别为 %s 类\n', ...
            i, i+20, dist_A, dist_B, predictions{i});
end

% 6. K-Means 聚类自验证 (充分性检验)
% 检查前 20 条已知数据在无监督下是否能被天然分开
[idx, ~] = kmeans(feature_matrix(1:20, :), 2, 'Replicates', 5);
fprintf('\n=== 特征有效性检验 (K-Means 聚类前 20 条已知序列) ===\n');
disp('如果聚类结果呈现前 10 个为一类，后 10 个为另一类，则证明 3-mer 特征提取充分且必要：');
disp(idx');