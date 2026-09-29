---
created_at: 2026-08-07 15:23:44
updated_at: 2026-08-31 09:17:28
note: workflow-sync — workflow-sync 自动同步 — 4/11 Change archived；7 applied；Sprint `planning`
---

# sprint-001 ProjectPmHarness 根级治理入口

## 1. 目标

补齐 ProjectPmHarness 自身 Harness 治理入口，避免 AI 将 `pm-harness/AGENTS.md` 模板入口误用于当前脚手架工程。

Sprint 目标编号列表：

- add-root-agents-entrypoint
- add-spec-logs-changelog
- apply-projectmoonbox-governance-patterns
- default-review-approve
- add-deepseek-governance-patterns
- apply-projectmoonbox-governance-increments
- add-tilesfst-upgrade-governance
- add-tilesfst-command-governance
- add-tilesfst-data-observability-governance
- add-tilesfst-sprint-md-governance
- add-tilesfst-ai-usage-session-discovery

### add-root-agents-entrypoint 要点

新增根目录 `AGENTS.md`，明确当前脚手架工程自身 AI 行为入口与模板目录边界。

### add-spec-logs-changelog 要点

新增 `docs/spec-logs/CHANGELOG.md`，作为规范、脚本、命令和技能更新历史总账。

### apply-projectmoonbox-governance-patterns 要点

应用 Git 安全、Issue 当前态索引、命令顺序、Prototype UI 验收和引导式反馈治理模式。

### default-review-approve 要点

将 review 命令默认语义调整为正向通过，反向结果必须显式声明。

### add-deepseek-governance-patterns 要点

应用文档层级、一事实一归属、治理决策记录和治理检查聚合思路。

### apply-projectmoonbox-governance-increments 要点

应用证据化根因、执行复盘、UI 返修对照、REQ 子文档扫尾和 Workflow Sync 输出增量治理。

### add-tilesfst-upgrade-governance 要点

应用版本升级路径治理、文档表达卫生和最小相关验证矩阵。

### add-tilesfst-command-governance 要点

应用 BUG review confirmed 根因门禁、Sprint 选择脚本和最终输出契约卫生校验。

### add-tilesfst-data-observability-governance 要点

应用产品数据采集与链路观测长期标准、硬门禁脚本和工作流 Skill 声明门禁。

### add-tilesfst-sprint-md-governance 要点

应用 `sprint.md` Scope 合同、Scope 校验、追加范围脚本、Workflow Sync 派生刷新、归档 readiness 和 Fact Sheet read-first 复盘入口。

### add-tilesfst-ai-usage-session-discovery 要点

应用 AI Usage session 默认自动发现、脱敏事实源边界和 compact hook 输出口径。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| Change | add-root-agents-entrypoint | Root AGENTS entrypoint | archived | - | 已归档根入口治理 |
| Change | add-spec-logs-changelog | Spec logs changelog | applied | - | 已建立 spec-logs 总账 |
| Change | apply-projectmoonbox-governance-patterns | ProjectMoonBox governance patterns | applied | - | 已应用基础治理模式 |
| Change | default-review-approve | Default review approve | archived | - | 已归档 review 默认语义 |
| Change | add-deepseek-governance-patterns | DeepSeek governance patterns | applied | - | 已应用文档治理模式 |
| Change | apply-projectmoonbox-governance-increments | ProjectMoonBox governance increments | applied | - | 已应用质量治理增量 |
| Change | add-tilesfst-upgrade-governance | TilesFST upgrade governance | archived | - | 已归档升级治理 |
| Change | add-tilesfst-command-governance | TilesFST command governance | applied | - | 已应用命令门禁 |
| Change | add-tilesfst-data-observability-governance | TilesFST data observability governance | applied | - | 已应用数据采集观测治理 |
| Change | add-tilesfst-sprint-md-governance | TilesFST sprint.md governance | archived | - | 已归档 Sprint 文档治理 |
| Change | add-tilesfst-ai-usage-session-discovery | TilesFST AI Usage session discovery | applied | - | 已应用 AI Usage session 自动发现治理 |

REQ：无正式范围；BUG：无正式范围；当前 Sprint 仅承载 ProjectPmHarness 根级治理 Change。

Change：已纳入 10 个纯治理 Change；执行开发与归档时以 Scope 表状态、关联 Change 和 acceptance-report 为准。

### 包含需求

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
<!-- workflow-sync:scope-requirements:end -->

### 包含 BUG

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
<!-- workflow-sync:scope-bugs:end -->

### 包含 Change

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-root-agents-entrypoint` | — | archived | archived `add-root-agents-entrypoint`（2026-08-07 23:59:59） |
| `add-spec-logs-changelog` | — | applied | apply 6/6；待 archive `add-spec-logs-changelog` |
| `apply-projectmoonbox-governance-patterns` | — | applied | apply 10/10；待 archive `apply-projectmoonbox-governance-patterns` |
| `add-deepseek-governance-patterns` | — | applied | apply 7/7；待 archive `add-deepseek-governance-patterns` |
| `apply-projectmoonbox-governance-increments` | — | applied | apply 9/9；待 archive `apply-projectmoonbox-governance-increments` |
| `default-review-approve` | — | archived | archived `default-review-approve`（2026-08-21 23:59:59） |
| `add-tilesfst-upgrade-governance` | — | archived | archived `add-tilesfst-upgrade-governance`（2026-08-21 23:59:59） |
| `add-tilesfst-command-governance` | — | applied | apply 7/7；待 archive `add-tilesfst-command-governance` |
| `add-tilesfst-data-observability-governance` | — | applied | apply 8/8；待 archive `add-tilesfst-data-observability-governance` |
| `add-tilesfst-sprint-md-governance` | — | archived | archived `add-tilesfst-sprint-md-governance`（2026-08-31 23:59:59） |
| `add-tilesfst-ai-usage-session-discovery` | — | applied | apply 6/6；待 archive `add-tilesfst-ai-usage-session-discovery` |
<!-- workflow-sync:scope-changes:end -->

## 3. 验收

- 根目录存在 `AGENTS.md`。
- `AGENTS.md` 明确当前项目运行态目录和模板目录边界。
- 治理校验通过。
- ProjectMoonBox 治理学习应用报告落入 `docs/spec-logs/`，并完成只读保护复核。
- TilesFST 升级治理、文档卫生和最小相关验证矩阵通过 active Change 落地，并完成模板同步与只读保护复核。
- TilesFST 命令治理门禁通过 active Change 落地：BUG review confirmed 根因门禁、Sprint 选择脚本和最终输出契约卫生校验均通过验证。
- TilesFST 产品数据采集与链路观测治理通过 active Change 落地：长期标准、硬门禁脚本和工作流 Skill 数据采集声明门禁均通过验证。
- TilesFST `sprint.md` 治理通过 active Change 落地：Scope 合同、追加范围脚本、Scope 校验、Workflow Sync 派生刷新、归档 readiness 和 Fact Sheet read-first 均通过验证。
- TilesFST AI Usage session 自动发现治理通过 active Change 落地：真实 CLI wrapper、默认 session 自动发现说明、脱敏事实源边界和模板同步均通过验证。
