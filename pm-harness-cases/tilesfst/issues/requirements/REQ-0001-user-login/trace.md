---
title: 需求追踪
purpose: 记录 REQ-0001 用户登录的来源、关联文档、迭代、OpenSpec 与实现追踪
content: 基于 requirement.md 与项目目录结构维护
source: AI根据 PRD 生成，项目团队确认
update_method: 状态、迭代或 OpenSpec 变更时同步更新
owner: 产品负责人
status: draft
note: REQ-0001 用户登录
---

# 需求追踪

## 1. 基本信息

```yaml
requirement_id: REQ-0001
requirement_name: 用户登录
requirement_type: 基础能力 / 认证授权
priority: P0
status: in_progress
source: 瓷砖信息管理平台基础认证能力需求
target_users:
  - 企业内部员工
  - 系统管理员
  - 瓷砖零售店店主（预留）
target_clients:
  - web_admin: 本期实现
  - web_catalog: 本期预留
  - wechat_miniapp: 本期预留
iteration: sprint-01
change_id: add-user-login
related_changes:
  - add-design-system
  - refactor-login-ui
  - align-login-prototype
  - fix-login-pixel-fidelity
```

## 2. 关联文档

| 文档 | 路径 | 说明 |
|---|---|---|
| 需求 PRD | `requirement.md` | 完整功能、接口、数据模型与验收要求 |
| 用户故事 | `user-stories.md` | 分角色用户故事与验收要点 |
| 业务流程 | `business-flow.md` | 登录、鉴权、分流、退出流程 |
| 验收标准 | `acceptance.md` | 功能、接口、数据、UI 验收清单 |
| Web 原型图 | `prototype/web/user-login.png` | 登录页视觉稿 |
| Web 原型说明 | `prototype/web/user-login.md` | 组件树、Design Token、交互规范 |

## 3. OpenSpec 追踪

| 阶段 | 路径 | 状态 |
|---|---|---|
| Change | `openspec/changes/add-user-login/` | 已实现，待验收归档 |
| Change — Design System | `openspec/changes/archive/2026-06-13-add-design-system/` | 已归档 |
| Change — 登录 UI 重构 | `openspec/changes/archive/2026-06-13-refactor-login-ui/` | 已归档 |
| Change — checklist 对齐 | `openspec/changes/archive/2026-06-13-align-login-prototype/` | 已归档 |
| Change — PNG 像素级 | `openspec/changes/archive/2026-06-13-fix-login-pixel-fidelity/` | **已实现，待归档** |
| Change 追踪 | `openspec/changes/add-user-login/trace.md` | 已创建 |
| Change 追踪 — DS | `openspec/changes/add-design-system/trace.md` | 已创建 |
| 目标 Spec | `openspec/specs/auth/`（归档后） | 未生效 |
| 关联 Spec | `openspec/specs/web-client/spec.md`（归档后） | 未生效 |
| 迭代 | `iterations/sprint-01/sprint.md` | 进行中（含 add-design-system） |

建议 Change 目录结构：

```text
openspec/changes/add-user-login/
├── proposal.md
├── design.md
├── tasks.md
├── trace.md
├── acceptance.md
├── test-plan.md
├── specs/
│   ├── web-client/spec.md
│   └── auth/spec.md
└── implementation/
    ├── api.md
    ├── db.md
    ├── frontend.md
    └── rollout.md
```

## 4. 功能需求追踪

