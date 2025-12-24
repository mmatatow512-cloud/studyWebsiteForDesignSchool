# 极简音频生成测试脚本
import os
import sys
import tempfile
import pyttsx3

# 定义详细的日志函数
def log(message):
    print(f"[LOG] {message}")
    # 同时写入日志文件
    with open("audio_test_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{message}\n")

# 清理旧的日志文件
if os.path.exists("audio_test_log.txt"):
    os.remove("audio_test_log.txt")

log("=== 开始极简音频生成测试 ===")
log(f"Python版本: {sys.version}")
log(f"当前工作目录: {os.getcwd()}")

# 测试pyttsx3基本功能
try:
    log("正在初始化pyttsx3引擎...")
    engine = pyttsx3.init()
    log("pyttsx3引擎初始化成功")
    
    # 获取可用语音
    log("正在获取可用语音...")
    voices = engine.getProperty('voices')
    log(f"找到 {len(voices)} 个可用语音")
    
    for i, voice in enumerate(voices):
        log(f"语音 {i+1}: 名称={voice.name}, ID={voice.id}, 语言={voice.languages}")
    
    # 尝试找到中文语音
    chinese_voice = None
    for voice in voices:
        if any(keyword in voice.id.lower() for keyword in ['chinese', 'mandarin', 'zh']):
            chinese_voice = voice
            break
    
    if chinese_voice:
        log(f"选择中文语音: {chinese_voice.name} (ID: {chinese_voice.id})")
        engine.setProperty('voice', chinese_voice.id)
    else:
        log(f"未找到中文语音，使用默认语音: {voices[0].name}")
        engine.setProperty('voice', voices[0].id)
    
    # 设置语速
    engine.setProperty('rate', 170)
    log(f"设置语速为: 170")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    log(f"创建临时目录: {temp_dir}")
    
    # 测试音频文件路径
    audio_path = os.path.join(temp_dir, "test_audio.wav")
    log(f"音频输出路径: {audio_path}")
    
    # 生成音频
    log("正在生成音频...")
    engine.save_to_file("这是测试音频，用于验证TTS功能是否正常工作。", audio_path)
    engine.runAndWait()
    log("音频生成完成")
    
    # 验证音频文件
    if os.path.exists(audio_path):
        file_size = os.path.getsize(audio_path)
        log(f"音频文件存在，大小: {file_size} 字节")
        
        if file_size > 1024:
            log(f"音频文件大小正常")
        else:
            log(f"[警告] 音频文件太小")
    else:
        log(f"[错误] 音频文件不存在")
    
    # 清理
    engine.stop()
    log("关闭pyttsx3引擎")
    
    log("=== 测试完成 ===")
    
except Exception as e:
    log(f"[严重错误] 测试失败: {e}")
    import traceback
    error_details = traceback.format_exc()
    log(f"错误详情: {error_details}")
    
    # 将错误信息写入文件
    with open("audio_test_error.txt", "w", encoding="utf-8") as f:
        f.write(f"错误: {e}\n")
        f.write(f"堆栈跟踪: {error_details}\n")
    
    log("错误详情已写入 audio_test_error.txt")
