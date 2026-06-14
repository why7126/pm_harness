---
purpose: Docker 基线说明
content: Compose 服务、脚本与目录约定
source: initialize-project / project.yaml
update_method: 部署架构变更时同步更新
---

# Docker 基线

本项目采用根目录 `docker-compose.yml` + 各服务 Dockerfile 的 Compose 部署模式。

## 服务

| 服务 | 镜像/构建 | 端口（宿主机默认） |
|------|-----------|-------------------|
| backend | `src/backend/Dockerfile` | 8000 |
| web | `src/web/Dockerfile` + nginx | 3000 |
| minio | `minio/minio` | 9000 / 9001 |
| minio-init | `minio/mc` | — |

## 脚本

```bash
./scripts/docker-up.sh
./scripts/docker-down.sh
```

## 环境变量

见根目录 `.env.example`；运行时复制为 `.env`（禁止提交）。

## 数据卷

```text
data/sqlite
data/minio
data/uploads
data/processed
data/tmp
```

## 文档

- `docs/02-deployment.md`
- `docker-compose.yml`

## 说明

按 `rules/directory-structure.md`，不在根目录新增 `docker/` 业务目录；Compose 与 Dockerfile 位置见上表。
