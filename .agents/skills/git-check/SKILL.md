---
name: "git-check"
description: "推送前 Git 安全检测 - 检查 staged/tracked 文件中的真实环境文件、运行时数据、数据库文件、大文件、密钥、Token、连接串和本机绝对路径"
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-10 23:19:03
---

# git-check

Use this skill when the user asks to run `/git-check`, perform a pre-push safety check, or verify that repository changes do not contain secrets, real env files, runtime data, local databases, large artifacts, local absolute paths, or private data.

## Must Read

- `AGENTS.md`
- `rules/security.md`
- `rules/agent-context-budget.md`

## Command

Default:

```bash
python scripts/git-check.py
```

Deep scan:

```bash
python scripts/git-check.py --all
```

## Output Contract

- 有 error 时返回非 0，并输出脱敏后的 error 摘要和修复建议。
- 无 error 时返回 0；warning 需要人工复核但不阻断。
- 不输出真实密钥、Token、Cookie、Authorization header、数据库连接串、真实 env 行或本机绝对路径原文。

## Guardrails

- 不自动修改 `.gitignore`。
- 不自动 unstage。
- 不删除本地文件。
- 不读取或输出 ignore 且未 staged/tracked 的真实 `.env` 内容。

## Final Output Contract

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、生产实施确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、生产实施确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
