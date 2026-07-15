---
name: "source-command-sprint-propose"
description: "提议并创建新 Sprint 迭代规划（四件套）"
---

# source-command-sprint-propose

Use this skill when the user asks to run `/sprint-propose` or create/update a Sprint plan.

## Context Budget Guardrails（MUST）

- Sprint 范围分析先读取候选 `trace.md` 与摘要，不得全量展开上一 Sprint 四件套、复盘库或所有 active changes。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 不要 `ls -R` 或全量 `cat iterations/** docs/knowledge-base/**`；先列清单，再分段读取。
- 复盘默认只读最近 1 份；只有 open 行动项跨 Sprint 复发或用户要求时读第 2 份。
- `best-practices/` 只读取候选 REQ/BUG/Change 标签命中的文件。
- 已存在 Sprint 时先读 `sprint.yaml` 和 `sprint.md` 的目标/Scope/知识库承接片段。
- 搜索候选项默认排除 `openspec/changes/archive/**`；编号冲突只看目录名。
- 命令输出优先 `max_output_tokens <= 8000`。

## Input

- `sprint-xxx`：指定 Sprint ID。
- 自然语言目标：由 Agent 推导候选范围和编号。
- Flags：`--req`、`--bug`、`--change`、`--duration 2w`、`--dry-run`。

## Must Read

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/document-governance.md
rules/requirement-management.md
rules/bug-management.md
rules/directory-structure.md
rules/iterations-lifecycle.md
.agents/skills/workflow-sync/SKILL.md
docs/knowledge-base/README.md（存在时）
```

按候选范围分段读取：

```text
project.yaml（容量，若存在）
issues/requirements/{plan,review,archive}/<REQ>/trace.md + requirement/acceptance 摘要
issues/bugs/{plan,review,archive}/<BUG>/trace.md + bug/root-cause/acceptance 摘要
openspec/changes/<change>/proposal.md + tasks.md 摘要
iterations/change|archive/<sprint>/sprint.yaml（编号/冲突）
docs/knowledge-base/retrospectives/<latest>-retrospective.md（最近复盘）
docs/knowledge-base/best-practices/<matched>.md（按标签）
```

## Gates

### Review Gate（MUST）

纳入 Sprint 正式规划前，REQ/BUG status MUST 为 `approved` 或 `in_sprint`。

未评审条目：

- 不得写入 `sprint.yaml` 的 `requirements[]` / `bugs[]`。
- 不得写入 Sprint 目标、Scope、里程碑、工作量合计、release、acceptance 正式范围。
- 不得更新 `trace.md` `iteration`。
- 只能列入 `sprint.md`「延后项（待评审）」并提示 `/req-review` 或 `/bug-review --approve`。

### Readiness Gate

| 类型 | Ready 条件 | Not Ready 处理 |
|---|---|---|
| REQ | `requirement.md`、`acceptance.md`、`trace.md` 齐全且 approved/in_sprint | 延后并建议 `/req-complete` 或 `/req-review` |
| BUG | `bug.md`、`root-cause.md`、`acceptance.md`、`trace.md` 齐全且 approved/in_sprint | 延后并建议 `/bug-complete` 或 `/bug-review` |
| Change | `proposal.md`、`design.md`、`tasks.md` 存在且未 archived | 缺失时提示 `/req-opsx` 或 `/bug-opsx` |

### Capacity Gate

- 优先级：P0 BUG > P0 REQ > P1 > P2。
- 估算：XS=0.5、S=1、M=3、L=5、XL=8、XXL=13 人天。
- add-* 主能力 SHOULD <= 6。
- fix 缓冲 SHOULD >= 30% SP/人天。
- 必须在生成正式四件套或更新 REQ/BUG/Change trace 前计算：
  `capacity_usage = estimated_person_days / capacity_person_days`。
- 若容量或估算缺失导致无法计算，MUST 先补齐输入；不得默认通过。
- `estimated_person_days > capacity_person_days * 1.2` 时 MUST 硬阻断正式规划：
  - 不得生成 `iterations/change/<sprint>/` 四件套。
  - 不得更新 `trace.md` 的 `iteration` 或 Change trace。
  - 输出硬提示：必须拆分 Sprint、移出低优先级项或替换范围后重新运行 `/sprint-propose`。
- `capacity_person_days < estimated_person_days <= capacity_person_days * 1.2` 时 MAY 继续，但 MUST 写入容量风险、fix 缓冲影响和延后项建议。
- `estimated_person_days <= capacity_person_days` 时按既有 Review Gate、Readiness Gate 和 Capacity Gate 继续。

## Knowledge Intake

- 读取最近 Sprint 复盘，提取 open 行动项并写入 §知识库承接。
- 按范围标签选择 best-practices：`admin-list`、`admin-form`、`admin-modal`、`media-upload`。
- `sprint.md` 必须包含 §横切预防清单，列出适用 best-practices 与验收 gate 摘要。

## Artifacts（非 `--dry-run` MUST）

目录：`iterations/change/sprint-xxx/`

```text
sprint.yaml
sprint.md
release-note.md
acceptance-report.md
```

`sprint.yaml` MUST 包含：

```yaml
sprint_id: sprint-xxx
status: planning
lifecycle_stage: change
start_date: YYYY-MM-DD HH:mm:ss
end_date: YYYY-MM-DD HH:mm:ss
capacity: { developers: <int>, testers: <int> }
requirements: []
bugs: []
changes: []
estimated_story_points: <number>
estimated_person_days: <number>
```

`sprint.md` MUST 包含：目标、Scope、工作量、fix 缓冲、里程碑、风险、知识库承接、横切预防清单、依赖 ASCII 树、发布计划、关联文档。

Markdown frontmatter MUST 含 `created_at`、`updated_at`；更新只改 `updated_at`。

## Trace Updates

对纳入的 REQ/BUG/Change 更新：

```text
trace.md iteration: sprint-xxx
openspec/changes/<change>/trace.md（若存在）
```

## Output

报告 Sprint ID、状态、纳入 REQ/BUG/Change 数量、估算、知识库承接、容量门禁、四件套路径、下一步。

## Final Step — Workflow Sync（MUST）

Run:

```bash
python scripts/sync-workflow-status.py --event sprint.propose --sprint <sprint-id>
```

- Exit code MUST be `0`。
- Print summary Workflow Sync Report；use `--output detail` only for debugging。
- Do not hand-edit workflow-sync marker blocks。
