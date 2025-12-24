#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试视频生成功能
"""

import os
import sys
import tempfile

# 直接导入需要的模块
from moviepy.video.VideoClip import ColorClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from moviepy.audio.AudioClip import AudioClip
import numpy as np

def main():
    """主测试函数"""
    print("=== 简单视频生成测试 ===")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp(prefix="simple_video_test_")
    print(f"临时目录: {temp_dir}")
    
    try:
        # 测试1: 生成简单的彩色视频
        print("\n1. 测试生成简单彩色视频...")
        test_clip = ColorClip(size=(320, 240), color=(0, 255, 0), duration=3)
        test_output = os.path.join(temp_dir, "test_color.mp4")
        
        print(f"  输出路径: {test_output}")
        print(f"  开始编码...")
        
        # 使用最基本的参数
        test_clip.write_videofile(
            test_output,
            fps=10,
            codec="libx264",
            audio_codec=None,
            preset="ultrafast",
            ffmpeg_params=['-pix_fmt', 'yuv420p', '-y'],
            logger='bar'
        )
        
        # 验证结果
        if os.path.exists(test_output):
            size = os.path.getsize(test_output)
            print(f"  ✅ 成功！文件大小: {size} 字节 ({size/1024:.2f} KB)")
        else:
            print(f"  ❌ 失败！文件未生成")
        
        # 测试2: 生成带有音频的视频
        print("\n2. 测试生成带音频的视频...")
        
        # 创建音频
        def make_sound(t):
            return 0.1 * np.sin(440 * 2 * np.pi * t)  # 440Hz正弦波
        
        audio_clip = AudioClip(make_sound, duration=3)
        video_with_audio = ColorClip(size=(320, 240), color=(255, 0, 0), duration=3)
        video_with_audio = video_with_audio.with_audio(audio_clip)
        
        audio_output = os.path.join(temp_dir, "test_with_audio.mp4")
        print(f"  输出路径: {audio_output}")
        print(f"  开始编码...")
        
        video_with_audio.write_videofile(
            audio_output,
            fps=10,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            ffmpeg_params=['-pix_fmt', 'yuv420p', '-y'],
            logger='bar'
        )
        
        # 验证结果
        if os.path.exists(audio_output):
            size = os.path.getsize(audio_output)
            print(f"  ✅ 成功！文件大小: {size} 字节 ({size/1024:.2f} KB)")
        else:
            print(f"  ❌ 失败！文件未生成")
        
        print("\n=== 测试完成 ===")
        print(f"测试文件保存在: {temp_dir}")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 不清理临时文件，方便用户查看
        print(f"\n临时文件未清理，可手动删除: {temp_dir}")

if __name__ == "__main__":
    main()