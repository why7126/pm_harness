---
created_at: 2026-08-08 21:03:04
updated_at: 2026-08-08 21:03:04
---

# Changelog Adoption Prompts

## 迭代目标

在 `docs/spec-logs/CHANGELOG.md` 变更历史表中新增“其他项目落地提示词”列，使每一条规范、脚本、命令、技能或模板治理更新都能沉淀一条可复用 prompt，方便其他项目按相同规范落地。

## 变更摘要

- `docs/spec-logs/CHANGELOG.md` 新增“其他项目落地提示词”列。
- 为既有历史记录补充可复制的跨项目落地 prompt。
- `docs/spec-logs/README.md` 增加 CHANGELOG 记录规则：每条记录 MUST 包含“其他项目落地提示词”。
- 更新 `add-spec-logs-changelog` Change 的任务、设计和 trace。

## 影响范围

- API：无影响。
- 数据库：无影响。
- Web：无影响。
- 小程序：无影响。
- 管理端：无影响。
- Orval：无影响。
- Docker：无影响。
- 模板：不修改 `pm-harness/` 或 init-skill 模板资产。

## 更新文件

- `docs/spec-logs/CHANGELOG.md`
- `docs/spec-logs/README.md`
- `docs/spec-logs/20260808205651-governance-spec-logs-changelog.md`
- `docs/spec-logs/20260808210304-governance-changelog-adoption-prompts.md`
- `openspec/changes/add-spec-logs-changelog/`

## 验证结果

- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- 缓存文件扫描：未发现 `.DS_Store`、`__pycache__` 或 `.pyc`。
