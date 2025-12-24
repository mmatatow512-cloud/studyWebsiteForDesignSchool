#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import time
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 直接导入moviepy组件
from moviepy.video.VideoClip import ColorClip

print("=== MoviePy直接视频测试 ===")
print(f"当前时间: {datetime.now()}")
print(f"Python版本: {sys.version}")
print(f"当前目录: {os.getcwd()}")

# 检查FFmpeg配置
print("\n=== FFmpeg配置检查 ===")
try:
    import imageio_ffmpeg
    print(f"imageio_ffmpeg版本: {imageio_ffmpeg.__version__}")
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"FFmpeg路径: {ffmpeg_path}")
    print(f"FFmpeg存在: {os.path.exists(ffmpeg_path)}")
    if os.path.exists(ffmpeg_path):
        print(f"FFmpeg文件大小: {os.path.getsize(ffmpeg_path)} 字节")
except Exception as e:
    print(f"FFmpeg检查失败: {e}")

# 创建测试视频
print("\n=== 创建测试视频 ===")
test_output = "direct_test_video.mp4"

print(f"输出路径: {test_output}")
print(f"开始编码时间: {datetime.now()}")

# 使用ColorClip创建一个简单的测试视频
try:
    # 创建一个3秒的绿色视频，尺寸640x480
    test_clip = ColorClip(size=(640, 480), color=(0, 255, 0), duration=3)
    
    # 配置FFmpeg参数
    ffmpeg_params = [
        '-pix_fmt', 'yuv420p',  # 兼容所有播放器
        '-b:v', '500k',         # 视频比特率
        '-y',                   # 覆盖现有文件
        '-loglevel', 'info'     # 详细日志
    ]
    
    print(f"FFmpeg参数: {ffmpeg_params}")
    
    # 写入视频文件
    test_clip.write_videofile(
        test_output,
        fps=20,                  # 降低帧率
        codec="libx264",          # 视频编码
        audio_codec=None,        # 无音频
        preset="ultrafast",      # 最快的编码速度
        threads=1,               # 单线程
        ffmpeg_params=ffmpeg_params,
        logger='bar'             # 显示进度条
    )
    
    test_clip.close()
    
    print(f"结束编码时间: {datetime.now()}")
    
    # 验证输出文件
    if os.path.exists(test_output):
        file_size = os.path.getsize(test_output)
        print(f"\n=== 测试成功！ ===")
        print(f"视频文件大小: {file_size} 字节 ({file_size / 1024:.2f} KB)")
        print(f"视频文件路径: {os.path.abspath(test_output)}")
    else:
        print("\n=== 测试失败！ ===")
        print("视频文件未生成")
        
except Exception as e:
    print(f"\n=== 测试失败！ ===")
    print(f"错误信息: {e}")
    import traceback
    traceback.print_exc()
