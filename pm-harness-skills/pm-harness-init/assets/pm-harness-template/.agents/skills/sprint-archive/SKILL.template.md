---
name: "sprint-archive"
description: "批量归档 Sprint 内 OpenSpec Change 并关闭迭代"
---

# sprint-archive

Use when the user asks `/sprint-archive <sprint-id>` or wants to close a Sprint.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- Start from `sprint.yaml`; do not full-read Sprint four-piece unless closing fields are needed.
- For each Change, read only `tasks.md`, trace/status, and delta headings.
- Reuse `.agents/skills/opsx-archive/SKILL.md`; do not duplicate full archive reasoning.
- `--dry-run` must stop after queue/readiness report.

## Product Data Observability Gate（MUST）

关闭 Sprint 前，若纳入项涉及 API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装、App 请求封装或工作流治理，MUST 读取 `docs/standards/product-data-collection-observability.md`，并确认归档证据含 `product_data_collection_observability`、`affected_layers`、`reason` 和 `validation`；不适用项 MUST 有 N/A 或 `not_applicable` 原因。

## Input

- `<sprint-id>` preferred; if omitted, infer only when one active Sprint exists.
- Flags: `--dry-run`、`--change <change-id>`、`--force`、`--skip-sync`（不推荐）、`--no-sprint-close`。

## Must Read / Run

```text
AGENTS.md
rules/document-governance.md
rules/directory-structure.md
rules/iterations-lifecycle.md
.agents/skills/opsx-archive/SKILL.md
.agents/skills/workflow-sync/SKILL.md
iterations/change/<sprint-id>/sprint.yaml
iterations/change/<sprint-id>/sprint.md（依赖/Scope 片段）
```

```bash
openspec list --json
python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id>
python scripts/generate-sprint-fact-sheet.py --sprint <sprint-id> --json
```

`validate-sprint-archive-readiness.py` includes the Sprint close stale scan. It MUST fail when Sprint four-piece docs or scoped REQ/BUG top-level Markdown files still contain stale intermediate wording such as "待 `/req-opsx`", "待 `/bug-opsx`", "待 `/opsx-apply`", stale `proposed` / `applied` semantics for archived Changes, unresolved `待验收` / `待实现`, active Change paths for archived Changes, or canonical `openspec/changes/archive/` links. For focused diagnosis, run:

```bash
python scripts/check-sprint-close-stale-scan.py --sprint <sprint-id>
```

Do not hand-edit `sprint.md` workflow-sync marker blocks while fixing stale scan blockers; rerun Workflow Sync or edit only non-derived human-authored notes.

Ignored local real env files do not participate in Sprint archive readiness. Do not ask the operator to delete `.env` / local deploy env files before `/sprint-archive`; block only if real env content is staged, committed, pasted into docs, or referenced as archive evidence.

For a Sprint with 10+ Change ids in `sprint.yaml`, first inspect the machine-readable `change_batches` from readiness / Fact Sheet JSON. Use batch summary counts, blockers, warnings and evidence hints to decide which raw `tasks.md` or `trace.md` snippets need detail. Successful output MUST stay compact: report total changes, batch count, archived/skipped/blocked counts, warning count and recommended next read; do not print full batch JSON or every raw tasks/trace detail.

For single change mode:

```bash
python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id> --change <change-id>
```

Readiness distinguishes active and archived Change semantics: active Changes are checked for directory/tasks completion; archived Changes are additionally rechecked for `trace.md`. If an archived Change lacks `trace.md`, `proposal.md`、`design.md` or `tasks.md` MUST contain a complete `## 归档验证摘要` covering validation command/result, acceptance verdict, Issue/Sprint status, and archive path/time evidence. This is a Sprint-level secondary gate; new single Change archives are expected to catch the same evidence gap during `/opsx-archive`.

Before any issue package is moved to `issues/**/archive/`, the promote step MUST pass the issue subdocument status gate:

```bash
python scripts/promote-issues-for-archive.py --sprint <sprint-id>
```

If scoped REQ/BUG child Markdown files still contain non-closed frontmatter or fenced YAML `status` values such as `draft`、`pending_review`、`in_sprint`、`applied`、`todo`、`open`, keep the Sprint close blocked until those documents are reconciled.

