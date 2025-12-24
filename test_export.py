import os
import sys
import win32com.client
import pythoncom
import tempfile
import shutil

# 配置Python路径
sys.path.insert(0, os.path.abspath('.'))

def test_ppt_export(ppt_path):
    """测试PPT幻灯片导出功能"""
    print("=== PPT导出测试 ===")
    print(f"测试文件: {ppt_path}")
    print(f"文件存在: {os.path.exists(ppt_path)}")
    if os.path.exists(ppt_path):
        print(f"文件大小: {os.path.getsize(ppt_path)} 字节")
    
    # 初始化COM组件
    pythoncom.CoInitialize()
    
    temp_dir = tempfile.mkdtemp()
    print(f"临时目录: {temp_dir}")
    
    try:
        # 创建PowerPoint COM对象
        print("创建PowerPoint COM对象...")
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = 1  # 设置为可见以便调试
        
        # 检查文件头
        with open(ppt_path, 'rb') as f:
            header = f.read(8)
            print(f"文件头8字节: {header.hex()}")
            if header.startswith(b'PK'):
                print("确认是PPTX文件 (ZIP格式)")
            elif header.startswith(b'\xd0\xcf\x11\xe0'):
                print("确认是PPT文件 (OLE格式)")
            else:
                print("警告: 可能不是标准PPT/PPTX文件")
        
        # 打开PPT文件
        print(f"打开PPT文件: {ppt_path}")
        presentation = powerpoint.Presentations.Open(os.path.abspath(ppt_path), WithWindow=True)
        
        # 获取幻灯片数量
        slides_count = len(presentation.Slides)
        print(f"幻灯片数量: {slides_count}")
        
        # 导出幻灯片
        exported_images = []
        for i, slide in enumerate(presentation.Slides):
            img_path = os.path.join(temp_dir, f"slide_{i+1:02d}.jpg")
            print(f"导出第 {i+1} 页到: {img_path}")
            
            try:
                slide.Export(img_path, "JPG", 1920, 1080)
                
                if os.path.exists(img_path):
                    img_size = os.path.getsize(img_path)
                    print(f"  导出成功，大小: {img_size} 字节")
                    exported_images.append(img_path)
                else:
                    print(f"  导出失败，文件不存在")
            except Exception as e:
                print(f"  导出错误: {e}")
        
        # 关闭PPT
        presentation.Close()
        
        # 退出PowerPoint
        powerpoint.Quit()
        
        print(f"\n=== 导出结果 ===")
        print(f"尝试导出: {slides_count} 张")
        print(f"成功导出: {len(exported_images)} 张")
        
        # 检查导出的图片
        if exported_images:
            for img_path in exported_images[:3]:  # 只显示前3张
                img_size = os.path.getsize(img_path)
                print(f"  {os.path.basename(img_path)}: {img_size} 字节")
        
        return exported_images
        
    except Exception as e:
        print(f"\n=== 错误信息 ===")
        print(f"导出失败: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"已清理临时目录: {temp_dir}")

if __name__ == "__main__":
    # 使用现有的测试PPT文件
    test_ppt_path = "test_ppt.pptx"
    if not os.path.exists(test_ppt_path):
        print(f"错误: 测试文件 {test_ppt_path} 不存在！")
        sys.exit(1)
    
    exported = test_ppt_export(test_ppt_path)
    if exported:
        print("\n✓ PPT导出测试成功！")
    else:
        print("\n✗ PPT导出测试失败！")
        sys.exit(1)
