#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import pythoncom
import win32com.client

print("=== PPT导出图片测试 ===")
print(f"Python版本: {sys.version}")

# 检查测试PPT文件
test_ppt = "test_ppt.pptx"
if not os.path.exists(test_ppt):
    print(f"ERROR: PPT文件不存在: {test_ppt}")
    sys.exit(1)

print(f"PPT文件: {test_ppt}")
print(f"文件大小: {os.path.getsize(test_ppt)} 字节")

# 初始化COM组件
pythoncom.CoInitialize()

try:
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    print(f"临时目录: {temp_dir}")
    
    # 打开PowerPoint
    print("\n打开PowerPoint...")
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = 1
    
    # 检查文件格式
    with open(test_ppt, 'rb') as f:
        header = f.read(8)
        print(f"文件头: {header.hex()}")
        if header.startswith(b'PK'):
            print("确认是PPTX文件 (ZIP格式)")
        elif header.startswith(b'\xd0\xcf\x11\xe0'):
            print("确认是PPT文件 (OLE格式)")
        else:
            print("警告: 可能不是标准PPT文件格式")
    
    # 打开PPT文件
    print(f"\n打开PPT文件: {test_ppt}")
    presentation = powerpoint.Presentations.Open(os.path.abspath(test_ppt), WithWindow=False)
    
    # 获取幻灯片数量
    print(f"幻灯片数量: {len(presentation.Slides)}")
    
    # 导出每张幻灯片
    print("\n导出幻灯片图片...")
    for i, slide in enumerate(presentation.Slides):
        img_path = os.path.join(temp_dir, f"slide_{i+1:02d}.jpg")
        print(f"  导出第 {i+1} 页到: {img_path}")
        
        # 导出图片
        slide.Export(img_path, "JPG", 0, 1080)
        
        # 验证导出
        if os.path.exists(img_path):
            size = os.path.getsize(img_path)
            print(f"  ✓ 成功，大小: {size} 字节")
        else:
            print(f"  ✗ 失败，文件不存在")
    
    # 关闭PPT
    presentation.Close()
    powerpoint.Quit()
    
    print("\n=== 测试完成 ===")
    print(f"临时目录中的文件: {os.listdir(temp_dir)}")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    # 清理
    pythoncom.CoUninitialize()
    print("\nCOM组件已释放")
