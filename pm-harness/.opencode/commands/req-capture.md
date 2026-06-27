---
description: 需求记录 - 轻量 capture，防遗忘，分配 REQ-ID
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 09:02:51
---

**Input**：一句话描述，或粘贴会议/反馈原文。用户可能一次性提供多个需求点，必须先评估是否需要拆分。

可选：`--priority P0|P1|P2`、`--parent REQ-xxxx`

**Output**：一个或多个 `issues/requirements/plan/REQ-NNNN-slug/capture.md` + `trace.md` 最小壳；更新 `_registry.yaml`。

**禁止**：创建 `requirement.md`、写 `src/`、写 `openspec/`。

---

## Steps

0. 读 `rules/requirement-management.md`、`issues/requirements/_registry.yaml`，并先做 **Split Assessment**：

   - 若输入包含多个独立用户目标、角色、业务价值、功能边界、验收标准、优先级或交付节奏，MUST 拆分为多个 REQ。
   - 若只是同一目标下的多个细节、约束、字段、边界条件或验收点，保留为一个 REQ。
   - 若拆分不确定，先输出拆分建议（候选标题、拆分理由、风险），向用户确认后再创建文件。
   - `--priority` 和 `--parent` 默认应用到拆分出的所有 REQ；用户输入中对单项另有说明时，以单项说明为准。

1. 输出 Capture Plan：列出将创建的 REQ 数量、每个 REQ 的一句话标题、拆分理由、继承的 priority/parent。
2. 为每个 REQ 分配连续的 `REQ-NNNN-kebab-slug`（`next_id` 按创建数量递增）。
3. 为每个 REQ 创建目录与 `capture.md`：

```markdown
---
req_id: REQ-0008-example
status: captured
created_at: YYYY-MM-DD hh:mm:ss
updated_at: YYYY-MM-DD hh:mm:ss
recorded_at: YYYY-MM-DD hh:mm:ss
recorded_by: product
source: 会议|反馈|竞品
priority_hint: P1
parent_requirement:
---

# 一句话
…

# 原始描述
…

# 待澄清
- [ ] …

# 探索结论
（/req-explore 后人工确认写入）
```

4. 为每个 REQ 创建 `trace.md`：`status: captured`，`lifecycle.captured` 填完整时间（YYYY-MM-DD hh:mm:ss）。
5. 更新 `_registry.yaml` entries + `next_id`，多 REQ 时必须一次性写入所有 entries。

## Next

`/req-explore REQ-xxxx` → `/req-generate REQ-xxxx`

## Final Step — Workflow Sync (MUST)

Run the shared `workflow-sync` step before reporting this command as complete:

```bash
python scripts/sync-workflow-status.py --event req.capture --req "<REQ-ID-1>" [--req "<REQ-ID-2>" ...]
```

Use every actual ID produced or changed by this command. If the script exits non-zero, read the drift report, fix the inconsistent workflow documents, rerun the sync, and include the final `## Workflow Sync` report in the command output.
