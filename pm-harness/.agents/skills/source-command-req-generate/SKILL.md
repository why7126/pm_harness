---
name: "source-command-req-generate"
description: "需求生成 - 仅生成 requirement.md（PRD）"
---

# source-command-req-generate

Use this skill when the user asks to run the migrated source command `req-generate`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

**Input**：`REQ-xxxx`（须存在 `capture.md`）

**Output**：**仅** `requirement.md`；`trace.md` → `status: draft`，`lifecycle.generated`

**禁止**：user-stories、acceptance、prototype、openspec、src

---

## Steps

1. 读 `capture.md`、探索对话上下文、`rules/requirement-management.md`
2. 读 1–2 个同类 REQ 作结构参考（如 `REQ-0005-user-management-list-refine/requirement.md`）
3. 写 `requirement.md` frontmatter：

```yaml
---
requirement_id: REQ-xxxx
title:
terminal: web-admin | web-catalog | miniapp | multi
version: v1
status: draft
owner: product
source: capture.md
priority: P1
parent_requirement:
---
```

4. 正文含：背景、目标用户、范围（含/不含）、功能要求（FR-xxx）、UI 约束、关联需求、状态块
5. 同步 `requirement.md` 与 `trace.md` 的 `status: draft`
6. 追加 trace 变更记录

## Next

`/req-complete REQ-xxxx`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event req.generate --req <REQ-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- Print the summary **Workflow Sync Report** to the user; use `--output detail` only for debugging.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).
