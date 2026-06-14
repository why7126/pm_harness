---
purpose: 部署文档
content: 部署组件、环境变量和运行方式
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# 部署说明


## 部署组件

- FastAPI 应用服务
- SQLite 数据库文件
- MinIO 对象存储
- Web 静态资源

## 环境变量

参考 `.env.example`。

## Docker Compose 部署方案

本项目默认支持 Docker Compose 本地开发与演示部署。

### 服务组成

| 服务 | 容器名 | 端口 | 说明 |
|---|---|---|---|
| backend | tile-info-backend | 8000 | FastAPI 后端服务 |
| web | tile-info-web | 3000 | React Web 展示端与管理端 |
| minio | tile-info-minio | 9000 / 9001 | 对象存储与控制台 |

### 启动命令

```bash
./scripts/docker-up.sh
```

### 停止命令

```bash
./scripts/docker-down.sh
```

### 数据持久化

- SQLite 数据文件挂载到 `./data/sqlite/`。
- MinIO 数据使用 Docker Volume：`minio-data`。

### 配置文件

| 文件 | 作用 |
|---|---|
| `docker-compose.yml` | 服务编排 |
| `src/backend/Dockerfile` | 后端镜像构建 |
| `src/backend/.env.docker` | 后端Docker环境变量 |
| `src/web/Dockerfile` | Web镜像构建 |
| `src/web/nginx.conf` | Web静态资源与API代理配置 |

### 注意事项

- 本地默认 MinIO 账号密码仅用于开发环境。
- 生产环境必须更换密钥，并使用安全的配置管理方式。
- SQLite 适合轻量级部署；如后续切换数据库，必须创建 OpenSpec Change。


## V4 环境变量与数据目录

初始化本地环境：

```bash
cp .env.example .env
./scripts/docker-up.sh
```

Docker Compose 会使用：

```text
.env.example
src/backend/.env.docker
data/sqlite/
data/uploads/
data/processed/
data/tmp/
```

生产环境不得直接使用示例密钥，必须通过部署平台注入真实环境变量。

## Docker Compose 端口策略

默认开发端口：

```text
Backend: 8000
Web: 3000
MinIO API: 9000
MinIO Console: 9001
```

采用：

```text
容器内部端口固定
宿主机端口通过 .env 配置
```

示例：

```env
HOST_PORT_BACKEND=18080
HOST_PORT_WEB=13000
```

## MinIO 单桶策略

使用一个项目一个 Bucket：

```env
MINIO_BUCKET=tile-info-platform
```

并在桶内通过前缀区分：

```text
original/
thumbnails/
processed/
videos/
videos/covers/
videos/transcoded/
```
