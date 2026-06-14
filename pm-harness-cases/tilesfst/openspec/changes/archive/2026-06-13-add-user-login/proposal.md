## Why

瓷砖信息管理平台的 Web 管理端涉及内部业务数据维护，当前缺少用户认证与路由鉴权能力，任何人可直接访问管理端页面，存在安全风险。REQ-0001 要求优先建立可扩展的统一登录基础能力，为后续权限控制、操作审计和多端用户体系打基础。

## What Changes

- 新增 Web 管理端登录页（`/admin/login`），视觉对齐 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.png` 暗色工业风原型。
- 新增后端认证 API：`POST /api/v1/auth/login`、`GET /api/v1/auth/me`、`POST /api/v1/auth/logout`。
- 新增 `users` 表及密码哈希存储，预留 `store_owner` 角色与 `login_logs` 表结构。
- 新增前端 `auth` feature：登录表单、登录态管理、管理端路由守卫、退出登录。
- 登录成功后按角色跳转：`admin` / `employee` → `/admin/dashboard`；`store_owner` 拒绝管理端访问。
- 登录页保留「忘记密码」「企业微信」「语言切换」占位入口，本期展示「功能建设中」，不实现完整流程。

## Capabilities

### New Capabilities

- `auth`：用户认证能力，涵盖账号密码登录、当前用户查询、退出登录、密码哈希、角色识别、禁用用户拒绝、错误码规范。
- `web-client`：Web 客户端登录页 UI、表单校验与交互、管理端路由鉴权、登录态保持与过期处理、无权限页展示。

### Modified Capabilities

（`openspec/specs/` 当前为空，无既有能力需 delta 修改。）

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 新增 `auth` 路由、Schema、Service、Repository、Security 模块；扩展 `schema.sql` |
| 前端 | 新增 `src/web/src/features/auth/`、`LoginPage`、`ProtectedRoute`；扩展路由配置 |
| 数据库 | 新增 `users` 表；预留 `login_logs` 表 |
| API 文档 | 更新 `docs/03-api-index.md`；触发 Orval 客户端生成 |
| 数据库文档 | 更新 `docs/04-database-design.md` |
| 测试 | 新增后端认证接口测试、前端登录与路由守卫测试 |
| 部署 | 需数据库种子脚本初始化首批管理员账号 |
| 需求追踪 | 关联 `issues/requirements/REQ-0001-user-login/` |
