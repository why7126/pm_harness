#!/usr/bin/env bash
# 文档用途：停止Docker Compose开发环境
# 文档内容：停止后端、Web、MinIO服务
# 内容来源：AI自动生成，项目团队确认
# 更新方式：compose服务变化时更新
# 备注：默认不删除卷数据

set -euo pipefail

docker compose down
