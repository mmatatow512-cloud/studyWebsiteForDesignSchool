import os
import sys
import tempfile
import shutil

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ppt2video import convert_presentation_to_video

def test_convert():
    # 使用项目中的测试PPT文件
    test_ppt = os.path.join(os.path.dirname(__file__), 'test_ppt.pptx')
    
    # 确保测试PPT存在
    if not os.path.exists(test_ppt):
        print(f"错误：测试PPT文件不存在：{test_ppt}")
        print("请确保在项目目录中有一个名为'test_ppt.pptx'的PPT文件")
        return False
    
    print(f"使用测试PPT：{test_ppt}")
    print(f"PPT文件大小：{os.path.getsize(test_ppt)} 字节")
    
    # 创建临时输出目录
    output_dir = tempfile.mkdtemp()
    output_path = os.path.join(output_dir, 'test_output.mp4')
    
    try:
        print(f"\n开始转换...")
        print(f"输出视频路径：{output_path}")
        
        # 调用转换函数
        result = convert_presentation_to_video(test_ppt, output_path)
        
        print(f"\n转换结果：{result}")
        
        # 检查输出文件
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"生成的视频文件大小：{file_size} 字节")
            
            # 检查是否有测试视频生成
            test_video_path = "test_simple.mp4"
            if os.path.exists(test_video_path):
                test_size = os.path.getsize(test_video_path)
                print(f"警告：发现测试视频文件：{test_video_path}")
                print(f"测试视频大小：{test_size} 字节")
                print(f"测试视频与生成视频大小是否相同：{file_size == test_size}")
                
                # 删除测试视频
                os.remove(test_video_path)
                print("已删除测试视频")
            
            # 检查是否存在其他可能的测试视频
            for f in os.listdir('.'):
                if f.endswith('.mp4') and f != os.path.basename(output_path):
                    print(f"警告：发现其他视频文件：{f}")
                    print(f"大小：{os.path.getsize(f)} 字节")
                    
            return True
        else:
            print(f"错误：视频文件未生成")
            return False
            
    finally:
        # 清理临时目录
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        print(f"\n清理完成")

if __name__ == "__main__":
    test_convert()