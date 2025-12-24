#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple diagnostic script to check Python environment and basic imports
"""

print("=== Python Environment Diagnostic ===")

import sys
print(f"Python interpreter: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Working directory: {sys.path[0]}")

# Check if we're using WindowsApps stub Python
if "WindowsApps" in sys.executable:
    print("ERROR: Using WindowsApps stub Python! This won't work.")
else:
    print("✓ Using real Python interpreter")

# Try basic imports
print("\n=== Testing Basic Imports ===")
try:
    import os
    print("✓ Imported os")
except ImportError as e:
    print(f"✗ Failed to import os: {e}")

try:
    import sys
    print("✓ Imported sys")
except ImportError as e:
    print(f"✗ Failed to import sys: {e}")

try:
    import tempfile
    print("✓ Imported tempfile")
except ImportError as e:
    print(f"✗ Failed to import tempfile: {e}")

try:
    import subprocess
    print("✓ Imported subprocess")
except ImportError as e:
    print(f"✗ Failed to import subprocess: {e}")

try:
    import json
    print("✓ Imported json")
except ImportError as e:
    print(f"✗ Failed to import json: {e}")

try:
    import re
    print("✓ Imported re")
except ImportError as e:
    print(f"✗ Failed to import re: {e}")

# Try ppt2video import
print("\n=== Testing ppt2video Import ===")
try:
    import ppt2video
    print("✓ Imported ppt2video module")
    
    # Check if ConverterLogic class exists
    if hasattr(ppt2video, 'ConverterLogic'):
        print("✓ Found ConverterLogic class")
        
        # Try to create a minimal instance
        def simple_log(message):
            print(f"[LOG] {message}")
        
        try:
            converter = ppt2video.ConverterLogic(logger_func=simple_log)
            print("✓ Created ConverterLogic instance successfully")
            
            # Check if generate_audio method exists
            if hasattr(converter, 'generate_audio'):
                print("✓ Found generate_audio method")
            else:
                print("✗ generate_audio method not found")
                
        except Exception as e:
            print(f"✗ Failed to create ConverterLogic instance: {e}")
    else:
        print("✗ ConverterLogic class not found")
        
except ImportError as e:
    print(f"✗ Failed to import ppt2video: {e}")
    import traceback
    traceback.print_exc()

except Exception as e:
    print(f"✗ Unexpected error importing ppt2video: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Diagnostic Complete ===")
