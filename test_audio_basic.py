# 最基本的音频生成测试
import os
import numpy as np
from moviepy.audio.AudioClip import AudioArrayClip

# 生成简单的正弦波音频
print("=== 基本音频生成测试开始 ===")

# 设置参数
duration = 3.0  # 3秒
sample_rate = 44100
frequency = 440.0  # A4音

# 创建音频数组
t = np.linspace(0, duration, int(sample_rate * duration))
audio_array = np.sin(2 * np.pi * frequency * t)

# 转换为立体声
audio_array = np.column_stack((audio_array, audio_array)).astype(np.float32)

# 创建音频片段
print("创建音频片段...")
audio_clip = AudioArrayClip(audio_array, fps=sample_rate)

# 保存音频文件
audio_path = "test_sine_wave.wav"
print(f"保存音频到: {audio_path}")
try:
    audio_clip.write_audiofile(audio_path, fps=sample_rate)
    print("音频保存成功")
    
    # 验证文件存在且大小合适
    if os.path.exists(audio_path):
        file_size = os.path.getsize(audio_path)
        print(f"文件大小: {file_size} 字节")
        if file_size > 1024:
            print("✓ 音频文件有效")
        else:
            print("✗ 音频文件太小")
    else:
        print("✗ 音频文件不存在")
        
except Exception as e:
    print(f"✗ 音频保存失败: {e}")
    import traceback
    traceback.print_exc()

print("=== 基本音频生成测试结束 ===")
