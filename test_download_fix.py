import requests
import sys
import os
import re

# 设置项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 登录URL和下载URL
login_url = 'http://127.0.0.1:5001/login'
download_competition_url = 'http://127.0.0.1:5001/download_competition_file/1'

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
        'username': username,
        'password': password,
        'csrf_token': csrf_token
    }
    
    response = session.post(login_url, data=login_data)
    
    if '登录成功' in response.text or response.status_code == 302:
        print("登录成功")
        return True
    else:
        print("登录失败")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:500]}...")
        return False

# 测试下载竞赛文件
def test_download_competition_file():
    print(f"\n测试竞赛文件下载: {download_competition_url}")
    
    response = session.get(download_competition_url, stream=True)
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    if response.status_code == 200:
        # 获取文件名
        content_disposition = response.headers.get('content-disposition', '')
        filename = re.search(r'attachment; filename="([^"]+)"', content_disposition)
        if filename:
            filename = filename.group(1)
        else:
            filename = 'downloaded_competition_file.pdf'
        
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
    print("===== 下载功能测试 =====")
    
    # 登录系统
    if login('学生一', '111'):
        # 测试竞赛文件下载
        test_download_competition_file()
    else:
        print("登录失败，无法测试下载功能")

if __name__ == "__main__":
    main()