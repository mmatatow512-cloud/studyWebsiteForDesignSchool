#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频生成和视频编码测试脚本
用于诊断视频没有声音的问题
"""

import os
import sys
import tempfile
import datetime
import numpy as np
import pyttsx3

# 确保我们在正确的目录中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# 导入所需的MoviePy组件
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from moviepy.audio.AudioClip import AudioArrayClip

def test_audio_generation():
    """测试音频生成功能"""
    print("=== 音频生成测试 ===")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"临时目录: {temp_dir}")
        
        # 测试文本
        test_texts = ["这是第一页的测试文本", "这是第二页的测试文本，用于验证音频生成功能"]
        
        # 测试TTS音频生成
        print("\n1. 测试TTS音频生成:")
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            
            # 获取可用语音
            voices = engine.getProperty('voices')
            print(f"   可用语音数量: {len(voices)}")
            for i, voice in enumerate(voices):
                print(f"   语音{i}: {voice.name} - {voice.id}")
                if 'chinese' in voice.id.lower() or 'mandarin' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    print(f"   选择了中文语音: {voice.name}")
                    break
            
            for i, text in enumerate(test_texts):
                audio_path = os.path.join(temp_dir, f"tts_audio_{i+1}.wav")
                print(f"   生成TTS音频 {i+1}: {text[:20]}...")
                
                engine.save_to_file(text, audio_path)
                engine.runAndWait()
                
                if os.path.exists(audio_path):
                    size = os.path.getsize(audio_path)
                    print(f"   ✓ 音频文件生成成功: {os.path.basename(audio_path)}, 大小: {size} 字节")
                    
                    # 验证音频文件是否可读取
                    try:
                        audio_clip = AudioFileClip(audio_path)
                        print(f"   ✓ 音频文件可读取，时长: {audio_clip.duration:.2f} 秒")
                        audio_clip.close()
                    except Exception as e:
                        print(f"   ✗ 音频文件读取失败: {e}")
                else:
                    print(f"   ✗ 音频文件生成失败")
            
            engine.stop()
        except Exception as e:
            print(f"   ✗ TTS音频生成失败: {e}")
        
        # 测试降级方案（正弦波音频）
        print("\n2. 测试降级方案（正弦波音频）:")
        try:
            for i, text in enumerate(test_texts):
                audio_path = os.path.join(temp_dir, f"sine_audio_{i+1}.wav")
                print(f"   生成正弦波音频 {i+1}")
                
                estimated_duration = max(2.0, len(text) * 0.33)
                samples = int(estimated_duration * 44100)
                t = np.linspace(0, estimated_duration, samples)
                audio_array = np.sin(2 * np.pi * 440 * t)
                audio_array = np.column_stack((audio_array, audio_array)).astype(np.float32)
                
                audio_clip = AudioArrayClip(audio_array, fps=44100)
                audio_clip.write_audiofile(audio_path, fps=44100)
                
                if os.path.exists(audio_path):
                    size = os.path.getsize(audio_path)
                    print(f"   ✓ 正弦波音频生成成功: {os.path.basename(audio_path)}, 大小: {size} 字节")
                    
                    # 验证音频文件是否可读取
                    try:
                        audio_clip = AudioFileClip(audio_path)
                        print(f"   ✓ 音频文件可读取，时长: {audio_clip.duration:.2f} 秒")
                        audio_clip.close()
                    except Exception as e:
                        print(f"   ✗ 音频文件读取失败: {e}")
                else:
                    print(f"   ✗ 正弦波音频生成失败")
        except Exception as e:
            print(f"   ✗ 正弦波音频生成失败: {e}")

def test_video_encoding():
    """测试视频编码功能，重点验证音频是否被正确编码"""
    print("\n=== 视频编码测试 ===")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"临时目录: {temp_dir}")
        
        # 创建测试图片
        print("\n1. 创建测试图片:")
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            for i in range(2):
                img_path = os.path.join(temp_dir, f"test_image_{i+1}.jpg")
                img = Image.new('RGB', (800, 600), color=(255, 255, 255))
                d = ImageDraw.Draw(img)
                font = ImageFont.truetype("arial", 30) if sys.platform == 'win32' else ImageFont.load_default()
                d.text((100, 250), f"测试页面 {i+1}", fill=(0, 0, 0), font=font)
                img.save(img_path)
                
                if os.path.exists(img_path):
                    size = os.path.getsize(img_path)
                    print(f"   ✓ 测试图片 {i+1} 生成成功: {os.path.basename(img_path)}, 大小: {size} 字节")
                else:
                    print(f"   ✗ 测试图片 {i+1} 生成失败")
        except Exception as e:
            print(f"   ✗ 测试图片生成失败: {e}")
            return
        
        # 生成测试音频
        print("\n2. 生成测试音频:")
        try:
            test_texts = ["这是第一页的测试文本", "这是第二页的测试文本"]
            
            for i, text in enumerate(test_texts):
                audio_path = os.path.join(temp_dir, f"test_audio_{i+1}.wav")
                estimated_duration = max(2.0, len(text) * 0.33)
                samples = int(estimated_duration * 44100)
                t = np.linspace(0, estimated_duration, samples)
                audio_array = np.sin(2 * np.pi * 440 * t)
                audio_array = np.column_stack((audio_array, audio_array)).astype(np.float32)
                
                audio_clip = AudioArrayClip(audio_array, fps=44100)
                audio_clip.write_audiofile(audio_path, fps=44100)
                
                if os.path.exists(audio_path):
                    size = os.path.getsize(audio_path)
                    print(f"   ✓ 测试音频 {i+1} 生成成功: {os.path.basename(audio_path)}, 大小: {size} 字节")
                else:
                    print(f"   ✗ 测试音频 {i+1} 生成失败")
        except Exception as e:
            print(f"   ✗ 测试音频生成失败: {e}")
            return
        
        # 生成视频
        print("\n3. 测试视频编码（包含音频）:")
        try:
            # 加载图片和音频
            image_paths = [os.path.join(temp_dir, f"test_image_{i+1}.jpg") for i in range(2)]
            audio_paths = [os.path.join(temp_dir, f"test_audio_{i+1}.wav") for i in range(2)]
            
            clips = []
            for img_path, aud_path in zip(image_paths, audio_paths):
                # 加载图片
                img_clip = ImageClip(img_path)
                
                # 加载音频
                audio_clip = AudioFileClip(aud_path)
                duration = audio_clip.duration + 0.5
                
                # 设置图片时长并添加音频
                img_clip = img_clip.with_duration(duration)
                final_clip = img_clip.with_audio(audio_clip)
                
                clips.append(final_clip)
            
            # 合并视频片段
            final_video = concatenate_videoclips(clips, method="compose")
            
            # 检查final_video是否有音频
            print(f"   合并后的视频是否有音频: {hasattr(final_video, 'audio') and final_video.audio is not None}")
            if hasattr(final_video, 'audio') and final_video.audio:
                print(f"   音频时长: {final_video.audio.duration:.2f} 秒")
            
            # 编码视频
            video_path = os.path.join(temp_dir, "test_video_with_audio.mp4")
            print(f"   开始编码视频: {os.path.basename(video_path)}")
            
            # 使用明确的音频编码参数
            final_video.write_videofile(
                video_path,
                fps=8,
                codec="libx264",
                audio_codec="aac",  # 明确指定音频编码，不使用条件判断
                preset="ultrafast",
                threads=1,
                ffmpeg_params=[
                    '-pix_fmt', 'yuv420p',
                    '-b:a', '64k',
                    '-b:v', '300k',
                    '-y',
                    '-loglevel', 'warning'
                ]
            )
            
            if os.path.exists(video_path):
                size = os.path.getsize(video_path)
                print(f"   ✓ 视频编码成功: {os.path.basename(video_path)}, 大小: {size} 字节")
                
                # 验证生成的视频是否包含音频
                print("\n4. 验证视频中的音频:")
                try:
                    video_clip = VideoFileClip(video_path)
                    print(f"   视频时长: {video_clip.duration:.2f} 秒")
                    print(f"   视频是否有音频: {hasattr(video_clip, 'audio') and video_clip.audio is not None}")
                    
                    if hasattr(video_clip, 'audio') and video_clip.audio:
                        print(f"   ✓ 视频包含音频流，音频时长: {video_clip.audio.duration:.2f} 秒")
                    else:
                        print(f"   ✗ 视频不包含音频流")
                    
                    video_clip.close()
                except Exception as e:
                    print(f"   ✗ 无法读取生成的视频: {e}")
            else:
                print(f"   ✗ 视频编码失败")
            
            # 清理资源
            final_video.close()
            for clip in clips:
                clip.close()
                
        except Exception as e:
            print(f"   ✗ 视频编码失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print(f"音频视频测试脚本启动时间: {datetime.datetime.now()}")
    print(f"Python版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 先安装必要的依赖
    print("\n=== 检查并安装依赖 ===")
    try:
        import pyttsx3
        print("✓ pyttsx3 已安装")
    except ImportError:
        print("安装 pyttsx3...")
        os.system(f"{sys.executable} -m pip install pyttsx3")
    
    try:
        from PIL import Image
        print("✓ Pillow 已安装")
    except ImportError:
        print("安装 Pillow...")
        os.system(f"{sys.executable} -m pip install Pillow")
    
    test_audio_generation()
    test_video_encoding()
    
    print("\n=== 测试完成 ===")
