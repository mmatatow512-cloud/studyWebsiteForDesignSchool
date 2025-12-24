# 用于删除ppt2video.py中的重复generate_audio函数

file_path = r'c:\Users\23576\Desktop\demo\project\ppt2video.py'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'原始文件总行数: {len(lines)}')

# 第一部分：从开始到第441行（索引0-440）
first_part = lines[:441]

# 第二部分：从第723行开始到结束（索引722及以后）
second_part = lines[722:]

# 合并两部分
new_lines = first_part + second_part

# 写入修改后的文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'修改后文件总行数: {len(new_lines)}')
print(f'已成功删除第442-722行的重复generate_audio函数')
print(f'删除的行数: {len(lines) - len(new_lines)}')