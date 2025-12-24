# 测试脚本，用于验证API密钥配置

# 添加项目根目录到Python路径
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入配置
from AI_analysis.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

print("=== API密钥配置测试 ===")
print(f"DEEPSEEK_API_KEY: {DEEPSEEK_API_KEY}")
print(f"DEEPSEEK_BASE_URL: {DEEPSEEK_BASE_URL}")
print(f"DEEPSEEK_MODEL: {DEEPSEEK_MODEL}")
print(f"API密钥是否为占位符: {DEEPSEEK_API_KEY == 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}")
