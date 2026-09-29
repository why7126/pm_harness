---
name: "release-prepare"
description: "执行发布前校验并生成或更新公开公告源文件"
---

# release-prepare

Use this skill when the user asks `/release-prepare <version>` or wants to run pre-release checks and generate/update the public announcement.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 从 `releases/<version>/release.json` 开始，只读取发布对象中列出的 Sprint / REQ / BUG / Change。
- 门禁失败时按脚本报告定位具体文件片段；不要全量读取 `docs/**`、`issues/**`、`iterations/**` 或归档目录。
- 测试、Docker、Orval、Mintlify 输出只保留摘要；失败时展开关键错误。
- 测试失败时 MUST 先做失败分类并写入输出或 release blockers：`archived_path_residual`（active Change 路径在归档后失效）、`fixture_schema_drift`（测试 fixture / snapshot 字段落后于契约）、`helper_payload_invalid`（共享 helper 仍提交废弃字段或非法 payload）、`product_regression`（真实产品行为回归）、`environment_blocker`（本地依赖、网络、权限或真实环境不可用）。
- 若失败属于前三类治理漂移，MUST 建议同步测试 helper、归档路径 resolver 或 fixture 契约；不得只要求人工复跑。

## Input

- `<version>`：必填，例如 `v0.1.0`。
- Flags：`--dry-run`、`--skip-tests`（不推荐）、`--skip-docker`（不推荐）、`--skip-mintlify`（不推荐）。

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
src/shared/product-version.ts（如存在）
```

按发布对象范围分段读取：

```text
iterations/change|archive/<sprint-id>/sprint.yaml
iterations/change|archive/<sprint-id>/release-note.md
iterations/change|archive/<sprint-id>/acceptance-report.md
openspec/archive/<date>-<change-id>/trace.md 或归档验证摘要
issues/requirements/{archive,review,plan}/<REQ>/trace.md
issues/bugs/{archive,review,plan}/<BUG>/trace.md
```

## Gates

Prepare MUST verify and record evidence for each applicable gate in `release.json`:

| Gate | Evidence |
|---|---|
| `openspec_archive` | All formal Changes are archived and merged into `openspec/specs/`; unarchived formal scope blocks publish. |
| `tests` | Relevant pytest / Vitest / smoke commands and pass summary. |
| `orval` | API changes have OpenAPI / Orval / docs sync evidence, or `na` rationale. |
| `docker_compose` | Deployment changes have Compose config/docs evidence, or `na` rationale. |
| `database_migration` | DB changes have schema/migration/docs/rollback evidence plus MySQL schema drift or target MySQL smoke evidence, or `na` rationale. |
| `env_example` | Env changes have `.env.example` evidence, or `na` rationale. |
| `product_version` | `PRODUCT_VERSION` equals release version, or rationale is explicit. |
| `mintlify_preview` | Mintlify build/preview or equivalent static MDX safety check evidence. |
| `image_prepare` | When `image_required=true`, `releases/<version>/image-build-plan.json` exists, validates, and is referenced by release metadata. |
| `image_build` | In prepare, record `na` with a blocker / next step when `releases/<version>/image-manifest.json` is not yet generated; publish is the stage that requires manifest or approved external build evidence. |

Do not write `status: pass` without concrete command/path/time evidence.

Local real env files may exist during release preparation and are not release blockers by themselves when they remain ignored and uncommitted. Release evidence MUST reference only `.env.example` / `*.env.example`, validation commands, variable names, and redacted summaries; never paste raw env values or require deletion of local real env files before archive/publish.

When release scope includes backend runtime, Web build output, Dockerfile, Compose, build env, image build scripts, database schema / migration, API / Orval generated client, or offline image delivery:

- Set or keep `image_required=true` in `release.json`.
- Require `/image-prepare <version>` evidence before marking prepare complete.
- Point to `/image-build <version>` when a built image or offline tarball must be delivered.
- Do not execute the heavy image build from `/release-prepare` by default.

## Commands

Required structural and safety validation:

```bash
python scripts/validate-release.py --release-dir releases/<version> --stage prepare
python scripts/validate-image-build.py validate-plan --release <version>
python scripts/validate-mintlify-site.py
```

Run additional checks according to release scope. Common commands:

```bash
uv run pytest
pnpm --dir src/web test -- --run
python scripts/validate-api-standard.py
./scripts/generate-openapi-client.sh
docker compose config --quiet
python scripts/check-mysql-schema-drift.py --database-url "$DATABASE_URL"
```

Only run expensive or environment-dependent checks when they match release scope or user requested full validation. If a command cannot run locally, record the blocker; do not invent evidence.

If `impact_scope.database` is not `none` / `na` / `不涉及`, `database_migration` MUST be `pass` and its evidence MUST explicitly mention MySQL or `schema.mysql.sql`, a schema drift / target MySQL smoke check, and database rollback or backup evidence. Do not paste raw `DATABASE_URL` or credentials into release artifacts.

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

## Final Step — AI Usage Post-command Hook (MUST)

After release preparation completes or records blockers, run:

```bash
python scripts/extract-ai-usage.py \
  --post-command-hook \
  --workflow-event release.prepare \
  --release <version> \
  [--release-sprint <sprint-id>] \
  [--sprint <sprint-id>] \
  [--req <REQ-id>] \
  [--bug <BUG-id>] \
  [--change <change-id>] \
  --json
```

- Pass Sprint / REQ / BUG / Change ids from `releases/<version>/release.json`.
- Pass `--release <version>` so the hook writes both release command run details under `data/ai-usage/command-runs/releases/<version>/<date>--release.prepare--<session-hash>.json` and the version artifact `data/ai-usage/command-runs/releases/<version>/release.prepare.json`.
- Treat the hook as incomplete if `outputs.command_runs` does not point under `data/ai-usage/command-runs/releases/<version>/`; release commands must not store their primary command-run details under `issues/` or `opsxs/` just because the release scope includes REQ / BUG / Change ids.
- Pass each release-scope Sprint with repeated `--release-sprint <sprint-id>` so the release artifact coverage records the full version scope.
- The hook accepts one `--sprint` value per invocation for Sprint snapshot refresh. For a release that spans multiple Sprint ids, run the hook once per Sprint only when you intentionally refresh Sprint snapshots; do not use repeated `--sprint` to express release scope.
- If no Sprint is associated, omit `--sprint`; Sprint snapshot output MUST be `skipped`.
- Print only the compact hook summary: `status`, `usage_mode`, `command_run_count`, `session_input`, `release_artifact`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
- If local session input is unavailable, report `usage_mode: unavailable` and the recommended action; do not treat that as parent command failure.
- If the hook reports `unsafe-records-skipped:<count>`, treat it as a usage-data blocker to fix or explicitly report; do not replace it with a deliberately missing `--session-jsonl`.
- Release scope often includes IDs such as password or token; these business IDs are allowed in command-run metadata and must not be treated as secrets unless they appear as raw credentials, auth headers, `.env` content, assigned secret-like fields, or local absolute paths.
