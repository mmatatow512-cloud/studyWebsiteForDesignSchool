import unittest
from unittest.mock import patch, MagicMock
import requests
from core.llm.deepseek_client import DeepSeekClient
import os

class TestDeepSeekClient(unittest.TestCase):
    def setUp(self):
        self.client = DeepSeekClient()
        self.question = "什么是设计原则？"
        self.context = "设计原则包括对比、重复、对齐、亲密性等"

    @patch('core.llm.deepseek_client.requests.post')
    def test_normal_call(self, mock_post):
        # 模拟正常响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "设计原则是指导设计决策的基本准则。核心结论：对比、重复、对齐、亲密性是四大设计原则。分步骤解析：1. 对比：通过差异突出重要信息；2. 重复：保持视觉元素的一致性；3. 对齐：确保元素间的视觉联系；4. 亲密性：将相关元素组合在一起。案例参考：网页设计中使用对比色突出按钮，重复使用相同的字体样式保持一致性。"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        # 调用方法
        result = self.client.generate_answer(self.question, self.context)

        # 验证结果
        self.assertIn("设计原则", result)
        self.assertIn("对比、重复、对齐、亲密性", result)
        mock_post.assert_called_once()

    @patch('core.llm.deepseek_client.requests.post')
    def test_api_key_error(self, mock_post):
        # 模拟API密钥错误
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized")
        mock_post.return_value = mock_response

        # 验证是否抛出预期异常
        with self.assertRaises(RuntimeError) as context:
            self.client.generate_answer(self.question, self.context)
        
        self.assertIn("答疑服务暂不可用，请稍后重试", str(context.exception))
        mock_post.assert_called_once()

    @patch('core.llm.deepseek_client.requests.post')
    def test_network_timeout(self, mock_post):
        # 模拟网络超时
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")

        # 验证是否抛出预期异常
        with self.assertRaises(RuntimeError) as context:
            self.client.generate_answer(self.question, self.context)
        
        self.assertIn("答疑服务暂不可用，请稍后重试", str(context.exception))
        # 验证重试了3次
        self.assertEqual(mock_post.call_count, 3)

    @patch('core.llm.deepseek_client.requests.post')
    def test_connection_error(self, mock_post):
        # 模拟连接错误
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")

        # 验证是否抛出预期异常
        with self.assertRaises(RuntimeError) as context:
            self.client.generate_answer(self.question, self.context)
        
        self.assertIn("答疑服务暂不可用，请稍后重试", str(context.exception))
        # 验证重试了3次
        self.assertEqual(mock_post.call_count, 3)

if __name__ == '__main__':
    unittest.main()