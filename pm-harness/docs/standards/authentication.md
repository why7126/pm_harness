---
purpose: 认证与授权规范
content: 认证方式、登录登出、Token/Session、权限模型、受保护接口、前端登录态、错误码、安全测试与维护规则
source: Harness docs/standards/authentication.md 抽象模板，初始化时基于用户输入生成
update_method: 认证方案、权限模型、会话策略、前端登录态、公开端点或安全边界变化时同步更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {SECURITY_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；无登录态项目可保留为未来启用规范并标记不适用
---

# 认证与授权规范

## 0. 文档定位 `[通用]`

本文档定义项目的认证与授权治理规则，覆盖认证方式、登录登出、Token/Session、刷新与失效、受保护接口、公开端点、权限模型、前端登录态、服务间认证、错误码、安全测试和维护流程。

本文档是 `rules/security.md` 中认证授权章节的落地细则，应与 `rules/api.md`、`docs/standards/api-governance.md`、`docs/standards/error-codes.md`、`docs/03-api-index.md` 保持一致。

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{SECURITY_OWNER}` | 安全与认证负责人 | 待确认 |
| `{AUTH_ENABLED}` | 是否启用认证 | true / false |
| `{AUTH_STRATEGY}` | 认证策略 | Token / Session / OAuth2 / OIDC / SSO / API Key / none |
| `{AUTH_PROVIDER}` | 认证提供方 | 自研账号 / 企业 SSO / 第三方身份源 / none |
| `{AUTH_HEADER}` | 认证 Header 或 Cookie | `Authorization: Bearer <token>` / Cookie |
| `{TOKEN_TYPE}` | Token 类型 | access token / refresh token / session id |
| `{TOKEN_EXPIRE_POLICY}` | Token 过期策略 | 待确认 |
| `{TOKEN_REFRESH_POLICY}` | 刷新策略 | 待确认 |
| `{TOKEN_STORAGE_POLICY}` | 前端存储策略 | HttpOnly Cookie / memory / controlled storage |
| `{PASSWORD_POLICY}` | 密码策略 | 待确认 |
| `{MFA_POLICY}` | 多因素认证策略 | disabled / optional / required |
| `{PERMISSION_MODEL}` | 权限模型 | RBAC / ABAC / owner-based / tenant-based / none |
| `{ROLE_MATRIX}` | 角色矩阵 | 待确认 |
| `{PUBLIC_ENDPOINTS}` | 公开端点清单 | 健康检查、登录、回调等 |
| `{AUTH_ERROR_CODE_RANGE}` | 认证授权错误码段 | `2xxxx` / 待确认 |
| `{AUTH_TEST_COMMAND}` | 认证测试命令 | 待确认 |

## 2. 启用条件 `[通用]`

满足以下任一条件时，应完整启用本文档：

- 项目存在用户登录、管理后台、成员体系、租户体系或账号体系。
- 项目需要区分匿名用户、普通用户、管理员、内部服务或第三方调用方。
- API、前端、移动端、微信小程序、SDK 或 Webhook 需要认证、授权、签名或访问控制。
- 项目存在敏感数据、管理操作、文件下载、导入导出或计费能力。

当 `{AUTH_ENABLED}=false` 且项目无任何登录态、用户身份、服务间凭证或访问控制需求时，可保留本文档为未来启用规范，并删除强制实现和测试要求。

## 3. 认证总原则 `[通用]`

| 原则 | 说明 |
|---|---|
| 默认保护 | 除明确登记的公开端点外，业务接口默认需要认证 |
| 后端可信 | 身份、角色、权限和资源归属必须由后端或可信认证服务判断 |
| 最小授权 | 用户、角色、服务账号和第三方调用方只获得必要权限 |
| 失败安全 | 认证失败、过期、签名错误或权限不足时必须拒绝请求 |
| 明确边界 | 用户端、管理端、内部接口、开放接口和回调接口必须区分认证边界 |
| 可撤销 | 禁用用户、撤销授权、退出登录、密钥轮换后必须有明确生效策略 |
| 可测试 | 登录、登出、刷新、过期、越权、匿名访问和公开端点必须可验证 |

## 4. 认证方式 `[通用 + 个性化]`

当前认证策略：

```text
{AUTH_STRATEGY}
```

认证提供方：

```text
{AUTH_PROVIDER}
```

生成规则：

- 使用 Token 时，必须明确签发方、签名或校验方式、过期时间、刷新机制、撤销策略和传递方式。
- 使用 Session 时，必须明确 Session 存储、Cookie 属性、CSRF 防护、过期与失效策略。
- 使用 OAuth2、OIDC、SSO 或企业身份源时，必须明确回调地址、state 校验、scope、用户映射、组织映射和失败处理。
- 使用 API Key 或服务凭证时，必须明确密钥生成、展示、存储、轮换、停用、访问范围和审计规则。
- `{AUTH_STRATEGY}=none` 时，只允许公开、离线或本地工具类场景；不得用于有敏感数据或管理操作的系统。

## 5. 凭证传递 `[通用 + 个性化]`

推荐传递方式：

```text
{AUTH_HEADER}
```

通用要求：

- 禁止通过 URL query 传递长期有效 Token、Session ID、API Key 或敏感凭证。
- 禁止在日志、错误上报、埋点、截图、浏览器地址栏和前端路由中暴露凭证。
- 认证 Header、Cookie、签名参数必须在 API 文档和 OpenAPI 契约中声明。
- 内部服务、Webhook、开放 API、管理端和普通用户端应使用不同凭证边界。

## 6. 登录、登出与刷新 `[通用 + 个性化]`

登录接口模板：

```http
POST {API_PREFIX}/auth/login
Content-Type: application/json

{
  "{LOGIN_IDENTIFIER_FIELD}": "...",
  "{LOGIN_SECRET_FIELD}": "...",
  "remember_me": false
}
```

登录成功响应应包含：

| 字段 | 说明 | 是否必须 |
|---|---|---|
| `{TOKEN_FIELD}` | 访问凭证或会话标识 | 按认证策略确定 |
| `{TOKEN_TYPE_FIELD}` | 凭证类型 | 条件启用 |
| `{EXPIRES_IN_FIELD}` | 过期时间 | 条件启用 |
| `{REFRESH_TOKEN_FIELD}` | 刷新凭证 | 条件启用 |
| `{CURRENT_USER_FIELD}` | 当前用户摘要 | 建议保留 |

登出与刷新规则：

- 登出必须清理服务端会话、刷新凭证或客户端凭证状态；不能只清理前端变量。
- 刷新凭证应比访问凭证权限更窄，并具备过期、轮换和撤销策略。
- 禁用用户、修改密码、权限变更、组织移除、密钥轮换后，应明确旧凭证是否立即失效。
- 登录失败、验证码失败、多因素认证失败和锁定策略必须返回受控错误码。

## 7. Token 与 Session 生命周期 `[通用 + 个性化]`

当前策略：

| 项 | 规则 |
|---|---|
| Token 类型 | `{TOKEN_TYPE}` |
| 过期策略 | `{TOKEN_EXPIRE_POLICY}` |
| 刷新策略 | `{TOKEN_REFRESH_POLICY}` |
| 存储策略 | `{TOKEN_STORAGE_POLICY}` |
| 撤销策略 | `{TOKEN_REVOKE_POLICY}` |

生命周期要求：

- 访问凭证过期时间不得无限期。
- 刷新凭证、Session 和 API Key 必须可撤销。
- 长期凭证必须有轮换、最后使用时间、来源标识和审计记录。
- 时钟偏差、重复刷新、并发刷新和过期边界应有明确处理。
- 凭证校验失败不得泄露签名算法、密钥、内部用户状态或系统路径。

## 8. 密码与账号安全 `[条件启用 + 个性化]`

当项目使用账号密码登录时启用。

密码策略：

```text
{PASSWORD_POLICY}
```

要求：

- 密码不得明文存储、明文传输、写入日志或出现在测试夹具中。
- 密码哈希应使用安全算法和随机盐，算法参数应可升级。
- 登录失败应有频率限制、锁定或延迟策略。
- 重置密码、修改密码、绑定邮箱或手机号等敏感操作应二次确认或重新认证。
- 默认账号、演示账号和初始化管理员必须有强制改密或一次性初始化机制。

## 9. 多因素认证 `[条件启用 + 个性化]`

当 `{MFA_POLICY}` 不为 `disabled` 时启用。

要求：

- 必须明确 MFA 适用范围，例如管理员、敏感操作、远程登录或全部用户。
- 必须明确备用恢复方式和恢复操作审计。
- MFA 失败、过期、重放、绑定变更必须返回受控错误码。
- 禁止为了联调或测试在生产环境绕过 MFA。

## 10. 受保护接口与公开端点 `[通用 + 个性化]`

公开端点事实源：

```text
{PUBLIC_ENDPOINTS}
```

要求：

- 公开端点必须在 `docs/03-api-index.md` 和 OpenAPI 契约中标记。
- 未列入公开端点清单的业务接口默认需要认证。
- 健康检查、静态资源、登录、OAuth/OIDC 回调、Webhook 接收等公开能力必须单独说明保护机制。
- 管理端接口、导入导出、文件下载、批量删除、权限变更、密钥管理、配置修改等高风险接口必须鉴权并授权。
- 认证失败返回 401，权限不足返回 403，资源归属不匹配不得泄露不该知道的资源存在性。

## 11. 权限模型 `[通用 + 个性化]`

当前权限模型：

```text
{PERMISSION_MODEL}
```

角色矩阵：

| 角色/主体 | 适用端 | 允许能力 | 禁止能力 | 数据范围 | 备注 |
|---|---|---|---|---|---|
| `{ROLE_NAME}` | `{CLIENT_SCOPE}` | `{ALLOWED_ACTIONS}` | `{DENIED_ACTIONS}` | `{DATA_SCOPE}` | `{NOTE}` |

授权要求：

- 不得信任前端传入的 `user_id`、`role`、`is_admin`、`tenant_id` 或数据范围。
- 资源所有者、协作者、组织成员、租户、管理员和服务账号必须有明确判定规则。
- 权限变更、角色调整、组织切换、用户禁用后的生效时间必须明确。
- 批量操作必须对每个目标资源做权限校验，不得只校验入口权限。
- 管理端权限不得复用普通用户端的宽松判断。

## 12. 前端登录态与路由守卫 `[条件启用 + 个性化]`

当前端存在 Web、移动端、微信小程序、桌面端、管理端或开放控制台时启用。

| 项 | 规则 |
|---|---|
| 登录态存储 | `{TOKEN_STORAGE_POLICY}` |
| 登录页路径 | `{LOGIN_ROUTE}` |
| 登录后跳转 | `{AFTER_LOGIN_ROUTE}` |
| 退出登录处理 | `{LOGOUT_BEHAVIOR}` |
| 路由守卫策略 | `{ROUTE_GUARD_POLICY}` |

要求：

- 前端路由守卫只用于体验优化，后端必须执行最终认证和授权。
- 401 应进入重新登录、刷新凭证或重新认证流程。
- 403 应展示权限不足，不得自动切换身份或重复提交高风险请求。
- Token、Session、Cookie、用户摘要不得写入 URL、日志、错误上报、埋点和截图。
- 多端登录、单端登录、会话互踢、离线状态和刷新失败的行为必须明确。

## 13. 服务间认证与开放接口 `[条件启用]`

当项目存在内部服务、开放 API、Webhook、SDK、异步任务或第三方集成时启用。

要求：

- 服务间调用必须使用受控凭证、签名、mTLS、网关身份或其他明确机制。
- Webhook 必须校验来源、签名、时间戳和重放窗口。
- API Key、Webhook Secret、服务账号凭证必须支持停用、轮换、权限范围和审计。
- 开放接口必须限制访问范围、调用频率、过期时间和错误回显。
- 内部管理接口不得因为部署在内网就跳过认证授权。

## 14. 错误码与响应 `[通用 + 个性化]`

认证授权错误码段：

```text
{AUTH_ERROR_CODE_RANGE}
```

推荐分类：

| 场景 | HTTP 状态 | 说明 |
|---|---|---|
| 未登录或凭证缺失 | 401 | 客户端需要登录或提供凭证 |
| 凭证过期 | 401 | 客户端可刷新或重新登录 |
| 凭证无效 | 401 | Token、Session、签名或 API Key 不合法 |
| 权限不足 | 403 | 已认证但不具备操作权限 |
| 账号禁用或锁定 | 403 | 主体不可继续访问 |
| 登录参数错误 | 400 | 请求体或登录字段不合法 |
| 登录失败 | 401 | 账号或密码等认证要素不匹配 |
| 频率限制 | 429 | 登录、刷新、验证码或敏感接口触发限流 |

要求：

- 错误码必须同步 `docs/standards/error-codes.md`。
- 认证错误不得暴露账号是否存在、密码规则细节、签名算法、密钥、内部用户状态或系统路径。
- 前端应基于错误码处理登录过期、权限不足、账号锁定和重新认证。

## 15. 测试与验收 `[通用 + 个性化]`

认证测试命令：

```bash
{AUTH_TEST_COMMAND}
```

测试要求：

- 登录成功、登录失败、登出、刷新、过期、撤销、禁用用户必须覆盖。
- 未认证访问受保护接口必须返回 401。
- 权限不足访问受保护资源必须返回 403 或项目约定错误码。
- 公开端点必须可匿名访问，但不得暴露敏感数据。
- 批量操作、文件下载、导入导出、管理操作必须覆盖越权测试。
- 前端路由守卫、401/403 处理、退出登录和刷新失败必须覆盖。
- 服务间凭证、Webhook 签名、API Key 轮换等条件启用能力必须有测试或人工验收步骤。

## 16. AI 修改规则 `[通用]`

AI 修改认证与授权相关内容时必须同步检查：

```text
rules/security.md
rules/api.md
docs/03-api-index.md
docs/standards/api-governance.md
docs/standards/authentication.md
docs/standards/error-codes.md
docs/standards/openapi-rules.md
tests/
```

要求：

- 不得为了联调、演示或通过测试而绕过认证、伪造当前用户、关闭权限校验。
- 不得新增未登记的公开端点。
- 不得新增未登记的角色、权限、错误码或凭证传递方式。
- 不得把认证状态只放在前端判断。
- 不得保留来源项目角色、路径、函数名、框架依赖或认证实现细节。

## 17. 初始化生成建议 `[通用]`

初始化生成本文档时应执行：

1. 根据用户输入替换 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{AUTH_ENABLED}`、`{AUTH_STRATEGY}`、`{AUTH_PROVIDER}`、`{AUTH_HEADER}`、`{TOKEN_STORAGE_POLICY}`、`{PERMISSION_MODEL}`、`{ROLE_MATRIX}`。
2. 保留所有 `[通用]` 模块。
3. 根据项目能力保留或删除 `[条件启用]` 模块，例如密码登录、MFA、前端登录态、服务间认证、Webhook、API Key、SSO。
4. 用真实端点、角色、权限和错误码替换示例占位；未知信息标记为 `待确认`。
5. 不得编造认证提供方、角色体系、Token 过期时间、刷新策略或公开端点。
6. 保持本文档与 `rules/security.md`、`rules/api.md`、`docs/03-api-index.md`、`docs/standards/api-governance.md`、`docs/standards/error-codes.md` 一致。

## 18. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- 认证策略、认证提供方、凭证传递方式变化。
- 登录、登出、刷新、Token/Session 生命周期变化。
- 新增或删除公开端点、管理端、开放接口、Webhook 或服务间调用。
- 角色、权限、租户、组织、资源归属或数据范围规则变化。
- 前端登录态、路由守卫、401/403 处理策略变化。
- 错误码、OpenAPI 契约、API 分组或安全测试要求变化。
