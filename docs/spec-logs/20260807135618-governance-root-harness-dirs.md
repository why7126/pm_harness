---
created_at: 2026-08-07 13:56:18
updated_at: 2026-08-07 13:56:18
---

# Root Harness Governance Directories

## 迭代目标

为当前 ProjectPmHarness 脚手架工程自身补齐根目录 Harness 治理资产，使其后续规范、脚本、技能和模板能力演进能够走独立于 `pm-harness/` 模板目录的治理闭环。

## 变更摘要

- 新增根目录 `issues/`，作为当前 ProjectPmHarness 的需求和 BUG 池。
- 新增根目录 `iterations/`，作为当前 ProjectPmHarness 的 Sprint / 迭代记录。
- 新增根目录 `openspec/`，作为当前 ProjectPmHarness 的 OpenSpec Change、Specs 和 Archive 事实源。
- 新增根目录 OpenSpec 配置、项目上下文和测试映射文档。
- 后续 `pm-harness/` 仍只作为生成新项目的模板目录，不承载当前项目运行态数据。

## 影响范围

- API：无影响。
- 数据库：无影响。
- Web：无影响。
- 小程序：无影响。
- 管理端：无影响。
- Orval：无影响。
- Docker：无影响。
- 模板：无运行态数据同步进模板。

## 后续建议

- 后续 ProjectPmHarness 自身的需求/BUG 从根目录 `issues/` 开始治理。
- 后续 ProjectPmHarness 自身 Sprint 从根目录 `iterations/` 管理。
- 后续 ProjectPmHarness 自身 OpenSpec Change 从根目录 `openspec/changes/` 创建。
