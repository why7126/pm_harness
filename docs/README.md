---
created_at: 2026-08-07 13:13:52
updated_at: 2026-08-07 13:13:52
---

# ProjectPmHarness Docs

`docs/` 用于沉淀当前 ProjectPmHarness 脚手架工程自身的长期产品、架构、治理和维护文档。

当前仓库同时包含两类对象：

- 当前脚手架工程：仓库根目录下的 `docs/`、`.agents/`、`pm-harness-skills/` 等。
- 新项目模板：`pm-harness/` 及 `pm-harness-skills/pm-harness-init/assets/pm-harness-template/`。

## 文档索引

| 文档 | 用途 |
|---|---|
| `00-project-governance.md` | 定义 ProjectPmHarness 自身迭代、脚手架模板迭代和运行日志边界 |
| `08-command-execution-order.md` | 定义 REQ/BUG、Sprint、OpenSpec、发布和治理命令的推荐执行顺序 |
| `standards/document-prose-hygiene.md` | 定义长期文档表达卫生、过程残留和敏感片段审计标准 |
| `docs/standards/product-data-collection-observability.md` | 定义产品数据采集、请求日志、Task Trace、端请求封装和治理声明的观测标准 |
| `standards/prototype-ui-acceptance.md` | 定义带 prototype 的 UI Change 验收合同、视觉证据和归档门禁 |
| `../rules/iterations-lifecycle.md` | 定义 Sprint 阶段目录、`sprint.md` Scope 合同、范围追加脚本和归档 readiness 门禁 |
| `../rules/root-cause-evidence.md` | 定义问题排查、BUG 完善和返修中的根因状态、证据链和补证要求 |
| `../README.md#pm-harness-skills` | 索引当前仓库维护的 Harness 应用 Skill，包括初始化、重构、UI 设计资产、PRD 链路和工具调研 |

## 边界

- 当前项目长期说明放入根目录 `docs/`。
- 当前项目维护的可复用 Harness 应用 Skill 放入根目录 `pm-harness-skills/`，目录清单和用途以根 `README.md` 的 `pm-harness-skills` 与 `Skill 应用` 章节为准。
- 当前项目需求/BUG、Sprint 和 OpenSpec 分别放入根目录 `issues/`、`iterations/`、`openspec/`。
- 当前项目 spec 学习、治理优化和规范迭代日志放入 `docs/spec-logs/`。
- `pm-harness/docs/` 是生成新项目时携带的模板文档目录，不承载当前 ProjectPmHarness 的实际项目数据。
- `pm-harness/docs/spec-logs/` 是生成新项目时携带的空日志目录，只保留 `.gitkeep`。
