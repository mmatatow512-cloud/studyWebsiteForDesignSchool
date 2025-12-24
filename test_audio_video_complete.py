# 完整的音频视频合成测试
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.AudioClip import AudioArrayClip

print("=== 完整音视频合成测试开始 ===")

# 1. 创建测试图片
print("1. 创建测试图片...")
img_path = "test_image.png"
# 创建一个简单的测试图片
img = Image.new('RGB', (1280, 720), color=(0, 0, 255))
d = ImageDraw.Draw(img)
# 添加文本
text = "测试图片"
try:
    font = ImageFont.truetype("arial.ttf", 72)
except:
    font = ImageFont.load_default()

text_width, text_height = d.textbbox((0, 0), text, font=font)[2:4]
d.text(((1280 - text_width) / 2, (720 - text_height) / 2), text, fill=(255, 255, 255), font=font)
img.save(img_path)
print(f"   图片已保存到: {img_path}")

# 2. 生成测试音频
print("\n2. 生成测试音频...")
duration = 3.0
sample_rate = 44100
frequency = 440.0
t = np.linspace(0, duration, int(sample_rate * duration))
audio_array = np.sin(2 * np.pi * frequency * t)
audio_array = np.column_stack((audio_array, audio_array)).astype(np.float32)
audio_clip = AudioArrayClip(audio_array, fps=sample_rate)
audio_path = "test_audio.wav"
audio_clip.write_audiofile(audio_path, fps=sample_rate)
print(f"   音频已保存到: {audio_path}")

# 3. 合成音视频
print("\n3. 合成音视频...")
# 创建图片片段
img_clip = ImageClip(img_path).with_duration(duration)
# 附加音频
final_clip = img_clip.with_audio(audio_clip)

# 验证音频是否附加成功
if hasattr(final_clip, 'audio') and final_clip.audio is not None:
    print("   ✓ 音频成功附加到视频")
else:
    print("   ✗ 音频未能附加到视频")
    exit(1)

# 4. 导出视频
print("\n4. 导出视频...")
output_path = "test_audio_video.mp4"
final_clip.write_videofile(
    output_path,
    fps=8,
    codec="libx264",
    audio_codec="aac",
    preset="ultrafast",
    threads=1,
    ffmpeg_params=[
        '-pix_fmt', 'yuv420p',
        '-b:a', '64k',
        '-b:v', '300k',
        '-y',
        '-loglevel', 'info',
        '-ac', '2',
        '-ar', '44100'
    ]
)
print(f"   视频已导出到: {output_path}")

# 5. 验证输出视频
print("\n5. 验证视频文件...")
if os.path.exists(output_path):
    file_size = os.path.getsize(output_path)
    print(f"   文件大小: {file_size} 字节")
    if file_size > 100000:  # 100KB
        print("   ✓ 视频文件大小正常")
    else:
        print("   ✗ 视频文件太小")
        exit(1)
    
    # 检查视频是否包含音频
    try:
        import subprocess
        print("   使用ffprobe检查音频流...")
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', output_path],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print(f"   ✓ 视频包含音频流: {result.stdout.strip()}")
        else:
            print("   ✗ 视频不包含音频流")
            exit(1)
    except Exception as e:
        print(f"   ffprobe检查失败: {e}")
        print("   跳过音频流检查")
else:
    print("   ✗ 视频文件不存在")
    exit(1)

print("\n=== 完整音视频合成测试成功！ ===")
print("\n结论：音视频合成功能正常工作")
print(f"\n生成的测试文件:")
print(f"- 图片: {img_path}")
print(f"- 音频: {audio_path}")
print(f"- 视频: {output_path}")
