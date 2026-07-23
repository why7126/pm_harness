---
name: "release-prepare"
description: "执行发布前校验并生成或更新公开公告源文件"
---

# release-prepare

Use this skill when the user asks to run `/release-prepare <version>` or prepare a product release for publication.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 从 `releases/<version>/release.json` 开始，只读取发布对象中列出的 Sprint / REQ / BUG / Change。
- 门禁失败时按脚本报告定位具体文件片段；不要全量读取 `docs/**`、`issues/**`、`iterations/**` 或归档目录。
- 测试、Docker、客户端生成、公告预览输出只保留摘要；失败时展开关键错误。
- 测试失败时 MUST 分类为：`archived_path_residual`、`fixture_schema_drift`、`helper_payload_invalid`、`product_regression` 或 `environment_blocker`。

## Input

- `<version>`：必填，例如 `v0.1.0`。
- Flags：`--dry-run`、`--skip-tests`、`--skip-docker`、`--skip-announcement-preview`。

## Must Read

```text
AGENTS.md
rules/document-governance.md
rules/directory-structure.md
rules/release.md
rules/security.md
rules/testing.md
rules/agent-context-budget.md
releases/<version>/release.json
releases/templates/announcement.mdx
```

按发布对象范围分段读取：

```text
iterations/change|archive/<sprint-id>/sprint.yaml
iterations/change|archive/<sprint-id>/release-note.md
iterations/change|archive/<sprint-id>/acceptance-report.md
openspec/changes/archive/<date>-<change-id>/trace.md
issues/requirements/{archive,review,plan}/<REQ>/trace.md
issues/bugs/{archive,review,plan}/<BUG>/trace.md
```

## Gates

Prepare MUST verify and record evidence for each applicable gate in `release.json`:

| Gate | Evidence |
|---|---|
| `openspec_archive` | All formal Changes are archived and merged into `openspec/specs/`; unarchived formal scope blocks publish. |
| `tests` | Relevant test / smoke commands and pass summary. |
| `client_generation` | API changes have OpenAPI / generated client / docs sync evidence, or `na` rationale. |
| `docker_compose` | Deployment changes have Compose config/docs evidence, or `na` rationale. |
| `database_migration` | DB changes have schema/migration/docs/rollback evidence plus target database drift/smoke evidence, or `na` rationale. |
| `env_example` | Env changes have `.env.example` evidence, or `na` rationale. |
| `product_version` | User-visible version equals release version, or rationale is explicit. |
| `announcement_preview` | Static announcement build/preview or equivalent MDX safety check evidence. |

Do not write `status: pass` without concrete command/path/time evidence.

## Commands

Required structural and safety validation:

```bash
python scripts/validate-release.py --release-dir releases/<version>
```

Run additional checks according to release scope. Common examples:

```bash
python scripts/validate-openspec.sh
python scripts/run-tests.sh
python scripts/validate-api-standard.py
./scripts/generate-openapi-client.sh
docker compose config --quiet
```

Only run expensive or environment-dependent checks when they match release scope or the user requested full validation. If a command cannot run locally, record the blocker; do not invent evidence.

If `impact_scope.database` is not `none` / `na` / `不涉及`, `database_migration` MUST be `pass` and its evidence MUST mention migration or schema SQL, a schema drift / target database smoke check, and rollback or backup evidence. Do not paste raw database URLs or credentials into release artifacts.

## Artifacts（非 `--dry-run` MUST）

Create or update:

```text
releases/<version>/release.json
releases/<version>/announcement.mdx
```

Announcement MUST include version, release time, related Sprint, new features, bug fixes, release notes, known issues, upgrade steps, rollback instructions, and impact scope. It MUST be public-safe.

## Output

Report version, gate status summary, commands run, updated files, blockers, and whether publish is ready. If ready, next command:

```text
/release-publish <version>
```
