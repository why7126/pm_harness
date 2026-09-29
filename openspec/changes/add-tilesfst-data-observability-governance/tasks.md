---
created_at: 2026-08-27 00:26:26
updated_at: 2026-08-27 00:26:26
---

# Tasks

根因状态：不适用。本 Change 为治理规则应用，不处理具体 BUG 根因；校验目标是建立后续产品数据采集与链路观测门禁。

- [x] 创建并纳入 TilesFST 数据采集治理学习应用 Change。
- [x] 新增产品数据采集与链路观测长期标准。
- [x] 新增标准完整性校验脚本。
- [x] 新增产品数据采集观测声明硬门禁脚本。
- [x] 将门禁接入 REQ、OpenSpec 和 Sprint 工作流 Skill。
- [x] 同步新项目模板与 init-skill 模板资产。
- [x] 生成本次 spec-study 学习应用报告并更新 CHANGELOG。
- [x] 运行治理校验、模板校验、Workflow Sync、AI Usage 和只读保护复核。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: tasks 跟踪的是治理标准、脚本、Skill 和模板同步；业务运行时数据采集不适用。
  validation: 所有任务完成后运行 `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-data-observability-governance`。
```
