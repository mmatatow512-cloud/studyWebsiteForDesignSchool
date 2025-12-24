#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试generate_audio方法的修复效果
"""

import sys
import os
import json
import tempfile
import shutil

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ppt2video import ConverterLogic

# 简单的日志函数
def simple_log(message):
    print(f"[LOG] {message}")

def test_generate_audio():
    """测试generate_audio方法"""
    print("=== 测试generate_audio方法修复效果 ===")
    print(f"Python版本: {sys.version}")
    
    # 创建临时目录
    temp_folder = tempfile.mkdtemp(prefix="audio_test_")
    print(f"临时目录: {temp_folder}")
    
    try:
        # 创建测试用的ConverterLogic实例
        logic = ConverterLogic(logger_func=simple_log)
        
        # 测试数据：包含之前导致卡住的特殊字符
        test_scripts = [
            "，，西方艺术风格的五个关键时代，，，• 古典艺术的奠基...",
            "文艺复兴时期的艺术特点包括人文主义、透视法和写实主义",
            "巴洛克艺术以戏剧性、动态感和装饰性为主要特征",
            "洛可可艺术风格轻盈、精致，充满了装饰性元素",
            "新古典主义回归古典艺术的简洁和理性",
            "现代主义艺术打破传统，探索新的表现形式"
        ]
        
        print(f"测试脚本数量: {len(test_scripts)}")
        for i, script in enumerate(test_scripts):
            print(f"  {i+1}. {script[:50]}..." if len(script) > 50 else f"  {i+1}. {script}")
        
        # 测试音频生成
        print("\n开始生成音频...")
        audio_paths = logic.generate_audio(
            scripts=test_scripts,
            temp_folder=temp_folder,
            voice_id=None,
            rate=150
        )
        
        print(f"\n音频生成完成")
        print(f"生成的音频文件数量: {len(audio_paths)}")
        
        # 验证音频文件
        valid_audio_count = 0
        for i, audio_path in enumerate(audio_paths):
            if os.path.exists(audio_path):
                size = os.path.getsize(audio_path)
                if size > 1024:  # 大于1KB才视为有效
                    valid_audio_count += 1
                    print(f"  ✓ 音频{i+1}: {os.path.basename(audio_path)} - 大小: {size} 字节")
                else:
                    print(f"  ✗ 音频{i+1}: {os.path.basename(audio_path)} - 太小 ({size} 字节)")
            else:
                print(f"  ✗ 音频{i+1}: {os.path.basename(audio_path)} - 文件不存在")
        
        print(f"\n有效音频文件数量: {valid_audio_count}/{len(test_scripts)}")
        
        if valid_audio_count == len(test_scripts):
            print("\n🎉 测试通过: 所有音频文件都成功生成！")
            return True
        else:
            print(f"\n❌ 测试失败: 只有 {valid_audio_count} 个音频文件有效")
            return False
            
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
    success = test_generate_audio()
    sys.exit(0 if success else 1)