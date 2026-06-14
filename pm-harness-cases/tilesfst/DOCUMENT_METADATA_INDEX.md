---
purpose: 文档治理
content: 文档元数据说明
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# 文档元数据索引


本项目 Markdown 文档均使用 Obsidian YAML Frontmatter 记录：

- `purpose`：文档用途
- `content`：文档内容
- `source`：内容来源
- `update_method`：更新方式
- `note`：备注

配置文件和脚本文件使用注释形式记录元数据，避免破坏语法。

## V2 新增文档与配置

| 路径 | 文档用途 | 内容来源 | 更新方式 |
|---|---|---|---|
| `docker-compose.yml` | Docker Compose部署编排 | AI自动生成，人工确认 | 服务拓扑变化时更新 |
| `src/backend/Dockerfile` | 后端镜像构建 | AI自动生成，人工确认 | 后端依赖或启动方式变化时更新 |
| `src/backend/.env.docker` | Docker后端环境变量 | AI自动生成，人工确认 | 部署配置变化时更新 |
| `src/web/Dockerfile` | Web镜像构建 | AI自动生成，人工确认 | 前端构建方式变化时更新 |
| `src/web/nginx.conf` | Web容器Nginx配置 | AI自动生成，人工确认 | API代理或路由策略变化时更新 |
| `rules/directory-structure.md` | 目录结构约束规范 | AI自动生成，人工确认 | 目录结构调整时更新 |
| `scripts/validate-directory-structure.py` | 目录结构校验脚本 | AI自动生成，人工确认 | 目录规范变化时更新 |
| `scripts/docker-up.sh` | Docker环境启动脚本 | AI自动生成，人工确认 | Compose服务变化时更新 |
| `scripts/docker-down.sh` | Docker环境停止脚本 | AI自动生成，人工确认 | Compose服务变化时更新 |


## V4新增文档

| 路径 | 文档用途 | 内容来源 | 更新方式 |
|---|---|---|---|
| `.env.example` | 环境变量示例 | AI自动生成，人工确认 | 配置变化时同步更新 |
| `data/README.md` | 数据目录说明 | AI自动生成，人工确认 | 新增数据类型或上传流程时更新 |
| `rules/data-management.md` | 数据治理规范 | AI自动生成，人工确认 | 数据目录、样例数据、运行时数据规则变化时更新 |
| `rules/environment.md` | 环境变量治理规范 | AI自动生成，人工确认 | 新增环境变量时更新 |
| `rules/media.md` | 图片/视频/文档媒体规范 | AI自动生成，人工确认 | 媒体能力变化时更新 |
| `docs/06-video-asset-management.md` | 视频资产管理说明 | AI自动生成，人工确认 | 视频上传、封面、转码、展示变化时更新 |
| `openspec/specs/media-assets/spec.md` | 媒体资产正式规范 | AI自动生成，人工确认 | 媒体相关Change归档后更新 |

## V5 新增/更新文档

| 文档 | 用途 | 更新说明 |
|---|---|---|
| `.env.example` | 环境变量示例 | 新增 HOST_PORT_* 与单 Bucket 前缀配置 |
| `rules/object-storage.md` | 对象存储规范 | 规定 MinIO 单桶 + 前缀策略 |
| `rules/port-management.md` | 端口管理规范 | 规定容器内固定、宿主机可配置策略 |
| `docs/07-object-storage-strategy.md` | 对象存储策略说明 | 说明为何采用单桶策略 |
| `openspec/specs/media-assets/spec.md` | 媒体资源正式规范 | 明确单桶与视频前缀行为 |
