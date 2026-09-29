---
created_at: 2026-08-27 00:26:26
updated_at: 2026-08-27 00:26:26
---

# Trace

## 来源

- 命令：`/spec-study apply TilesFST product-data-collection-observability-standard product-data-observability-hard-gate workflow-skill-data-collection-gate`
- 学习对象：`ProjectTilesFST`
- 学习模式：`--focus 数据采集`
- Sprint：`sprint-001`

## 只读保护

学习对象作为外部只读输入读取。应用阶段只修改 ProjectPmHarness 当前仓库治理资产与模板资产，不修改学习对象。

## 影响映射

| 采纳项 | 本项目落点 |
|---|---|
| product-data-collection-observability-standard | `docs/standards/product-data-collection-observability.md`、模板同名文件 |
| product-data-observability-hard-gate | `scripts/validate-product-data-observability-standard.py`、`scripts/validate-product-data-observability-gates.py`、模板同名文件 |
| workflow-skill-data-collection-gate | REQ、OpenSpec、Sprint 工作流 Skill 与模板同名文件 |

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 本 Change 触达工作流治理层，要求后续 API、DB、日志审计、行为埋点、Task Trace 和端请求封装相关变更显式声明观测影响；本次不改业务运行时数据采集。
  validation: 运行 `python scripts/validate-product-data-observability-standard.py`、`python scripts/validate-product-data-observability-gates.py --change add-tilesfst-data-observability-governance` 和模板同步校验。
```
