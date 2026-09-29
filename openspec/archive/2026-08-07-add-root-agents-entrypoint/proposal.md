---
created_at: 2026-08-07 15:23:44
updated_at: 2026-08-07 15:23:44
---

# add-root-agents-entrypoint

## 背景

ProjectPmHarness 根目录已经拥有自身的 `.agents/skills/`、`docs/`、`issues/`、`iterations/` 和 `openspec/`，但缺少根级 `AGENTS.md`。

现有 `pm-harness/AGENTS.md` 属于新项目脚手架模板，不应作为当前 ProjectPmHarness 自身的 AI 行为入口。

## 目标

新增根目录 `AGENTS.md`，明确当前脚手架工程自身的读取路由、目录边界、技能入口、模板同步规则和执行红线。

## 非目标

- 不修改业务源码。
- 不修改 `pm-harness/AGENTS.md` 模板入口。
- 不同步根目录运行态治理数据到 `pm-harness/` 或 init-skill 模板资产。

## 归档验证摘要

- 归档时间：2026-08-07 15:23:44。
- 归档类型：metadata-only governance Change，无 delta specs。
- 文档同步：根目录 `AGENTS.md`、`docs/spec-logs/20260807152344-governance-root-agents-entrypoint.md`、Sprint `sprint-001` 四件套已更新。
- 验证命令：模板同步、目录结构、Skill 包、Agent 上下文预算校验均通过。
- 业务影响：无 API、数据库、Web、小程序、管理端、Orval 或 Docker 影响。
