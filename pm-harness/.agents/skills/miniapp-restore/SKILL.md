---
name: "miniapp-restore"
description: "发布后恢复微信小程序默认环境策略"
---

# miniapp-restore

Use this skill when the user asks `/miniapp-restore` or wants to restore the miniapp environment after trial/release verification.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；只读取小程序环境配置、脚本和静态测试。

## Input

- Optional `--strategy dev|prod|auto`；默认恢复为 `auto`。
- 恢复为 `auto` 或 `dev` 时 SHOULD 同步关闭小程序 `project.private.config.json` 的 `setting.urlCheck`，避免开发版本地 HTTP API 被微信开发者工具拦截。

## Steps

1. 若 `scripts/miniapp-env.py` 存在，执行：

```bash
python scripts/miniapp-env.py restore --strategy auto
```

2. 执行可用的小程序静态测试，例如：

```bash
uv run pytest tests/test_miniapp_static.py
```

3. 若脚本或测试不存在，记录缺口并给出接入建议，不手写散落环境配置。
4. 输出恢复后的策略摘要、`project.private.config.json setting.urlCheck` 和测试结果。

## Output

说明恢复后的策略、修改文件、测试结果、开发者工具是否需要重新编译，以及是否仍需要人工上传小程序。
