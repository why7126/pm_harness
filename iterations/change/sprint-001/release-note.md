---
created_at: 2026-08-07 15:23:44
updated_at: 2026-10-28 11:36:10
---

# Release Note

- 新增 ProjectPmHarness 根级 `AGENTS.md`，作为当前脚手架工程自身的 AI 行为入口。
- 新增 `docs/spec-logs/CHANGELOG.md`，作为规范、脚本、命令和技能更新历史总账。
- 新增 TilesFST 命令治理门禁：BUG review confirmed 根因校验、Sprint 选择脚本和最终输出契约卫生校验。
- 新增 TilesFST 产品数据采集与链路观测治理：长期标准、硬门禁脚本和 REQ/OpenSpec/Sprint 工作流 Skill 声明门禁。
- 新增 TilesFST `sprint.md` 治理：目标编号列表、Scope 六列表、范围追加脚本、Scope 校验、Workflow Sync 派生刷新、归档 readiness 和 Fact Sheet read-first 复盘入口。
- 新增 TilesFST AI Usage session 自动发现治理：workflow hook 默认发现本地 session，并保持脱敏 compact 输出。

## Git 交付治理

新增 `/git-sync` 契约，补齐 index 与历史检查、无内容诊断、精确占位符和 env 忽略双向校验；模板与 init 资产同步。未执行发布或 Git 推送。证据见 `docs/spec-logs/20261028113427-study-moonbox-git-governance.md`。
