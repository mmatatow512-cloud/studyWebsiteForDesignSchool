from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.validate_input import router as validate_router

# 创建FastAPI应用
app = FastAPI(
    title="Input Validation API",
    description="设计学科文字/富文本输入校验接口",
    version="1.0.0"
)

# 配置CORS，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应设置为具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(validate_router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    根路径
    """
    return {"message": "Input Validation API is running"}

@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "healthy"}