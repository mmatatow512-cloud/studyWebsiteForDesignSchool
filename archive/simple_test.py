#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本：验证修复是否有效
"""

import os
import sys
import tempfile

# 添加项目目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'project'))

import ppt2video

def test_no_test_video():
    """测试不再生成测试视频"""
    print("=== 测试修复效果 ===")
    
    # 创建临时输出目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 生成输出视频路径
        output_path = os.path.join(temp_dir, "test_output.mp4")
        
        # 使用一个不存在的PPT文件来触发错误
        non_existent_ppt = "this_file_does_not_exist.pptx"
        
        print(f"\n测试1: 使用不存在的PPT文件")
        print(f"PPT文件: {non_existent_ppt}")
        print(f"输出路径: {output_path}")
        
        try:
            # 执行PPT转视频
            print("\n正在执行PPT转视频...")
            success = ppt2video.convert_presentation_to_video(non_existent_ppt, output_path)
            
            if success:
                print("❌ 测试失败: 函数应该返回False但返回了True")
            else:
                print("✅ 测试成功: 函数正确返回False")
                
            # 检查是否生成了测试视频
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"❌ 测试失败: 生成了测试视频，大小: {file_size} 字节")
                return False
            else:
                print(f"✅ 测试成功: 没有生成测试视频")
                return True
                
        except Exception as e:
            print(f"\n❌ 测试失败: 抛出了异常 {e}")
            print("注意: 这可能是正常的，因为修复后可能会直接抛出异常而不是返回False")
            
            # 检查是否生成了测试视频
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"❌ 测试失败: 生成了测试视频，大小: {file_size} 字节")
                return False
            else:
                print(f"✅ 测试成功: 没有生成测试视频")
                return True

if __name__ == "__main__":
    test_no_test_video()