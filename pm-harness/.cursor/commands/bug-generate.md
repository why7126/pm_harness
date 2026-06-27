---
name: /bug-generate
id: bug-generate
category: Workflow
description: 缺陷生成 - 仅生成 bug.md
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
---

**Input**：`BUG-xxxx`（须 `capture.md`）

**Output**：**仅** `bug.md`；trace → `status: draft`

## bug.md frontmatter

```yaml
---
bug_id: BUG-xxxx
title:
severity: high
status: draft
owner:
created_at: YYYY-MM-DD hh:mm:ss
updated_at: YYYY-MM-DD hh:mm:ss
discovered_at: YYYY-MM-DD hh:mm:ss
environment:
related_requirement:
related_change:
---
```

正文：现象、复现、期望/实际、影响范围、严重等级说明。

## Next

`/bug-complete BUG-xxxx`

## Final Step — Workflow Sync (MUST)

Run the shared `workflow-sync` step before reporting this command as complete:

```bash
python scripts/sync-workflow-status.py --event bug.generate --bug "<BUG-ID>"
```

Use the actual IDs produced or changed by this command. If the script exits non-zero, read the drift report, fix the inconsistent workflow documents, rerun the sync, and include the final `## Workflow Sync` report in the command output.
