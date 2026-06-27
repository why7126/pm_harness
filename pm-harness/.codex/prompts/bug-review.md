---
description: 缺陷评审 - 确认是否修复；仅 approved 可 bug-opsx 与进 Sprint
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
---

**Input**：`BUG-xxxx`

Flags：`--approve` | `--reject` | `--defer` | `--wont-fix`

**Output**：`review.md`；status → `approved` | `rejected` | `deferred` | `wont_fix`；按结果将整个 BUG 目录从 `issues/bugs/plan/` 移动到 `review/` 或 `archive/`

## 评审清单

- [ ] 可复现或根因充分
- [ ] 严重等级合理
- [ ] 回归验收明确
- [ ] 是否需 hotfix 路径

## Step 2 — 移动目录

| result | 目标目录 |
|--------|----------|
| approve | `issues/bugs/review/<BUG-ID>/` |
| reject / defer / wont-fix | `issues/bugs/archive/<BUG-ID>/` |

移动整个 BUG 目录后，更新 `_registry.yaml` 中路径或分区字段；`trace.md` 中保留完整生命周期时间。

## 门禁

**仅 `approved`** → `/bug-opsx`、`/sprint-propose`（P0 BUG 优先）

## Next

`/bug-opsx BUG-xxxx`

## Final Step — Workflow Sync (MUST)

Run the shared `workflow-sync` step before reporting this command as complete:

```bash
python scripts/sync-workflow-status.py --event bug.review --bug "<BUG-ID>"
```

Use the actual IDs produced or changed by this command. If the script exits non-zero, read the drift report, fix the inconsistent workflow documents, rerun the sync, and include the final `## Workflow Sync` report in the command output.
