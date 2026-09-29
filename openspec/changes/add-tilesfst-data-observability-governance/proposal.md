---
created_at: 2026-08-27 00:26:26
updated_at: 2026-08-27 00:26:26
---

# 应用 TilesFST 产品数据采集与链路观测治理

## 背景

`/spec-study TilesFST --focus 数据采集` 已完成只读学习，并确认应用以下候选项：

- `product-data-collection-observability-standard`
- `product-data-observability-hard-gate`
- `workflow-skill-data-collection-gate`

这些内容属于长期治理标准、校验脚本和工作流 Skill 门禁变化，必须通过 active OpenSpec Change 承载，并纳入 Sprint scope。

## 目标

- 建立产品数据采集、请求日志、Task Trace 和端请求封装的长期治理标准。
- 增加标准完整性校验与 REQ/BUG/Change/Sprint 触达面硬门禁。
- 将门禁接入 REQ、OpenSpec 和 Sprint 命令技能。
- 同步 `pm-harness/` 新项目模板和 init-skill 模板资产。

## 非目标

- 不引入 TilesFST 的具体业务表、接口、埋点事件或日志实现。
- 不修改学习对象 TilesFST。
- 不修改 `src/` 业务代码、API、数据库、Web、小程序、管理端或 Orval 生成物。
- 不直接修改 `openspec/specs/` 正式规格。

## 影响范围

- 根项目 `docs/standards/`、`rules/`、`.agents/skills/`、`scripts/`、`docs/spec-logs/` 和 active Change/Sprint 事实源。
- `pm-harness/` 新项目模板。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 初始化模板资产。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 本 Change 新增产品数据采集与链路观测治理标准、硬门禁脚本和工作流技能声明要求；不触达业务 API、DB、端请求实现或运行时日志数据。
  validation: 运行标准校验、门禁脚本、OpenSpec 校验、模板同步校验、Workflow Sync 和 AI Usage hook。
```
