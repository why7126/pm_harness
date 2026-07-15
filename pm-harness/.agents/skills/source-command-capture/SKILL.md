---
name: "source-command-capture"
description: "智能收集 - 自动区分需求与缺陷，按需拆分并分别走 req-capture / bug-capture 落盘"
---

# source-command-capture

Use this skill when the user asks to run the migrated source command `capture`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

**Input**：用户不确定是需求还是 BUG 时的原始描述；可含混合多条。可选：`--priority`、`--severity`、`--parent REQ-xxxx`

**Output**：分类分析表 + 各 REQ/BUG 的 capture.md + trace.md + registry 更新

**禁止**：`requirement.md`、`bug.md`、`src/`、`openspec/`

**定位**：类型已知时用 `/req-capture` 或 `/bug-capture`；本命令用于类型未决或混合输入。

---

## Steps

1. 读 `rules/requirement-management.md`、`rules/bug-management.md`、两个 `_registry.yaml`
2. **解析 → 分类（REQ/BUG）→ 拆分**（见 `.agents/skills/source-command-capture/SKILL.md`）
3. 落盘：REQ 遵循 req-capture 模板与规则；BUG 遵循 bug-capture 模板与规则；frontmatter 加 `captured_via: capture` 与 `classification_rationale`
4. 输出分类分析表 + Capture 摘要

---

## 分类要点

- 已有能力/规范下的偏差 → **BUG**
- 尚未交付的新能力/流程 → **REQ**
- 混合输入 → 拆条目后分别归类
- 新功能 PRD 未达标 → BUG + `related_requirement`
- 边界不清 → 分类表标注待澄清，capture 写待澄清项

拆分分别套用 `/req-capture` Multi-REQ 与 `/bug-capture` Multi-BUG 规则。

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md`.对每条创建的 REQ / BUG：

```bash
for req in REQ-xxxx-slug ...; do
  python scripts/sync-workflow-status.py --event req.capture --req "$req" --sprint auto || exit 1
done
for bug in BUG-xxxx-slug ...; do
  python scripts/sync-workflow-status.py --event bug.capture --bug "$bug" --sprint auto || exit 1
done
```

- Exit code **MUST** be `0`
- Print summary **Workflow Sync Report**（注明 REQ N 条 + BUG M 条）；use `--output detail` only for debugging
- Do **not** hand-edit `sprint.md` Scope marker blocks
