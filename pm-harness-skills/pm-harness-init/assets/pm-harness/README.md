---
purpose: 项目说明
content: 项目介绍、技术栈、启动方式
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# 瓷砖信息管理平台


## 项目简介

瓷砖信息管理平台用于帮助瓷砖零售店店主了解瓷砖产品信息，并帮助企业内部员工维护瓷砖资料、规格、分类和图片。

## 用户角色

| 用户 | 使用端 | 核心目标 |
|---|---|---|
| 瓷砖零售店店主 | Web端、微信小程序 | 浏览、查询、了解瓷砖信息 |
| 企业内部员工 | 管理端Web | 维护瓷砖信息、分类、规格、图片 |

## 技术栈

### 后端

- Python3.12
- FastAPI
- Pydantic
- uv
- SQLite
- MinIO

### 前端

- React19
- TypeScript
- Tailwind
- shadcn/ui
- Axios
- Orval
- pnpm

## 快速启动

```bash
# 后端
cd src/backend
uv sync
uv run fastapi dev app/main.py

# 前端
cd src/web
pnpm install
pnpm dev
```

## 目录说明

- `openspec/`：需求与规格事实源
- `src/backend/`：FastAPI后端
- `src/web/`：Web展示端与管理端
- `src/miniapp/`：微信小程序
- `tests/`：测试目录

## Docker Compose 启动

本项目提供 Docker Compose 本地开发与演示部署方式。

```bash
./scripts/docker-up.sh
```

启动后访问：

| 服务 | 地址 |
|---|---|
| Web展示端/管理端 | http://localhost:3000 |
| 后端API文档 | http://localhost:8000/docs |
| MinIO控制台 | http://localhost:9001 |

停止服务：

```bash
./scripts/docker-down.sh
```

默认 MinIO 账号密码仅用于本地开发：

```text
账号：minioadmin
密码：minioadmin123
```

生产环境必须修改默认账号密码，并使用独立环境变量管理。

## AI目录结构约束

本项目要求 AI Agent 严格遵循当前目录结构，不允许随意新增顶层目录或将文件放到错误位置。

目录约束规则见：

```text
rules/directory-structure.md
```

目录校验命令：

```bash
python scripts/validate-directory-structure.py
```


## 新增能力

- 新增根目录 `.env.example`，统一管理本地开发、Docker Compose、MinIO、SQLite、图片/视频上传相关环境变量。
- 新增 `data/` 目录，用于本地SQLite、上传缓存、视频处理产物、样例素材和运行时数据。
- 新增 `rules/data-management.md`、`rules/environment.md`、`rules/media.md`。
- 新增 `docs/06-video-asset-management.md`。
- 新增 `openspec/specs/media-assets/spec.md`。
- 新增后端 `src/backend/app/modules/media/` 和 `src/backend/app/video/` 模块边界。

## 初始化建议

```bash
cp .env.example .env
./scripts/docker-up.sh
```

如果项目不需要视频能力，不建议直接删除目录，应先创建 OpenSpec Change 说明裁剪范围。

## V5 更新说明

### MinIO 单桶策略

将 MinIO 从多 Bucket 策略调整为：

```text
一个项目一个 Bucket
桶内通过前缀区分图片、视频、缩略图、导入导出等资源
```

默认：

```env
MINIO_BUCKET=tile-info-platform
```

### 端口策略

保留开发常用端口：

```text
Backend: 8000
Web: 3000
```

如果本机多个项目冲突，只需要在 `.env` 中修改宿主机端口：

```env
HOST_PORT_BACKEND=18080
HOST_PORT_WEB=13000
```

容器内部端口保持不变。
