---
name: "image-prepare"
description: "生成或校验发布镜像构建计划"
---

# image-prepare

Use this skill when the user asks `/image-prepare <version>` or wants to prepare image build inputs for a release.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接。
- 从 `releases/<version>/release.json` 开始，只读取该版本关联的发布对象、构建输入和 validator 报告。
- MUST NOT 默认读取所有 `releases/**`、`openspec/archive/**`、generated OpenAPI client、完整 Docker logs 或 raw env 文件。
- 只读取 `scripts/build-images.env.example` 与安全摘要；真实 `scripts/build-images.env` 不得把敏感内容写入 plan 或回复。

## Input

- `<version>`：必填，例如 `v0.2.0`。
- Optional：`--env-file <path>` 指定本地构建 env；默认 `scripts/build-images.env`。

## Must Read

```text
AGENTS.md
rules/release.md
rules/security.md
rules/environment.md
rules/document-governance.md
rules/agent-context-budget.md
releases/<version>/release.json
scripts/build-images.env.example
scripts/validate-image-build.py
```

按 validator 报告分段读取：

```text
src/shared/product-version.ts
src/backend/Dockerfile
src/web/Dockerfile
src/web/nginx.conf
docker-compose.prod.yml
docker-compose.prod.external.yml
.env.example
src/backend/app/db/schema.sql
src/backend/app/db/schema.mysql.sql
src/backend/app/db/migrations.py
src/backend/app/db/mysql_migrations.py
docs/04-database-design.md
docs/08-production-image-release.md
```

## Gates

`/image-prepare` MUST:

- 读取 `releases/<version>/release.json`，缺失时阻断。
- 判断 `image_required`，或在发布对象缺少显式值时按 backend、database、docker、object storage 影响推断。
- 校验用户可见版本事实源、`IMAGE_BUILD_TAG`、Compose image 引用和构建 env 示例。
- 将 release、Dockerfile、Compose、构建脚本、构建 env 示例、Nginx、schema、migration 和数据库文档纳入 input hash。
- 生成或更新 `releases/<version>/image-build-plan.json`。
- Docker 不可用、网络不可用、缺少 env 或版本不一致时记录 blocker；不得伪造 pass 证据。
- 不写入真实 `.env` 内容、密钥、数据库连接串、Authorization header、Cookie、真实客户数据或本机绝对路径。

## Command

```bash
python scripts/validate-image-build.py prepare --release <version>
python scripts/validate-image-build.py validate-plan --release <version>
```

## Output

Report compact summary only:

- version
- image_required
- plan path
- blocker count
- key blockers
- next command: `/image-build <version>` when plan is unblocked and image delivery is required

## AI Usage Post-command Hook（MUST）

After the command completes or records blockers, run:

```bash
python scripts/extract-ai-usage.py \
  --post-command-hook \
  --workflow-event image.prepare \
  --release <version> \
  --json
```

Print only the compact hook summary.
