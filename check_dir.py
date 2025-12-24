#!/usr/bin/env python3
import os

# 检查目录状态
test_dir = "test_output"
if os.path.exists(test_dir):
    print(f"{test_dir} 目录存在")
    files = os.listdir(test_dir)
    if files:
        print(f"目录内容: {files}")
        for file in files:
            file_path = os.path.join(test_dir, file)
            print(f"  {file}: {os.path.getsize(file_path)} 字节")
    else:
        print("目录为空")
else:
    print(f"{test_dir} 目录不存在")

# 检查当前目录
print("\n当前目录内容:")
for file in os.listdir("."):
    if os.path.isfile(file):
        print(f"  {file}: {os.path.getsize(file)} 字节")
