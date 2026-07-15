---
name: "source-command-req-review"
description: "需求评审 - 状态变更；仅 approved 可进 Sprint 与 req-opsx"
---

# source-command-req-review

Use this skill when the user asks to run the migrated source command `req-review`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

**Input**：`REQ-xxxx`

Flags：`--approve` | `--reject` | `--defer`（无 flag 时输出评审检查清单并 AskUserQuestion）

**Output**：`review.md`；`trace.md` + `requirement.md` → `status: approved|rejected|deferred`

---

## Step 1 — 前置检查

- `status` 应为 `pending_review`（或 `enriching` 且 Readiness ≥ Partially Ready）
- 读 requirement、acceptance、trace；UI 类读 prototype

## Step 2 — 评审清单

- [ ] 范围清晰，Out of Scope 明确
- [ ] 验收标准可测试
- [ ] 优先级与依赖合理
- [ ] UI 类：原型或实现策略已决
- [ ] 无与现有 REQ 重复未说明

## Step 3 — 写 review.md

```markdown
---
review_id: REV-REQ-xxxx-001
date: YYYY-MM-DD
participants: []
result: approved | rejected | deferred
---

## 评审结论
…

## 条件通过项
- [ ] …
```

## Step 4 — 更新 status

| result | status |
|--------|--------|
| approve | `approved` |
| reject | `rejected` |
| defer | `deferred` |

填写 `lifecycle.reviewed`、`lifecycle.approved`（若 approve）

## Step 5 — 目录迁移（MUST，`--approve` 时）

Read `rules/issues-lifecycle.md`。

| Flag | 迁移 |
|------|------|
| `--approve` | `plan/` → `review/` |
| `--reject` / `--defer` | **跳过**（保留 `plan/`） |

`--approve` 时 **MUST** 在 Workflow Sync **之前**运行：

```bash
python scripts/promote-issue-stage.py --req <REQ-id> --to review --reason "/req-review --approve"
```

- Exit code **MUST** be `0`（已在 `review/` 时可 no-op）。
- 打印脚本 stdout（迁移路径、引用更新计数）。
- `--dry-run` 仅用于预检，不得作为命令结束状态。

## 门禁

**仅 `approved`** 可执行 `/req-opsx`、`/sprint-propose` 纳入。

## Next

`/req-opsx REQ-xxxx` → `/sprint-propose`（可选）

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event req.review --req <REQ-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- Print the summary **Workflow Sync Report** to the user; use `--output detail` only for debugging.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).
