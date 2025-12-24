import os
import sys
import tempfile
import shutil

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# 导入ConverterLogic
from ppt2video import ConverterLogic

class TestLogger:
    def log(self, message):
        print(f"[LOG] {message}")

# 测试generate_audio方法
def test_generate_audio():
    print("=== 测试音频生成功能 ===")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    print(f"创建临时目录: {temp_dir}")
    
    try:
        # 创建ConverterLogic实例，传递日志函数
        def logger_func(message):
            print(f"[LOG] {message}")
        
        converter = ConverterLogic(logger_func)
        
        # 测试文本，包含用户提到的特殊字符
        test_texts = [
            "，，西方艺术风格的五个关键时代，，，• 古典艺术的奠基",
            "西方艺术风格的五个关键时代，• 古典艺术的奠基",
            "空白测试",
            "这是一个很长的测试文本，用于测试文本过长时的截断功能。这是一个很长的测试文本，用于测试文本过长时的截断功能。这是一个很长的测试文本，用于测试文本过长时的截断功能。"
        ]
        
        print(f"测试文本数量: {len(test_texts)}")
        for i, text in enumerate(test_texts):
            print(f"第{i+1}个文本: {text[:50]}...")
        
        # 调用generate_audio方法
        print("\n开始生成音频...")
        audio_paths = converter.generate_audio(test_texts, temp_dir, None, 150)
        
        print(f"\n音频生成结果: 共生成 {len(audio_paths)} 个音频文件")
        
        # 验证生成的音频文件
        for i, audio_path in enumerate(audio_paths):
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path)
                print(f"第{i+1}个音频: {os.path.basename(audio_path)} - 大小: {file_size} 字节 - 成功")
            else:
                print(f"第{i+1}个音频: {os.path.basename(audio_path)} - 失败")
        
        return len(audio_paths) > 0
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)
        print(f"\n清理临时目录: {temp_dir}")

if __name__ == "__main__":
    success = test_generate_audio()
    if success:
        print("\n✅ 测试通过！音频生成功能正常工作。")
        sys.exit(0)
    else:
        print("\n❌ 测试失败！音频生成功能存在问题。")
        sys.exit(1)
