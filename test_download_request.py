import requests
import sys
import os
import re

# 设置项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 登录URL和下载URL
login_url = 'http://127.0.0.1:5001/login'
download_url = 'http://127.0.0.1:5001/download_assignment_file/1'

# 创建会话
session = requests.Session()

# 获取登录页面，查找CSRF令牌
def get_csrf_token():
    response = session.get(login_url)
    # 查找CSRF令牌
    csrf_token = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', response.text)
    if csrf_token:
        return csrf_token.group(1)
    else:
        print("无法找到CSRF令牌")
        return None

# 登录系统
def login(username, password):
    csrf_token = get_csrf_token()
    if not csrf_token:
        return False
    
    login_data = {
        'csrf_token': csrf_token,
        'username': username,
        'password': password
    }
    
    response = session.post(login_url, data=login_data, allow_redirects=True)
    
    print(f"登录请求状态码: {response.status_code}")
    print(f"登录后重定向到: {response.url}")
    
    # 检查是否登录成功
    if '/login' not in response.url and '用户名或密码错误' not in response.text:
        print("登录成功")
        return True
    else:
        print("登录失败")
        if '用户名或密码错误' in response.text:
            print("错误信息: 用户名或密码错误")
        return False

# 测试下载功能
def test_download():
    # 发送下载请求
    response = session.get(download_url, stream=True)
    
    print(f"\n下载请求状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    if response.status_code == 200:
        # 获取文件名
        content_disposition = response.headers.get('content-disposition', '')
        filename = re.search(r'attachment; filename="([^"]+)"', content_disposition)
        if filename:
            filename = filename.group(1)
        else:
            filename = 'downloaded_file.pdf'
        
        # 保存文件
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"文件下载成功，保存为: {filename}")
        print(f"文件大小: {os.path.getsize(filename)} 字节")
        return True
    else:
        print("下载失败")
        print(f"响应内容: {response.text[:500]}...")
        return False

# 主函数
def main():
    # 登录系统
    if login('学生一', '111'):
        # 测试下载功能
        test_download()
    else:
        print("登录失败，无法测试下载功能")

if __name__ == "__main__":
    main()
