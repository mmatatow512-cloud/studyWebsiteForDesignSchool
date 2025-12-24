import os
import sys
import tempfile
import numpy as np
from PIL import Image
import time

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 直接导入所需的组件
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip, concatenate_videoclips
from moviepy.video.VideoClip import TextClip, ColorClip
from moviepy.audio.AudioClip import AudioClip

# 简单的日志函数
def simple_log(message):
    print(f"[视频合成测试] {message}")

def test_video_synthesis():
    """测试视频合成核心功能"""
    simple_log("开始测试视频合成功能...")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        simple_log(f"创建临时目录：{temp_dir}")
        
        # 1. 创建测试图片
        images = []
        for i in range(3):  # 创建3张测试图片
            img_path = os.path.join(temp_dir, f"test_img_{i+1}.png")
            # 创建纯色图片
            img = Image.new('RGB', (1920, 1080), color=(i*80, 255-i*80, 0))
            img.save(img_path)
            images.append(img_path)
            simple_log(f"创建测试图片：{img_path}")
        
        # 2. 创建测试音频
        audios = []
        for i in range(3):  # 创建3个测试音频
            audio_path = os.path.join(temp_dir, f"test_audio_{i+1}.wav")
            # 使用moviepy创建简单的正弦波音频
            import numpy as np
            
            duration = 2  # 2秒音频
            def make_sound(t):
                return 0.5 * np.sin(2 * np.pi * 440 * t)  # 440Hz正弦波
            
            audio_clip = AudioClip(make_sound, duration=duration)
            audio_clip.write_audiofile(audio_path, fps=44100)
            audios.append(audio_path)
            simple_log(f"创建测试音频：{audio_path}")
        
        # 3. 测试视频合成
        output_video = os.path.join(temp_dir, "test_synthesis.mp4")
        
        try:
            simple_log("开始合成视频...")
            clips = []
            
            for i, (img_path, audio_path) in enumerate(zip(images, audios)):
                simple_log(f"处理第 {i+1} 个片段...")
                
                # 加载音频
                audio_clip = AudioFileClip(audio_path)
                duration = audio_clip.duration
                
                # 加载图片
                img_clip = ImageClip(img_path).set_duration(duration)
                
                # 组合音视频
                final_clip = img_clip.set_audio(audio_clip)
                clips.append(final_clip)
            
            simple_log(f"合并 {len(clips)} 个片段...")
            final_video = concatenate_videoclips(clips, method="compose")
            
            simple_log("开始编码视频...")
            final_video.write_videofile(
                output_video,
                fps=24,
                codec="libx264",
                audio_codec="aac",
                preset="medium",
                threads=4,
                ffmpeg_params=[
                    '-pix_fmt', 'yuv420p',
                    '-b:a', '128k',
                    '-b:v', '2000k'
                ],
                logger=None
            )
            
            # 验证输出文件
            if os.path.exists(output_video):
                file_size = os.path.getsize(output_video)
                simple_log(f"✓ 视频合成成功！")
                simple_log(f"视频文件大小：{file_size} 字节 ({file_size / 1024:.2f} KB)")
                
                if file_size > 10240:  # 大于10KB才视为有效
                    simple_log("✓ 视频文件有效")
                    # 复制到当前目录方便查看
                    dest_path = os.path.join(os.getcwd(), "synthesis_test_result.mp4")
                    import shutil
                    shutil.copy2(output_video, dest_path)
                    simple_log(f"✓ 视频已复制到：{dest_path}")
                    return True
                else:
                    simple_log(f"✗ 视频文件太小：{file_size} 字节")
                    return False
            else:
                simple_log("✗ 视频文件不存在")
                return False
                
        except Exception as e:
            simple_log(f"✗ 视频合成失败：{e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    simple_log("启动视频合成核心功能测试...")
    success = test_video_synthesis()
    
    if success:
        simple_log("✓ 所有测试通过！")
    else:
        simple_log("✗ 测试失败！")
    
    sys.exit(0 if success else 1)