#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test to verify audio generation functionality
"""

import os
import sys
import time
import tempfile
import subprocess
import json
import re

def test_audio_generation():
    """Test audio generation"""
    print("=== Audio Generation Test ===")
    
    # Test text (simulating the problematic second page text)
    test_text = "，，西方艺术风格的五个关键时代，，，• 古典艺术的奠基（古希腊与古罗马），• 追求理想与比例：以人体..."
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    print(f"Temp directory: {temp_dir}")
    
    try:
        # Test with simple text first
        simple_text = "这是一个简单的测试音频"
        simple_audio = os.path.join(temp_dir, "simple.wav")
        
        print("\n1. Testing with simple text...")
        success, message = generate_audio(simple_text, simple_audio, 170)
        print(f"   Result: {'Success' if success else 'Failed'}")
        print(f"   Message: {message}")
        if success and os.path.exists(simple_audio):
            print(f"   File size: {os.path.getsize(simple_audio)} bytes")
        
        # Test with problematic text
        print("\n2. Testing with problematic text...")
        problematic_audio = os.path.join(temp_dir, "problematic.wav")
        start_time = time.time()
        success, message = generate_audio(test_text, problematic_audio, 170)
        duration = time.time() - start_time
        print(f"   Result: {'Success' if success else 'Failed'}")
        print(f"   Message: {message}")
        print(f"   Duration: {duration:.1f} seconds")
        if success and os.path.exists(problematic_audio):
            print(f"   File size: {os.path.getsize(problematic_audio)} bytes")
        
    finally:
        # Clean up
        if os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)

def generate_audio(text, filename, rate):
    """Generate audio using subprocess"""
    # Clean text first
    cleaned_text = text
    # Remove duplicate punctuation
    cleaned_text = re.sub(r'[，。、；：“”‘’"\'\n\r]+', '，', cleaned_text)
    # Remove duplicate commas
    cleaned_text = re.sub(r'[，]+', '，', cleaned_text)
    # Remove ellipsis
    cleaned_text = re.sub(r'[.]+', '', cleaned_text)
    # Remove bullet points
    cleaned_text = re.sub(r'[•●■◆]', '', cleaned_text)
    # Limit text length
    if len(cleaned_text) > 100:
        cleaned_text = cleaned_text[:100] + "..."
    
    if not cleaned_text.strip():
        cleaned_text = "空白幻灯片"
    
    print(f"   Cleaned text: {cleaned_text}")
    
    # Create temporary script
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(f'''
import pyttsx3
import os
import sys
import json
import time

# Get parameters
text = {json.dumps(cleaned_text)!r}
filename = {json.dumps(filename)!r}
rate = {rate}

result = {{"success": False, "message": "未知错误"}}

try:
    # Initialize engine
    start_time = time.time()
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    
    # Set Chinese voice
    voices = engine.getProperty('voices')
    chinese_voice_found = False
    for voice in voices:
        if 'chinese' in voice.id.lower() or 'zh' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            chinese_voice_found = True
            break
    
    if not chinese_voice_found and voices:
        engine.setProperty('voice', voices[0].id)
    
    # Generate audio
    engine.save_to_file(text, filename)
    engine.runAndWait()
    
    # Verify file
    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
        if file_size > 1024:
            result["success"] = True
            result["message"] = f"Generated successfully, size: {{file_size}} bytes"
        else:
            result["success"] = False
            result["message"] = f"File too small ({{file_size}} bytes)"
    else:
        result["success"] = False
        result["message"] = "File not generated"
    
except Exception as e:
    result["success"] = False
    result["message"] = f"Error: {{e}}"

# Output result
print(json.dumps(result, ensure_ascii=False))
''')
        temp_script = f.name
    
    try:
        # Run the script with timeout
        process = subprocess.Popen(
            [sys.executable, temp_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8'
        )
        
        # Wait for process to complete with 15 seconds timeout
        stdout, stderr = process.communicate(timeout=15)
        
        if process.returncode == 0:
            try:
                result = json.loads(stdout)
                return result["success"], result["message"]
            except json.JSONDecodeError:
                return False, f"Failed to parse result: {stdout[:100]}..."
        else:
            return False, f"Script execution failed: {stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        process.kill()
        return False, "Generation timeout"
    except Exception as e:
        return False, f"Execution error: {e}"
    finally:
        # Clean up
        if os.path.exists(temp_script):
            try:
                os.unlink(temp_script)
            except:
                pass

if __name__ == "__main__":
    test_audio_generation()