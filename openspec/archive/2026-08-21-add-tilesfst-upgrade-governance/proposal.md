---
created_at: 2026-08-21 22:28:02
updated_at: 2026-08-21 22:28:02
---

# 应用 TilesFST 升级治理与文档卫生模式

## 背景

`/spec-study TilesFST` 已完成只读学习，并确认应用以下候选项：

- `upgrade-governance`
- 文档卫生
- 最小相关验证矩阵

这些内容涉及新增命令、治理扩展、目录边界和脚本校验行为变化，必须通过 active OpenSpec Change 承载，并纳入 Sprint scope。

## 目标

- 为 ProjectPmHarness 和新项目模板补齐版本部署升级与回滚计划治理。
- 新增 `/upgrade-plan` 与 `/upgrade-validate` 命令技能，生成和校验 `from_version -> to_version` 升级路径对象。
- 新增通用 `validate-release-upgrade.py` 脚本，避免把业务项目专属字段直接带入模板。
- 补齐长期文档表达卫生标准与轻量校验入口。
- 将命令执行顺序文档升级为包含最小相关验证矩阵的门禁说明。
- 生成本次 `/spec-study apply` 学习应用报告，并更新规范工程变更历史。

## 非目标

- 不修改学习对象 TilesFST。
- 不复制 TilesFST 的业务事实、运行时数据、源码或长脚本。
- 不修改 `src/` 业务代码。
- 不直接修改 `openspec/specs/` 正式规格。
- 不执行生产升级、真实 env 写入、数据库写入迁移、DB restore 或对象存储写入维护任务。
- 不恢复 `.claude`、`.codex`、`.cursor`、`.kiro`、`.opencode` 等多 Agent 入口。

## 影响范围

- 根项目治理规则、文档、脚本、Skill、OpenSpec Change 和 Sprint scope。
- `pm-harness/` 新项目模板。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 初始化模板资产。
- 不影响 API、数据库、Web、小程序、管理端、Orval 或业务运行时代码。

## 归档验证摘要

- OpenSpec CLI 已将 3 条 `project-governance` ADDED requirements 合并至正式 spec。
- 文档同步已在 `/spec-study apply` 阶段完成，并记录于 `docs/spec-logs/20260821223459-study-tilesfst-upgrade-governance.md`。
- 归档后执行目录结构、Workflow Sync、Issue promote 和 AI Usage Hook。
