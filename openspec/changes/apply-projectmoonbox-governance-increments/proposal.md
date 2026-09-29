---
created_at: 2026-08-21 08:24:48
updated_at: 2026-08-21 08:24:48
---

# 应用 ProjectMoonBox 增量治理模式

## 背景

`/spec-study MoonBox` 已完成只读学习，并确认应用 ProjectMoonBox 在既有治理模式之后沉淀的增量候选项：

- `root-cause-evidence-governance`
- `command-execution-review-hook`
- `opsx-modify-ui-screenshot-comparison-gate`
- `opsx-modify-req-subdocument-sweep`
- `workflow-sync-issue-output-next`

这些内容属于治理扩展、命令契约和校验脚本行为变化，必须通过 active OpenSpec Change 承载，并纳入 Sprint scope。

## 目标

- 为 ProjectPmHarness 补齐证据化根因分析规则与校验入口。
- 为 workflow 命令补齐执行链路复盘输出契约。
- 为 UI 型 `/opsx-modify` 补齐附件截图逐项视觉对照门禁。
- 为 REQ 来源 `/opsx-modify` 补齐子文档一致性扫尾检查。
- 优化 Workflow Sync 对 Issue 子文档 apply 和下一步推导的说明边界。

## 非目标

- 不修改学习对象 ProjectMoonBox。
- 不复制 ProjectMoonBox 的业务事实、运行时数据、源码或长脚本。
- 不修改 `src/` 业务代码。
- 不直接修改 `openspec/specs/` 正式规格。
- 不恢复 `.claude`、`.codex`、`.cursor`、`.kiro`、`.opencode` 等多 Agent 入口。

## 影响范围

- 根项目治理规则、文档、脚本、Skill、OpenSpec Change 和 Sprint scope。
- `pm-harness/` 新项目模板。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 初始化模板资产。
- 不影响 API、数据库、Web、小程序、管理端、Orval、Docker Compose 或运行时代码。
