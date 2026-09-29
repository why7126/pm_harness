---
created_at: 2026-08-21 08:24:48
updated_at: 2026-08-21 08:24:48
---

# Trace

## 来源

- 命令：`/spec-study apply root-cause-evidence-governance command-execution-review-hook opsx-modify-ui-screenshot-comparison-gate opsx-modify-req-subdocument-sweep workflow-sync-issue-output-next`
- 学习对象：`ProjectMoonBox`
- 学习模式：`auto`
- Sprint：`sprint-001`

## 只读保护

学习对象作为外部只读输入读取。应用阶段只修改 ProjectPmHarness 当前仓库治理资产与模板资产，不修改学习对象。

## 影响映射

| 采纳项 | 本项目落点 |
|---|---|
| root-cause-evidence-governance | `rules/root-cause-evidence.md`、`scripts/validate-root-cause-evidence.py`、相关 Skill |
| command-execution-review-hook | `docs/08-command-execution-order.md`、`.agents/skills/workflow-sync/SKILL.md`、`rules/agent-context-budget.md` |
| opsx-modify-ui-screenshot-comparison-gate | `rules/ui-design.md`、`docs/standards/prototype-ui-acceptance.md`、`.agents/skills/opsx-modify/SKILL.md` |
| opsx-modify-req-subdocument-sweep | `.agents/skills/opsx-modify/SKILL.md` |
| workflow-sync-issue-output-next | `.agents/skills/workflow-sync/SKILL.md`、`scripts/sync-workflow-status.py` |
