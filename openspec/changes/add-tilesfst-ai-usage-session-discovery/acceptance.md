---
created_at: 2026-08-31 09:13:31
updated_at: 2026-08-31 09:13:31
---

# Acceptance

- [x] 根项目 `extract-ai-usage.py` 不再是 placeholder。
- [x] AI Usage session 自动发现顺序写入规则、技能和 `data/ai-usage/README.md`。
- [x] 模板资产同步，不包含当前项目真实 usage JSON 或原始 session。
- [x] Workflow Sync 与 AI Usage hook 可用。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: acceptance 验收的是 workflow AI Usage 治理能力。
  validation: 运行 AI Usage hook dry-run、Workflow Sync、AI Usage post-command hook 和产品数据观测门禁。
```
