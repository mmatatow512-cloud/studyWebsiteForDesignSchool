import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

try:
    # 创建浏览器实例
    driver = webdriver.Chrome(options=chrome_options)
    
    print("=== 浏览器测试 /courses 路由 ===")
    
    # 访问登录页面
    driver.get("http://127.0.0.1:5001/login")
    print(f"1. 访问登录页面: {driver.current_url} (状态码: {driver.title})")
    
    # 输入用户名和密码
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    
    username_input.send_keys("学生一")
    password_input.send_keys("password")
    
    # 提交表单
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    
    # 等待页面加载
    time.sleep(2)
    
    print(f"2. 登录后页面: {driver.current_url} (状态码: {driver.title})")
    
    # 访问/courses路由
    driver.get("http://127.0.0.1:5001/courses")
    
    # 等待页面加载
    time.sleep(2)
    
    print(f"3. 访问/courses路由: {driver.current_url} (状态码: {driver.title})")
    
    # 检查页面内容
    page_source = driver.page_source
    
    if "我的课程" in page_source:
        print("4. 页面包含'我的课程'，加载成功！")
    else:
        print("4. 页面不包含'我的课程'，加载失败！")
        print("页面内容前500字符:", page_source[:500])
        
    # 截图
    driver.save_screenshot("courses_screenshot.png")
    print("5. 已保存页面截图到courses_screenshot.png")
    
except Exception as e:
    print(f"测试过程中出错: {e}")
finally:
    # 关闭浏览器
    if 'driver' in locals():
        driver.quit()
        print("\n=== 浏览器测试完成 ===")
