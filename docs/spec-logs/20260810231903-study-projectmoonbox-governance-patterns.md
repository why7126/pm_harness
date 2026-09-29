---
purpose: ProjectMoonBox 治理模式学习应用报告
content: 记录 Git 安全、Issue 当前态索引、命令顺序、Prototype UI 验收、spec-study 日志优先和引导式反馈在 ProjectPmHarness 的适配结果
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-10 23:19:03
---

# ProjectMoonBox 治理模式学习应用报告

## 基本信息

- 学习对象：ProjectMoonBox（本地只读项目）
- 学习模式：`/spec-study ProjectMoonBox` 后确认应用候选项
- 执行时间：2026-08-10 23:19:03
- 承载 Change：`apply-projectmoonbox-governance-patterns`
- 承载 Sprint：`sprint-001`

## 学习到的治理能力

- `/git-check` 可作为提交/推送前安全门禁，阻断真实 env、运行时数据、密钥、连接串、本机路径和大文件。
- `issues/*/CHANGELOG.md` 可作为 REQ/BUG 当前态看板索引，提高全局定位效率，但不替代 registry、trace、Sprint 和 OpenSpec。
- `docs/08-command-execution-order.md` 可把下一步命令、参数保留和串行写入边界制度化。
- 带 prototype 的 UI Change 需要 UI Contract、Skeleton、视觉证据、computed style 和 Mock/API 边界。
- `/spec-study` 应优先读取 `docs/spec-logs/CHANGELOG.md`，再读单次日志，再横向校验当前资产。
- 命令遇到用户决策或阻塞时，应提供结构化选项、推荐项和可补充说明。

## 已采纳内容

- 采纳 `git-check-security-gate`：新增根级 `/git-check` Skill 和 `scripts/git-check.py`，并同步到新项目模板。
- 采纳 `issues-changelog-current-state`：新增根级 REQ/BUG 当前态索引文件和规则说明，并同步模板规则。
- 采纳 `command-execution-order`：新增命令执行顺序文档，并在入口文件中引用。
- 采纳 `prototype-ui-acceptance`：新增 UI 验收专项标准，并在 UI 规则中引用。
- 采纳 `spec-study-log-first-learning`：更新 `/spec-study` 学习顺序和上下文预算规则。
- 采纳 `guided-command-feedback`：在入口规则和上下文预算规则中加入引导式反馈契约。

## 未采纳内容

- 未采纳 ProjectMoonBox 业务产品定位、Web/API/MinIO/MySQL 启用状态；这些是业务事实，不属于 ProjectPmHarness 默认治理能力。
- 未采纳 ProjectMoonBox 运行时代码、测试实现和运行时数据；本次只迁移治理模式。
- 未恢复 `.claude/`、`.cursor/`、`.kiro/`、`.opencode/` 等多 Agent 入口；ProjectPmHarness 继续只使用 `.agents/skills/`。

## 更新文件清单

- `AGENTS.md`：补充安全、命令顺序、Prototype UI 验收和引导式反馈入口。
- `.agents/skills/git-check/SKILL.md`：新增 Git 安全检测命令入口。
- `.agents/skills/spec-study/SKILL.md`：补充日志优先学习顺序。
- `rules/security.md`：新增 Git 安全门禁和输出脱敏边界。
- `rules/issues-lifecycle.md`：新增 REQ/BUG 当前态索引规范。
- `rules/document-governance.md`：补充 spec-log、Issue 当前态索引和公开安全边界。
- `rules/agent-context-budget.md`：补充日志优先学习和引导式反馈。
- `rules/ui-design.md`：补充 Prototype-driven UI Gate。
- `docs/08-command-execution-order.md`：新增命令顺序速查。
- `docs/standards/prototype-ui-acceptance.md`：新增原型驱动 UI 验收标准。
- `issues/requirements/CHANGELOG.md`、`issues/bugs/CHANGELOG.md`：新增当前态看板索引。
- `scripts/git-check.py`：新增安全扫描脚本。
- `scripts/validate-*.py`、`scripts/sync-workflow-status.py`、`scripts/extract-ai-usage.py`：补根级治理校验和 workflow hook。
- `pm-harness/**` 与 `pm-harness-skills/pm-harness-init/assets/pm-harness-template/**`：同步新项目默认治理能力。
- `openspec/changes/apply-projectmoonbox-governance-patterns/**`、`iterations/change/sprint-001/**`：记录 Change 与 Sprint scope。

## 影响评估

| 项 | 影响 |
|---|---|
| API | 不涉及 |
| 数据库 | 不涉及 |
| Web | 不涉及运行时代码 |
| 小程序 | 不涉及 |
| 管理端 | 不涉及运行时代码 |
| Orval | 不涉及 |
| Docker Compose | 不涉及 Compose 行为 |
| 测试 | 新增治理脚本校验；业务测试不适用 |

## 校验记录

- `python scripts/git-check.py`：通过，errors 0，warnings 0。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate apply-projectmoonbox-governance-patterns`：通过。
- `python pm-harness/scripts/validate-template-sync.py`：通过。
- `python pm-harness/scripts/validate-directory-structure.py`：通过。
- `python pm-harness/scripts/validate-skill-package.py`：通过，248 files，exactly one `SKILL.md`。
- `python pm-harness/scripts/validate-agent-context-budget.py`：通过。
- `python scripts/sync-workflow-status.py --event opsx.apply --change apply-projectmoonbox-governance-patterns --sprint auto`：通过，解析到 `sprint-001`，errors 0。
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change apply-projectmoonbox-governance-patterns --sprint sprint-001 --json`：通过，warning 0。
- `git diff --name-only -- src`：无输出，本次未修改 `src/`。

## 学习对象只读保护

本次只对 ProjectMoonBox 执行只读文件读取和 Git 状态查询，未对学习对象执行写入、格式化、安装、生成、迁移、测试修复、清理、提交或分支操作。只读复核时学习对象显示存在预先已有的未提交改动与运行时数据删除记录，本次未改变该状态。

## 后续建议

- 可在后续 Change 中让 Workflow Sync 自动维护 `issues/*/CHANGELOG.md` 当前态行，减少人工遗漏。
- 可进一步把 Prototype UI 验收证据扫描做成 `/opsx-archive` 前置校验。