| 编号 | 需求摘要 | 用户故事 | 验收章节 |
|---|---|---|---|
| FR-001 | 账号密码提交登录 | US-001 | acceptance §1.2 |
| FR-002 | 前端非空校验 | US-001 | acceptance §1.2 |
| FR-003 | 登录 loading 防重复提交 | US-001 | acceptance §1.2 |
| FR-004 | 成功后保存态并跳转 | US-001 | acceptance §1.3 |
| FR-005 | 失败错误提示 | US-001 | acceptance §1.3 |
| FR-006 | 受保护页调用当前用户接口 | US-001, US-002 | acceptance §1.4 |
| FR-007 | 返回 ID、显示名、角色、状态 | US-002 | acceptance §1.4 |
| FR-008 | 非启用用户拒绝访问 | US-002 | acceptance §1.3 |
| FR-009 | 顶部菜单退出登录 | US-001 | acceptance §1.6 |
| FR-010 | 退出清除态并跳转 | US-001 | acceptance §1.6 |
| FR-011 | 退出后受保护页跳转登录 | US-001 | acceptance §1.6 |
| FR-012 | 管理端除登录页外受保护 | US-001 | acceptance §1.5 |
| FR-013 | 未登录跳转 `/admin/login` | US-001 | acceptance §1.5 |
| FR-014 | 已登录访问登录页跳转首页 | US-001 | acceptance §1.5 |
| FR-015 | 权限不足展示无权限 | US-002, US-003 | acceptance §1.4 |

## 5. 接口追踪

| 方法 | 路径 | PRD 章节 | 文档同步 |
|---|---|---|---|
| POST | `/api/v1/auth/login` | requirement §10.1 | `docs/03-api-index.md`（待更新） |
| GET | `/api/v1/auth/me` | requirement §10.2 | `docs/03-api-index.md`（待更新） |
| POST | `/api/v1/auth/logout` | requirement §10.3 | `docs/03-api-index.md`（待更新） |

## 6. 数据模型追踪

| 表名 | PRD 章节 | 文档同步 | 本期实现 |
|---|---|---|---|
| `users` | requirement §11.1 | `docs/04-database-design.md`（待更新） | 是 |
| `login_logs` | requirement §11.2 | `docs/04-database-design.md`（待更新） | 预留 |

## 7. 实现路径追踪（候选）

| 层级 | 候选路径 |
|---|---|
| 前端 Feature | `src/web/src/features/auth/` |
| 前端页面 | `src/web/src/pages/admin/LoginPage.tsx` |
| 前端路由守卫 | `src/web/src/app/router/ProtectedRoute.tsx` |
| 后端 API | `src/backend/app/api/v1/auth.py` |
| 后端 Schema | `src/backend/app/schemas/auth.py` |
| 后端 Service | `src/backend/app/services/auth_service.py` |
| 后端 Repository | `src/backend/app/repositories/user_repository.py` |
| 后端 Security | `src/backend/app/core/security.py` |

## 8. 状态流转

```text
draft → approved → in_progress → resolved → closed
```

| 日期 | 状态 | 说明 |
|---|---|---|
| 2026-06-13 | draft | 基于 PRD 与登录页原型补齐配套文档 |
| 2026-06-13 | approved | 纳入 Sprint 01，OpenSpec add-user-login 规划完成 |
| 2026-06-13 | in_progress | add-user-login 实现完成，后端/前端/测试已交付 |
| 2026-06-13 | in_progress | 同 Sprint 纳入 add-design-system；登录页 UI 对齐待 refactor-login-ui |
| 2026-06-13 | in_progress | fix-login-pixel-fidelity 实现完成；视觉基准为 user-login.png |

## 9. 待确认项

以下问题在 PRD §18 中列出，确认后需回写 `requirement.md` 与本追踪文档：

- [ ] 登录标识是否仅支持用户名，还是同时支持手机号和邮箱？
- [ ] Web 展示端店主是否本期必须登录？
- [ ] 小程序是否本期需要接入微信登录？
- [ ] 登录态采用 Bearer Token、HttpOnly Cookie 还是双 Token 刷新机制？
- [ ] 是否需要本期实现登录失败次数限制和账号锁定？
- [ ] 是否需要本期接入企业微信登录？
- [ ] 首批管理员账号如何初始化：脚本、后台创建还是数据库种子？

## 10. 测试追踪

| 类型 | 范围 | 状态 |
|---|---|---|
| 后端单元/集成测试 | 登录、me、logout 接口 | 待补充 |
| 前端组件测试 | LoginForm、PasswordInput | 待补充 |
| 前端路由测试 | ProtectedRoute、登录跳转 | 待补充 |
| E2E | 完整登录 → 访问管理端 → 退出 | 待补充 |
