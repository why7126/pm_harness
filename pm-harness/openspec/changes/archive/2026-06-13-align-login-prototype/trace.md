---
title: Change 追踪
purpose: 记录 align-login-prototype 与 Sprint 001、REQ-0001 的追踪关系
source: 登录页与 user-login.png 视觉差距分析
status: implemented
---

# Change 追踪

## 基本信息

```yaml
change_id: align-login-prototype
requirement_id: REQ-0001
priority: P0
status: implemented
iteration: sprint-001
depends_on:
  - add-design-system
  - refactor-login-ui
related:
  - add-user-login
source: prototype/web/user-login.png 高保真还原
```

## 迭代关联

```yaml
iteration: sprint-001
sprint_doc: iterations/sprint-001/sprint.md
release_note: iterations/sprint-001/release-note.md
acceptance_report: iterations/sprint-001/acceptance-report.md
```

## 与 refactor-login-ui 的关系

```text
refactor-login-ui  → Design Token + shadcn 组件化（已归档）
align-login-prototype → 像素级/高保真原型还原（已实现，待归档）
```

## Artifacts 状态

| Artifact | 路径 | 状态 |
|---|---|---|
| proposal | `proposal.md` | done |
| design | `design.md` | done |
| specs | `specs/web-client/spec.md` | done |
| tasks | `tasks.md` | done（23/23 完成） |

## 实现摘要

| 类别 | 路径 / 说明 |
|---|---|
| 背景 JPG | `src/web/public/images/login-material-showcase.jpg`（768×1024，自 PNG 左栏裁切） |
| 企微图标 | `src/web/public/icons/wecom.svg` |
| 样例说明 | `data/samples/images/README.md` |
| LanguageSwitcher | `src/web/src/features/auth/components/LanguageSwitcher.tsx` |
| WeComLoginButton | `src/web/src/features/auth/components/WeComLoginButton.tsx` |
| LoginCopyright | `src/web/src/features/auth/components/LoginCopyright.tsx` |
| AuthBrandPanel | JPG + gradient overlay |
| LoginPage | LanguageSwitcher、Copyright、overflow-hidden |
| LoginForm | WeComLoginButton、spacing 精修 |

## Auth 逻辑隔离（任务 4.3）

以下文件在本 Change 中**未修改**（只读验证）：

- `src/web/src/features/auth/store/`
- `src/web/src/features/auth/hooks/useAuth.ts`
- `src/web/src/features/auth/api/auth-api.ts`

## 视觉对比记录（任务 7.1）

对照 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.png` 与 `user-login.md`：

| 检查点 | 原型要求 | 实现状态 |
|---|---|---|
| 左栏背景 | 暗色石材/展厅摄影 | ✓ JPG `login-material-showcase.jpg`，opacity-80 |
| 左栏渐变 | from-page/95 → to-page/25 | ✓ `bg-gradient-to-r from-page/95 via-page/65 to-page/25` |
| 右栏语言切换 | 简体中文 + ChevronDown | ✓ `LanguageSwitcher` @ `right-6 top-6` |
| 企微入口 | SVG 图标 + 「企业微信」文案 | ✓ `WeComLoginButton`，移除「企」占位 |
| 标题间距 | 标题到表单 48px | ✓ `mb-12` |
| 表单项间距 | 28px | ✓ `space-y-7` |
| 第三方区间距 | 主按钮到第三方 56px | ✓ `pt-14` |
| 表单宽度 | max 520px | ✓ `max-w-[520px]` |
| 输入框高度 | 64px（桌面）/ 52px（移动） | ✓ `h-16 max-sm:h-[52px]` |
| 版权信息 | 页脚居中 | ✓ `LoginCopyright` |
| Design Token | 无裸 Hex | ✓ 沿用 globals.css token |
| 分屏布局 | lg 双栏 / 移动单栏 | ✓ `lg:grid-cols-2`，左栏 `hidden lg:flex` |

**建议团队验收**：在 `http://localhost:3000/admin/login` 与 `user-login.png` 并排对比，确认像素级差异可接受后勾选 Sprint acceptance-report 视觉项。

## 测试与构建

| 命令 | 结果 |
|---|---|
| `vitest run` | 16 passed（含 LanguageSwitcher、WeCom 测试） |
| `vite build` | ✓ |
| `docker compose build web` | ✓ |

## 下一步

- `/opsx:archive align-login-prototype` 归档并合并 spec delta
- Sprint 001 团队视觉 sign-off 后关闭 L-01
