#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试音频生成修复是否有效
"""

import os
import sys
import tempfile
import shutil

# 添加项目目录到Python路径
sys.path.append(r'c:\Users\23576\Desktop\demo\project')

from ppt2video import PPTtoVideoConverter

def test_audio_generation():
    """测试音频生成功能"""
    # 创建临时目录
    temp_folder = tempfile.mkdtemp()
    
    try:
        # 创建PPTtoVideoConverter实例
        ppt_converter = PPTtoVideoConverter()
        
        # 测试之前导致问题的文本
        test_texts = [
            "，，西方艺术风格的五个关键时代，，，• 古典艺术的奠基...",
            "第二页内容",
            "第三页内容包含特殊符号•和●",
            "第四页有重复的标点符号，，，，，，和省略号........",
            "",  # 空白幻灯片
        ]
        
        print("=== 测试音频生成功能 ===")
        print(f"测试文本: {test_texts}")
        print(f"临时目录: {temp_folder}")
        
        # 生成音频
        audio_paths = ppt_converter.generate_audio(
            scripts=test_texts,
            temp_folder=temp_folder,
            voice_id=None,
            rate=150
        )
        
        print(f"\n=== 测试结果 ===")
        print(f"生成的音频文件数量: {len(audio_paths)}")
        
        # 检查音频文件是否有效
        for i, audio_path in enumerate(audio_paths):
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path)
                print(f"  音频 {i+1}: {audio_path} - 大小: {file_size} 字节 {'✓' if file_size > 1024 else '✗'}")
            else:
                print(f"  音频 {i+1}: {audio_path} - 文件不存在 ✗")
        
        # 验证是否所有幻灯片都生成了音频
        if len(audio_paths) == len(test_texts):
            print(f"\n✅ 测试通过: 所有 {len(test_texts)} 页幻灯片都生成了音频")
            return True
        else:
            print(f"\n❌ 测试失败: 只生成了 {len(audio_paths)} 个音频文件，应该生成 {len(test_texts)} 个")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试失败: 发生错误 {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理临时目录
        shutil.rmtree(temp_folder)

if __name__ == "__main__":
    # 获取真实的Python路径
    real_python = r'C:\Users\23576\AppData\Local\Programs\Python\Python314\python.exe'
    
    if os.path.exists(real_python):
        print(f"使用真实Python解释器: {real_python}")
        print(f"当前Python解释器: {sys.executable}")
    
    test_audio_generation()
