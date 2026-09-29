#!/usr/bin/env bash
# 文档用途：按部署域与环境 ID 启动 Docker Compose
# 更新方式：新增部署环境时同步更新 case 映射和 README

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DOMAIN="${1:-local}"
ENVIRONMENT="${2:-default}"
COMPOSE_PROFILES=()

case "${DOMAIN}:${ENVIRONMENT}" in
  local:default)
    ENV_FILE="${ROOT_DIR}/deploy/local/default.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/local/default.env.example"
    COMPOSE_FILE="${ROOT_DIR}/docker-compose.yml"
    ;;
  prod:external)
    ENV_FILE="${ROOT_DIR}/deploy/prod/external.env"
    EXAMPLE_FILE="${ROOT_DIR}/deploy/prod/external.env.example"
    COMPOSE_FILE="${ROOT_DIR}/docker-compose.prod.yml"
    COMPOSE_PROFILES=("docs-site")
    ;;
  *)
    echo "未知部署环境：${DOMAIN} ${ENVIRONMENT}" >&2
    echo "请查看 deploy/README.md 获取可用环境 ID。" >&2
    exit 2
    ;;
esac

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  echo "BLOCKED: Compose 文件不存在：${COMPOSE_FILE}" >&2
  echo "请先为 ${DOMAIN}-${ENVIRONMENT} 补齐 Compose，或更新 deploy/scripts/up.sh 映射。" >&2
  exit 1
fi

if [[ ! -f "${ENV_FILE}" ]]; then
  ENV_FILE="${EXAMPLE_FILE}"
  echo "未找到真实 env，使用示例文件进行启动/校验：${ENV_FILE}"
  echo "需要真实部署时请复制为去掉 .example 的 env 文件并替换占位值。"
fi

python "${ROOT_DIR}/deploy/scripts/validate-env.py" --domain "${DOMAIN}" --environment "${ENVIRONMENT}" --env-file "${ENV_FILE}"

PROJECT_NAME="${COMPOSE_PROJECT_NAME:-pm-harness}"
COMPOSE_ARGS=(--project-name "${PROJECT_NAME}" --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}")
for COMPOSE_PROFILE in "${COMPOSE_PROFILES[@]}"; do
  COMPOSE_ARGS=(--profile "${COMPOSE_PROFILE}" "${COMPOSE_ARGS[@]}")
done

export PM_HARNESS_DEPLOY_ENV_FILE="${ENV_FILE}"
docker compose "${COMPOSE_ARGS[@]}" up -d --build

HOST_PORT_WEB="$(grep -E '^HOST_PORT_WEB=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
HOST_PORT_BACKEND="$(grep -E '^HOST_PORT_BACKEND=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
HOST_PORT_MINTLIFY_DOCS="$(grep -E '^HOST_PORT_MINTLIFY_DOCS=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
HOST_PORT_WEB="${HOST_PORT_WEB:-3000}"
HOST_PORT_BACKEND="${HOST_PORT_BACKEND:-8000}"
HOST_PORT_MINTLIFY_DOCS="${HOST_PORT_MINTLIFY_DOCS:-3001}"

echo "服务已启动："
echo "- Environment: ${DOMAIN}-${ENVIRONMENT}"
echo "- Web: http://localhost:${HOST_PORT_WEB}"
echo "- Backend API: http://localhost:${HOST_PORT_BACKEND}/docs"
echo "- Docs Site: http://localhost:${HOST_PORT_MINTLIFY_DOCS}"
