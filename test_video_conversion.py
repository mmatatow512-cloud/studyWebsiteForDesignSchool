import sys
import os
import tempfile
import ppt2video

# 创建一个简单的测试PPT文件路径
# 这里需要用户提供一个测试用的PPT文件
if len(sys.argv) < 2:
    print("请提供一个测试用的PPT文件路径")
    print(f"用法: python {sys.argv[0]} test_ppt.pptx")
    sys.exit(1)

ppt_path = sys.argv[1]
if not os.path.exists(ppt_path):
    print(f"PPT文件不存在: {ppt_path}")
    sys.exit(1)

# 创建临时输出路径
output_path = os.path.join(tempfile.gettempdir(), "test_output.mp4")

print(f"开始测试视频转换: {ppt_path} -> {output_path}")

try:
    result = ppt2video.convert_presentation_to_video(ppt_path, output_path, rate=170)
    if result:
        print(f"视频转换成功！输出文件: {output_path}")
        print(f"文件大小: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
    else:
        print("视频转换失败")
except Exception as e:
    print(f"转换过程中发生错误: {e}")
    import traceback
    traceback.print_exc()
