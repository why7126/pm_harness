---
purpose: 端口管理规范
content: 说明开发端口、Docker 端口、冲突处理、AI 更新规则
source: Harness Token 优化模板
update_method: 服务端口或部署拓扑变化时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-14 00:00:00
note: 推荐“容器内固定、宿主机可变”的端口策略
---

# 端口管理规范

## 1. 默认端口

项目初始化后必须在 `.env.example` 和 `docs/02-deployment.md` 中明确默认端口。推荐变量：

```env
HOST_PORT_BACKEND=18080
HOST_PORT_WEB=13000
```

## 2. 端口冲突处理

不要为规避本机冲突随意修改应用内部监听端口，优先修改 `.env` 中宿主机映射端口。

Docker Compose 中左侧是宿主机端口，可变；右侧是容器端口，原则上保持稳定。

## 3. AI 禁止行为

- 禁止为了规避冲突随意修改应用内部默认端口。
- 禁止把端口写死在多个文件中。
- 禁止只更新 docker-compose 而不更新 `.env.example`。
- 禁止修改端口后不更新 README 和部署文档。
