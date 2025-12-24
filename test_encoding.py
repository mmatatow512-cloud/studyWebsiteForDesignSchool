#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试视频编码功能的简单脚本
用于验证FFmpeg和MoviePy是否能正常生成视频文件
"""

import os
import sys
import tempfile
import datetime

# 添加直接导入MoviePy组件
from moviepy.video.VideoClip import ColorClip

print("=== 视频编码测试脚本 ===")
print(f"当前时间: {datetime.datetime.now()}")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")

# 测试1: 简单颜色视频
print("\n1. 测试简单颜色视频生成...")
try:
    # 创建2秒的红色视频
    clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=2)
    output_path = "test_red.mp4"
    
    # 使用最简参数
    clip.write_videofile(
        output_path,
        fps=10,
        codec="libx264",
        audio_codec=None,
        preset="ultrafast",
        threads=1,
        ffmpeg_params=[
            '-pix_fmt', 'yuv420p',
            '-y',  # 覆盖现有文件
            '-loglevel', 'info'  # 显示详细日志
        ],
        logger='bar'  # 显示进度条
    )
    
    # 释放资源
    clip.close()
    
    # 验证结果
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"✓ 测试成功!")
        print(f"  输出文件: {output_path}")
        print(f"  文件大小: {file_size} 字节 ({file_size / 1024:.2f} KB)")
    else:
        print(f"✗ 测试失败: 文件未生成")
        
except Exception as e:
    print(f"✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试2: 绿色视频
print("\n2. 测试绿色视频生成...")
try:
    # 创建3秒的绿色视频
    clip = ColorClip(size=(320, 240), color=(0, 255, 0), duration=3)
    output_path = "test_green.mp4"
    
    # 使用更多参数
    clip.write_videofile(
        output_path,
        fps=15,
        codec="libx264",
        audio_codec=None,
        preset="fast",
        threads=2,
        ffmpeg_params=[
            '-pix_fmt', 'yuv420p',
            '-b:v', '500k',  # 视频比特率
            '-y',
            '-loglevel', 'info'
        ],
        logger='bar'
    )
    
    # 释放资源
    clip.close()
    
    # 验证结果
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"✓ 测试成功!")
        print(f"  输出文件: {output_path}")
        print(f"  文件大小: {file_size} 字节 ({file_size / 1024:.2f} KB)")
    else:
        print(f"✗ 测试失败: 文件未生成")
        
except Exception as e:
    print(f"✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试完成 ===")
