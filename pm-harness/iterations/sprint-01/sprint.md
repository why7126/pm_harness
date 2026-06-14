---
title: Sprint 01 迭代说明
purpose: 记录 Sprint 01 目标、范围、Change、工作量与风险
content: 基于 REQ-0001 及全部登录相关 OpenSpec Change 规划
source: AI根据 issues/openspec 目录生成，项目团队确认
update_method: 迭代范围或状态变化时更新
owner: 项目负责人
status: in_progress
note: fix-login-pixel-fidelity 为 Sprint 01 视觉收尾（PNG golden reference）
---

# Sprint 01

## Sprint 目标

本迭代交付 REQ-0001 **用户登录**完整能力（功能 + 视觉），含：

- Web 管理端账号密码登录（`/admin/login`）
- 后端认证 API、用户模型、路由守卫、角色分流
- Web Design System（Token + shadcn/ui）
- 登录页 UI 组件化（`refactor-login-ui`）
- **登录页 PNG 像素级对齐**（`fix-login-pixel-fidelity`）← 当前收尾

本迭代为 `add-tile-catalog`、`add-tile-admin` 提供安全与视觉基础。

## Scope

### 包含需求

| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0001 | 用户登录 | P0 | in_progress | 视觉对齐 `user-login.png`；`fix-login-pixel-fidelity` 已实现，待团队 sign-off |

### 包含技术改造

| 名称 | Change | 状态 |
|---|---|---|
| Web Design System | `add-design-system` | ✓ 已归档 |
| 登录页 DS 组件化 | `refactor-login-ui` | ✓ 已归档 |
| 登录页 checklist 对齐 | `align-login-prototype` | ✓ 已归档 |
| **登录页 PNG 像素级** | `fix-login-pixel-fidelity` | **✓ 已实现，待归档** |

### 不包含（延后）

| 项目 | 延后原因 |
|---|---|
| 瓷砖目录/管理 | 依赖本 Sprint 完成 |
| 企微 OAuth / 忘记密码 / 小程序登录 | REQ-0001 子项 P2+ |

## Change 列表

| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-user-login` | REQ-0001 | 已归档 | 认证 API、路由守卫 |
| `add-design-system` | REQ-0001 | 已归档 | Design Token、shadcn |
| `refactor-login-ui` | REQ-0001 | 已归档 | DS 组件化 |
| `align-login-prototype` | REQ-0001 | 已归档 | checklist 对齐 |
| **`fix-login-pixel-fidelity`** | REQ-0001 | **✓ 已实现，待归档** | **PNG golden reference** |

**活跃 Change 路径：** 无（待归档 `fix-login-pixel-fidelity`）

## 工作量预估

| 工作包 | Change | 人天 | 状态 |
|---|---|---|---|
| 认证 + DS + UI 组件化 | 前三个 Change | 22.5 | ✓ |
| **原型 checklist** | align-login-prototype | 2.5 | ✓ |
| **PNG 像素级** | fix-login-pixel-fidelity | 2 | ✓ |
| Sprint 验收 | 全部 | 1 | 进行中 |
| **合计** | | **28** | |

## 里程碑

| 阶段 | 交付 | 状态 |
|---|---|---|
| M1–M3 认证 + DS + 组件化 | 前三个 Change | ✓ |
| **M4 checklist 对齐** | align-login-prototype | ✓ |
| **M5 PNG 像素级** | fix-login-pixel-fidelity | **✓** |
| M6 Sprint 验收 | acceptance-report 全项 | 进行中 |

## 依赖关系

```text
REQ-0001
  ├── add-user-login ✓
  ├── add-design-system ✓
  ├── refactor-login-ui ✓
  └── align-login-prototype ✓
        └── fix-login-pixel-fidelity ✓（待归档）
              └── [后续] add-tile-catalog / add-tile-admin
```

## 关联文档

| 文档 | 路径 |
|---|---|
| Web 原型 | `issues/requirements/REQ-0001-user-login/prototype/web/` |
| OpenSpec | `openspec/changes/archive/2026-06-13-fix-login-pixel-fidelity/` |
| 正式 Spec | `openspec/specs/web-client/spec.md` |
| Sprint 验收 | `iterations/sprint-01/acceptance-report.md` |
