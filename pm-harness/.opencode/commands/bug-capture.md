---
description: 缺陷记录 - 轻量 capture，分配 BUG-ID
---

**Input**：现象描述、复现步骤、环境（可选截图路径）

Flags：`--severity blocker|critical|high|medium|low`

**Output**：`issues/bugs/BUG-NNNN-slug/capture.md` + `trace.md`；更新 `_registry.yaml`

**禁止**：`bug.md`、`src/`、`openspec/`

---

## capture.md 模板

```markdown
---
bug_id: BUG-0001-example
status: captured
recorded_at: YYYY-MM-DD
severity_hint: high
environment: local|docker|prod
---

# 现象
…

# 复现步骤
1. …

# 期望 vs 实际
…

# 附件
screenshots/…  logs/…
```

## Next

`/bug-explore BUG-xxxx` → `/bug-generate BUG-xxxx`
