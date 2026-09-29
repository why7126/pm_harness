---
created_at: 2026-08-07 15:23:44
updated_at: 2026-08-07 15:23:44
---

# Root Agents Entrypoint

## 迭代目标

为 ProjectPmHarness 仓库根目录新增 `AGENTS.md`，作为当前脚手架工程自身的 AI 行为入口，避免误用 `pm-harness/AGENTS.md` 模板入口。

## 变更摘要

- 新增根目录 `AGENTS.md`。
- 新增根目录 OpenSpec Change：`openspec/changes/add-root-agents-entrypoint/`。
- 新增根目录 Sprint 记录：`iterations/change/sprint-001/`。
- 明确根项目运行态治理资产与 `pm-harness/` 模板资产的边界。

## 影响范围

- API：无影响。
- 数据库：无影响。
- Web：无影响。
- 小程序：无影响。
- 管理端：无影响。
- Orval：无影响。
- Docker：无影响。
- 模板：不修改 `pm-harness/AGENTS.md`，不把根运行态治理数据同步进模板。

## 更新文件

- `AGENTS.md`
- `openspec/changes/add-root-agents-entrypoint/`
- `iterations/change/sprint-001/`
- `docs/spec-logs/20260807152344-governance-root-agents-entrypoint.md`

## 验证结果

- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- 缓存文件扫描：未发现 `.DS_Store`、`__pycache__` 或 `.pyc`。

## 归档结果

- Change `add-root-agents-entrypoint` 已归档到 `openspec/archive/2026-08-07-add-root-agents-entrypoint/`。
- 本 Change 无 delta specs，正式规格不变。
- 根目录目前没有独立 Workflow Sync 脚本；`pm-harness/scripts/` 仍用于模板校验，因此本次归档采用根 `openspec/` 手工归档并在 Change 中保留归档验证摘要。

## 后续建议

- 后续当前脚手架工程自身任务先读根 `AGENTS.md`。
- 涉及新项目模板能力时，再读取并同步 `pm-harness/` 与 init-skill 模板资产。
