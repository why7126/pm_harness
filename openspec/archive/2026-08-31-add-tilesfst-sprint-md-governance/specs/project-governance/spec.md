---
created_at: 2026-08-27 01:02:22
updated_at: 2026-08-27 01:02:22
---

# project-governance Delta

## ADDED Requirements

### Requirement: sprint.md Scope 合同

ProjectPmHarness SHALL keep `sprint.md` as a user-readable view derived from `sprint.yaml` formal scope.

#### Scenario: Sprint 范围出现在用户可读目标和 Scope

- GIVEN `sprint.yaml` lists a REQ, BUG or pure Change in formal scope
- WHEN Sprint documentation is generated, updated or validated
- THEN `sprint.md` SHALL contain the item in the Sprint target id list
- AND `sprint.md` `## 2. Scope` SHALL use the six-column main table `类型 | 编号 | 标题 | 状态 | 估算 | 说明`
- AND Workflow Sync grouped tables SHALL include the same formal scope

### Requirement: Sprint Scope 校验门禁

ProjectPmHarness SHALL validate `sprint.md` Scope against `sprint.yaml` before completing Sprint planning or Sprint governance updates.

#### Scenario: Scope 主表缺失 Change

- GIVEN `sprint.yaml` contains `add-example-governance` in `changes[]`
- WHEN `python scripts/validate-sprint-scope.py <sprint-id> --item add-example-governance` runs
- THEN the validator SHALL return non-zero if `sprint.md` target id list, main Scope table or Workflow Sync changes table misses the Change

### Requirement: Sprint 追加范围脚本

ProjectPmHarness SHALL use a deterministic script to append REQ, BUG or Change scope to an existing Sprint machine source.

#### Scenario: 追加纯治理 Change

- GIVEN an active Sprint already exists
- WHEN a governance Change must be added to the Sprint
- THEN `scripts/add-sprint-scope-item.py` SHALL update `sprint.yaml` machine scope before Workflow Sync refreshes Markdown views

### Requirement: Sprint 收口 readiness

ProjectPmHarness SHALL block Sprint close when Sprint four-piece documents or scoped Issue documents contain stale intermediate state.

#### Scenario: stale sprint.md wording remains before archive

- GIVEN a scoped Change is archived
- WHEN Sprint archive readiness runs
- THEN stale text such as pending apply, pending archive, legacy archive path or unresolved acceptance SHALL block close-out until reconciled

### Requirement: Sprint Fact Sheet read-first

ProjectPmHarness SHALL use a compact Sprint Fact Sheet before reading detailed Sprint, Issue or Change documents during retrospectives.

#### Scenario: Sprint 复盘需要证据

- GIVEN a Sprint has multiple scoped Changes
- WHEN `/sprint-exps` prepares retrospective input
- THEN it SHALL read Fact Sheet summary first
- AND only read detailed source snippets when warnings, blockers or evidence hints require detail
