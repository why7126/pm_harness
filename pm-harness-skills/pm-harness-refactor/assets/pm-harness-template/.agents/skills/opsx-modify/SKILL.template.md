---
name: "opsx-modify"
description: "验收返修：在 OpenSpec Change 已 opsx-apply、未 archive 前，根据验收反馈调整实现并同步文档、验证和 AI Usage"
---

# opsx-modify

Use this skill when the user asks `/opsx-modify <change-id|REQ-id|BUG-id> <修改内容>` or wants to adjust implementation after `/opsx-apply` during acceptance, before `/opsx-archive`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，优先摘要复用，不重复全量读取。
- 返修定位先读验收反馈、`tasks.md`、`trace.md`、相关 acceptance 摘要；不要全量重读 Issue、Sprint、archive 或 generated 文件。
- 大 diff 先用 `git diff --stat` / `git diff --name-only`；只展开手写源码、测试和本次文档片段。
- 命令输出优先 `max_output_tokens <= 8000`；测试失败只展开失败用例、关键栈和相关片段。

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

## Input

```text
/opsx-modify <change-id|REQ-id|BUG-id> <修改内容>
```

Examples:

```text
/opsx-modify add-login-page 登录按钮 hover 色和验收稿不一致，改成金色 token，并补截图验收说明
/opsx-modify REQ-0008-login-page 验收发现移动端标题溢出，修正响应式布局
```

## Scope

`/opsx-modify` 用于 **apply 后、archive 前** 的验收返修。

适用：

- 原验收项未满足。
- 原实现的 UI、API、数据、测试或文档存在偏差。
- 验收反馈仍属于当前 Change 的目标与边界。
- 需要补充二次验证证据和 AI Usage 统计。

不适用：

- 新增原需求未包含的功能。
- 改变新的 API / DB / 权限 / 部署 / 对象存储边界。
- 发现独立缺陷且影响范围超出当前 Change。
- 当前 Change 已 archive。

超出范围时 MUST stop，并建议走 `/req-capture`、`/bug-capture` 或新 OpenSpec Change。