If readiness returns non-zero or `Verdict: BLOCKED`, stop unless user explicitly passed `--force` and confirms each blocker.

## Queue Rules

1. Only archive Change ids listed in `sprint.yaml`.
2. Skip already archived changes and record path.
3. Block by default when tasks/artifacts are incomplete, `tasks.md` is missing, change dir is missing, or MODIFIED title cannot be matched.
4. Sort dependencies as in sprint apply: base `add-*` before dependent `fix-*` / `update-*`; unrelated changes keep `sprint.yaml` order.
5. Output Sprint Archive Queue Report before moving anything.

Queue Report MUST include Sprint, mode, readiness verdict, each change action (`SKIP` / `ARCHIVE NEXT` / `QUEUE` / `BLOCKED`), blockers, and warnings.

## AI Usage Snapshot Gate（MUST before Close Sprint）

Before the final close step, check the Sprint AI usage snapshot through the Fact Sheet:

```bash
python scripts/generate-sprint-fact-sheet.py --sprint <sprint-id> --json
```

Inspect `ai_usage_snapshot.snapshot_status`、`ai_usage_snapshot.ai_usage_mode`、`generated_at`、`coverage`、`warnings` and `recommended_action`.

- If `snapshot_status: present` and `ai_usage_mode: actual`, output only a compact summary: status, mode, path, generated_at, coverage status and warning_count.
- If snapshot is `missing`、`stale` or `failed`, first try the AI Usage default session discovery chain. Use explicit session input only when automatic discovery cannot find a suitable local session or when doing historical backfill:

```bash
python scripts/extract-ai-usage.py --post-command-hook --workflow-event sprint.archive --sprint <sprint-id> --json
```

- If automatic discovery, explicit local session input or generation fails, continue only with an explicit warning in the close report: `ai_usage_mode: estimated_fallback`, reason, impact, and recommended_action. Do not state that real token usage was used.
- Do not print raw session JSONL, prompts, system/developer instructions, local absolute paths, tool output bodies, or full snapshot contents.

## Archive Loop

For each `ARCHIVE NEXT`:

1. Execute `/opsx-archive` equivalent using `.agents/skills/opsx-archive/SKILL.md`.
2. Prefer `openspec archive "<change-id>" -y`; use manual fallback only with delta self-check.
3. Stop the whole Sprint archive on title mismatch, archive target conflict, failed sync/promote script, or user interruption.

## Close Sprint

Unless `--no-sprint-close`, close only when all Sprint changes are archived and readiness passes without `--force`:

```bash
python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id>
```

Then update the four-piece as needed:

```text
sprint.yaml: status completed, lifecycle_stage archive
acceptance-report.md: final verdict/date/check summary
release-note.md: draft -> published if applicable
sprint.md: closure note only outside workflow-sync marker blocks
```

Move directory with `git mv iterations/change/<sprint-id> iterations/archive/<sprint-id>`.

## Archived Path Residual Gate（MUST after Close Sprint）

After the Sprint directory has moved to `iterations/archive/<sprint-id>/` and Workflow Sync / issue promotion have succeeded, run:

```bash
python scripts/check-archived-path-residuals.py --sprint <sprint-id>
python scripts/check-sprint-close-stale-scan.py --sprint <sprint-id>
```

- Exit code `0` means no stale `iterations/change/<sprint-id>/` or active `openspec/changes/<change-id>/` references were found in this Sprint scope.
- Exit code `1` MUST block a silent success close-out. Report the file, line, old path, suggested path, and exact retry command from the residual report.
- The check scope MUST come from `sprint.yaml` requirements / bugs / changes and Sprint four-piece documents; do not broad-scan all `issues/**`, `openspec/archive/**`, or legacy `openspec/changes/archive/**`.
- The stale scan MUST also pass before close-out; report blocker severity, kind, target, file, line and retry command when it fails.
- Do not hand-edit workflow-sync marker blocks while fixing residual links.

## Final Step — Workflow Sync（MUST）

```bash
python scripts/sync-workflow-status.py --event sprint.archive --sprint <sprint-id>
```

Exit code MUST be `0`; print summary Workflow Sync Report; use `--output detail` only for debugging.

## Output

Report archived/skipped/blocked counts, Sprint close status, updated files, validation commands, archived path residual check summary, and exact retry command if paused.
