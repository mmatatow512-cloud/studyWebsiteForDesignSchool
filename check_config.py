import moviepy.config

# 查看config模块的内容
print(dir(moviepy.config))
print()

# 查看config模块的文档
print(moviepy.config.__doc__)
print()

# 尝试查看具体的配置方法
print("尝试获取FFMPEG路径:")
try:
    print(f"FFMPEG路径: {moviepy.config.FFMPEG_BINARY}")
except Exception as e:
    print(f"错误: {e}")

print()
print("尝试获取IMAGEMAGICK路径:")
try:
    print(f"IMAGEMAGICK路径: {moviepy.config.IMAGEMAGICK_BINARY}")
except Exception as e:
    print(f"错误: {e}")

# 查看config模块的源代码
print()
print("查看config模块的源代码:")
import inspect
print(inspect.getsource(moviepy.config))