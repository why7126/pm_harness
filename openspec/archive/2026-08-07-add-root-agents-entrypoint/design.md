---
created_at: 2026-08-07 15:23:44
updated_at: 2026-08-07 15:23:44
---

# Design

## 方案

在仓库根目录新增 `AGENTS.md`，作为 ProjectPmHarness 自身的 AI 行为入口。

该入口与 `pm-harness/AGENTS.md` 分离：

- 根 `AGENTS.md` 服务当前脚手架工程自身治理。
- `pm-harness/AGENTS.md` 服务未来生成的新项目模板。

## 同步边界

本次新增的根 `AGENTS.md` 属于当前 ProjectPmHarness 运行态治理资产，不同步进 `pm-harness/` 或 init-skill 模板资产。

## 验证

运行模板同步、目录结构、Skill 包和上下文预算校验，确认该新增入口不会污染模板资产。

## 归档验证摘要

- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- 缓存扫描：未发现 `.DS_Store`、`__pycache__` 或 `.pyc`。
