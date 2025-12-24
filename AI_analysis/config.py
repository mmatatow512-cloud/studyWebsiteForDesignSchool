# API配置文件

# DeepSeek API配置（保留旧配置作为备份）
DEEPSEEK_API_KEY = "sk-361d41da6a3841348567026cc993e629"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

# 阿里云百炼API配置
DASHSCOPE_API_KEY = "sk-361d41da6a3841348567026cc993e629"
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DASHSCOPE_MODEL = "deepseek-r1"

# 评分维度配置
GRADING_DIMENSIONS = {
    "topic_relevance": "主题相关性",
    "logic_structure": "逻辑结构完整性",
    "content_depth": "内容深度与广度",
    "language_accuracy": "语言表达准确性"
}

# 评分等级配置
SCORE_LEVELS = {
    "excellent": {"range": (90, 100), "desc": "优秀"},
    "good": {"range": (80, 89), "desc": "良好"},
    "average": {"range": (70, 79), "desc": "中等"},
    "below_average": {"range": (60, 69), "desc": "及格"},
    "poor": {"range": (0, 59), "desc": "不及格"}
}
