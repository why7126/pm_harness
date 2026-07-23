---
name: "build-design-system"
description: "基于 rules/ui-design.md 建设可执行 Design System（Token / 组件 / 校验）"
---

# build-design-system

Use this skill when the user asks to run the migrated source command `build-design-system`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

将 `rules/ui-design.md` 落地为 Token、组件、模板、预览页与 `validate-design-system.py`。

**关联 REQ**：`REQ-0000-build-design-system`（`change_id: build-design-system`，已归档见 `openspec/specs/design-system/`）

**Input**：`--verify` 仅校验；默认实现/补全缺失资产

---

## 必须读取

```text
AGENTS.md
rules/ui-design.md
rules/directory-structure.md
rules/coding.md
rules/testing.md
rules/requirement-management.md
src/web/README.md
src/shared/design-system/tokens/*
openspec/specs/design-system/spec.md
```

---

## 与 req / opsx 关系

| 场景 | 做法 |
|------|------|
| 绿场首次建设 | `/req-capture` … `/req-opsx` → `add-design-system` 或 `build-design-system` |
| 已归档（本项目） | 直接按本命令补代码；**规范变更**须新 REQ + `/req-opsx` |
| 实现 | `/opsx-apply`（若有活跃 change） |

**禁止**：手写 `openspec/changes/` 无 `.openspec.yaml`；业务页硬编码 Hex。

---

## Step 1 — 目录与 spec

确保存在：

```text
src/shared/design-system/tokens/
src/web/src/styles/globals.css
src/web/tailwind.config.ts
src/web/src/components/ui/          # shadcn
src/web/src/shared/ui/
src/web/src/shared/business/
src/web/src/shared/templates/
src/web/src/pages/dev/DesignSystemPage.tsx
scripts/validate-design-system.py
```

`design-system/spec.md` 可选；上游以 `rules/ui-design.md` 为准。

---

## Step 2 — Tokens 与 CSS

- 更新 `src/shared/design-system/tokens/*`
- 颜色 → `globals.css` CSS Variables
- 非颜色 → `pnpm sync:tokens` → `tokens.generated.css`
- 前端样式配置引用项目 semantic class

---

## Step 3 — 组件与模板

按 AGENTS.md Design System 应用规范优先级：

```text
templates → business → shared/ui → components/ui
```

禁止在 `features/` 重复实现 DS 组件。

---

## Step 4 — 预览与校验

- `/design-system` 路由可展示 Token 与组件
- 运行 `python scripts/validate-design-system.py`

---

## Step 5 — OpenSpec（仅当需要新 change）

**不得**重复创建已归档的 `build-design-system`。若需增量能力：

```text
/req-capture → … → /req-review --approve → /req-opsx REQ-xxxx
```

delta spec **MODIFIED** 标题须与 `openspec/specs/design-system/spec.md` 一致。

---

## 验收

```text
□ Token / globals / tailwind 一致
□ 无裸 Hex（校验脚本 pass）
□ DesignSystemPage 可访问
□ REQ-0000 trace 含 change_id: build-design-system
```

## 参考

- `issues/requirements/archive/REQ-0000-build-design-system/`
- `openspec/changes/archive/2026-06-13-add-design-system/`（如存在）
