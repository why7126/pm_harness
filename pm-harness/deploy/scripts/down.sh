#!/usr/bin/env bash
# 文档用途：按部署域停止 Docker Compose

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DOMAIN="${1:-local}"
PROJECT_NAME="${COMPOSE_PROJECT_NAME:-pm-harness}"

case "${DOMAIN}" in
  local)
    COMPOSE_FILE="${ROOT_DIR}/docker-compose.yml"
    ;;
  prod)
    COMPOSE_FILE="${ROOT_DIR}/docker-compose.prod.yml"
    ;;
  *)
    echo "未知部署域：${DOMAIN}" >&2
    echo "可用部署域：local, prod" >&2
    exit 2
    ;;
esac

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  echo "BLOCKED: Compose 文件不存在：${COMPOSE_FILE}" >&2
  exit 1
fi

docker compose --project-name "${PROJECT_NAME}" --profile docs-site -f "${COMPOSE_FILE}" down --remove-orphans
echo "${DOMAIN} 域服务已停止。外部数据库、对象存储和 data/ 目录由对应环境策略保留。"
