---
title: Change 追踪
purpose: 记录 refactor-login-ui 与 Sprint 01、REQ-0001 的追踪关系
source: Path C Phase 2 登录页 UI 重构
status: done
---

# Change 追踪

## 基本信息

```yaml
change_id: refactor-login-ui
requirement_id: REQ-0001
priority: P0
status: done
iteration: sprint-01
depends_on:
  - add-design-system
related:
  - add-user-login
source: prototype/web/user-login.md + Sprint 01 验收遗留 L-01
```

## 迭代关联

```yaml
iteration: sprint-01
sprint_doc: iterations/sprint-01/sprint.md
release_note: iterations/sprint-01/release-note.md
acceptance_report: iterations/sprint-01/acceptance-report.md
```

## UI 差距清单（refactor 前 → 后）

| 差距项 | refactor 前 | refactor 后 |
|---|---|---|
| 色值 | 裸 Hex `#18160F` 等 | Design Token（`bg-page`、`text-brand-gold` 等） |
| 用户名输入 | 自定义 div + input | `IconInput` + shadcn `Input` |
| 密码输入 | 自定义 div + input | shadcn `Input` + `Button` 显隐 |
| 记住我 | 原生 checkbox | shadcn `Checkbox` + `Label` |
| 登录按钮 | 原生 button | shadcn `Button` |
| 分割线 | 手写 div | `DividerText` |
| 左栏 gradient | Hex rgba | `from-page/95 via-page/65 to-page/25` |

## Auth 只读边界（未修改）

- `src/web/src/features/auth/store/auth-store.ts`
- `src/web/src/features/auth/hooks/useAuth.ts`
- `src/web/src/features/auth/api/auth-api.ts`

## Artifacts 状态

| Artifact | 路径 | 状态 |
|---|---|---|
| proposal | `proposal.md` | done |
| design | `design.md` | done |
| specs | `specs/web-client/spec.md` | done |
| tasks | `tasks.md` | done（24/24 完成） |

## 状态流转

| 日期 | 状态 | 说明 |
|---|---|---|
| 2026-06-13 | planned | OpenSpec artifacts 创建 |
| 2026-06-13 | done | 登录页 UI 迁移 Design System 完成 |
