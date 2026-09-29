---
name: "sprint-propose"
description: "提议并创建新 Sprint 迭代规划（四件套）"
---

# sprint-propose

Use this skill when the user asks to run `/sprint-propose` or create/update a Sprint plan.

## Context Budget Guardrails（MUST）

- Sprint 范围分析先读取候选 `trace.md` 与摘要，不得全量展开上一 Sprint 四件套、复盘库或所有 active changes。
- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 不要 `ls -R` 或全量 `cat iterations/** docs/knowledge-base/**`；先列清单，再分段读取。
- 复盘默认只读最近 1 份；只有 open 行动项跨 Sprint 复发或用户要求时读第 2 份。
- `best-practices/` 只读取候选 REQ/BUG/Change 标签命中的文件。
- 已存在 Sprint 时先读 `sprint.yaml` 和 `sprint.md` 的目标/Scope/知识库承接片段。
- 搜索候选项默认排除 `openspec/archive/**`；编号冲突只看目录名。
- 命令输出优先 `max_output_tokens <= 8000`。

## Product Data Observability Gate（MUST）

纳入 Sprint 的 REQ、BUG 或 Change 若涉及 API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装、App 请求封装或工作流治理，MUST 读取或确认其已引用 `docs/standards/product-data-collection-observability.md`，并在 Sprint 摘要或 trace 中保留 `product_data_collection_observability`、`affected_layers`、`reason` 和 `validation` 状态。若不适用，MUST 写明 N/A 或 `not_applicable` 原因。

## Input

- `sprint-xxx`：指定 Sprint ID。
- 自然语言目标：由 Agent 推导候选范围和编号。
- Flags：`--req`、`--bug`、`--change`、`--duration 2w`、`--dry-run`。

## Sprint ID Rules（MUST）

- Sprint ID MUST 使用 `sprint-xxx` 三位数字递增格式，例如 `sprint-022`。
- 命令在选择或创建 Sprint 前 MUST 运行：

```bash
python scripts/validate-sprint-selection.py [--sprint <sprint-id>]
```

- 当用户未指定 Sprint ID 且当前没有 `iterations/change/sprint-xxx/` active Sprint 时，MAY 自动创建下一个 Sprint。
- 当用户未指定 Sprint ID 且当前仅有一个 `iterations/change/sprint-xxx/` active Sprint 时，MUST 默认使用该 Sprint 作为当前 Sprint。
- 当用户未指定 Sprint ID 且当前存在两个或以上 active Sprint 时，MUST 阻断命令，并引导用户使用 `/sprint-propose --sprint <sprint-id>` 指定当前 Sprint。
- 自动编号 MUST 同时扫描 `iterations/archive/` 与 `iterations/change/` 下符合 `sprint-[0-9]{3}` 的目录和 `sprint.yaml:sprint_id`，取最大编号加一。
- 用户显式指定一个尚不存在的 Sprint 时，该 Sprint ID MUST 等于最大规范编号加一；不得跳号创建。
- 如果已存在一个 active Sprint，只有当前 Sprint 容量硬阻断或用户明确拆分范围时，才允许通过 `--sprint <next-sprint>` 创建下一个连续编号 Sprint。
- 如果已存在两个 active Sprint，MUST 禁止创建第三个 active Sprint；用户只能指定其中一个现有 active Sprint。
- 不得使用日期、主题词或混合命名创建 Sprint。

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
- 只能列入 `sprint.md`「延后项（待评审）」并提示 `/req-review` 或 `/bug-review`。

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
  - 输出硬提示：必须拆分 Sprint、移出低优先级项、替换范围，或使用 `/sprint-propose --sprint <next-sprint>` 创建下一个连续编号 Sprint 后重新规划。
  - `<next-sprint>` MUST 通过 `scripts/validate-sprint-selection.py --sprint <next-sprint>`，不得跳号。
- `capacity_person_days < estimated_person_days <= capacity_person_days * 1.2` 时 MAY 继续，但 MUST 写入容量风险、fix 缓冲影响和延后项建议。
- `estimated_person_days <= capacity_person_days` 时按既有 Review Gate、Readiness Gate 和 Capacity Gate 继续。

### Archived Sprint Freeze Gate（MUST）

- `/sprint-propose` MUST NOT 修改 `iterations/archive/<sprint-id>/` 或其关联 REQ/BUG/Change 的交付语义。
- 若用户指定已归档 Sprint 或目标 Issue/Change 已随所属 Sprint 归档，MUST 阻断普通规划写入，并引导将偏差作为新生命周期输入处理。
- 归档事实只允许由 `explore`、`*-explore`、`sprint-exps`、`release-*`、`image-*`、`upgrade-*` 读取或消费；敏感信息清理、归档路径残留或状态漂移修复必须走明确授权的治理命令。

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

对正式纳入 `iterations/change/<sprint-id>/` 四件套的 REQ/BUG/Change 更新：

```text
trace.md iteration: sprint-xxx
trace.md status: in_sprint
openspec/changes/<change>/trace.md（若存在）
```

`sprint.yaml` `status: planning` 已表示正式规划完成、尚未开始批量执行；它不是“未启动 Sprint”。`/sprint-propose` 成功后 MUST 通过 Workflow Sync 将纳入项置为 `in_sprint`，使后续 `/opsx-apply --sprint auto` 可直接解析该 planning Sprint。

## Output

报告 Sprint ID、状态、纳入 REQ/BUG/Change 数量、估算、知识库承接、容量门禁、四件套路径、下一步、待用户决策/处理。

若纳入范围存在已评审但尚未 Change 的 REQ/BUG，下一步输出真实可执行命令，且不在「待用户决策/处理」重复要求确认同一组命令。

正例：

```text
下一步：
- /req-opsx REQ-0123-upload-stage-trace-spans
- /bug-opsx BUG-0144-miniapp-usage-events-overreporting
待用户决策/处理：
- 无
```

若 Sprint 编号、容量策略或范围取舍尚未确定，下一步被用户决策阻塞。

正例：

```text
下一步：暂无可推进下一步
待用户决策/处理：
- 请选择目标 sprint-xxx，或确认是否创建下一编号 Sprint。
```

## Final Step — Workflow Sync（MUST）

Run:

```bash
python scripts/sync-workflow-status.py --event sprint.propose --sprint <sprint-id>
```

- Exit code MUST be `0`。
- MUST verify included REQ/BUG traces are updated to `status: in_sprint` and `iteration: <sprint-id>`。
- Print summary Workflow Sync Report；use `--output detail` only for debugging。
- Do not hand-edit workflow-sync marker blocks。
