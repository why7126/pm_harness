---
purpose: API 设计与接口契约规范
content: 路由命名、请求响应、错误码、分页、鉴权、OpenAPI、客户端生成、跨模块契约、Webhook、接口变更流程
scope: 后端接口、前端 API 调用、SDK、Webhook、跨模块服务契约
source: Harness api.md 抽象模板，基于多个项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；新增接口、修改接口、调整错误码、变更 OpenAPI 或客户端生成方式时更新
note: 适用于 {PRODUCT_NAME} 项目；API 变更必须同步接口文档、OpenSpec 规格、客户端类型和测试
template_scope: 可作为工程初始化时的 rules/api.md 模块
---

# API 设计规范

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如前端生成客户端、Webhook、文件上传、外部服务、SDK。

## 0. 规则定位 [通用]

`rules/api.md` 约束所有接口设计、接口实现、接口调用和接口变更。AI Agent 新增或修改 API 前必须读取：

```text
AGENTS.md
rules/global.md
rules/api.md
rules/security.md
rules/testing.md
docs/03-api-index.md
openspec/changes/<change-id>/（如为正式变更）
```

如果接口涉及数据库、文件上传、对象存储、前端生成客户端、跨模块契约或部署配置，还必须继续读取对应规则：

```text
rules/database.md
rules/media.md
rules/object-storage.md
rules/environment.md
rules/compatibility.md
docs/openapi-rules.md
docs/api-governance.md
```

初始化生成本文件时，必须替换占位符；缺失信息可以标记为 `待确认`，不得编造接口、服务地址或生成命令。

常用占位符：

| 占位符 | 含义 | 归属 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | [个性化] |
| `{API_PREFIX}` | API 前缀，默认 `/api/v1` | [个性化] |
| `{BACKEND_STACK}` | 后端技术栈 | [个性化] |
| `{FRONTEND_STACK}` | 前端技术栈 | [个性化] |
| `{API_CLIENT_GENERATOR}` | 客户端生成工具，如 Orval、OpenAPI Generator | [条件启用] |
| `{API_CLIENT_GENERATE_COMMAND}` | 客户端生成命令 | [条件启用] |
| `{API_DOC_PATH}` | API 索引或契约文档路径 | [个性化] |
| `{OPENAPI_SOURCE}` | OpenAPI 来源，如 FastAPI `/openapi.json` | [个性化] |
| `{API_GENERATED_DIR}` | 生成客户端目录 | [条件启用] |
| `{AUTH_SCHEME}` | 鉴权方案，如 Bearer Token、Cookie Session | [条件启用] |
| `{EXTERNAL_CONTRACT_DOCS}` | 外部服务或跨模块契约文档 | [条件启用] |

## 1. API 设计原则 [通用]

- 接口必须围绕资源、动作边界和业务状态设计，不按页面临时拼接。
- API 路径、请求、响应、错误码和鉴权规则必须可被 OpenAPI 或契约文档描述。
- 对外暴露的字段必须稳定；破坏性变更必须通过 OpenSpec Change 说明兼容策略。
- 前后端、SDK、外部服务和 Webhook 必须以同一份契约为准。
- AI 不得新增“只有调用方知道”的隐藏字段、隐藏状态或隐式约定。
- 所有接口变更必须补充或更新测试。

## 2. 路径规范 [通用 + 个性化]

接口统一使用 `{API_PREFIX}` 前缀。默认推荐：

```text
/api/v1
```

路由命名规则：

- 使用 RESTful 风格：`{API_PREFIX}/{resources}`。
- 资源名使用复数形式：`/users`、`/orders`、`/files`。
- 多词资源使用 kebab-case：`/user-profiles`、`/meeting-minutes`。
- 嵌套资源用路径表达：`/users/{user_id}/roles`。
- 管理端或内部接口应明确命名空间：`/admin/*`、`/internal/*`。
- 不在路径中使用动词表达普通 CRUD：优先用 HTTP Method 表达。
- 对非 CRUD 动作可使用动作子资源：`/jobs/{job_id}/cancel`、`/files/{file_id}/preview-url`。

