---
created_at: 2026-08-19 11:25:48
updated_at: 2026-08-19 11:25:48
---

# Trace

## 来源

- 命令：`/spec-study apply Agent Decision Notes + 文档层级与一事实一归属 + 治理检查聚合器`
- 学习对象：`https://github.com/deepseek-ai/deepseek-harness`
- 学习模式：`auto`
- Sprint：`sprint-001`

## 只读保护

学习对象作为外部只读快照读取。应用阶段只修改 ProjectPmHarness 当前仓库治理资产与模板资产，不修改学习对象。

## 影响映射

| 采纳项 | 本项目落点 |
|---|---|
| Agent Decision Notes | `rules/governance-decision-notes.md`、`docs/decision-notes/` |
| 文档层级与一事实一归属 | `rules/document-governance.md` |
| 治理检查聚合器 | `scripts/run-governance-checks.py` |
