---
name: "REQ: Explore"
description: 需求探索 - 思考分析已记录需求，默认不写任何文档
category: Workflow
tags: [workflow]
---

对标 `/opsx-explore`，面向 **需求域**。探讨范围、用户、风险、与现有 REQ 重复、是否子需求。

**Input**：`REQ-xxxx` 或 capture 阶段的一句话（无 ID 则先建议 `/req-capture`）

**默认**：**不生成任何文件、不写代码**。

**可选**：用户明确要求「记录结论」时，才更新 `capture.md#探索结论`；可将 trace `status` 标为 `exploring`。

---

## Stance

- 好奇、可视化（ASCII 依赖/范围图）
- 可读 `capture.md`、类似 REQ、相关 `src/`（只读）
- 不 prescriptive 到单一方案

## 可探讨

- 范围 In/Out、与 REQ-0005 等重复？
- 子需求 vs 独立 REQ
- UI 是否需要 prototype
- 技术风险与 Sprint 容量

## 禁止

- 写 `requirement.md`、六件套、OpenSpec
- 写 `src/`
- 自动更新文件（除非用户明确要求）

## Next

`/req-generate REQ-xxxx` 或继续 explore
