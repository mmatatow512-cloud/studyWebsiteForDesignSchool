#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试PPT转视频功能，将结果写入文件
"""

import os
import sys
import traceback

# 确保可以导入当前目录的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 记录日志到文件
def log(message):
    with open('direct_test.log', 'a', encoding='utf-8') as f:
        f.write(f"[DIRECT TEST] {message}\n")

log("=== 开始直接测试 PPT 转视频功能 ===")
log(f"Python 版本: {sys.version}")
log(f"当前工作目录: {os.getcwd()}")

# 检查依赖
try:
    import numpy
    log(f"[成功] numpy 版本: {numpy.__version__}")
except Exception as e:
    log(f"[失败] numpy 导入失败: {e}")
    log(traceback.format_exc())

try:
    import moviepy
    log(f"[成功] moviepy 版本: {moviepy.__version__}")
except Exception as e:
    log(f"[失败] moviepy 导入失败: {e}")
    log(traceback.format_exc())

try:
    from pptx import Presentation
    log("[成功] python-pptx 导入成功")
except Exception as e:
    log(f"[失败] python-pptx 导入失败: {e}")
    log(traceback.format_exc())

# 检查测试PPT文件
test_ppt_path = "test_ppt.pptx"
if os.path.exists(test_ppt_path):
    log(f"[成功] 测试PPT文件存在: {test_ppt_path}")
    log(f"  文件大小: {os.path.getsize(test_ppt_path)} 字节")
else:
    log(f"[失败] 测试PPT文件不存在: {test_ppt_path}")
    log(f"  当前目录文件: {os.listdir('.')}")

# 尝试导入并使用我们的模块
try:
    log("尝试导入ppt2video模块...")
    from ppt2video import convert_presentation_to_video
    log("[成功] ppt2video模块导入成功")
    
    # 检查测试PPT是否存在
    if os.path.exists(test_ppt_path):
        log("开始转换测试PPT...")
        output_path = "test_output.mp4"
        
        # 尝试转换
        result = convert_presentation_to_video(
            ppt_path=test_ppt_path,
            output_path=output_path,
            rate=170
        )
        
        log(f"转换结果: {'成功' if result else '失败'}")
        
        # 检查输出文件
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            log(f"[成功] 输出视频文件存在: {output_path}")
            log(f"  文件大小: {file_size} 字节")
            if file_size < 1024:
                log("[失败] 视频文件太小，可能有问题")
            else:
                log("[成功] 视频文件大小正常")
        else:
            log(f"[失败] 输出视频文件不存在: {output_path}")
    else:
        log("跳过转换测试：测试PPT不存在")
        
except Exception as e:
    log(f"[失败] 导入或转换失败: {e}")
    log(traceback.format_exc())

log("=== 直接测试完成 ===")
log("\n")
