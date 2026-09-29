---
created_at: 2026-08-27 01:02:22
updated_at: 2026-08-27 01:02:22
---

# 应用 TilesFST sprint.md 治理

## 背景

`/spec-study TilesFST --focus sprint.md` 已完成只读学习，并确认应用以下候选项：

- `sprint-md-scope-contract`
- `sprint-scope-validation-gate`
- `sprint-scope-append-script`
- `workflow-sync-sprint-md-derived-refresh`
- `sprint-close-stale-readiness`
- `sprint-fact-sheet-read-first`

这些内容属于 Sprint 文档合同、治理脚本、Workflow Sync 派生刷新和 Sprint 命令技能变化，必须通过 active OpenSpec Change 承载，并纳入 Sprint scope。

## 目标

- 固化 `sprint.md` 目标编号列表和 Scope 六列表合同。
- 增加 Sprint scope 追加脚本和 `sprint.md` 一致性校验。
- 将 Workflow Sync 扩展为可刷新 `sprint.md` Scope 主表、分组表、release-note 与 acceptance-report 的派生源。
- 增加 Sprint 归档 readiness、stale scan、归档路径残留检查和 Fact Sheet read-first 复盘入口。
- 同步根项目运行态、`pm-harness/` 新项目模板和 init-skill 模板资产。

## 非目标

- 不复制 TilesFST 的业务 Sprint、REQ、BUG、Change、源码路径或运行时数据。
- 不修改学习对象 TilesFST。
- 不修改 `src/` 业务代码、API、数据库、Web、小程序、管理端或 Orval 生成物。
- 不直接修改 `openspec/specs/` 正式规格。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 本 Change 触达 Sprint 工作流治理、Scope 派生刷新和归档校验脚本；不触达业务 API、DB、端请求封装或运行时日志数据。
  validation: 运行 Sprint scope 校验、archive readiness、Fact Sheet summary、OpenSpec、目录、模板同步、Workflow Sync 与 AI Usage hook。
```
