---
created_at: 2026-08-31 09:13:31
updated_at: 2026-08-31 09:13:31
---

# Design

## Context

TilesFST 的 AI Usage 治理已将本机 Codex sessions 目录纳入默认发现链路，并要求 hook 输出 compact summary。ProjectPmHarness 已同步核心 `ai_usage.py`，但入口脚本和技能文案仍落后。

## Approach

1. 保持 `ai_usage.py` 为唯一实现入口，`extract-ai-usage.py` 只做薄 wrapper，避免双实现漂移。
2. 在 Workflow Sync、Sprint Archive、Sprint Exps 和上下文预算规则中描述统一发现顺序。
3. 用 `data/ai-usage/README.md` 承接长期安全边界：只保存脱敏聚合，不保存原始 session 或本机路径。
4. 模板同步时只放规则、脚本和 README，不同步当前项目的真实 `data/ai-usage` 运行态 JSON。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: design 约束 AI Usage hook 的 session 输入发现、脱敏写入和输出摘要，不涉及业务 API 或数据库采集。
  validation: 使用 `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-ai-usage-session-discovery`。
```
