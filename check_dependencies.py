import sys
print('Python版本:', sys.version)

try:
    import os
    print('os模块导入成功')
except ImportError as e:
    print('os模块导入失败:', e)

try:
    import numpy
    print('NumPy版本:', numpy.__version__)
except ImportError as e:
    print('NumPy导入失败:', e)

try:
    from PIL import Image
    print('PIL/Pillow版本:', Image.__version__)
except ImportError as e:
    print('PIL/Pillow导入失败:', e)

try:
    import pyttsx3
    # pyttsx3没有__version__属性，直接打印导入成功
    print('pyttsx3导入成功')
except ImportError as e:
    print('pyttsx3导入失败:', e)

try:
    import moviepy
    print('MoviePy版本:', moviepy.__version__)
    # 检查MoviePy内部模块
    try:
        from moviepy.video.VideoClip import ImageClip
        print('ImageClip导入成功')
    except ImportError as e:
        print('ImageClip导入失败:', e)
    
    try:
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        print('AudioFileClip导入成功')
    except ImportError as e:
        print('AudioFileClip导入失败:', e)
    
    try:
        from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
        print('concatenate_videoclips导入成功')
    except ImportError as e:
        print('concatenate_videoclips导入失败:', e)
        
    # 检查FFmpeg配置
    try:
        from moviepy.config import FFMPEG_BINARY
        print('FFMPEG_BINARY:', FFMPEG_BINARY)
    except ImportError as e:
        print('FFmpeg配置检查失败:', e)
        
except ImportError as e:
    print('MoviePy导入失败:', e)
    import traceback
    traceback.print_exc()