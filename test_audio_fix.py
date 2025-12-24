#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试音频生成修复效果的脚本
"""

import sys
import os
import tempfile
import shutil

# 添加项目目录到Python路径
sys.path.append('c:\\Users\\23576\\Desktop\\demo\\project')

from ppt2video import ConverterLogic

def test_log(message):
    """测试用日志函数"""
    print(f"[LOG] {message}")

def main():
    """测试音频生成功能"""
    test_log("=== 开始测试音频生成修复效果 ===")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    test_log(f"创建临时目录: {temp_dir}")
    
    try:
        # 创建ConverterLogic实例
        converter = ConverterLogic(test_log)
        
        # 测试用例1：之前卡住的文本
        test_text = "，，西方艺术风格的五个关键时代，，，• 古典艺术的奠基..."
        
        # 测试用例2：包含特殊符号的文本
        test_text2 = "• 古典艺术时期 • 文艺复兴时期 • 巴洛克艺术 • 新古典主义 • 现代艺术"
        
        # 测试用例3：正常文本
        test_text3 = "这是一张测试幻灯片，包含正常的中文文本内容。"
        
        # 组合测试
        scripts = [
            test_text,      # 幻灯片1：之前卡住的文本
            test_text2,     # 幻灯片2：包含特殊符号
            test_text3      # 幻灯片3：正常文本
        ]
        
        test_log(f"准备测试 {len(scripts)} 个幻灯片的音频生成")
        
        # 测试音频生成
        test_log("\n开始生成音频...")
        audio_paths = converter.generate_audio(scripts, temp_dir, None, 150)
        
        test_log(f"\n音频生成完成，共生成 {len(audio_paths)} 个音频文件")
        
        # 验证生成的文件
        success_count = 0
        for i, audio_path in enumerate(audio_paths):
            if os.path.exists(audio_path):
                size = os.path.getsize(audio_path)
                if size > 1024:  # 大于1KB视为有效
                    test_log(f"✓ 幻灯片 {i+1} 音频文件有效: {audio_path} ({size/1024:.2f} KB)")
                    success_count += 1
                else:
                    test_log(f"✗ 幻灯片 {i+1} 音频文件太小: {audio_path} ({size/1024:.2f} KB)")
            else:
                test_log(f"✗ 幻灯片 {i+1} 音频文件不存在: {audio_path}")
        
        test_log(f"\n测试结果: {success_count}/{len(scripts)} 个音频生成成功")
        
        if success_count == len(scripts):
            test_log("✓ 所有测试用例通过！音频生成修复成功！")
            return True
        else:
            test_log("✗ 部分测试用例失败！")
            return False
            
    except Exception as e:
        test_log(f"✗ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)
        test_log(f"\n清理临时目录: {temp_dir}")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
