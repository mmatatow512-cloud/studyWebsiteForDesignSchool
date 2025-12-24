import pyttsx3
import os

try:
    print("初始化pyttsx3引擎...")
    engine = pyttsx3.init()
    print("✓ pyttsx3引擎初始化成功")
    
    # 测试基本功能
    print("\n获取语音包列表...")
    voices = engine.getProperty('voices')
    print(f"✓ 获取到 {len(voices)} 个语音包")
    
    # 简单文本合成
    text = "测试"
    output_file = "simple_test.wav"
    
    print(f"\n将文本 '{text}' 合成到文件 {output_file}...")
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    
    if os.path.exists(output_file):
        size = os.path.getsize(output_file)
        print(f"✓ 合成成功，文件大小: {size} 字节")
    else:
        print(f"✗ 合成失败，文件不存在")
        
except Exception as e:
    print(f"✗ 错误: {e}")
    import traceback
    traceback.print_exc()