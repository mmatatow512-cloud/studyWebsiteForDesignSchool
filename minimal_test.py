#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简测试脚本：直接执行并将结果写入文件
"""

import os
import sys
import traceback
import tempfile
import shutil

# 配置路径
test_ppt = "test_ppt.pptx"
test_output = "test_output.mp4"
log_file = "minimal_test.log"

# 清空旧日志
if os.path.exists(log_file):
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("")

# 简单的日志函数
def log(message):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{message}\n")

# 开始测试
log("=== 开始极简测试 ===")
log(f"当前目录: {os.getcwd()}")
log(f"Python版本: {sys.version}")

# 检查测试文件
if not os.path.exists(test_ppt):
    log(f"错误: 测试PPT不存在: {test_ppt}")
    sys.exit(1)

log(f"测试PPT: {test_ppt}")
log(f"PPT大小: {os.path.getsize(test_ppt)} 字节")
log(f"输出路径: {test_output}")

# 创建临时目录
temp_img_dir = tempfile.mkdtemp()
temp_aud_dir = tempfile.mkdtemp()

log(f"临时图片目录: {temp_img_dir}")
log(f"临时音频目录: {temp_aud_dir}")

# 导入核心模块
try:
    log("\n导入核心模块...")
    from pptx import Presentation
    import numpy as np
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.video.VideoClip import ImageClip, ColorClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip, concatenate_videoclips
    from moviepy.audio.AudioClip import AudioClip
    log("核心模块导入成功")
except Exception as e:
    log(f"模块导入失败: {e}")
    log(traceback.format_exc())
    sys.exit(1)

# 测试MoviePy是否能生成简单视频
log("\n测试MoviePy生成简单视频...")
try:
    test_clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=2)
    test_output_simple = "simple_test.mp4"
    test_clip.write_videofile(
        test_output_simple,
        fps=10,
        codec="libx264",
        audio_codec=None,
        preset="ultrafast",
        ffmpeg_params=['-pix_fmt', 'yuv420p'],
        logger=None
    )
    test_clip.close()
    
    if os.path.exists(test_output_simple):
        size = os.path.getsize(test_output_simple)
        log(f"简单视频生成成功，大小: {size} 字节")
    else:
        log("简单视频生成失败")
except Exception as e:
    log(f"简单视频生成错误: {e}")
    log(traceback.format_exc())

# 清理临时目录
log("\n清理临时目录...")
shutil.rmtree(temp_img_dir)
shutil.rmtree(temp_aud_dir)

log("=== 测试结束 ===")
