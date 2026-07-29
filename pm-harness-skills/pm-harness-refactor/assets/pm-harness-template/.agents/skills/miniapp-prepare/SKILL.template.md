---
name: "miniapp-prepare"
description: "小程序发布前准备：切生产、静态测试、生产接口 smoke、输出上传体验版清单"
---

# miniapp-prepare

Use this skill when the user asks `/miniapp-prepare` or wants to prepare the WeChat miniapp for trial/review/release.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；只读取小程序环境配置、生产发布相关规则和脚本。
- 测试和 smoke 输出使用摘要；失败时只展开关键错误。

## Must Read

```text
rules/coding.md
rules/testing.md
rules/security.md
rules/directory-structure.md
rules/agent-context-budget.md
```

按实际目录读取存在的文件：

```text
src/wechat-miniapp/README.md
src/miniapp/README.md
scripts/miniapp-env.py
```

## Gates

Prepare MUST be blocked unless:

- 小程序策略已切到 `prod`，或项目明确采用其它提审策略。
- 小程序 `project.private.config.json` 的 `setting.urlCheck` 已切到 `true`，或项目说明无需该文件。
- 小程序静态测试通过，或项目尚未接入测试且阻塞项已记录。
- 生产 API smoke 通过，或用户明确只做本地预检。

## Steps

1. 若 `scripts/miniapp-env.py` 存在，执行：

```bash
python scripts/miniapp-env.py prepare
```

2. 若脚本不存在，输出需要接入的 `miniapp-env.py` 能力清单，并继续执行可用的静态检查。
3. 如 sandbox 阻止测试缓存或外网 smoke，按审批规则重跑必要命令。
4. 输出微信开发者工具上传、公众平台设为体验版、手机删除旧体验版入口、重新扫码最新体验版二维码的 checklist。

## Output

报告门禁结果、当前策略、`urlCheck=true` 状态、测试命令、生产接口 smoke、人工 checklist、下一步 `/miniapp-confirm` 或 `/miniapp-restore`。
