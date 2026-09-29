---
created_at: 2026-08-27 01:02:22
updated_at: 2026-08-27 01:02:22
---

# Tasks

根因状态：不适用。本 Change 为 Sprint 文档治理应用，不处理具体 BUG 根因。

- [x] 创建并纳入 TilesFST `sprint.md` 治理学习应用 Change。
- [x] 提升 Sprint scope 追加、Scope 校验、archive readiness、stale scan、Fact Sheet 和 Workflow Sync 脚本到根项目运行态。
- [x] 更新 Sprint 相关 Skill 和 Workflow Sync Skill。
- [x] 新增根项目 `rules/iterations-lifecycle.md` 并更新入口索引。
- [x] 将 `sprint-001/sprint.md` 调整为目标编号列表 + Scope 六列表 + workflow-sync 分组结构。
- [x] 同步新项目模板、init-skill 模板资产和本机安装版。
- [x] 生成本次 spec-study 学习应用报告并更新 CHANGELOG。
- [x] 运行 Sprint scope、archive readiness、Fact Sheet、治理校验、模板校验、Workflow Sync、AI Usage 和只读保护复核。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: tasks 跟踪的是 Sprint 文档治理和脚本门禁；业务运行时数据采集不适用。
  validation: 运行 `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-sprint-md-governance`。
```
