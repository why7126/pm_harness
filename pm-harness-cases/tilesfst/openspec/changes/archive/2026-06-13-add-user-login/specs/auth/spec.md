## ADDED Requirements

### Requirement: 用户账号密码登录

系统 MUST 提供 `POST /api/v1/auth/login` 接口，接受 `username`、`password` 和可选 `remember_me` 字段，校验通过后返回 JWT access token 与用户基本信息。

#### Scenario: 登录成功

- **WHEN** 用户提供正确的 username 和 password，且用户 status 为 `active`
- **THEN** 系统返回 HTTP 200，包含 `access_token`、`token_type`（Bearer）、`expires_in` 和用户对象（id、username、display_name、role、status）
- **AND** 系统更新用户 `last_login_at` 字段

#### Scenario: 账号或密码错误

- **WHEN** 用户提供错误的 username 或 password
- **THEN** 系统返回 HTTP 401，错误码 `AUTH_INVALID_CREDENTIALS`，消息为「账号或密码错误」
- **AND** 响应不得区分「用户不存在」与「密码错误」

#### Scenario: 用户被禁用

- **WHEN** 用户提供正确的凭证但用户 status 为 `disabled`
- **THEN** 系统返回 HTTP 403，错误码 `AUTH_USER_DISABLED`，消息为「账号已停用，请联系管理员」

#### Scenario: 请求参数无效

- **WHEN** 请求体缺少 username 或 password，或字段为空
- **THEN** 系统返回 HTTP 400，错误码 `AUTH_INVALID_REQUEST`

#### Scenario: remember_me 延长有效期

- **WHEN** 用户设置 `remember_me` 为 true 且登录成功
- **THEN** 系统签发的 token 有效期 MUST 为 7 天

#### Scenario: 默认 token 有效期

- **WHEN** 用户未设置 `remember_me` 或设为 false 且登录成功
- **THEN** 系统签发的 token 有效期 MUST 为 2 小时

### Requirement: 密码安全存储

系统 MUST 使用 bcrypt 算法哈希存储用户密码，数据库中 MUST NOT 存在明文密码。

#### Scenario: 密码哈希验证

- **WHEN** 系统创建或验证用户密码
- **THEN** 系统 MUST 使用 passlib bcrypt 进行哈希与校验
- **AND** 日志与 API 响应 MUST NOT 包含明文密码

### Requirement: 当前用户信息查询

系统 MUST 提供 `GET /api/v1/auth/me` 接口，返回当前已认证用户的信息。

#### Scenario: 已登录用户查询

- **WHEN** 请求携带有效 Bearer token
- **THEN** 系统返回 HTTP 200，包含用户 id、username、display_name、role、status

#### Scenario: 未登录或 token 无效

- **WHEN** 请求未携带 token 或 token 已过期/无效
- **THEN** 系统返回 HTTP 401

#### Scenario: 用户被禁用后 token 仍有效

- **WHEN** 用户 status 变为 `disabled` 后携带旧 token 请求
- **THEN** 系统返回 HTTP 403，错误码 `AUTH_USER_DISABLED`

### Requirement: 退出登录

系统 MUST 提供 `POST /api/v1/auth/logout` 接口，允许已认证用户退出。

#### Scenario: 退出成功

- **WHEN** 已认证用户调用 logout 接口
- **THEN** 系统返回 HTTP 200，`data.success` 为 true
- **AND** 客户端 MUST 清除本地 token

### Requirement: 用户数据模型

系统 MUST 维护 `users` 表，支持以下角色：`admin`（系统管理员）、`employee`（企业内部员工）、`store_owner`（瓷砖零售店店主，本期预留）。

#### Scenario: 用户角色字段

- **WHEN** 系统存储用户信息
- **THEN** role 字段 MUST 为 `admin`、`employee` 或 `store_owner` 之一
- **AND** status 字段 MUST 为 `active` 或 `disabled`

#### Scenario: 用户名唯一

- **WHEN** 系统创建用户
- **THEN** username MUST 在表中唯一

### Requirement: 管理端角色访问控制

系统 MUST 在后端依赖注入层校验用户角色，仅允许 `admin` 和 `employee` 访问管理端 API。

#### Scenario: 员工访问管理端 API

- **WHEN** 角色为 `employee` 或 `admin` 的用户携带有效 token 访问受保护管理端 API
- **THEN** 系统 MUST 允许访问

#### Scenario: 店主访问管理端 API

- **WHEN** 角色为 `store_owner` 的用户携带有效 token 访问管理端 API
- **THEN** 系统 MUST 返回 HTTP 403，拒绝访问

### Requirement: 登录日志表预留

系统 MUST 创建 `login_logs` 表结构，包含 id、user_id、login_identifier、result、failure_reason、ip、user_agent、created_at 字段，本期不要求写入业务数据。

#### Scenario: 表结构存在

- **WHEN** 数据库 migration 执行完成
- **THEN** `login_logs` 表 MUST 存在于 schema 中

### Requirement: API 响应格式

认证相关 API MUST 遵循项目统一响应结构 `{ code, message, data }`。

#### Scenario: 成功响应格式

- **WHEN** 认证 API 调用成功
- **THEN** 响应 MUST 包含 `code: 0`、`message: "success"` 和 `data` 字段

#### Scenario: 错误响应格式

- **WHEN** 认证 API 调用失败
- **THEN** 响应 MUST 包含非零 `code`、可读 `message` 和 `data: null`

### Requirement: 管理员账号初始化

系统 MUST 提供种子机制，通过环境变量配置首批管理员账号密码。

#### Scenario: 种子管理员创建

- **WHEN** 部署环境设置 `ADMIN_INITIAL_PASSWORD` 且数据库无 admin 用户
- **THEN** 系统 MUST 创建 role 为 `admin` 的默认用户
