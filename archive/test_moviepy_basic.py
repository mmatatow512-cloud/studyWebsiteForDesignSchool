import os
import sys
import tempfile
import datetime

print("=== MoviePy 基础功能测试 ===")
print(f"当前时间: {datetime.datetime.now()}")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")

# 测试1: 检查MoviePy是否正确导入
print("\n--- 测试1: 导入MoviePy组件 ---")
try:
    from moviepy.video.VideoClip import ColorClip
    from moviepy.audio.AudioClip import AudioClip
    import numpy as np
    print("✅ MoviePy组件导入成功")
except Exception as e:
    print(f"❌ MoviePy导入失败: {e}")
    sys.exit(1)

# 测试2: 检查FFmpeg配置
print("\n--- 测试2: FFmpeg配置检查 ---")
try:
    import imageio_ffmpeg
    print(f"  imageio_ffmpeg版本: {imageio_ffmpeg.__version__}")
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"  FFmpeg路径: {ffmpeg_path}")
    print(f"  FFmpeg存在: {os.path.exists(ffmpeg_path)}")
    if os.path.exists(ffmpeg_path):
        print(f"  FFmpeg文件大小: {os.path.getsize(ffmpeg_path):,} 字节")
    else:
        print("  ❌ FFmpeg不存在")
        sys.exit(1)
except Exception as e:
    print(f"❌ FFmpeg检查失败: {e}")
    sys.exit(1)

# 测试3: 生成简单的彩色视频
print("\n--- 测试3: 生成简单彩色视频 ---")
try:
    # 创建临时目录
    temp_dir = tempfile.mkdtemp(prefix="moviepy_test_")
    print(f"  临时目录: {temp_dir}")
    
    # 生成简单彩色视频
    output_path = os.path.join(temp_dir, "test_color.mp4")
    print(f"  输出路径: {output_path}")
    
    # 使用最小的参数设置
    color_clip = ColorClip(size=(320, 240), color=(0, 255, 0), duration=2)
    color_clip.write_videofile(
        output_path,
        fps=10,
        codec="libx264",
        audio_codec=None,
        preset="ultrafast",
        threads=1,
        ffmpeg_params=[
            '-pix_fmt', 'yuv420p',
            '-y',
            '-loglevel', 'info'
        ],
        logger='bar'
    )
    color_clip.close()
    
    # 检查文件
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"✅ 彩色视频生成成功！")
        print(f"  文件大小: {file_size:,} 字节 ({file_size/1024:.2f} KB)")
        print(f"  文件路径: {output_path}")
        
        if file_size < 1024:
            print("❌ 警告: 文件大小小于1KB，可能存在问题")
        else:
            print("✅ 文件大小正常")
    else:
        print("❌ 彩色视频生成失败，文件不存在")
except Exception as e:
    print(f"❌ 彩色视频生成失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试4: 生成带音频的视频
print("\n--- 测试4: 生成带音频的视频 ---")
try:
    output_path = os.path.join(temp_dir, "test_audio.mp4")
    print(f"  输出路径: {output_path}")
    
    # 创建音频（简单的正弦波）
    def make_sound(t):
        return 0.1 * np.sin(440 * 2 * np.pi * t)  # 440Hz正弦波
    
    audio_clip = AudioClip(make_sound, duration=2)
    audio_path = os.path.join(temp_dir, "test_audio.wav")
    audio_clip.write_audiofile(audio_path, fps=44100)
    print(f"✅ 音频文件生成成功: {audio_path}")
    
    # 创建视频并添加音频
    color_clip = ColorClip(size=(320, 240), color=(0, 255, 0), duration=2)
    video_with_audio = color_clip.with_audio(audio_clip)
    
    video_with_audio.write_videofile(
        output_path,
        fps=10,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=1,
        ffmpeg_params=[
            '-pix_fmt', 'yuv420p',
            '-y',
            '-loglevel', 'info'
        ],
        logger='bar'
    )
    
    color_clip.close()
    audio_clip.close()
    
    # 检查文件
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"✅ 带音频视频生成成功！")
        print(f"  文件大小: {file_size:,} 字节 ({file_size/1024:.2f} KB)")
        print(f"  文件路径: {output_path}")
        
        if file_size < 1024:
            print("❌ 警告: 文件大小小于1KB，可能存在问题")
        else:
            print("✅ 文件大小正常")
    else:
        print("❌ 带音频视频生成失败，文件不存在")
except Exception as e:
    print(f"❌ 带音频视频生成失败: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试完成 ===")
print(f"测试结果已保存到临时目录: {temp_dir}")
print(f"测试结束时间: {datetime.datetime.now()}")
