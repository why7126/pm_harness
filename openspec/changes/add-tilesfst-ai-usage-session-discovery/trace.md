---
created_at: 2026-08-31 09:13:31
updated_at: 2026-08-31 09:13:31
---

# Trace

## 来源

- 命令：`/spec-study apply TilesFST ai-usage-session-auto-discovery`
- 学习对象：`ProjectTilesFST`
- 学习模式：`auto`
- Sprint：`sprint-001`

## 只读保护

学习对象作为外部只读输入读取。应用阶段只修改 ProjectPmHarness 当前仓库治理资产、模板资产和 active Change/Sprint 事实源，不修改学习对象。

## 影响映射

| 采纳项 | 本项目落点 |
|---|---|
| ai-usage-session-auto-discovery | `scripts/extract-ai-usage.py`、`scripts/ai_usage.py`、`.agents/skills/workflow-sync/SKILL.md`、`.agents/skills/sprint-archive/SKILL.md`、`.agents/skills/sprint-exps/SKILL.md`、`rules/agent-context-budget.md`、`data/ai-usage/README.md` |

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 本 Change 触达 workflow AI Usage hook，不改业务运行时数据采集。
  validation: 运行 AI Usage hook dry-run、Sprint scope、OpenSpec 和产品数据观测门禁校验。
```
