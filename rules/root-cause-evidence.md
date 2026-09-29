---
purpose: 证据化根因分析治理
content: 根因状态、证据链、人工补证和校验边界
created_at: 2026-08-21 08:24:48
updated_at: 2026-08-27 00:04:20
---

# 证据化根因分析治理

## 根因状态

问题排查、BUG 完善、实现返修和效果不如预期时，MUST 区分根因确定性：

| 状态 | 含义 | 输出要求 |
|---|---|---|
| `unknown` | 尚无可定位线索 | 说明缺少什么证据，并给出补证步骤 |
| `hypothesis` | 只有初步假设 | 标明推测依据和待验证点 |
| `probable` | 多项证据指向同一原因，但仍缺闭环验证 | 列出证据链和剩余验证 |
| `confirmed` | 已有可定位、可复核、可回扣的证据闭环 | 写明证据入口、触发条件、修复或处置关系 |

无证据或证据不足时，MUST NOT 把根因写成 `confirmed`。

## 证据链

根因证据 SHOULD 包含：

- 触发条件或复现步骤。
- 日志、错误输出、截图、测试失败、代码位置、配置差异或用户补证摘要。
- 证据时间、来源和脱敏说明。
- 根因与处置动作的对应关系。

证据不得包含真实密钥、真实客户数据、未脱敏日志、本机绝对路径、真实 `.env` 内容或隐私截图原文。

## 人工补证

当 Agent 无法直接取得证据时，必须输出人工补证步骤，而不是继续猜测。补证步骤 SHOULD 包含：

- 要执行的操作或要观察的页面/状态。
- 需要收集的日志、截图、请求、响应或测试结果。
- 脱敏要求。
- 收到补证后如何判断根因状态。

## 命令接入

- `/explore`、`/bug-explore`、`/bug-complete`、`/opsx-apply`、`/opsx-modify` 涉及根因判断时 MUST 遵守本规则。
- `/bug-review` 默认 approve 或显式 `--approve` 前 MUST 运行 `python scripts/validate-root-cause-evidence.py --bug <BUG-id> --require-confirmed`；未达到 `root_cause_status: confirmed` 或 confirmed 缺证据链时必须阻断 approve。
- BUG 来源 Change 的 `design.md`、`trace.md`、`root-cause.md` 或验收返修记录中出现根因结论时 SHOULD 写明根因状态。
- `/opsx-archive` 前如仍为 `unknown` 或 `hypothesis`，必须说明为何不阻断归档，或转为新的 BUG/REQ 跟进。
