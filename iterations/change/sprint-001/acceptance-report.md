---
note: workflow-sync — 4/11 Change 已 archive；7 applied；待人工 sign-off
created_at: 2026-08-07 15:23:44
updated_at: 2026-08-31 09:17:28
---

# Acceptance Report

## 验收项

- [x] 根目录 `AGENTS.md` 已创建。
- [x] 治理校验通过。
- [x] 未污染 `pm-harness/` 模板资产。

## 验证结果

- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- 缓存文件扫描：未发现 `.DS_Store`、`__pycache__` 或 `.pyc`。

## 归档结果

- Change `add-root-agents-entrypoint` 已归档到 `openspec/archive/2026-08-07-add-root-agents-entrypoint/`。
- 当前 Sprint 仍处于 `planning`，Sprint 目录不因单个 Change 归档而迁移。

## add-spec-logs-changelog

- [x] `docs/spec-logs/CHANGELOG.md` 已创建。
- [x] `docs/spec-logs/README.md` 已说明 CHANGELOG 用途。
- [x] `docs/spec-logs/CHANGELOG.md` 已新增“其他项目落地提示词”列。
- [x] 治理校验通过。

验证结果：

- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- 缓存文件扫描：未发现 `.DS_Store`、`__pycache__` 或 `.pyc`。

## add-tilesfst-command-governance

- [x] `/bug-review` approve 路径已接入 confirmed 根因证据门禁。
- [x] `/sprint-propose` 已接入 Sprint 选择、连续编号和归档冻结门禁。
- [x] `validate-agent-context-budget.py` 已覆盖已有 Final Output Contract 的输出卫生检查。
- [x] 新项目模板和 init-skill 模板资产已同步。

验证结果：

- `python scripts/validate-root-cause-evidence.py --all-active --json`：通过。
- `python scripts/validate-sprint-selection.py --json`：通过。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate add-tilesfst-command-governance`：通过。
- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- Workflow Sync 与 AI Usage hook：通过。

## add-tilesfst-data-observability-governance

- [x] 产品数据采集与链路观测长期标准已新增。
- [x] 标准完整性校验与硬门禁脚本已新增。
- [x] REQ、OpenSpec、Sprint 工作流 Skill 已接入数据采集声明门禁。
- [x] 新项目模板和 init-skill 模板资产已同步。

验证结果：

- `python scripts/validate-product-data-observability-standard.py`：通过。
- `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-data-observability-governance`：通过。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate add-tilesfst-data-observability-governance`：通过。
- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- `python pm-harness/scripts/validate-product-data-observability-standard.py`：通过。
- `python pm-harness/scripts/validate-product-data-observability-gates.py`：通过。
- Workflow Sync 与 AI Usage hook：通过。

## add-tilesfst-sprint-md-governance

- [x] `sprint.md` 目标编号列表与 Scope 六列表合同已落地。
- [x] Sprint scope 追加脚本、Scope 校验脚本、Workflow Sync 派生刷新脚本已进入根项目运行态。
- [x] Sprint archive readiness、stale scan、归档路径残留检查和 Fact Sheet read-first 复盘入口已进入根项目运行态。
- [x] 新项目模板和 init-skill 模板资产已同步。

验证结果：

- `python scripts/validate-sprint-selection.py --json`：通过。
- `python scripts/validate-sprint-scope.py sprint-001 --item add-tilesfst-sprint-md-governance`：通过。
- `python scripts/validate-sprint-archive-readiness.py --sprint sprint-001 --change add-tilesfst-sprint-md-governance`：通过。
- `python scripts/check-sprint-close-stale-scan.py --sprint sprint-001`：通过。
- `python scripts/generate-sprint-fact-sheet.py --sprint sprint-001 --summary`：通过。
- `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-sprint-md-governance`：通过。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate add-tilesfst-sprint-md-governance`：通过。
- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- Workflow Sync 与 AI Usage hook：通过。

## add-tilesfst-ai-usage-session-discovery

- [x] 根项目 `extract-ai-usage.py` 已接入真实 `ai_usage.py` CLI。
- [x] Workflow Sync、Sprint Archive、Sprint Exps 与上下文预算规则已补充 session 自动发现顺序。
- [x] `data/ai-usage/README.md` 已记录脱敏事实源和原始 session 禁止入库边界。
- [x] 新项目模板和 init-skill 模板资产已同步。

验证结果：

- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event explore --dry-run --json`：通过。
- `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-ai-usage-session-discovery`：通过。
- `python scripts/validate-sprint-scope.py sprint-001 --item add-tilesfst-ai-usage-session-discovery`：通过。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate add-tilesfst-ai-usage-session-discovery`：通过。
- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- Workflow Sync 与 AI Usage hook：通过。
