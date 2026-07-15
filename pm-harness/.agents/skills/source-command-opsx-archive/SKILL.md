---
name: "source-command-opsx-archive"
description: "Archive a completed OpenSpec change"
---

# source-command-opsx-archive

Use when the user asks `/opsx-archive <change-id>` or wants to archive one OpenSpec change.

## Context Budget Guardrails（MUST）

- 归档复核优先 `openspec status`、`tasks.md` checkbox、delta spec heading 与 sync/promote 报告摘要；不得为归档全量读取 active/archived specs。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- Read focused artifacts only: `tasks.md`, delta spec headings, related trace/status snippets.
- Do not full-read `issues/**`, `iterations/**`, or all `openspec/specs/**`; use `rg -n "^### Requirement:|^### ADDED|^### MODIFIED|^### REMOVED"` then open the relevant sections.
- If a script fails, inspect the named files/snippets from the report instead of broad directory reads.
- Keep command output summarized; include full stdout only for validation reports or failures.

## Input

- `<change-id>` preferred.
- If omitted and not uniquely inferable, list active changes from `openspec list --json` and ask; never guess.

## Must Read / Run

```text
AGENTS.md
openspec/project.md
rules/document-governance.md
rules/directory-structure.md
rules/issues-lifecycle.md
.agents/skills/workflow-sync/SKILL.md
openspec/changes/<change-id>/tasks.md
openspec/changes/<change-id>/trace.md（存在时）
```

```bash
openspec status --change "<change-id>" --json
```

## Gates

| Gate | Default |
|---|---|
| Artifact status | incomplete => warn + require explicit user confirmation |
| Task status | `- [ ]` exists => warn + require explicit user confirmation |
| Delta spec | if `specs/` exists, assess ADDED/MODIFIED/REMOVED before moving |
| MODIFIED title | matching `openspec/specs/<capability>/spec.md` requirement title MUST exist |
| Archive target | `openspec/changes/archive/YYYY-MM-DD-<change-id>/` MUST NOT already exist |
| Archive evidence | if a historical archived Change lacks `trace.md`, it MUST contain a complete `## 归档验证摘要` fallback in proposal/design/tasks before Sprint close readiness can pass |

## Steps

1. Resolve change and verify active directory exists.
2. Count tasks and artifact status; stop on incomplete items unless user confirms.
3. Assess delta specs:
   - no delta specs => archive as metadata-only change;
   - delta exists => summarize capability, operation type, and affected Requirement titles;
   - prefer `openspec archive "<change-id>" -y` for sync + move.
4. If CLI is unavailable, manual fallback is allowed only after delta self-check:
   - merge delta into `openspec/specs/` according to OpenSpec semantics;
   - move to `openspec/changes/archive/YYYY-MM-DD-<change-id>/`.
5. Update related issue/change trace only through workflow sync/promote scripts where possible.

## Final Steps（MUST）

```bash
python scripts/sync-workflow-status.py --event opsx.archive --change <change-id> --sprint auto
python scripts/promote-issues-for-archive.py --change <change-id> --reason "/opsx-archive <change-id>"
```

- Both exit codes MUST be `0`.
- Print summary Workflow Sync Report and Promote Issue Stage report; use `--output detail` only for debugging.
- `promote-issues-for-archive.py` includes the issue subdocument status gate. If it reports `Issue Subdocument Status Gate` blockers, stop and reconcile the listed child Markdown `status` values before retrying; do not move REQ/BUG packages to `archive/` with residual `draft`、`pending_review`、`in_sprint`、`applied`、`todo`、`open` or equivalent non-closed states.
- Do not hand-edit `sprint.md` workflow-sync marker blocks.

## Output

Report change id, archive path, spec sync status, warnings/confirmations, scripts run, promoted issues, and next step.
