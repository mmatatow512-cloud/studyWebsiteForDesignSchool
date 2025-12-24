import http.client
import time

print("=== Simple Server Test ===")

# 等待服务器完全启动
time.sleep(2)

# 测试服务器是否运行
print("\n1. Testing server connection...")
try:
    conn = http.client.HTTPConnection("127.0.0.1", 5001, timeout=10)
    conn.request("GET", "/")
    response = conn.getresponse()
    print(f"Server is running: ✓ (Status: {response.status} {response.reason})")
    conn.close()
    server_ok = True
except Exception as e:
    print(f"Server connection error: {e}")
    server_ok = False

# 测试/courses路由是否存在
if server_ok:
    print("\n2. Testing /courses route...")
    conn = http.client.HTTPConnection("127.0.0.1", 5001, timeout=10)
    conn.request("GET", "/courses")
    response = conn.getresponse()
    print(f"/courses route: ✓ (Status: {response.status} {response.reason})")
    conn.close()

# 测试/course_library路由是否存在
if server_ok:
    print("\n3. Testing /course_library route...")
    conn = http.client.HTTPConnection("127.0.0.1", 5001, timeout=10)
    conn.request("GET", "/course_library")
    response = conn.getresponse()
    print(f"/course_library route: ✓ (Status: {response.status} {response.reason})")
    conn.close()

print("\n=== Test Complete ===")
