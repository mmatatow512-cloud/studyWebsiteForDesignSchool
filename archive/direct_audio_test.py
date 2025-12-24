#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct test for audio generation functionality
"""

import os
import sys
import tempfile
import traceback

# 添加项目目录到Python路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.join(script_dir, 'project')
sys.path.append(project_path)
print(f"Added project path: {project_path}")

# 简单的日志函数
def log(message):
    print(f"[LOG] {message}")

def main():
    """Main test function"""
    print("=== Direct Audio Generation Test ===")
    
    try:
        # 导入ConverterLogic类
        log("Importing ConverterLogic...")
        from ppt2video import ConverterLogic
        
        # 创建ConverterLogic实例
        converter = ConverterLogic(logger_func=log)
        
        # 测试脚本 - 包含之前导致卡住的问题文本
        test_scripts = [
            "，，西方艺术风格的五个关键时代，，，• 古典艺术的奠基...",
            "这是一个正常的测试文本。",
            "••• 测试特殊符号的处理 •••",
            "测试非常长的文本，这是一个非常长的测试文本，目的是测试文本长度限制功能是否正常工作，应该会被截断到100字符以内..."
        ]
        
        log(f"测试脚本数量: {len(test_scripts)}")
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        log(f"临时目录: {temp_dir}")
        
        # 测试音频生成
        log("开始音频生成...")
        audio_paths = converter.generate_audio(
            scripts=test_scripts,
            temp_folder=temp_dir,
            voice_id=None,
            rate=150
        )
        
        log(f"音频生成完成，生成了 {len(audio_paths)} 个音频文件")
        
        # 验证音频文件
        success = True
        for i, audio_path in enumerate(audio_paths):
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path)
                log(f"第 {i+1} 个音频文件: {audio_path}，大小: {file_size} 字节")
                if file_size > 1024:
                    log("✓ 音频文件有效")
                else:
                    log("✗ 音频文件太小")
                    success = False
            else:
                log(f"✗ 第 {i+1} 个音频文件未生成: {audio_path}")
                success = False
        
        # 清理临时目录
        import shutil
        shutil.rmtree(temp_dir)
        log("临时目录已清理")
        
        if success and len(audio_paths) == len(test_scripts):
            print("\n🎉 音频生成测试成功！")
            return 0
        else:
            print("\n❌ 音频生成测试失败！")
            return 1
            
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())