#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test to verify ppt2video audio functionality
"""

import os
import sys
import time
import tempfile
import shutil

def main():
    """Main test function"""
    print("=== Simple PPT to Video Audio Test ===")
    
    # Check Python path
    python_path = sys.executable
    print(f"Python interpreter: {python_path}")
    
    # Check test PPT
    test_ppt = "test_ppt.pptx"
    if not os.path.exists(test_ppt):
        print(f"Error: Test PPT not found ({test_ppt})")
        return 1
    
    print(f"Using test PPT: {test_ppt}")
    
    # Create output directory
    output_dir = "test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate output video path
    output_video = os.path.join(output_dir, f"test_{int(time.time())}.mp4")
    
    print(f"Output video: {output_video}")
    
    # Import ppt2video
    print("Importing ppt2video...")
    try:
        import ppt2video
    except ImportError as e:
        print(f"Error importing ppt2video: {e}")
        return 1
    
    # Run conversion
    print("Running conversion...")
    start_time = time.time()
    
    try:
        result = ppt2video.convert_presentation_to_video(test_ppt, output_video, rate=170)
        duration = time.time() - start_time
        
        print(f"Conversion finished in {duration:.1f} seconds")
        
        if result:
            print("✓ Conversion successful!")
            
            if os.path.exists(output_video):
                file_size = os.path.getsize(output_video)
                print(f"Video size: {file_size/1024:.1f} KB")
                
                # Copy to root for easy access
                shutil.copy2(output_video, "latest_test.mp4")
                print("Video copied to: latest_test.mp4")
                return 0
            else:
                print("✗ Output video not found")
                return 1
        else:
            print("✗ Conversion failed")
            return 1
            
    except Exception as e:
        print(f"Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
