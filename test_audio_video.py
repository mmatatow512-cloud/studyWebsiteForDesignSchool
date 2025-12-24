import os
import numpy as np
from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
import tempfile

def test_audio_video():
    print("=== 测试音频视频生成 ===")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    print(f"使用临时目录: {temp_dir}")
    
    try:
        # 生成测试图像（简单的颜色图片）
        image_path = os.path.join(temp_dir, "test_image.jpg")
        print(f"生成测试图像: {image_path}")
        
        # 使用ImageClip创建简单图像
        image_clip = ImageClip(np.zeros((720, 1280, 3), dtype=np.uint8) + 255)  # 白色图像
        image_clip.save_frame(image_path, t=0)
        
        # 生成测试音频（440Hz的正弦波）
        audio_path = os.path.join(temp_dir, "test_audio.wav")
        print(f"生成测试音频: {audio_path}")
        
        duration = 5  # 5秒
        samples = int(duration * 44100)
        t = np.linspace(0, duration, samples)
        audio_array = np.sin(2 * np.pi * 440 * t)  # 440Hz正弦波
        audio_array = np.column_stack((audio_array, audio_array))  # 立体声
        audio_array = audio_array.astype(np.float32)
        
        audio_clip = AudioArrayClip(audio_array, fps=44100)
        audio_clip.write_audiofile(audio_path, fps=44100)
        
        # 验证生成的音频文件
        if os.path.exists(audio_path):
            audio_size = os.path.getsize(audio_path)
            print(f"音频文件大小: {audio_size} 字节")
            if audio_size > 1024:
                print("✓ 音频文件生成成功")
            else:
                print("✗ 音频文件太小，可能无效")
        else:
            print("✗ 音频文件生成失败")
            return False
        
        # 创建视频片段
        print("创建视频片段...")
        img_clip = ImageClip(image_path).with_duration(duration)
        
        # 加载音频并附加到视频
        print("加载音频并附加到视频...")
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        loaded_audio_clip = AudioFileClip(audio_path)
        final_clip = img_clip.with_audio(loaded_audio_clip)
        
        # 验证视频是否有音频
        if hasattr(final_clip, 'audio') and final_clip.audio is not None:
            print("✓ 音频已成功附加到视频")
        else:
            print("✗ 音频未能附加到视频")
            return False
        
        # 生成视频文件
        output_path = os.path.join(temp_dir, "test_output.mp4")
        print(f"生成视频文件: {output_path}")
        
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",  # 明确指定音频编码
            preset="ultrafast",
            ffmpeg_params=[
                '-pix_fmt', 'yuv420p',
                '-b:a', '64k',
                '-y'
            ]
        )
        
        # 验证生成的视频文件
        if os.path.exists(output_path):
            video_size = os.path.getsize(output_path)
            print(f"视频文件大小: {video_size} 字节")
            if video_size > 1024:
                print("✓ 视频文件生成成功")
                
                # 使用ffprobe检查视频信息
                try:
                    import subprocess
                    result = subprocess.run(
                        ['ffprobe', '-v', 'error', '-show_entries', 'format=nb_streams,duration,bit_rate', '-of', 'csv=p=0', output_path],
                        capture_output=True,
                        text=True
                    )
                    print(f"ffprobe信息: {result.stdout.strip()}")
                    
                    # 检查音频流
                    result = subprocess.run(
                        ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', output_path],
                        capture_output=True,
                        text=True
                    )
                    if result.stdout.strip():
                        print(f"✓ 视频包含音频流: {result.stdout.strip()}")
                    else:
                        print("✗ 视频不包含音频流")
                        return False
                except Exception as e:
                    print(f"获取视频信息失败: {e}")
                    # 继续验证其他部分
                    
                return True
            else:
                print("✗ 视频文件太小，可能无效")
                return False
        else:
            print("✗ 视频文件生成失败")
            return False
            
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理临时文件
        print(f"清理临时目录: {temp_dir}")
        import shutil
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    success = test_audio_video()
    if success:
        print("\n✓ 测试完成，音频视频生成正常!")
    else:
        print("\n✗ 测试失败，请检查错误信息!")
