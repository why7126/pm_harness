---
created_at: 2026-08-19 11:25:48
updated_at: 2026-08-19 11:25:48
---

# project-governance Delta

## ADDED Requirements

### Requirement: 治理决策记录

ProjectPmHarness SHALL provide a durable governance decision note convention for non-trivial governance changes that need long-term rationale beyond an execution report.

#### Scenario: 记录非平凡治理变更

- GIVEN 治理变更会影响规范、脚本、Skill、目录边界、模板能力或校验策略
- WHEN 用户确认该变更需要长期保留决策依据
- THEN 项目 SHALL 使用 `docs/decision-notes/` 记录问题、决策或提案、替代方案和后果

### Requirement: 文档事实源归属

ProjectPmHarness SHALL define document tiers so each durable fact has one owning source and other documents reference that source instead of duplicating long rules.

#### Scenario: 避免重复规则漂移

- GIVEN 同一治理事实需要出现在多个入口
- WHEN 该事实已有长期事实源
- THEN 其他入口 SHALL 使用链接或短路由引用该事实源，而不是复制整段规则

### Requirement: 治理检查聚合器

ProjectPmHarness SHALL provide a read-only governance check aggregate for commonly required root governance validations.

#### Scenario: 运行默认治理校验

- GIVEN 用户需要验证根项目治理资产
- WHEN 执行 `python scripts/run-governance-checks.py`
- THEN 脚本 SHALL 运行上下文预算、OpenSpec 语言和目录结构校验，并在任一失败时返回非零
