import os
import sys
import tempfile

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ppt2video import convert_presentation_to_video

def test_no_test_video():
    """
    测试是否不再生成测试视频
    """
    print("=== 验证修复：确保不再生成测试视频 ===\n")
    
    # 1. 检查当前目录是否有测试视频文件
    test_video_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.mp4')]
    if test_video_files:
        print(f"发现现有测试视频文件：{test_video_files}")
        print("正在删除...")
        for f in test_video_files:
            os.remove(f)
        print("删除完成\n")
    
    # 2. 使用项目中的测试PPT文件
    test_ppt = os.path.join(os.path.dirname(__file__), 'test_ppt.pptx')
    
    if not os.path.exists(test_ppt):
        print("注意：未找到test_ppt.pptx文件，将创建一个简单的测试")
        # 创建一个简单的测试函数来验证修复
        test_without_ppt()
        return
    
    # 3. 创建临时输出目录
    output_dir = tempfile.mkdtemp()
    output_path = os.path.join(output_dir, 'test_output.mp4')
    
    try:
        print(f"使用测试PPT：{test_ppt}")
        print(f"输出视频：{output_path}")
        
        # 4. 调用转换函数
        result = convert_presentation_to_video(test_ppt, output_path)
        
        print(f"\n转换结果：{'成功' if result else '失败'}")
        
        # 5. 检查是否生成了测试视频
        test_video_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.mp4')]
        if test_video_files:
            print(f"\n❌ 错误：发现生成的测试视频文件：{test_video_files}")
            return False
        else:
            print(f"\n✅ 成功：没有生成测试视频文件")
        
        # 6. 检查生成的视频文件
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"生成的视频大小：{file_size} 字节")
            
            if file_size > 10240:  # 大于10KB
                print(f"✅ 视频文件大小正常")
            else:
                print(f"⚠️  视频文件较小：{file_size} 字节")
        else:
            print(f"❌ 错误：视频文件未生成")
            return False
            
        return True
        
    finally:
        # 清理临时目录
        if os.path.exists(output_dir):
            import shutil
            shutil.rmtree(output_dir)

def test_without_ppt():
    """
    在没有PPT文件的情况下测试
    """
    print("\n=== 测试无PPT文件情况 ===")
    
    # 1. 检查当前目录是否有测试视频文件
    test_video_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.mp4')]
    if test_video_files:
        print(f"删除现有测试视频：{test_video_files}")
        for f in test_video_files:
            os.remove(f)
    
    # 2. 使用不存在的PPT文件
    non_existent_ppt = "non_existent_file.pptx"
    output_path = "test_output_nonexistent.mp4"
    
    try:
        print(f"使用不存在的PPT：{non_existent_ppt}")
        print(f"输出视频：{output_path}")
        
        # 3. 调用转换函数
        result = convert_presentation_to_video(non_existent_ppt, output_path)
        
        print(f"\n转换结果：{'成功' if result else '失败'}")
        
        # 4. 检查是否生成了测试视频
        test_video_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.mp4')]
        if test_video_files:
            print(f"❌ 错误：发现生成的测试视频文件：{test_video_files}")
            return False
        else:
            print(f"✅ 成功：没有生成测试视频文件")
        
        # 5. 检查是否生成了输出视频
        if os.path.exists(output_path):
            print(f"❌ 错误：在PPT文件不存在的情况下生成了视频文件")
            return False
        else:
            print(f"✅ 成功：在PPT文件不存在的情况下没有生成视频文件")
            
        return True
        
    finally:
        # 清理输出文件
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    print("开始验证修复...\n")
    
    # 运行测试
    test1_result = test_no_test_video()
    test2_result = test_without_ppt()
    
    print("\n=== 验证结果汇总 ===")
    print(f"测试1（正常转换）：{'通过' if test1_result else '失败'}")
    print(f"测试2（无PPT情况）：{'通过' if test2_result else '失败'}")
    
    if test1_result and test2_result:
        print("\n🎉 所有测试通过！修复成功！")
    else:
        print("\n❌ 部分测试失败！")