#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试完整的PPT转视频流程
"""

import sys
import os
import tempfile
import shutil
import time

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ppt2video import ConverterLogic

def simple_log(message):
    """简单的日志函数"""
    print(f"[LOG] {message}")

def test_full_ppt2video():
    """测试完整的PPT转视频流程"""
    print("=== 测试完整的PPT转视频流程 ===")
    print(f"Python版本: {sys.version}")
    
    # 创建临时目录
    temp_folder = tempfile.mkdtemp(prefix="ppt2video_test_")
    print(f"临时目录: {temp_folder}")
    
    # 确保有测试用的PPT文件
    test_ppt_path = "test_ppt.pptx"
    if not os.path.exists(test_ppt_path):
        print(f"❌ 测试PPT文件不存在: {test_ppt_path}")
        return False
    
    print(f"测试PPT文件: {test_ppt_path}")
    
    try:
        # 创建ConverterLogic实例
        logic = ConverterLogic(logger_func=simple_log)
        
        # 测试步骤1: 导出PPT图片
        print("\n=== 步骤1: 导出PPT图片 ===")
        image_paths = logic.export_images(test_ppt_path, temp_folder)
        if not image_paths:
            print("❌ PPT图片导出失败")
            return False
        print(f"✅ 成功导出 {len(image_paths)} 张图片")
        for i, img_path in enumerate(image_paths):
            print(f"  图片{i+1}: {os.path.basename(img_path)}")
        
        # 测试步骤2: 生成音频
        print("\n=== 步骤2: 生成音频 ===")
        # 使用简单的测试脚本
        test_scripts = [
            f"这是第{i+1}页的测试文本，用于演示PPT转视频功能。"
            for i in range(len(image_paths))
        ]
        
        audio_paths = logic.generate_audio(
            scripts=test_scripts,
            temp_folder=temp_folder,
            voice_id=None,
            rate=150
        )
        
        if not audio_paths or len(audio_paths) != len(image_paths):
            print(f"❌ 音频生成失败，期望 {len(image_paths)} 个音频，实际生成 {len(audio_paths)} 个")
            return False
        print(f"✅ 成功生成 {len(audio_paths)} 个音频文件")
        for i, audio_path in enumerate(audio_paths):
            if os.path.exists(audio_path):
                size = os.path.getsize(audio_path)
                print(f"  音频{i+1}: {os.path.basename(audio_path)} ({size/1024:.2f} KB)")
            else:
                print(f"  音频{i+1}: {os.path.basename(audio_path)} - 文件不存在")
        
        # 测试步骤3: 合成视频
        print("\n=== 步骤3: 合成视频 ===")
        output_path = os.path.join(temp_folder, f"test_output_{int(time.time())}.mp4")
        result = logic.create_video(image_paths, audio_paths, output_path)
        
        if result and os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✅ 视频合成成功")
            print(f"   输出文件: {output_path}")
            print(f"   文件大小: {size/1024/1024:.2f} MB")
        else:
            print("❌ 视频合成失败")
            return False
        
        print("\n🎉 完整的PPT转视频测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理临时目录
        print(f"\n清理临时目录: {temp_folder}")
        shutil.rmtree(temp_folder, ignore_errors=True)

if __name__ == "__main__":
    success = test_full_ppt2video()
    sys.exit(0 if success else 1)