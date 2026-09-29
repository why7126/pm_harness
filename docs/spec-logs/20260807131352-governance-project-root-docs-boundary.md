---
created_at: 2026-08-07 13:13:52
updated_at: 2026-08-07 13:13:52
---

# Project Root Docs Boundary

## 迭代目标

明确 ProjectPmHarness 作为脚手架工程时的自身迭代边界：根目录 `docs/` 承载长期说明，`docs/spec-logs/` 承载 spec 迭代日志，`pm-harness/` 只作为生成新项目的模板。

## 变更摘要

- 新增根目录 `docs/README.md`。
- 新增根目录 `docs/00-project-governance.md`。
- 更新 `README.md`，明确当前项目数据与脚手架模板数据的边界。
- 保持 `docs/spec-logs/` 作为当前 ProjectPmHarness 的治理日志目录。
- 保持 `pm-harness/docs/spec-logs/` 作为新项目模板内的空日志目录。

## 影响范围

- API：无影响。
- 数据库：无影响。
- Web：无影响。
- 小程序：无影响。
- 管理端：无影响。
- Orval：无影响。
- Docker：无影响。
- 模板：仅更新边界说明，不引入当前项目运行数据。

## 后续建议

- 后续 ProjectPmHarness 自身的长期治理说明继续放入根目录 `docs/`。
- 后续 `/spec-opt` 与 `/spec-study apply` 产生的实际日志继续放入 `docs/spec-logs/`。
- 只有通用脚手架能力才同步进 `pm-harness/` 和 init-skill 模板资产。
