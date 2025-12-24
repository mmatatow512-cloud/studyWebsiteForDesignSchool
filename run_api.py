import uvicorn
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.v1.validate_input import app

if __name__ == "__main__":
    uvicorn.run(
        "api.v1.validate_input:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
