---
created_at: 2026-10-28 11:15:57
updated_at: 2026-10-28 11:36:10
---

## Why

Git 检查读取工作区而非暂存快照，命中行输出可能泄露同一行的凭证，整行与子串豁免可能漏检。需要将 MoonBox G1–G4 适配为可复用的扫描和同步治理。

## What Changes

- 分离 index、worktree 和待推送历史扫描，忽略真实本地 env 的未跟踪内容。
- 输出不含内容片段；使用精确占位符和路径规则，补正反例回归。
- 建立 env 忽略双向校验与 git-sync 技能，同步模板和 init 资产。

## Capabilities

### New Capabilities
- `git-delivery-safety`: 暂存与历史安全检查、脱敏报告、交付范围同步和发布标签门禁。

### Modified Capabilities
无。

## Impact

影响 scripts、规则、技能、模板及治理文档；不涉及业务 API、DB、Web、小程序、管理端、Orval 或 Docker Compose 运行配置。

product_data_collection_observability: not_applicable
affected_layers: []
reason: 仅本地 Git 静态检查与命令契约，不新增产品事件或日志采集。
validation: 临时仓库回归、模板同步与治理校验。
