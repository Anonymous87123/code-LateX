% 作业1: 用MATLAB软件保存名画五牛图
% 假设当前目录下已有名画图像文件 'FiveOxen.jpg'

try
    % 1. 读取图像到矩阵
    img_oxen = imread('FiveOxen.jpg'); 
    
    % 显示原图以确认读取成功
    figure('Name', '世界著名油画 - 五牛图');
    imshow(img_oxen);
    title('原图：五牛图');
    
    % 2. 保存图像
    % 方法A：无损保存为PNG格式，防止多次编辑带来的失真
    imwrite(img_oxen, 'FiveOxen_Lossless.png');
    
    % 方法B：保存为JPG并设置压缩质量为95（范围0-100）
    imwrite(img_oxen, 'FiveOxen_Compressed.jpg', 'Quality', 95);
    
    % 方法C：将图像数据矩阵直接保存为MAT文件，方便后续科学计算
    save('FiveOxen_Data.mat', 'img_oxen');
    
    disp('五牛图保存成功！已生成PNG, JPG及MAT文件。');
catch ME
    disp(['读取或保存出错，请检查文件名与路径。错误信息: ', ME.message]);
end