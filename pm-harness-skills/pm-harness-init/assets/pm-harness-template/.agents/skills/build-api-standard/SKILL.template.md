---
name: "build-api-standard"
description: "建立 API Governance（统一响应 / 错误码 / OpenAPI / Orval）"
---

# build-api-standard

Use this skill when the user asks to run the migrated source command `build-api-standard`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

将 `rules/api.md` 落地为可执行 API 治理：文档、Schema、校验脚本与 后端分层约定。

**关联 REQ**：`REQ-0000-build-api-standard`（`change_id: build-api-standard`，已归档见 `openspec/specs/api-governance/`）

**Input**：`--verify` 仅校验

---

## 必须读取

```text
AGENTS.md
rules/api.md
rules/security.md
rules/testing.md
rules/coding.md
openspec/specs/api-governance/spec.md
src/backend/app/**
src/web/orval.config.ts
docs/03-api-index.md
```

---

## 与 req / opsx 关系

| 场景 | 做法 |
|------|------|
| 新业务 API | 对应业务 REQ 的 `/req-opsx` → `add-*` |
| 治理规范变更 | 新 REQ + `/req-opsx`（MODIFIED `api-governance`） |
| 接口实现后 | **MUST** 更新 OpenAPI + `scripts/generate-openapi-client.sh` |

---

## Step 1 — 治理文档

核对/更新：

```text
docs/standards/api-governance.md
docs/standards/error-codes.md
docs/standards/openapi-rules.md
docs/standards/authentication.md
docs/standards/file-upload.md
docs/03-api-index.md
```

---

## Step 2 — 统一结构

```text
src/backend/app/schemas/common/     # response, pagination, error
src/backend/app/core/error_codes.py
src/backend/app/api/v1/
```

统一响应：`{ code, message, data }`；分页 `page` / `page_size` / `items` / `total`。

---

## Step 3 — OpenAPI First

- 路由须 `response_model`、`summary`、`tags`
- 导出 `src/web/openapi.json` 为契约
- Orval → `src/web/src/shared/api/generated.ts`

---

## Step 4 — 测试与校验

```text
src/backend/tests/                  # 集成测试
scripts/validate-api-standard.py
```

每接口：成功、失败、权限、边界。

---

## Step 5 — OpenSpec

已归档 **勿重建** `build-api-standard`。新治理需求走 `/req-opsx`。

---

## 验收

```text
□ validate-api-standard.py pass
□ Orval 生成无报错
□ error_codes 与 rules/api.md 一致
```
