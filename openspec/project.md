---
created_at: 2026-08-07 13:56:18
updated_at: 2026-08-07 13:56:18
---

# ProjectPmHarness OpenSpec 项目上下文

本文档定义当前 ProjectPmHarness 脚手架工程自身的 OpenSpec 上下文。它不属于 `pm-harness/` 新项目模板，也不得被同步到 init-skill 模板资产。

## 项目定位

ProjectPmHarness 是用于维护 PM Harness 脚手架模板、初始化技能、存量项目接入技能和相关治理资产的工程。

它自身也需要通过 Harness 工程治理持续演进，包括：

- 脚手架模板结构与默认文件。
- `.agents/skills/` 命令技能。
- `pm-harness-skills/` 中的初始化、重构和设计资产 Skill。
- 治理规则、校验脚本、发布/部署辅助脚本。
- 当前项目自身的长期文档和 spec 迭代日志。

## 事实源边界

| 类型 | 当前项目事实源 | 是否同步进 `pm-harness/` |
|---|---|---:|
| 当前项目需求/BUG | `issues/` | 否 |
| 当前项目 Sprint | `iterations/` | 否 |
| 当前项目 OpenSpec | `openspec/` | 否 |
| 当前项目长期文档 | `docs/` | 否 |
| 当前项目 spec 日志 | `docs/spec-logs/` | 否 |
| 新项目模板 | `pm-harness/` | 是 |
| init-skill 模板资产 | `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` | 是 |

## Change 范围

ProjectPmHarness 根目录 OpenSpec Change 用于描述脚手架工程自身的治理或模板能力变化。

适用范围：

- 新增或调整默认命令技能。
- 新增或调整脚手架模板目录、规则、脚本或文档。
- 新增或调整 init-skill、refactor-skill、uidesign-skill。
- 新增或调整当前项目自身的治理流程。

不适用范围：

- 具体业务项目的需求、BUG 或实现。
- 目标项目运行时数据。
- 真实 `.env`、密钥、客户数据、构建产物、运行时数据库。

## 执行约束

- 当前项目运行态数据必须留在根目录治理资产中，不得写入 `pm-harness/` 模板目录。
- 只有确认会作为新项目默认能力交付的内容，才同步进 `pm-harness/` 与 init-skill 模板资产。
- 根目录 `openspec/`、`iterations/`、`issues/` 不得同步进 `pm-harness/`。
- 修改模板能力后，应运行模板同步、目录结构、Skill 包和上下文预算校验。
