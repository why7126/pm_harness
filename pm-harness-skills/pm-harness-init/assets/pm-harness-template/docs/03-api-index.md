---
purpose: API 接口索引
content: API 分组、基础约定、认证授权、响应结构、错误码、OpenAPI、客户端生成、接口维护规则
source: Harness docs/03-api-index.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；API 新增、变更、废弃、错误码调整或客户端生成规则变化时更新；后续由 AI 辅助更新并经人工 Review
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {API_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 docs/03-api-index.md 模块
---

# API 接口索引

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如认证、前端客户端生成、文件上传、Webhook、SDK、外部集成。

## 0. 文档定位 `[通用]`

本文是 `{PRODUCT_NAME}` 的 API 索引入口，用于让研发、测试、前端、移动端、SDK、外部集成和 AI Agent 快速定位接口分组、基础约定、契约来源、错误码和维护规则。

本文不替代完整接口规范：

- API 设计规则见 `rules/api.md`。
- 错误码治理见 `{ERROR_CODE_DOC_PATH}`。
- OpenAPI 或接口契约来源见 `{OPENAPI_SOURCE}`。
- API 变更的需求与规格见 `issues/requirements/`、`openspec/changes/`、`openspec/specs/`。
- 数据模型和持久化设计见 `docs/04-database-design.md`。

## 1. 生成参数 `[个性化]`

初始化生成本文时，应优先使用用户输入填充以下参数。缺失信息可以标记为 `待确认`，不得编造接口事实。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{API_PREFIX}` | API 基础路径 | `/api/v1` 或待确认 |
| `{BACKEND_STACK}` | 后端技术栈 | 待确认 |
| `{FRONTEND_STACK}` | 前端技术栈 | 待确认 |
| `{AUTH_STRATEGY}` | 认证策略 | 待确认 |
| `{PERMISSION_MODEL}` | 权限模型 | 待确认 |
| `{RESPONSE_ENVELOPE}` | 统一响应结构 | 待确认 |
| `{ERROR_CODE_DOC_PATH}` | 错误码文档路径 | 待确认 |
| `{OPENAPI_SOURCE}` | OpenAPI 或接口契约来源 | 待确认 |
| `{API_DOC_PATH}` | Swagger、Scalar、Redoc 或其他 API 文档入口 | 待确认 |
| `{API_CLIENT_GENERATOR}` | 客户端生成工具 | 待确认 |
| `{API_CLIENT_GENERATE_COMMAND}` | 客户端生成命令 | 待确认 |
| `{API_GENERATED_DIR}` | 生成代码目录 | 待确认 |
| `{API_GROUPS}` | API 分组清单 | 待确认 |
| `{API_OWNER}` | API 文档负责人 | 待确认 |

## 2. 通用约定 `[通用 + 个性化]`

### 2.1 基础路径 `[个性化]`

```text
{API_PREFIX}
```

如果 API 前缀尚未确认，初始化时可使用 `/api/v1` 作为建议值，并标记为 `待确认`。

### 2.2 协议与格式 `[通用 + 个性化]`

| 项 | 约定 |
|---|---|
| 协议 | `{API_PROTOCOL}` |
| 数据格式 | `{API_DATA_FORMAT}` |
| 字段命名 | `{API_FIELD_CASE}` |
| 时间格式 | `{API_TIME_FORMAT}` |
| 分页方式 | `{PAGINATION_POLICY}` |
| 排序/筛选 | `{SORT_FILTER_POLICY}` |
| 幂等策略 | `{IDEMPOTENCY_POLICY}` |
| 版本策略 | `{API_VERSION_POLICY}` |

### 2.3 统一响应结构 `[通用 + 个性化]`

成功响应：

```json
{SUCCESS_RESPONSE_EXAMPLE}
```

错误响应：

```json
{ERROR_RESPONSE_EXAMPLE}
```

响应结构必须与 `rules/api.md` 保持一致。如果项目不使用统一 envelope，应在本节明确哪些接口返回裸模型、原因、迁移计划和兼容策略。

### 2.4 认证头与公共请求头 `[条件启用]`

需认证接口的请求头：

```http
{AUTH_HEADER_EXAMPLE}
```

公共请求头：

| Header | 必填 | 说明 |
|---|---:|---|
| `{HEADER_NAME_1}` | `{HEADER_REQUIRED_1}` | `{HEADER_DESCRIPTION_1}` |
| `{HEADER_NAME_2}` | `{HEADER_REQUIRED_2}` | `{HEADER_DESCRIPTION_2}` |

## 3. OpenAPI 与契约来源 `[通用 + 个性化]`

| 资源 | 路径/命令 | 说明 |
|---|---|---|
| OpenAPI / 契约源 | `{OPENAPI_SOURCE}` | 接口契约事实来源 |
| API 文档入口 | `{API_DOC_PATH}` | Swagger、Redoc、Scalar 或其他入口 |
| 健康检查 | `{HEALTHCHECK_ENDPOINT}` | 服务可用性检查 |
| 契约校验 | `{API_CONTRACT_VALIDATE_COMMAND}` | 校验契约与实现 |

契约规则：

- API 新增、修改、删除必须先更新 OpenSpec 或项目约定的契约来源。
- 前端、移动端、微信小程序、SDK 或第三方依赖的接口不得无兼容策略直接变更。
- OpenAPI 与运行时实现、测试、客户端生成结果必须保持一致。

## 4. 客户端生成 `[条件启用]`

当前客户端生成方案：

```text
{API_CLIENT_GENERATOR}
```

生成命令：

```bash
{API_CLIENT_GENERATE_COMMAND}
```

生成位置：

```text
{API_GENERATED_DIR}
```

维护要求：

- API 契约变更后必须重新生成客户端。
- 生成代码目录必须写入 `rules/directory-structure.md` 的生成代码边界。
- 不得手写修改生成代码；如必须修改，需记录原因并调整生成配置。
- 生成结果影响前端、移动端、微信小程序或 SDK 时，必须补充调用方验证。

未启用客户端生成时，应删除本节，保留契约同步要求。

## 5. API 分组 `[通用 + 个性化]`

初始化时应根据 `{API_GROUPS}` 生成真实分组。未实现、规划中或废弃接口必须标明状态。

| 分组 | 路径前缀 | 认证 | 主要职责 | 状态 | 契约/规格 |
|---|---|---|---|---|---|
| `{API_GROUP_1}` | `{API_GROUP_PREFIX_1}` | `{API_GROUP_AUTH_1}` | `{API_GROUP_DESCRIPTION_1}` | `{API_GROUP_STATUS_1}` | `{API_GROUP_SPEC_1}` |
| `{API_GROUP_2}` | `{API_GROUP_PREFIX_2}` | `{API_GROUP_AUTH_2}` | `{API_GROUP_DESCRIPTION_2}` | `{API_GROUP_STATUS_2}` | `{API_GROUP_SPEC_2}` |

状态建议：

- `planned`：已规划，尚未实现。
- `stub`：桩实现或示例返回。
- `implemented`：已实现并有测试。
- `deprecated`：已废弃，保留兼容。
- `removed`：已移除。

## 6. 接口清单模板 `[通用]`

每个 API 分组应使用以下结构维护接口清单。

### 6.1 `{API_GROUP_NAME}` `[个性化]`

实现位置：

```text
{API_IMPLEMENTATION_PATH}
```

契约来源：

```text
{API_SPEC_PATH}
```

| 方法 | 路径 | 认证 | 请求 | 响应 | 状态 | 说明 |
|---|---|---|---|---|---|---|
| `{METHOD_1}` | `{PATH_1}` | `{AUTH_1}` | `{REQUEST_MODEL_1}` | `{RESPONSE_MODEL_1}` | `{STATUS_1}` | `{DESCRIPTION_1}` |
| `{METHOD_2}` | `{PATH_2}` | `{AUTH_2}` | `{REQUEST_MODEL_2}` | `{RESPONSE_MODEL_2}` | `{STATUS_2}` | `{DESCRIPTION_2}` |

关键查询参数：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `{QUERY_NAME_1}` | `{QUERY_TYPE_1}` | `{QUERY_REQUIRED_1}` | `{QUERY_DEFAULT_1}` | `{QUERY_DESCRIPTION_1}` |

关键请求体：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `{BODY_FIELD_1}` | `{BODY_TYPE_1}` | `{BODY_REQUIRED_1}` | `{BODY_DESCRIPTION_1}` |

关键响应：

| 字段 | 类型 | 说明 |
|---|---|---|
| `{RESPONSE_FIELD_1}` | `{RESPONSE_TYPE_1}` | `{RESPONSE_DESCRIPTION_1}` |

错误码：

| HTTP | code | 场景 | 说明 |
|---|---|---|---|
| `{HTTP_STATUS_1}` | `{ERROR_CODE_1}` | `{ERROR_SCENARIO_1}` | `{ERROR_DESCRIPTION_1}` |

## 7. 认证与权限 `[条件启用]`

认证策略：

```text
{AUTH_STRATEGY}
```

权限模型：

```text
{PERMISSION_MODEL}
```

角色与 API 权限：

| 角色 | 可访问分组 | 禁止访问 | 说明 |
|---|---|---|---|
| `{ROLE_1}` | `{ROLE_1_ALLOWED}` | `{ROLE_1_DENIED}` | `{ROLE_1_NOTE}` |
| `{ROLE_2}` | `{ROLE_2_ALLOWED}` | `{ROLE_2_DENIED}` | `{ROLE_2_NOTE}` |

认证与权限变化必须同步：

- `rules/security.md`
- `docs/standards/authentication.md` 或项目实际认证文档
- API 契约
- 集成测试和安全测试

## 8. 文件上传与媒体接口 `[条件启用]`

当项目启用上传、媒体、对象存储或导入导出时保留本节。

| 接口 | 方法 | 路径 | 认证 | 文件字段 | 限制 | 存储策略 |
|---|---|---|---|---|---|---|
| `{UPLOAD_API_1}` | `{UPLOAD_METHOD_1}` | `{UPLOAD_PATH_1}` | `{UPLOAD_AUTH_1}` | `{UPLOAD_FIELD_1}` | `{UPLOAD_LIMIT_1}` | `{UPLOAD_STORAGE_1}` |

维护要求：

- 上传大小、MIME、扩展名、扫描、鉴权、签名 URL 必须与 `rules/media.md` 和 `rules/object-storage.md` 一致。
- 对象 key、bucket、前缀策略必须与对象存储文档一致。
- 文件元数据落库时必须同步 `docs/04-database-design.md`。

## 9. 异步任务、Webhook 与外部集成 `[条件启用]`

### 9.1 异步任务 API

| 接口 | 方法 | 路径 | 功能 | 状态追踪 | 幂等/重试 |
|---|---|---|---|---|---|
| `{ASYNC_API_1}` | `{ASYNC_METHOD_1}` | `{ASYNC_PATH_1}` | `{ASYNC_DESCRIPTION_1}` | `{ASYNC_STATUS_POLICY_1}` | `{ASYNC_RETRY_POLICY_1}` |

### 9.2 Webhook

| Webhook | 方向 | 事件 | 签名 | 重试 | 契约 |
|---|---|---|---|---|---|
| `{WEBHOOK_1}` | `{WEBHOOK_DIRECTION_1}` | `{WEBHOOK_EVENTS_1}` | `{WEBHOOK_SIGNATURE_1}` | `{WEBHOOK_RETRY_1}` | `{WEBHOOK_CONTRACT_1}` |

### 9.3 外部服务

| 外部服务 | 用途 | 协议 | 鉴权 | 超时 | 降级 |
|---|---|---|---|---|---|
| `{EXTERNAL_SERVICE_1}` | `{EXTERNAL_PURPOSE_1}` | `{EXTERNAL_PROTOCOL_1}` | `{EXTERNAL_AUTH_1}` | `{EXTERNAL_TIMEOUT_1}` | `{EXTERNAL_FALLBACK_1}` |

## 10. 错误码速查 `[通用 + 个性化]`

完整错误码登记见：

```text
{ERROR_CODE_DOC_PATH}
```

| HTTP | code | 常量/标识 | 典型 message | 场景 |
|---|---|---|---|---|
| `{HTTP_STATUS_1}` | `{ERROR_CODE_1}` | `{ERROR_SYMBOL_1}` | `{ERROR_MESSAGE_1}` | `{ERROR_SCENARIO_1}` |
| `{HTTP_STATUS_2}` | `{ERROR_CODE_2}` | `{ERROR_SYMBOL_2}` | `{ERROR_MESSAGE_2}` | `{ERROR_SCENARIO_2}` |

错误码规则：

- 新增错误码必须先登记。
- 同一错误码不得表达多个语义。
- 对外 message 不得泄漏密钥、SQL、堆栈、内部路径或敏感数据。

## 11. 版本、兼容与废弃策略 `[通用 + 个性化]`

| 项 | 策略 |
|---|---|
| API 版本 | `{API_VERSION_POLICY}` |
| 兼容窗口 | `{API_COMPAT_WINDOW}` |
| 废弃标记 | `{API_DEPRECATION_POLICY}` |
| 移除流程 | `{API_REMOVAL_POLICY}` |
| 客户端同步 | `{CLIENT_SYNC_POLICY}` |

破坏性变更必须：

1. 创建或更新 OpenSpec Change。
2. 标明影响的调用方。
3. 提供迁移策略或兼容窗口。
4. 补充契约测试和回归测试。
5. 更新本文和相关客户端。

## 12. API 测试要求 `[通用 + 个性化]`

| 测试类型 | 路径/命令 | 说明 |
|---|---|---|
| 契约测试 | `{CONTRACT_TEST_COMMAND}` | 校验契约与实现一致 |
| 集成测试 | `{API_INTEGRATION_TEST_COMMAND}` | 覆盖核心 API 流程 |
| 权限测试 | `{API_AUTH_TEST_COMMAND}` | 覆盖未登录、越权、禁用角色 |
| 错误码测试 | `{ERROR_CODE_TEST_COMMAND}` | 验证错误响应 |
| 客户端生成测试 | `{CLIENT_GENERATION_TEST_COMMAND}` | 验证生成代码可用 |

API 变更后必须根据影响面补充或更新测试。无法运行测试时必须说明原因和风险。

## 13. 维护规则 `[通用]`

API 新增、修改、废弃或删除时必须：

1. 更新需求或 BUG 文档。
2. 更新 `openspec/changes/*/specs/` 或已归档 `openspec/specs/`。
3. 更新 `rules/api.md` 中相关约定（如规则变化）。
4. 更新本文的 API 分组、接口清单、错误码、权限、客户端生成信息。
5. 更新 OpenAPI 或项目契约来源。
6. 重新生成客户端（如启用）。
7. 补充契约测试、集成测试、权限测试或回归测试。
8. 同步前端、移动端、微信小程序、SDK、外部集成或文档。

## 14. 相关文档 `[通用]`

| 文档 | 说明 |
|---|---|
| `rules/api.md` | API 设计与维护强制规则 |
| `{API_GOVERNANCE_DOC_PATH}` | API 治理细则 |
| `{ERROR_CODE_DOC_PATH}` | 错误码登记与分段规则 |
| `{OPENAPI_RULES_DOC_PATH}` | OpenAPI 注解、生成和校验规则 |
| `{AUTH_DOC_PATH}` | 认证与权限说明 |
| `{FILE_UPLOAD_DOC_PATH}` | 文件上传和对象存储接口说明 |
| `docs/01-architecture.md` | API 在系统架构中的位置 |
| `docs/04-database-design.md` | API 涉及的数据模型 |
| `rules/testing.md` | API 测试要求 |
| `rules/security.md` | API 安全要求 |

## 15. 初始化生成建议 `[通用]`

工程初始化工具生成本文时应遵循：

1. 保留所有 `[通用]` 模块。
2. 用用户输入替换所有 `[个性化]` 占位符。
3. 根据项目能力保留或删除 `[条件启用]` 模块。
4. 根据 `{API_GROUPS}` 生成真实 API 分组，不得保留来源项目业务资源。
5. 根据 `{AUTH_STRATEGY}` 和 `{PERMISSION_MODEL}` 生成认证权限章节；无认证时标记公开 API 边界。
6. 根据 `{OPENAPI_SOURCE}` 和 `{API_CLIENT_GENERATOR}` 生成契约与客户端生成章节；未启用客户端生成时删除硬性生成命令。
7. 根据媒体、对象存储、Webhook、SDK、外部集成能力保留或删除对应章节。
8. 未确认信息标记为 `待确认`。
9. 不得保留来源项目的接口路径、资源名、角色名、错误 message、脚本路径或生成目录。
10. 生成后检查本文是否能回答：
   - API 基础路径是什么？
   - 有哪些 API 分组？
   - 哪些接口需要认证和权限？
   - 契约来源在哪里？
   - 变更 API 后如何同步客户端和测试？
