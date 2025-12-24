#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=== 简单调试PPT转视频 ===")
print(f"Python版本: {sys.version}")

# 定义测试文件路径
test_ppt = "test_ppt.pptx"
output_video = "simple_debug_output.mp4"

# 验证测试文件是否存在
if not os.path.exists(test_ppt):
    print(f"错误：测试PPT文件不存在: {test_ppt}")
    sys.exit(1)

print(f"测试PPT文件: {test_ppt}")
print(f"输出视频路径: {output_video}")

# 导入convert_presentation_to_video函数
try:
    from ppt2video import convert_presentation_to_video
    print("导入函数成功")
    
    # 调用函数
    print("\n开始转换PPT到视频...")
    success = convert_presentation_to_video(test_ppt, output_video, rate=170)
    print(f"转换结果: {'成功' if success else '失败'}")
    
    # 检查输出文件
    if os.path.exists(output_video):
        file_size = os.path.getsize(output_video)
        print(f"视频文件大小: {file_size} 字节")
    else:
        print("视频文件未生成")
        
except Exception as e:
    print(f"\n转换过程中发生异常: {e}")
    print("堆栈跟踪:")
    traceback.print_exc()
