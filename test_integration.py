import requests
import time

# 测试配置
FASTAPI_URL = "http://localhost:8000/api/v1/validate"
FLASK_URL = "http://127.0.0.1:5000"
TEST_TIMEOUT = 5  # 5秒超时

print("开始测试前后端集成...")
print("=" * 50)

# 1. 测试FastAPI验证服务是否正常运行
print("\n1. 测试FastAPI验证服务...")
try:
    response = requests.get("http://localhost:8000/api/v1/health", timeout=TEST_TIMEOUT)
    if response.status_code == 200:
        print("✅ FastAPI验证服务正常运行")
    else:
        print(f"❌ FastAPI验证服务状态异常: {response.status_code}")
except Exception as e:
    print(f"❌ FastAPI验证服务无法访问: {str(e)}")

# 2. 测试验证接口
print("\n2. 测试验证接口...")

# 测试纯文本验证
test_cases = [
    # 正常内容
    ({"content": "这是一个正常的测试内容", "is_rich_text": False}, True),
    # 敏感词测试
    ({"content": "这是一个测试敏感词的内容", "is_rich_text": False}, False),
    # 无意义内容测试
    ({"content": "aaaaa", "is_rich_text": False}, False),
    # 空内容测试
    ({"content": "", "is_rich_text": False}, False),
    # 富文本测试
    ({"content": "<p>这是一个<strong>富文本</strong>测试内容</p>", "is_rich_text": True}, True),
    # 包含敏感词的富文本
    ({"content": "<p>这是一个包含敏感词1的富文本</p>", "is_rich_text": True}, False),
]

for i, (test_data, expected_valid) in enumerate(test_cases, 1):
    try:
        start_time = time.time()
        response = requests.post(FASTAPI_URL, json=test_data, timeout=TEST_TIMEOUT)
        response_time = (time.time() - start_time) * 1000  # 转换为毫秒
        
        if response.status_code == 200:
            result = response.json()
            status = "✅" if result["valid"] == expected_valid else "❌"
            response_time_status = "✅" if response_time <= 100 else "⚠️"
            print(f"   {i}. {status} 测试内容: {test_data['content'][:30]}...")
            print(f"      预期: {'有效' if expected_valid else '无效'}, 实际: {'有效' if result['valid'] else '无效'}")
            print(f"      响应时间: {response_time:.2f}ms {response_time_status} (≤100ms)")
            if result['msg']:
                print(f"      消息: {result['msg']}")
        else:
            print(f"   {i}. ❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"   {i}. ❌ 测试失败: {str(e)}")

# 3. 测试Flask主服务是否正常运行
print("\n3. 测试Flask主服务...")
try:
    response = requests.get(FLASK_URL, timeout=TEST_TIMEOUT)
    if response.status_code == 200:
        print("✅ Flask主服务正常运行")
    else:
        print(f"❌ Flask主服务状态异常: {response.status_code}")
except Exception as e:
    print(f"❌ Flask主服务无法访问: {str(e)}")

# 4. 测试text_input页面是否可以访问
print("\n4. 测试text_input页面...")
try:
    response = requests.get(f"{FLASK_URL}/text_input", timeout=TEST_TIMEOUT, allow_redirects=False)
    if response.status_code in [200, 302]:  # 302是重定向到登录页面，也视为正常
        print(f"✅ text_input页面可访问 (状态码: {response.status_code})")
    else:
        print(f"❌ text_input页面访问失败: {response.status_code}")
except Exception as e:
    print(f"❌ text_input页面无法访问: {str(e)}")

print("\n" + "=" * 50)
print("集成测试完成！")
