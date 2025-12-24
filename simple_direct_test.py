#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单直接测试脚本：直接执行PPT转视频功能
"""

import os
import sys
import traceback
import time

# 确保我们在正确的目录下
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=== 开始简单直接测试 ===")
print(f"当前目录: {os.getcwd()}")

# 测试文件路径
test_ppt_path = "test_ppt.pptx"
test_output_path = "test_output.mp4"

# 检查测试PPT是否存在
if not os.path.exists(test_ppt_path):
    print(f"错误: 测试PPT文件不存在: {test_ppt_path}")
    sys.exit(1)

print(f"测试PPT路径: {test_ppt_path}")
print(f"PPT大小: {os.path.getsize(test_ppt_path)} 字节")
print(f"输出视频路径: {test_output_path}")

# 直接导入并执行转换
print("\n开始导入转换函数...")
try:
    from ppt2video import convert_presentation_to_video
    print("导入成功")
except Exception as e:
    print(f"导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 执行转换
print("\n开始执行转换...")
try:
    result = convert_presentation_to_video(test_ppt_path, test_output_path)
    print(f"转换结果: {'成功' if result else '失败'}")
    
    # 检查输出文件
    if os.path.exists(test_output_path):
        size = os.path.getsize(test_output_path)
        print(f"输出文件大小: {size} 字节")
        if size > 1024:
            print("文件大小正常！")
        else:
            print("警告: 文件大小异常！")
    else:
        print("错误: 输出文件不存在！")
        
except Exception as e:
    print(f"转换过程出错: {e}")
    traceback.print_exc()

print("\n=== 测试结束 ===")
