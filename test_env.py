# Simple Python environment test
print("=== Python Environment Test ===")
print(f"Python path: {__import__('sys').executable}")
print(f"Python version: {__import__('sys').version}")
print(f"Current directory: {__import__('os').getcwd()}")

# Check critical dependencies
try:
    import numpy
    print(f"✓ numpy imported: {numpy.__version__}")
except ImportError as e:
    print(f"✗ numpy import failed: {e}")

try:
    from moviepy.audio.AudioClip import AudioArrayClip
    print("✓ moviepy AudioArrayClip imported")
except ImportError as e:
    print(f"✗ moviepy import failed: {e}")

print("=== Test Complete ===")