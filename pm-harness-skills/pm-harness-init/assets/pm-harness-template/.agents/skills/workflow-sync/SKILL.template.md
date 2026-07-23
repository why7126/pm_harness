---
name: workflow-sync
description: Sync REQ/BUG/Sprint/OpenSpec workflow status after req/bug/sprint/opsx commands
---

# workflow-sync

After any workflow command that changes REQ, BUG, Change, or Sprint scope/status, **MUST** run workflow sync.

## Command

```bash
python scripts/sync-workflow-status.py \
  --event <event> \
  [--sprint auto|sprint-xxx] \
  [--change <change-id>] \
  [--req <REQ-id>] \
  [--bug <BUG-id>]
```

## AI Usage Post-command Hook（MUST after successful workflow sync）

After a `/req-*`, `/bug-*`, `/opsx-*`, or `/sprint-*` workflow command finishes its main work and the Workflow Sync command above exits with code `0`, run the unified AI usage hook or report why it is skipped:

```bash
python scripts/extract-ai-usage.py \
  --post-command-hook \
  --workflow-event <event> \
  [--req <REQ-id>] \
  [--bug <BUG-id>] \
  [--change <change-id>] \
  [--sprint <sprint-id>] \
  [--session-jsonl <local-session.jsonl>] \
  --json
```

Rules:

1. The hook is best-effort for normal workflow commands. If session input is unavailable, print the short `usage_mode: unavailable` summary and recommended action; do not fail the parent command.
2. If the command has no Sprint scope, command-run generation may proceed, but Sprint snapshot output MUST be `skipped`; do not invent a Sprint.
3. Successful output MUST stay compact: `status`, `usage_mode`, `command_run_count`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
4. The hook MUST NOT persist prompt text, system/developer instructions, skill bodies, raw session JSONL, local absolute paths, tool output bodies, secrets, cookies, Authorization headers, or `.env` content.
5. Exploration commands with no workflow state change MAY run the hook in `--dry-run` mode or output the same recommended action; they MUST NOT modify REQ/BUG/Change/Sprint status just to create usage data.

Session input discovery:

- Prefer explicit `--session-jsonl <local-session.jsonl>` when available.
- Otherwise the hook checks `AI_USAGE_SESSION_JSONL`, then `CODEX_SESSION_JSONL`.
- Raw session files remain local-only and MUST NOT be copied into the repository.

| Flag | Purpose |
|------|---------|
| `--sprint auto` | Resolve sprint by context (see below) |
| `--sprint none` | Skip sprint-level artifacts; sync issue/trace/registry only |
| `--check` | Fail if derived docs drift (CI) |
| `--dry-run` | Report only, no writes |
| `--output summary\|detail` | Report verbosity; default `summary` hides no-delta file lists, `detail` prints every result |

### Sprint resolution (`--sprint auto`)

| Event kind | Resolution |
|------------|------------|
| `req.*` / `bug.*` with `--req` / `--bug` | Sync sprint **only if** that issue is listed in `iterations/<sprint>/sprint.yaml` `requirements` or `bugs`; otherwise skip sprint artifacts and report `_skipped — BUG-xxxx not in sprint scope_` |
| `opsx.*` with `--change` | Sync sprint **only if** that change is in sprint `changes` |
| `sprint.*` | Use explicit sprint or the single `in_progress` sprint |
| No issue/change focus | Fall back to single `in_progress` sprint (legacy default) |

When sprint sync is skipped, the script still updates the target issue `trace.md`, `_registry.yaml`, and parent requirement related-bug index when applicable.

For `opsx.apply`, sprint sync skipped/unresolved is a **blocking precondition failure** for REQ/BUG-sourced changes. The parent command MUST stop before implementation and ask to run `/sprint-propose` first, unless the Change is explicitly documented as a non-REQ/BUG pure technical governance Change.

### Issue subdocument residual status reconcile

