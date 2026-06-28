---
name: workflow-sync
description: Synchronize workflow status after req, bug, sprint, and opsx commands. Use as the final step of every governance command that changes issues, iterations, or OpenSpec changes.
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
---

# Workflow Sync

Run this skill after any `req-*`, `bug-*`, `sprint-*`, or `opsx-*` command changes workflow state.

## Required Inputs

- `event`: command event name, for example `req.capture`, `bug.opsx`, `opsx.archive`, or `sprint.apply`.
- Entity ids changed by the command:
  - `--req REQ-xxxx`
  - `--bug BUG-xxxx`
  - `--change change-id`
  - `--sprint sprint-xxx` or `--sprint auto`

## Steps

1. Run `python scripts/sync-workflow-status.py --event <event> ...`.
2. If the command changed a sprint, pass `--sprint <id>`; if only one sprint is `in_progress`, `--sprint auto` is allowed.
3. For `opsx.archive`, run `python scripts/promote-issue-stage.py --to archive --change <change-id> --reason "opsx.archive"` after workflow sync.
4. For `sprint.archive`, run `python scripts/promote-issue-stage.py --to archive --sprint <sprint-id> --reason "sprint.archive"` after workflow sync.
5. If any script exits non-zero, read the report, fix the source documents or rerun without `--check`, then run the failed step again.
6. End the command output with the script reports, including `## Issue Stage Promotion` for archive events.

## Guardrails

- Do not finish a workflow command without running this sync step.
- Do not finish `opsx.archive` or `sprint.archive` without running issue stage promotion.
- Do not manually edit machine-maintained `workflow-sync` marker blocks except to add missing markers.
- `--check` failures mean the workflow command is incomplete until drift is resolved.
- If a document has no marker block yet, keep the script report in the final output so the missing automation boundary is visible.
- If issue promotion reports Blocked because linked changes are not all archived, leave the issue in `review/` and report the blocker.
