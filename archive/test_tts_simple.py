import pyttsx3
import json
import os
import tempfile

# 测试文本
test_text = "这是一段测试文本，用于验证TTS功能是否正常工作。"
temp_file = tempfile.mktemp(suffix='.wav')

print("测试pyttsx3 TTS功能...")
print(f"测试文本: {test_text}")
print(f"输出文件: {temp_file}")

try:
    # 初始化引擎
    engine = pyttsx3.init()
    print("\n1. 引擎初始化成功")
    
    # 获取所有可用语音
    voices = engine.getProperty('voices')
    print(f"\n2. 找到 {len(voices)} 个可用语音:")
    for i, voice in enumerate(voices):
        print(f"   {i+1}. ID: {voice.id}")
        print(f"      Name: {voice.name}")
        if hasattr(voice, 'languages'):
            print(f"      Languages: {voice.languages}")
        if hasattr(voice, 'gender'):
            print(f"      Gender: {voice.gender}")
        if hasattr(voice, 'age'):
            print(f"      Age: {voice.age}")
    
    # 查找中文语音
    print("\n3. 查找中文语音:")
    chinese_voice = None
    for voice in voices:
        voice_id_lower = voice.id.lower()
        voice_name_lower = voice.name.lower()
        
        # 中文语音关键词匹配
        if any(keyword in voice_id_lower or keyword in voice_name_lower 
               for keyword in ['chinese', 'zh', 'mandarin', '中文', '普通话', 'cantonese', 'yue']):
            chinese_voice = voice
            print(f"   找到中文语音: {voice.name} (ID: {voice.id})")
            break
    
    if chinese_voice:
        engine.setProperty('voice', chinese_voice.id)
        print(f"   使用中文语音: {chinese_voice.name}")
    else:
        print(f"   未找到中文语音，使用默认语音")
    
    # 设置语速
    engine.setProperty('rate', 150)
    
    # 生成音频
    print("\n4. 生成音频...")
    engine.save_to_file(test_text, temp_file)
    engine.runAndWait()
    
    # 检查文件
    if os.path.exists(temp_file):
        file_size = os.path.getsize(temp_file)
        print(f"   音频文件生成成功，大小: {file_size} 字节")
    else:
        print("   音频文件生成失败")
        
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成")
