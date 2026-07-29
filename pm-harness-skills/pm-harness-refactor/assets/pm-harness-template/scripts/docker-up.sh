#!/usr/bin/env bash
# 文档用途：启动Docker Compose开发环境
# 文档内容：构建并启动后端、Web、MinIO
# 内容来源：AI自动生成，项目团队确认
# 更新方式：compose服务变化时更新
# 备注：执行前请确保已安装Docker和Docker Compose

set -euo pipefail

docker compose up -d --build

echo "服务已启动："
echo "- Web: http://localhost:3000"
echo "- Backend API: http://localhost:8000/docs"
echo "- MinIO Console: http://localhost:9001"
