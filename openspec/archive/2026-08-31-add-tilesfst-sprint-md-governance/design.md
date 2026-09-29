---
created_at: 2026-08-27 01:02:22
updated_at: 2026-08-27 01:02:22
---

# Design

## 方案

本 Change 采用“机器事实源 + 派生刷新 + 收口校验”的 Sprint 文档治理设计：

- `sprint.yaml` 继续作为 Sprint 范围机器事实源。
- `sprint.md` 增加 `## 1. 目标` 的 Sprint 目标编号列表，并保持 `## 2. Scope` 主表六列。
- `scripts/add-sprint-scope-item.py` 用于向既有 Sprint 串行追加 REQ、BUG 或 Change 范围。
- `scripts/validate-sprint-scope.py` 校验目标编号列表、Scope 主表和 Workflow Sync 分组表与 `sprint.yaml` 一致。
- Workflow Sync 使用 `scripts/workflow_sync/` 派生刷新 Sprint 四件套中的状态摘要。
- `/sprint-archive` 使用 readiness、stale scan 和归档路径残留检查阻断陈旧中间态文案。
- `/sprint-exps` 使用 Fact Sheet summary-first 策略降低读取成本。

## 模板同步

本能力会影响未来生成的新项目，因此同步到：

- `pm-harness/`
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/`
- 本机安装版 `pm-harness-init`

## 风险与取舍

- 根项目运行态首次启用完整 Workflow Sync 包，需要通过聚焦脚本校验当前 `sprint-001`。
- `sprint.md` 中的 workflow-sync marker block 由脚本维护，人工只改非派生段落。
- 当前 ProjectPmHarness 的 Sprint 主要承载治理 Change，REQ/BUG 分组为空是合法状态。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 设计层新增 Sprint 文档派生刷新和校验门禁，属于工作流治理触达；业务数据采集不适用。
  validation: 以本 Change test-plan 的最小相关验证矩阵为准。
```
