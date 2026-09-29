---
created_at: 2026-08-21 08:24:48
updated_at: 2026-08-21 08:24:48
---

# Design

## 证据化根因分析

新增根项目 `rules/root-cause-evidence.md`，将根因判断分为 `unknown`、`hypothesis`、`probable`、`confirmed`。`confirmed` 必须绑定可定位证据；证据不足时输出人工补证步骤，不得把猜测写成结论。

新增轻量脚本 `scripts/validate-root-cause-evidence.py`，检查 active Change 和 Issue 文档中出现根因结论时是否包含根因状态或证据字段。模板侧同步同名规则与脚本，供未来项目使用更完整的 BUG/REQ 目录时扩展。

## 执行链路复盘 Hook

在 `docs/08-command-execution-order.md` 和 `.agents/skills/workflow-sync/SKILL.md` 中增加中央输出契约。所有 workflow 命令完成后输出：

- 链路状态。
- 问题证据。
- 规范优化建议。
- follow-up 状态。

默认不自动创建 follow-up Issue/Change，只输出可复制 capture 文案并等待用户授权。

## UI 返修门禁

在 `rules/ui-design.md`、`docs/standards/prototype-ui-acceptance.md` 和 `.agents/skills/opsx-modify/SKILL.md` 中补充附件截图逐项视觉对照表。UI 型返修如果包含附件截图、标注图、原型截图或实际截图，必须先记录截图编号、页面/状态、期望、实际、偏差、检查方式、处置结论和证据入口。

## REQ 子文档扫尾

在 `.agents/skills/opsx-modify/SKILL.md` 中加入 REQ 子文档一致性扫尾检查。REQ 来源返修完成前，必须按 linked REQ 目录实际存在的子文档判断是否需同步；无需更新也要记录理由。

## Workflow Sync 输出与下一步

根项目当前 Workflow Sync 是轻量脚本，不直接迁移 ProjectMoonBox 的完整派生引擎。此次补充命令说明与脚本输出契约：Issue 子文档 apply 应报告更新文件数、字段数、验收状态和安全同步项；`req.opsx` / `bug.opsx` 后下一步应推导到 `/opsx-apply <REQ|BUG-full-id>`。
