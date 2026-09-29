---
created_at: 2026-08-21 13:16:11
updated_at: 2026-08-21 13:16:11
---

# project-governance Delta

## ADDED Requirements

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
