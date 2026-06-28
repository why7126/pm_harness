---
title: Knowledge Base Usage
purpose: 规定 docs/knowledge-base 如何被后续 Sprint、需求完善和 OpenSpec 实现流程复用
content: 知识库入口、行动项状态、命令读取门禁和落地要求
source: workflow governance
update_method: Sprint 复盘、best-practice 或命令门禁变化时更新
owner: 项目负责人
status: active
---

# Knowledge Base Usage

`docs/knowledge-base/` 保存跨 Sprint 可复用的经验、复盘、事故和最佳实践。它不是事后报告库；后续规划、需求完善和实现命令必须把这里的内容作为输入。

## 目录职责

| 路径 | 职责 | 使用时机 |
|---|---|---|
| `sprints/` | Sprint 复盘、行动项、容量与流程经验 | `/sprint-propose` 必读上一 Sprint 和未关闭行动项 |
| `incidents/` | 故障、事故、线上问题复盘 | `/bug-opsx`、`/opsx-apply`、`/sprint-apply` 处理相关能力时必读 |
| `best-practices/` | 可复用设计、组件、测试、验收模式 | `/req-complete`、`/opsx-apply`、`/sprint-apply` 按主题匹配读取 |

## 行动项状态

复盘行动项必须使用以下状态之一：

| 状态 | 含义 |
|---|---|
| `open` | 已提出，尚未进入 Sprint 或 Change |
| `in_sprint` | 已被当前或未来 Sprint 承接 |
| `done` | 已通过 REQ/BUG/Change 或规则更新落地 |
| `deferred` | 明确延期，并记录原因 |
| `rejected` | 明确不做，并记录原因 |

## 命令门禁

| 命令 | 必须读取 | 必须落地 |
|---|---|---|
| `/sprint-propose` | 最近一次 Sprint 复盘、所有 `open`/`in_sprint` 行动项、相关 best-practices | 在 `sprint.md` 写「知识库承接项」，在 `sprint.yaml` 记录承接的 action id |
| `/req-complete` | 与需求领域、UI 模式、数据流、上传、权限、测试相关的 best-practices | 在 `acceptance.md` 增加知识库 checklist，无法适用时写明原因 |
| `/opsx-apply` | 当前 Change 关联领域的 best-practices 与 incidents | 实现前输出 Knowledge Gate，不能只在修 Bug 后引用 |
| `/sprint-apply` | Sprint 承接项、相关 best-practices、相关 incidents | Queue Report 中列出 Knowledge Gate 状态 |

## 禁止事项

- 禁止只在 `/sprint-exps` 写入知识库，而在下一 Sprint 规划中不读取。
- 禁止将 `open` 行动项长期保留而不标记 `in_sprint`、`done`、`deferred` 或 `rejected`。
- 禁止 add-* Change 忽略已存在的同类 best-practice，等 Bug 出现后才引用。
