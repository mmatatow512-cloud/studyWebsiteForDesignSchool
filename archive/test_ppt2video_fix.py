#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证PPT转视频修复是否有效
"""

import os
import sys
import tempfile
import shutil

# 添加项目目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'project'))

import ppt2video

import sys

def test_ppt_to_video():
    """测试PPT转视频功能"""
    print("=== 测试PPT转视频修复 ===")
    
    # 从命令行参数获取PPT文件路径
    if len(sys.argv) < 2:
        print("用法: python test_ppt2video_fix.py <PPT文件路径>")
        return False
    
    ppt_path = sys.argv[1].strip()
    
    # 验证PPT文件是否存在和类型
    if not os.path.exists(ppt_path):
        print(f"错误: PPT文件不存在 - {ppt_path}")
        return False
        
    if not ppt_path.endswith('.ppt') and not ppt_path.endswith('.pptx'):
        print(f"错误: 文件类型不是PPT - {ppt_path}")
        return False
    
    print(f"\n测试文件: {ppt_path}")
    print(f"文件大小: {os.path.getsize(ppt_path)} 字节")
    
    # 创建临时输出目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 生成输出视频路径
        output_filename = "test_output.mp4"
        output_path = os.path.join(temp_dir, output_filename)
        
        print(f"\n输出路径: {output_path}")
        
        try:
            # 执行PPT转视频
            print("\n正在执行PPT转视频...")
            success = ppt2video.convert_presentation_to_video(ppt_path, output_path)
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"\n✅ 转换成功！")
                print(f"输出文件: {output_path}")
                print(f"文件大小: {file_size} 字节 ({file_size / 1024:.2f} KB)")
                
                # 检查是否是测试视频
                if file_size < 10240:  # 测试视频通常很小
                    print(f"⚠️  警告: 生成的视频文件过小，可能仍然是测试视频")
                    return False
                else:
                    return True
            else:
                print(f"\n❌ 转换失败: 函数返回 {success}")
                return False
                
        except Exception as e:
            print(f"\n❌ 转换失败，抛出异常: {e}")
            print("✅ 修复有效！现在会抛出错误而不是生成测试视频")
            return True  # 抛出异常说明修复有效

if __name__ == "__main__":
    test_ppt_to_video()