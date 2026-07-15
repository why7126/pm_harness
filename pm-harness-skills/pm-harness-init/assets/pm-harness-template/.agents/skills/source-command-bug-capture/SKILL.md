---
name: "source-command-bug-capture"
description: "缺陷记录 - 轻量 capture，分配 BUG-ID；支持一次输入多条并按需拆分"
---

# source-command-bug-capture

Use this skill when the user asks to run the migrated source command `bug-capture`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

**Input**：现象描述、复现步骤、环境（可选截图路径）。用户可能在一条消息中描述**多个**独立缺陷。

Flags：`--severity blocker|critical|high|medium|low`（单条时；拆分时按每条单独评估）

**Output**：每条缺陷 → `issues/bugs/BUG-NNNN-slug/capture.md` + `trace.md`；更新 `_registry.yaml`

**禁止**：`bug.md`、`src/`、`openspec/`

---

## Steps

1. 读 `rules/bug-management.md`、`issues/bugs/_registry.yaml`
2. **评估并拆分**（见下节）
3. 为每条 BUG 分配 ID、创建 capture + trace、更新 registry
4. 输出 Capture 摘要（多条用表格）

---

## Multi-BUG 评估（MUST）

解析用户输入，决定 **1 条** 还是 **N 条** BUG。

**应拆分**（任一满足）：不同界面/层级；不同缺陷类型；不同修复面或独立 `fix-*` Change；独立严重度或交付优先级；用户显式枚举多条。

**保持单条**（全部满足）：同一页面/弹窗且一次修复可闭环；同一根因的不可分割现象；拆分会导致重复 repro/acceptance。

**规则**：每条独立 BUG-ID 与目录；禁止 umbrella BUG；同属一 REQ 时填相同 `related_requirement`；因果链用 `related_bug`。未拆分时回复一句话 rationale。

---

## capture.md 模板

```markdown
---
bug_id: BUG-0001-example
status: captured
created_at: YYYY-MM-DD HH:mm:ss
updated_at: YYYY-MM-DD HH:mm:ss
severity_hint: high
environment: local|docker|prod
related_requirement:
related_bug:
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

每条：`/bug-explore BUG-xxxx` → `/bug-generate BUG-xxxx`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md`.对**本次创建的每一条** BUG：

```bash
for bug in BUG-xxxx-slug ...; do
  python scripts/sync-workflow-status.py --event bug.capture --bug "$bug" --sprint auto || exit 1
done
```

- Exit code **MUST** be `0`
- Print summary **Workflow Sync Report**（多条时注明共 N 条）；use `--output detail` only for debugging
- Do **not** hand-edit `sprint.md` Scope marker blocks
