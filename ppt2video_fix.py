# 修复后的generate_audio方法代码
    def generate_audio(self, scripts, temp_folder, voice_id, rate):
        # 导入必要的模块
        import os
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        audio_paths = []
        self.log("正在生成音频文件...")
        
        # 导入所需库
        import numpy as np
        import pyttsx3
        import threading
        import queue
        import re
        import subprocess
        import time
        import tempfile
        import json
        
        self.log(f"    设置语速: {rate or 150}")
        self.log(f"    使用语音生成系统: pyttsx3 + 超时保护")
        
        def generate_audio_with_timeout(text, filename, rate, timeout=15):
            """带超时的音频生成函数 - 使用进程级保护"""
            # 清理文本
            cleaned_text = re.sub(r'[，。、；："\'\n\r]+', '，', text)
            cleaned_text = re.sub(r'^，+|，+$', '', cleaned_text)
            if not cleaned_text.strip():
                cleaned_text = "空白幻灯片"
            if len(cleaned_text) > 100:
                cleaned_text = cleaned_text[:97] + "..."
            
            # 创建临时脚本内容
            script_content = '''
import pyttsx3
import os
import sys
import json
import threading
import re
import time

# 获取参数
text = {text!r}
filename = {filename!r}
rate = {rate}

result = {result_init!r}

# 进一步清理文本，移除过多的标点和省略号
cleaned_text = text
# 移除重复的标点符号
cleaned_text = re.sub(r'[，。、；："\'\n\r]+', '，', cleaned_text)
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
                result["message"] = f"生成成功，大小: {{file_size}} 字节"
            else:
                result["success"] = False
                result["message"] = f"文件太小 ({{file_size}} 字节)"
        else:
            result["success"] = False
            result["message"] = "文件未生成"
            
    except Exception as e:
        result["success"] = False
        result["message"] = f"生成错误: {{e}}"

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
    result["message"] = f"生成错误: {{e}}"
    # 确保引擎被正确关闭
    try:
        if 'engine' in locals():
            engine.stop()
    except:
        pass

# 输出结果
print(json.dumps(result, ensure_ascii=False))
'''
            
            # 替换参数
            script_content = script_content.format(
                text=json.dumps(cleaned_text),
                filename=json.dumps(filename),
                rate=rate or 150,
                result_init={"success": False, "message": "未知错误"}
            )
            
            # 写入临时脚本
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(script_content)
                temp_script = f.name
                
                try:
                    # 运行临时脚本
                    process = subprocess.Popen(
                        [sys.executable, temp_script],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        encoding='utf-8',
                        errors='replace'
                    )
                    
                    # 等待超时
                    stdout, stderr = process.communicate(timeout=timeout)
                    
                    if process.returncode == 0:
                        result = json.loads(stdout)
                        return result["success"], result["message"]
                    else:
                        stderr_msg = stderr.strip() if stderr else "未知错误"
                        return False, f"脚本执行失败: {stderr_msg}"
                        
                except subprocess.TimeoutExpired:
                    process.kill()
                    return False, "生成超时"
                except json.JSONDecodeError:
                    return False, f"结果解析失败: {stdout[:100]}..."
                except Exception as e:
                    return False, f"执行错误: {e}"
                finally:
                    # 清理临时脚本
                    if os.path.exists(temp_script):
                        try:
                            os.unlink(temp_script)
                        except:
                            pass
        
        # 使用带超时的音频生成
        for i, text in enumerate(scripts):
            filename = os.path.join(temp_folder, f"audio_{i + 1:02d}.wav")
            self.log(f"  - 处理第 {i + 1} 页音频...")
            self.log(f"    文本内容: {text[:50]}..." if len(text) > 50 else f"    文本内容: {text}")

            try:
                # 使用带超时的音频生成
                self.log(f"    生成语音...")
                success, message = generate_audio_with_timeout(text, filename, rate)
                
                if success:
                    self.log(f"    音频文件{message}")
                    audio_paths.append(filename)
                    self.log(f"    音频文件有效，已添加到列表")
                else:
                    self.log(f"    [警告] {message}，尝试重新生成...")
                    
                    # 尝试重新生成一次
                    success, message = generate_audio_with_timeout(text, filename, rate)
                    
                    if success:
                        self.log(f"    重新生成成功，{message}")
                        audio_paths.append(filename)
                    else:
                        self.log(f"    [错误] 重新生成失败 ({message})，使用降级方案")
                        # 降级方案
                        try:
                            from moviepy.audio.AudioClip import AudioArrayClip
                            estimated_duration = max(2.0, len(text) * 0.33)
                            samples = int(estimated_duration * 44100)
                            t = np.linspace(0, estimated_duration, samples)
                            audio_array = np.sin(2 * np.pi * 440 * t)
                            audio_array = np.column_stack((audio_array, audio_array)).astype(np.float32)
                            audio_clip = AudioArrayClip(audio_array, fps=44100)
                            audio_clip.write_audiofile(filename, fps=44100)
                            
                            if os.path.exists(filename) and os.path.getsize(filename) > 1024:
                                self.log(f"    降级方案生成成功")
                                audio_paths.append(filename)
                            else:
                                self.log(f"    [错误] 降级方案生成的文件无效")
                        except Exception as e3:
                            self.log(f"    [错误] 降级方案执行失败: {e3}")
            except Exception as e:
                self.log(f"    [错误] 音频生成失败: {e}")
                # 降级方案
                self.log(f"    [降级方案] 使用简单音频生成替代")
                try:
                    from moviepy.audio.AudioClip import AudioArrayClip
                    estimated_duration = max(2.0, len(text) * 0.33)
                    samples = int(estimated_duration * 44100)
                    t = np.linspace(0, estimated_duration, samples)
                    audio_array = np.sin(2 * np.pi * 440 * t)
                    audio_array = np.column_stack((audio_array, audio_array)).astype(np.float32)
                    audio_clip = AudioArrayClip(audio_array, fps=44100)
                    audio_clip.write_audiofile(filename, fps=44100)
                    
                    if os.path.exists(filename) and os.path.getsize(filename) > 1024:
                        self.log(f"    降级方案生成成功")
                        audio_paths.append(filename)
                except Exception as e2:
                    self.log(f"    [错误] 降级方案也失败: {e2}")
                    continue
        
        self.log(f"  音频生成完成，共生成 {len(audio_paths)} 个音频文件")
        return audio_paths