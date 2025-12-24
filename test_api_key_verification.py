# 测试API密钥的有效性
import requests
import json
from AI_analysis.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

print("=== 测试API密钥有效性 ===")
print(f"API密钥: {DEEPSEEK_API_KEY}")
print(f"基础URL: {DEEPSEEK_BASE_URL}")
print(f"模型: {DEEPSEEK_MODEL}")

# 测试API调用
try:
    url = f"{DEEPSEEK_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": "你是一名专业的AI助教，帮助学生解答学习相关的问题。"},
            {"role": "user", "content": "你好，测试一下API连接"}
        ],
        "stream": False
    }
    
    print("\n发送测试请求...")
    response = requests.post(url, headers=headers, json=data, timeout=10)
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ API密钥验证成功！")
    else:
        print(f"\n❌ API密钥验证失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ 请求异常: {type(e).__name__}: {str(e)}")
