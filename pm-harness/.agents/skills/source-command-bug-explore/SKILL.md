---
name: "source-command-bug-explore"
description: "缺陷探索 - 复现与影响分析，默认不写文档"
---

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 不要默认 `cat rules/*.md`、`cat AGENTS.md openspec/project.md rules/...` 或读取整目录；按本命令 Step 0 列表读取必要文件，已在同一会话读取过且无变更时用摘要承接。
- 检索先用 `rg -l` / `rg --files` 定位文件，再用 `sed -n '<start>,<end>p'` 或 `nl -ba ... | sed -n` 读取必要片段。
- 大范围 `rg` MUST 限制目录与输出：优先加 `--glob '!openspec/changes/archive/**' --glob '!**/node_modules/**' --glob '!**/.git/**'`；只有追溯历史归档时才放开 archive，并说明原因。
- 对 Harness / 模板工程 / agent 资产目录执行搜索时，默认排除 `pm-harness*/**`、`**/assets/**`、历史/外部 agent 目录（如 `.claude/**`、`.kiro/**`、`.opencode/**`）；除非当前任务明确要求分析这些目录。
- 命令输出优先控制在 `max_output_tokens <= 8000`；预期超出时先输出文件清单或命中计数，再分段读取。
- 不重复读取同一大文件集合；若需要再次确认，优先读取变更片段、`git diff -- <file>` 或具体 frontmatter/status 字段。

# source-command-bug-explore

Use this skill when the user asks to run the migrated source command `bug-explore`.

## Command Template

探讨：能否稳定复现、影响面、是否回归、关联 REQ/Change、hotfix vs 常规 fix。

**Input**：`BUG-xxxx`

**默认**：不写任何文件、不写代码、不改 `src/`

用户明确要求时可更新 `capture.md`；trace 可标 `exploring`。

## 禁止

- 写 `bug.md`、root-cause、OpenSpec
- 自动修复代码

## Next

`/bug-generate BUG-xxxx`
