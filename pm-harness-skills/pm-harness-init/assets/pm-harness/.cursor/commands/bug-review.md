---
name: /bug-review
id: bug-review
category: Workflow
description: 缺陷评审 - 确认是否修复；仅 approved 可 bug-opsx 与进 Sprint
---

**Input**：`BUG-xxxx`

Flags：`--approve` | `--reject` | `--defer` | `--wont-fix`

**Output**：`review.md`；status → `approved` | `rejected` | `deferred` | `wont_fix`

## 评审清单

- [ ] 可复现或根因充分
- [ ] 严重等级合理
- [ ] 回归验收明确
- [ ] 是否需 hotfix 路径

## 门禁

**仅 `approved`** → `/bug-opsx`、`/sprint-propose`（P0 BUG 优先）

## Next

`/bug-opsx BUG-xxxx`
