---
name: "source-command-req-capture"
description: "需求记录 - 轻量 capture，防遗忘，分配 REQ-ID；支持一次输入多条并按需拆分"
---

# source-command-req-capture

Use this skill when the user asks to run the migrated source command `req-capture`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

**Input**：一句话描述，或粘贴会议/反馈原文。用户可能在一条消息中描述**多个**独立需求。

可选：`--priority P0|P1|P2`、`--parent REQ-xxxx`

**Output**：每条需求 → `issues/requirements/REQ-NNNN-slug/capture.md` + `trace.md`；更新 `_registry.yaml`

**禁止**：创建 `requirement.md`、写 `src/`、写 `openspec/`。

---

## Steps

1. 读 `rules/requirement-management.md`、`issues/requirements/_registry.yaml`
2. **评估并拆分**（见下节）
3. 为每条 REQ 分配 ID、创建 capture + trace、更新 registry
4. 输出 Capture 摘要（多条用表格）

---

## Multi-REQ 评估（MUST）

解析用户输入，决定 **1 条** 还是 **N 条** REQ。

**应拆分**（任一满足）：不同业务能力/模块/端；独立优先级；独立 OpenSpec Change 或验收闭环；用户显式枚举多条。

**保持单条**（全部满足）：同一功能域的一个交付单元；同一 PRD 内的细节展开；对已有 REQ 的小幅 refinement → 优先 `--parent` 或更新原 REQ，而非新 peer REQ。

**实为缺陷** → 引导 `/bug-capture`，不要 req-capture。

**规则**：每条独立 REQ-ID 与目录；禁止 umbrella REQ。未拆分时回复一句话 rationale。

---

## capture.md 模板

```markdown
---
req_id: REQ-0008-example
status: captured
created_at: YYYY-MM-DD HH:mm:ss
updated_at: YYYY-MM-DD HH:mm:ss
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

## Next

每条：`/req-explore REQ-xxxx` → `/req-generate REQ-xxxx`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md`.对**本次创建的每一条** REQ：

```bash
for req in REQ-xxxx-slug ...; do
  python scripts/sync-workflow-status.py --event req.capture --req "$req" --sprint auto || exit 1
done
```

- Exit code **MUST** be `0`
- Print summary **Workflow Sync Report**（多条时注明共 N 条）；use `--output detail` only for debugging
- Do **not** hand-edit `sprint.md` Scope marker blocks
