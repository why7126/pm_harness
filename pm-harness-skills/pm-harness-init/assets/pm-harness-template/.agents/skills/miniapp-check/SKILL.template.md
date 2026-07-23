---
name: "miniapp-check"
description: "检查微信小程序环境策略、运行入口同步和生产接口可访问性"
---

# miniapp-check

Use this skill when the user asks `/miniapp-check` or wants to verify miniapp environment configuration before preview, trial, review, or release.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；只读取小程序环境配置、脚本和测试片段。
- 生产 smoke 失败时输出关键状态码和 URL，不输出长响应体。

## Input

- Optional flags: `--smoke` to check production endpoints.

## Must Read

```text
rules/coding.md
rules/testing.md
rules/security.md
rules/agent-context-budget.md
```

按实际目录读取存在的文件：

```text
scripts/miniapp-env.py
src/wechat-miniapp/README.md
src/wechat-miniapp/project.private.config.json
src/miniapp/README.md
src/miniapp/project.private.config.json
```

## Steps

1. 若 `scripts/miniapp-env.py` 存在，优先执行：

```bash
python scripts/miniapp-env.py check --smoke
```

2. 若脚本不存在，检查小程序目录、环境配置、`project.private.config.json` 和 README，输出缺失的脚本接入项。
3. 执行静态测试（除非用户只要求快速查看）：

```bash
uv run pytest tests/test_miniapp_static.py
```

4. 报告当前策略、入口同步状态、`setting.urlCheck` 是否符合策略、生产接口 smoke 结果、合法域名和手机缓存检查提醒。

## Output

明确给出是否可继续上传体验版；若 blocked，给出最短修复路径。若策略为 `auto` 或 `dev` 且 `urlCheck=true`，优先通过 `/miniapp-env auto` 或 `/miniapp-env dev` 修复。
