---
purpose: 环境变量管理规范
content: .env.example维护、环境变量命名、安全边界、Docker Compose环境同步规则
source: AI自动生成初稿，项目团队确认
update_method: 新增服务、端口、密钥、第三方配置、对象存储、数据库或视频处理参数时更新
note: .env.example 可提交，.env 禁止提交
---

# 环境变量管理规范

## 1. 基本原则

- 根目录必须提供 `.env.example`。
- 真实 `.env` 文件禁止提交Git。
- 新增任何环境变量时，必须同步更新 `.env.example`。
- Docker Compose 使用的变量必须在 `.env.example` 中有说明。
- 不允许在代码、文档示例、测试中写入真实密钥。

## 2. 命名规范

环境变量使用大写蛇形命名：

```text
SERVICE_NAME_CONFIG_NAME
```

示例：

```text
MINIO_BUCKET_TILE_IMAGES
MAX_VIDEO_SIZE_MB
VITE_API_BASE_URL
```

## 3. AI更新规则

AI修改以下内容时，必须检查 `.env.example`：

- `docker-compose.yml`
- `src/backend/.env.example`
- `src/backend/.env.docker`
- `src/web/package.json`
- `src/web/orval.config.ts`
- MinIO存储桶
- SQLite数据库路径
- 上传大小限制
- 视频处理配置

## 4. 安全要求

- `.env.example` 只能包含示例值。
- 密码必须使用明显的示例值，不得伪装成真实密码。
- 生产环境密钥应通过部署平台或密钥管理系统注入。
