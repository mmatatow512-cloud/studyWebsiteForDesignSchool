#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 ppt2video.py 核心功能的脚本
"""

import sys
import os
import traceback
import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ppt2video import convert_presentation_to_video


class Logger:
    def __init__(self, log_file="test_detailed.log"):
        self.log_file = log_file
        # 清空日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"[LOG START] {datetime.datetime.now()}\n")
        self.stdout = sys.stdout
        # 重定向标准输出
        sys.stdout = self
    
    def write(self, message):
        # 写入文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(message)
        # 同时输出到控制台
        self.stdout.write(message)
    
    def flush(self):
        self.stdout.flush()


def main():
    logger = Logger()
    print("[TEST] 开始测试 ppt2video.py 核心功能...")
    
    try:
        # 1. 测试直接调用核心转换函数
        print("[TEST] 1. 调用 convert_presentation_to_video 函数...")
        
        # 确保输出目录存在
        if not os.path.exists("test_output"):
            os.makedirs("test_output")
        
        # 调用转换函数
        success = convert_presentation_to_video(
            ppt_path="test_ppt.pptx",
            output_path=r"test_output\test_result.mp4",
            rate=170
        )
        
        print(f"[TEST] 转换结果: {'成功' if success else '失败'}")
        
        # 2. 检查输出文件
        print("[TEST] 2. 检查输出文件...")
        output_file = r"test_output\test_result.mp4"
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"[TEST] 输出文件存在，大小: {file_size} 字节 ({file_size / 1024:.2f} KB)")
            
            if file_size < 1024:
                print("[TEST] [警告] 输出文件太小，可能有问题")
            else:
                print("[TEST] [成功] 输出文件大小正常")
        else:
            print("[TEST] [错误] 输出文件不存在")
            
        return success
        
    except Exception as e:
        print(f"[TEST] [错误] 测试过程中发生异常: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
