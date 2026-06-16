---
name: "REQ: OPSX"
description: 已评审需求 → OpenSpec Change（CLI 驱动）；原 /requirement-to-opsx
category: Workflow
tags: [workflow]
---

将 **`approved`** 的 `issues/requirements/REQ-*` 转为 `openspec/changes/<change-id>/`（proposal / design / specs / tasks）。**不写 `src/`**；实现用 `/opsx-apply`。

**Input**：`REQ-xxxx` 或 `REQ-xxxx-name`

| Flag | 含义 |
|------|------|
| `--type add\|fix\|update` | 强制 change 类型 |
| `--strategy <name>` | css-port、tailwind-ds 等 |
| `--skip-explore` | 跳过 UI 策略探讨 |
| `--change-name <kebab-case>` | 指定 change id |

---

## 前置关系

```text
/req-capture → /req-explore → /req-generate → /req-complete → /req-review (approved)
        │
        └─ /req-opsx REQ-*  →  /opsx-apply  →  /opsx-archive
```

---

## Step 0 — 必须读取

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/requirement-management.md
rules/ui-design.md
rules/testing.md
rules/directory-structure.md
```

```bash
openspec list --json
openspec list --specs
```

REQ 目录：requirement.md、user-stories.md、business-flow.md、acceptance.md、trace.md、prototype/**

---

## Step 0.5 — 评审门禁（MUST）

读 `trace.md`（或 requirement.md frontmatter）`status`：

| status | 动作 |
|--------|------|
| `approved` | 继续 |
| `pending_review` / `draft` / … | **停止** → `/req-review REQ-xxxx` |
| `in_sprint` / `done` | 可继续（已评审过） |

---

## Step 1 — Readiness

输出 **Requirement Readiness Report**（ready / partially ready / not ready）。

**Not Ready** → `/req-complete REQ-xxxx`，**停止**，不创建 change。

---

## Step 2 — 影响分析与 Change 分类

```yaml
impact: { backend, web, miniapp, admin, database, storage, api }
capabilities: { new: [], modified: [] }
```

| 条件 | change_type | 示例 |
|------|-------------|------|
| 无相关 spec | add | add-user-login |
| 已有实现，验收/视觉未过 | fix | fix-login-css-port |
| 仅规范文案 | update | update-login-acceptance-sync |

---

## Step 3 — 原型与验收冲突（MUST）

`prototype/web/` 存在时输出 Conflict Report；优先级：

```text
HTML > PNG > *-context.md > acceptance.md > ui-design.md > openspec/specs
```

design.md **MUST** 含 Conflict Resolution；delta spec 用 MODIFIED/REMOVED 消化。

---

## Step 4 — UI Explore Gate

`impact.web` 且有 prototype 时，无 `--strategy` 且非 `--skip-explore`：选 CSS Port / DS / Asset，写入 design.md D1。

---

## Step 5 — 创建 Change（CLI）

```bash
openspec new change "<change-id>"
openspec status --change "<change-id>" --json
```

---

## Step 6 — 生成 Artifacts

```bash
openspec instructions <artifact-id> --change "<change-id>" --json
```

按 schema 顺序写 proposal、design、specs、tasks。MODIFIED 标题 **MUST** 与 `openspec/specs/` 一致。

---

## Step 7 — 追溯

更新 REQ `trace.md`：

```yaml
openspec_changes:
  - change_id: …
    type: fix
    status: proposed
```

创建 `openspec/changes/<id>/trace.md`（UI 类含 PNG checklist）。

---

## Step 8 — 输出

```text
## Req → OpenSpec 完成
**REQ:** …
**Change:** …
**Next:** /opsx-apply <change> 或 /sprint-apply sprint-xxx
```

---

## Guardrails

| 规则 | 说明 |
|------|------|
| 仅 approved | 未评审不得 opsx |
| 不替代 req-complete | 文档不全先 complete |
| 不跳过 CLI | 禁止手写 change 目录 |
| 不写 src | 实现用 opsx-apply |

---

## 参考

- `.cursor/commands/req-complete.md`
- `.cursor/commands/opsx-apply.md`、`opsx-archive.md`、`opsx-explore.md`
- 归档样例：`openspec/changes/archive/`
