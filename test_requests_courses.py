import requests

# 创建一个会话
with requests.Session() as session:
    print("=== 使用requests测试 /courses 路由 ===")
    
    # 1. 访问登录页面获取cookies
    login_page = session.get("http://127.0.0.1:5001/login")
    print(f"1. 访问登录页面: 状态码 {login_page.status_code}")
    
    # 2. 登录
    login_data = {
        "username": "学生一",
        "password": "password",
        "role": "student"
    }
    
    login_response = session.post("http://127.0.0.1:5001/login", data=login_data)
    print(f"2. 登录请求: 状态码 {login_response.status_code}")
    print(f"   登录后重定向到: {login_response.url}")
    
    # 3. 访问dashboard页面
    dashboard_response = session.get("http://127.0.0.1:5001/dashboard")
    print(f"3. 访问dashboard页面: 状态码 {dashboard_response.status_code}")
    
    # 4. 访问/courses路由
    courses_response = session.get("http://127.0.0.1:5001/courses")
    print(f"4. 访问/courses路由: 状态码 {courses_response.status_code}")
    
    # 5. 检查响应内容
    if courses_response.status_code == 200:
        if "我的课程" in courses_response.text:
            print("5. 页面包含'我的课程'，加载成功！")
        else:
            print("5. 页面不包含'我的课程'，可能加载失败！")
            print("页面内容前500字符:", courses_response.text[:500])
    else:
        print(f"5. 访问失败，状态码: {courses_response.status_code}")
        
    print("\n=== 测试完成 ===")
