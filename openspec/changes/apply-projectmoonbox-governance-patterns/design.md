---
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-10 23:19:03
---

# 设计

## 设计原则

- 学习对象只读，应用内容按 ProjectPmHarness 目录边界重写。
- 根项目运行态治理资产与模板资产分开维护。
- 新项目默认能力同步到 `pm-harness/` 与 init-skill 模板资产。
- 脚本输出必须脱敏，不输出真实 env、密钥、连接串或本机路径原文。

## 应用映射

| 候选项 | ProjectPmHarness 落点 |
|---|---|
| `git-check-security-gate` | `scripts/git-check.py`、`.agents/skills/git-check/SKILL.md`、`rules/security.md`、模板同名文件 |
| `issues-changelog-current-state` | `issues/*/CHANGELOG.md`、`rules/issues-lifecycle.md`、`rules/document-governance.md`、模板同名文件 |
| `command-execution-order` | `docs/08-command-execution-order.md`、`AGENTS.md`、模板同名文件 |
| `prototype-ui-acceptance` | `docs/standards/prototype-ui-acceptance.md`、`rules/ui-design.md`、模板同名文件 |
| `spec-study-log-first-learning` | `.agents/skills/spec-study/SKILL.md`、`rules/agent-context-budget.md`、模板同名文件 |
| `guided-command-feedback` | `AGENTS.md`、`rules/agent-context-budget.md`、核心命令 Skill 共享契约 |

## 校验策略

- 根级：运行上下文预算、OpenSpec 中文、目录结构、`git-check` 和 OpenSpec validate。
- 模板侧：运行模板同步、目录结构、Skill 包和上下文预算校验。
- 复核：确认 `src/` 无修改，并查询学习对象 Git 状态以证明未写入。
