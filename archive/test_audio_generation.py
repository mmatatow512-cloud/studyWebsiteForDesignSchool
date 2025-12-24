import os
import sys
import tempfile
import shutil

# 添加项目路径到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'project')))

# 导入ConverterLogic类
from ppt2video import ConverterLogic

# 简单的日志函数
def simple_log(message):
    print(message)

# 测试音频生成功能
def test_audio_generation():
    print("=== 测试音频生成功能 ===")
    
    # 创建临时目录
    temp_folder = tempfile.mkdtemp()
    print(f"临时目录: {temp_folder}")
    
    try:
        # 创建ConverterLogic实例
        converter = ConverterLogic(simple_log)
        
        # 测试文本
        test_scripts = [
            "测试中文语音生成功能",
            "这是第二页的测试文本内容",
            "PPT转视频工具音频生成测试"
        ]
        
        print(f"\n测试脚本数量: {len(test_scripts)}")
        for i, script in enumerate(test_scripts):
            print(f"  {i+1}. {script}")
        
        # 生成音频
        print("\n开始生成音频...")
        audio_paths = converter.generate_audio(test_scripts, temp_folder, None, 150)
        
        print(f"\n音频生成完成")
        print(f"生成的音频文件数量: {len(audio_paths)}")
        
        if audio_paths:
            print("\n生成的音频文件:")
            for i, audio_path in enumerate(audio_paths):
                if os.path.exists(audio_path):
                    file_size = os.path.getsize(audio_path)
                    print(f"  ✓ {audio_path} - 大小: {file_size/1024:.2f} KB")
                else:
                    print(f"  ✗ {audio_path} - 文件不存在")
        
        return audio_paths
        
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        # 清理临时目录
        print(f"\n清理临时目录: {temp_folder}")
        shutil.rmtree(temp_folder)

# 主函数
if __name__ == "__main__":
    print("=== 音频生成测试工具 ===")
    print(f"Python版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    
    audio_files = test_audio_generation()
    
    if audio_files:
        print("\n✓ 测试成功! 生成了有效的音频文件")
    else:
        print("\n✗ 测试失败! 没有生成有效的音频文件")
    
    print("\n=== 测试完成 ===")
