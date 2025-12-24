#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import time
from datetime import datetime
import traceback

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=== 完整PPT转视频测试 ===")
print(f"当前时间: {datetime.now()}")
print(f"Python版本: {sys.version}")
print(f"当前目录: {os.getcwd()}")

# 检查测试PPT文件
print("\n=== 测试文件检查 ===")
test_ppt_path = os.path.join(os.path.dirname(__file__), "test_ppt.pptx")

if not os.path.exists(test_ppt_path):
    print(f"错误：测试PPT文件不存在: {test_ppt_path}")
    sys.exit(1)

print(f"测试PPT文件: {test_ppt_path}")
print(f"PPT文件大小: {os.path.getsize(test_ppt_path)} 字节")

# 创建输出视频路径
output_path = "comprehensive_test_output.mp4"

print(f"输出视频路径: {output_path}")

# 导入并调用转换函数
print("\n=== 开始PPT转视频测试 ===")
start_time = time.time()

# 直接导入转换函数
from ppt2video import convert_presentation_to_video

try:
    # 调用转换函数
    success = convert_presentation_to_video(test_ppt_path, output_path, rate=170)
    
    end_time = time.time()
    print(f"\n=== 测试完成 ===")
    print(f"转换耗时: {end_time - start_time:.2f} 秒")
    print(f"转换结果: {'成功' if success else '失败'}")
    
    # 验证输出文件
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"\n=== 视频文件信息 ===")
        print(f"文件路径: {os.path.abspath(output_path)}")
        print(f"文件大小: {file_size} 字节 ({file_size / 1024:.2f} KB)")
        print(f"文件存在: {os.path.exists(output_path)}")
        
        if file_size < 1024:
            print("[警告] 视频文件过小，可能存在问题")
        else:
            print("[成功] 视频文件大小正常")
    else:
        print(f"\n[错误] 输出文件不存在: {output_path}")
        
except Exception as e:
    print(f"\n=== 测试过程中发生错误 ===")
    print(f"错误信息: {e}")
    print("堆栈跟踪:")
    traceback.print_exc()
    sys.exit(1)
