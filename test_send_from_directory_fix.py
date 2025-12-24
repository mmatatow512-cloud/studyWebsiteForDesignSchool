import os
import sys

# 设置项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory

# 创建一个简单的Flask应用
app = Flask(__name__)

# 测试修复后的send_from_directory调用
@app.route('/test_download')
def test_download():
    # 测试用的文件路径
    test_dir = os.path.join(app.root_path, 'static', 'uploads')
    test_file = 'test.txt'
    
    # 创建测试文件
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, test_file), 'w') as f:
        f.write('这是一个测试文件，用于验证send_from_directory的修复')
    
    print(f"测试文件路径: {os.path.join(test_dir, test_file)}")
    print(f"目录存在: {os.path.exists(test_dir)}")
    print(f"文件存在: {os.path.exists(os.path.join(test_dir, test_file))}")
    
    # 使用修复后的参数调用send_from_directory
    try:
        return send_from_directory(
            directory=test_dir,
            filename=test_file,  # 正确的参数名
            as_attachment=True
        )
    except Exception as e:
        print(f"错误: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"错误: {type(e).__name__}: {str(e)}"

if __name__ == '__main__':
    print("启动测试服务器在端口5003...")
    print("访问 http://127.0.0.1:5003/test_download 测试下载功能")
    app.run(debug=True, port=5003)