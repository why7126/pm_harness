---
created_at: 2026-08-27 01:02:22
updated_at: 2026-08-27 01:02:22
type: spec-study-apply
source_project: TilesFST
change_id: add-tilesfst-sprint-md-governance
sprint_id: sprint-001
---

# TilesFST Sprint 文档治理学习应用

## 学习输入

- 命令：`/spec-study apply TilesFST sprint-md-scope-contract sprint-scope-validation-gate sprint-scope-append-script workflow-sync-sprint-md-derived-refresh sprint-close-stale-readiness sprint-fact-sheet-read-first`
- 聚焦：`sprint.md`
- 只读对象：ProjectTilesFST 治理资产。

## 采纳项

| 候选项 | 应用结论 |
|---|---|
| sprint-md-scope-contract | 采纳；`sprint.md` 明确目标编号列表与六列 Scope 主表。 |
| sprint-scope-validation-gate | 采纳；Sprint 选择、追加范围和收口阶段加入 `validate-sprint-scope.py`。 |
| sprint-scope-append-script | 采纳；根项目补齐 `add-sprint-scope-item.py` 并接入 Workflow Sync 范围更新能力。 |
| workflow-sync-sprint-md-derived-refresh | 采纳；根项目使用完整 Workflow Sync 引擎刷新 `sprint.md`、`release-note.md` 和 `acceptance-report.md`。 |
| sprint-close-stale-readiness | 采纳；Sprint 归档前执行 readiness 与 stale scan。 |
| sprint-fact-sheet-read-first | 采纳；Sprint 复盘前先生成 Fact Sheet 摘要。 |

## 本项目落点

- 新增 active Change：`add-tilesfst-sprint-md-governance`。
- 更新当前 Sprint：`sprint-001` 纳入本 Change，并让 `sprint.md` 表达机器 Scope、派生区和验收条件。
- 补齐根项目 Sprint/Workflow Sync 脚本与技能入口。
- 同步模板命令矩阵，确保新项目继承相同 Sprint 范围校验与收口门禁。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 本次变更触达 Sprint 工作流治理、状态同步和验证脚本，不改业务运行时采集、端请求封装或审计日志。
  validation:
    - python scripts/validate-product-data-observability-gates.py --change add-tilesfst-sprint-md-governance
```

## 验证摘要

- Sprint scope：`python scripts/validate-sprint-scope.py sprint-001 --item add-tilesfst-sprint-md-governance`
- Sprint readiness：`python scripts/validate-sprint-archive-readiness.py --sprint sprint-001 --change add-tilesfst-sprint-md-governance`
- Sprint stale scan：`python scripts/check-sprint-close-stale-scan.py --sprint sprint-001`
- Sprint Fact Sheet：`python scripts/generate-sprint-fact-sheet.py --sprint sprint-001 --summary`
- OpenSpec：`openspec validate add-tilesfst-sprint-md-governance`
- 模板同步：`python pm-harness/scripts/validate-template-sync.py`

## 只读保护

本次应用只修改 ProjectPmHarness 当前仓库治理资产、active Change/Sprint 和模板资产；学习对象保持只读。
