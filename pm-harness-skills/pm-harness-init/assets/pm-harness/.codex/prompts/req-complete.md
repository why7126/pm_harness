---
description: 需求完善 - 基于 requirement.md 补齐六件套（不含 OpenSpec）
---

替代原 `/requirement-to-change` 的**文档部分**。不创建 `openspec/changes/`。

**Input**：`REQ-xxxx`（须存在 `requirement.md`）

**Output**：user-stories、business-flow、acceptance、trace（扩写）、prototype（UI 类）；Readiness Report

---

## Step 0 — 读取

```text
AGENTS.md
rules/requirement-management.md
rules/ui-design.md          # UI 类
issues/requirements/<REQ-ID>/requirement.md
issues/requirements/<REQ-ID>/capture.md
```

## Step 1 — 生成/补齐文档

| 文件 | 内容要点 |
|------|----------|
| `user-stories.md` | US-xxx、验收要点 |
| `business-flow.md` | 流程 ASCII、与父 REQ 差异 |
| `acceptance.md` | AC-xxx 可勾选清单 |
| `trace.md` | 扩写 yaml、关联、变更记录 |
| `prototype/web/*` | UI 类：html、context.md；PNG 可标待导出 |

`status` → `enriching`（补齐中）→ 文档齐后 `pending_review`

## Step 2 — Readiness Report

| readiness | 条件 |
|-------------|------|
| Ready | 五件套齐（+ UI 有 prototype 策略） |
| Partially Ready | 缺 PNG 等非阻塞 |
| Not Ready | 缺 acceptance 等 |

## Step 3 — 输出

```text
## Req Complete

**REQ:** REQ-xxxx
**Readiness:** Ready | Partially Ready | Not Ready
**Status:** pending_review

**Next:**
1. /req-review REQ-xxxx --approve
2. 通过后 /req-opsx REQ-xxxx
```

## Guardrails

- 不写 `src/`、不 `openspec new change`
- 不替代 `/req-generate`（若无 requirement.md 先 generate）
