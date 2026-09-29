---
created_at: 2026-08-27 00:04:20
updated_at: 2026-08-27 00:04:20
---

# Test Plan

## 最小相关验证矩阵

| 影响面 | 验证命令 |
|---|---|
| 根因门禁脚本 | `python scripts/validate-root-cause-evidence.py --all-active --json` |
| Sprint 选择脚本 | `python scripts/validate-sprint-selection.py --json` |
| 根级上下文预算与输出契约卫生 | `python scripts/validate-agent-context-budget.py` |
| OpenSpec 中文规范 | `python scripts/validate-openspec-language.py` |
| 根级目录结构 | `python scripts/validate-directory-structure.py` |
| OpenSpec Change | `openspec validate add-tilesfst-command-governance` |
| 模板同步 | `python pm-harness/scripts/validate-template-sync.py` |
| 模板目录结构 | `python pm-harness/scripts/validate-directory-structure.py` |
| 模板 Skill 包 | `python pm-harness/scripts/validate-skill-package.py` |
| 模板上下文预算 | `python pm-harness/scripts/validate-agent-context-budget.py` |
