from app import app, db, Unit, Course
import os
import requests
import time

# 验证数据库中的路径格式
with app.app_context():
    print("=== 验证数据库中的路径格式 ===")
    
    # 验证单元路径
    units = Unit.query.all()
    print(f"\n单元路径检查 ({len(units)} 个单元):")
    unit_ok = 0
    unit_error = 0
    
    for unit in units:
        if '\\' in unit.file_path:
            print(f"  ❌ 单元ID: {unit.id}, 文件路径: {unit.file_path} (包含反斜杠)")
            unit_error += 1
        else:
            unit_ok += 1
    
    print(f"  ✅ 正常: {unit_ok}, ❌ 错误: {unit_error}")
    
    # 验证课程视频路径
    courses = Course.query.all()
    print(f"\n课程视频路径检查 ({len(courses)} 个课程):")
    course_ok = 0
    course_error = 0
    
    for course in courses:
        if course.video_path:
            if '\\' in course.video_path:
                print(f"  ❌ 课程ID: {course.id}, 视频路径: {course.video_path} (包含反斜杠)")
                course_error += 1
            else:
                course_ok += 1
        else:
            course_ok += 1
    
    print(f"  ✅ 正常: {course_ok}, ❌ 错误: {course_error}")

# 验证文件访问
print("\n=== 验证文件访问 ===")

# 等待服务器启动
time.sleep(2)

# 测试单元视频文件
with app.app_context():
    units = Unit.query.all()
    print(f"\n测试单元视频文件 ({len(units)} 个):")
    
    for unit in units:
        if unit.file_path:
            url = f'http://127.0.0.1:5001/course_files/{unit.file_path}'
            print(f"\n单元ID: {unit.id}, 路径: {unit.file_path}")
            print(f"  URL: {url}")
            
            try:
                response = requests.head(url, timeout=10)
                if response.status_code == 200:
                    print(f"  ✅ 访问成功，状态码: {response.status_code}")
                    print(f"  内容类型: {response.headers.get('content-type')}")
                else:
                    print(f"  ❌ 访问失败，状态码: {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"  ❌ 连接失败")
            except requests.exceptions.Timeout:
                print(f"  ❌ 请求超时")
            except Exception as e:
                print(f"  ❌ 发生错误: {str(e)}")

# 测试课程视频文件
with app.app_context():
    courses = Course.query.all()
    print(f"\n测试课程视频文件 ({len(courses)} 个):")
    
    for course in courses:
        if course.video_path:
            url = f'http://127.0.0.1:5001/course_files/{course.video_path}'
            print(f"\n课程ID: {course.id}, 代码: {course.course_code}, 路径: {course.video_path}")
            print(f"  URL: {url}")
            
            try:
                response = requests.head(url, timeout=10)
                if response.status_code == 200:
                    print(f"  ✅ 访问成功，状态码: {response.status_code}")
                    print(f"  内容类型: {response.headers.get('content-type')}")
                else:
                    print(f"  ❌ 访问失败，状态码: {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"  ❌ 连接失败")
            except requests.exceptions.Timeout:
                print(f"  ❌ 请求超时")
            except Exception as e:
                print(f"  ❌ 发生错误: {str(e)}")

print("\n=== 验证完成 ===")