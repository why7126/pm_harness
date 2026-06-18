---
purpose: 部署文档
content: 部署目标、部署组件、环境变量、端口策略、运行方式、数据持久化、安全要求、验证与回滚
source: Harness docs/02-deployment.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；部署组件、环境变量、端口、镜像、数据卷或发布方式变化时更新；后续由 AI 辅助更新并经人工 Review
owner: {DEPLOYMENT_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 docs/02-deployment.md 模块
---

# 部署说明

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如 Docker Compose、Kubernetes、对象存储、数据库服务、算法服务、私有化部署。

## 0. 文档定位 `[通用]`

本文说明 `{PRODUCT_NAME}` 的部署方式、运行组件、环境变量、端口、数据持久化、启动停止、验证、回滚和安全边界。

本文重点回答：

- 本项目有哪些运行时服务。
- 每个服务如何构建、启动、停止和健康检查。
- 环境变量来自哪里，哪些变量必须由部署平台注入。
- 数据库、对象存储、上传文件、模型文件等如何持久化。
- 部署变更后如何验证和回滚。
- AI Agent 修改部署相关文件时必须同步哪些文档和规则。

相关规则：

- 环境变量规范：`rules/environment.md`
- 端口规范：`rules/port-management.md`
- 发布与回滚：`rules/release.md`
- 安全要求：`rules/security.md`
- 数据边界：`rules/data-management.md`
- 对象存储：`rules/object-storage.md`
- 兼容性：`rules/compatibility.md`

## 1. 生成参数 `[个性化]`

初始化生成本文时，应优先使用用户输入填充以下参数。缺失信息可以标记为 `待确认`，不得编造部署事实。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{DEPLOYMENT_STACK}` | 部署方式，如 Docker Compose、Kubernetes、SaaS、私有化部署 | 待确认 |
| `{DEPLOYMENT_ENVIRONMENTS}` | 环境列表，如 local、dev、test、staging、prod | 待确认 |
| `{SERVICE_MATRIX}` | 服务、镜像、端口、依赖矩阵 | 待确认 |
| `{BACKEND_STACK}` | 后端技术栈 | 待确认 |
| `{FRONTEND_STACK}` | 前端技术栈 | 待确认 |
| `{DATABASE_STACK}` | 数据库方案 | 待确认 |
| `{OBJECT_STORAGE_STACK}` | 对象存储方案 | 待确认 |
| `{ASYNC_TASK_STACK}` | 异步任务、队列、调度系统 | 待确认 |
| `{ALGORITHM_STACK}` | 算法、模型、AI 服务栈 | 待确认 |
| `{DEPLOYMENT_OWNER}` | 部署文档负责人 | 待确认 |
| `{PRIMARY_DEPLOY_COMMAND}` | 主要部署命令 | 待确认 |
| `{PRIMARY_VERIFY_COMMAND}` | 部署后统一验证命令 | 待确认 |

## 2. 部署目标 `[通用 + 个性化]`

部署目标：

- 让 `{PRODUCT_NAME}` 在 `{DEPLOYMENT_ENVIRONMENTS}` 中可重复启动、停止、验证和回滚。
- 将服务配置、密钥、端口、数据卷和运行时文件边界显式化。
- 保证本地开发、测试、演示、预发布、生产或私有化部署之间的差异可追踪。
- 让 AI Agent 修改部署时有明确的同步文件和验证要求。

当前部署方式：

```text
{DEPLOYMENT_STACK}
```

## 3. 部署组件 `[通用 + 个性化]`

初始化时应根据 `{SERVICE_MATRIX}` 生成真实服务清单。未启用的服务必须删除。

| 服务 | 组件类型 | 镜像/构建来源 | 内部端口 | 宿主/入口端口 | 依赖 | 健康检查 | 状态 |
|---|---|---|---:|---:|---|---|---|
| `{SERVICE_NAME_1}` | `{SERVICE_TYPE_1}` | `{IMAGE_OR_BUILD_1}` | `{INTERNAL_PORT_1}` | `{HOST_OR_ENTRY_PORT_1}` | `{DEPENDENCIES_1}` | `{HEALTHCHECK_1}` | `{STATUS_1}` |
| `{SERVICE_NAME_2}` | `{SERVICE_TYPE_2}` | `{IMAGE_OR_BUILD_2}` | `{INTERNAL_PORT_2}` | `{HOST_OR_ENTRY_PORT_2}` | `{DEPENDENCIES_2}` | `{HEALTHCHECK_2}` | `{STATUS_2}` |

常见组件类型：

- Backend API / Gateway
- Web 静态资源 / SSR 服务
- Admin / Console
- Database
- Object Storage
- Cache / Search
- Worker / Scheduler
- Algorithm / Model Runtime
- Reverse Proxy / Ingress

## 4. 环境与配置文件 `[通用 + 个性化]`

| 文件/来源 | 用途 | 是否提交 Git | 备注 |
|---|---|---:|---|
| `.env.example` | 根级环境变量样例 | 是 | 不得包含真实密钥 |
| `.env` | 本地真实环境变量 | 否 | 必须加入 `.gitignore` |
| `{SERVICE_ENV_FILE}` | 服务级环境变量样例或部署配置 | `{COMMIT_POLICY}` | `{SERVICE_ENV_NOTE}` |
| `docker-compose.yml` | Docker Compose 编排 | `[条件启用]` | 启用 Compose 时保留 |
| `deploy/` | 部署编排、脚本、环境模板 | `[条件启用]` | Kubernetes、Helm、私有化等放这里 |
| CI/CD Secret | CI/CD 平台密钥 | 否 | 由平台注入 |
| 部署平台配置 | 云服务、PaaS、K8s Secret/ConfigMap | 否/按策略 | 生产密钥不得进仓库 |

环境变量规则：

- 新增或修改环境变量必须同步 `.env.example`。
- 生产环境不得直接使用示例密钥、默认密码或本地开发配置。
- 密钥、token、私钥、数据库密码、对象存储凭据必须由部署平台或本地 `.env` 注入。
- 前端公开变量必须有明确前缀和安全审查，不能暴露服务端密钥。

## 5. 环境变量矩阵 `[通用 + 个性化]`

| 变量名 | 作用 | 默认值 | 环境 | 是否敏感 | 所属服务 | 备注 |
|---|---|---|---|---:|---|---|
| `{ENV_NAME_1}` | `{ENV_PURPOSE_1}` | `{ENV_DEFAULT_1}` | `{ENVIRONMENTS_1}` | `{IS_SECRET_1}` | `{ENV_SERVICE_1}` | `{ENV_NOTE_1}` |
| `{ENV_NAME_2}` | `{ENV_PURPOSE_2}` | `{ENV_DEFAULT_2}` | `{ENVIRONMENTS_2}` | `{IS_SECRET_2}` | `{ENV_SERVICE_2}` | `{ENV_NOTE_2}` |

生成要求：

- 敏感变量默认值必须为空或使用占位符。
- 端口变量必须与 `rules/port-management.md` 一致。
- 数据库、对象存储、媒体、算法服务变量必须与对应规则一致。

## 6. 端口策略 `[通用 + 个性化]`

端口策略：

```text
{PORT_POLICY}
```

推荐原则：

- 容器或服务内部端口保持稳定。
- 本机端口冲突优先通过宿主机端口映射或环境变量解决。
- 不得为了本机临时冲突随意修改应用内部端口。
- 对外暴露端口必须经过安全审查。

| 服务 | 内部端口 | 宿主/入口端口 | 环境变量 | 暴露范围 | 说明 |
|---|---:|---:|---|---|---|
| `{SERVICE_NAME_1}` | `{INTERNAL_PORT_1}` | `{HOST_PORT_1}` | `{PORT_ENV_1}` | `{EXPOSURE_1}` | `{PORT_NOTE_1}` |
| `{SERVICE_NAME_2}` | `{INTERNAL_PORT_2}` | `{HOST_PORT_2}` | `{PORT_ENV_2}` | `{EXPOSURE_2}` | `{PORT_NOTE_2}` |

## 7. Docker Compose 部署 `[条件启用]`

当 `{DEPLOYMENT_STACK}` 包含 Docker Compose 时保留本节。

### 7.1 服务组成 `[个性化]`

| 服务 | compose service | 容器名 | 构建/镜像 | 端口 | volume | depends_on |
|---|---|---|---|---|---|---|
| `{COMPOSE_SERVICE_1}` | `{COMPOSE_KEY_1}` | `{CONTAINER_NAME_1}` | `{COMPOSE_IMAGE_1}` | `{COMPOSE_PORTS_1}` | `{COMPOSE_VOLUMES_1}` | `{COMPOSE_DEPENDS_1}` |
| `{COMPOSE_SERVICE_2}` | `{COMPOSE_KEY_2}` | `{CONTAINER_NAME_2}` | `{COMPOSE_IMAGE_2}` | `{COMPOSE_PORTS_2}` | `{COMPOSE_VOLUMES_2}` | `{COMPOSE_DEPENDS_2}` |

### 7.2 启动与停止 `[个性化]`

初始化本地环境：

```bash
{LOCAL_ENV_INIT_COMMAND}
```

启动：

```bash
{DOCKER_UP_COMMAND}
```

停止：

```bash
{DOCKER_DOWN_COMMAND}
```

查看日志：

```bash
{DOCKER_LOG_COMMAND}
```

清理本地运行数据：

```bash
{DOCKER_CLEAN_COMMAND}
```

如果命令不存在，应删除或替换，不得保留虚假命令。

### 7.3 Compose 配置文件 `[个性化]`

| 文件 | 作用 | 更新触发 |
|---|---|---|
| `docker-compose.yml` | 服务编排 | 服务、端口、volume、网络变化 |
| `{BACKEND_DOCKERFILE}` | 后端镜像构建 | 后端构建方式变化 |
| `{FRONTEND_DOCKERFILE}` | 前端镜像构建 | 前端构建方式变化 |
| `{REVERSE_PROXY_CONFIG}` | 静态资源、网关、反向代理 | 路由、域名、TLS、API 代理变化 |
| `{SERVICE_ENV_FILE}` | 容器环境变量 | 配置项变化 |

## 8. Kubernetes / Helm 部署 `[条件启用]`

当 `{DEPLOYMENT_STACK}` 包含 Kubernetes、Helm 或云原生部署时保留本节。

| 资源 | 路径 | 用途 | 备注 |
|---|---|---|---|
| Namespace | `{K8S_NAMESPACE_FILE}` | 命名空间 | `{K8S_NAMESPACE_NOTE}` |
| Deployment | `{K8S_DEPLOYMENT_PATH}` | 工作负载 | `{K8S_DEPLOYMENT_NOTE}` |
| Service | `{K8S_SERVICE_PATH}` | 服务发现 | `{K8S_SERVICE_NOTE}` |
| Ingress/Gateway | `{K8S_INGRESS_PATH}` | 外部入口 | `{K8S_INGRESS_NOTE}` |
| ConfigMap | `{K8S_CONFIGMAP_PATH}` | 非敏感配置 | `{K8S_CONFIGMAP_NOTE}` |
| Secret | `{K8S_SECRET_POLICY}` | 敏感配置 | 不得提交真实密钥 |
| PVC/StorageClass | `{K8S_STORAGE_PATH}` | 持久化存储 | `{K8S_STORAGE_NOTE}` |
| Helm Chart | `{HELM_CHART_PATH}` | 参数化部署 | `{HELM_NOTE}` |

Kubernetes 规则：

- Secret 不得以真实值提交。
- Readiness、liveness、资源限制和滚动更新策略必须明确。
- 数据库、对象存储、模型文件和上传目录必须有持久化策略。
- Ingress、TLS、域名、CORS、安全 Header 必须与安全规则一致。

## 9. SaaS / PaaS / 私有化部署 `[条件启用]`

当项目采用 SaaS、PaaS、离线包或私有化交付时保留本节。

| 部署模式 | 目标环境 | 交付物 | 配置方式 | 验证方式 | 回滚方式 |
|---|---|---|---|---|---|
| `{DEPLOYMENT_MODE_1}` | `{TARGET_ENV_1}` | `{ARTIFACTS_1}` | `{CONFIG_METHOD_1}` | `{VERIFY_METHOD_1}` | `{ROLLBACK_METHOD_1}` |
| `{DEPLOYMENT_MODE_2}` | `{TARGET_ENV_2}` | `{ARTIFACTS_2}` | `{CONFIG_METHOD_2}` | `{VERIFY_METHOD_2}` | `{ROLLBACK_METHOD_2}` |

私有化部署必须额外说明：

- 操作系统、CPU 架构、数据库、浏览器或内网环境兼容性。
- license、激活、客户侧密钥管理方式。
- 离线镜像、安装包、初始化脚本和升级脚本。
- 日志、备份、监控、巡检和故障恢复。

## 10. 数据持久化 `[通用 + 个性化]`

| 数据类型 | 存储位置 | 是否持久化 | 备份策略 | 清理策略 | 关联规则 |
|---|---|---:|---|---|---|
| 数据库数据 | `{DATABASE_STORAGE}` | 是 | `{DATABASE_BACKUP}` | `{DATABASE_CLEANUP}` | `rules/database.md` |
| 上传文件/媒体 | `{MEDIA_STORAGE}` | `{MEDIA_PERSISTENCE}` | `{MEDIA_BACKUP}` | `{MEDIA_CLEANUP}` | `rules/media.md` |
| 对象存储数据 | `{OBJECT_STORAGE_DATA}` | `{OBJECT_STORAGE_PERSISTENCE}` | `{OBJECT_STORAGE_BACKUP}` | `{OBJECT_STORAGE_CLEANUP}` | `rules/object-storage.md` |
| 本地样例数据 | `data/` | 按策略 | `{LOCAL_DATA_BACKUP}` | `{LOCAL_DATA_CLEANUP}` | `rules/data-management.md` |
| 模型文件 | `models/` 或外部挂载 | 按策略 | `{MODEL_BACKUP}` | `{MODEL_CLEANUP}` | `rules/data-management.md` |
| 日志/缓存/临时文件 | `{RUNTIME_TMP}` | 否/按策略 | `{LOG_BACKUP}` | `{TMP_CLEANUP}` | `rules/data-management.md` |

禁止提交真实生产数据、运行时数据库、真实上传素材、临时处理文件和大模型权重。

## 11. 对象存储与媒体部署 `[条件启用]`

当项目启用对象存储、文件上传或媒体能力时保留本节。

对象存储方案：

```text
{OBJECT_STORAGE_STACK}
```

Bucket / 容器策略：

```text
{BUCKET_POLICY}
```

对象 Key / 前缀策略：

```text
{OBJECT_KEY_PREFIXES}
```

部署要求：

- 本地开发和生产环境的 bucket、endpoint、access key、secret key 必须区分。
- 生产凭据必须由部署平台或 `.env` 注入，不得写入文档或仓库。
- 上传大小、MIME 类型、访问权限、签名 URL、生命周期策略必须与 `rules/media.md` 和 `rules/object-storage.md` 一致。

## 12. 数据库部署 `[条件启用]`

数据库方案：

```text
{DATABASE_STACK}
```

| 项 | 内容 |
|---|---|
| 数据库服务 | `{DATABASE_SERVICE}` |
| 连接方式 | `{DATABASE_CONNECTION}` |
| 迁移命令 | `{DATABASE_MIGRATION_COMMAND}` |
| Seed 命令 | `{DATABASE_SEED_COMMAND}` |
| 备份方式 | `{DATABASE_BACKUP_COMMAND}` |
| 回滚方式 | `{DATABASE_ROLLBACK_COMMAND}` |

数据库变更必须同步：

- `docs/04-database-design.md`
- `rules/database.md`
- `.env.example`
- 迁移脚本
- 测试 fixtures
- 兼容性说明

## 13. 算法 / 模型服务部署 `[条件启用]`

当项目启用算法、模型推理或 AI 服务时保留本节。

| 项 | 内容 |
|---|---|
| 模型服务 | `{ALGORITHM_SERVICE}` |
| 模型路径 | `{MODEL_PATH}` |
| 模型版本 | `{MODEL_VERSION}` |
| 启动命令 | `{ALGORITHM_START_COMMAND}` |
| 健康检查 | `{ALGORITHM_HEALTHCHECK}` |
| 资源要求 | `{ALGORITHM_RESOURCE_REQUIREMENTS}` |
| 降级策略 | `{ALGORITHM_FALLBACK_POLICY}` |

部署要求：

- 模型文件默认不直接提交到 Git。
- `models/README.md` 应说明获取方式、版本、校验和、许可和放置路径。
- 推理接口、输入输出、性能和失败策略必须有部署验证记录。

## 14. 部署安全 `[通用]`

部署安全规则：

- 生产环境不得使用默认账号、默认密码、示例密钥。
- `.env`、私钥、token、证书私钥、数据库密码不得提交到 Git。
- 容器或运行用户应避免 root 权限，除非有明确理由。
- 对外暴露的服务必须明确鉴权、TLS、CORS、安全 Header 和访问控制。
- 管理后台、对象存储控制台、数据库控制台等高风险入口不得默认公网暴露。
- 日志不得输出密钥、token、个人敏感信息或客户数据。

## 15. 部署验证 `[通用 + 个性化]`

部署完成后必须执行：

```bash
{PRIMARY_VERIFY_COMMAND}
```

按能力补充：

| 验证项 | 命令/方式 | 期望结果 |
|---|---|---|
| 服务启动 | `{SERVICE_START_VERIFY}` | `{SERVICE_START_EXPECTED}` |
| 健康检查 | `{HEALTHCHECK_VERIFY}` | `{HEALTHCHECK_EXPECTED}` |
| API 可用性 | `{API_VERIFY}` | `{API_EXPECTED}` |
| 前端访问 | `{WEB_VERIFY}` | `{WEB_EXPECTED}` |
| 数据库连接 | `{DATABASE_VERIFY}` | `{DATABASE_EXPECTED}` |
| 对象存储 | `{OBJECT_STORAGE_VERIFY}` | `{OBJECT_STORAGE_EXPECTED}` |
| 上传/媒体 | `{MEDIA_VERIFY}` | `{MEDIA_EXPECTED}` |
| 算法/模型 | `{ALGORITHM_VERIFY}` | `{ALGORITHM_EXPECTED}` |
| 日志检查 | `{LOG_VERIFY}` | `{LOG_EXPECTED}` |

无法执行验证时，必须说明原因、风险和建议补验方式。

## 16. 回滚与故障处理 `[通用 + 个性化]`

| 场景 | 回滚方式 | 数据处理 | 风险 | 负责人 |
|---|---|---|---|---|
| 应用版本回滚 | `{APP_ROLLBACK}` | `{APP_ROLLBACK_DATA}` | `{APP_ROLLBACK_RISK}` | `{OWNER}` |
| 配置回滚 | `{CONFIG_ROLLBACK}` | `{CONFIG_ROLLBACK_DATA}` | `{CONFIG_ROLLBACK_RISK}` | `{OWNER}` |
| 数据库回滚 | `{DB_ROLLBACK}` | `{DB_ROLLBACK_DATA}` | `{DB_ROLLBACK_RISK}` | `{OWNER}` |
| 对象存储回滚 | `{STORAGE_ROLLBACK}` | `{STORAGE_ROLLBACK_DATA}` | `{STORAGE_ROLLBACK_RISK}` | `{OWNER}` |

故障处理记录应沉淀到 `docs/knowledge-base/incidents/`。发布回滚策略应同步 `rules/release.md`。

## 17. AI 修改部署的规则 `[通用]`

AI Agent 修改部署相关内容时必须：

1. 先读取 `AGENTS.md`、`rules/environment.md`、`rules/port-management.md`、`rules/security.md`、`rules/release.md` 和本文。
2. 判断是否需要 OpenSpec Change；涉及服务拓扑、端口、数据库、对象存储、权限、发布方式变化时必须创建或更新 change。
3. 同步更新 `.env.example`、`docker-compose.yml`、`deploy/`、`README.md`、`docs/01-architecture.md`、`docs/05-compatibility-matrix.md`。
4. 不得为了本机临时端口冲突随意修改应用内部端口。
5. 不得写入真实密钥、真实客户数据、生产地址或私有凭据。
6. 完成后执行部署验证；无法执行时说明原因。

## 18. 更新触发条件 `[通用]`

发生以下情况时，必须更新本文：

- 新增、删除或重命名服务。
- 端口、环境变量、镜像、Dockerfile、Compose、K8s、deploy 脚本变化。
- 数据库、对象存储、上传目录、模型目录、volume 变化。
- 部署方式从本地切换为云、Kubernetes、SaaS 或私有化。
- 安全、TLS、CORS、鉴权、密钥管理方式变化。
- 发布、回滚、健康检查、监控或日志策略变化。

同步检查：

- `docs/01-architecture.md`
- `docs/04-database-design.md`
- `docs/05-compatibility-matrix.md`
- `README.md`
- `AGENTS.md`
- `.env.example`
- `docker-compose.yml`
- `deploy/`
- `rules/environment.md`
- `rules/port-management.md`
- `rules/security.md`
- `rules/release.md`

## 19. 初始化生成建议 `[通用]`

工程初始化工具生成本文时应遵循：

1. 保留所有 `[通用]` 模块。
2. 用用户输入替换所有 `[个性化]` 占位符。
3. 根据 `{DEPLOYMENT_STACK}` 保留 Docker Compose、Kubernetes、SaaS、私有化等 `[条件启用]` 模块。
4. 根据 `{SERVICE_MATRIX}` 生成真实服务、端口、环境变量、volume 和健康检查。
5. 根据数据库、对象存储、媒体、算法、异步任务能力保留或删除对应章节。
6. 未确认信息标记为 `待确认`。
7. 不得保留来源项目的容器名、bucket、端口、账号、密码、服务名或部署命令。
8. 生成后检查本文是否能回答：
   - 如何启动和停止？
   - 有哪些服务和端口？
   - 配置和密钥从哪里来？
   - 数据如何持久化和备份？
   - 部署后如何验证？
   - 出问题如何回滚？
