---
created_at: 2026-08-27 01:02:22
updated_at: 2026-08-27 01:02:22
---

# Test Plan

## 验证矩阵

| 范围 | 命令 |
|---|---|
| Sprint 选择 | `python scripts/validate-sprint-selection.py --json` |
| Sprint Scope 合同 | `python scripts/validate-sprint-scope.py sprint-001 --item add-tilesfst-sprint-md-governance` |
| Sprint archive readiness | `python scripts/validate-sprint-archive-readiness.py --sprint sprint-001 --change add-tilesfst-sprint-md-governance` |
| Sprint stale scan | `python scripts/check-sprint-close-stale-scan.py --sprint sprint-001` |
| Sprint Fact Sheet | `python scripts/generate-sprint-fact-sheet.py --sprint sprint-001 --summary` |
| 产品数据观测门禁 | `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-sprint-md-governance` |
| Agent 上下文预算 | `python scripts/validate-agent-context-budget.py` |
| OpenSpec 文案 | `python scripts/validate-openspec-language.py` |
| OpenSpec Change | `openspec validate add-tilesfst-sprint-md-governance` |
| 目录边界 | `python scripts/validate-directory-structure.py` |
| 模板同步 | `python pm-harness/scripts/validate-template-sync.py` |
| 模板目录 | `python pm-harness/scripts/validate-directory-structure.py` |
| 模板 Skill | `python pm-harness/scripts/validate-skill-package.py` |
| 模板上下文预算 | `python pm-harness/scripts/validate-agent-context-budget.py` |

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 测试计划覆盖 Sprint 文档治理门禁；业务 API、DB 或端请求实现不适用。
  validation: 以本文件验证矩阵的通过结果为准。
```
