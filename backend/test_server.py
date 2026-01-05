"""
简化的测试服务器
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# 简化的配置
class SimpleConfig:
    PROJECT_NAME = "DoodleSketchAI"
    VERSION = "1.0.0"
    API_V1_STR = "/api/v1"
    UPLOAD_DIR = "uploads"
    DEBUG = True
    BACKEND_CORS_ORIGINS = ["*"]

settings = SimpleConfig()

# 创建应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="文件上传测试 API",
    version=settings.VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[        
        "http://localhost:3000",          # 本地开发（可选）
        "http://127.0.0.1:3000"],          # 本地开发（可选
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保上传目录存在
if settings.UPLOAD_DIR and not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# 挂载静态文件
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

@app.get("/")
async def root():
    return {"message": "Test Server Running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
