---
created_at: 2026-08-08 20:56:51
updated_at: 2026-08-08 20:56:51
---

# Design

## 方案

在 `docs/spec-logs/` 下新增 `CHANGELOG.md`。

`CHANGELOG.md` 保持为人工可读索引，按倒序维护条目。每条记录包含：

- 时间。
- 类型：规范、脚本、命令、模板、技能、目录、学习应用等。
- 摘要。
- 影响范围。
- 其他项目落地提示词。
- 关联日志。
- 关联 Change / Sprint。
- 验证结果。

## 边界

`CHANGELOG.md` 属于当前 ProjectPmHarness 运行态治理资产，不进入 `pm-harness/` 模板目录。未来生成的新项目若需要类似能力，应通过模板能力变更另行评估。
