import requests
import time

# 等待服务器完全启动
time.sleep(2)

print("=== 测试服务器连接和视频访问 ===")

# 测试课程库页面
print("\n1. 测试课程库页面 (GET /course_library):")
try:
    response = requests.get('http://127.0.0.1:5001/course_library', timeout=10)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ 课程库页面可以正常访问")
    else:
        print("   ❌ 课程库页面访问失败")
except requests.exceptions.ConnectionError:
    print("   ❌ 连接失败 - 服务器可能没有运行")
except Exception as e:
    print(f"   ❌ 发生错误: {str(e)}")

# 测试有问题的视频URL
print("\n2. 测试视频文件 (GET /course_files/P001/unit_2_5af2f06321637469ff1b56dabf7f2d05.mp4):")
try:
    response = requests.head('http://127.0.0.1:5001/course_files/P001/unit_2_5af2f06321637469ff1b56dabf7f2d05.mp4', timeout=10)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ 视频文件可以正常访问")
        print(f"   内容类型: {response.headers.get('content-type')}")
        print(f"   内容长度: {response.headers.get('content-length')} 字节")
    else:
        print("   ❌ 视频文件访问失败")
except requests.exceptions.ConnectionError:
    print("   ❌ 连接失败 - 服务器可能没有运行")
except Exception as e:
    print(f"   ❌ 发生错误: {str(e)}")

# 测试其他视频URL
print("\n3. 测试其他视频URL:")
video_urls = [
    'http://127.0.0.1:5001/course_files/B001/unit_1_2ff1b400ce557d715052ab3286d37716.mp4',
    'http://127.0.0.1:5001/course_files/P001/unit_1_729605751-1-208.mp4'
]

for url in video_urls:
    print(f"\n   测试: {url}")
    try:
        response = requests.head(url, timeout=10)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 视频文件可以正常访问")
        else:
            print("   ❌ 视频文件访问失败")
    except requests.exceptions.ConnectionError:
        print("   ❌ 连接失败 - 服务器可能没有运行")
    except Exception as e:
        print(f"   ❌ 发生错误: {str(e)}")

print("\n=== 测试完成 ===")