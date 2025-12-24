#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试音频生成功能
"""

import sys
import os
import traceback
import tempfile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ppt2video import ConverterLogic

def simple_log(message):
    print(f"[LOG] {message}")

def main():
    print("[TEST] 开始测试音频生成功能...")
    
    try:
        # 创建临时目录
        temp_aud = tempfile.mkdtemp()
        print(f"[TEST] 临时目录: {temp_aud}")
        
        # 创建转换器实例
        logic = ConverterLogic(simple_log)
        
        # 测试音频生成
        scripts = ["这是测试文本1", "这是测试文本2", "这是测试文本3"]
        print(f"[TEST] 测试文本: {scripts}")
        
        audios = logic.generate_audio(scripts, temp_aud, None, 170)
        print(f"[TEST] 生成音频文件数量: {len(audios)}")
        
        # 检查音频文件
        for i, audio in enumerate(audios):
            if os.path.exists(audio):
                size = os.path.getsize(audio)
                print(f"[TEST] 音频文件 {i+1}: {audio}，大小: {size} 字节")
            else:
                print(f"[TEST] 音频文件 {i+1}: {audio} 不存在")
        
        return True
        
    except Exception as e:
        print(f"[TEST] 发生异常: {e}")
        traceback.print_exc()
        return False
    finally:
        # 清理临时目录
        if 'temp_aud' in locals() and os.path.exists(temp_aud):
            import shutil
            try:
                shutil.rmtree(temp_aud)
                print(f"[TEST] 清理临时目录: {temp_aud}")
            except:
                pass

if __name__ == "__main__":
    main()