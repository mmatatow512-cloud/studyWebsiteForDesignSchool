import os
import sys
import tempfile
from PIL import Image
import numpy as np

# 确保直接导入MoviePy的必要组件
try:
    from moviepy.video.VideoClip import ImageClip
    from moviepy.audio.AudioClip import AudioClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
    print("✅ MoviePy组件导入成功")
except ImportError as e:
    print("❌ MoviePy组件导入失败:", e)
    sys.exit(1)

# 创建测试用的图片和音频文件
def create_test_files():
    temp_dir = tempfile.mkdtemp()
    print(f"创建测试文件目录: {temp_dir}")
    
    # 创建两张简单的图片
    images = []
    for i in range(2):
        img_path = os.path.join(temp_dir, f"test_{i+1}.png")
        # 创建一个红色背景的图片
        img = Image.new('RGB', (1280, 720), color='red')
        # 在图片上添加白色文字
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default(size=48)
        draw.text((640, 360), f"Slide {i+1}", fill='white', anchor='mm')
        img.save(img_path)
        images.append(img_path)
        print(f"  创建图片: {img_path}")
    
    # 创建简单的音频文件
    audios = []
    for i in range(2):
        audio_path = os.path.join(temp_dir, f"test_{i+1}.wav")
        # 创建一个简单的正弦波音频
        def make_sound(t):
            return 0.1 * np.sin(440 * 2 * np.pi * t)
        
        audio_clip = AudioClip(make_sound, duration=2)
        audio_clip.write_audiofile(audio_path, fps=44100)
        audios.append(audio_path)
        print(f"  创建音频: {audio_path}")
    
    return temp_dir, images, audios

# 测试视频合成功能
def test_video_synthesis():
    print("\n=== 开始测试视频合成功能 ===")
    
    # 创建测试文件
    temp_dir, images, audios = create_test_files()
    
    try:
        output_video = os.path.join(temp_dir, "output_test.mp4")
        print(f"\n输出视频路径: {output_video}")
        
        # 创建视频片段
        clips = []
        for i, (img_path, audio_path) in enumerate(zip(images, audios)):
            print(f"\n处理片段 {i+1}:")
            print(f"  图片: {img_path}, 大小: {os.path.getsize(img_path)} 字节")
            print(f"  音频: {audio_path}, 大小: {os.path.getsize(audio_path)} 字节")
            
            # 加载图片和音频
            img_clip = ImageClip(img_path).with_duration(2.5)  # 2.5秒/张
            audio_clip = AudioFileClip(audio_path)
            
            # 组合图片和音频
            clip = img_clip.with_audio(audio_clip)
            clips.append(clip)
            print(f"  ✅ 片段 {i+1} 创建成功")
        
        if not clips:
            print("❌ 没有创建任何视频片段")
            return False
        
        # 合并视频片段
        print(f"\n合并 {len(clips)} 个片段...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # 生成视频文件
        print("编码视频文件...")
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
            print(f"\n✅ 视频生成成功！")
            print(f"   文件路径: {output_video}")
            print(f"   文件大小: {file_size} 字节 ({file_size / 1024:.2f} KB)")
            
            if file_size > 1024:  # 大于1KB才是有效的视频文件
                print("   ✅ 视频文件大小正常")
                return True
            else:
                print("   ❌ 视频文件太小 (1KB)，生成失败")
                return False
        else:
            print(f"\n❌ 视频文件生成失败，文件不存在")
            return False
            
    except Exception as e:
        print(f"\n❌ 视频合成过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理临时文件
        # shutil.rmtree(temp_dir)  # 注释掉以便检查生成的文件
        print(f"\n临时文件目录: {temp_dir} (未清理，可手动检查)")

# 执行测试
if __name__ == "__main__":
    print("Python版本:", sys.version)
    success = test_video_synthesis()
    sys.exit(0 if success else 1)