推荐资源应在初始化时根据业务生成：

```text
{API_RESOURCE_EXAMPLES}
```

HTTP Method 约定：

| Method | 用途 | 幂等性 |
|---|---|---|
| `GET` | 查询列表或详情 | 是 |
| `POST` | 创建资源、提交任务、触发非幂等动作 | 否 |
| `PUT` | 全量替换资源 | 是 |
| `PATCH` | 部分更新资源 | 通常是 |
| `DELETE` | 删除或软删除资源 | 是 |

## 3. 请求规范 [通用]

### 3.1 参数位置

| 参数类型 | 放置位置 | 示例 |
|---|---|---|
| 资源 ID | path | `/users/{user_id}` |
| 筛选、分页、排序 | query | `?page=1&page_size=20&sort=-created_at` |
| 创建、更新正文 | body | JSON request body |
| 鉴权信息 | header/cookie | `Authorization: Bearer <token>` |
| 文件上传 | multipart | `multipart/form-data` |

### 3.2 命名与类型

- JSON 字段命名默认使用 `snake_case`，除非项目明确要求 `camelCase`。
- 路径参数使用稳定 ID 字段，例如 `{resource_id}`。
- 时间字段使用 ISO 8601 字符串，必须明确时区。
- 金额、数量、百分比等字段必须说明单位和精度。
- 枚举字段必须在 Schema 或契约文档中列出合法值。
- 可空字段必须明确 `null` 与缺省字段的区别。

### 3.3 校验

- 后端必须使用框架 Schema 能力校验入参，例如 Pydantic、Zod、Joi、class-validator。
- 分页、排序、筛选、上传大小、MIME 类型、枚举和字符串长度必须有边界。
- 不信任前端传入的用户 ID、角色、租户、权限字段。
- 批量接口必须限制批量数量。

## 4. 响应结构 [通用 + 个性化]

默认统一响应结构：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

字段语义：

| 字段 | 类型 | 说明 |
|---|---|---|
| `code` | number/string | 业务错误码；成功为 `0` 或项目约定成功码 |
| `message` | string | 面向调用方的简短说明 |
| `data` | object/array/null | 业务数据 |
| `request_id` | string | 请求追踪 ID，建议生产环境启用 |

如项目采用 HTTP 状态码 + 直接资源响应，不使用统一包装，初始化时必须在本节明确替换，并同步前端调用规范。

### 4.1 分页响应 [通用]

分页参数：

```text
page       从 1 开始
page_size  默认 20，最大值由项目配置决定
```

