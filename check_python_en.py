# Python Environment Check
import sys

def main():
    print("Python Version:", sys.version)
    print("Python Executable:", sys.executable)
    print("sys module available")
    
    # Check numpy
    try:
        import numpy
        print("numpy available, version:", numpy.__version__)
    except ImportError:
        print("numpy NOT available")
        
    # Check moviepy
    try:
        import moviepy
        print("moviepy available")
        
        # Check specific components
        try:
            from moviepy.video.VideoClip import ImageClip
            print("ImageClip available")
        except ImportError:
            print("ImageClip NOT available")
            
        try:
            from moviepy.audio.AudioClip import AudioFileClip
            print("AudioFileClip available")
        except ImportError:
            print("AudioFileClip NOT available")
            
        try:
            from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
            print("concatenate_videoclips available")
        except ImportError:
            print("concatenate_videoclips NOT available")
            
    except ImportError:
        print("moviepy NOT available")

if __name__ == "__main__":
    print("=== Python Environment Check Started ===")
    main()
    print("=== Python Environment Check Completed ===")
