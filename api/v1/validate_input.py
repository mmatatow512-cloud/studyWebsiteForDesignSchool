from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import time

# 创建FastAPI应用
app = FastAPI(title="Input Validation API", version="1.0")

# 创建API路由前缀
from fastapi import APIRouter
api_v1_router = APIRouter(prefix="/api/v1")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 敏感词列表（示例）
SENSITIVE_WORDS = {
    "敏感词1", "敏感词2", "敏感词3", "测试敏感词", "不良信息"
}

# 无意义内容模式
MEANINGLESS_PATTERNS = [
    r'^\s*$',  # 空内容
    r'^[\s\.\,\;\:\-\_\+\=\*\/\#\@\!\~\`\(\)\[\]\{\}\"\'\|\\]+$',  # 只有符号
    r'^(\w)\1{4,}$',  # 同一个字符重复5次以上
    r'^(\w+)(\s+\1){3,}$',  # 同一个词重复4次以上
    r'^[a-zA-Z0-9]{20,}$',  # 过长的无意义字符串
    r'^\d{10,}$',  # 过长的数字
    r'^[a-zA-Z]{15,}$',  # 过长的字母
]

# 请求模型
class ValidationRequest(BaseModel):
    content: str
    is_rich_text: bool = False

# 响应模型
class ValidationResponse(BaseModel):
    valid: bool
    msg: str
    sensitive_words: list = []
    response_time: float = 0.0

# 提取纯文本内容（从HTML中）
def extract_plain_text(html_content: str) -> str:
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', html_content)
    # 移除HTML实体
    text = re.sub(r'&[a-zA-Z0-9#]+;', '', text)
    return text.strip()

# 检查敏感词
def check_sensitive_words(content: str) -> list:
    detected_words = []
    for word in SENSITIVE_WORDS:
        if word in content:
            detected_words.append(word)
    return detected_words

# 检查无意义内容
def is_meaningless(content: str) -> bool:
    for pattern in MEANINGLESS_PATTERNS:
        if re.match(pattern, content):
            return True
    return False

# 主验证接口
@api_v1_router.post("/validate", response_model=ValidationResponse)
async def validate_input(request: ValidationRequest):
    start_time = time.time()
    
    try:
        content = request.content
        is_rich_text = request.is_rich_text
        
        # 如果是富文本，提取纯文本进行验证
        if is_rich_text:
            text_to_check = extract_plain_text(content)
        else:
            text_to_check = content
        
        # 检查内容是否为空
        if not text_to_check:
            response_time = time.time() - start_time
            return ValidationResponse(
                valid=False,
                msg="输入内容为空或只包含HTML标签",
                response_time=round(response_time * 1000, 2)
            )
        
        # 检查敏感词
        sensitive_words = check_sensitive_words(text_to_check)
        if sensitive_words:
            response_time = time.time() - start_time
            return ValidationResponse(
                valid=False,
                msg=f"检测到敏感词：{', '.join(sensitive_words)}",
                sensitive_words=sensitive_words,
                response_time=round(response_time * 1000, 2)
            )
        
        # 检查无意义内容
        if is_meaningless(text_to_check):
            response_time = time.time() - start_time
            return ValidationResponse(
                valid=False,
                msg="输入内容无意义，请重新输入",
                response_time=round(response_time * 1000, 2)
            )
        
        # 所有检查通过
        response_time = time.time() - start_time
        return ValidationResponse(
            valid=True,
            msg="输入内容验证通过",
            response_time=round(response_time * 1000, 2)
        )
        
    except Exception as e:
        response_time = time.time() - start_time
        return ValidationResponse(
            valid=False,
            msg=f"验证过程中发生错误：{str(e)}",
            response_time=round(response_time * 1000, 2)
        )

# 健康检查接口
@api_v1_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Input Validation API"}

# 敏感词管理接口（示例）
@api_v1_router.get("/sensitive-words")
async def get_sensitive_words():
    return {"sensitive_words": list(SENSITIVE_WORDS)}

@api_v1_router.post("/sensitive-words")
async def add_sensitive_word(word: str):
    if not word or len(word.strip()) < 2:
        raise HTTPException(status_code=400, detail="敏感词长度必须至少为2个字符")
    
    cleaned_word = word.strip()
    SENSITIVE_WORDS.add(cleaned_word)
    return {"message": f"敏感词 '{cleaned_word}' 已添加", "total_words": len(SENSITIVE_WORDS)}

@api_v1_router.delete("/sensitive-words/{word}")
async def remove_sensitive_word(word: str):
    if word not in SENSITIVE_WORDS:
        raise HTTPException(status_code=404, detail="敏感词不存在")
    
    SENSITIVE_WORDS.remove(word)
    return {"message": f"敏感词 '{word}' 已移除", "total_words": len(SENSITIVE_WORDS)}

# 将API路由添加到应用
app.include_router(api_v1_router)
