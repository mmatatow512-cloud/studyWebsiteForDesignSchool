import os

# 获取course_files目录的绝对路径
COURSE_FILES_PATH = os.path.abspath('course_files')
print(f"Course files directory: {COURSE_FILES_PATH}")

# 检查目录是否存在
if not os.path.exists(COURSE_FILES_PATH):
    print(f"Directory not found: {COURSE_FILES_PATH}")
    exit()

# 列出要检查的视频文件
video_files = [
    'B001/unit_1_2ff1b400ce557d715052ab3286d37716.mp4',
    'P001/unit_1_729605751-1-208.mp4',
    'P001/unit_2_5af2f06321637469ff1b56dabf7f2d05.mp4'
]

# 检查每个文件是否存在
for video_file in video_files:
    file_path = os.path.join(COURSE_FILES_PATH, video_file)
    print(f"Checking file: {video_file}")
    print(f"Full path: {file_path}")
    print(f"Exists: {os.path.exists(file_path)}")
    print()

# 列出course_files目录中的所有文件和子目录
print("Contents of course_files directory:")
for root, dirs, files in os.walk(COURSE_FILES_PATH):
    level = root.replace(COURSE_FILES_PATH, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        print(f"{subindent}{file}")
