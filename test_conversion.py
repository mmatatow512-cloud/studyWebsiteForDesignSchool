import os
import sys
import tempfile
import shutil

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ppt2video

# 简单的日志函数
def simple_log(message):
    print(f"[测试] {message}")

def test_conversion():
    # 创建一个简单的测试PPT文件
    simple_log("正在创建测试PPT...")
    
    # 为了简化测试，我们使用一个已存在的PPT文件（如果有的话）
    # 或者创建一个新的简单PPT
    
    # 找一个测试PPT文件
    test_ppt_path = None
    
    # 检查当前目录是否有PPT文件
    for file in os.listdir('.'):
        if file.endswith(('.pptx', '.ppt')):
            test_ppt_path = file
            break
    
    if not test_ppt_path:
        simple_log("错误：当前目录没有找到PPT文件，请放入一个测试PPT文件后再运行测试")
        return False
    
    simple_log(f"找到测试PPT文件：{test_ppt_path}")
    simple_log(f"PPT文件大小：{os.path.getsize(test_ppt_path)} 字节")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        simple_log(f"创建临时目录：{temp_dir}")
        
        # 定义输出视频路径
        output_video = os.path.join(temp_dir, "test_output.mp4")
        
        try:
            # 调用转换函数
            simple_log("开始转换PPT到视频...")
            success = ppt2video.convert_presentation_to_video(test_ppt_path, output_video, rate=170)
            
            simple_log(f"转换结果：{success}")
            
            if success:
                # 检查视频文件
                if os.path.exists(output_video):
                    file_size = os.path.getsize(output_video)
                    simple_log(f"视频文件生成成功！")
                    simple_log(f"视频文件路径：{output_video}")
                    simple_log(f"视频文件大小：{file_size} 字节 ({file_size / 1024:.2f} KB)")
                    
                    if file_size > 10240:  # 大于10KB才视为有效
                        simple_log("✓ 测试成功：视频文件有效")
                        # 复制视频文件到当前目录，方便检查
                        dest_path = os.path.join(os.getcwd(), "test_result.mp4")
                        shutil.copy2(output_video, dest_path)
                        simple_log(f"✓ 视频文件已复制到：{dest_path}")
                        return True
                    else:
                        simple_log(f"✗ 测试失败：视频文件太小 ({file_size} 字节)")
                        return False
                else:
                    simple_log("✗ 测试失败：视频文件不存在")
                    return False
            else:
                simple_log("✗ 测试失败：转换函数返回失败")
                return False
                
        except Exception as e:
            simple_log(f"✗ 测试失败：发生异常：{e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    simple_log("开始PPT转视频功能测试...")
    success = test_conversion()
    
    if success:
        simple_log("✓ 所有测试通过！")
    else:
        simple_log("✗ 测试失败！")
    
    sys.exit(0 if success else 1)