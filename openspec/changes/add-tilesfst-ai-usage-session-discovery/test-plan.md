---
created_at: 2026-08-31 09:13:31
updated_at: 2026-08-31 09:13:31
---

# Test Plan

## Commands

- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event explore --dry-run --json`
- `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-ai-usage-session-discovery`
- `python scripts/validate-sprint-scope.py sprint-001 --item add-tilesfst-ai-usage-session-discovery`
- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate add-tilesfst-ai-usage-session-discovery`
- `python pm-harness/scripts/validate-template-sync.py`
- `python pm-harness/scripts/validate-directory-structure.py`
- `python pm-harness/scripts/validate-skill-package.py`
- `python pm-harness/scripts/validate-agent-context-budget.py`

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: test-plan 校验 workflow hook 的自动发现、脱敏输出和治理门禁。
  validation: 本文件列出的 hook dry-run 与产品数据观测门禁。
```
