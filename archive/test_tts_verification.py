import os
import sys
import tempfile
import re

# 测试gTTS是否可用
def test_gtts_available():
    print("=== 测试gTTS是否可用 ===")
    try:
        from gtts import gTTS
        print("✓ gTTS模块已安装")
        return True
    except ImportError as e:
        print(f"✗ gTTS模块未安装: {e}")
        return False

# 测试gTTS生成中文语音
def test_gtts_tts(text="测试中文语音生成功能"):
    print("\n=== 测试gTTS生成中文语音 ===")
    if not test_gtts_available():
        print("无法测试gTTS，模块未安装")
        return False
    
    try:
        from gtts import gTTS
        import subprocess
        
        # 清理文本
        cleaned_text = re.sub(r'[，。、；："\'\n\r]+', '，', text)
        cleaned_text = re.sub(r'[•●■◆]', '', cleaned_text)
        cleaned_text = re.sub(r'[，]+', '，', cleaned_text)
        cleaned_text = re.sub(r'^[，]+|[，]+$', '', cleaned_text)
        
        print(f"使用文本: {cleaned_text}")
        
        # 创建临时文件
        temp_file = tempfile.mktemp(suffix='.mp3')
        wav_file = temp_file.replace('.mp3', '.wav')
        
        print(f"临时文件: {temp_file}")
        print(f"输出文件: {wav_file}")
        
        # 使用gTTS生成语音
        tts = gTTS(text=cleaned_text, lang='zh-cn', slow=False)
        tts.save(temp_file)
        
        print(f"✓ gTTS生成MP3文件成功")
        print(f"  文件大小: {os.path.getsize(temp_file)} 字节")
        
        # 测试转换为WAV
        try:
            subprocess.run(
                ['ffmpeg', '-i', temp_file, '-acodec', 'pcm_s16le', '-ar', '44100', wav_file],
                check=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
            print(f"✓ 成功转换为WAV格式")
            print(f"  WAV文件大小: {os.path.getsize(wav_file)} 字节")
        except Exception as e:
            print(f"✗ 转换为WAV失败: {e}")
            try:
                # 尝试使用moviepy转换
                from moviepy.editor import AudioFileClip
                audio = AudioFileClip(temp_file)
                audio.write_audiofile(wav_file, codec='pcm_s16le')
                audio.close()
                print(f"✓ 使用moviepy成功转换为WAV格式")
                print(f"  WAV文件大小: {os.path.getsize(wav_file)} 字节")
            except Exception as e2:
                print(f"✗ 使用moviepy转换为WAV也失败: {e2}")
                # 直接使用MP3文件
                os.rename(temp_file, wav_file.replace('.wav', '.mp3'))
                print(f"✓ 使用MP3文件作为替代")
        
        # 清理文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        if os.path.exists(wav_file):
            os.unlink(wav_file)
        
        return True
    except Exception as e:
        print(f"✗ gTTS生成语音失败: {e}")
        import traceback
        traceback.print_exc()
        return False

# 测试pyttsx3
def test_pyttsx3_tts(text="测试中文语音生成功能"):
    print("\n=== 测试pyttsx3生成中文语音 ===")
    try:
        import pyttsx3
        print("✓ pyttsx3模块已安装")
        
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        print(f"\n可用语音列表 ({len(voices)}个):")
        chinese_voices = []
        for i, voice in enumerate(voices):
            voice_id_lower = voice.id.lower()
            voice_name_lower = voice.name.lower()
            is_chinese = any(keyword in voice_id_lower or keyword in voice_name_lower 
                           for keyword in ['chinese', 'zh', 'mandarin', '中文', '普通话', 'cantonese', 'yue'])
            
            print(f"{i+1}. {voice.name} ({voice.id}) - 中文: {is_chinese}")
            if is_chinese:
                chinese_voices.append(voice)
        
        if chinese_voices:
            print(f"\n找到{len(chinese_voices)}个中文语音包:")
            for voice in chinese_voices:
                print(f"  - {voice.name} ({voice.id})")
        else:
            print("\n未找到中文语音包")
        
        # 测试生成语音
        temp_file = tempfile.mktemp(suffix='.wav')
        print(f"\n测试生成语音到: {temp_file}")
        
        # 设置中文语音（如果有）
        if chinese_voices:
            engine.setProperty('voice', chinese_voices[0].id)
            print(f"使用中文语音: {chinese_voices[0].name}")
        else:
            print("使用默认语音")
        
        engine.setProperty('rate', 150)
        engine.save_to_file(text, temp_file)
        engine.runAndWait()
        
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 1024:
            print(f"✓ 语音生成成功")
            print(f"  文件大小: {os.path.getsize(temp_file)} 字节")
            os.unlink(temp_file)
            return True
        else:
            print(f"✗ 语音生成失败或文件太小")
            if os.path.exists(temp_file):
                print(f"  文件大小: {os.path.getsize(temp_file)} 字节")
                os.unlink(temp_file)
            return False
            
    except Exception as e:
        print(f"✗ pyttsx3测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

# 测试文本清理功能
def test_text_cleaning():
    print("\n=== 测试文本清理功能 ===")
    original_text = "测试文本•包含特殊符号◆和
换行符，以及中文标点；：'""
    print(f"原始文本: {repr(original_text)}")
    
    # 使用与ppt2video.py相同的清理逻辑
    cleaned_text = re.sub(r'[，。、；："\'\n\r]+', '，', original_text)
    cleaned_text = re.sub(r'[•●■◆]', '', cleaned_text)
    cleaned_text = re.sub(r'[，]+', '，', cleaned_text)
    cleaned_text = re.sub(r'^[，]+|[，]+$', '', cleaned_text)
    
    print(f"清理后: {repr(cleaned_text)}")
    return cleaned_text

# 主测试函数
def main():
    print("=== TTS验证测试工具 ===")
    print(f"Python版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    
    # 测试文本清理
    test_text_cleaning()
    
    # 测试gTTS
    test_gtts_tts()
    
    # 测试pyttsx3
    test_pyttsx3_tts()
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()
