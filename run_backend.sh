#!/bin/bash

# PRE系统后端启动脚本
# 功能：自动检查环境、初始化数据库、并启动 FastAPI 服务

# 1. 配置信息
BACKEND_DIR="/Users/shaiweiminglei/pre_system/pre_backend"
HOST="127.0.0.1"
PORT=8000

echo "🚀 正在准备启动 PRE 系统后端..."

# 2. 进入目录
cd "$BACKEND_DIR" || { echo "❌ 找不到后端目录: $BACKEND_DIR"; exit 1; }

# 3. 检查端口占用并清理
EXISTING_PID=$(lsof -ti :$PORT)
if [ -n "$EXISTING_PID" ]; then
    echo "⚠️  端口 $PORT 已被占用 (PID: $EXISTING_PID)，正在清理..."
    kill -9 "$EXISTING_PID"
    sleep 1
fi

# 4. 检查 Python 依赖 (如果需要)
# python3 -m pip install -r requirements.txt --quiet

# 5. 启动服务
echo "✅ 环境就绪，正在启动服务于 http://$HOST:$PORT ..."
echo "📝 日志将实时输出在当前终端，按 CTRL+C 可停止服务。"
echo "------------------------------------------------------"

# 使用 python3 直接运行 main.py (内部已配置 uvicorn)
python3 main.py
