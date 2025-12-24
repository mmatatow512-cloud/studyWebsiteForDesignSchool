import pyttsx3

def list_available_voices():
    """列出系统中所有可用的语音包"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print("系统中可用的语音包:")
    print(f"总共找到 {len(voices)} 个语音包")
    print("=" * 60)
    
    for i, voice in enumerate(voices):
        print(f"语音包 {i + 1}:")
        print(f"  ID: {voice.id}")
        print(f"  姓名: {voice.name}")
        print(f"  语言: {voice.languages}")
        print(f"  性别: {voice.gender}")
        print(f"  年龄: {voice.age}")
        print(f"  ID小写: {voice.id.lower()}")
        print("=" * 60)
    
    # 测试中文语音检测
    print("\n中文语音检测测试:")
    chinese_voices = [voice for voice in voices if 
                      'chinese' in voice.id.lower() or 
                      'zh' in voice.id.lower() or 
                      'mandarin' in voice.id.lower() or
                      '中文' in voice.name or
                      '普通话' in voice.name]
    
    print(f"检测到 {len(chinese_voices)} 个中文语音包")
    for voice in chinese_voices:
        print(f"  - {voice.name} ({voice.id})")
    
    return voices

def test_tts(text, voice_id=None):
    """测试TTS功能"""
    print(f"\n测试TTS功能，文本: '{text}'")
    print(f"使用语音包: {voice_id}")
    
    engine = pyttsx3.init()
    
    if voice_id:
        engine.setProperty('voice', voice_id)
    
    # 设置语速
    engine.setProperty('rate', 150)
    
    # 保存到文件测试
    output_file = "test_tts_output.wav"
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    
    import os
    if os.path.exists(output_file):
        size = os.path.getsize(output_file)
        print(f"✓ TTS成功，生成文件: {output_file} ({size} 字节)")
    else:
        print(f"✗ TTS失败，未生成文件")

if __name__ == "__main__":
    voices = list_available_voices()
    
    # 测试中文TTS
    test_text = "这是一个中文语音合成测试，用于检查PPT转视频工具的语音功能。"
    
    # 尝试使用中文语音包
    chinese_voices = [voice for voice in voices if 
                      'chinese' in voice.id.lower() or 
                      'zh' in voice.id.lower() or 
                      'mandarin' in voice.id.lower()]
    
    if chinese_voices:
        test_tts(test_text, chinese_voices[0].id)
    else:
        # 尝试使用第一个可用语音
        if voices:
            test_tts(test_text, voices[0].id)
        else:
            print("系统中没有可用的语音包!")