# project-governance Specification

## Purpose
Define stable governance behavior for ProjectPmHarness command workflows, review defaults, and lifecycle gates.
## Requirements
### Requirement: Review Commands Default To Approval

ProjectPmHarness SHALL treat no-flag `/req-review <REQ-id>` and `/bug-review <BUG-id>` invocations as approved review outcomes while preserving explicit flags for non-approval outcomes.

#### Scenario: REQ review without flag

- GIVEN a REQ is ready for review
- WHEN the user invokes `/req-review <REQ-id>` without `--reject` or `--defer`
- THEN the command SHALL produce an approved review result and update status to `approved`

#### Scenario: BUG review without flag

- GIVEN a BUG is ready for review
- WHEN the user invokes `/bug-review <BUG-id>` without `--reject`, `--defer`, or `--wont-fix`
- THEN the command SHALL produce an approved review result and update status to `approved`

#### Scenario: Explicit non-approval remains required

- GIVEN the intended review result is reject, defer, or won't-fix
- WHEN the user invokes the review command
- THEN the command SHALL require the corresponding explicit flag and SHALL NOT infer a non-approval outcome from missing flags

### Requirement: 版本升级路径治理

ProjectPmHarness SHALL provide a release upgrade path governance model that distinguishes target release facts from verified deployment upgrade paths.

#### Scenario: 生成升级计划

- GIVEN a release version has a `releases/<version>/release.json`
- WHEN an operator requests `/upgrade-plan --from <fresh|version> --to <version>`
- THEN the project SHALL generate a plan under `releases/<version>/upgrade-plans/` with support level, safe env diff summary, impact summary, steps, rollback, blockers, warnings, and evidence

#### Scenario: 禁止自动执行生产升级

- GIVEN an upgrade plan exists
- WHEN `/upgrade-plan` or `/upgrade-validate` runs
- THEN the command SHALL NOT automatically modify real env files, execute production upgrades, run write-type database maintenance, run DB restore, or perform object-storage write maintenance

### Requirement: 文档表达卫生审计

ProjectPmHarness SHALL provide a lightweight prose hygiene standard and validation entry for durable governance documents.

#### Scenario: 发现长期文档中的过程残留

- GIVEN a durable document under `docs/`, `rules/`, `.agents/skills/`, or `AGENTS.md`
- WHEN prose hygiene validation is run
- THEN the validator SHALL report likely session reasoning, temporary draft references, review conversation residue, unresolved local paths, and sensitive snippets without automatically rewriting the document

### Requirement: 最小相关验证矩阵

ProjectPmHarness SHALL define a command validation matrix that maps changed governance scope to the minimum relevant local checks.

#### Scenario: 选择验证范围

- GIVEN a command changes governance assets
- WHEN the command reaches validation
- THEN the agent SHALL choose checks based on diff scope and mandatory workflow gates instead of mechanically running unrelated full matrices

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

