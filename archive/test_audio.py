import sys
import os

# 添加项目目录到Python路径
sys.path.append(os.path.abspath('project'))

from ppt2video import ConverterLogic
import tempfile
import shutil

def test_audio_generation():
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 简单的日志函数
        def simple_log(message):
            print(f"[LOG] {message}")
        
        # 创建ConverterLogic实例
        converter = ConverterLogic(logger_func=simple_log)
        
        # 测试脚本 - 包含之前导致卡住的问题文本
        test_scripts = [
            "，，西方艺术风格的五个关键时代，，，• 古典艺术的奠基...",
            "这是一个正常的测试文本。",
            "••• 测试特殊符号的处理 •••",
            "测试非常长的文本，这是一个非常长的测试文本，目的是测试文本长度限制功能是否正常工作，应该会被截断到100字符以内..."
        ]
        
        print("开始测试音频生成...")
        print(f"测试脚本数量: {len(test_scripts)}")
        
        # 测试音频生成
        audio_paths = converter.generate_audio(
            scripts=test_scripts,
            temp_folder=temp_dir,
            voice_id=None,
            rate=150
        )
        
        print(f"音频生成完成，生成了 {len(audio_paths)} 个音频文件")
        
        # 验证音频文件
        for i, audio_path in enumerate(audio_paths):
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path)
                print(f"第 {i+1} 个音频文件: {audio_path}，大小: {file_size} 字节")
                if file_size > 1024:
                    print("✓ 音频文件有效")
                else:
                    print("✗ 音频文件太小")
            else:
                print(f"✗ 第 {i+1} 个音频文件未生成: {audio_path}")
        
        return len(audio_paths) == len(test_scripts)
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)
        print("临时目录已清理")

if __name__ == "__main__":
    success = test_audio_generation()
    if success:
        print("\n🎉 音频生成测试成功！")
        sys.exit(0)
    else:
        print("\n❌ 音频生成测试失败！")
        sys.exit(1)
