---
created_at: 2026-08-27 00:04:20
updated_at: 2026-08-27 00:04:20
---

# project-governance Delta

## ADDED Requirements

### Requirement: BUG 评审 confirmed 根因门禁

ProjectPmHarness SHALL require confirmed root-cause evidence before approving a BUG review.

#### Scenario: approve 前根因未确认

- GIVEN BUG 的 `root-cause.md` 缺失、缺少 `root_cause_status` 或状态不是 `confirmed`
- WHEN 执行 `/bug-review <BUG-id>` 的默认 approve 路径
- THEN 系统 SHALL 阻断 approve，并提示先补齐 confirmed 根因证据或选择非 approve 评审结果

### Requirement: Sprint 选择与冻结门禁

ProjectPmHarness SHALL validate Sprint selection before creating or updating Sprint planning artifacts.

#### Scenario: 未指定 Sprint 且存在多个 active Sprint

- GIVEN `iterations/change/` 下存在两个或以上 active Sprint
- WHEN 执行 `/sprint-propose` 且未指定 Sprint ID
- THEN 系统 SHALL 阻断命令，并要求用户显式指定目标 Sprint

#### Scenario: 新建 Sprint 跳号

- GIVEN 当前已知最大 Sprint 编号为 `sprint-001`
- WHEN 用户请求新建 `sprint-003`
- THEN 系统 SHALL 阻断命令，并提示下一个允许编号为 `sprint-002`

### Requirement: 最终输出契约卫生校验

ProjectPmHarness SHALL validate existing command Final Output Contract sections for user-visible output hygiene.

#### Scenario: 技能残留旧占位模板

- GIVEN 命令 Skill 的 Final Output Contract 残留尖括号占位模板、通用示例或重复下一步确认反模式
- WHEN 执行 `python scripts/validate-agent-context-budget.py`
- THEN 系统 SHALL 返回非零，并输出对应 Skill 路径和问题摘要
