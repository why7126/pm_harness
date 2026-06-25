# 默认命令目录

## 使用规则

- 生成 Agent 命令前必须完整读取本文档。
- 所有启用 Agent 工具必须实现同一套命令语义。
- 命令中的产品名、路径、示例业务和技术栈必须参数化；不得保留来源项目业务信息。

| 命令族 | 默认命令 | 阶段/作用 | 是否生成文档 | 是否生成代码 |
|---|---|---|---:|---:|
| 需求治理 | `/req-capture`、`/req-explore`、`/req-generate`、`/req-complete`、`/req-review`、`/req-opsx` | 记录、探索、生成、完善、评审、转 OpenSpec | 除 explore 外是 | 否 |
| 缺陷治理 | `/bug-capture`、`/bug-explore`、`/bug-generate`、`/bug-complete`、`/bug-review`、`/bug-opsx` | 记录、分析、生成、完善、评审、转 OpenSpec | 除 explore 外是 | 否 |
| Sprint 治理 | `/sprint-propose`、`/sprint-explore`、`/sprint-apply`、`/sprint-archive` | 规划、分析、执行、归档 | 视命令而定 | 仅 apply |
| OpenSpec | `/opsx-explore`、`/opsx-propose`、`/opsx-apply`、`/opsx-archive` | 探索、提案、实现、归档 | 视命令而定 | 仅 apply |
| 项目基线 | `/initialize-project`、`/build-design-system`、`/build-api-standard`、`/build-test-framework` | 初始化或建立治理标准 | 是 | 否 |

## 条件启用

- 需求、缺陷、Sprint、OpenSpec 与项目基线默认启用。
- 用户明确禁用某一治理流程时，删除该流程命令、目录、强制规则与相关检查项，或标记为 `planned`。
- 未知命令不得伪造；记录为 `待确认`。
