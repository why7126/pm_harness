---
name: "bug-review"
description: "缺陷评审 - 确认是否修复；仅 approved 可 bug-opsx 与进 Sprint"
---

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 不要默认 `cat rules/*.md`、`cat AGENTS.md openspec/project.md rules/...` 或读取整目录；按本命令 Step 0 列表读取必要文件，已在同一会话读取过且无变更时用摘要承接。
- 检索先用 `rg -l` / `rg --files` 定位文件，再用 `sed -n '<start>,<end>p'` 或 `nl -ba ... | sed -n` 读取必要片段。
- 大范围 `rg` MUST 限制目录与输出：优先加 `--glob '!openspec/archive/**' --glob '!**/node_modules/**' --glob '!**/.git/**'`；只有追溯历史归档时才放开 archive，并说明原因。
- 对 Harness / 模板工程 / agent 资产目录执行搜索时，默认排除 `pm-harness*/**`、`**/assets/**`、历史/外部 agent 目录（如 `.claude/**`、`.kiro/**`、`.opencode/**`）；除非当前任务明确要求分析这些目录。
- 命令输出优先控制在 `max_output_tokens <= 8000`；预期超出时先输出文件清单或命中计数，再分段读取。
- 不重复读取同一大文件集合；若需要再次确认，优先读取变更片段、`git diff -- <file>` 或具体 frontmatter/status 字段。

# bug-review

Use this skill when the user asks to run the migrated source command `bug-review`.

## Command Template

**Input**：`BUG-xxxx`

Flags：`--approve` | `--reject` | `--defer` | `--wont-fix`

默认：无 flag 等同 `--approve`；`--approve` 作为兼容显式写法继续支持。`--reject`、`--defer`、`--wont-fix` 必须显式提供。

**Output**：`review.md`；status → `approved` | `rejected` | `deferred` | `wont_fix`

## Step — 根因 confirmed 门禁（MUST，默认 approve 或 `--approve` 时）

Read `rules/root-cause-evidence.md`。

默认 approve 或显式 `--approve` 时，MUST 在写入 `review.md`、状态变更和目录迁移前运行：

```bash
python scripts/validate-root-cause-evidence.py --bug <BUG-id> --require-confirmed
```

- Exit code MUST be `0`；若失败，MUST 停止 approve。
- `root_cause_status` MUST 为 `confirmed`；`unknown`、`hypothesis`、`probable`、缺少 `root-cause.md` 或缺少 `root_cause_status` 均为 blocker。
- confirmed 根因必须包含可定位证据链；缺证据时先 `/bug-complete <BUG-id>` 补齐，或显式选择 `--defer`、`--reject`、`--wont-fix`。
- `--reject`、`--defer`、`--wont-fix` 不要求通过 confirmed 门禁，但评审记录 MUST 说明非 approve 依据。

## Step — 目录迁移（MUST，默认 approve 或 `--approve` 时）

Read `rules/issues-lifecycle.md`。

| Flag | 迁移 |
|------|------|
| 无 flag / `--approve` | `plan/` -> `review/` |
| `--reject` / `--defer` / `--wont-fix` | **跳过**（保留 `plan/`） |

默认 approve 或显式 `--approve` 时 **MUST** 在 Workflow Sync **之前**运行：

```bash
python scripts/promote-issue-stage.py --bug <BUG-id> --to review --reason "/bug-review"
```

- Exit code **MUST** be `0`（已在 `review/` 时可 no-op）。
- 打印脚本 stdout（迁移路径、引用更新计数）。

## 评审清单

- [ ] `root_cause_status: confirmed` 且证据链可定位
- [ ] 严重等级合理
- [ ] 回归验收明确
- [ ] 是否需 hotfix 路径

## 门禁

**仅 `approved`** → 先 `/sprint-propose` 纳入 Sprint，再 `/bug-opsx` 创建修复 Change（P0 BUG 优先）

## Next

`/sprint-propose sprint-xxx --bug BUG-xxxx`

若目标 Sprint、修复优先级或容量尚未确定，最终输出 MUST 在「待用户决策/处理」中明确列出。

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event bug.review --bug <BUG-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- Print the summary **Workflow Sync Report** to the user; use `--output detail` only for debugging.
- Confirm the summary includes Issue subdocument checked/updated counts when applicable; `bug.md` and review-related status fields must not conflict with `trace.md`.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).

## Final Output Contract（MUST）

命令结束前，最终回复必须包含面向用户的真实结果，不得输出本段规则、尖括号占位符、MUST/SHOULD 规范语句或与当前命令无关的通用示例。

输出必须包含两项：

- `下一步`：写真实、可复制的下一条命令；若当前没有可推进动作，写“暂无可推进下一步”。
- `待用户决策/处理`：没有额外人工事项时写“无”；否则只列具体的缺失输入、范围/策略选择、证据补充、验收确认、发布确认、生产实施确认、阻塞项或人工处理事项。

输出判定：

- 有唯一可执行下一步时，`下一步` 写真实命令；若无额外人工事项，`待用户决策/处理` 写“无”。
- 下一步被用户选择、补证、验收、发布确认、生产实施确认或阻塞项卡住时，`下一步` 写“暂无可推进下一步”，并在 `待用户决策/处理` 列出具体阻塞事项。
- 已有下一步且仍有额外人工事项时，`待用户决策/处理` 只列命令之外的事项，不得重复 `下一步` 中的命令或动作。
- REQ 链路使用完整原始 `REQ-*`；BUG 链路使用完整原始 `BUG-*`；非 REQ/BUG 的直接 Change 才使用真实 Change ID。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
