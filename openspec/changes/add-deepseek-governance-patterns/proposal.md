---
created_at: 2026-08-19 11:25:48
updated_at: 2026-08-19 11:25:48
---

# 应用 DeepSeek Harness 治理模式

## 背景

`/spec-study https://github.com/deepseek-ai/deepseek-harness` 已完成只读学习，并确认应用以下候选项：

- Agent Decision Notes
- 文档层级与一事实一归属
- 治理检查聚合器

这些内容属于治理扩展、目录边界说明和脚本校验行为变化，必须通过 active OpenSpec Change 承载，并纳入 Sprint scope。

## 目标

- 为 ProjectPmHarness 根项目和新项目模板补齐治理决策记录规范。
- 为文档治理补齐文档层级、事实归属和链接替代重复的规则。
- 新增根项目治理校验聚合脚本，统一运行常用只读校验。
- 生成本次 `/spec-study apply` 学习应用报告，并更新规范工程变更历史。

## 非目标

- 不修改学习对象 DeepSeek Harness。
- 不恢复 `.claude`、`.codex`、`.cursor`、`.kiro`、`.opencode` 等多 Agent 入口。
- 不修改 `src/` 业务代码。
- 不直接修改 `openspec/specs/` 正式规格。
- 不复制 DeepSeek Harness 的源码、长规范或运行时架构。

## 影响范围

- 根项目治理规则、文档、脚本、OpenSpec Change 和 Sprint scope。
- `pm-harness/` 新项目模板。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 初始化模板资产。
- 不影响 API、数据库、Web、小程序、管理端、Orval 或运行时代码。
