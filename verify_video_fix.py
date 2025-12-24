from app import app, db, Unit, Course
import os
import requests
import time

# 验证数据库中的路径是否已更新为正斜杠
with app.app_context():
    print("=== 验证数据库中的路径格式 ===")
    units = Unit.query.all()
    
    for unit in units:
        print(f"单元ID: {unit.id}, 文件路径: {unit.file_path}")
        if '\\' in unit.file_path:
            print(f"  ❌ 仍然包含反斜杠")
        else:
            print(f"  ✅ 使用了正斜杠")

# 验证文件访问路径
print("\n=== 验证文件访问路径 ===")

# 重启应用服务（如果需要）
try:
    # 尝试访问本地服务器上的视频文件
    print("尝试访问本地服务器上的视频文件...")
    time.sleep(2)  # 等待服务器启动
    
    # 测试路径
    test_paths = [
        '/course_files/B001/unit_1_2ff1b400ce557d715052ab3286d37716.mp4',
        '/course_files/P001/unit_1_729605751-1-208.mp4',
        '/course_files/P001/unit_2_5af2f06321637469ff1b56dabf7f2d05.mp4'
    ]
    
    for path in test_paths:
        url = f'http://127.0.0.1:5001{path}'
        print(f"\n测试URL: {url}")
        
        try:
            response = requests.get(url, stream=True, timeout=5)
            if response.status_code == 200:
                print(f"  ✅ 访问成功，状态码: {response.status_code}")
                print(f"  内容类型: {response.headers.get('content-type')}")
            else:
                print(f"  ❌ 访问失败，状态码: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"  ❌ 连接失败，请确保服务器已启动")
        except requests.exceptions.Timeout:
            print(f"  ❌ 请求超时")
        except Exception as e:
            print(f"  ❌ 发生错误: {str(e)}")
            
except Exception as e:
    print(f"启动测试服务时发生错误: {str(e)}")