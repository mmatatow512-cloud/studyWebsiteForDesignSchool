#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超级简单的视频生成测试脚本
"""

import os
import sys
import datetime

# 直接写入日志文件
log_file = "super_simple_test.log"

def write_log(message):
    """直接写入日志文件"""
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.datetime.now()}] {message}\n")

# 清空日志文件
with open(log_file, 'w', encoding='utf-8') as f:
    f.write("=== 超级简单测试开始 ===\n")
    f.write(f"Python版本: {sys.version}\n")
    f.write(f"当前工作目录: {os.getcwd()}\n\n")

# 测试1: 基本的文件写入
write_log("1. 测试基本文件写入...")
test_file = "test_write.txt"
try:
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("测试文件写入成功\n")
    if os.path.exists(test_file):
        write_log("✓ 文件写入成功")
        write_log(f"   文件大小: {os.path.getsize(test_file)} 字节")
        os.remove(test_file)
        write_log("   文件已删除")
    else:
        write_log("✗ 文件写入失败")
except Exception as e:
    write_log(f"✗ 文件写入失败: {e}")

# 测试2: 尝试导入MoviePy组件
write_log("\n2. 测试MoviePy导入...")
try:
    from moviepy.video.VideoClip import ColorClip
    write_log("✓ ColorClip导入成功")
except Exception as e:
    write_log(f"✗ ColorClip导入失败: {e}")
    import traceback
    write_log(f"   详细错误: {traceback.format_exc()}")

# 测试3: 尝试生成简单视频
write_log("\n3. 测试视频生成...")
try:
    from moviepy.video.VideoClip import ColorClip
    
    # 创建简单的视频
    clip = ColorClip(size=(320, 240), color=(0, 255, 0), duration=2)
    output_path = "super_simple_test.mp4"
    
    write_log(f"   开始生成视频: {output_path}")
    clip.write_videofile(
        output_path,
        fps=10,
        codec="libx264",
        audio_codec=None,
        preset="ultrafast",
        threads=1,
        ffmpeg_params=[
            '-pix_fmt', 'yuv420p',
            '-y',
            '-loglevel', 'error'
        ],
        logger=None
    )
    
    clip.close()
    
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        write_log("✓ 视频生成成功")
        write_log(f"   文件路径: {output_path}")
        write_log(f"   文件大小: {file_size} 字节")
    else:
        write_log("✗ 视频生成失败: 文件不存在")
        
except Exception as e:
    write_log(f"✗ 视频生成失败: {e}")
    import traceback
    write_log(f"   详细错误: {traceback.format_exc()}")

write_log("\n=== 超级简单测试完成 ===")
