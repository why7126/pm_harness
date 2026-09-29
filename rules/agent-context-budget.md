---
purpose: Agent 上下文预算治理
content: 读取范围、搜索排除、大输出处理和跨项目学习顺序
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-31 09:13:31
---

# Agent 上下文预算治理

## 默认策略

- 先定位，再摘要，再片段读取。
- 同一会话已读且无变更的规则和 Skill 文件，用摘要承接，不重复全量读取。
- 大范围搜索默认排除依赖、构建产物、运行时数据、历史归档和 generated 文件。
- 长脚本、大 diff、测试日志和 Workflow Sync 输出只报告摘要、命中数或关键错误片段。

## spec-study 日志优先学习

跨项目学习时，如果学习对象存在 `docs/spec-logs/CHANGELOG.md`，MUST 优先按以下顺序学习：

```text
日志索引 -> 相关单次 study/governance 日志 -> 当前真实治理资产 -> 必要脚本或配置片段
```

日志索引只作为入口地图和历史背景，不能替代当前资产事实源。最终候选项必须横向校验项目入口、规则、Agent 能力、脚本和部署边界。

## 引导式反馈

命令需要用户选择、确认、补充信息或处理阻塞时，SHOULD 提供结构化选项、推荐项和可补充说明。每轮聚焦 1-3 个关键决策，避免把多个不相关开放问题堆给用户。

## 执行链路复盘

Workflow 命令完成后 MUST 输出执行链路复盘，并且状态必须基于校验、脚本输出、文件证据、日志、截图、验收记录或用户补证，不得凭感觉判断。

复盘字段固定为：

```text
执行链路复盘：
- 链路状态：正常 / warning / blocked
- 问题证据：无 / <脚本输出、文件路径、校验报告、日志摘要或用户证据>
- 规范优化建议：无明显优化点 / <建议命令或 capture 文案>
- follow-up 状态：未自动创建 Issue/Change
```

发现可优化点时，默认只输出建议命令或标准 capture 文案。除非用户明确授权自动 capture，否则不得自动创建 follow-up REQ/BUG。

## AI Usage Session 发现

常规 workflow 命令的 AI Usage hook SHOULD 优先自动发现本地 session，发现顺序为显式 `--session-jsonl`、`AI_USAGE_SESSION_JSONL`、`CODEX_SESSION_JSONL`、`AI_USAGE_SESSIONS_DIR`、本机默认 Codex sessions 目录。自动发现失败时，输出 compact `usage_mode: unavailable` 与 `recommended_action`，不得仅因缺少本地 session 阻断父命令。

AI Usage 输出只能包含脱敏聚合摘要、关联对象、`session_input` 类型和 warning 计数，不得输出原始 session JSONL、本机绝对路径、prompt、system/developer instructions、完整工具输出、密钥、Cookie、Authorization header 或 `.env` 内容。

## 最终输出契约卫生

命令型 Skill 若包含 `Final Output Contract`，MUST 使用真实结果输出规则，不得保留可被原样输出的尖括号模板、通用 BUG 示例、重复确认下一步命令或 `MUST/SHOULD` 规范语气示例。

`python scripts/validate-agent-context-budget.py` MUST 检查已有 Final Output Contract：

- 必须说明不得输出规则文本、尖括号占位符、规范语气和无关通用示例。
- 必须包含“下一步”和“待用户决策/处理”的三态判定。
- 已在“下一步”给出的命令或动作，不得在“待用户决策/处理”中重复要求确认。
