---
purpose: 端口管理规范
content: 规范开发端口、Docker 端口、宿主机映射、环境变量、冲突处理、服务拓扑和 AI 更新规则
source: Harness port-management.md 抽象模板，基于多项目端口治理规则沉淀
update_method: 项目初始化时按用户输入生成；新增服务、修改监听端口、调整 Docker Compose、部署拓扑或网关路由时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
note: 适用于 {PRODUCT_NAME} 项目；默认采用“容器内固定、宿主机可变”的端口策略
template_scope: 可作为工程初始化的 port-management.md 模块
---

# 端口管理规范

## 0. 规则定位 [通用]

本文档用于约束 `{PRODUCT_NAME}` 项目的服务端口、Docker 端口映射、环境变量、冲突处理和 AI 更新规则，避免：

- 为了规避冲突随意修改应用内部监听端口。
- 同一端口在多个服务或多个 compose 文件中重复占用。
- 只修改 `docker-compose.yml`，没有同步 `.env.example`、README、部署文档。
- 前后端、OpenAPI、客户端生成、网关路径使用不一致的地址。
- 本地开发、完整部署、私有化部署的端口规则混淆。

### 0.1 初始化占位符 [通用]

| 占位符 | 含义 | 生成要求 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品中文名 | 来自用户输入 |
| `{PRODUCT_CODE}` | 项目代码名 | kebab-case |
| `{SERVICE_PORT_MATRIX}` | 服务端口矩阵 | 按实际服务生成 |
| `{BACKEND_PORT}` | 后端容器监听端口 | 默认可为 `8000`，按技术栈生成 |
| `{WEB_PORT}` | Web 容器/开发端口 | 默认可为 `3000` 或框架默认 |
| `{GATEWAY_PORT}` | 网关端口 | 按部署模式生成 |
| `{DATABASE_PORT}` | 数据库端口 | 按 `{DATABASE_STACK}` 生成 |
| `{OBJECT_STORAGE_PORTS}` | 对象存储端口 | MinIO/S3 兼容等按需生成 |
| `{ALGORITHM_PORT}` | 算法服务端口 | 有算法服务时生成 |
| `{DEPLOYMENT_PORT_MATRIX}` | 部署端口矩阵 | Docker Compose、K8s、私有化等 |
| `{PORT_ENV_VARS}` | 宿主机端口环境变量 | 如 `HOST_PORT_BACKEND` |
| `{PORT_CHECK_COMMAND}` | 端口校验命令 | 未知写 `待确认` |

生成初始化工程时，必须替换所有占位符；未知项写 `待确认`，不得保留样例项目的端口或服务名。

## 1. 文档模块分类 [通用]

- `[通用]`：所有 Harness 工程默认保留。
- `[个性化]`：根据产品形态、技术栈、服务数量、部署方式生成。
- `[条件启用]`：仅在对应服务启用时保留，例如 Web、数据库、Redis、对象存储、算法、工作流、网关、HTTPS。

未启用的服务不得出现在“必须占用端口”的矩阵中。

## 2. 总体策略 [通用]

默认端口策略：

```text
容器内固定，宿主机可变
```

含义：

- 应用内部监听端口保持稳定，便于服务发现、容器网络、健康检查和文档一致。
- 宿主机映射端口可通过 `.env`、`.env.local`、Docker Compose override 或部署平台配置调整。
- 遇到本地端口冲突，优先修改宿主机映射端口，不修改应用内部监听端口。
- 端口变更必须同步环境变量示例、部署文档、README 和相关规则。

## 3. 默认端口矩阵 [通用 + 个性化]

初始化时生成项目端口矩阵：

```text
{SERVICE_PORT_MATRIX}
```

推荐格式：

| 服务 | 容器/应用端口 | 默认宿主机端口 | 环境变量 | 启用条件 | 说明 |
|---|---:|---:|---|---|---|
| Backend API | `{BACKEND_PORT}` | `{BACKEND_PORT}` | `HOST_PORT_BACKEND` | 必有 | 后端 API |
| Web | `{WEB_PORT}` | `{WEB_PORT}` | `HOST_PORT_WEB` | 有 Web | 前端开发或静态服务 |
| Gateway | `{GATEWAY_PORT}` | `{GATEWAY_PORT}` | `HOST_PORT_GATEWAY` | 有网关 | API 网关 / 反向代理 |
| Database | `{DATABASE_PORT}` | 待确认 | `HOST_PORT_DATABASE` | 有数据库服务 | 本地数据库 |
| Redis | `6379` | 待确认 | `HOST_PORT_REDIS` | 有缓存/队列 | 本地 Redis |
| Object Storage API | 待确认 | 待确认 | `HOST_PORT_STORAGE_API` | 有对象存储 | MinIO/S3 兼容 API |
| Object Storage Console | 待确认 | 待确认 | `HOST_PORT_STORAGE_CONSOLE` | 有对象存储控制台 | 本地开发 |
| Algorithm API | `{ALGORITHM_PORT}` | 待确认 | `HOST_PORT_ALGORITHM` | 有算法服务 | 推理/算法 API |
| Workflow | 待确认 | 待确认 | `HOST_PORT_WORKFLOW` | 有工作流服务 | 异步工作流 |

