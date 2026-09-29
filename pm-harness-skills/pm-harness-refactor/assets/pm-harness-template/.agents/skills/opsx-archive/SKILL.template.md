---
name: "opsx-archive"
description: "Archive a completed OpenSpec change"
---

# opsx-archive

Use when the user asks `/opsx-archive <change-id>` or wants to archive one OpenSpec change.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- 归档复核优先 `openspec status`、`tasks.md` checkbox、delta spec heading 与 sync/promote 报告摘要；不得为归档全量读取 active/archived specs。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
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
| Documentation sync | before archive, affected long-lived docs / README / `.env.example` / API index / DB design / Orval notes / release or deployment docs MUST be checked and updated or explicitly marked not applicable |
| Archive target | `openspec/archive/YYYY-MM-DD-<change-id>/` MUST NOT already exist |
| Legacy archive root | `openspec/changes/archive/` MUST NOT exist before or after archive; if present, stop and migrate its children to `openspec/archive/` first |
| Archive evidence | if a historical archived Change lacks `trace.md`, it MUST contain a complete `## 归档验证摘要` fallback in proposal/design/tasks before Sprint close readiness can pass |

## Steps

1. Resolve change and verify active directory exists.
   - Also verify `openspec/changes/archive/` does not exist as a real directory. Compatibility references in scripts/tests are allowed; the filesystem path is not.
2. Count tasks and artifact status; stop on incomplete items unless user confirms.
3. Assess delta specs:
   - no delta specs => archive as metadata-only change;
   - delta exists => summarize capability, operation type, and affected Requirement titles;
   - prefer `scripts/archive-change.sh "<change-id>"` so OpenSpec CLI output is normalized to canonical `openspec/archive/` and legacy `openspec/changes/archive/` is migrated/blocked.
4. Before moving or merging the Change, complete documentation sync:
   - inspect `tasks.md`, `trace.md`, delta spec headings, and implementation notes to identify affected docs;
   - update required long-lived docs according to `rules/document-governance.md` and task-specific rules, including `docs/03-api-index.md` / Orval notes for API changes, `docs/04-database-design.md` for DB changes, deployment / release docs and `.env.example` for environment or Docker changes, and README or compatibility docs when affected;
   - if no documentation update is required, record the reason in the archive output; do not silently skip this gate.
5. If the wrapper fails because OpenSpec CLI is unavailable, manual fallback is allowed only after delta self-check:
   - merge delta into `openspec/specs/` according to OpenSpec semantics;
   - move to `openspec/archive/YYYY-MM-DD-<change-id>/`.
6. Update related issue/change trace only through workflow sync/promote scripts where possible.

## Final Steps（MUST）

Run these commands strictly sequentially. Do not use parallel execution or `multi_tool_use.parallel` for directory validation, Workflow Sync and issue promotion: each step depends on the files written by the previous step, and issue promotion depends on the files written by Workflow Sync.

```bash
python scripts/validate-directory-structure.py
python scripts/sync-workflow-status.py --event opsx.archive --change <change-id> --sprint auto
python scripts/promote-issues-for-archive.py --change <change-id> --reason "/opsx-archive <change-id>"
```

- All exit codes MUST be `0`.
- Directory validation MUST fail if `openspec/changes/archive/` exists. Do not continue by treating it as a historical archive location; migrate to `openspec/archive/` first.
- Print summary Workflow Sync Report and Promote Issue Stage report; use `--output detail` only for debugging.
- `promote-issues-for-archive.py` includes the issue subdocument status gate. If it reports `Issue Subdocument Status Gate` blockers, stop and reconcile the listed child Markdown `status` values before retrying; do not move REQ/BUG packages to `archive/` with residual `draft`、`pending_review`、`in_sprint`、`applied`、`todo`、`open` or equivalent non-closed states.
- Single REQ/BUG promote after `/opsx-archive <change-id>` MUST NOT be blocked solely because the containing Sprint is still planning/in_progress. Sprint completion remains a `/sprint-archive` gate, not a single Issue archive gate.
- Do not hand-edit `sprint.md` workflow-sync marker blocks.

## Final Step — AI Usage Post-command Hook (MUST)

After Workflow Sync and issue promotion exit with code `0`, run:

```bash
python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.archive --change <change-id> --sprint <resolved-sprint-id> [--req <linked-REQ-id>] [--bug <linked-BUG-id>] --json
```

- If the archived change has `source_requirement` / `source_bug` or an issue trace link, pass the linked REQ/BUG explicitly. The extractor must also enrich `opsx.archive` from active or archived change trace/proposal and issue traces before writing usage facts.
- Print only the compact hook summary: `status`, `usage_mode`, `command_run_count`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
- Use the Sprint resolved by Workflow Sync; do not pass the literal value `auto` to `extract-ai-usage.py`.
- If local session input is unavailable, report `usage_mode: unavailable` and the recommended action; do not treat that as parent command failure.

## Output

Report change id, archive path, documentation sync status, spec sync status, warnings/confirmations, scripts run, promoted issues, and next step.
