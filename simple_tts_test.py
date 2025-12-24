#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化的TTS测试脚本
"""

import pyttsx3
import os
import sys
import json
import re

def main():
    # 测试文本
    text = "，，西方艺术风格的五个关键时代，，，• 古典艺术的奠基..."
    
    # 清理文本
    cleaned_text = text
    # 移除重复的标点符号
    cleaned_text = re.sub(r'[，。、；："\'\n\r]+', '，', cleaned_text)
    # 移除重复的顿号
    cleaned_text = re.sub(r'[，]+', '，', cleaned_text)
    # 移除省略号
    cleaned_text = re.sub(r'[.]+', '', cleaned_text)
    # 移除特殊符号
    cleaned_text = re.sub(r'[•●■◆]', '', cleaned_text)
    # 限制文本长度
    if len(cleaned_text) > 100:
        cleaned_text = cleaned_text[:100] + "..."

    if not cleaned_text.strip():
        cleaned_text = "空白幻灯片"
    
    print(f"清理后的文本: {cleaned_text}")
    
    # 初始化引擎
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    
    # 设置中文语音
    voices = engine.getProperty('voices')
    chinese_voice_found = False
    for voice in voices:
        print(f"可用语音: {voice.id}, {voice.name}")
        if 'chinese' in voice.id.lower() or 'zh' in voice.id.lower() or 'mandarin' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            chinese_voice_found = True
            break
    
    if not chinese_voice_found and voices:
        print(f"未找到中文语音，使用第一个可用语音: {voices[0].id}")
        engine.setProperty('voice', voices[0].id)
    
    # 生成音频
    output_file = "test_tts.wav"
    engine.save_to_file(cleaned_text, output_file)
    engine.runAndWait()
    
    # 验证文件
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"\n音频文件生成成功: {output_file}")
        print(f"文件大小: {file_size} 字节")
    else:
        print(f"\n音频文件生成失败: {output_file}")

if __name__ == "__main__":
    main()