"""
应用配置管理
使用 Pydantic Settings 管理环境变量和配置
"""

from typing import List, Optional, Union, Any
from pydantic import AnyHttpUrl, validator, PostgresDsn
from pydantic_settings import BaseSettings
import secrets
import os


class Settings(BaseSettings):
    """应用配置类"""
    
    # 基础配置
    PROJECT_NAME: str = "DoodleSketchAI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # 调试模式
    DEBUG: bool = False
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_VIDEO_FORMATS: List[str] = ["mp4", "avi", "mov", "wmv", "flv", "webm"]
    ALLOWED_IMAGE_FORMATS: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    BACKEND_CORS_ORIGINS:List[str] = [        
        "http://localhost:3000",
        "http://127.0.0.1:3000"]
    # C++ 服务配置
    # CPP_SERVICE_URL: str = "localhost:50051"
    # CPP_SERVICE_HOST: str = "localhost"
    # CPP_SERVICE_PORT: int = 50051
    
    # @validator("CPP_SERVICE_URL", pre=True)
    # def assemble_cpp_service_url(cls, v: Optional[str], values: dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
        
    #     return f"{values.get('CPP_SERVICE_HOST')}:{values.get('CPP_SERVICE_PORT')}"
    

    
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"


# 创建全局配置实例
settings = Settings()


# 开发环境特殊配置
if settings.DEBUG:
    settings.BACKEND_CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]


def get_settings() -> Settings:
    """获取配置实例"""
    return settings
