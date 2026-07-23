---
name: "miniapp-confirm"
description: "记录小程序体验版或正式版验证确认结论"
---

# miniapp-confirm

Use this skill when the user asks `/miniapp-confirm` or wants to record trial/release verification results for the miniapp.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；只读取小程序环境配置、脚本和相关发布记录片段。
- 不记录敏感信息、微信会话密钥、Cookie、Authorization header、`.env` 内容或真实用户隐私。

## Input

Recommended flags:

```text
--channel trial|release
--version <version>
--result passed|blocked|follow_up
--notes <text>
```

## Steps

1. 确认渠道、版本和验证结果；缺失时询问用户。
2. 若 `scripts/miniapp-env.py` 存在，执行：

```bash
python scripts/miniapp-env.py confirm --channel <trial|release> --version <version> --result <passed|blocked|follow_up> --notes "<text>"
```

3. 若脚本不存在，输出可落入 `releases/<version>/release.json`、Sprint 验收报告或发布记录的安全摘要，并提示补齐确认记录脚本。

## Output

报告确认结论、验证范围、剩余风险和下一步 `/miniapp-restore`。
