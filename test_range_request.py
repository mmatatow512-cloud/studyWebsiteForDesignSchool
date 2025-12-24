import requests

# 测试视频文件的Range请求
url = 'http://127.0.0.1:5001/course_files/B001/unit_1_2ff1b400ce557d715052ab3286d37716.mp4'

# 测试1: 完整文件请求
print("测试1: 完整文件请求")
try:
    response = requests.head(url)
    print(f"状态码: {response.status_code}")
    print(f"Content-Length: {response.headers.get('Content-Length')}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Accept-Ranges: {response.headers.get('Accept-Ranges')}")
except Exception as e:
    print(f"错误: {e}")

# 测试2: Range请求
print("\n测试2: Range请求")
try:
    headers = {'Range': 'bytes=0-100'}
    response = requests.get(url, headers=headers, stream=True)
    print(f"状态码: {response.status_code}")
    print(f"Content-Range: {response.headers.get('Content-Range')}")
    print(f"Content-Length: {response.headers.get('Content-Length')}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    # 读取前几个字节验证响应
    content = response.raw.read(10)
    print(f"响应内容(前10字节): {content[:10]}")
except Exception as e:
    print(f"错误: {e}")
