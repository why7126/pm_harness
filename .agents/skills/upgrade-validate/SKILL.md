---
name: "upgrade-validate"
description: "校验版本部署升级与回滚计划"
---

# upgrade-validate

Use this skill when the user asks `/upgrade-validate --plan <path>` or wants to validate a generated upgrade / rollback plan.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接。
- 只读取指定 plan、目标 release 和必要镜像/部署证据。
- 校验成功默认输出摘要；失败时只展开 blocker/warning 和修复命令。
- 不输出真实 `.env`、密钥、连接串、Cookie、Authorization header、本机绝对路径或真实客户数据。

## Must Read

```text
AGENTS.md
rules/release.md（脚手架仓库中读取 pm-harness/rules/release.md）
rules/environment.md（脚手架仓库中读取 pm-harness/rules/environment.md）
rules/database.md（脚手架仓库中读取 pm-harness/rules/database.md）
rules/security.md
<plan path>
```

## Command

```bash
python scripts/validate-release-upgrade.py validate-plan --plan <path>
```

## Boundaries

- MUST NOT 自动执行生产升级。
- MUST NOT 自动修改真实 env。
- MUST NOT 自动执行 DB restore、写入型 migration 或对象存储维护任务。
- MUST NOT 将 `cross-version-upgrade-requires-manual-review` 解释为已支持跨版本升级。

## Output

报告 plan path、from version、to version、support level、blocker/warning 数、校验结果、下一步和待用户决策/处理。

当 `support_level=cross-version-upgrade-requires-manual-review` 时，输出必须提醒人工复核中间版本 release 事实、env diff、DB drift/smoke、对象存储影响和回滚证据。

## Final Output Contract（MUST）

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、生产实施确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、生产实施确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
