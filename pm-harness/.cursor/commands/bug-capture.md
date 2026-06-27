---
name: /bug-capture
id: bug-capture
category: Workflow
description: 缺陷记录 - 轻量 capture，分配 BUG-ID
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 09:02:51
---

**Input**：现象描述、复现步骤、环境（可选截图路径）。用户可能一次性提供多个缺陷，必须先评估是否需要拆分。

Flags：`--severity blocker|critical|high|medium|low`

**Output**：一个或多个 `issues/bugs/BUG-NNNN-slug/capture.md` + `trace.md`；更新 `_registry.yaml`

**禁止**：`bug.md`、`src/`、`openspec/`

---

## Steps

0. 读 `rules/bug-management.md`、`issues/bugs/_registry.yaml`，并先做 **Split Assessment**：

   - 若输入包含多个独立现象、不同模块/页面/接口、不同触发路径、不同期望行为、不同严重等级，或可独立修复和验证，MUST 拆分为多个 BUG。
   - 若多个表现明显来自同一根因、同一操作路径、同一修复点，或只是不同环境/账号下的同一现象，保留为一个 BUG，并在 `capture.md` 中记录影响范围。
   - 若拆分不确定，先输出拆分建议（候选标题、拆分理由、风险），向用户确认后再创建文件。
   - `--severity` 默认应用到拆分出的所有 BUG；用户输入中对单项另有说明时，以单项说明为准。

1. 输出 Capture Plan：列出将创建的 BUG 数量、每个 BUG 的一句话标题、拆分理由、继承的 severity/environment。
2. 为每个 BUG 分配连续的 `BUG-NNNN-kebab-slug`（`next_id` 按创建数量递增）。
3. 为每个 BUG 创建目录、`capture.md` 与 `trace.md`，并更新 `_registry.yaml` entries + `next_id`。

## capture.md 模板

```markdown
---
bug_id: BUG-0001-example
status: captured
created_at: YYYY-MM-DD hh:mm:ss
updated_at: YYYY-MM-DD hh:mm:ss
recorded_at: YYYY-MM-DD hh:mm:ss
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

## Final Step — Workflow Sync (MUST)

Run the shared `workflow-sync` step before reporting this command as complete:

```bash
python scripts/sync-workflow-status.py --event bug.capture --bug "<BUG-ID-1>" [--bug "<BUG-ID-2>" ...]
```

Use every actual ID produced or changed by this command. If the script exits non-zero, read the drift report, fix the inconsistent workflow documents, rerun the sync, and include the final `## Workflow Sync` report in the command output.
