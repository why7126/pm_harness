---
created_at: 2026-08-08 20:56:51
updated_at: 2026-08-31 09:13:31
---

# 规范工程变更历史

本文档用于记录 ProjectPmHarness 每一次规范、脚本、命令、技能、目录边界和模板治理能力更新的历史索引。

单次变更的详细说明仍以同目录下的 `YYYYMMDDhhmmss-study-xxx.md` 或 `YYYYMMDDhhmmss-governance-xxx.md` 为准；本文档只维护便于回溯的总账。

## 记录规则

- 新增或修改规范、脚本、命令、技能、目录边界、模板能力或校验规则后，MUST 在本文档追加一条记录。
- 记录按时间倒序维护，最新记录放在最上方。
- 每条记录 SHOULD 包含时间、类型、摘要、影响范围、其他项目落地提示词、关联日志、关联 Change / Sprint 和验证结果。
- 不得记录隐私、密钥、真实客户数据、未脱敏日志、本机绝对路径或学习对象源码。

## 变更历史

| 时间 | 类型 | 摘要 | 影响范围 | 其他项目落地提示词 | 关联日志 | 关联 Change / Sprint | 验证 |
|---|---|---|---|---|---|---|---|
| 2026-08-31 09:13:31 | 学习应用 | 从 TilesFST 应用 AI Usage session 默认自动发现、脱敏事实源边界和 compact hook 输出口径 | 根项目治理脚本、Workflow Sync/Sprint 技能、上下文预算规则、模板资产 | `请只读学习参考项目的 AI Usage session 自动发现治理：让 workflow hook 按显式 session、环境变量、AI_USAGE_SESSIONS_DIR 和本机默认 Codex sessions 目录自动发现；输出 compact summary，不持久化原始 session、本机路径、prompt、密钥或完整工具输出。` | `20260831091331-study-tilesfst-ai-usage-session-discovery.md` | `add-tilesfst-ai-usage-session-discovery` / `sprint-001` | 通过 |
| 2026-08-27 01:02:22 | 学习应用 | 从 TilesFST 应用 sprint.md Scope 合同、Scope 校验、追加范围脚本、Workflow Sync 派生刷新、归档 readiness 和 Fact Sheet read-first 复盘入口 | 根项目治理规则、Sprint 文档、Workflow Sync 脚本、技能、模板资产 | `请只读学习参考项目的 sprint.md Scope 合同、Sprint scope 校验、范围追加脚本、Workflow Sync 派生刷新、Sprint 归档 stale readiness 和 Fact Sheet read-first 复盘入口，并通过 active Change/Sprint 将适合本项目的治理能力改写落地；不得复制参考项目业务 Sprint 内容或修改学习对象。` | `20260827010222-study-tilesfst-sprint-md-governance.md` | `add-tilesfst-sprint-md-governance` / `sprint-001` | 通过 |
| 2026-08-27 00:26:26 | 学习应用 | 从 TilesFST 应用产品数据采集与链路观测标准、硬门禁脚本和工作流 Skill 数据采集声明门禁 | 根项目治理规则、脚本、技能、模板资产 | `请只读学习参考项目的产品数据采集与链路观测标准、硬门禁脚本和 REQ/OpenSpec/Sprint 工作流数据采集声明门禁，并通过 active Change/Sprint 将适合本项目的治理能力改写落地；不得复制参考项目业务表、接口路径、运行日志或端侧实现细节。` | `20260827002626-study-tilesfst-data-observability.md` | `add-tilesfst-data-observability-governance` / `sprint-001` | 通过 |
| 2026-08-27 00:11:53 | 学习应用 | 从 TilesFST 应用 BUG review confirmed 根因门禁、Sprint 选择门禁和最终输出契约卫生校验 | 根项目治理规则、脚本、技能、模板资产 | `请只读学习参考项目的 BUG review confirmed 根因门禁、Sprint active/连续编号选择脚本和 Final Output Contract 输出卫生校验，并通过 active Change/Sprint 将适合本项目的治理能力改写落地；不得引入未确认范围之外的 AI Usage 矩阵治理。` | `20260827001153-study-tilesfst-command-governance.md` | `add-tilesfst-command-governance` / `sprint-001` | 通过 |
| 2026-08-21 22:34:59 | 学习应用 | 从 TilesFST 应用版本升级路径治理、文档表达卫生和最小相关验证矩阵 | 根项目治理规则、脚本、技能、模板资产 | `请只读学习参考项目的 upgrade-plan/upgrade-validate、版本升级路径对象、文档表达卫生审计和命令最小相关验证矩阵，并通过 active Change/Sprint 将适合本项目的治理能力改写落地；upgrade 命令只生成和校验计划，不自动执行生产升级或修改真实 env。` | `20260821223459-study-tilesfst-upgrade-governance.md` | `add-tilesfst-upgrade-governance` / `sprint-001` | 通过；文档卫生返回非阻塞 warning |
| 2026-08-21 08:24:48 | 学习应用 | 从 ProjectMoonBox 应用证据化根因、执行复盘、UI 返修对照、REQ 子文档扫尾和 Workflow Sync 输出增量治理 | 根项目治理规则、脚本、技能、模板资产 | `请只读学习参考项目的证据化根因分析、命令执行复盘 Hook、UI 型 opsx-modify 附件截图对照、REQ 子文档一致性扫尾和 Workflow Sync Issue 输出/下一步推导，并通过 active Change/Sprint 将适合本项目的治理能力改写落地。` | `20260821082448-study-projectmoonbox-governance-increments.md` | `apply-projectmoonbox-governance-increments` / `sprint-001` | 通过 |
| 2026-08-19 11:28:41 | 学习应用 | 从 DeepSeek Harness 应用治理决策记录、文档层级与一事实一归属、治理检查聚合器 | 根项目治理规则、脚本、文档目录、模板资产 | `请只读学习参考项目的 Agent Notes、文档层级/事实归属和检查聚合脚本，将适合本项目的治理决策记录、文档事实源规则和只读治理检查聚合器，通过 active Change/Sprint 改写落地。` | `20260819112841-study-deepseek-governance-patterns.md` | `add-deepseek-governance-patterns` / `sprint-001` | 通过 |
| 2026-08-10 23:19:03 | 学习应用 | 从 ProjectMoonBox 应用 Git 安全、Issue 当前态索引、命令顺序、Prototype UI 验收、spec-study 日志优先和引导式反馈治理模式 | 根项目治理规则、脚本、技能、模板资产 | `请只读学习参考项目的 git-check、issues CHANGELOG 当前态索引、命令执行顺序、prototype UI 验收、spec-study 日志优先学习和引导式反馈契约，并通过 active Change/Sprint 将适合本项目的治理能力改写落地。` | `20260810231903-study-projectmoonbox-governance-patterns.md` | `apply-projectmoonbox-governance-patterns` / `sprint-001` | 通过 |
| 2026-08-08 21:03:04 | 规范 / 文档 | 为 `CHANGELOG.md` 新增“其他项目落地提示词”列 | 规范工程变更历史总账 | `请在 docs/spec-logs/CHANGELOG.md 的变更历史表中新增“其他项目落地提示词”列，并为每条规范/脚本/命令/技能更新记录补充可复制的跨项目落地 prompt。` | `20260808210304-governance-changelog-adoption-prompts.md` | `add-spec-logs-changelog` / `sprint-001` | 通过 |
| 2026-08-08 20:56:51 | 规范 / 文档 | 新增规范工程变更历史总账 `docs/spec-logs/CHANGELOG.md` | 当前 ProjectPmHarness 运行态治理文档 | `请在 docs/spec-logs/ 下新增 CHANGELOG.md，作为规范、脚本、命令、技能、目录边界和模板治理能力更新的变更历史总账，并按时间倒序维护记录。` | `20260808205651-governance-spec-logs-changelog.md` | `add-spec-logs-changelog` / `sprint-001` | 通过 |
| 2026-08-07 15:23:44 | 规范 / 入口 | 新增根目录 `AGENTS.md`，明确当前脚手架工程自身 AI 行为入口 | 根项目治理入口、OpenSpec、Sprint | `请为当前仓库新增根目录 AGENTS.md，作为项目自身 AI 行为入口，明确根项目运行态治理资产与模板目录的边界、技能入口、读取路由和执行红线。` | `20260807152344-governance-root-agents-entrypoint.md` | `add-root-agents-entrypoint` / `sprint-001` | 通过 |
| 2026-08-07 15:10:22 | 规范 / 学习应用 | 从 TilesFST 学习并补齐 `docs/spec-logs/README.md` 与模板日志同步边界 | spec 日志目录说明、模板同步脚本 | `请为 docs/spec-logs/ 新增 README.md，定义 study/governance 日志命名、去重、隐私和源码边界，并让模板同步脚本同步 README 但忽略时间戳开头的实际日志。` | `20260807151022-study-tilesfst-spec-opt-study-refresh.md` | 无 | 通过 |
| 2026-08-07 13:56:18 | 规范 / 目录 | 新增根目录 `issues/`、`iterations/`、`openspec/`，补齐 ProjectPmHarness 自身 Harness 治理骨架 | 根项目治理目录、OpenSpec 配置 | `请为脚手架工程自身新增根目录 issues/、iterations/、openspec/，作为当前项目运行态治理资产，并明确这些目录不得同步进模板目录。` | `20260807135618-governance-root-harness-dirs.md` | 无 | 通过 |
| 2026-08-07 13:13:52 | 规范 / 文档 | 新增根目录 `docs/` 长期文档边界，明确当前项目与脚手架模板职责 | 根 docs、项目治理边界 | `请为脚手架工程自身新增根目录 docs/，沉淀长期产品、架构、治理和维护文档，并区分当前项目运行态文档与模板目录内文档。` | `20260807131352-governance-project-root-docs-boundary.md` | 无 | 通过 |
| 2026-08-07 12:17:51 | 学习应用 | 从 TilesFST 学习并引入 `spec-study`、增强 `spec-opt` 与规范工程日志机制 | `.agents/skills`、规则、脚本、模板资产 | `请只读学习参考项目的 spec-study/spec-opt、docs/spec-logs、规则和校验脚本，将适合本项目的跨项目学习、治理日志和只读保护机制转写进本项目治理资产。` | `20260807121751-study-tilesfst-spec-governance.md` | 无 | 通过 |
