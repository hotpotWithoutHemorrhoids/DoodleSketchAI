# DoodleSketchAI 项目构建和部署脚本

.PHONY: help install dev build test clean docker-up docker-down logs

# 默认目标
help:
	@echo "DoodleSketchAI 开发命令"
	@echo ""
	@echo "可用命令:"
	@echo "  install     - 安装所有依赖"
	@echo "  dev         - 启动开发环境"
	@echo "  build       - 构建生产版本"
	@echo "  test        - 运行测试"
	@echo "  clean       - 清理临时文件"
	@echo "  docker-up   - 启动 Docker 服务"
	@echo "  docker-down - 停止 Docker 服务"
	@echo "  logs        - 查看服务日志"
	@echo "  format      - 格式化代码"
	@echo "  lint        - 代码检查"

# 安装所有依赖
install:
	@echo "安装前端依赖..."
	cd frontend && npm install
	@echo "安装后端依赖..."
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	@echo "安装 C++ 依赖..."
	cd cpp-server && mkdir -p build && cd build && cmake .. && make

# 启动开发环境
dev:
	@echo "启动开发环境..."
	docker-compose up -d mysql redis
	@echo "等待数据库启动..."
	sleep 10
	@echo "启动后端服务..."
	cd backend && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
	@echo "启动前端服务..."
	cd frontend && npm run dev &
	@echo "启动 C++ 服务..."
	cd cpp-server && ./build/cpp_server --port 50051 &
	@echo "所有服务已启动"

# 构建生产版本
build:
	@echo "构建前端..."
	cd frontend && npm run build
	@echo "构建后端..."
	cd backend && source venv/bin/activate && pip install -r requirements.txt
	@echo "构建 C++ 服务..."
	cd cpp-server && mkdir -p build && cd build && cmake .. && make release
	@echo "构建 Docker 镜像..."
	docker-compose build

# 运行测试
test:
	@echo "运行前端测试..."
	cd frontend && npm run test
	@echo "运行后端测试..."
	cd backend && source venv/bin/activate && pytest
	@echo "运行 C++ 测试..."
	cd cpp-server && ./build/tests

# 清理临时文件
clean:
	@echo "清理前端文件..."
	cd frontend && rm -rf node_modules dist
	@echo "清理后端文件..."
	cd backend && rm -rf venv __pycache__ .pytest_cache
	@echo "清理 C++ 文件..."
	cd cpp-server && rm -rf build
	@echo "清理 Docker 文件..."
	docker-compose down -v
	docker system prune -f

# 启动 Docker 服务
docker-up:
	docker-compose up -d
	@echo "Docker 服务已启动"

# 停止 Docker 服务
docker-down:
	docker-compose down
	@echo "Docker 服务已停止"

# 查看服务日志
logs:
	docker-compose logs -f

# 格式化代码
format:
	@echo "格式化前端代码..."
	cd frontend && npm run format
	@echo "格式化后端代码..."
	cd backend && source venv/bin/activate && black . && isort .
	@echo "格式化 C++ 代码..."
	cd cpp-server && clang-format -i src/**/*.cpp src/**/*.h

# 代码检查
lint:
	@echo "检查前端代码..."
	cd frontend && npm run lint
	@echo "检查后端代码..."
	cd backend && source venv/bin/activate && flake8 . && mypy .
	@echo "检查 C++ 代码..."
	cd cpp-server && cppcheck --enable=all src/

# 数据库操作
db-migrate:
	@echo "运行数据库迁移..."
	docker-compose exec mysql mysql -u doodlesketch -pdoodlesketch123 doodlesketchai < scripts/init.sql

db-reset:
	@echo "重置数据库..."
	docker-compose exec mysql mysql -u root -prootpassword -e "DROP DATABASE IF EXISTS doodlesketchai; CREATE DATABASE doodlesketchai;"
	make db-migrate

# 模型下载
download-models:
	@echo "下载 AI 模型..."
	mkdir -p cpp-server/models
	# U2Net 模型
	wget -O cpp-server/models/u2net.pth https://github.com/xuebinqin/U-2-Net/releases/download/v1.0/u2net.pth
	# 简笔画生成模型 (示例)
	# wget -O cpp-server/models/sketch_model.onnx [模型URL]

# 生产部署
deploy:
	@echo "部署到生产环境..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# 开发环境快速启动
quick-start: install docker-up
	@echo "等待服务启动..."
	sleep 15
	@echo "运行数据库迁移..."
	make db-migrate
	@echo "下载 AI 模型..."
	make download-models
	@echo "开发环境已就绪！"
	@echo "前端: http://localhost:3000"
	@echo "后端 API: http://localhost:8000"
	@echo "API 文档: http://localhost:8000/docs"
