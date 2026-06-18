---
purpose: API 错误码治理
content: 错误码分段、命名、HTTP 映射、响应结构、登记流程、实现同步、测试与维护规则
source: Harness docs/standards/error-codes.md 抽象模板，初始化时基于用户输入生成
update_method: 新增、删除、调整错误码或响应结构时同步更新
owner: {API_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；错误码必须与 API、认证、安全、前端处理和测试保持一致
---

# 错误码体系

## 0. 文档定位 `[通用]`

本文档定义项目错误码的治理规则，覆盖错误码分段、HTTP 状态映射、错误响应结构、错误码登记表、命名与消息规范、实现同步、前端处理、测试验收和 AI 修改边界。

本文档是 `rules/api.md` 中错误码规则的事实源，应与 `docs/standards/api-governance.md`、`docs/standards/authentication.md`、`docs/03-api-index.md`、`docs/standards/openapi-rules.md` 保持一致。

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{API_OWNER}` | API 治理负责人 | 待确认 |
| `{ERROR_CODE_STYLE}` | 错误码风格 | numeric / string / mixed |
| `{SUCCESS_CODE}` | 成功码 | `0` |
| `{RESPONSE_ENVELOPE}` | 统一响应结构 | `{ code, message, data }` |
| `{ERROR_CODE_RANGES}` | 错误码分段规则 | 待确认 |
| `{AUTH_ERROR_CODE_RANGE}` | 认证授权错误码段 | 待确认 |
| `{BUSINESS_ERROR_CODE_RANGE}` | 业务错误码段 | 待确认 |
| `{PARAMETER_ERROR_CODE_RANGE}` | 参数错误码段 | 待确认 |
| `{DEPENDENCY_ERROR_CODE_RANGE}` | 外部依赖错误码段 | 待确认 |
| `{ERROR_CODE_IMPL_PATH}` | 错误码常量实现路径 | 待确认 |
| `{EXCEPTION_IMPL_PATH}` | 异常与响应处理路径 | 待确认 |
| `{FRONTEND_ERROR_HANDLER_PATH}` | 前端错误处理路径 | 待确认 |
| `{ERROR_CODE_TEST_COMMAND}` | 错误码校验命令 | 待确认 |

## 2. 启用条件 `[通用]`

满足以下任一条件时，应完整启用本文档：

- 项目暴露 API、SDK、Webhook、RPC、GraphQL 或对外集成能力。
- 项目有前端、移动端、小程序或第三方调用方需要基于错误码处理状态。
- 项目存在认证、权限、业务校验、参数校验、上传、外部依赖、异步任务或导入导出。
- 项目需要统一错误响应、日志排障、用户提示、测试断言或兼容治理。

无 API 或无错误响应治理需求的项目可保留本文档为未来启用规范，并标记为“不适用”。

## 3. 设计原则 `[通用]`

| 原则 | 说明 |
|---|---|
| 唯一性 | 一个错误码只能表达一个稳定含义 |
| 稳定性 | 已发布错误码不得随意改含义、复用或删除 |
| 可机器判断 | 客户端必须能根据错误码稳定处理分支 |
| 可排障 | message、trace_id、日志和文档应能帮助定位问题 |
| 不泄密 | 错误响应不得暴露密钥、Token、SQL、堆栈、内部路径或敏感数据 |
| 可测试 | 新增错误码必须有测试或人工验收步骤 |
| 文档先行 | 新增或调整错误码必须先登记，再实现和测试 |

## 4. 错误响应结构 `[通用 + 个性化]`

当前统一响应结构：

```json
{RESPONSE_ENVELOPE}
```

推荐错误响应：

```json
{
  "code": "{ERROR_CODE}",
  "message": "{ERROR_MESSAGE}",
  "data": null,
  "trace_id": "{TRACE_ID}"
}
```

要求：

- 成功响应和失败响应必须使用同一套 envelope 或明确兼容策略。
- `code` 或等价字段必须可机器判断。
- `message` 应用于排障和前端提示映射，不得包含敏感实现细节。
- `trace_id`、`request_id` 或等价字段建议用于日志关联。
- 字段命名必须与 `rules/language.md` 保持一致。

## 5. 分段规则 `[通用 + 个性化]`

默认建议使用数字分段。初始化时可根据 `{ERROR_CODE_STYLE}` 和 `{ERROR_CODE_RANGES}` 调整。

| 区间/前缀 | 含义 | 是否通用 | 负责人 | 备注 |
|---|---|---|---|---|
| `{SUCCESS_CODE}` | 成功 | 通用 | `{API_OWNER}` | 默认成功 |
| `1xxxx` | 系统错误 | 通用 | `{API_OWNER}` | 未预期异常、服务内部错误 |
| `{AUTH_ERROR_CODE_RANGE}` | 认证授权 | 条件启用 | `{SECURITY_OWNER}` | 登录、Token、权限、账号状态 |
| `{BUSINESS_ERROR_CODE_RANGE}` | 业务错误 | 个性化 | `{BUSINESS_OWNER}` | 按业务域生成 |
| `{PARAMETER_ERROR_CODE_RANGE}` | 参数错误 | 通用 | `{API_OWNER}` | 参数格式、分页、枚举、字段校验 |
| `{DEPENDENCY_ERROR_CODE_RANGE}` | 外部依赖 | 条件启用 | `{INFRA_OWNER}` | 存储、第三方服务、消息队列等 |

规则：

- 错误码区间必须与业务域、认证域、参数域、外部依赖域边界一致。
- 业务错误码必须按项目真实核心能力生成，不得保留来源项目业务资源。
- 外部依赖错误码应使用通用依赖类型，初始化时再替换为项目实际依赖。
- 保留未使用区间时必须标记为“预留”，不得伪造已实现错误。

## 6. HTTP 状态映射 `[通用]`

| HTTP 状态 | 使用场景 | 说明 |
|---|---|---|
| 200 | 业务成功 | 如项目约定错误也返回 200，必须在 API 治理文档中说明 |
| 400 | 参数错误、请求格式错误 | 客户端请求不符合契约 |
| 401 | 未认证、凭证缺失、凭证过期或无效 | 客户端需登录、刷新或重新认证 |
| 403 | 已认证但权限不足、账号禁用、越权访问 | 不应泄露资源是否存在 |
| 404 | 资源不存在或不可见 | 可用于隐藏无权资源存在性 |
| 409 | 资源冲突、重复提交、状态冲突 | 适用于唯一性、版本冲突、幂等冲突 |
| 422 | 语义校验失败 | 可选，适用于复杂校验 |
| 429 | 限流、登录尝试过多、高成本接口保护 | 应说明重试策略 |
| 500 | 未预期系统错误 | 不得暴露内部细节 |
| 502/503/504 | 外部依赖、网关、服务不可用或超时 | 应区分可重试与不可重试 |

## 7. 已登记错误码 `[通用 + 个性化]`

初始化后，所有已实现或计划实现的错误码必须登记在下表。

| 错误码 | HTTP | 分组 | 名称 | 用户提示 | 开发说明 | 是否可重试 | 前端处理 | 状态 |
|---|---|---|---|---|---|---|---|---|
| `{SUCCESS_CODE}` | 200 | success | success | 操作成功 | 成功响应 | 否 | 正常处理 | active |
| `{ERROR_CODE}` | `{HTTP_STATUS}` | `{ERROR_GROUP}` | `{ERROR_NAME}` | `{USER_MESSAGE}` | `{DEV_MESSAGE}` | `{RETRYABLE}` | `{FRONTEND_ACTION}` | `{STATUS}` |

状态说明：

- `active`：当前可用。
- `reserved`：已预留但未实现。
- `deprecated`：已废弃但仍需兼容。
- `removed`：已删除，仅保留历史记录，不得继续返回。

## 8. 通用错误码建议 `[通用]`

初始化时可保留以下通用错误码，也可按项目分段策略调整：

| 错误码 | HTTP | 分组 | 名称 | 说明 |
|---|---|---|---|---|
| `0` | 200 | success | success | 成功 |
| `10001` | 500 | system | internal_error | 系统内部错误 |
| `10002` | 503 | system | service_unavailable | 服务不可用 |
| `10003` | 504 | system | request_timeout | 请求处理超时 |
| `20001` | 401 | auth | unauthenticated | 未登录或凭证缺失 |
| `20002` | 401 | auth | invalid_credential | 凭证无效 |
| `20003` | 401 | auth | credential_expired | 凭证过期 |
| `20004` | 403 | auth | permission_denied | 权限不足 |
| `20005` | 403 | auth | account_disabled | 账号不可用 |
| `40001` | 400 | parameter | invalid_parameter | 请求参数无效 |
| `40002` | 400 | parameter | invalid_pagination | 分页参数无效 |
| `40003` | 400 | parameter | invalid_sort | 排序字段无效 |
| `50001` | 502 | dependency | dependency_unavailable | 外部依赖不可用 |
| `50002` | 504 | dependency | dependency_timeout | 外部依赖超时 |

要求：

- 以上仅为通用建议，初始化时必须根据项目分段策略确认是否保留。
- 未启用认证、分页或外部依赖时，应删除或标记对应错误码为“不适用”。
- 业务错误码必须来自需求、API 设计或业务规则，不得照搬来源项目错误。

## 9. 命名与消息规范 `[通用]`

错误名称：

- 推荐使用稳定的英文标识，例如 `invalid_parameter`、`permission_denied`。
- 名称应表达错误类型，不应包含动态业务值。
- 同一错误码的名称、HTTP 状态、含义和前端处理不得随意变化。

用户提示：

- 面向用户的提示应清晰、克制、可操作。
- 不得暴露账号是否存在、权限内部规则、存储路径、SQL、对象 key、Token、签名或堆栈。
- 多语言项目应将用户提示交给 i18n 或前端文案体系管理。

开发说明：

- 可包含排障方向、常见原因、日志关键词和关联 trace。
- 不得包含真实密钥、生产配置、用户隐私、完整请求体或敏感返回值。

## 10. 实现同步 `[通用 + 个性化]`

错误码常量实现路径：

```text
{ERROR_CODE_IMPL_PATH}
```

异常与响应处理路径：

```text
{EXCEPTION_IMPL_PATH}
```

前端错误处理路径：

```text
{FRONTEND_ERROR_HANDLER_PATH}
```

要求：

- 文档、后端常量、异常处理、OpenAPI、前端错误处理和测试必须同步。
- 禁止在业务代码中直接散落魔法数字或未登记字符串错误码。
- 后端应提供统一异常类型或错误响应构造方式。
- 前端应基于错误码处理登录过期、权限不足、参数错误、业务冲突、可重试依赖错误。
- OpenAPI 应声明主要错误响应结构和常见错误码。

## 11. 新增与变更流程 `[通用]`

新增错误码流程：

1. 确认错误场景是否已有可复用错误码。
2. 选择合适分组和区间。
3. 在本文档登记错误码、HTTP 状态、名称、用户提示、开发说明、前端处理和状态。
4. 同步后端常量、异常处理、API 文档、OpenAPI 和前端处理。
5. 补充单元测试、集成测试或人工验收步骤。

变更规则：

- 已发布错误码不得复用为其他含义。
- 修改 HTTP 状态、message、前端处理或可重试语义属于兼容性变更，必须评估影响。
- 废弃错误码必须保留兼容期，并标记替代错误码。
- 删除错误码必须确认无客户端依赖，并同步兼容性矩阵或发布说明。

## 12. 测试与验收 `[通用 + 个性化]`

错误码校验命令：

```bash
{ERROR_CODE_TEST_COMMAND}
```

测试要求：

- 参数错误、认证错误、权限错误、业务错误、外部依赖错误必须覆盖。
- 每个已登记错误码至少应有单元测试、集成测试或契约测试之一覆盖。
- 未登记错误码不得从 API 返回。
- 统一响应 envelope 必须在成功和失败场景中保持一致。
- 前端必须覆盖 401、403、参数错误、业务冲突、可重试外部依赖错误的处理。
- OpenAPI、接口文档和错误码登记表必须一致。

## 13. AI 修改规则 `[通用]`

AI 新增或修改错误码时必须同步检查：

```text
rules/api.md
rules/security.md
docs/03-api-index.md
docs/standards/api-governance.md
docs/standards/authentication.md
docs/standards/error-codes.md
docs/standards/openapi-rules.md
tests/
```

要求：

- 不得随意使用未登记数字、字符串或临时错误码。
- 不得复用已有错误码表达新含义。
- 不得只改后端而不同步文档、OpenAPI、前端处理和测试。
- 不得在错误 message 中泄露敏感信息。
- 不得保留来源项目业务错误、依赖名称、实现路径或技术栈。

## 14. 初始化生成建议 `[通用]`

初始化生成本文档时应执行：

1. 根据用户输入替换 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{ERROR_CODE_STYLE}`、`{SUCCESS_CODE}`、`{RESPONSE_ENVELOPE}`、`{ERROR_CODE_RANGES}`。
2. 保留所有 `[通用]` 模块。
3. 根据项目能力保留或删除 `[条件启用]` 错误码，例如认证授权、外部依赖、上传、对象存储、异步任务、支付、短信、LLM、Webhook。
4. 根据产品能力、需求和 API 设计生成业务错误码；未知时标记为 `待确认`。
5. 用项目真实实现路径替换 `{ERROR_CODE_IMPL_PATH}`、`{EXCEPTION_IMPL_PATH}`、`{FRONTEND_ERROR_HANDLER_PATH}`；未知时标记为 `待确认`。
6. 不得编造业务错误、外部依赖、错误码实现路径或前端处理路径。

## 15. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- 新增、删除、废弃或调整错误码。
- 统一响应结构、HTTP 状态映射或字段命名变化。
- 认证、权限、业务规则、参数校验、上传、外部依赖或异步任务新增错误场景。
- 后端异常处理、前端错误处理、OpenAPI 契约或测试命令变化。
- 发布兼容策略、SDK、Webhook、第三方集成对错误码有新增要求。
