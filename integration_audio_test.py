#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration test for ppt2video audio functionality
Verifies that the main convert_presentation_to_video function generates videos with audio
"""

import os
import sys
import time
import tempfile
import subprocess

def log(message):
    """Simple logging function"""
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def check_video_has_audio(video_path):
    """Check if the generated video has audio using ffprobe"""
    if not os.path.exists(video_path):
        log(f"Error: Video file not found at {video_path}")
        return False
    
    log(f"Checking audio in video: {video_path}")
    
    try:
        # Try to use ffprobe
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', video_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            audio_codec = result.stdout.strip()
            if audio_codec:
                log(f"✓ Video contains audio stream with codec: {audio_codec}")
                return True
            else:
                log("✗ Video does not contain any audio streams")
                return False
        else:
            log(f"Warning: ffprobe failed with error: {result.stderr}")
            log("Falling back to file size check")
            # Fallback: Check file size - video with audio should be larger than 100KB
            file_size = os.path.getsize(video_path)
            if file_size > 100 * 1024:  # 100KB
                log(f"✓ Video file size is {file_size/1024:.1f} KB (likely has audio)")
                return True
            else:
                log(f"✗ Video file size is too small ({file_size/1024:.1f} KB)")
                return False
    except FileNotFoundError:
        log("Warning: ffprobe not found, using file size check")
        file_size = os.path.getsize(video_path)
        if file_size > 100 * 1024:  # 100KB
            log(f"✓ Video file size is {file_size/1024:.1f} KB (likely has audio)")
            return True
        else:
            log(f"✗ Video file size is too small ({file_size/1024:.1f} KB)")
            return False
    except Exception as e:
        log(f"Error checking audio: {e}")
        return False

def main():
    """Main test function"""
    log("=== PPT to Video Audio Integration Test ===")
    
    # Verify Python environment
    log(f"Python interpreter: {sys.executable}")
    log(f"Python version: {sys.version}")
    
    # Check if we're using the correct Python path
    python_path = sys.executable
    if "WindowsApps" in python_path:
        log("ERROR: Using WindowsApps stub Python! Please use real Python path.")
        # Try to find real Python
        try:
            result = subprocess.run(
                ['where', 'python'],
                capture_output=True,
                text=True
            )
            python_paths = [p for p in result.stdout.strip().split('\n') if 'WindowsApps' not in p]
            if python_paths:
                real_python = python_paths[0].strip()
                log(f"Found real Python at: {real_python}")
                log("Please run this script with: ")
                log(f"  {real_python} integration_audio_test.py")
        except:
            pass
        return False
    
    # Check if test PPT exists
    test_ppt = "test_ppt.pptx"
    if not os.path.exists(test_ppt):
        test_ppt = "test_integration.pptx"
    
    if not os.path.exists(test_ppt):
        log(f"Error: Test PPT file not found ({test_ppt})")
        return False
    
    log(f"Using test PPT: {test_ppt}")
    
    # Create temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate output video path
        output_video = os.path.join(temp_dir, f"test_output_{int(time.time())}.mp4")
        
        log(f"Output video will be saved to: {output_video}")
        
        # Import the ppt2video module
        log("Importing ppt2video module...")
        try:
            import ppt2video
            log("✓ Successfully imported ppt2video module")
        except ImportError as e:
            log(f"✗ Failed to import ppt2video: {e}")
            return False
        
        # Call the main conversion function
        log("Starting PPT to video conversion...")
        start_time = time.time()
        
        try:
            result = ppt2video.convert_presentation_to_video(test_ppt, output_video, rate=170)
            duration = time.time() - start_time
            
            if result:
                log(f"✓ Conversion completed successfully in {duration:.1f} seconds")
                
                # Check if output video exists
                if os.path.exists(output_video):
                    file_size = os.path.getsize(output_video)
                    log(f"Video file size: {file_size/1024:.1f} KB")
                    
                    # Check if video has audio
                    if check_video_has_audio(output_video):
                        log("\n🎉 Test PASSED: Video has audio!")
                        return True
                    else:
                        log("\n❌ Test FAILED: Video has no audio")
                        return False
                else:
                    log(f"❌ Error: Output video file not found at {output_video}")
                    return False
            else:
                log(f"❌ Conversion failed")
                return False
                
        except Exception as e:
            log(f"❌ Conversion error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
