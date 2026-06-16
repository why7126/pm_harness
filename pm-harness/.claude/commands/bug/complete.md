---
name: "BUG: Complete"
description: 缺陷完善 - 补齐 root-cause、workaround、acceptance、trace
category: Workflow
tags: [workflow]
---

**Input**：`BUG-xxxx`（须 `bug.md`）

**Output**：root-cause.md、workaround.md、acceptance.md、trace.md；logs/、screenshots/ 目录（若需）

**禁止**：`openspec/`、`src/`

---

## 文档要点

| 文件 | 内容 |
|------|------|
| root-cause.md | 直接原因、根本原因、触发条件、分类（code/design/db/…） |
| workaround.md | 临时规避或无 |
| acceptance.md | 回归 AC-xxx |
| trace.md | status → enriching → pending_review |

## Readiness

Ready：bug + root-cause + acceptance + trace

## Next

`/bug-review BUG-xxxx --approve`
