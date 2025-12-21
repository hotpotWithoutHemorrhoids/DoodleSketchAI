# DoodleSketchAI C++ 服务端 Dockerfile
# 多阶段构建以优化镜像大小

# 构建阶段
FROM ubuntu:22.04 AS builder

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive

# 安装构建依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    git \
    wget \
    curl \
    unzip \
    libssl-dev \
    libgrpc++-dev \
    libprotobuf-dev \
    protobuf-compiler-grpc \
    libopencv-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libavutil-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /build

# 复制源代码
COPY . .

# 构建应用
RUN mkdir -p build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc) && \
    make install

# 运行阶段
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive \
    LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    libssl3 \
    libgrpc++1 \
    libprotobuf23 \
    libopencv-core4.5d \
    libopencv-imgproc4.5d \
    libopencv-imgcodecs4.5d \
    libopencv-videoio4.5d \
    libavcodec58 \
    libavformat58 \
    libswscale5 \
    libavutil56 \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 创建应用目录
RUN mkdir -p /app /app/models /app/config /app/logs

# 从构建阶段复制二进制文件
COPY --from=builder /usr/local/bin/DoodleSketchAI_CPP /app/doodlesketch-server

# 复制配置文件
COPY config/ /app/config/

# 创建非 root 用户
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app

# 切换到非 root 用户
USER appuser

# 设置工作目录
WORKDIR /app

# 暴露端口
EXPOSE 50051

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50051/health || exit 1

# 启动命令
CMD ["./doodlesketch-server", "--port", "50051", "--config", "config/config.yaml"]
