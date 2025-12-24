#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试TTS子进程执行问题
"""

import os
import sys
import json
import tempfile
import subprocess

def test_tts_subprocess():
    """测试TTS子进程执行"""
    print("=== 调试TTS子进程执行 ===")
    print(f"Python版本: {sys.version}")
    print(f"Python解释器: {sys.executable}")
    
    # 创建临时音频文件路径
    temp_audio = tempfile.mktemp(suffix=".wav", prefix="test_tts_")
    
    # 测试文本
    test_text = "，，西方艺术风格的五个关键时代，，，• 古典艺术的奠基..."
    
    # 创建完整的脚本模板
    script_template = """
import pyttsx3
import os
import sys
import json
import threading
import re
import time

# 获取参数
text = {text}
filename = {filename}
rate = {rate}

result = {result_init}

# 进一步清理文本，移除过多的标点和省略号
cleaned_text = text
# 移除重复的标点符号
cleaned_text = re.sub(r'[，。、；：\\"\\'\\n\\r]+', '，', cleaned_text)
# 移除重复的顿号
cleaned_text = re.sub(r'[，]+', '，', cleaned_text)
# 移除省略号
cleaned_text = re.sub(r'[.]+', '', cleaned_text)
# 移除特殊符号
cleaned_text = re.sub(r'[•●■◆]', '', cleaned_text)
# 限制文本长度
if len(cleaned_text) > 100:
    cleaned_text = cleaned_text[:100] + "..."

if not cleaned_text.strip():
    cleaned_text = "空白幻灯片"

# 子进程内部的超时处理
class TimeoutError(Exception):
    pass

# 超时处理函数
timeout_occurred = False
def timeout_handler():
    global timeout_occurred
    timeout_occurred = True
    raise TimeoutError("音频生成超时")

def audio_generation_thread():
    """在单独的线程中生成音频"""
    global result
    
    try:
        # 初始化引擎
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        
        # 设置中文语音
        voices = engine.getProperty('voices')
        chinese_voice_found = False
        for voice in voices:
            if 'chinese' in voice.id.lower() or 'zh' in voice.id.lower() or 'mandarin' in voice.id.lower():
                engine.setProperty('voice', voice.id)
                chinese_voice_found = True
                break
        
        if not chinese_voice_found and voices:
            # 如果没有找到中文语音，使用第一个可用语音
            engine.setProperty('voice', voices[0].id)
        
        # 生成音频
        engine.save_to_file(cleaned_text, filename)
        engine.runAndWait()
        
        # 验证文件
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            if file_size > 1024:
                result["success"] = True
                result["message"] = "生成成功，大小: " + str(file_size) + " 字节"
            else:
                result["success"] = False
                result["message"] = "文件太小 (" + str(file_size) + " 字节)"
        else:
            result["success"] = False
            result["message"] = "文件未生成"
            
    except Exception as e:
        result["success"] = False
        result["message"] = "生成错误: " + str(e)

print("[DEBUG] 开始执行TTS脚本")
print(f"[DEBUG] 文本: {{text}}")
print(f"[DEBUG] 输出文件: {{filename}}")
print(f"[DEBUG] 语速: {{rate}}")
print(f"[DEBUG] 初始结果: {{result}}")

try:
    
    # 使用threading.Timer实现超时
    timeout_timer = threading.Timer(10.0, timeout_handler)
    timeout_timer.start()
    
    try:
        # 启动音频生成线程
        audio_thread = threading.Thread(target=audio_generation_thread)
        audio_thread.start()
        
        # 等待音频生成完成
        audio_thread.join(10.0)
        
        if audio_thread.is_alive():
            # 线程仍在运行，说明超时
            result["success"] = False
            result["message"] = "子进程生成超时"
            # 无法强制终止线程，只能返回错误
    except TimeoutError:
        result["success"] = False
        result["message"] = "子进程生成超时"
    finally:
        # 取消超时计时器
        timeout_timer.cancel()
    
except Exception as e:
    result["success"] = False
    result["message"] = "生成错误: " + str(e)
    # 确保引擎被正确关闭
    try:
        if 'engine' in locals():
            engine.stop()
    except:
        pass

print(f"[DEBUG] 执行结果: {{result}}")
# 输出结果
print(json.dumps(result, ensure_ascii=False))
"""
    
    # 格式化脚本内容
    script_content = script_template.format(
        text=json.dumps(test_text),
        filename=json.dumps(temp_audio),
        rate=150,
        result_init=json.dumps({"success": False, "message": "未知错误"})
    )
    
    # 写入临时脚本
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(script_content)
        temp_script = f.name
    
    print(f"\n生成的临时脚本: {temp_script}")
    
    try:
        # 运行临时脚本
        process = subprocess.Popen(
            [sys.executable, temp_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='replace'
        )
        
        # 等待执行
        stdout, stderr = process.communicate(timeout=20)
        
        print(f"\n执行结果:")
        print(f"返回码: {process.returncode}")
        print(f"stdout长度: {len(stdout)} 字节")
        print(f"stdout内容: '{stdout}'")
        print(f"stderr长度: {len(stderr)} 字节")
        print(f"stderr内容: '{stderr}'")
        
        # 尝试解析JSON
        if stdout:
            try:
                result = json.loads(stdout)
                print(f"\nJSON解析成功:")
                print(f"  success: {result['success']}")
                print(f"  message: {result['message']}")
            except json.JSONDecodeError as e:
                print(f"\nJSON解析失败: {e}")
        
        # 检查音频文件是否生成
        if os.path.exists(temp_audio):
            file_size = os.path.getsize(temp_audio)
            print(f"\n音频文件生成: {temp_audio}")
            print(f"文件大小: {file_size} 字节")
            
            # 清理音频文件
            os.unlink(temp_audio)
        else:
            print(f"\n音频文件未生成: {temp_audio}")
    
    except subprocess.TimeoutExpired:
        print("\n执行超时")
        process.kill()
    except Exception as e:
        print(f"\n执行错误: {e}")
    finally:
        # 清理临时脚本
        if os.path.exists(temp_script):
            try:
                os.unlink(temp_script)
            except:
                pass

if __name__ == "__main__":
    test_tts_subprocess()