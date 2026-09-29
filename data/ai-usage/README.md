---
purpose: AI Usage 本地事实源边界
content: 说明 command run 与 Sprint usage snapshot 的生成、默认 session 发现顺序和安全约束
created_at: 2026-08-31 09:13:31
updated_at: 2026-08-31 09:13:31
---

# AI Usage 本地事实源边界

`data/ai-usage/` 用于保存脱敏后的 command run 摘要、release command 摘要和 Sprint usage snapshot。目录内只允许保存聚合 token、模型调用、工具调用、关联 REQ/BUG/Change/Sprint/release 和安全摘要。

AI Usage hook 的 session 输入发现顺序：

1. 显式 `--session-jsonl <local-session.jsonl>`。
2. `AI_USAGE_SESSION_JSONL`。
3. `CODEX_SESSION_JSONL`。
4. `AI_USAGE_SESSIONS_DIR`。
5. 本机默认 Codex sessions 目录。

原始 session JSONL、本机绝对路径、prompt、system/developer instructions、完整工具输出、密钥、Cookie、Authorization header 和 `.env` 内容不得写入仓库。

常规 workflow hook 若无法自动发现可用 session，应返回 compact `usage_mode: unavailable` 与 `recommended_action`，不得阻断父命令；历史回溯、补账或精确归因仍应使用显式 session 或 manual map。
