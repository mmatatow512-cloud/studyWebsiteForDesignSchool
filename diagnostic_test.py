#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频生成诊断测试脚本
用于详细诊断PPT转视频过程中的问题，特别是视频编码和文件大小问题
"""

import os
import sys
import time
import tempfile
import subprocess
import traceback
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入需要的模块
import pythoncom
from moviepy.video.VideoClip import ColorClip, ImageClip
from moviepy.audio.AudioClip import AudioClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
import numpy as np

# 日志函数
def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open("diagnostic_test.log", "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

def check_ffmpeg():
    """检查FFmpeg配置"""
    log("=== 检查FFmpeg配置 ===")
    
    try:
        # 检查moviepy的FFmpeg配置
        from moviepy.config import FFMPEG_BINARY
        log(f"MoviePy FFMPEG_BINARY: {FFMPEG_BINARY}")
        log(f"FFmpeg存在: {os.path.exists(FFMPEG_BINARY)}")
        
        # 检查imageio_ffmpeg
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        log(f"imageio_ffmpeg路径: {ffmpeg_path}")
        log(f"imageio_ffmpeg存在: {os.path.exists(ffmpeg_path)}")
        
        # 测试FFmpeg版本
        result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            log(f"FFmpeg版本信息:")
            for line in result.stdout.splitlines()[:3]:  # 只显示前3行
                log(f"  {line}")
        else:
            log(f"FFmpeg版本检查失败: {result.stderr}")
            
        return True
        
    except Exception as e:
        log(f"FFmpeg检查失败: {e}")
        traceback.print_exc()
        return False

def test_simple_video():
    """测试简单视频生成"""
    log("=== 测试简单视频生成 ===")
    
    test_videos = [
        (320, 240, "test_320x240.mp4"),
        (640, 480, "test_640x480.mp4"),
        (1280, 720, "test_1280x720.mp4")
    ]
    
    for width, height, filename in test_videos:
        log(f"\n测试 {width}x{height} 视频...")
        try:
            # 创建纯色视频
            clip = ColorClip(size=(width, height), color=(0, 255, 0), duration=2)
            
            # 编码参数
            start_time = time.time()
            clip.write_videofile(
                filename,
                fps=10,
                codec="libx264",
                audio_codec=None,
                preset="ultrafast",
                threads=1,
                ffmpeg_params=['-pix_fmt', 'yuv420p', '-y', '-loglevel', 'info'],
                logger=None
            )
            end_time = time.time()
            
            clip.close()
            
            # 验证文件
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                log(f"✓ 视频生成成功: {filename}")
                log(f"  文件大小: {size} 字节 ({size/1024:.2f} KB)")
                log(f"  生成耗时: {end_time - start_time:.2f} 秒")
                
                # 如果文件太小，标记警告
                if size < 1024:
                    log(f"⚠️  文件过小，可能存在问题")
            else:
                log(f"✗ 视频文件未生成: {filename}")
                
        except Exception as e:
            log(f"✗ 视频生成失败: {e}")
            traceback.print_exc()

def test_with_audio():
    """测试带音频的视频生成"""
    log("\n=== 测试带音频的视频生成 ===")
    
    try:
        # 创建视频
        clip = ColorClip(size=(640, 480), color=(0, 0, 255), duration=2)
        
        # 创建测试音频
        def make_sound(t):
            return 0.1 * np.sin(440 * 2 * np.pi * t)
        
        audio_clip = AudioClip(make_sound, duration=2)
        
        # 添加音频到视频
        final_clip = clip.with_audio(audio_clip)
        
        # 编码
        filename = "test_with_audio.mp4"
        final_clip.write_videofile(
            filename,
            fps=10,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=1,
            ffmpeg_params=['-pix_fmt', 'yuv420p', '-y', '-loglevel', 'info'],
            logger=None
        )
        
        final_clip.close()
        audio_clip.close()
        
        # 验证
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            log(f"✓ 带音频视频生成成功: {filename}")
            log(f"  文件大小: {size} 字节 ({size/1024:.2f} KB)")
        else:
            log(f"✗ 带音频视频文件未生成")
            
    except Exception as e:
        log(f"✗ 带音频视频生成失败: {e}")
        traceback.print_exc()

def test_concatenation():
    """测试视频片段合并"""
    log("\n=== 测试视频片段合并 ===")
    
    try:
        # 创建两个视频片段
        clip1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=1)
        clip2 = ColorClip(size=(640, 480), color=(0, 255, 0), duration=1)
        
        # 合并片段
        final_clip = concatenate_videoclips([clip1, clip2], method="compose")
        
        # 编码
        filename = "test_concat.mp4"
        final_clip.write_videofile(
            filename,
            fps=10,
            codec="libx264",
            audio_codec=None,
            preset="ultrafast",
            threads=1,
            ffmpeg_params=['-pix_fmt', 'yuv420p', '-y', '-loglevel', 'info'],
            logger=None
        )
        
        final_clip.close()
        clip1.close()
        clip2.close()
        
        # 验证
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            log(f"✓ 视频合并成功: {filename}")
            log(f"  文件大小: {size} 字节 ({size/1024:.2f} KB)")
        else:
            log(f"✗ 合并视频文件未生成")
            
    except Exception as e:
        log(f"✗ 视频合并失败: {e}")
        traceback.print_exc()

def test_with_image():
    """测试使用图片生成视频"""
    log("\n=== 测试使用图片生成视频 ===")
    
    try:
        # 创建测试图片
        from PIL import Image, ImageDraw
        
        # 创建一个简单的测试图片
        img = Image.new('RGB', (640, 480), color=(255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), "Test Image", fill=(0, 0, 0))
        img_path = "test_image.jpg"
        img.save(img_path)
        log(f"创建测试图片: {img_path}")
        
        # 使用图片创建视频
        clip = ImageClip(img_path).with_duration(2)
        
        # 编码
        filename = "test_with_image.mp4"
        clip.write_videofile(
            filename,
            fps=10,
            codec="libx264",
            audio_codec=None,
            preset="ultrafast",
            threads=1,
            ffmpeg_params=['-pix_fmt', 'yuv420p', '-y', '-loglevel', 'info'],
            logger=None
        )
        
        clip.close()
        
        # 验证
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            log(f"✓ 图片视频生成成功: {filename}")
            log(f"  文件大小: {size} 字节 ({size/1024:.2f} KB)")
            
            # 清理测试图片
            os.remove(img_path)
        else:
            log(f"✗ 图片视频文件未生成")
            
    except Exception as e:
        log(f"✗ 图片视频生成失败: {e}")
        traceback.print_exc()

def test_ppt2video_integration():
    """测试与ppt2video模块的集成"""
    log("\n=== 测试与ppt2video模块的集成 ===")
    
    try:
        # 导入模块
        from ppt2video import convert_presentation_to_video
        
        # 检查测试PPT是否存在
        test_ppt = "test_ppt.pptx"
        if not os.path.exists(test_ppt):
            log(f"✗ 测试PPT不存在: {test_ppt}")
            log("  请先创建测试PPT文件")
            return
        
        log(f"使用测试PPT: {test_ppt}")
        log(f"PPT文件大小: {os.path.getsize(test_ppt)} 字节")
        
        # 测试转换
        output_video = "integration_test.mp4"
        result = convert_presentation_to_video(test_ppt, output_video)
        
        if result:
            log(f"✓ PPT转视频集成测试成功")
            if os.path.exists(output_video):
                size = os.path.getsize(output_video)
                log(f"  生成的视频文件: {output_video}")
                log(f"  文件大小: {size} 字节 ({size/1024:.2f} KB)")
        else:
            log(f"✗ PPT转视频集成测试失败")
            
    except Exception as e:
        log(f"✗ 集成测试失败: {e}")
        traceback.print_exc()

def analyze_1kb_problem():
    """分析1KB视频问题"""
    log("\n=== 分析1KB视频问题 ===")
    
    # 检查是否存在1KB的视频文件
    one_kb_videos = []
    for file in os.listdir("."):
        if file.endswith(".mp4"):
            size = os.path.getsize(file)
            if size <= 1024:
                one_kb_videos.append((file, size))
    
    if one_kb_videos:
        log(f"发现 {len(one_kb_videos)} 个1KB以下的视频文件:")
        for file, size in one_kb_videos:
            log(f"  {file}: {size} 字节")
            
        # 尝试读取文件内容
        log("\n查看1KB视频文件内容:")
        for file, size in one_kb_videos:
            if size > 0:
                try:
                    with open(file, "rb") as f:
                        content = f.read()
                    log(f"  {file} 内容:")
                    log(f"    十六进制: {content.hex()[:32]}...")  # 只显示前32个字符
                    log(f"    字符形式: {repr(content[:32])}...")
                except Exception as e:
                    log(f"    读取失败: {e}")
    else:
        log("没有发现1KB以下的视频文件")

def main():
    """主函数"""
    log("=== 视频生成诊断测试开始 ===")
    
    # 初始化COM组件
    pythoncom.CoInitialize()
    
    # 运行所有测试
    check_ffmpeg()
    test_simple_video()
    test_with_audio()
    test_concatenation()
    test_with_image()
    analyze_1kb_problem()
    # test_ppt2video_integration()  # 这个测试需要测试PPT文件
    
    log("\n=== 视频生成诊断测试完成 ===")
    log("详细日志请查看: diagnostic_test.log")

if __name__ == "__main__":
    main()
