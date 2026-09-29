---
created_at: 2026-08-21 22:28:02
updated_at: 2026-08-21 22:28:02
---

# project-governance Delta

## ADDED Requirements

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
