import http.client
import urllib.parse
import json

# 创建连接
conn = http.client.HTTPConnection("127.0.0.1", 5001)

# 1. 获取登录页面的cookies
print("1. Getting login page cookies...")
conn.request("GET", "/login")
response = conn.getresponse()
cookies = response.getheader('Set-Cookie')
print(f"Cookies: {cookies}")

# 2. 登录
print("\n2. Logging in...")
login_data = urllib.parse.urlencode({
    'username': '学生一',  # 使用实际的测试用户名
    'password': 'password'       # 使用默认密码
})
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': cookies
}
conn.request("POST", "/login", login_data, headers)
response = conn.getresponse()
print(f"Status: {response.status} {response.reason}")
print(f"Location: {response.getheader('Location')}")

# 更新cookies
if response.getheader('Set-Cookie'):
    cookies = response.getheader('Set-Cookie')
    print(f"Updated cookies: {cookies}")

# 3. 访问/courses路由
print("\n3. Accessing /courses route...")
headers = {
    'Cookie': cookies
}
conn.request("GET", "/courses", headers=headers)
response = conn.getresponse()
print(f"Status: {response.status} {response.reason}")
print(f"Content-Type: {response.getheader('Content-Type')}")

# 读取部分内容
content = response.read(500).decode('utf-8')
print(f"Response content (first 500 chars): {content}")

conn.close()
