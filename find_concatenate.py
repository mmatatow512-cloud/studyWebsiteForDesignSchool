import os
import sys

# 获取moviepy的安装路径
import moviepy
moviepy_path = os.path.dirname(moviepy.__file__)
print(f"moviepy安装路径: {moviepy_path}")

# 搜索所有包含concatenate的Python文件
def search_concatenate():
    print("\n正在搜索包含concatenate的Python文件...")
    found_files = []
    
    for root, dirs, files in os.walk(moviepy_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'concatenate' in content.lower():
                            found_files.append(file_path)
                            print(f"找到文件: {file_path}")
                except Exception as e:
                    print(f"读取文件失败: {file_path}, 错误: {e}")
    
    return found_files

# 查看找到的文件内容，寻找concatenate_videoclips函数
def check_files(files):
    print("\n正在检查文件内容...")
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'concatenate_videoclips' in content:
                    print(f"\n在文件中找到concatenate_videoclips: {file_path}")
                    # 显示函数定义附近的内容
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'concatenate_videoclips' in line:
                            start = max(0, i-3)
                            end = min(len(lines), i+10)
                            print("函数定义附近内容:")
                            for j in range(start, end):
                                print(f"  {j+1}: {lines[j]}")
                            break
        except Exception as e:
            print(f"读取文件失败: {file_path}, 错误: {e}")

if __name__ == "__main__":
    found_files = search_concatenate()
    check_files(found_files)