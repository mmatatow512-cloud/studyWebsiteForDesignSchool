import os
import numpy as np
import sys

print("=== 简单音频测试 ===")
print(f"Python版本: {sys.version}")

# 尝试导入moviepy相关模块
try:
    from moviepy.audio.AudioClip import AudioArrayClip
    print("✓ 成功导入AudioArrayClip")
except Exception as e:
    print(f"✗ 导入AudioArrayClip失败: {e}")
    exit(1)

# 生成简单的正弦波音频
try:
    duration = 2  # 2秒
    samples = int(duration * 44100)
    t = np.linspace(0, duration, samples)
    audio_array = np.sin(2 * np.pi * 440 * t)  # 440Hz正弦波
    audio_array = np.column_stack((audio_array, audio_array))  # 立体声
    audio_array = audio_array.astype(np.float32)
    
    print(f"✓ 音频数组生成成功")
    print(f"  数组形状: {audio_array.shape}")
    print(f"  数组类型: {audio_array.dtype}")
    
    # 创建AudioArrayClip
    audio_clip = AudioArrayClip(audio_array, fps=44100)
    print("✓ AudioArrayClip创建成功")
    
    # 保存音频文件
    output_path = "test_audio.wav"
    audio_clip.write_audiofile(output_path, fps=44100)
    
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"✓ 音频文件保存成功: {output_path}")
        print(f"  文件大小: {file_size} 字节")
        if file_size > 1024:
            print("✓ 音频文件有效")
        else:
            print("✗ 音频文件可能无效（太小）")
    else:
        print(f"✗ 音频文件保存失败: {output_path}")
        
except Exception as e:
    print(f"✗ 音频生成过程中出错: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n=== 测试完成 ===")
