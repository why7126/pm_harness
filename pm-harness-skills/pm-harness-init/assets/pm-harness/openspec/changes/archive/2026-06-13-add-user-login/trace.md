---
title: Change 追踪
purpose: 记录 add-user-login 与需求、迭代、实现的追踪关系
content: 基于 REQ-0001 与 Sprint 001 规划
source: AI根据 OpenSpec 与迭代规划生成
update_method: 实现进度或迭代变更时更新
owner: 项目负责人
status: planned
note: add-user-login OpenSpec Change
---

# Change 追踪

## 基本信息

```yaml
change_id: add-user-login
requirement_id: REQ-0001
requirement_name: 用户登录
priority: P0
status: implemented
iteration: sprint-001
schema: spec-driven
created: 2026-06-13
```

## 关联需求

| 文档 | 路径 |
|---|---|
| 需求 PRD | `issues/requirements/REQ-0001-user-login/requirement.md` |
| 用户故事 | `issues/requirements/REQ-0001-user-login/user-stories.md` |
| 业务流程 | `issues/requirements/REQ-0001-user-login/business-flow.md` |
| 验收标准 | `issues/requirements/REQ-0001-user-login/acceptance.md` |
| 需求追踪 | `issues/requirements/REQ-0001-user-login/trace.md` |

## 迭代关联

```yaml
iteration: sprint-001
sprint_doc: iterations/sprint-001/sprint.md
release_note: iterations/sprint-001/release-note.md
acceptance_report: iterations/sprint-001/acceptance-report.md
related_changes:
  - add-design-system
  - refactor-login-ui
```

## Artifacts 状态

| Artifact | 路径 | 状态 |
|---|---|---|
| proposal | `proposal.md` | done |
| design | `design.md` | done |
| specs/auth | `specs/auth/spec.md` | done |
| specs/web-client | `specs/web-client/spec.md` | done |
| tasks | `tasks.md` | done（41/41 完成） |

## 实现进度

| 阶段 | 状态 | 说明 |
|---|---|---|
| OpenSpec 规划 | 完成 | proposal/design/specs/tasks 已创建 |
| 后端实现 | 完成 | auth API、users 表、种子脚本、集成测试 |
| 前端实现 | 完成 | 登录页、auth feature、路由守卫、Orval 客户端 |
| 集成验证 | 完成 | 后端 pytest 7/7、前端 vitest 6/6、curl E2E |
| 归档至 openspec/specs/ | 未开始 | 验收通过后执行 archive |

## 目标 Spec（归档后）

| Spec | 路径 |
|---|---|
| auth | `openspec/specs/auth/spec.md` |
| web-client | `openspec/specs/web-client/spec.md` |

## 状态流转

```text
planned → in_progress → implemented → archived
```

| 日期 | 状态 | 说明 |
|---|---|---|
| 2026-06-13 | implemented | 全部 tasks 完成，待 Sprint 验收与 archive |
| 2026-06-13 | — | 同 Sprint 纳入 add-design-system（Path C Phase 1） |
