---
name: "upgrade-plan"
description: "生成版本首次部署、相邻升级或跨版本升级与回滚计划"
---

# upgrade-plan

Use this skill when the user asks `/upgrade-plan --from <fresh|version> --to <version>` or wants to generate a deployment upgrade / rollback plan.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接。
- 从 `releases/<to-version>/release.json`、目标 `image-manifest.json` 和指定升级计划开始，只按 `from_version` 与 `to_version` 定位必要 release 目录。
- 跨版本分析先列版本范围和影响摘要，不默认全量展开所有历史 release、OpenSpec archive、生成物、大日志或完整 manifest。
- 输出只展示 compact summary，不打印完整 env、真实 `.env`、密钥、连接串、Cookie、Authorization header、本机绝对路径或真实客户数据。

## Must Read

```text
AGENTS.md
rules/release.md（脚手架仓库中读取 pm-harness/rules/release.md）
rules/environment.md（脚手架仓库中读取 pm-harness/rules/environment.md）
rules/database.md（脚手架仓库中读取 pm-harness/rules/database.md）
rules/security.md
docs/02-deployment.md（脚手架仓库中读取 pm-harness/docs/02-deployment.md）
docs/08-production-image-release.md（存在时）
releases/<to-version>/release.json
releases/<to-version>/image-manifest.json（若存在）
```

## Command

```bash
python scripts/validate-release-upgrade.py plan --from <fresh|version> --to <version>
python scripts/validate-release-upgrade.py validate-plan --plan releases/<version>/upgrade-plans/<from>-to-<version>.json
```

## Boundaries

- MUST NOT 自动执行生产升级。
- MUST NOT 自动修改真实生产 env。
- MUST NOT 自动执行数据库写入迁移、DB restore 或对象存储写入维护任务。
- MUST NOT 为首次部署、相邻升级、跨版本升级构建不同业务镜像；同一目标版本复用同一份 image manifest。
- MUST NOT 把真实 env 值、密钥、连接串、Cookie、Authorization header、本机绝对路径或客户数据写入 plan。

## Output

报告 from version、to version、support level、source confidence、blocker/warning 数、plan path、validate result、下一步和待用户决策/处理。

下一步通常为：

```text
/upgrade-validate --plan releases/<version>/upgrade-plans/<from>-to-<version>.json
```

若计划已校验通过且需要实施，提示人工按计划执行；不得自动实施。

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