项目没有对应服务时，删除该行或标记 `未启用`。

## 4. 端口分层 [通用 + 个性化]

| 层级 | 示例 | 规则 |
|---|---|---|
| 应用监听端口 | 后端监听 `8000` | 由应用配置控制，默认不随冲突修改 |
| 容器端口 | Dockerfile/Compose 内部端口 | 与应用监听端口一致或明确映射 |
| 宿主机映射端口 | `HOST_PORT_BACKEND=18080` | 可变，用于规避本地冲突 |
| 网关端口 | `80`/`443`/自定义 | 由部署方式决定 |
| 外部访问端口 | 公网/内网入口 | 生产由部署平台管理 |

端口冲突只应优先调整“宿主机映射端口”或“外部访问端口”，不要随意调整应用监听端口。

## 5. 环境变量映射 [通用 + 个性化]

端口环境变量：

```text
{PORT_ENV_VARS}
```

推荐示例：

```env
HOST_PORT_BACKEND=8000
HOST_PORT_WEB=3000
HOST_PORT_GATEWAY=8080
HOST_PORT_DATABASE=5432
HOST_PORT_REDIS=6379
HOST_PORT_STORAGE_API=9000
HOST_PORT_STORAGE_CONSOLE=9001
```

规则：

- 宿主机端口变量统一使用 `HOST_PORT_<SERVICE>`。
- 应用内部监听端口可使用 `<SERVICE>_PORT`，但不得与宿主机端口混淆。
- `.env.example` 必须说明每个端口变量的用途。
- Docker Compose 中的端口映射应优先引用环境变量。

示例：

```yaml
ports:
  - "${HOST_PORT_BACKEND:-8000}:8000"
```

左侧是宿主机端口，可变；右侧是容器端口，原则上不变。

## 6. Docker Compose 规则 [条件启用]

启用 Docker Compose 时：

- `ports` 映射必须优先使用环境变量。
- 同一 compose 文件内不得映射重复宿主机端口。
- 多个 compose 文件可能同时启动时，必须设计不同宿主机端口或明确禁止同时启动。
- `expose` 仅用于容器内部网络，不代表宿主机可访问。
- 修改端口时必须同步 `.env.example`、README、`docs/02-deployment.md`。

根目录开发编排与完整本地部署如同时存在，应分别维护端口矩阵：

```text
{DEPLOYMENT_PORT_MATRIX}
```

## 7. 前后端与 API 地址 [条件启用]

有前端、OpenAPI 客户端或 SDK 时：

- 前端 API Base URL 必须与后端宿主机端口或网关端口一致。
- OpenAPI 生成配置不得硬编码过期端口。
- 本地开发、Docker、生产的 API 地址必须区分。
- 前端公开环境变量中的端口必须同步 `rules/environment.md`。

常见变量：

```env
VITE_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

具体前缀根据前端技术栈生成。

## 8. 数据库、缓存与中间件端口 [条件启用]

启用数据库、Redis、消息队列、对象存储等中间件时：

- 容器内部默认端口可沿用官方默认。
- 宿主机端口可根据冲突情况调整。
- 生产环境不一定暴露中间件端口到公网或宿主机。
- 仅本地调试需要暴露的端口应在文档中说明。

示例：

| 服务 | 容器端口 | 宿主机端口 | 是否生产暴露 |
|---|---:|---:|---:|
| PostgreSQL | `5432` | 待确认 | 否 |
| MySQL | `3306` | 待确认 | 否 |
| Redis | `6379` | 待确认 | 否 |
| MinIO API | `9000` | 待确认 | 视部署 |
| MinIO Console | `9001` | 待确认 | 否 |

## 9. 多部署模式端口 [条件启用]

按 `{DEPLOYMENT_PORT_MATRIX}` 生成：

| 部署模式 | 端口规则 |
|---|---|
| 本地开发 | 可直接暴露后端、前端、中间件端口 |
| Docker Compose | 容器内固定，宿主机通过 `.env` 调整 |
| Kubernetes | Service/Ingress 管理端口，Pod 内端口固定 |
| SaaS | 外部入口由网关/负载均衡控制 |
| 私有化部署 | 需避免客户环境端口冲突，支持端口覆盖 |
| HTTPS | 通常由网关/反向代理处理 `443` |

未启用的部署模式应删除或标记 `未启用`。

## 10. 端口冲突处理 [通用]

遇到端口冲突时，按顺序处理：

1. 确认冲突端口对应服务。
2. 判断冲突发生在宿主机端口还是应用内部监听端口。
3. 优先修改 `.env` 或 compose override 中的宿主机映射端口。
4. 不修改应用内部默认端口，除非 OpenSpec 或部署约束明确要求。
5. 同步更新 `.env.example`、README、部署文档、本文档。
6. 重新运行端口校验和服务启动验证。

示例：

```env
HOST_PORT_BACKEND=18080
HOST_PORT_WEB=13000
```

```yaml
ports:
  - "${HOST_PORT_BACKEND:-8000}:8000"
