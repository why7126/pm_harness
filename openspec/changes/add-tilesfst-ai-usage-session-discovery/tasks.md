---
created_at: 2026-08-31 09:13:31
updated_at: 2026-08-31 09:13:31
---

# Tasks

根因状态：不适用。本 Change 为 AI Usage workflow 治理应用，不处理具体 BUG 根因。

- [x] 创建并纳入 TilesFST AI Usage session 自动发现学习应用 Change。
- [x] 将根项目 `scripts/extract-ai-usage.py` 接入真实 `ai_usage.py` CLI。
- [x] 更新 Workflow Sync、Sprint Archive、Sprint Exps 和上下文预算规则的 session 发现说明。
- [x] 新增 `data/ai-usage/README.md` 并同步模板资产。
- [x] 生成本次 spec-study 学习应用报告并更新 CHANGELOG。
- [x] 运行 AI Usage hook、治理校验、模板校验、Workflow Sync、AI Usage 和只读保护复核。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: tasks 跟踪 AI Usage workflow hook 和本地脱敏事实源治理；业务运行时产品数据采集不适用。
  validation: 运行 `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-ai-usage-session-discovery`。
```
