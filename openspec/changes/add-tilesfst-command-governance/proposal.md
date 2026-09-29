---
created_at: 2026-08-27 00:04:20
updated_at: 2026-08-27 00:04:20
---

# 应用 TilesFST 命令治理门禁

## 背景

`/spec-study TilesFST` 已完成只读学习，并确认应用以下候选项：

- `bug-review-confirmed-gate`
- `sprint-propose-selection`
- `final-output-contract-hygiene`

这些内容属于命令技能、治理脚本和校验行为变化，必须通过 active OpenSpec Change 承载，并纳入 Sprint scope。

## 目标

- 为 `/bug-review` approve 路径增加 `root_cause_status: confirmed` 与证据链硬门禁。
- 为 `/sprint-propose` 增加 active Sprint 选择、连续编号和归档冻结门禁。
- 为已有 Final Output Contract 增加输出卫生校验，阻止尖括号模板、通用示例和重复确认反模式泄漏到用户可见回复。

## 非目标

- 不引入 TilesFST 的 AI Usage 未观测矩阵治理。
- 不修改学习对象 TilesFST。
- 不修改 `src/` 业务代码、API、数据库、Web、小程序、管理端或 Orval 生成物。
- 不直接修改 `openspec/specs/` 正式规格。

## 影响范围

- 根项目 `.agents/skills/`、`rules/`、`scripts/`、`docs/spec-logs/` 和 active Change/Sprint 事实源。
- `pm-harness/` 新项目模板。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 初始化模板资产。
