#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 修复ppt2video.py中的重复函数定义问题
import os

# 定义文件路径
file_path = os.path.abspath('project/ppt2video.py')
print(f'处理文件: {file_path}')

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'原始文件行数: {len(lines)}')

# 删除第442-722行（索引从441到721）
if len(lines) > 722:
    new_lines = lines[:441] + lines[722:]
    print(f'修改后文件行数: {len(new_lines)}')
    print(f'删除了 {len(lines) - len(new_lines)} 行')
    
    # 写入修改后的文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print('重复的generate_audio函数已成功删除！')
else:
    print('文件行数不足，可能已经被修改过了。')
    print(f'当前文件行数: {len(lines)}')
