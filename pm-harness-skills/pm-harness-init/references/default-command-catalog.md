# 默认命令目录

## 使用规则

- 生成 Agent 技能前必须完整读取本文档。
- 所有默认命令只在 `.agents/skills/<command-name>/SKILL.md` 中维护。
- 命令中的产品名、路径、示例业务和技术栈必须参数化；不得保留来源项目业务信息。

| 命令族 | 默认命令 | 阶段/作用 | 是否生成文档 | 是否生成代码 |
|---|---|---|---:|---:|
| 综合捕获 | `/capture` | 未分类反馈的需求/BUG 分析、拆分与路由捕获 | 是 | 否 |
| 需求治理 | `/req-capture`、`/req-explore`、`/req-generate`、`/req-complete`、`/req-review`、`/req-opsx` | 记录/必要拆分、探索、生成、完善、评审、转 OpenSpec | 除 explore 外是 | 否 |
| 缺陷治理 | `/bug-capture`、`/bug-explore`、`/bug-generate`、`/bug-complete`、`/bug-review`、`/bug-opsx` | 记录/必要拆分、分析、生成、完善、评审、转 OpenSpec | 除 explore 外是 | 否 |
| Sprint 治理 | `/sprint-propose`、`/sprint-explore`、`/sprint-apply`、`/sprint-exps`、`/sprint-archive` | 规划、分析、执行、经验沉淀、归档 | 视命令而定 | 仅 apply |
| OpenSpec | `/opsx-explore`、`/opsx-propose`、`/opsx-apply`、`/opsx-archive` | 探索、提案、实现、归档 | 视命令而定 | 仅 apply |
| 小程序发布辅助 | `/miniapp-env`、`/miniapp-check`、`/miniapp-prepare`、`/miniapp-confirm`、`/miniapp-restore` | 切换环境、发布前检查、体验/正式验证确认、发布后恢复 | 是 | 否 |
| 发布治理 | `/release-propose`、`/release-prepare`、`/release-publish` | 创建产品版本发布对象、执行发布门禁、生成/确认公告 | 是 | 否 |
| 项目基线 | `/initialize-project`、`/build-design-system`、`/build-api-standard`、`/build-test-framework` | 初始化或建立治理标准 | 是 | 否 |

## 条件启用

- 综合捕获、需求、缺陷、Sprint、OpenSpec、小程序发布辅助、发布治理与项目基线默认启用。
- 用户明确禁用某一治理流程时，删除该流程命令、目录、强制规则与相关检查项，或标记为 `planned`。
- 未知命令不得伪造；记录为 `待确认`。
- 需求或缺陷未完成评审、评审未通过或状态不是 `approved`/`in_sprint` 时，MUST 停止在评审门禁：不得 `/req-opsx` 或 `/bug-opsx`，不得 `/sprint-apply` 或等价开发，也不得写入 Sprint 规划文件。
- `/sprint-propose` 遇到未评审 REQ/BUG 时，只能在命令输出中列为 Blocked/Deferred 并提示评审；不得把这些条目写入 `iterations/<sprint-id>/sprint.yaml`、`sprint.md`、`release-note.md` 或 `acceptance-report.md`。

## Workflow Sync 钩子

除 `*-explore` 和项目基线命令外，`/capture` 以及所有 `req-*`、`bug-*`、`sprint-*`、`opsx-*` 命令末尾必须保留 `Final Step — Workflow Sync (MUST)`，并调用：

```bash
python scripts/sync-workflow-status.py --event <event> [--req REQ-xxxx] [--bug BUG-xxxx] [--change change-id] [--sprint sprint-xxx|auto]
```

`/opsx-archive` 与 `/sprint-archive` 的 Final Step 必须额外运行：

```bash
python scripts/promote-issue-stage.py --to archive [--change change-id] [--sprint sprint-xxx] --reason "<event>"
```

新增或修改命令技能时，必须在 `.agents/skills/<command-name>/SKILL.md` 中同步该 Final Step。

## Knowledge Base 复用钩子

以下命令必须保留 knowledge-base 读取和落地门禁：

- `/sprint-propose`：读取 `docs/knowledge-base/README.md`、最近 Sprint 复盘、`open`/`in_sprint` 行动项和相关 best-practices，并写入 Sprint「知识库承接项」。
- `/req-complete`：读取相关 best-practices / incidents，并把适用项写入 `acceptance.md` checklist。
- `/opsx-apply`、`/sprint-apply`：实现前输出 Knowledge Gate，列出已读取条目、适用约束和不适用原因。

新增或修改命令技能时，必须在 `.agents/skills/<command-name>/SKILL.md` 中同步 knowledge-base gate。