When issue archive promotion is blocked by residual `status` fields in issue subdocuments, do not hand-edit files in bulk. Use workflow sync reconcile mode:

```bash
python scripts/sync-workflow-status.py \
  --event req.archive \
  --req REQ-xxxx-slug \
  --sprint auto \
  --reconcile-issue-status-residuals \
  --dry-run
```

```bash
python scripts/sync-workflow-status.py \
  --event req.archive \
  --req REQ-xxxx-slug \
  --sprint auto \
  --reconcile-issue-status-residuals \
  --apply-reconcile
```

Use `--bug BUG-xxxx-slug` and `--event bug.archive` for BUGs.

Guardrails:

1. Always run dry-run first and inspect file path, source, old status, target status, and `updated_at`.
2. Reconcile is only for already-closed issues. If the report says the issue trace, linked Change, or linked Sprint is not closed, run the upstream workflow command first.
3. Reconcile MUST NOT be used to bypass review, acceptance, `/opsx-archive`, or `/sprint-archive`.
4. Successful reconcile refreshes modified Markdown `updated_at` and reports changed file/field counts.

## Event mapping

| Command family | `--event` |
|----------------|-----------|
| capture | `req.capture` 与/或 `bug.capture`（按本次创建的条目分别执行） |
| req-capture | `req.capture` |
| req-generate | `req.generate` |
| req-complete | `req.complete` |
| req-review | `req.review` |
| req-opsx | `req.opsx` |
| bug-capture | `bug.capture` |
| bug-generate | `bug.generate` |
| bug-complete | `bug.complete` |
| bug-review | `bug.review` |
| bug-opsx | `bug.opsx` |
| opsx-propose | `opsx.propose` |
| opsx-apply | `opsx.apply` |
| opsx-archive | `opsx.archive` |
| sprint-propose | `sprint.propose` |
| sprint-apply | `sprint.apply` |
| sprint-archive | `sprint.archive` |

## Guardrails

1. Print the **Workflow Sync Report** from script stdout. Successful commands SHOULD use the default summary output; rerun with `--output detail` only when diagnosing drift, skipped files, or failures.
2. If exit code != 0, fix drift and re-run before ending the parent command.
3. Do **not** hand-edit `sprint.md` Scope marker blocks; use the script.
4. Marker blocks: `<!-- workflow-sync:scope-*:start/end -->`.
5. Scope 表 archived 时间与 §里程碑「目标日期」MUST 为 `YYYY-MM-DD HH:mm:ss` 且时分秒 MUST 非 `00:00:00`（见 `rules/document-governance.md` §6.1）。
6. §Sprint 目标 不在 sync 范围；纳入 REQ/BUG 时 MUST 同步更新 **编号列表** 与 **`### xxx 要点`** 两处。
7. Issue `trace.md` 的 `## 变更记录` MUST 保持表头紧跟章节标题；若历史记录行出现在表头前，脚本 SHOULD 自动归一化并在报告中体现 delta。
8. `/opsx-apply` 前 MUST confirm linked REQ/BUG is in a `sprint-xxx`; `--sprint auto` unresolved means do not run apply.

## Refreshed artifacts

- `iterations/<sprint>/sprint.md` Scope tables + note；§里程碑「目标日期」列 legacy 仅日期 → `YYYY-MM-DD HH:mm:ss`
- `iterations/<sprint>/acceptance-report.md` issue status lines + note
- `iterations/<sprint>/release-note.md` publish status
- `issues/requirements|bugs/*/trace.md` status + iteration + `openspec_changes[].status`（Frontmatter 与 fenced `yaml` 块均需同步）+ `## 变更记录` workflow event 行 / 表格格式归一化
- parent requirement `trace.md` related bug index
- `issues/requirements/_registry.yaml` / `issues/bugs/_registry.yaml`
- 写入时自动维护 Frontmatter `created_at` / `updated_at`（`rules/document-governance.md` §2.4）
