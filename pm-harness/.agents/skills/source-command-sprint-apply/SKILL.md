---
name: "source-command-sprint-apply"
description: "按 Sprint 依赖与优先级编排 OpenSpec Change 开发"
---

# source-command-sprint-apply

Use this skill when the user asks to run `/sprint-apply <sprint-id>`.

## Context Budget Guardrails（MUST）

- Sprint apply 必须逐 Change 聚焦读取，不得把整个 Sprint 历史、全部 issue 包或全部 active changes 同时装入上下文。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 先读 `sprint.yaml` 与必要 trace/status 片段，不全量读取 Sprint 四件套。
- 每个 Change 只读 `proposal.md`、`tasks.md`、依赖字段和必要 design/spec 片段。
- UI gate 只读取命中标签的 best-practices。
- Queue report 输出摘要；大 diff/test 输出分段读取。

## Input

- `<sprint-id>` required unless only one active Sprint exists.
- Flags: `--dry-run`、`--parallel`、`--force-req-check`、`--skip-cross-cutting-gate`（仅 P0 热修）。

## Must Read

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/testing.md
rules/requirement-management.md
rules/bug-management.md
rules/iterations-lifecycle.md
rules/directory-structure.md
.agents/skills/workflow-sync/SKILL.md
iterations/change|archive/<sprint>/sprint.yaml
```

Focused snippets as needed:

```text
iterations/<stage>/<sprint>/sprint.md §目标/Scope/依赖/横切预防清单
issues/requirements|bugs/<stage>/<id>/trace.md
openspec/changes/<change>/proposal.md + tasks.md + trace.md
```

## Gates

### Review Gate（MUST）

All Sprint REQ/BUG in formal scope MUST be `approved` or `in_sprint`. If not, stop and report remediation; do not apply related changes.

### Change Status Gate

| Status | Action |
|---|---|
| archived | skip |
| all tasks complete | skip or suggest archive |
| blocked / missing artifacts | pause |
| active with pending tasks | eligible |

### Cross-cutting Gate

Before editing `src/`, run the same gate as `.agents/skills/source-command-opsx-apply/SKILL.md` for each APPLY NEXT change.

## Queue Algorithm

1. Resolve Sprint directory via lifecycle rules.
2. Load `requirements[]`、`bugs[]`、`changes[]` from `sprint.yaml`.
3. Map each Change to related REQ/BUG and priority.
4. Build dependencies from proposal/design/tasks/trace and Sprint dependency section.
5. Sort: P0 BUG > P0 REQ > P1 > P2; prerequisites before dependents.
6. Output Sprint Queue Report before changing files.

Queue Report MUST include:

```text
Sprint / status / lifecycle_stage
Eligible changes
Skipped changes + reason
Blocked changes + reason
Topological order
Next APPLY target
```

`--dry-run` stops after Queue Report.

## Execution Loop

For each eligible Change:

1. Announce APPLY target.
2. Execute `/opsx-apply` equivalent using `.agents/skills/source-command-opsx-apply/SKILL.md`.
3. Run focused tests/checks.
4. Update tasks and trace.
5. Continue until queue exhausted, blocked, or user interrupts.

Do not archive automatically unless user explicitly asks for sprint/archive flow.

## Output

Report completed changes, skipped/blocked items, tests/checks, Sprint progress, and next suggested command.

## Final Step — Workflow Sync（MUST）

Run:

```bash
python scripts/sync-workflow-status.py --event sprint.apply --sprint <sprint-id>
```

- Exit code MUST be `0`。
- Print summary Workflow Sync Report；use `--output detail` only for debugging。
- Do not hand-edit workflow-sync marker blocks。
