---
created_at: 2026-08-31 09:13:31
updated_at: 2026-08-31 09:13:31
---

# Proposal

## Why

ProjectPmHarness 已具备 AI Usage 聚合脚本能力，但根项目 `extract-ai-usage.py` 仍是占位入口，Workflow Sync 与 Sprint 技能说明也未完整表达默认 session 自动发现顺序。常规 workflow hook 因此容易输出低信息量 summary 或误导操作者必须手工提供 session。

## What Changes

- 将根项目 `scripts/extract-ai-usage.py` 接到 `scripts/ai_usage.py` 的真实 CLI。
- 明确 AI Usage session 发现顺序：显式参数、环境变量、`AI_USAGE_SESSIONS_DIR`、本机默认 Codex sessions 目录。
- 新增 `data/ai-usage/README.md`，记录脱敏事实源、原始 session 禁止入库和历史回溯边界。
- 同步根项目、`pm-harness/` 模板、init-skill 模板资产和本机安装版。
- 通过 active Change 与 Sprint scope 记录本次跨项目学习应用。

## Non-Goals

- 不复制 TilesFST 原始 session、usage snapshot 或业务数据。
- 不修改业务 `src/`、API、DB、Web、小程序、管理端、Orval 或 Docker Compose。
- 不改变 AI Usage 的持久化 schema，只修正入口和治理说明。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 本 Change 触达 workflow AI Usage hook 与本地脱敏事实源治理，不改业务运行时产品数据采集。
  validation: 运行 AI Usage hook dry-run、Sprint scope、OpenSpec、目录结构、模板同步和产品数据观测门禁。
```
