import os
import sys
import tempfile
import json
import subprocess
import re

# 测试文本内容，包含用户提到的特殊字符
test_texts = [
    "，，西方艺术风格的五个关键时代，，，• 古典艺术的奠基",
    "这是正常文本的测试",
    "• 第一点：测试项目符号",
    "古典艺术，，，的主要特点包括：比例和谐，对称均衡",
    "• 文艺复兴时期的艺术作品，以达芬奇、米开朗基罗等为代表",
    "空白文本测试"
]

def test_pyttsx3_directly():
    """直接测试pyttsx3是否工作正常"""
    print("=== 直接测试pyttsx3 ===")
    import pyttsx3
    
    try:
        engine = pyttsx3.init()
        
        # 获取可用语音
        voices = engine.getProperty('voices')
        print(f"可用语音数量: {len(voices)}")
        for i, voice in enumerate(voices):
            print(f"  语音 {i+1}: {voice.id} - {voice.name}")
        
        # 测试生成音频
        test_file = os.path.join(tempfile.gettempdir(), "direct_test.wav")
        engine.save_to_file("这是一个直接测试", test_file)
        engine.runAndWait()
        
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"直接测试音频生成成功，文件大小: {file_size} 字节")
            os.remove(test_file)
            return True
        else:
            print("直接测试音频生成失败")
            return False
    
    except Exception as e:
        print(f"直接测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_subprocess_script():
    """测试使用子进程执行的脚本"""
    print("\n=== 测试子进程脚本 ===")
    
    # 创建与ppt2video.py中相同的脚本模板
    script_template = '''
import pyttsx3
import os
import sys
import json
import re

# 获取参数
text = {text}
filename = {filename}
rate = {rate}

# 清理文本
cleaned_text = text
# 使用三重引号来避免转义字符问题
cleaned_text = re.sub(r'[，。、；："\'\n\r]+', '，', cleaned_text)
cleaned_text = re.sub(r'[•●■◆]', '', cleaned_text)
cleaned_text = re.sub(r'[，]+', '，', cleaned_text)
cleaned_text = re.sub(r'^[，]+|[，]+$', '', cleaned_text)
if not cleaned_text.strip():
    cleaned_text = "空白幻灯片"
if len(cleaned_text) > 100:
    cleaned_text = cleaned_text[:97] + "..."

result = {{"success": False, "message": "未知错误"}}

# 保存调试信息
with open('tts_subprocess_debug.log', 'a', encoding='utf-8') as f:
    f.write(f"Text: {{text[:200]}}\n")
    f.write(f"Cleaned text: {{cleaned_text[:200]}}\n")
    f.write(f"Filename: {{filename}}\n")
    f.write(f"Rate: {{rate}}\n")

try:
    # 初始化引擎
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    
    # 设置中文语音
    voices = engine.getProperty('voices')
    chinese_voice_found = False
    for voice in voices:
        if 'chinese' in voice.id.lower() or 'zh' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            chinese_voice_found = True
            break
    
    if not chinese_voice_found and voices:
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
    result["message"] = "生成错误: " + str(e)
    with open('tts_subprocess_error.log', 'a', encoding='utf-8') as f:
        f.write(f"Error: {{str(e)}}\n")

# 输出结果
print(json.dumps(result, ensure_ascii=False))
'''
    
    success_count = 0
    
    for i, text in enumerate(test_texts):
        print(f"\n测试文本 {i+1}: {text[:50]}{'...' if len(text) > 50 else ''}")
        
        # 准备参数
        output_file = os.path.join(tempfile.gettempdir(), f"subprocess_test_{i+1}.wav")
        script_content = script_template.format(
            text=json.dumps(text),
            filename=json.dumps(output_file),
            rate=150
        )
        
        # 写入临时脚本
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            # 使用更安全的方式写入脚本内容，避免转义字符问题
            f.write("import pyttsx3\n")
            f.write("import os\n")
            f.write("import sys\n")
            f.write("import json\n")
            f.write("import re\n")
            f.write("\n")
            f.write("# 获取参数\n")
            f.write(f"text = {json.dumps(text)}\n")
            f.write(f"filename = {json.dumps(output_file)}\n")
            f.write(f"rate = 150\n")
            f.write("\n")
            f.write("# 清理文本\n")
            f.write("cleaned_text = text\n")
            f.write("cleaned_text = re.sub(r'[，。、；：\"\'\n\r]+', '，', cleaned_text)\n")
            f.write("cleaned_text = re.sub(r'[•●■◆]', '', cleaned_text)\n")
            f.write("cleaned_text = re.sub(r'[，]+', '，', cleaned_text)\n")
            f.write("cleaned_text = re.sub(r'^[，]+|[，]+$', '', cleaned_text)\n")
            f.write("if not cleaned_text.strip():\n")
            f.write("    cleaned_text = '空白幻灯片'\n")
            f.write("if len(cleaned_text) > 100:\n")
            f.write("    cleaned_text = cleaned_text[:97] + '...'\n")
            f.write("\n")
            f.write("result = {'success': False, 'message': '未知错误'}\n")
            f.write("\n")
            f.write("# 保存调试信息\n")
            f.write("with open('tts_subprocess_debug.log', 'a', encoding='utf-8') as f_debug:\n")
            f.write("    f_debug.write(f'Text: {{text[:200]}}\n')\n")
            f.write("    f_debug.write(f'Cleaned text: {{cleaned_text[:200]}}\n')\n")
            f.write("    f_debug.write(f'Filename: {{filename}}\n')\n")
            f.write("    f_debug.write(f'Rate: {{rate}}\n')\n")"\'\n\r]+', '，', cleaned_text)\n")
            f.write("cleaned_text = re.sub(r'[•●■◆]', '', cleaned_text)\n")
            f.write("cleaned_text = re.sub(r'[，]+', '，', cleaned_text)\n")
            f.write("cleaned_text = re.sub(r'^[，]+|[，]+$', '', cleaned_text)\n")
            f.write("if not cleaned_text.strip():\n")
            f.write("    cleaned_text = '空白幻灯片'\n")
            f.write("if len(cleaned_text) > 100:\n")
            f.write("    cleaned_text = cleaned_text[:97] + '...'\n")
            f.write("\n")
            f.write("result = {'success': False, 'message': '未知错误'}\n")
            f.write("\n")
            f.write("# 保存调试信息\n")
            f.write("with open('tts_subprocess_debug.log', 'a', encoding='utf-8') as f_debug:\n")
            f.write("    f_debug.write(f'Text: {text[:200]}\n')\n")
            f.write("    f_debug.write(f'Cleaned text: {cleaned_text[:200]}\n')\n")
            f.write("    f_debug.write(f'Filename: {output_file}\n')\n")
            f.write("    f_debug.write(f'Rate: 150\n')\n")
            f.write("\n")
            f.write("try:\n")
            f.write("    # 初始化引擎\n")
            f.write("    engine = pyttsx3.init()\n")
            f.write("    engine.setProperty('rate', rate)\n")
            f.write("    \n")
            f.write("    # 设置中文语音\n")
            f.write("    voices = engine.getProperty('voices')\n")
            f.write("    chinese_voice_found = False\n")
            f.write("    for voice in voices:\n")
            f.write("        if 'chinese' in voice.id.lower() or 'zh' in voice.id.lower():\n")
            f.write("            engine.setProperty('voice', voice.id)\n")
            f.write("            chinese_voice_found = True\n")
            f.write("            break\n")
            f.write("    \n")
            f.write("    if not chinese_voice_found and voices:\n")
            f.write("        engine.setProperty('voice', voices[0].id)\n")
            f.write("    \n")
            f.write("    # 生成音频\n")
            f.write("    engine.save_to_file(cleaned_text, filename)\n")
            f.write("    engine.runAndWait()\n")
            f.write("    \n")
            f.write("    # 验证文件\n")
            f.write("    if os.path.exists(filename):\n")
            f.write("        file_size = os.path.getsize(filename)\n")
            f.write("        if file_size > 1024:\n")
            f.write("            result['success'] = True\n")
            f.write("            result['message'] = f'生成成功，大小: {file_size} 字节'\n")
            f.write("        else:\n")
            f.write("            result['success'] = False\n")
            f.write("            result['message'] = f'文件太小 ({file_size} 字节)'\n")
            f.write("    else:\n")
            f.write("        result['success'] = False\n")
            f.write("        result['message'] = '文件未生成'\n")
            f.write("        \n")
            f.write("except Exception as e:\n")
            f.write("    result['success'] = False\n")
            f.write("    result['message'] = '生成错误: ' + str(e)\n")
            f.write("    with open('tts_subprocess_error.log', 'a', encoding='utf-8') as f_error:\n")
            f.write("        f_error.write(f'Error: {str(e)}\n')\n")
            f.write("\n")
            f.write("# 输出结果\n")
            f.write("print(json.dumps(result, ensure_ascii=False))\n")
            temp_script = f.name
        
        try:
            # 执行脚本
            process = subprocess.Popen(
                [sys.executable, temp_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='replace'
            )
            
            stdout, stderr = process.communicate(timeout=20)
            
            print(f"  子进程退出码: {process.returncode}")
            
            if stdout:
                try:
                    result = json.loads(stdout)
                    print(f"  执行结果: {result}")
                    
                    if result["success"]:
                        success_count += 1
                        if os.path.exists(output_file):
                            os.remove(output_file)
                except json.JSONDecodeError:
                    print(f"  JSON解析失败，输出: {stdout}")
            else:
                print(f"  子进程没有输出")
                if stderr:
                    print(f"  错误输出: {stderr}")
            
        except subprocess.TimeoutExpired:
            print("  子进程超时")
            process.kill()
        except Exception as e:
            print(f"  执行错误: {e}")
        finally:
            # 清理临时文件
            if os.path.exists(temp_script):
                os.remove(temp_script)
            if os.path.exists(output_file):
                os.remove(output_file)
    
    print(f"\n子进程测试完成，成功: {success_count}/{len(test_texts)}")
    return success_count

def test_text_cleaning():
    """测试文本清理逻辑"""
    print("\n=== 测试文本清理 ===")
    
    for text in test_texts:
        cleaned = text
        cleaned = re.sub(r'[，。、；："\'\n\r]+', '，', cleaned)
        cleaned = re.sub(r'[•●■◆]', '', cleaned)
        cleaned = re.sub(r'[，]+', '，', cleaned)
        cleaned = re.sub(r'^[，]+|[，]+$', '', cleaned)
        if not cleaned.strip():
            cleaned = "空白幻灯片"
        if len(cleaned) > 100:
            cleaned = cleaned[:97] + "..."
        
        print(f"  原始: {text[:50]}{'...' if len(text) > 50 else ''}")
        print(f"  清理后: {cleaned}")

if __name__ == "__main__":
    print("开始测试音频生成功能")
    print(f"Python版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    
    # 测试文本清理
    test_text_cleaning()
    
    # 直接测试pyttsx3
    pyttsx3_works = test_pyttsx3_directly()
    
    # 测试子进程脚本
    success_count = test_subprocess_script()
    
    print("\n=== 测试总结 ===")
    print(f"直接pyttsx3测试: {'通过' if pyttsx3_works else '失败'}")
    print(f"子进程脚本测试: {success_count}/{len(test_texts)} 通过")
    
    if pyttsx3_works and success_count == len(test_texts):
        print("所有测试都通过了！")
    else:
        print("测试中发现了问题，请检查上面的输出")