分页响应推荐：

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 20
}
```

如采用 cursor 分页，必须说明：

```json
{
  "items": [],
  "next_cursor": null,
  "has_more": false
}
```

### 4.2 空值与错误响应 [通用]

- 查询不到资源应返回 404 或项目约定的资源不存在错误码。
- 空列表返回 `items: []`，不返回 `null`。
- 删除成功可返回空 data、删除后的资源摘要或操作结果，但必须统一。
- 错误响应不得泄露 SQL、堆栈、密钥、内部路径或第三方凭据。

## 5. 错误码规范 [通用 + 个性化]

错误码必须稳定、可检索、可测试，并在文档中维护。

推荐错误码分段：

| 范围 | 类别 | HTTP 状态码 | 示例 |
|---|---|---|---|
| `1xxx` | 客户端错误 | 400-429 | 参数无效、未授权、无权限、资源不存在 |
| `2xxx` | 业务逻辑错误 | 400-409 | 状态非法、重复提交、额度不足 |
| `3xxx` | 外部服务错误 | 502-504 | 第三方不可用、对象存储失败、算法服务失败 |
| `4xxx` | 服务端内部错误 | 500 | 内部错误、数据库错误、任务调度失败 |
| `8xxx` | 部署或环境错误 | 500-503 | 配置缺失、依赖未就绪 |
| `9xxx` | 授权、License 或配额错误 | 403-429 | License 过期、并发超限、租户配额超限 |

项目错误码文档路径：

```text
docs/error-codes.md
```

新增错误码时必须同步：

- 后端错误码定义。
- API 文档或 OpenAPI 示例。
- 前端错误处理映射。
- 测试用例。
- `docs/error-codes.md`。

## 6. 鉴权、权限与安全 [条件启用]

项目鉴权方案：

```text
{AUTH_SCHEME}
```

通用要求：

- 所有非公开接口必须明确鉴权要求。
- 管理端、内部接口、租户接口必须区分权限边界。
- 后端必须从可信上下文获取用户、租户、角色和权限，不信任请求体传入。
- 文件上传、下载、预览 URL、导入导出必须做权限校验。
- Webhook 或外部回调必须具备签名、token、IP allowlist 或其他可信校验机制。
- 错误信息不得泄露敏感信息。

## 7. OpenAPI 与客户端生成 [条件启用]

项目 OpenAPI 来源：

```text
{OPENAPI_SOURCE}
```

客户端生成工具：

```text
{API_CLIENT_GENERATOR}
```

生成命令：

```bash
{API_CLIENT_GENERATE_COMMAND}
```

生成目录：

```text
{API_GENERATED_DIR}
```

规则：

- 后端必须正确暴露或维护 OpenAPI Spec。
- 前端、SDK 或调用方类型必须从 OpenAPI 或契约源生成，避免手写重复类型。
- 生成产物目录必须明确是否提交到 Git。
- API 变更后必须重新生成客户端，并检查调用方编译或类型检查。
- 禁止手写已由生成工具覆盖的 API 调用函数，除非项目明确允许扩展层封装。

## 8. 前端 API 调用规范 [条件启用]

前端存在时必须启用本节。

推荐分层：

```text
generated client -> request adapter -> domain service/hook -> UI component
```

规则：

- UI 组件不直接拼接 URL。
- API 调用统一走项目封装的 client 或 service。
- 统一处理鉴权、刷新 token、错误提示、request_id、超时和取消请求。
- 上传、下载、长轮询、SSE、WebSocket 使用独立 client 或明确配置。
- 前端不得依赖后端未文档化字段。

常见 client 配置：

| Client | 用途 | 默认超时 |
|---|---|---|
| `{DEFAULT_API_CLIENT}` | 普通 API | `{DEFAULT_API_TIMEOUT}` |
| `{UPLOAD_API_CLIENT}` | 文件上传 | `{UPLOAD_API_TIMEOUT}` |
| `{INTERNAL_API_CLIENT}` | 内部或管理接口 | `{INTERNAL_API_TIMEOUT}` |

## 9. 文件、媒体与导入导出 API [条件启用]

涉及文件、图片、音频、视频、文档、模型文件或导入导出时启用本节。

上传接口必须明确：

- 文件字段名。
- 支持 MIME 类型。
- 大小限制。
- 鉴权与权限。
- 存储位置或对象 key 规则。
- 病毒扫描、内容校验或异步处理策略（如适用）。

媒体或文件上传响应推荐包含：

- `file_id` 或 `media_id`
- `object_key`
- `url` 或 `preview_url`
- `mime_type`
- `size`
- `checksum`（如适用）
- `width` / `height`（图片或视频适用）
- `duration`（音视频适用）
- `cover_url`（视频适用）

导入导出接口必须说明同步/异步模式、任务状态查询、失败明细和下载有效期。

## 10. 异步任务与长流程 API [条件启用]

涉及转码、导入导出、模型推理、报告生成、音视频处理等长耗时任务时启用本节。

推荐模式：

```text
POST /jobs              创建任务
GET /jobs/{job_id}      查询任务状态
POST /jobs/{job_id}/cancel 取消任务
```

任务状态必须可枚举，例如：

```text
pending -> running -> succeeded / failed / canceled
```

响应必须包含：

- `job_id`
- `status`
- `progress`（如适用）
- `result`（成功时）
- `error`（失败时）
- `created_at`、`updated_at`

## 11. Webhook 与外部回调 [条件启用]

涉及外部服务回调时启用本节。

Webhook 要求：

- 回调地址必须由配置或任务创建响应明确生成。
- 回调必须幂等，相同事件重复投递不得造成重复副作用。
- 回调必须校验签名、token、时间戳或来源。
- 回调处理应尽快返回；耗时处理放入异步任务。
- 必须记录事件 ID、重试次数、处理结果和失败原因。
- 需要定义重试策略、超时、死信或人工补偿方案。

Webhook 契约必须写入：

```text
{EXTERNAL_CONTRACT_DOCS}
```

## 12. 外部服务与跨模块契约 [条件启用]

涉及算法服务、工作流、支付、消息、对象存储、用户中心、第三方平台或子项目间调用时启用本节。

跨模块契约文档：

```text
{EXTERNAL_CONTRACT_DOCS}
```

规则：

- 外部服务调用必须通过防腐层 client 或 adapter，不在业务代码中散落 HTTP 拼接。
- 契约必须声明请求、响应、错误、超时、重试、幂等和兼容策略。
- 第三方错误必须转换为项目错误码。
- 不得把第三方 SDK 类型泄漏到业务核心层，除非项目明确接受。
- 契约变更必须同步调用方、被调用方、测试和文档。

## 13. 兼容性与版本策略 [通用]

- 破坏性变更必须新建 OpenSpec Change 并说明迁移方式。
- 删除字段前应先废弃并保留兼容期，除非项目尚未发布或用户明确允许。
- 新增响应字段通常兼容；修改字段含义、类型、必填性通常不兼容。
- API 版本变化应体现在路径、Header 或契约版本中。
- 移动端、小程序、第三方集成或私有化部署场景必须额外考虑旧客户端兼容。

## 14. API 变更流程 [通用]

AI 新增或修改 API 时，必须按顺序处理：

1. 确认是否需要 OpenSpec Change。
2. 更新 `openspec/changes/<change-id>/specs/**/spec.md`。
3. 更新后端路由、Schema、错误码和权限校验。
4. 更新或生成 OpenAPI。
5. 更新前端、SDK 或调用方客户端。
6. 更新 `docs/03-api-index.md`、`docs/api-governance.md`、`docs/openapi-rules.md` 或相关契约文档。
7. 补充单元、集成、契约或 E2E 测试。
8. 运行客户端生成、类型检查、接口测试和相关验证。
9. 在回复中说明接口路径、请求、响应、错误码、兼容性和验证结果。

## 15. 测试要求 [通用]

API 相关变更至少考虑：

- Schema 校验测试。
- 成功响应测试。
- 错误码测试。
- 权限测试。
- 分页、筛选、排序测试。
- 文件上传大小和 MIME 测试（如适用）。
- Webhook 幂等和签名测试（如适用）。
- 外部服务失败、超时和重试测试（如适用）。
- 前端生成客户端类型检查（如适用）。

## 16. 完成任务后检查清单 [通用 + 条件启用]

```text
□ 是否读取 rules/api.md 和相关 rules
□ 是否确认 API 前缀、命名、Method 和资源边界
□ 是否更新 OpenSpec Change（正式接口变更）
□ 是否更新后端路由、Schema、错误码和权限
□ 是否更新 OpenAPI 或契约文档
□ 是否重新生成前端/SDK 客户端
□ 是否更新 docs/03-api-index.md 或相关 docs/specs
□ 是否补充接口测试、契约测试或前端类型检查
□ 是否确认分页、错误响应、鉴权和兼容性
□ 文件/媒体 API：是否校验 MIME、大小、权限和对象存储 key
□ Webhook：是否校验签名、幂等、重试和失败记录
□ 外部服务：是否通过 adapter/client 调用并转换错误码
□ 是否在回复中说明请求、响应、错误码、影响范围和验证结果
```

## 17. 初始化生成建议 [通用]

工程初始化工具生成 `rules/api.md` 时应：

1. 保留 [通用] 模块。
2. 用用户输入替换 [个性化] 占位符。
3. 根据项目能力保留或删除 [条件启用] 模块。
4. 从实际后端框架生成 OpenAPI 来源。
5. 从实际前端技术栈生成客户端生成工具和命令。
6. 根据产品形态和业务领域生成资源示例，不保留模板业务词。
7. 删除指向不存在目录、命令、文档或服务的内容。
8. 未知项标记为 `待确认`。
