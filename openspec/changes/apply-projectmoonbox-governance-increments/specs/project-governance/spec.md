---
created_at: 2026-08-21 08:24:48
updated_at: 2026-08-21 08:24:48
---

# project-governance Delta

## ADDED Requirements

### Requirement: 证据化根因分析

ProjectPmHarness SHALL distinguish root-cause certainty levels and require evidence before treating a root cause as confirmed.

#### Scenario: 证据不足时不确认根因

- GIVEN Agent is handling exploration, BUG completion, implementation, or acceptance rework
- WHEN root-cause evidence is missing or only inferred
- THEN Agent SHALL mark the cause as `unknown`, `hypothesis`, or `probable` and provide manual evidence collection steps instead of claiming a confirmed cause

### Requirement: 命令执行链路复盘

ProjectPmHarness SHALL require workflow commands to report execution status, evidence, governance improvement suggestions, and follow-up creation status.

#### Scenario: workflow 命令完成

- GIVEN a workflow command changed or checked REQ, BUG, Sprint, OpenSpec, release, image, usage docs, or governance state
- WHEN the command finishes
- THEN the final output SHALL include an execution review based on validation, files, logs, screenshots, user evidence, or script output

### Requirement: UI 返修视觉对照

ProjectPmHarness SHALL require screenshot-by-screenshot comparison before UI rework when acceptance feedback includes visual attachments.

#### Scenario: UI 返修包含附件截图

- GIVEN `/opsx-modify` receives screenshots, annotations, prototype captures, or actual UI captures
- WHEN the feedback concerns UI behavior or visual appearance
- THEN Agent SHALL prepare a comparison table before modifying implementation and SHALL block if evidence is insufficient

### Requirement: REQ 子文档扫尾

ProjectPmHarness SHALL require REQ-sourced acceptance rework to check linked REQ subdocuments before completion.

#### Scenario: REQ 来源返修完成前

- GIVEN `/opsx-modify` targets a REQ-sourced Change
- WHEN the rework changes or clarifies product behavior, UI behavior, acceptance, boundary, or validation
- THEN Agent SHALL check the existing linked REQ subdocuments and either update them or record why no update is needed
