---
name: /bug-explore
id: bug-explore
category: Workflow
description: 缺陷探索 - 复现与影响分析，默认不写文档
---

探讨：能否稳定复现、影响面、是否回归、关联 REQ/Change、hotfix vs 常规 fix。

**Input**：`BUG-xxxx`

**默认**：不写任何文件、不写代码、不改 `src/`

用户明确要求时可更新 `capture.md`；trace 可标 `exploring`。

## 禁止

- 写 `bug.md`、root-cause、OpenSpec
- 自动修复代码

## Next

`/bug-generate BUG-xxxx`
