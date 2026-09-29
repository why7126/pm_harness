---
created_at: 2026-08-27 00:26:26
updated_at: 2026-08-27 00:26:26
---

# Test Plan

## 验证矩阵

| 范围 | 命令 |
|---|---|
| 标准完整性 | `python scripts/validate-product-data-observability-standard.py` |
| 当前 Change 门禁 | `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-data-observability-governance` |
| Agent 上下文预算 | `python scripts/validate-agent-context-budget.py` |
| OpenSpec 文案 | `python scripts/validate-openspec-language.py` |
| OpenSpec Change | `openspec validate add-tilesfst-data-observability-governance` |
| 目录边界 | `python scripts/validate-directory-structure.py` |
| 模板同步 | `python pm-harness/scripts/validate-template-sync.py` |
| 模板目录 | `python pm-harness/scripts/validate-directory-structure.py` |
| 模板 Skill | `python pm-harness/scripts/validate-skill-package.py` |
| 模板上下文预算 | `python pm-harness/scripts/validate-agent-context-budget.py` |
| 模板标准完整性 | `python pm-harness/scripts/validate-product-data-observability-standard.py` |
| 模板门禁入口 | `python pm-harness/scripts/validate-product-data-observability-gates.py` |

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 测试计划覆盖治理门禁自身，验证后续数据采集相关变更的声明要求。
  validation: 以本文件验证矩阵的通过结果为准；不触达业务 API、DB 或端请求实现。
```
