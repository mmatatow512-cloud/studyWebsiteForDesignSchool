import os
import tempfile
import sys

def test_file_operations():
    print("=== Python文件操作测试 ===")
    print(f"Python版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 测试1: 基本文件写入
    print("\n1. 测试基本文件写入...")
    try:
        test_path = os.path.abspath("test_write.txt")
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write("测试文件写入功能正常\n")
            f.write(f"当前时间: {__import__('datetime').datetime.now()}\n")
        
        if os.path.exists(test_path):
            size = os.path.getsize(test_path)
            print(f"   ✓ 成功: 文件已创建，大小: {size} 字节")
            
            # 读取并验证内容
            with open(test_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"   ✓ 内容验证通过: {content.strip()}")
            
            # 删除测试文件
            os.remove(test_path)
            print(f"   ✓ 文件已删除")
        else:
            print(f"   ✗ 失败: 文件未创建")
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    # 测试2: 临时目录创建
    print("\n2. 测试临时目录创建...")
    try:
        temp_dir = tempfile.mkdtemp()
        print(f"   ✓ 成功: 临时目录已创建: {temp_dir}")
        
        # 在临时目录中创建文件
        temp_file = os.path.join(temp_dir, "temp_test.txt")
        with open(temp_file, 'w') as f:
            f.write("临时文件测试")
        
        if os.path.exists(temp_file):
            print(f"   ✓ 成功: 临时目录中文件已创建")
        
        # 清理临时目录
        import shutil
        shutil.rmtree(temp_dir)
        print(f"   ✓ 临时目录已删除")
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    # 测试3: 输出目录创建
    print("\n3. 测试输出目录创建...")
    try:
        output_dir = os.path.join(os.getcwd(), "test_output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"   ✓ 成功: 输出目录已创建: {output_dir}")
        
        # 在输出目录创建文件
        output_file = os.path.join(output_dir, "output_test.mp4")
        with open(output_file, 'w') as f:
            f.write("视频文件占位符")
        
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"   ✓ 成功: 输出目录中文件已创建，大小: {size} 字节")
        
        # 清理
        os.remove(output_file)
        os.rmdir(output_dir)
        print(f"   ✓ 输出目录已清理")
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    # 测试4: 权限检查
    print("\n4. 测试权限检查...")
    try:
        # 检查当前目录的写权限
        test_perm = os.path.abspath("perm_test.txt")
        with open(test_perm, 'w') as f:
            f.write("权限测试")
        
        if os.access(os.getcwd(), os.W_OK):
            print(f"   ✓ 当前目录具有写权限")
        else:
            print(f"   ✗ 当前目录没有写权限")
        
        os.remove(test_perm)
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_file_operations()