---
name: "release-propose"
description: "创建或更新产品版本发布计划"
---

# release-propose

Use this skill when the user asks to run `/release-propose <version>` or create/update a product release plan.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 先从候选 Sprint 的 `sprint.yaml`、`release-note.md` 摘要和 Change/Issue 状态定位发布范围，不得全量读取所有 `iterations/**`、`issues/**` 或 `openspec/changes/archive/**`。
- 搜索历史归档时只按候选 Sprint / Change ID 精确定位。
- 命令输出优先摘要：版本、范围、门禁缺口、生成/更新文件、下一步。

## Input

- `<version>`：必填，SemVer 风格，如 `v0.1.0`。
- Flags：`--sprint <sprint-id>`、`--req <REQ-id>`、`--bug <BUG-id>`、`--change <change-id>`、`--dry-run`。

## Must Read

```text
AGENTS.md
openspec/project.md
rules/document-governance.md
rules/directory-structure.md
rules/release.md
rules/security.md
rules/agent-context-budget.md
releases/README.md
releases/templates/release.json
```

按候选范围分段读取：

```text
iterations/change|archive/<sprint-id>/sprint.yaml
iterations/change|archive/<sprint-id>/release-note.md
iterations/change|archive/<sprint-id>/acceptance-report.md
issues/requirements/{plan,review,archive}/<REQ>/trace.md
issues/bugs/{plan,review,archive}/<BUG>/trace.md
openspec/changes/<change-id>/trace.md 或 openspec/changes/archive/<date>-<change-id>/trace.md
```

## Gates

| Gate | Rule |
|---|---|
| Version | `<version>` MUST match `vX.Y.Z` or SemVer-like pre-release form. |
| Scope | Release scope MUST come from Sprint / REQ / BUG / Change traceable artifacts. |
| Formal scope | `formal_scope_only` MUST be `true`; unreviewed or non-delivered items MUST NOT enter formal scope. |
| Change | Formal Changes SHOULD be archived before publish; unarchived Changes are allowed in propose only as prepare/publish blockers. |
| Public safety | Do not include secrets, real customer data, internal DB URLs, object storage credentials, tokens, or non-public ops details. |
| Product version | If the project has a user-visible version source and it differs from `<version>`, set `version_change_rationale` or list the mismatch as a blocker. |

## Artifacts（非 `--dry-run` MUST）

Create or update:

```text
releases/<version>/release.json
```

Use `releases/templates/release.json` as the base shape. The release object MUST include:

- `version`
- `release_time` in `YYYY-MM-DD HH:mm:ss`
- `owner`
- `formal_scope_only: true`
- `sprints`
- `requirements`
- `bugs`
- `changes`
- `gates`
- `known_issues`
- `upgrade_steps`
- `rollback`
- `impact_scope`
- `announcement`

For propose, unknown gates MAY remain `na` with clear `rationale`. Do not mark a gate `pass` without concrete evidence.

## Validation

Run after writing:

```bash
python scripts/validate-release.py --release-dir releases/<version>
```

If validation fails because publish-time evidence is still missing, report the gaps clearly and keep the release as a draft plan. Structural errors, invalid JSON, missing required keys, or public-safety failures MUST be fixed before ending.

## Output

Report version, selected Sprint / REQ / BUG / Change counts, created/updated path, current gate gaps, validation result, and next command:

```text
/release-prepare <version>
```
