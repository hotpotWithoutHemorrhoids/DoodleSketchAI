# DoodleSketchAI 后端 Dockerfile
# Python FastAPI 服务

# 使用官方 Python 基础镜像
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libmysqlclient-dev \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libavutil-dev \
    libgtk2.0-dev \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    libwebp-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip
RUN pip install --upgrade pip setuptools wheel

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建非 root 用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p /app/uploads /app/logs /app/temp && \
    chown -R appuser:appuser /app

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
