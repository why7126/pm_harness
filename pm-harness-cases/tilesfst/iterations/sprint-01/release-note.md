---
title: Sprint 01 发布说明
purpose: 记录 Sprint 01 计划交付能力与发布注意事项
content: 基于 REQ-0001 及全部登录相关 OpenSpec Change
source: AI根据迭代范围生成，项目团队确认
update_method: Sprint 完成或范围变更时更新
owner: 项目负责人
status: draft
note: 发布前需完成 acceptance-report 验收
---

# Sprint 01 发布说明

## 版本信息

| 字段 | 内容 |
|---|---|
| Sprint | sprint-01 |
| 关联需求 | REQ-0001 用户登录 |
| 关联 Change | 前序 + **`fix-login-pixel-fidelity`（已实现，待归档）** |
| 发布状态 | 功能与视觉实现完成；待团队 PNG sign-off 后发布 |

## 新增能力

### Web 管理端登录

- 新增登录页 `/admin/login`，左右分屏布局（功能完整）
- 支持用户名 + 密码登录，表单校验、loading 状态、密码显隐切换
- 「记住我」延长登录态（7 天）；未勾选默认 2 小时
- 「忘记密码」「企业微信」占位入口，点击提示「功能建设中」

### 认证与鉴权

- 新增后端认证 API：
  - `POST /api/v1/auth/login`
  - `GET /api/v1/auth/me`
  - `POST /api/v1/auth/logout`
- JWT Bearer Token 认证，密码 bcrypt 哈希存储
- 管理端路由守卫：未登录跳转登录页；已登录访问登录页跳转 dashboard
- 角色分流：`admin` / `employee` 可进管理端；`store_owner` 拒绝并展示无权限
- 管理端顶部菜单支持退出登录

### Web Design System（add-design-system）

- Design Token 层：`src/web/src/styles/globals.css`，映射 `rules/ui-design.md` 色彩/圆角/字距
- shadcn/ui 基础组件（New York 风格）：Button、Input、Checkbox、Label、Separator
- 复合组件：`IconInput`、`DividerText`
- 工具函数：`cn()`（`src/web/src/shared/lib/cn.ts`）
- 预览页：`/design-system`，展示 token 样本与组件交互状态
- Vite `@/` 路径别名与 `components.json` 配置

### 数据模型

- 新增 `users` 表（username、role、status、password_hash 等）
- 预留 `login_logs` 表结构（本期不写入业务数据）
- 预留 `store_owner` 角色，为后续店主端登录扩展

### 部署与初始化

- 管理员种子脚本，通过 `ADMIN_INITIAL_PASSWORD` 环境变量配置初始密码
- Docker Compose 环境可完成：种子 → 登录 → dashboard → 退出 全链路

### 登录页 checklist 对齐（align-login-prototype，已实现）

- JPG 背景、LanguageSwitcher、WeCom SVG、spacing 数字

### 登录页 PNG 像素级（fix-login-pixel-fidelity，已实现）

- STONEX 品牌衬线字体（Cormorant Garamond / `font-brand`）
- 企微官方绿色图标（`#2BAD13`）
- 组件拆分：`LoginFormPanel` / `LoginHeader` / `ThirdPartyLoginSection`
- 登录页 shadcn override（border-only focus、轻量 eye 按钮）
- 移除 notice 横幅；占位交互 noop
- `rules/ui-design.md` §9 登录页专章

## 不包含

- 店主 Web / 小程序登录入口
- 忘记密码、手机验证码、企业微信 OAuth 完整流程
- 登录失败限流与账号锁定
- 细粒度 RBAC 配置页与登录审计报表
- 瓷砖目录、瓷砖管理等业务功能

## 升级说明

1. 拉取最新代码并重建 Docker 镜像
2. 设置环境变量 `ADMIN_INITIAL_PASSWORD`（`.env.example` 参考）
3. 启动服务后执行数据库 migration / 种子脚本
4. 访问 `http://localhost:3000/admin/login` 使用种子 admin 账号登录
5. 开发环境可访问 `http://localhost:5173/design-system` 验收 Design System
6. 运行 `./scripts/generate-openapi-client.sh` 同步前端 API 客户端（若后端 API 有变更）

## 已知限制

- 登录标识本期仅支持 `username`
- Token 存储于 localStorage / sessionStorage，非 HttpOnly Cookie
- Design System 预览页 `/design-system` 为开发验收入口，生产环境是否保留待产品确认

## 关联验收

完整验收项见：

- `issues/requirements/REQ-0001-user-login/acceptance.md`
- `iterations/sprint-01/acceptance-report.md`
- `openspec/changes/refactor-login-ui/specs/web-client/spec.md`
