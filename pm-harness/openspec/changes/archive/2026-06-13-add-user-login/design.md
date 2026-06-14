## Context

- **需求来源**：`issues/requirements/REQ-0001-user-login/`（PRD、用户故事、业务流程、验收标准、Web 原型）。
- **当前状态**：后端仅有瓷砖相关 API，无用户表与认证中间件；前端无登录页与路由守卫；`openspec/specs/` 为空。
- **约束**：FastAPI + Pydantic + SQLite + React 19 + Tailwind + Orval；密码不得明文存储；API 遵循 `rules/api.md` 统一响应结构；UI 遵循暗色工业风 `rules/ui-design.md`。
- **干系人**：企业内部员工、系统管理员（本期）；瓷砖零售店店主（数据模型预留，登录入口本期不开放）。

## Goals / Non-Goals

**Goals:**

- 实现 Web 管理端账号密码登录完整闭环（登录 → 鉴权 → 退出）。
- 后端提供 JWT Bearer Token 认证，前端封装独立 `auth` feature。
- 登录页视觉与交互对齐原型 `prototype/web/user-login.png`。
- 角色识别与基础路由权限：`admin` / `employee` 可进管理端；`store_owner` 拒绝。
- 为后续小程序登录、企业微信 OAuth、RBAC 扩展预留接口与数据模型。

**Non-Goals:**

- 店主自助注册、忘记密码闭环、手机验证码登录。
- 企业微信扫码登录（仅占位 UI）。
- 微信小程序登录。
- 多租户、细粒度 RBAC 配置页、登录审计报表。
- 登录失败次数限制与账号锁定（可后续 Change 引入）。

## Decisions

### D1：登录标识 — 本期仅支持 `username`

- **决策**：登录请求体使用 `username` + `password`，不支持手机号/邮箱多标识查询。
- **理由**：PRD 建议项目初期快速落地；减少 Repository 查询复杂度。
- **备选**：同时支持 username/phone/email — 留待后续 Change。

### D2：认证方案 — JWT Bearer Token

- **决策**：登录成功返回 `access_token`（JWT），前端在 `Authorization: Bearer <token>` 头携带；`remember_me=true` 时 token 有效期 7 天，否则 2 小时。
- **理由**：与 FastAPI 生态（python-jose / PyJWT）契合；Orval 生成客户端友好；无状态便于 Docker 部署。
- **备选**：HttpOnly Cookie — 更安全但需 CSRF 防护与 nginx 代理配置，本期复杂度偏高。

### D3：密码哈希 — bcrypt（passlib）

- **决策**：使用 `passlib[bcrypt]` 哈希存储，cost factor 默认 12。
- **理由**：行业惯例，与 `rules/security.md` 一致。
- **备选**：argon2 — 更安全但依赖与兼容性需额外验证。

### D4：JWT Payload

```json
{
  "sub": "<user_id>",
  "role": "admin|employee|store_owner",
  "exp": 1234567890
}
```

- 不在 JWT 中存储敏感信息；`/auth/me` 返回完整用户 profile。

### D5：API 响应格式

遵循 `rules/api.md` 统一包装：

```json
{
  "code": 0,
  "message": "success",
  "data": { "access_token": "...", "token_type": "Bearer", "expires_in": 7200, "user": {...} }
}
```

错误响应：

```json
{
  "code": 40101,
  "message": "账号或密码错误",
  "data": null
}
```

### D6：数据库 Schema

**users 表**（TEXT 主键 UUID）：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | TEXT PK | UUID |
| username | TEXT UNIQUE NOT NULL | 登录名 |
| phone | TEXT | 预留，可为空 |
| email | TEXT | 预留，可为空 |
| password_hash | TEXT NOT NULL | bcrypt 哈希 |
| display_name | TEXT NOT NULL | 显示名 |
| role | TEXT NOT NULL | `admin` / `employee` / `store_owner` |
| status | TEXT NOT NULL DEFAULT 'active' | `active` / `disabled` |
| last_login_at | TEXT | ISO8601 |
| created_at | TEXT NOT NULL | ISO8601 |
| updated_at | TEXT NOT NULL | ISO8601 |

**login_logs 表**：本期仅建表，不写入业务逻辑。

### D7：后端模块结构

```text
src/backend/app/
├── api/v1/auth.py          # 路由
├── schemas/auth.py         # Pydantic 请求/响应
├── services/auth_service.py
├── repositories/user_repository.py
├── core/security.py        # 哈希、JWT 编解码、依赖注入
└── core/deps.py            # get_current_user 依赖
```

### D8：前端模块结构

```text
src/web/src/features/auth/
├── api/                    # Orval 生成客户端封装
├── components/
│   ├── LoginForm.tsx
│   ├── PasswordInput.tsx
│   └── AuthBrandPanel.tsx
├── hooks/useAuth.ts
├── store/auth-store.ts     # Zustand
├── types/auth.types.ts
└── utils/auth-token.ts

src/web/src/pages/admin/LoginPage.tsx
src/web/src/app/router/ProtectedRoute.tsx
```

### D9：路由策略

| 路由 | 策略 |
|---|---|
| `/admin/login` | 公开；已登录跳转 `/admin/dashboard` |
| `/admin/*`（除 login） | 需登录 + 角色 `admin` 或 `employee` |
| `/admin/*` + 角色 `store_owner` | 跳转无权限页 |
| `/login` | 本期不实现 |

### D10：管理员初始化

- **决策**：提供 `scripts/seed-admin.py` 或 backend 启动种子，创建默认 `admin` 账号；密码通过环境变量 `ADMIN_INITIAL_PASSWORD` 注入，不硬编码。
- **理由**：PRD 待确认项中「脚本/种子」为最快落地方式。

### D11：占位功能交互

- 「忘记密码」「企业微信」：点击展示 Toast「功能建设中」。
- 「简体中文」：静态展示，不实现 i18n 切换。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| JWT 存 localStorage 有 XSS 窃取风险 | 遵循 `rules/security.md` 输入消毒；后续可迁移 HttpOnly Cookie |
| 无登录失败限流易被暴力破解 | 本期不实现；后续 Change 加 rate limit |
| 仅 username 登录限制灵活性 | 数据模型预留 phone/email 字段 |
| 种子管理员密码泄露 | 通过环境变量注入，文档强调首次登录后改密（后续 Change） |

## Migration Plan

1. 执行数据库 migration：新增 `users`、`login_logs` 表。
2. 运行种子脚本创建管理员账号。
3. 部署后端 auth 路由。
4. 部署前端登录页与路由守卫。
5. 验证 Docker Compose 全链路：登录 → dashboard → 退出。

**回滚**：移除 auth 路由注册；前端回退路由配置；数据库表可保留（无破坏性）。

## Open Questions

| 问题 | 本期决策 | 后续 |
|---|---|---|
| 登录标识范围 | 仅 username | 可扩展 phone/email |
| 登录态方案 | JWT Bearer | 可迁移 Cookie |
| 登录失败限流 | 不实现 | 单独 Change |
| 企业微信登录 | 占位 | 单独 Change |
