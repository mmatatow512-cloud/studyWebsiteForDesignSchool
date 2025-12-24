#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 极简测试脚本

import os
import sys
import time

# 使用绝对路径确保文件写入到预期位置
log_path = os.path.abspath("ultra_minimal.log")

# 直接打开文件写入
with open(log_path, "w") as f:
    f.write("START\n")
    f.write(f"Python path: {sys.executable}\n")
    f.write(f"Version: {sys.version}\n")
    f.write(f"CWD: {os.getcwd()}\n")
    f.write(f"Time: {time.time()}\n")
    f.write("END\n")

# 尝试输出到stdout（可能被重定向）
print("TEST_COMPLETE")
