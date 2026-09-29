---
created_at: 2026-08-27 00:26:26
updated_at: 2026-08-27 00:26:26
---

# Design

## 方案

本 Change 采用“长期标准 + 硬门禁脚本 + 工作流 Skill 声明”的三层设计：

- 长期标准：新增 `docs/standards/product-data-collection-observability.md`，定义使用事件、请求日志、Task Trace、端请求封装和治理声明字段。
- 硬门禁：新增 `scripts/validate-product-data-observability-standard.py` 与 `scripts/validate-product-data-observability-gates.py`，分别校验标准完整性和触达面声明。
- 工作流接入：REQ、OpenSpec、Sprint 命令 Skill 在前置阶段读取标准，并要求声明 `product_data_collection_observability`、`affected_layers`、`reason` 和 `validation`；N/A 使用 `not_applicable` 或 N/A 原因。

## 模板同步

会影响未来生成的新项目，因此同步到：

- `pm-harness/`
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/`
- 本机安装版 `/Users/why7126/.codex/skills/pm-harness-init`

## 风险与取舍

- 脚本采用关键词触发，不替代人工判断；误报通过补齐 N/A 或 `not_applicable` 原因处理。
- 当前仓库自身无业务 `src/` 触达，本次只验证治理资产、模板资产和 active Change/Sprint 事实源。
- 标准内容适配为 PM Harness 通用治理语言，不复制 TilesFST 业务实现细节。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 设计层新增数据采集观测标准和声明硬门禁，属于工作流治理触达；业务 API、DB、端请求实现均不适用。
  validation: 通过 change-specific 门禁校验和模板校验复核。
```