## Must Read

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/coding.md
rules/testing.md
rules/security.md
rules/document-governance.md
rules/directory-structure.md
rules/requirement-management.md
rules/bug-management.md
rules/iterations-lifecycle.md
.agents/skills/workflow-sync/SKILL.md
```

Resolve target:

- If input is `REQ-*` / `BUG-*`, read its `trace.md` and resolve linked `openspec_changes[]`.
- If multiple active Changes match, ask user to choose.
- If target Change is archived, BLOCKED.

Then read focused snippets:

```text
openspec/changes/<change-id>/tasks.md
openspec/changes/<change-id>/trace.md（存在时）
openspec/changes/<change-id>/acceptance.md（存在时）
issues/requirements|bugs/**/<REQ-or-BUG>/acceptance.md
issues/requirements|bugs/**/<REQ-or-BUG>/trace.md
iterations/change|archive/<sprint>/acceptance-report.md
iterations/change|archive/<sprint>/sprint.yaml
```

Run preflight:

```bash
python scripts/sync-workflow-status.py --event opsx.modify --change <change-id> --sprint auto --dry-run
```

If sprint cannot resolve for a REQ/BUG-sourced Change, BLOCKED and ask to fix Sprint trace/scope first.

## Workflow

1. **Clarify Feedback**
   - Summarize the acceptance issue in 1-3 bullets.
   - Identify whether it is in-scope for the current Change.
   - Identify affected files and tests.

2. **Modify Implementation**
   - Make minimal scoped code changes.
   - Add or adjust tests when behavior changes.
   - Do not mark new feature scope as complete under this command.

3. **Update Documents**
   - Documentation update is a **MUST gate**, not optional bookkeeping. Before validation, decide whether the acceptance feedback changes any behavior, UI rule, validation rule, user-visible text, API/DB contract, release note, acceptance criterion, or archive-bound spec wording.
   - Update `openspec/changes/<change-id>/tasks.md` with a `## 验收返修记录` section if absent.
   - Update Change `trace.md` when present with feedback, adjustment, and validation summary.
   - If feedback changes or clarifies acceptance criteria, update the linked Issue `acceptance.md` or BUG acceptance/repro document, preserving frontmatter and refreshing `updated_at`.
   - If feedback changes or clarifies product behavior, UI/UE behavior, boundary, non-goal, validation strategy, or implementation decision while staying within the same Change scope, update the active Change docs such as `proposal.md`, `design.md`, `acceptance.md`, `test-plan.md`, or `implementation/` notes as applicable.
   - If feedback changes archive-bound capability wording, update `openspec/changes/<change-id>/specs/**/spec.md` delta so `/opsx-archive` will merge the corrected behavior into `openspec/specs/`.
   - If feedback changes Sprint-visible scope, acceptance evidence, release note, or user-visible behavior, update `iterations/change|archive/<sprint>/acceptance-report.md`, `sprint.md`, and/or `release-note.md` as applicable. Do not hand-edit workflow-sync marker blocks in `sprint.md`.
   - If feedback changes long-lived API, DB, deployment, compatibility, security, media, or product documentation, update the corresponding `docs/**` file required by `rules/document-governance.md`.
   - Update linked Issue `trace.md` through Workflow Sync rather than hand-editing marker blocks.
   - If docs/spec wording must change but capability boundary is unchanged, update the active Change docs; if boundary changes, BLOCKED and suggest `/req-capture`, `/bug-capture`, or a new OpenSpec Change.
   - Run focused documentation checks after edits: at minimum `openspec validate <change-id> --strict` when active Change docs/specs change, and `git diff --check -- <touched-docs>` for touched Markdown/spec files.

   Documentation decision matrix:

   | Feedback touches | MUST update |
   |---|---|
   | Acceptance wording, pass/fail criteria, or verification evidence | `openspec/changes/<change-id>/tasks.md`, Change `trace.md`, linked Issue `acceptance.md` if criteria changed, Sprint `acceptance-report.md` |
   | Product/UI behavior that should survive archive | Change `design.md` and/or `proposal.md`, `openspec/changes/<change-id>/specs/**/spec.md`, linked Issue `requirement.md` / BUG doc when applicable |
   | User-visible release behavior | Sprint `release-note.md` |
   | Sprint plan, scope notes, risk notes, or implementation notes | Sprint `sprint.md` outside workflow-sync marker blocks |
   | API, DB, deployment, environment, security, media, compatibility, or public product docs | Corresponding `docs/**` file per `rules/document-governance.md` |
   | Pure implementation-only bug with no behavior/spec/docs drift | Still update `tasks.md` + Change `trace.md`; explicitly record “无需更新其他文档” with reason |

4. **Validate**
   - Run focused tests/checks for touched areas.
   - Run broader checks when API / DB / UI / deployment / security boundary is touched.
   - Keep validation output summarized.

5. **Workflow Sync**

```bash
python scripts/sync-workflow-status.py --event opsx.modify --change <change-id> --sprint auto
```

- Exit code MUST be `0`.
- Print summary Workflow Sync Report.
- Do not hand-edit workflow-sync marker blocks.

6. **AI Usage（MUST）**

After successful workflow sync, run the post-command hook:

```bash
python scripts/extract-ai-usage.py \
  --post-command-hook \
  --workflow-event opsx.modify \
  --change <change-id> \
  --sprint <sprint-id|auto-resolved-id-if-known> \
  --json
```

Rules:

- If session JSONL is unavailable, report the compact `usage_mode: unavailable` summary and recommended action.
- Do not fail `/opsx-modify` solely because AI Usage session input is unavailable.
- Do not persist prompt text, raw session logs, tool outputs, secrets, `.env` content, cookies, tokens, or local absolute paths.

## Completion Output

Report:

```text
Change:
验收反馈:
调整内容:
文档更新:
文档未更新项与原因:
验证:
Workflow Sync:
AI Usage:
是否仍可 archive:
```

## Event

Workflow event: `opsx.modify`

This event means “验收返修已同步”，not first implementation and not archive.
