---
purpose: 端口管理规范
content: 说明开发端口、Docker端口、冲突处理、AI更新规则
source: 人工编写 + AI辅助生成
update_method: 服务端口或部署拓扑变化时更新
note: V5 采用“容器内固定、宿主机可变”的端口策略
---

# 端口管理规范

## 1. 默认端口

```text
Backend: 8000
Web: 3000
MinIO API: 9000
MinIO Console: 9001
```

保留 8000 和 3000 的原因：

- FastAPI 和前端开发生态常用，开发体验好；
- 新成员更容易理解；
- OpenAPI、Orval、前后端联调配置更简单。

## 2. 端口冲突处理

不要改应用内部监听端口，优先修改 `.env` 中宿主机映射端口：

```env
HOST_PORT_BACKEND=18080
HOST_PORT_WEB=13000
```

Docker Compose 中左侧是宿主机端口，可变；右侧是容器端口，原则上不变。

## 3. AI禁止行为

- 禁止为了规避冲突随意修改应用内部默认端口；
- 禁止把端口写死在多个文件中；
- 禁止只更新 docker-compose 而不更新 `.env.example`；
- 禁止修改端口后不更新 README 和部署文档。
