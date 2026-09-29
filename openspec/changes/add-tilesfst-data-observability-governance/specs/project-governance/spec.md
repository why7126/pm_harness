---
created_at: 2026-08-27 00:26:26
updated_at: 2026-08-27 00:26:26
---

# project-governance Delta

## ADDED Requirements

### Requirement: 产品数据采集与链路观测标准

ProjectPmHarness SHALL provide a reusable governance standard for product data collection, request logs, Task Trace, endpoint request wrappers and workflow declarations.

#### Scenario: 数据采集相关变更需要统一事实源

- GIVEN a REQ, BUG, Sprint or OpenSpec Change touches API, DB, request logs, usage events, Task Trace, Web request wrappers, MiniApp request wrappers, App request wrappers or workflow governance
- WHEN the agent prepares or validates the governance artifact
- THEN the artifact SHALL reference `docs/standards/product-data-collection-observability.md`
- AND SHALL declare `product_data_collection_observability`, `affected_layers`, `reason` and `validation`

### Requirement: 产品数据采集观测硬门禁

ProjectPmHarness SHALL validate product data observability governance coverage before completing data-collection related workflow steps.

#### Scenario: 触达面缺少声明

- GIVEN a data-collection related Change contains API, DB, audit log, behavior event, Task Trace or endpoint wrapper scope
- WHEN `python scripts/validate-product-data-observability-gates.py --change <change-id>` runs
- THEN the validator SHALL return non-zero if the Change lacks `product_data_collection_observability`, `affected_layers`, `reason` or `validation`

#### Scenario: 明确不适用

- GIVEN a governance artifact contains data collection trigger terms only as routing or exclusion context
- WHEN the artifact declares N/A or `not_applicable` with a reason
- THEN the validator SHALL treat the declaration as explicit non-applicability rather than an omission

### Requirement: 工作流技能数据采集门禁

ProjectPmHarness SHALL require REQ, OpenSpec and Sprint workflow skills to check product data observability impact before writing final artifacts or closing workflow stages.

#### Scenario: REQ 到 Sprint 链路传播观测声明

- GIVEN a REQ, Change or Sprint item touches API, DB, audit logs, behavior events, Task Trace or endpoint request wrappers
- WHEN the agent runs req-generate, req-complete, req-review, req-opsx, opsx-propose, opsx-apply, opsx-modify, opsx-archive, sprint-propose, sprint-apply or sprint-archive
- THEN the skill SHALL require reading the standard
- AND SHALL preserve `product_data_collection_observability`, `affected_layers`, `reason` and `validation` or an explicit N/A / `not_applicable` reason
