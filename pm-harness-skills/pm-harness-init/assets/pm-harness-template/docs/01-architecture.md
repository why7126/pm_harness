---
title: 系统架构
purpose: 描述系统上下文、模块边界、分层架构、部署视图、数据流、接口契约、存储策略、AI 开发边界和架构演进规则
content: 架构总览、模块职责、技术栈、运行时拓扑、关键链路、数据与存储、接口与集成、非功能要求、架构决策与更新规则
source: Harness docs/01-architecture.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；架构、模块边界、部署拓扑、数据流或技术栈变化时更新；后续由 AI 辅助更新并经人工 Review
owner: {ARCHITECTURE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 docs/01-architecture.md 模块
---

# 系统架构

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如 Web、微信小程序、移动端、对象存储、媒体、算法模型、异步任务、外部集成、私有化部署。

## 0. 文档定位 `[通用]`

本文是 `{PRODUCT_NAME}` 的架构入口文档，用于说明系统如何由产品能力落到工程结构、运行时组件、数据流和部署形态。

本文重点回答：

- 系统由哪些模块组成，各模块职责是什么。
- 用户、前端、后端、数据库、对象存储、算法服务、第三方系统之间如何交互。
- 源码目录与架构模块如何映射。
- 接口、数据、媒体、模型、部署和测试的边界在哪里。
- AI Agent 修改架构相关内容时必须遵守哪些约束。

本文不替代详细规则：

- 目录边界见 `rules/directory-structure.md`。
- API 规范见 `rules/api.md` 与 `docs/03-api-index.md`。
- 数据库设计见 `rules/database.md` 与 `docs/04-database-design.md`。
- 部署说明见 `docs/02-deployment.md`。
- 数据、媒体、对象存储见 `rules/data-management.md`、`rules/media.md`、`rules/object-storage.md`。
- 兼容性见 `docs/05-compatibility-matrix.md` 与 `rules/compatibility.md`。

## 1. 生成参数 `[个性化]`

初始化生成本文时，应优先使用用户输入填充以下参数。缺失信息可以标记为 `待确认`，不得编造架构事实。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{PRODUCT_FORMS}` | 产品形态，如 Web、管理后台、微信小程序、移动端、API 服务 | 待确认 |
| `{BACKEND_STACK}` | 后端技术栈 | 待确认 |
| `{FRONTEND_STACK}` | 前端技术栈 | 待确认 |
| `{DATABASE_STACK}` | 数据库与迁移方案 | 待确认 |
| `{OBJECT_STORAGE_STACK}` | 对象存储方案 | 待确认 |
| `{ASYNC_TASK_STACK}` | 异步任务、队列、调度系统 | 待确认 |
| `{ALGORITHM_STACK}` | 算法、模型、AI 服务栈 | 待确认 |
| `{DEPLOYMENT_STACK}` | 部署方式，如 Docker Compose、Kubernetes、私有化部署 | 待确认 |
| `{EXTERNAL_INTEGRATIONS}` | 外部系统、第三方 API、Webhook | 待确认 |
| `{ARCHITECTURE_OWNER}` | 架构文档负责人 | 待确认 |
| `{PRIMARY_VERIFY_COMMAND}` | 架构变更后的统一验证命令 | 待确认 |

## 2. 架构原则 `[通用 + 个性化]`

通用原则：

- 需求、BUG 和高影响架构变更必须通过 `issues/` 与 `openspec/changes/` 进入实现。
- 架构模块必须能映射到明确的源码目录、接口契约、测试范围和部署组件。
- 跨模块通信优先通过显式 API、事件、SDK、共享类型或文件协议，不得依赖隐式目录耦合。
- 数据库、对象存储、运行时数据和模型文件必须有清晰边界，不得把生产数据或大文件直接提交到 Git。
- 部署拓扑、端口、环境变量、服务依赖变化时，必须同步更新 `docs/02-deployment.md`、`.env.example` 和相关规则。

项目个性化原则：

```text
{ARCHITECTURE_PRINCIPLES}
```

## 3. 总体架构 `[通用 + 个性化]`

初始化时应根据 `{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{ALGORITHM_STACK}` 和 `{DEPLOYMENT_STACK}` 生成真实架构图。

```text
{CLIENT_LAYER}
        ↓
{API_OR_GATEWAY_LAYER}
        ↓
{APPLICATION_LAYER}
        ↓
{DATA_AND_STORAGE_LAYER}
        ↓
{EXTERNAL_OR_ALGORITHM_LAYER}
```

示例占位：

```text
Web / Admin / Mobile / WeChat Miniapp / API Client
        ↓
Backend API / Gateway
        ↓
Application Services / Domain Services / Jobs
        ↓
Database / Object Storage / Cache / Search
        ↓
External Services / Algorithm Service / Model Runtime
```

生成要求：

- 未启用的端或服务必须删除，不得保留无效占位。
- 如果系统是单体应用，应明确“单体内部分层”。
- 如果系统是多服务架构，应明确服务间通信协议和调用方向。
- 如果存在外部系统，应标明数据进出方向和鉴权方式。

## 4. 系统上下文 `[通用 + 个性化]`

| 外部参与者/系统 | 与本系统关系 | 交互方式 | 输入 | 输出 | 备注 |
|---|---|---|---|---|---|
| `{ACTOR_OR_SYSTEM_1}` | `{RELATIONSHIP_1}` | `{INTERACTION_1}` | `{INPUT_1}` | `{OUTPUT_1}` | `{NOTE_1}` |
| `{ACTOR_OR_SYSTEM_2}` | `{RELATIONSHIP_2}` | `{INTERACTION_2}` | `{INPUT_2}` | `{OUTPUT_2}` | `{NOTE_2}` |

上下文边界要求：

- 用户角色来自 `docs/00-product-overview.md`。
- 外部系统和第三方服务必须在 `{EXTERNAL_INTEGRATIONS}` 中列出。
- 涉及敏感数据、回调、文件传输或跨网访问时，必须同步 `rules/security.md` 与 `rules/compatibility.md`。

## 5. 模块职责 `[通用 + 个性化]`

| 模块 | 源码/目录 | 职责 | 输入 | 输出 | 依赖 | 状态 |
|---|---|---|---|---|---|---|
| 后端 API | `src/backend/` | `{BACKEND_RESPONSIBILITY}` | `{BACKEND_INPUT}` | `{BACKEND_OUTPUT}` | `{BACKEND_DEPENDENCIES}` | `{BACKEND_STATUS}` |
| Web 前端 | `src/web/` | `{WEB_RESPONSIBILITY}` | `{WEB_INPUT}` | `{WEB_OUTPUT}` | `{WEB_DEPENDENCIES}` | `{WEB_STATUS}` |
| 微信小程序 | `src/wechat-miniapp/` | `{WECHAT_MINIAPP_RESPONSIBILITY}` | `{WECHAT_MINIAPP_INPUT}` | `{WECHAT_MINIAPP_OUTPUT}` | `{WECHAT_MINIAPP_DEPENDENCIES}` | `{WECHAT_MINIAPP_STATUS}` |
| 移动端 | `src/mobile/`、`src/android/`、`src/ios/` | `{MOBILE_RESPONSIBILITY}` | `{MOBILE_INPUT}` | `{MOBILE_OUTPUT}` | `{MOBILE_DEPENDENCIES}` | `{MOBILE_STATUS}` |
| 共享层 | `src/shared/` | `{SHARED_RESPONSIBILITY}` | `{SHARED_INPUT}` | `{SHARED_OUTPUT}` | `{SHARED_DEPENDENCIES}` | `{SHARED_STATUS}` |
| SDK/客户端 | `src/sdk/` | `{SDK_RESPONSIBILITY}` | `{SDK_INPUT}` | `{SDK_OUTPUT}` | `{SDK_DEPENDENCIES}` | `{SDK_STATUS}` |
| 算法/模型 | `src/algorithm/`、`models/` | `{ALGORITHM_RESPONSIBILITY}` | `{ALGORITHM_INPUT}` | `{ALGORITHM_OUTPUT}` | `{ALGORITHM_DEPENDENCIES}` | `{ALGORITHM_STATUS}` |
| 基础设施 | `src/infrastructure/`、`deploy/` | `{INFRA_RESPONSIBILITY}` | `{INFRA_INPUT}` | `{INFRA_OUTPUT}` | `{INFRA_DEPENDENCIES}` | `{INFRA_STATUS}` |

未启用模块应从初始化后的文档中删除。新增模块必须先更新 `rules/directory-structure.md` 并通过 OpenSpec Change 说明边界。

## 6. 源码分层 `[通用 + 个性化]`

### 6.1 后端分层 `[条件启用]`

根据 `{BACKEND_STACK}` 生成真实分层。常见分层示例：

```text
api / controllers
  ↓
schemas / dto / validators
  ↓
services / use_cases
  ↓
repositories / dao
  ↓
models / entities
  ↓
database / external clients
```

后端规则：

- API 层只处理协议、鉴权上下文、参数解析和响应封装。
- Service 或 Use Case 层承载业务流程，不直接依赖 Web UI。
- Repository 或 DAO 层封装持久化访问，不把 SQL/ORM 细节泄漏到上层。
- Schema、DTO、Model、Entity 的命名和边界必须符合 `rules/language.md` 与 `rules/coding.md`。

### 6.2 前端分层 `[条件启用]`

根据 `{FRONTEND_STACK}` 生成真实分层。常见分层示例：

```text
pages / routes
  ↓
features / modules
  ↓
shared ui / components
  ↓
api client / state / hooks
  ↓
design tokens / shared types
```

前端规则：

- 页面层负责编排，不重复实现共享组件。
- 业务组件、复合组件、基础组件应按 `rules/ui-design.md` 放置。
- API 客户端、类型生成、错误处理应符合 `rules/api.md`。
- Design Token 和主题变量变更必须同步 UI 规范和视觉验收。

### 6.3 算法/模型分层 `[条件启用]`

```text
model metadata / configs
  ↓
preprocess / postprocess
  ↓
inference service / runner
  ↓
domain integration
  ↓
monitoring / evaluation
```

模型规则：

- 大模型权重、商业模型文件和敏感训练数据不得直接提交到 Git。
- `models/` 应保存模型说明、版本、校验和、下载方式、许可和放置路径。
- 推理接口、输入输出格式和失败策略必须有测试或验收记录。

## 7. 运行时拓扑 `[通用 + 个性化]`

根据 `{DEPLOYMENT_STACK}` 生成运行时拓扑。

| 运行时组件 | 进程/容器 | 端口 | 依赖 | 数据卷/存储 | 健康检查 |
|---|---|---:|---|---|---|
| `{RUNTIME_COMPONENT_1}` | `{PROCESS_OR_CONTAINER_1}` | `{PORT_1}` | `{RUNTIME_DEPENDENCY_1}` | `{VOLUME_OR_STORAGE_1}` | `{HEALTHCHECK_1}` |
| `{RUNTIME_COMPONENT_2}` | `{PROCESS_OR_CONTAINER_2}` | `{PORT_2}` | `{RUNTIME_DEPENDENCY_2}` | `{VOLUME_OR_STORAGE_2}` | `{HEALTHCHECK_2}` |

部署说明必须与以下文件一致：

- `docs/02-deployment.md`
- `.env.example`
- `docker-compose.yml` 或 `deploy/`
- `rules/environment.md`
- `rules/port-management.md`

## 8. 关键数据流 `[通用 + 个性化]`

### 8.1 业务主链路 `[个性化]`

```text
{PRIMARY_BUSINESS_FLOW}
```

每条主链路应说明：

- 触发角色。
- 入口端。
- 调用的 API 或服务。
- 写入或读取的数据对象。
- 失败、重试、回滚或补偿方式。
- 对应需求、OpenSpec 或测试。

### 8.2 文件/媒体链路 `[条件启用]`

```text
客户端选择文件
  ↓
后端或网关鉴权与校验
  ↓
对象存储或文件服务保存
  ↓
数据库保存元数据
  ↓
前端或外部系统展示/下载
```

生成时应替换为项目实际方案，并同步：

- `rules/media.md`
- `rules/object-storage.md`
- `rules/data-management.md`
- `docs/07-object-storage-strategy.md`

### 8.3 异步任务链路 `[条件启用]`

```text
业务触发
  ↓
任务入队 / 调度
  ↓
Worker 执行
  ↓
状态回写 / 事件通知
  ↓
用户或系统读取结果
```

启用异步任务时必须说明任务幂等、重试、超时、失败告警和状态追踪方式。

### 8.4 算法/模型链路 `[条件启用]`

```text
业务输入
  ↓
预处理
  ↓
模型推理 / 算法计算
  ↓
后处理
  ↓
业务结果落库或返回
```

启用算法/模型时必须说明模型版本、输入输出、性能指标、失败降级、测试集和可观测性。

## 9. 数据与存储架构 `[通用 + 个性化]`

| 存储类型 | 技术/服务 | 存储内容 | 访问模块 | 持久化策略 | 备份/迁移 | 规则文档 |
|---|---|---|---|---|---|---|
| 关系数据库 | `{DATABASE_STACK}` | `{DATABASE_CONTENT}` | `{DATABASE_ACCESS_MODULES}` | `{DATABASE_PERSISTENCE}` | `{DATABASE_MIGRATION}` | `rules/database.md` |
| 对象存储 | `{OBJECT_STORAGE_STACK}` | `{OBJECT_STORAGE_CONTENT}` | `{OBJECT_STORAGE_ACCESS_MODULES}` | `{OBJECT_STORAGE_PERSISTENCE}` | `{OBJECT_STORAGE_BACKUP}` | `rules/object-storage.md` |
| 本地数据 | `data/` | `{LOCAL_DATA_CONTENT}` | `{LOCAL_DATA_ACCESS_MODULES}` | `{LOCAL_DATA_POLICY}` | `{LOCAL_DATA_BACKUP}` | `rules/data-management.md` |
| 模型文件 | `models/` | `{MODEL_CONTENT}` | `{MODEL_ACCESS_MODULES}` | `{MODEL_POLICY}` | `{MODEL_VERSION_POLICY}` | `rules/data-management.md` |
| 缓存/搜索 | `{CACHE_OR_SEARCH_STACK}` | `{CACHE_OR_SEARCH_CONTENT}` | `{CACHE_OR_SEARCH_ACCESS_MODULES}` | `{CACHE_OR_SEARCH_POLICY}` | `{CACHE_OR_SEARCH_RECOVERY}` | `{RELATED_RULE}` |

未启用的存储类型应删除或标记为“不适用”。数据库表、索引、迁移和 seed 细节放入 `docs/04-database-design.md`。

## 10. API 与集成架构 `[条件启用]`

| 接口/集成 | 提供方 | 消费方 | 协议 | 鉴权 | 契约来源 | 兼容策略 |
|---|---|---|---|---|---|---|
| `{API_OR_INTEGRATION_1}` | `{PROVIDER_1}` | `{CONSUMER_1}` | `{PROTOCOL_1}` | `{AUTH_1}` | `{CONTRACT_SOURCE_1}` | `{COMPAT_POLICY_1}` |
| `{API_OR_INTEGRATION_2}` | `{PROVIDER_2}` | `{CONSUMER_2}` | `{PROTOCOL_2}` | `{AUTH_2}` | `{CONTRACT_SOURCE_2}` | `{COMPAT_POLICY_2}` |

接口规则：

- API 变更必须同步 `docs/03-api-index.md`、`rules/api.md`、OpenAPI 或项目约定契约文件。
- 前端、移动端、微信小程序、SDK 或外部系统依赖的字段不得无兼容策略直接删除。
- Webhook、第三方集成和回调必须说明重试、签名、幂等和安全策略。

## 11. 安全与权限架构 `[通用 + 个性化]`

| 安全域 | 策略 | 涉及模块 | 关联文档 |
|---|---|---|---|
| 认证 | `{AUTH_STRATEGY}` | `{AUTH_MODULES}` | `rules/security.md` |
| 授权 | `{PERMISSION_MODEL}` | `{PERMISSION_MODULES}` | `rules/security.md` |
| 数据保护 | `{DATA_PROTECTION_POLICY}` | `{DATA_PROTECTION_MODULES}` | `rules/data-management.md` |
| 文件访问 | `{FILE_ACCESS_POLICY}` | `{FILE_ACCESS_MODULES}` | `rules/media.md`、`rules/object-storage.md` |
| 审计日志 | `{AUDIT_POLICY}` | `{AUDIT_MODULES}` | `rules/security.md` |

安全边界变化必须同步需求、OpenSpec、测试和发布说明。

## 12. 非功能要求 `[通用 + 个性化]`

| 类型 | 要求 | 验证方式 | 关联文档 |
|---|---|---|---|
| 性能 | `{PERFORMANCE_REQUIREMENTS}` | `{PERFORMANCE_VERIFY}` | `{PERFORMANCE_DOC}` |
| 可用性 | `{AVAILABILITY_REQUIREMENTS}` | `{AVAILABILITY_VERIFY}` | `{AVAILABILITY_DOC}` |
| 可维护性 | `{MAINTAINABILITY_REQUIREMENTS}` | `{MAINTAINABILITY_VERIFY}` | `rules/coding.md` |
| 可测试性 | `{TESTABILITY_REQUIREMENTS}` | `{TESTABILITY_VERIFY}` | `rules/testing.md` |
| 兼容性 | `{COMPATIBILITY_REQUIREMENTS}` | `{COMPATIBILITY_VERIFY}` | `rules/compatibility.md` |
| 可观测性 | `{OBSERVABILITY_REQUIREMENTS}` | `{OBSERVABILITY_VERIFY}` | `{OBSERVABILITY_DOC}` |

## 13. 测试与验证边界 `[通用]`

架构变更后至少检查：

```text
{PRIMARY_VERIFY_COMMAND}
```

按影响面补充：

- API 变更：契约测试、集成测试、客户端生成验证。
- 数据库变更：迁移测试、回滚验证、Repository/DAO 测试。
- UI 变更：组件测试、视觉验收、端兼容性测试。
- 部署变更：启动验证、健康检查、端口冲突检查。
- 对象存储/媒体变更：上传、下载、权限、过期访问和失败重试测试。
- 算法/模型变更：输入输出样例、性能、降级和版本一致性验证。

测试策略必须与 `rules/testing.md` 和 `docs/05-compatibility-matrix.md` 一致。

## 14. AI 开发边界 `[通用]`

AI Agent 修改架构相关内容时必须遵守：

- 不允许直接凭空修改 `src/`、`deploy/`、数据库 schema 或接口契约。
- 正式能力、接口、数据库、部署、权限、模型、数据流变化必须先进入 `issues/` 与 `openspec/changes/`。
- 不允许绕过 `rules/directory-structure.md` 新增顶层目录或模块。
- 不允许把运行时数据、真实客户数据、密钥、模型大文件提交到 Git。
- 不允许让架构文档与 `README.md`、`AGENTS.md`、`project.yaml`、`docs/02-deployment.md`、`docs/04-database-design.md`、`rules/` 互相矛盾。

AI 完成架构变更后，必须在回复中说明：

- 影响的模块和目录。
- 是否影响 API、数据库、部署、端口、对象存储、模型或 UI。
- 同步更新了哪些文档和规则。
- 执行了哪些验证，或为什么无法执行。

## 15. 架构决策记录 `[通用 + 条件启用]`

如果项目使用 ADR，应在此记录入口；否则可在 OpenSpec change 的 `design.md` 中承载。

| 决策 | 背景 | 选型 | 影响 | 记录位置 |
|---|---|---|---|---|
| `{ARCH_DECISION_1}` | `{DECISION_CONTEXT_1}` | `{DECISION_CHOICE_1}` | `{DECISION_IMPACT_1}` | `{DECISION_RECORD_1}` |
| `{ARCH_DECISION_2}` | `{DECISION_CONTEXT_2}` | `{DECISION_CHOICE_2}` | `{DECISION_IMPACT_2}` | `{DECISION_RECORD_2}` |

重大架构决策必须可追踪到需求、OpenSpec Change、评审记录或 ADR。

## 16. 更新触发条件 `[通用]`

发生以下情况时，必须更新本文：

- 产品形态、模块边界或源码目录变化。
- 技术栈、数据库、对象存储、缓存、队列、算法服务变化。
- 部署拓扑、端口、环境变量、网络、volume、镜像变化。
- 核心数据流、文件链路、模型链路或外部集成变化。
- 安全、权限、审计、数据保护策略变化。
- 非功能要求、兼容性矩阵或验证方式变化。

同步检查：

- `docs/00-product-overview.md`
- `docs/02-deployment.md`
- `docs/03-api-index.md`
- `docs/04-database-design.md`
- `docs/05-compatibility-matrix.md`
- `README.md`
- `AGENTS.md`
- `project.yaml`
- `rules/`
- `openspec/project.md`

## 17. 初始化生成建议 `[通用]`

工程初始化工具生成本文时应遵循：

1. 保留所有 `[通用]` 模块。
2. 用用户输入替换所有 `[个性化]` 占位符。
3. 根据项目能力保留或删除 `[条件启用]` 模块。
4. 根据 `{PRODUCT_FORMS}` 生成真实总体架构和模块职责。
5. 根据 `{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{ALGORITHM_STACK}`、`{DEPLOYMENT_STACK}` 生成技术与运行时视图。
6. 未启用媒体、对象存储、异步任务、算法模型、外部集成时，删除对应链路。
7. 不得保留来源项目的业务名、服务名、端口、技术栈或存储方案。
8. 生成后检查本文是否能回答：
   - 系统有哪些模块？
   - 模块之间如何调用？
   - 数据存在哪里、如何流动？
   - 部署时有哪些运行时组件？
   - AI 修改架构时应该同步哪些文档和验证？
