---
description: 需求评审 - 状态变更；仅 approved 可进 Sprint 与 req-opsx
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
---

**Input**：`REQ-xxxx`

Flags：`--approve` | `--reject` | `--defer`（无 flag 时输出评审检查清单并 AskUserQuestion）

**Output**：`review.md`；`trace.md` + `requirement.md` → `status: approved|rejected|deferred`；按结果将整个 REQ 目录从 `issues/requirements/plan/` 移动到 `review/` 或 `archive/`

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
created_at: YYYY-MM-DD hh:mm:ss
updated_at: YYYY-MM-DD hh:mm:ss
date: YYYY-MM-DD hh:mm:ss
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

填写 `lifecycle.reviewed`、`lifecycle.approved`（若 approve），时间值使用 `YYYY-MM-DD hh:mm:ss`

## Step 5 — 移动目录

| result | 目标目录 |
|--------|----------|
| approve | `issues/requirements/review/<REQ-ID>/` |
| reject / defer | `issues/requirements/archive/<REQ-ID>/` |

移动整个 REQ 目录后，更新 `_registry.yaml` 中路径或分区字段；`trace.md` 中保留完整生命周期时间。



## 门禁

**仅 `approved`** 可执行 `/req-opsx`、`/sprint-propose` 纳入。

## Next

`/req-opsx REQ-xxxx` → `/sprint-propose`（可选）

## Final Step — Workflow Sync (MUST)

Run the shared `workflow-sync` step before reporting this command as complete:

```bash
python scripts/sync-workflow-status.py --event req.review --req "<REQ-ID>"
```

Use the actual IDs produced or changed by this command. If the script exits non-zero, read the drift report, fix the inconsistent workflow documents, rerun the sync, and include the final `## Workflow Sync` report in the command output.
