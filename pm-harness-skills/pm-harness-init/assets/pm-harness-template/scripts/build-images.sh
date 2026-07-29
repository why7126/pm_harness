#!/usr/bin/env bash
# 文档用途：构建生产 Docker 镜像与可选离线镜像包
# 文档内容：从 env 文件读取镜像 tag、平台、builder 与导出目录
# 内容来源：add-image-build-script-env
# 更新方式：镜像构建参数、Dockerfile 路径或交付包格式变化时同步更新
# 备注：默认读取 scripts/build-images.env；可通过第一个参数指定其他 env 文件

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEFAULT_ENV_FILE="${PROJECT_ROOT}/scripts/build-images.env"
ENV_FILE="${1:-${DEFAULT_ENV_FILE}}"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "未找到构建配置：${ENV_FILE}" >&2
  echo "请先执行：cp scripts/build-images.env.example scripts/build-images.env" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +a

IMAGE_BUILD_TAG="${IMAGE_BUILD_TAG:-v0.0.1}"
IMAGE_BUILD_PLATFORM="${IMAGE_BUILD_PLATFORM:-linux/amd64}"
BACKEND_PYTHON_BASE_IMAGE="${BACKEND_PYTHON_BASE_IMAGE:-python:3.12-slim}"
WEB_NODE_BASE_IMAGE="${WEB_NODE_BASE_IMAGE:-node:22-alpine}"
WEB_NGINX_BASE_IMAGE="${WEB_NGINX_BASE_IMAGE:-nginx:1.27-alpine}"
IMAGE_BUILD_BACKEND_IMAGE="${IMAGE_BUILD_BACKEND_IMAGE:-pm-harness-backend}"
IMAGE_BUILD_WEB_IMAGE="${IMAGE_BUILD_WEB_IMAGE:-pm-harness-web}"
IMAGE_BUILD_BUILDER="${IMAGE_BUILD_BUILDER:-pm-harness-builder}"
IMAGE_BUILD_CREATE_BUILDER="${IMAGE_BUILD_CREATE_BUILDER:-true}"
IMAGE_BUILD_LOAD="${IMAGE_BUILD_LOAD:-true}"
IMAGE_BUILD_EXPORT_TAR="${IMAGE_BUILD_EXPORT_TAR:-true}"
IMAGE_BUILD_RELEASE_DIR="${IMAGE_BUILD_RELEASE_DIR:-${PROJECT_ROOT}/releases/${IMAGE_BUILD_TAG}}"
IMAGE_BUILD_TAR_NAME="${IMAGE_BUILD_TAR_NAME:-pm-harness-${IMAGE_BUILD_TAG}-${IMAGE_BUILD_PLATFORM//\//-}.tar.gz}"

BACKEND_REF="${IMAGE_BUILD_BACKEND_IMAGE}:${IMAGE_BUILD_TAG}"
WEB_REF="${IMAGE_BUILD_WEB_IMAGE}:${IMAGE_BUILD_TAG}"
TAR_PATH="${IMAGE_BUILD_RELEASE_DIR}/images/${IMAGE_BUILD_TAR_NAME}"

require_command() {
  local command_name="$1"
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "缺少命令：${command_name}" >&2
    exit 1
  fi
}

ensure_builder() {
  docker buildx version >/dev/null

  if [[ "${IMAGE_BUILD_CREATE_BUILDER}" == "true" ]]; then
    if docker buildx inspect "${IMAGE_BUILD_BUILDER}" >/dev/null 2>&1; then
      docker buildx use "${IMAGE_BUILD_BUILDER}" >/dev/null
    else
      docker buildx create --name "${IMAGE_BUILD_BUILDER}" --driver docker-container --use >/dev/null
    fi
    docker buildx inspect --bootstrap >/dev/null
  fi
}

build_load_flag() {
  if [[ "${IMAGE_BUILD_LOAD}" == "true" ]]; then
    printf '%s' "--load"
  fi
}

inspect_platform() {
  local image_ref="$1"
  docker image inspect "${image_ref}" --format '{{.Os}}/{{.Architecture}}'
}

