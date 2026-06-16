---
name: "REQ: Capture"
description: 需求记录 - 轻量 capture，防遗忘，分配 REQ-ID
category: Workflow
tags: [workflow]
---

**Input**：一句话描述，或粘贴会议/反馈原文。

可选：`--priority P0|P1|P2`、`--parent REQ-xxxx`

**Output**：`issues/requirements/REQ-NNNN-slug/capture.md` + `trace.md` 最小壳；更新 `_registry.yaml`。

**禁止**：创建 `requirement.md`、写 `src/`、写 `openspec/`。

---

## Steps

1. 读 `rules/requirement-management.md`、`issues/requirements/_registry.yaml`
2. 分配 `REQ-NNNN-kebab-slug`（`next_id` 递增）
3. 创建目录与 `capture.md`：

```markdown
---
req_id: REQ-0008-example
status: captured
recorded_at: YYYY-MM-DD
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

4. 创建 `trace.md`：`status: captured`，`lifecycle.captured` 填日期
5. 更新 `_registry.yaml` entries + `next_id`

## Next

`/req-explore REQ-xxxx` → `/req-generate REQ-xxxx`
