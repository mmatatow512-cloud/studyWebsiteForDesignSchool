import requests
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, RetryError
from core.config import DeepSeekConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekClient:
    def __init__(self):
        self.config = DeepSeekConfig
        self.headers = {
            "Authorization": f"Bearer {self.config.API_KEY}",
            "Content-Type": "application/json"
        }

    def generate_answer(self, question: str, context: str = ""):
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_fixed(1),
            retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout))
        )
        def _request():
            system_prompt = """你是设计学科线上课程AI助教，需基于课程上下文精准解答。输出规则：
            1. 设计原理类：核心结论+分步骤解析+案例参考
            2. 软件操作类（PS/AI等）：菜单路径+快捷键+操作截图提示
            3. 标注知识点关联，未关联需说明
            4. 语言简洁专业"""
            payload = {
                "model": self.config.MODEL_NAME,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"上下文：{context}\n问题：{question}"}
                ],
                "max_tokens": self.config.MAX_TOKENS,
                "temperature": self.config.TEMPERATURE
            }
            response = requests.post(
                self.config.BASE_URL,
                headers=self.headers,
                json=payload,
                timeout=self.config.TIMEOUT
            )
            response.raise_for_status()
            return response.json()

        try:
            result = _request()
            return result["choices"][0]["message"]["content"]
        except RetryError as e:
            logger.error(f"DeepSeek API调用重试失败：{str(e)}")
            raise RuntimeError(f"答疑服务暂不可用，请稍后重试") from None
        except Exception as e:
            logger.error(f"DeepSeek API调用失败：{str(e)}")
            raise RuntimeError(f"答疑服务暂不可用，请稍后重试") from e