assert_platform() {
  local image_ref="$1"
  local actual_platform
  actual_platform="$(inspect_platform "${image_ref}")"
  if [[ "${actual_platform}" != "${IMAGE_BUILD_PLATFORM}" ]]; then
    echo "镜像平台不匹配：${image_ref} actual=${actual_platform} expected=${IMAGE_BUILD_PLATFORM}" >&2
    exit 1
  fi
}

write_checksum() {
  local file_path="$1"
  local file_dir
  local file_name
  file_dir="$(dirname "${file_path}")"
  file_name="$(basename "${file_path}")"

  if command -v shasum >/dev/null 2>&1; then
    (cd "${file_dir}" && shasum -a 256 "${file_name}") > "${file_path}.sha256"
    return
  fi
  if command -v sha256sum >/dev/null 2>&1; then
    (cd "${file_dir}" && sha256sum "${file_name}") > "${file_path}.sha256"
    return
  fi
  echo "缺少命令：shasum 或 sha256sum" >&2
  exit 1
}

cd "${PROJECT_ROOT}"

require_command docker
require_command gzip

echo "镜像构建配置："
echo "- env: ${ENV_FILE}"
echo "- platform: ${IMAGE_BUILD_PLATFORM}"
echo "- backend: ${BACKEND_REF}"
echo "- web: ${WEB_REF}"
echo "- backend base image: ${BACKEND_PYTHON_BASE_IMAGE}"
echo "- web node base image: ${WEB_NODE_BASE_IMAGE}"
echo "- web nginx base image: ${WEB_NGINX_BASE_IMAGE}"
echo "- builder: ${IMAGE_BUILD_BUILDER}"
echo "- export tar: ${IMAGE_BUILD_EXPORT_TAR}"
echo "- release dir: ${IMAGE_BUILD_RELEASE_DIR}"

ensure_builder

LOAD_FLAG="$(build_load_flag)"
if [[ -z "${LOAD_FLAG}" ]]; then
  echo "IMAGE_BUILD_LOAD=false 时无法执行本地镜像验证和离线包导出。" >&2
  echo "请保持 IMAGE_BUILD_LOAD=true，或手动扩展脚本支持 push-only 流程。" >&2
  exit 1
fi

echo "构建后端镜像：${BACKEND_REF}"
docker buildx build \
  --platform "${IMAGE_BUILD_PLATFORM}" \
  --build-arg "BACKEND_PYTHON_BASE_IMAGE=${BACKEND_PYTHON_BASE_IMAGE}" \
  -t "${BACKEND_REF}" \
  -f src/backend/Dockerfile \
  "${LOAD_FLAG}" \
  src/backend

echo "构建 Web 镜像：${WEB_REF}"
docker buildx build \
  --platform "${IMAGE_BUILD_PLATFORM}" \
  --build-arg "WEB_NODE_BASE_IMAGE=${WEB_NODE_BASE_IMAGE}" \
  --build-arg "WEB_NGINX_BASE_IMAGE=${WEB_NGINX_BASE_IMAGE}" \
  -t "${WEB_REF}" \
  -f src/web/Dockerfile \
  "${LOAD_FLAG}" \
  .

echo "验证镜像平台"
assert_platform "${BACKEND_REF}"
assert_platform "${WEB_REF}"

echo "验证后端依赖"
docker run --rm --platform "${IMAGE_BUILD_PLATFORM}" "${BACKEND_REF}" \
  uv run --no-sync python -c "import fastapi, sqlalchemy, pymysql, minio; print('backend deps ok')"

echo "验证 Web Nginx 配置"
docker run --rm --platform "${IMAGE_BUILD_PLATFORM}" --add-host backend:127.0.0.1 "${WEB_REF}" nginx -t

if [[ "${IMAGE_BUILD_EXPORT_TAR}" == "true" ]]; then
  mkdir -p "$(dirname "${TAR_PATH}")"
  echo "导出离线镜像包：${TAR_PATH}"
  docker save "${BACKEND_REF}" "${WEB_REF}" | gzip > "${TAR_PATH}"
  write_checksum "${TAR_PATH}"
  echo "已生成校验文件：${TAR_PATH}.sha256"
fi

echo "镜像构建完成"
