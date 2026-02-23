% 作业3: 帧差法提取视频前景目标
% 假设视频文件名为 'monitor_video.mp4'

try
    % 1. 读取视频对象
    videoSrc = VideoReader('monitor_video.mp4');
    
    % 创建视频播放器用于对比显示
    videoPlayer = vision.VideoPlayer('Name', '前景提取对比 (左:原图, 右:前景Mask)', ...
        'Position', [100, 100, 1000, 400]);
    
    % 2. 读取第一帧并转换为灰度图作为初始前一帧
    frame_prev = readFrame(videoSrc);
    gray_prev = rgb2gray(frame_prev);
    
    % 设定差分阈值 (根据视频的光照情况调整，一般取 15-30)
    threshold = 25; 
    
    % 定义形态学处理的结构元素 (用于去噪和连通区域)
    se = strel('disk', 3);
    
    % 3. 逐帧处理视频
    while hasFrame(videoSrc)
        % 读取当前帧
        frame_curr = readFrame(videoSrc);
        gray_curr = rgb2gray(frame_curr);
        
        % 核心算法：相邻帧绝对差分
        diff_frame = abs(double(gray_curr) - double(gray_prev));
        
        % 二值化（阈值分割）
        mask = diff_frame > threshold;
        
        % 形态学操作：先开运算(去噪)，后闭运算(填充目标内部空洞)
        mask_clean = imopen(mask, se);
        mask_clean = imclose(mask_clean, se);
        
        % 为了可视化，将逻辑掩膜转换为uint8的黑白图像
        mask_disp = uint8(mask_clean) * 255;
        % 将单通道mask复制为三通道以便与原视频拼接显示
        mask_rgb = cat(3, mask_disp, mask_disp, mask_disp); 
        
        % 拼接原帧和前景掩膜
        combined_frame = [frame_curr, mask_rgb];
        
        % 播放结果
        step(videoPlayer, combined_frame);
        
        % 更新前一帧
        gray_prev = gray_curr;
        
        % 稍微暂停以控制播放速度 (可选)
        pause(0.03); 
    end
    
    release(videoPlayer);
    disp('视频前景提取处理完毕。');
    
catch ME
    disp(['视频处理出错，请确保存在测试视频文件。错误信息: ', ME.message]);
end