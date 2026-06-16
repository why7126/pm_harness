---
name: /req-review
id: req-review
category: Workflow
description: 需求评审 - 状态变更；仅 approved 可进 Sprint 与 req-opsx
---

**Input**：`REQ-xxxx`

Flags：`--approve` | `--reject` | `--defer`（无 flag 时输出评审检查清单并 AskUserQuestion）

**Output**：`review.md`；`trace.md` + `requirement.md` → `status: approved|rejected|deferred`

---

## Step 1 — 前置检查

- `status` 应为 `pending_review`（或 `enriching` 且 Readiness ≥ Partially Ready）
- 读 requirement、acceptance、trace；UI 类读 prototype

## Step 2 — 评审清单

- [ ] 范围清晰，Out of Scope 明确
- [ ] 验收标准可测试
- [ ] 优先级与依赖合理
- [ ] UI 类：原型或实现策略已决
- [ ] 无与现有 REQ 重复未说明

## Step 3 — 写 review.md

```markdown
---
review_id: REV-REQ-xxxx-001
date: YYYY-MM-DD
participants: []
result: approved | rejected | deferred
---

## 评审结论
…

## 条件通过项
- [ ] …
```

## Step 4 — 更新 status

| result | status |
|--------|--------|
| approve | `approved` |
| reject | `rejected` |
| defer | `deferred` |

填写 `lifecycle.reviewed`、`lifecycle.approved`（若 approve）

## 门禁

**仅 `approved`** 可执行 `/req-opsx`、`/sprint-propose` 纳入。

## Next

`/req-opsx REQ-xxxx` → `/sprint-propose`（可选）
