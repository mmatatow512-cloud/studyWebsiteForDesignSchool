import os
import sys
import moviepy

# 检查moviepy版本和路径
print(f"Python版本: {sys.version}")
print(f"moviepy版本: {moviepy.__version__}")
print(f"moviepy路径: {moviepy.__file__}")

# 检查editor.py文件是否存在
moviepy_dir = os.path.dirname(moviepy.__file__)
editor_path = os.path.join(moviepy_dir, 'editor.py')
print(f"\neditor.py路径: {editor_path}")
print(f"editor.py存在: {os.path.exists(editor_path)}")

# 如果存在，查看文件内容
if os.path.exists(editor_path):
    with open(editor_path, 'r') as f:
        content = f.read(500)  # 只读取前500字符
        print(f"\neditor.py前500字符: {content}")

# 尝试导入修改后的组件
print("\n尝试导入修改后的组件:")
try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
    print("✓ 成功导入VideoFileClip")
except Exception as e:
    print(f"✗ 导入VideoFileClip失败: {e}")

try:
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    print("✓ 成功导入AudioFileClip")
except Exception as e:
    print(f"✗ 导入AudioFileClip失败: {e}")

try:
    from moviepy.video.VideoClip import ImageClip
    print("✓ 成功导入ImageClip")
except Exception as e:
    print(f"✗ 导入ImageClip失败: {e}")

try:
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    print("✓ 成功导入CompositeVideoClip")
except Exception as e:
    print(f"✗ 导入CompositeVideoClip失败: {e}")

try:
    from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
    print("✓ 成功导入concatenate_videoclips")
except Exception as e:
    print(f"✗ 导入concatenate_videoclips失败: {e}")

# 尝试导入其他可能需要的组件
try:
    from moviepy.video.VideoClip import TextClip, ColorClip
    print("✓ 成功导入TextClip和ColorClip")
except Exception as e:
    print(f"✗ 导入TextClip和ColorClip失败: {e}")

try:
    from moviepy.audio.AudioClip import AudioClip
    print("✓ 成功导入AudioClip")
except Exception as e:
    print(f"✗ 导入AudioClip失败: {e}")
