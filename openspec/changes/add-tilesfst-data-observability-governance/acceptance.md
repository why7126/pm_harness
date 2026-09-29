---
created_at: 2026-08-27 00:26:26
updated_at: 2026-08-27 00:26:26
---

# Acceptance

## 验收标准

- [x] 已新增产品数据采集与链路观测长期标准。
- [x] 已新增标准完整性校验与硬门禁脚本。
- [x] REQ、OpenSpec、Sprint 工作流 Skill 已接入数据采集声明门禁。
- [x] `pm-harness/` 与 init-skill 模板资产已同步。
- [x] 本 Change 自身包含 `product_data_collection_observability` 声明、`affected_layers`、`reason` 和 `validation`。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 验收确认治理门禁落地；业务运行时数据采集层不在本次范围。
  validation: 运行本 Change test-plan 中的最小相关验证矩阵。
```
