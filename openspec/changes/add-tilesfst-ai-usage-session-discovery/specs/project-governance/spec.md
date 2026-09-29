---
created_at: 2026-08-31 09:13:31
updated_at: 2026-08-31 09:13:31
---

# project-governance Delta

## ADDED Requirements

### Requirement: AI Usage session 自动发现

ProjectPmHarness SHALL allow workflow AI Usage hooks to discover a local Codex session automatically before asking the operator for an explicit session file.

#### Scenario: Workflow hook 自动发现 session

- GIVEN a workflow command runs the AI Usage post-command hook without `--session-jsonl`
- WHEN `AI_USAGE_SESSION_JSONL` and `CODEX_SESSION_JSONL` are not set
- THEN the hook SHALL search `AI_USAGE_SESSIONS_DIR` and the local default Codex sessions directory for a matching session JSONL
- AND the hook SHALL return a compact summary with `session_input` describing whether discovery used explicit, env, auto or unavailable input

### Requirement: AI Usage 原始 session 安全边界

ProjectPmHarness SHALL store only redacted AI usage facts in repository data files.

#### Scenario: Session input unavailable

- GIVEN the hook cannot find a suitable session
- WHEN a normal workflow command completes
- THEN the hook SHALL return `usage_mode: unavailable` with a recommended action
- AND the parent workflow command SHALL NOT fail only because local session input is unavailable
- AND raw session JSONL, local absolute paths, prompts, system or developer instructions, secrets and full tool outputs SHALL NOT be persisted
