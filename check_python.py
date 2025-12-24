# 检查Python版本和基本功能
import sys

def main():
    print("Python版本:", sys.version)
    print("Python解释器路径:", sys.executable)
    print("sys模块可用")
    
    # 尝试导入numpy和moviepy
    try:
        import numpy
        print("numpy模块可用，版本:", numpy.__version__)
    except ImportError:
        print("numpy模块不可用")
        
    try:
        # 检查moviepy模块
        import moviepy
        print("moviepy模块可用")
        
        # 检查具体的moviepy组件
        try:
            from moviepy.video.VideoClip import ImageClip
            print("ImageClip可用")
        except ImportError:
            print("ImageClip不可用")
            
        try:
            from moviepy.audio.AudioClip import AudioFileClip
            print("AudioFileClip可用")
        except ImportError:
            print("AudioFileClip不可用")
            
        try:
            from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
            print("concatenate_videoclips可用")
        except ImportError:
            print("concatenate_videoclips不可用")
            
    except ImportError:
        print("moviepy模块不可用")

if __name__ == "__main__":
    print("=== Python环境检查开始 ===")
    main()
    print("=== Python环境检查结束 ===")
