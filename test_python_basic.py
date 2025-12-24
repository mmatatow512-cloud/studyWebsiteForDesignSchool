print("Hello, Python!")
print("Python is working!")

import os
print("Current directory:", os.getcwd())
print("Files in directory:")
for f in os.listdir('.')[:5]:  # 只显示前5个文件
    print("  -", f)
