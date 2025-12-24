import os
from dotenv import load_dotenv

load_dotenv()

class DeepSeekConfig:
    API_KEY = os.getenv("DEEPSEEK_API_KEY")
    BASE_URL = os.getenv("DEEPSEEK_API_BASE_URL")
    MODEL_NAME = os.getenv("DEEPSEEK_MODEL_NAME")
    MAX_TOKENS = int(os.getenv("DEEPSEEK_MAX_TOKENS", 2048))
    TEMPERATURE = float(os.getenv("DEEPSEEK_TEMPERATURE", 0.3))
    TIMEOUT = int(os.getenv("DEEPSEEK_TIMEOUT", 10))

    @classmethod
    def validate(cls):
        if not all([cls.API_KEY, cls.BASE_URL, cls.MODEL_NAME]):
            raise ValueError("DeepSeek配置不完整，请检查.env文件")

DeepSeekConfig.validate()