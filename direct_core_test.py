#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试视频生成核心功能
"""

import os
import sys
import tempfile
import shutil

# 确保在正确的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 配置路径
test_ppt = "test_ppt.pptx"
test_output = "direct_core_test_output.mp4"
log_file = "direct_core_test.log"

# 清空旧日志
with open(log_file, 'w', encoding='utf-8') as f:
    f.write("")

# 简单的日志函数
def log(message):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{message}\n")
    print(message, flush=True)

log("=== 开始直接核心测试 ===")
log(f"Python版本: {sys.version}")
log(f"当前目录: {os.getcwd()}")

# 检查测试PPT
if not os.path.exists(test_ppt):
    log(f"错误: 测试PPT不存在: {test_ppt}")
    sys.exit(1)

log(f"测试PPT: {test_ppt}")
log(f"PPT大小: {os.path.getsize(test_ppt)} 字节")
log(f"输出路径: {test_output}")

# 直接测试MoviePy是否能生成简单视频
log("\n=== 测试MoviePy核心功能 ===")
try:
    from moviepy.video.VideoClip import ColorClip
    
    # 创建一个简单的红色视频
    log("创建简单红色测试视频...")
    test_clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=2)
    
    # 直接使用write_videofile
    test_clip.write_videofile(
        test_output,
        fps=10,
        codec="libx264",
        audio_codec=None,
        preset="ultrafast",
        threads=1,
        ffmpeg_params=[
            '-pix_fmt', 'yuv420p',
            '-y',
            '-loglevel', 'info'
        ],
        logger='bar'
    )
    
    test_clip.close()
    
    # 检查结果
    if os.path.exists(test_output):
        size = os.path.getsize(test_output)
        log(f"测试视频生成成功！")
        log(f"文件路径: {test_output}")
        log(f"文件大小: {size} 字节 ({size / 1024:.2f} KB)")
        
        if size > 1024:
            log("✅ 视频文件大小正常")
        else:
            log("❌ 视频文件太小")
    else:
        log("❌ 测试视频生成失败")
        
except Exception as e:
    log(f"❌ MoviePy测试失败: {e}")
    import traceback
    traceback.print_exc()

log("\n=== 测试结束 ===")
