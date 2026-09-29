---
created_at: 2026-08-07 13:56:18
updated_at: 2026-08-07 13:56:18
---

# ProjectPmHarness 测试映射

本文档记录当前 ProjectPmHarness 脚手架工程自身需求、BUG、OpenSpec Change 与验证命令之间的追溯关系。

## 默认验证命令

| 验证项 | 命令 |
|---|---|
| 模板同步 | `python pm-harness/scripts/validate-template-sync.py` |
| 目录结构 | `python pm-harness/scripts/validate-directory-structure.py` |
| Skill 包 | `python pm-harness/scripts/validate-skill-package.py` |
| Agent 上下文预算 | `python pm-harness/scripts/validate-agent-context-budget.py` |
| 发布对象 | `python pm-harness/scripts/validate-release.py` |
| Mintlify 投影 | `python pm-harness/scripts/validate-mintlify-site.py` |

## 映射规则

- 根目录 `issues/` 中进入实现的需求或 BUG，必须能追溯到根目录 `openspec/changes/` 中的 Change，或说明无需 OpenSpec 的豁免原因。
- 根目录 `openspec/changes/` 的 Change 归档前，必须记录已运行的验证命令和结果。
- 修改 `pm-harness/` 或 init-skill 模板资产时，必须至少运行模板同步、目录结构、Skill 包和上下文预算校验。
- 当前项目运行态验证记录不得写入 `pm-harness/` 模板目录。

## 当前映射

暂无 active Change。
