import os
import sys

# 添加project目录到Python路径
sys.path.append("c:/Users/23576/Desktop/demo/project")

import ppt2video
import tempfile
import time

# 检查是否有测试PPT文件
test_ppt_path = "c:/Users/23576/Desktop/demo/project/test_ppt.pptx"
if not os.path.exists(test_ppt_path):
    print("错误：测试PPT文件不存在")
    sys.exit(1)

# 创建临时目录保存输出
with tempfile.TemporaryDirectory() as temp_dir:
    output_video = os.path.join(temp_dir, f"test_output_{int(time.time())}.mp4")
    print(f"开始测试视频转换：{test_ppt_path} -> {output_video}")
    
    try:
        # 调用转换函数
        success = ppt2video.convert_presentation_to_video(test_ppt_path, output_video, rate=170)
        print(f"转换结果：{success}")
        
        # 检查输出文件
        if os.path.exists(output_video):
            file_size = os.path.getsize(output_video)
            print(f"视频文件大小：{file_size} 字节")
            if file_size < 10240:
                print("[错误] 视频文件过小，可能无效")
            else:
                print("[成功] 视频文件生成正常")
        else:
            print("[错误] 视频文件未生成")
            
    except Exception as e:
        print(f"[错误] 转换过程中出现异常：{e}")
        import traceback
        traceback.print_exc()
    