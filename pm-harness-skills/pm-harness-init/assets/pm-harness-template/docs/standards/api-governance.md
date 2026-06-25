---
purpose: API 治理体系
content: API 设计原则、资源命名、URL/Method/版本、请求响应、错误码、认证授权、分页排序、幂等、OpenAPI、客户端生成、测试与维护规则
source: Harness docs/standards/api-governance.md 抽象模板，初始化时基于用户输入生成
update_method: API 风格、响应结构、认证、错误码、OpenAPI、客户端生成或兼容策略变化时同步更新
owner: {API_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；无 API 项目可保留为未来启用规范并标记不适用
---

# API 治理体系

## 0. 文档定位 `[通用]`

本文档定义项目 API 的长期治理规则，覆盖 API 设计原则、资源命名、URL、HTTP Method、版本、请求响应、错误码、认证授权、分页排序、幂等、文件上传、OpenAPI 契约、客户端生成、测试验收和维护流程。

本文档是 `rules/api.md` 的落地细则，应与 `docs/03-api-index.md`、`docs/standards/openapi-rules.md`、`docs/standards/error-codes.md`、`docs/standards/authentication.md`、`docs/standards/file_upload.md` 保持一致。

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{API_OWNER}` | API 治理负责人 | 待确认 |
| `{API_ENABLED}` | 是否启用 API | true / false |
| `{API_STYLE}` | API 风格 | REST / RPC / GraphQL / mixed |
| `{API_PREFIX}` | API 基础前缀 | `/api/v1` |
| `{API_VERSION_STRATEGY}` | 版本策略 | URL path / header / media type |
| `{BACKEND_STACK}` | 后端技术栈 | 待确认 |
| `{FRONTEND_STACK}` | 前端技术栈 | 待确认 |
| `{RESPONSE_ENVELOPE}` | 统一响应结构 | `{ code, message, data }` |
| `{ERROR_CODE_DOC_PATH}` | 错误码文档路径 | `docs/standards/error-codes.md` |
| `{AUTH_STRATEGY}` | 鉴权策略 | Token / Session / OAuth2 / API Key / none |
| `{PERMISSION_MODEL}` | 权限模型 | RBAC / ABAC / owner-based / none |
| `{OPENAPI_SOURCE}` | OpenAPI 契约来源 | 待确认 |
| `{API_CLIENT_GENERATOR}` | 客户端生成器 | OpenAPI Generator / Kiota / 自定义生成器 / none |
| `{API_CLIENT_GENERATE_COMMAND}` | 客户端生成命令 | 待确认 |
| `{API_VERIFY_COMMAND}` | API 治理校验命令 | `python scripts/validate-api-standard.py` |

## 2. 启用条件 `[通用]`

满足以下任一条件时，应完整启用本文档：

- 项目暴露 HTTP API、RPC API、GraphQL API、Webhook 或 SDK 接口。
- 前端、移动端、微信小程序、第三方系统或内部服务需要通过接口访问后端能力。
- 项目需要生成 OpenAPI、客户端 SDK、接口测试或契约测试。
- 项目存在认证、权限、错误码、分页、上传、异步任务等接口治理需求。

无 API 项目可保留本文档为未来启用规范，但必须标记 `{API_ENABLED}=false`，并删除强制实现、测试和客户端生成要求。

## 3. 设计原则 `[通用]`

| 原则 | 说明 |
|---|---|
| 契约优先 | API 契约必须可被文档、测试和客户端生成复用 |
| 资源清晰 | URL 表达资源或能力边界，避免含糊命名 |
| 兼容优先 | 非破坏性扩展优先；破坏性变更必须走版本或迁移策略 |
| 响应统一 | 成功、失败、分页、批量操作必须有统一结构 |
| 错误可定位 | 错误码、message、trace 信息应能支持排障 |
| 权限前置 | API 必须明确认证、授权和数据归属规则 |
| 可测试 | 每类接口必须能被单元、集成、契约或 E2E 测试覆盖 |

## 4. API 风格 `[通用 + 个性化]`

默认建议使用 REST 风格。若项目使用 GraphQL、RPC、gRPC、Webhook 或混合风格，应在初始化时替换本节并说明选择理由。

| 风格 | 适用场景 | 生成要求 |
|---|---|---|
| REST | 资源型业务接口、常规 CRUD、管理后台 | 保留 URL/Method/分页/错误码规范 |
| GraphQL | 前端聚合查询强、字段选择复杂 | 增加 schema、resolver、权限和复杂度限制 |
| RPC | 操作语义强、资源边界弱 | 增加方法命名、请求响应和幂等规范 |
| Webhook | 对外事件通知 | 增加签名、重试、幂等、事件版本规范 |
| SDK | 对外集成能力 | 增加包版本、兼容策略和示例规范 |

## 5. URL 与资源命名 `[通用 + 个性化]`

REST URL 推荐格式：

```text
{API_PREFIX}/{resource}
{API_PREFIX}/{resource}/{id}
{API_PREFIX}/{resource}/{id}/{sub_resource}
```

命名规则：

- 资源名使用复数名词。
- URL path 推荐 kebab-case。
- 查询参数推荐 snake_case 或项目约定字段风格，必须与 `rules/language.md` 一致。
- 禁止使用动词式 CRUD 路径，例如把查询、删除、更新动作直接编码进 path 名称。
- 管理端、内部端、公开端 API 应通过路径、网关、鉴权或权限模型明确区分。

示例模板：

```text
{API_PREFIX}/{business_resources}
{API_PREFIX}/{business_resources}/{id}
{API_PREFIX}/auth/login
{API_PREFIX}/uploads/{resource_type}
```

初始化时必须用项目真实资源替换 `{business_resources}`，不得保留来源项目资源名。

## 6. HTTP Method `[通用]`

| Method | 场景 | 幂等性 | 说明 |
|---|---|---|---|
| GET | 查询、列表、详情 | 是 | 不得产生业务副作用 |
| POST | 创建、提交、登录、上传、触发任务 | 否 / 可通过 idempotency key 保证 | 创建类接口默认非幂等 |
| PUT | 全量更新、替换 | 是 | 客户端提交完整资源 |
| PATCH | 部分更新 | 视实现而定 | 必须明确可更新字段 |
| DELETE | 删除、撤销、解绑 | 是 | 应明确软删除或硬删除 |

禁止为了规避 Method 语义而把所有操作都做成 `POST /action`。

## 7. 版本策略 `[通用 + 个性化]`

当前 API 版本策略：

```text
{API_VERSION_STRATEGY}
```

推荐默认：

```text
{API_PREFIX} = /api/v1
```

规则：

- 非破坏性新增字段、接口或枚举值可在当前版本扩展。
- 删除字段、改变字段类型、改变必填性、改变错误码含义、改变权限边界属于破坏性变更。
- 破坏性变更必须进入新版本或提供迁移窗口。
- API 版本变化必须同步 `docs/03-api-index.md`、OpenAPI、客户端生成和兼容性矩阵。

## 8. 请求规范 `[通用 + 个性化]`

| 项 | 规则 |
|---|---|
| Content-Type | JSON 默认使用 `application/json` |
| 文件上传 | 使用 `multipart/form-data` 或预签名上传，见 `docs/standards/file_upload.md` |
| 字段命名 | 与 `rules/language.md` 一致 |
| 必填字段 | 必须由 schema 或验证器声明 |
| 默认值 | 必须由服务端统一处理，不依赖客户端猜测 |
| 枚举 | 必须列入契约和文档 |
| 时间字段 | 必须明确时区和格式 |

请求体不得接受未声明字段，除非项目明确允许扩展字段并说明兼容策略。

## 9. 统一响应结构 `[通用 + 个性化]`

推荐响应 envelope：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

初始化时可根据 `{RESPONSE_ENVELOPE}` 调整，但必须满足：

- 成功和失败结构一致。
- `code` 或等价字段可机器判断。
- `message` 面向排障，不应泄漏敏感信息。
- `data` 可为空，但类型必须明确。
- 需要链路排查时可增加 `trace_id`、`request_id` 或等价字段。

错误响应示例：

```json
{
  "code": 40001,
  "message": "invalid parameter",
  "data": null
}
```

实现路径应在初始化时填入：

```text
{RESPONSE_SCHEMA_PATH}
{EXCEPTION_HANDLER_PATH}
```

## 10. 分页、排序与过滤 `[通用]`

分页响应推荐：

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 100
}
```

规则：

- 列表接口必须明确分页默认值和最大值。
- 排序字段必须白名单控制。
- 过滤字段必须可追踪到业务字段或索引策略。
- 大数据量列表应支持游标分页或明确性能边界。
- 前端展示字段与后端查询字段不一致时，必须说明映射关系。

## 11. 错误码 `[通用 + 个性化]`

错误码事实源：

```text
{ERROR_CODE_DOC_PATH}
```

规则：

- 业务错误、认证错误、权限错误、参数错误、资源不存在、冲突、限流、系统错误必须可区分。
- 错误码不得复用为不同含义。
- 新增错误码必须同步错误码文档、API 文档、测试和前端处理。
- 用户可见文案与开发排障 message 可分离，但不得互相矛盾。

## 12. 认证与授权 `[条件启用 + 个性化]`

当 `{AUTH_STRATEGY}` 不为 `none` 时启用。

| 项 | 规则 |
|---|---|
| 鉴权策略 | `{AUTH_STRATEGY}` |
| 权限模型 | `{PERMISSION_MODEL}` |
| 认证头 | `{AUTH_HEADER}` |
| Token / Session 存储 | `{TOKEN_STORAGE_POLICY}` |
| 匿名访问 | `{ANONYMOUS_ACCESS_POLICY}` |

要求：

- 每个 API 分组必须声明是否需要认证。
- 管理端、用户端、内部服务接口必须明确权限边界。
- 资源归属校验不得只依赖前端传参。
- 鉴权细则见 `docs/standards/authentication.md` 和 `rules/security.md`。

## 13. 幂等与并发 `[通用 + 条件启用]`

需要启用幂等控制的场景：

- 支付、扣减、创建订单、提交表单、导入导出、批量任务。
- 网络重试或客户端自动重试。
- Webhook 消费。
- 异步任务触发。

规则：

- POST 可通过 `Idempotency-Key` 或业务唯一键实现幂等。
- PUT/DELETE 必须具备重复调用安全性。
- 并发更新应使用版本号、更新时间、锁或业务冲突检测。
- 幂等失败与业务冲突必须返回可识别错误码。

## 14. 文件上传与媒体接口 `[条件启用]`

当项目存在上传、导入、导出、图片、视频、文档或对象存储能力时启用。

要求：

- 上传接口必须鉴权。
- 必须校验文件大小、扩展名、MIME 和文件头。
- 上传后的对象存储 key、元数据和业务对象必须一致。
- 大文件、视频或弱网场景应考虑分片上传或预签名上传。
- 细则见 `docs/standards/file_upload.md`、`docs/06-video-asset-management.md`、`docs/07-object-storage-strategy.md`。

## 15. OpenAPI 与契约 `[条件启用 + 个性化]`

当项目启用 OpenAPI 或等价契约系统时启用。

| 项 | 规则 |
|---|---|
| 契约来源 | `{OPENAPI_SOURCE}` |
| 契约输出 | `{OPENAPI_OUTPUT_PATH}` |
| 客户端生成器 | `{API_CLIENT_GENERATOR}` |
| 生成命令 | `{API_CLIENT_GENERATE_COMMAND}` |
| 生成目录 | `{API_GENERATED_DIR}` |

要求：

- 后端路由或契约定义必须包含 summary、description、tags、request、response、错误响应。
- OpenAPI 更新后必须重新生成客户端或明确说明不生成。
- 前端不得手写与契约重复的接口类型。
- 细则见 `docs/standards/openapi-rules.md`。

## 16. API 分组与标签 `[通用 + 个性化]`

API 分组必须与 `docs/03-api-index.md` 保持一致。

| 分组 | 路径前缀 | 是否认证 | 负责人 | 状态 |
|---|---|---|---|---|
| `{API_GROUP}` | `{API_GROUP_PREFIX}` | `{AUTH_REQUIRED}` | `{OWNER}` | `{STATUS}` |

生成规则：

- 分组名称必须来自项目能力，不得保留来源项目业务名。
- 每个分组必须能映射到后端模块、前端调用方或外部集成方。
- 废弃接口必须有状态、迁移说明和删除计划。

## 17. API 测试与校验 `[通用 + 个性化]`

推荐校验命令：

```bash
{API_VERIFY_COMMAND}
```

测试要求：

- API 单元测试覆盖参数校验、响应 schema、错误码。
- 集成测试覆盖认证、权限、数据库、对象存储和外部依赖。
- 契约测试覆盖 OpenAPI 输出与客户端生成。
- 安全测试覆盖越权、未认证、非法输入、上传绕过。
- 破坏性变更必须补充兼容性测试或迁移验证。

## 18. AI 修改规则 `[通用]`

AI 修改 API 时必须同步检查：

```text
rules/api.md
rules/security.md
rules/language.md
docs/03-api-index.md
docs/standards/api-governance.md
docs/standards/openapi-rules.md
docs/standards/error-codes.md
docs/standards/authentication.md
docs/standards/file_upload.md
tests/
```

要求：

- 不得只改后端接口而不更新 API 索引、契约、客户端或测试。
- 不得新增未登记的错误码。
- 不得绕过认证和权限规则新增管理能力。
- 不得保留来源项目 API 路径、资源名、角色名、生成器或技术栈。

## 19. 初始化生成建议 `[通用]`

初始化生成本文档时应执行：

1. 根据用户输入替换 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{API_PREFIX}`、`{API_STYLE}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{AUTH_STRATEGY}`、`{PERMISSION_MODEL}`、`{RESPONSE_ENVELOPE}`、`{OPENAPI_SOURCE}`、`{API_CLIENT_GENERATOR}`。
2. 保留所有 `[通用]` 模块。
3. 根据项目能力保留或删除 `[条件启用]` 模块，例如认证、OpenAPI、客户端生成、文件上传、Webhook、SDK、异步任务。
4. 用真实业务资源生成 URL 示例，不得保留来源项目资源名。
5. 未知信息标记为 `待确认`，不得编造后端路径、生成命令、客户端目录或认证策略。
6. 保持本文档与 `rules/api.md`、`docs/03-api-index.md`、`docs/standards/openapi-rules.md`、`docs/standards/error-codes.md` 一致。

## 20. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- API 风格、基础前缀、版本策略变化。
- 统一响应结构、错误码、分页、字段命名变化。
- 认证、权限、匿名访问或内部接口策略变化。
- OpenAPI 契约来源、输出路径、客户端生成方式变化。
- 新增上传、导入导出、Webhook、SDK 或外部集成。
- API 测试、校验命令或发布准入变化。
