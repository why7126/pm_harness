---
purpose: 文档治理规范
content: 文档分类、时间格式、spec-logs、Issue 当前态索引和安全边界
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-27 00:26:26
---

# 文档治理规范

## 文档分类

- `docs/`：当前 ProjectPmHarness 的长期产品、架构、治理和维护文档。
- `docs/spec-logs/`：跨项目学习和治理优化日志。
- `docs/decision-notes/`：非平凡治理决策的长期理由、取舍和后果。
- `issues/`：当前项目 REQ/BUG，不得写入 `pm-harness/` 模板目录。
- `iterations/`：当前项目 Sprint。
- `openspec/`：当前项目 OpenSpec Change、Specs 和 Archive。

## 文档层级

每类事实 MUST 只有一个长期事实源，其他位置用链接或一句话路由指向事实源，避免复制整段规则。

| 层级 | 事实源职责 |
|---|---|
| `AGENTS.md` | AI 必须随时知道的入口规则、读取路由和执行红线 |
| `README.md` | 项目定位、目录说明和协作模型总览 |
| `rules/*.md` | 可执行治理约束、边界、命令契约和安全规则 |
| `docs/*.md` | 长期产品、架构、治理和维护说明 |
| `docs/spec-logs/*.md` | 一次 `/spec-study` 或 `/spec-opt` 的证据、结果和验证 |
| `docs/decision-notes/*.md` | 长期治理决策的动机、取舍、替代方案和后果 |
| `issues/**` | REQ/BUG 当前事实、验收、追踪和状态 |
| `iterations/**` | Sprint 范围、承诺、验收和发布说明 |
| `openspec/changes/**` | 待实施或实施中的工程变更事实 |
| `openspec/specs/**` | 已归档后的稳定能力规格 |

## 一事实一归属

- 入口文档只保留站立规则，不展开长流程；长流程放入对应 `rules/`、`docs/` 或 Skill。
- 规则文档只维护当前有效约束；历史原因放入 `docs/decision-notes/` 或 `docs/spec-logs/`。
- `/spec-study` 与 `/spec-opt` 报告只记录一次命令的学习、应用和验证，不作为长期规范的唯一来源。
- OpenSpec Change 只记录本次变更范围和实施状态；稳定规则归档后应沉淀到 `rules/`、`docs/` 或 `openspec/specs/`。
- 重复段落 SHOULD 改为相对链接。只有 AI 入口、安全红线、模板边界等必须常驻上下文的短规则 MAY 重复。

## 产品数据采集与链路观测事实源

产品数据采集、请求日志、行为事件、Task Trace 和端请求封装的长期事实源为 `docs/standards/product-data-collection-observability.md`；其他文档只保留入口链接、适用条件和本次变更摘要。

若 REQ、BUG、Sprint 或 OpenSpec Change 涉及 API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装，MUST 复核 `product_data_collection_observability` 声明、`affected_layers` 适用层级、`reason` 原因和 `validation` 验证摘要；不适用时 MUST 写明 N/A 或 `not_applicable` 原因。

## 时间格式

新增或更新 Markdown Frontmatter MUST 使用：

```text
created_at: YYYY-MM-DD HH:mm:ss
updated_at: YYYY-MM-DD HH:mm:ss
```

默认时区为 `Asia/Shanghai`。更新文档时不得改 `created_at`，必须刷新 `updated_at`。

## Spec Logs

`/spec-study apply` 的正式学习报告 MUST 写入 `docs/spec-logs/YYYYMMDDhhmmss-study-xxx.md`，同一次学习应用流程只生成一份 `study` 报告。

`/spec-opt` 或非学习来源治理优化使用 `YYYYMMDDhhmmss-governance-xxx.md`。

`docs/spec-logs/CHANGELOG.md` 是规范工程变更历史总账，新增或修改规范、脚本、命令、技能、目录边界、模板能力或校验规则后 SHOULD 更新。

## 治理决策记录

`docs/decision-notes/` 用于保存非平凡治理变更的长期理由。写入规则见 `rules/governance-decision-notes.md`。

## Issue 当前态索引

`issues/requirements/CHANGELOG.md` 与 `issues/bugs/CHANGELOG.md` 是 REQ/BUG 当前态看板索引。它们不参与机器状态判断，机器事实源仍以 registry、trace、Sprint 和 OpenSpec 为准。

## 公开安全

文档、报告、OpenSpec、Sprint 和最终回复不得包含真实密钥、真实客户数据、未脱敏日志、本机绝对路径、真实 env 内容或学习对象源码。
