"""
应用配置管理
使用 Pydantic Settings 管理环境变量和配置
"""

from typing import List, Optional, Union, Any
from pydantic import AnyHttpUrl, BaseSettings, validator, PostgresDsn
import secrets
import os


class Settings(BaseSettings):
    """应用配置类"""
    
    # 基础配置
    PROJECT_NAME: str = "DoodleSketchAI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # 调试模式
    DEBUG: bool = False
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 数据库配置
    DATABASE_URL: Optional[Union[PostgresDsn, str]] = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "doodlesketch"
    DB_PASSWORD: str = "doodlesketch123"
    DB_NAME: str = "doodlesketchai"
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        return f"mysql+pymysql://{values.get('DB_USER')}:{values.get('DB_PASSWORD')}@{values.get('DB_HOST')}:{values.get('DB_PORT')}/{values.get('DB_NAME')}"
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    @validator("REDIS_URL", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        password_part = f":{values.get('REDIS_PASSWORD')}@" if values.get('REDIS_PASSWORD') else ""
        return f"redis://{password_part}{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}/{values.get('REDIS_DB')}"
    
    # CORS 配置
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_VIDEO_FORMATS: List[str] = ["mp4", "avi", "mov", "wmv", "flv", "webm"]
    ALLOWED_IMAGE_FORMATS: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    # C++ 服务配置
    CPP_SERVICE_URL: str = "localhost:50051"
    CPP_SERVICE_HOST: str = "localhost"
    CPP_SERVICE_PORT: int = 50051
    
    @validator("CPP_SERVICE_URL", pre=True)
    def assemble_cpp_service_url(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        return f"{values.get('CPP_SERVICE_HOST')}:{values.get('CPP_SERVICE_PORT')}"
    
    # JWT 配置
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    ALGORITHM: str = "HS256"
    
    # 任务队列配置
    TASK_QUEUE_NAME: str = "doodlesketch_tasks"
    MAX_CONCURRENT_TASKS: int = 5
    TASK_TIMEOUT: int = 300  # 5 minutes
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE: Optional[str] = None
    
    # 缓存配置
    CACHE_TTL: int = 3600  # 1 hour
    SESSION_TTL: int = 86400  # 24 hours
    
    # 性能配置
    WORKERS: int = 1
    LIMIT_CONCURRENT_REQUESTS: int = 1000
    LIMIT_CONNECTIONS: int = 100
    
    # 监控配置
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # 安全配置
    BCRYPT_ROUNDS: int = 12
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_HTTPONLY: bool = True
    
    # AI 模型配置
    U2NET_MODEL_PATH: str = "models/u2net.pth"
    SKETCH_MODEL_PATH: str = "models/sketch_model.onnx"
    MODEL_DEVICE: str = "cpu"  # cpu, cuda, mps
    
    # 外部服务配置
    NOTIFICATION_SERVICE_URL: Optional[str] = None
    ANALYTICS_SERVICE_URL: Optional[str] = None
    
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
