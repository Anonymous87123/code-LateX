% ==========================================
% 作业 2：鸢尾花数据集神经网络分类
% ==========================================

% 1. 加载数据 
% 鸢尾花是 MATLAB 的内置经典数据集，可直接调用
load fisheriris; 

% 2. 数据预处理
% 输入数据: 4个特征，转置为 4 x 150 的矩阵
X = meas';
% 目标数据: 将字符串标签转换为 3 x 150 的独热编码矩阵
Y = dummyvar(grp2idx(species))'; 

% 3. 构建模式识别神经网络 (隐藏层设为 10 个神经元)
net2 = patternnet(10);
net2.trainParam.showWindow = false;

% 4. 解决数据集划分问题 (打乱后划分 100训练 / 30验证 / 20测试)
rng(42); % 设置随机种子，保证每次运行划分结果一致
total_samples = size(X, 2);
rand_idx = randperm(total_samples);

% 提取随机打乱后的索引
train_idx = rand_idx(1:100);       % 100个用于学习
val_idx   = rand_idx(101:130);     % 30个用于验证
test_idx  = rand_idx(131:150);     % 剩余20个用于识别

% 将自定义划分应用到网络配置中
net2.divideFcn = 'divideind';
net2.divideParam.trainInd = train_idx;
net2.divideParam.valInd   = val_idx;
net2.divideParam.testInd  = test_idx;

% 5. 训练网络
[net2, tr] = train(net2, X, Y);

% 6. 测试网络 (仅在未参与训练的测试集上进行评估)
testX = X(:, test_idx);
testY = Y(:, test_idx);
predY = net2(testX);

% 7. 计算准确率与混淆矩阵
true_classes = vec2ind(testY);
pred_classes = vec2ind(predY);

% 计算完全匹配的数量
accuracy = sum(true_classes == pred_classes) / length(true_classes) * 100;

% 输出结果
disp('--- 作业 2: 鸢尾花神经网络分类结果 ---');
fprintf('参与学习(训练)样本数: %d\n', length(tr.trainInd));
fprintf('参与验证样本数: %d\n', length(tr.valInd));
fprintf('参与识别(测试)样本数: %d\n', length(tr.testInd));
fprintf('识别集上的准确率: %.2f%%\n', accuracy);

% 打印详细的测试集对比
disp('测试集详细对比 (预测值 vs 真实值):');
disp([pred_classes', true_classes']);