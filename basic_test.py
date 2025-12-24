#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

print("=== 基础环境测试 ===")
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")
print(f"当前工作目录: {os.getcwd()}")
print(f"当前目录文件: {os.listdir('.')}")

# 检查测试PPT文件
test_ppt = "test_ppt.pptx"
if os.path.exists(test_ppt):
    print(f"\n✓ 测试PPT文件存在")
    print(f"  文件名: {test_ppt}")
    print(f"  文件大小: {os.path.getsize(test_ppt)} 字节")
else:
    print(f"\n✗ 测试PPT文件不存在: {test_ppt}")

# 检查关键模块
try:
    import pythoncom
    print("\n✓ pythoncom 导入成功")
except Exception as e:
    print(f"\n✗ pythoncom 导入失败: {e}")

try:
    import win32com.client
    print("✓ win32com.client 导入成功")
except Exception as e:
    print(f"✗ win32com.client 导入失败: {e}")

try:
    import pptx
    print("✓ python-pptx 导入成功")
except Exception as e:
    print(f"✗ python-pptx 导入失败: {e}")

try:
    import moviepy
    print("✓ moviepy 导入成功")
except Exception as e:
    print(f"✗ moviepy 导入失败: {e}")

try:
    from moviepy.video.VideoClip import ImageClip
    print("✓ ImageClip 导入成功")
except Exception as e:
    print(f"✗ ImageClip 导入失败: {e}")

try:
    from moviepy.audio.AudioClip import AudioClip
    print("✓ AudioClip 导入成功")
except Exception as e:
    print(f"✗ AudioClip 导入失败: {e}")

print("\n=== 测试完成 ===")
