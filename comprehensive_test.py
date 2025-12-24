#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面测试脚本：测试PPT转视频功能
"""

import os
import sys
import traceback
import logging
import time

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ppt2video import convert_presentation_to_video

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='comprehensive_test.log',
    filemode='w',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

# 控制台也输出日志
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(console_handler)

def main():
    """主测试函数"""
    logger.info("=== 开始PPT转视频全面测试 ===")
    
    # 测试文件路径
    test_ppt_path = "test_ppt.pptx"
    test_output_path = "test_output.mp4"
    
    # 检查测试PPT是否存在
    if not os.path.exists(test_ppt_path):
        logger.error(f"测试PPT文件不存在: {test_ppt_path}")
        logger.error("请确保在当前目录下有一个名为 test_ppt.pptx 的测试文件")
        return False
    
    logger.info(f"测试PPT路径: {os.path.abspath(test_ppt_path)}")
    logger.info(f"PPT文件大小: {os.path.getsize(test_ppt_path)} 字节")
    logger.info(f"输出视频路径: {os.path.abspath(test_output_path)}")
    
    # 记录开始时间
    start_time = time.time()
    
    try:
        # 执行转换
        logger.info("开始执行PPT转视频转换...")
        success = convert_presentation_to_video(test_ppt_path, test_output_path)
        
        # 记录结束时间
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"转换耗时: {elapsed_time:.2f} 秒")
        
        if success:
            logger.info("=== 测试成功！视频已生成 ===")
            # 验证输出文件
            if os.path.exists(test_output_path):
                file_size = os.path.getsize(test_output_path)
                logger.info(f"视频文件大小: {file_size} 字节 ({file_size / 1024:.2f} KB)")
                
                if file_size < 10240:  # 小于10KB视为异常
                    logger.error(f"[警告] 视频文件过小: {file_size} 字节")
                    return False
                else:
                    logger.info("视频文件大小正常")
                    return True
            else:
                logger.error("视频文件生成失败，文件不存在")
                return False
        else:
            logger.error("=== 测试失败！视频生成失败 ===")
            # 检查是否生成了测试视频
            if os.path.exists(test_output_path):
                file_size = os.path.getsize(test_output_path)
                logger.info(f"测试视频文件大小: {file_size} 字节")
            return False
            
    except Exception as e:
        logger.error(f"测试过程中发生异常: {e}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    result = main()
    sys.exit(0 if result else 1)
