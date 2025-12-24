#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback

# 简单的测试脚本，只测试最基本的功能
print("=== Ultra Simple Test ===")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")

# 检查测试PPT文件
print("\n检查测试PPT文件...")
test_ppt = "test_ppt.pptx"
if os.path.exists(test_ppt):
    print(f"✓ 测试PPT文件存在: {test_ppt}")
    print(f"  文件大小: {os.path.getsize(test_ppt)} 字节")
else:
    print(f"✗ 测试PPT文件不存在: {test_ppt}")
    print(f"  当前目录文件: {os.listdir('.')}")
    sys.exit(1)

# 尝试导入模块
print("\n尝试导入基本模块...")
try:
    import moviepy
    print(f"✓ 成功导入 moviepy: {moviepy.__version__}")
except Exception as e:
    print(f"✗ 导入 moviepy 失败: {e}")
    print(traceback.format_exc())
    sys.exit(1)

try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.video.VideoClip import ImageClip
    from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
    print("✓ 成功导入所有MoviePy组件")
except Exception as e:
    print(f"✗ 导入MoviePy组件失败: {e}")
    print(traceback.format_exc())
    sys.exit(1)

try:
    import win32com.client
    print("✓ 成功导入 win32com.client")
except Exception as e:
    print(f"✗ 导入 win32com.client 失败: {e}")
    print(traceback.format_exc())
    sys.exit(1)

try:
    from pptx import Presentation
    print("✓ 成功导入 python-pptx")
except Exception as e:
    print(f"✗ 导入 python-pptx 失败: {e}")
    print(traceback.format_exc())
    sys.exit(1)

print("\n=== 所有基本测试通过 ===")
print("环境配置基本正确，可以尝试运行实际转换")