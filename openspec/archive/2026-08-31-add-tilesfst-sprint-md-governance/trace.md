---
created_at: 2026-08-27 01:02:22
updated_at: 2026-08-27 01:02:22
---

# Trace

## 来源

- 命令：`/spec-study apply TilesFST sprint-md-scope-contract sprint-scope-validation-gate sprint-scope-append-script workflow-sync-sprint-md-derived-refresh sprint-close-stale-readiness sprint-fact-sheet-read-first`
- 学习对象：`ProjectTilesFST`
- 学习模式：`--focus sprint.md`
- Sprint：`sprint-001`

## 只读保护

学习对象作为外部只读输入读取。应用阶段只修改 ProjectPmHarness 当前仓库治理资产、模板资产和 active Change/Sprint 事实源，不修改学习对象。

## 影响映射

| 采纳项 | 本项目落点 |
|---|---|
| sprint-md-scope-contract | `rules/iterations-lifecycle.md`、`.agents/skills/sprint-propose/SKILL.md`、Sprint `sprint-001` 四件套 |
| sprint-scope-validation-gate | `scripts/validate-sprint-scope.py`、`docs/08-command-execution-order.md` |
| sprint-scope-append-script | `scripts/add-sprint-scope-item.py`、`scripts/workflow_sync/` |
| workflow-sync-sprint-md-derived-refresh | `scripts/sync-workflow-status.py`、`scripts/workflow_sync/`、`.agents/skills/workflow-sync/SKILL.md` |
| sprint-close-stale-readiness | `scripts/validate-sprint-archive-readiness.py`、`scripts/check-sprint-close-stale-scan.py`、`.agents/skills/sprint-archive/SKILL.md` |
| sprint-fact-sheet-read-first | `scripts/generate-sprint-fact-sheet.py`、`.agents/skills/sprint-exps/SKILL.md` |

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 本 Change 触达 Sprint 工作流治理，不改业务运行时数据采集。
  validation: 运行 Sprint scope、archive readiness、Fact Sheet summary 和 Change-specific 产品数据观测门禁校验。
```
