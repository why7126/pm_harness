---
created_at: 2026-08-27 00:04:20
updated_at: 2026-08-27 00:04:20
---

# 设计

## 设计原则

- 学习对象只读，只吸收治理机制，不复制业务事实或运行态数据。
- 根项目治理资产与模板资产同步，但当前项目 Issue、Sprint、OpenSpec 和 spec 日志不写入模板。
- 脚本以确定性门禁为主，输出保持 compact，失败时给出可定位 blocker。

## 应用映射

| 候选项 | ProjectPmHarness 落点 |
|---|---|
| `bug-review-confirmed-gate` | `.agents/skills/bug-review/SKILL.md`、`scripts/validate-root-cause-evidence.py`、`rules/root-cause-evidence.md` |
| `sprint-propose-selection` | `.agents/skills/sprint-propose/SKILL.md`、`scripts/validate-sprint-selection.py`、Sprint 四件套 |
| `final-output-contract-hygiene` | `scripts/validate-agent-context-budget.py`、已有 Final Output Contract 的命令 Skill |

## 校验策略

- 根级：运行上下文预算、OpenSpec 中文、目录结构、OpenSpec validate 和改动脚本自检。
- 模板侧：运行模板同步、目录结构、Skill 包和上下文预算校验。
- 复核：确认 `src/` 无修改，并查询学习对象 Git 状态以证明未写入。