```

## 11. 端口校验 [通用 + 个性化]

端口校验命令：

```text
{PORT_CHECK_COMMAND}
```

推荐校验内容：

- 端口变量是否为数字。
- 端口是否在合法范围 `1-65535`。
- 同一部署模式下宿主机端口是否重复。
- Docker Compose 引用的端口变量是否存在于 `.env.example`。
- README 和部署文档中的端口是否与 compose 一致。

可选命令示例：

```bash
python scripts/validate_ports.py
```

未知命令必须写 `待确认`，不得编造。

## 12. 安全边界 [通用]

- 数据库、Redis、消息队列、对象存储控制台默认不应暴露到公网。
- 管理后台、调试端口、Metrics、Health、Profiler 必须限制访问范围。
- 生产环境公开端口应尽量收敛到网关、负载均衡或 Ingress。
- 不得把本地调试端口当作生产安全策略。
- HTTPS 端口和证书配置应在部署文档中说明。

## 13. AI 更新规则 [通用]

AI 修改以下内容时，必须检查端口同步：

| 修改内容 | 必须同步 |
|---|---|
| `docker-compose.yml` | `.env.example`、README、部署文档、本文档 |
| 新增后端服务 | 端口矩阵、环境变量、健康检查 |
| 新增前端服务 | 前端 env、README、联调说明 |
| 新增数据库/Redis/中间件 | 端口矩阵、环境变量、安全边界 |
| 新增对象存储 | `object-storage.md`、环境变量、端口矩阵 |
| 新增算法/工作流服务 | 端口矩阵、API 文档、部署文档 |
| 修改 API Base URL | 前端配置、OpenAPI 客户端、README |
| 修改网关/HTTPS | 部署文档、兼容性、安全说明 |

## 14. 禁止事项 [通用]

- 禁止为了规避冲突随意修改应用内部默认端口。
- 禁止把端口写死在多个文件中且没有统一说明。
- 禁止只更新 `docker-compose.yml` 而不更新 `.env.example`。
- 禁止修改端口后不更新 README、部署文档和本文档。
- 禁止在生产环境无保护地暴露数据库、Redis、对象存储控制台。
- 禁止保留样例项目服务名、端口矩阵或部署路径。

## 15. 初始化生成建议 [通用]

将本文档作为工程初始化模块时，生成器应按以下步骤处理：

1. 根据 `{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}` 生成 `{SERVICE_PORT_MATRIX}`。
2. 根据是否启用 Web、数据库、Redis、对象存储、算法、工作流、网关裁剪端口矩阵。
3. 根据 Docker Compose、Kubernetes、SaaS、私有化等部署模式生成 `{DEPLOYMENT_PORT_MATRIX}`。
4. 生成 `{PORT_ENV_VARS}`，并确保与 `.env.example`、`docker-compose.yml` 一致。
5. 根据实际脚本生成 `{PORT_CHECK_COMMAND}`；未知写 `待确认`。
6. 删除未启用服务的强制端口、环境变量和安全要求。
7. 检查本文档与 `environment.md`、`object-storage.md`、`compatibility.md`、`security.md`、`docs/02-deployment.md`、README 一致。

## 16. 完成任务后检查清单 [通用]

```text
□ 端口策略明确为“容器内固定，宿主机可变”
□ [通用]、[个性化]、[条件启用] 模块标识完整
□ 服务端口矩阵只包含已启用服务
□ 宿主机端口环境变量与 .env.example 一致
□ Docker Compose 左侧/右侧端口含义说明清楚
□ 冲突处理优先修改宿主机映射端口
□ 安全边界覆盖数据库、缓存、中间件、对象存储控制台
□ AI 更新规则覆盖 compose、env、README、部署文档
□ 未保留样例项目端口矩阵或不适用服务
```
