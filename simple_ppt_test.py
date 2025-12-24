#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import time
from datetime import datetime

print("=== 简单PPT转视频测试 ===")
print(f"当前时间: {datetime.now()}")
print(f"Python版本: {sys.version}")

# 检查测试PPT文件
test_ppt_path = "test_ppt.pptx"
if not os.path.exists(test_ppt_path):
    print(f"错误：PPT文件不存在: {test_ppt_path}")
    sys.exit(1)

print(f"测试PPT: {test_ppt_path}")

# 直接导入核心模块
print("\n=== 导入核心模块 ===")
try:
    from pptx import Presentation
    print("✓ python-pptx 导入成功")
    
    import win32com.client
    print("✓ win32com.client 导入成功")
    
    from moviepy.video.VideoClip import ColorClip
    print("✓ moviepy 导入成功")
    
    import imageio_ffmpeg
    print(f"✓ imageio_ffmpeg 导入成功 (版本: {imageio_ffmpeg.__version__})")
    print(f"  FFmpeg路径: {imageio_ffmpeg.get_ffmpeg_exe()}")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    sys.exit(1)

# 测试PPT转图片
print("\n=== 测试PPT转图片 ===")
temp_img_dir = tempfile.mkdtemp()
print(f"临时图片目录: {temp_img_dir}")

# 使用PPTX导出图片
try:
    prs = Presentation(test_ppt_path)
    slide_count = len(prs.slides)
    print(f"PPT包含 {slide_count} 张幻灯片")
except Exception as e:
    print(f"PPT解析失败: {e}")
    sys.exit(1)

# 测试直接视频合成
print("\n=== 测试直接视频合成 ===")
test_output = "simple_test_video.mp4"

try:
    # 创建一个简单的测试视频
    clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=3)
    clip.write_videofile(
        test_output,
        fps=10,
        codec="libx264",
        audio_codec=None,
        preset="ultrafast",
        ffmpeg_params=['-pix_fmt', 'yuv420p', '-y', '-loglevel', 'info'],
        logger=None
    )
    
    if os.path.exists(test_output):
        file_size = os.path.getsize(test_output)
        print(f"✓ 视频合成成功!")
        print(f"  文件: {test_output}")
        print(f"  大小: {file_size} 字节 ({file_size/1024:.2f} KB)")
    else:
        print("✗ 视频合成失败，文件未生成")
except Exception as e:
    print(f"✗ 视频合成失败: {e}")

print("\n=== 测试完成 ===")
