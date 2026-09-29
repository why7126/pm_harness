---
created_at: 2026-08-27 00:11:53
updated_at: 2026-08-27 00:18:00
---

# TilesFST 命令治理门禁学习应用

## 学习对象与模式

- 学习对象：ProjectTilesFST
- 学习模式：`auto`
- 执行时间：2026-08-27 00:11:53
- 应用命令：`/spec-study apply TilesFST bug-review-confirmed-gate sprint-propose-selection final-output-contract-hygiene`

## 学习到的治理能力

1. BUG review approve 前使用 `--require-confirmed` 硬门禁，阻断未确认或缺证据根因。
2. Sprint propose 前使用独立选择脚本校验 active Sprint、连续编号和第三个 active Sprint 风险。
3. 上下文预算校验脚本检查已有 Final Output Contract，避免尖括号模板、通用示例、重复确认和规范语气泄漏。

## 已采纳内容

| 采纳项 | 原因 |
|---|---|
| `bug-review-confirmed-gate` | ProjectPmHarness 已有根因状态规则，但 approve 路径缺少脚本级硬阻断，容易把 probable/hypothesis 当作可评审通过。 |
| `sprint-propose-selection` | 当前 Sprint 编号和 active Sprint 管理依赖人工判断，新增脚本可减少跳号、并发 Sprint 和归档写入风险。 |
| `final-output-contract-hygiene` | 既有命令输出契约仍残留旧模板，校验脚本可把输出卫生问题变为可重复验证的治理门禁。 |

## 未采纳内容

| 未采纳项 | 原因 |
|---|---|
| AI Usage 未观测矩阵语义 | 范围涉及 Fact Sheet、AI Usage 聚合和复盘矩阵，超出本次三项确认范围，建议后续单独学习应用。 |

## 更新文件清单

| 文件 | 修改原因 |
|---|---|
| `.agents/skills/bug-review/SKILL.md` | 接入 confirmed 根因门禁和输出契约卫生规则。 |
| `.agents/skills/sprint-propose/SKILL.md` | 接入 Sprint 选择脚本、连续编号和归档冻结门禁。 |
| `.agents/skills/{explore,git-check,spec-opt,spec-study,upgrade-plan,upgrade-validate}/SKILL.md` | 替换旧 Final Output Contract 占位模板。 |
| `scripts/validate-root-cause-evidence.py` | 增加 BUG 定位、`--bug` 和 `--require-confirmed` 校验模式。 |
| `scripts/validate-sprint-selection.py` | 新增 Sprint 选择和连续编号校验。 |
| `scripts/validate-agent-context-budget.py` | 增加已有 Final Output Contract 的输出卫生检查。 |
| `rules/root-cause-evidence.md` | 记录 `/bug-review` approve confirmed 根因门禁。 |
| `rules/agent-context-budget.md` | 记录最终输出契约卫生校验规则。 |
| `docs/08-command-execution-order.md` | 更新最小相关验证矩阵。 |
| `openspec/changes/add-tilesfst-command-governance/` | 承载本次治理学习应用事实源。 |
| `iterations/change/sprint-001/` | 纳入本次治理 Change 并更新 Sprint 验收摘要。 |
| `pm-harness/` 与 `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 对应文件 | 同步新项目默认治理能力。 |

## 影响分析

| 领域 | 影响 |
|---|---|
| API | 无运行时 API 影响。 |
| 数据库 | 无 schema、迁移或数据影响。 |
| Web | 无前端运行时代码影响。 |
| 小程序 | 无小程序运行时代码影响。 |
| 管理端 | 无管理端运行时代码影响。 |
| Orval | 无 OpenAPI 或 Orval 生成物影响。 |
| Docker Compose | 无 Compose 行为影响。 |
| 测试 | 增加治理脚本自检和模板校验。 |

## 校验命令和结果

| 命令 | 结果 |
|---|---|
| `python scripts/validate-root-cause-evidence.py --all-active --json` | 通过，`blocker_count=0`，`warning_count=0`。 |
| `python scripts/validate-sprint-selection.py --json` | 通过，active Sprint 为 `sprint-001`，下一编号为 `sprint-002`。 |
| `python scripts/validate-agent-context-budget.py` | 通过。 |
| `python scripts/validate-openspec-language.py` | 通过。 |
| `python scripts/validate-directory-structure.py` | 通过。 |
| `openspec validate add-tilesfst-command-governance` | 通过。 |
| `python pm-harness/scripts/validate-template-sync.py` | 通过。 |
| `python pm-harness/scripts/validate-directory-structure.py` | 通过；首次运行发现本地缓存 `.DS_Store`，清理后通过。 |
| `python pm-harness/scripts/validate-skill-package.py` | 通过。 |
| `python pm-harness/scripts/validate-agent-context-budget.py` | 通过。 |
| `python pm-harness/scripts/validate-root-cause-evidence.py --all-active --json` | 通过。 |
| `python pm-harness/scripts/validate-sprint-selection.py --json` | 通过，模板默认无 active Sprint。 |
| `python scripts/sync-workflow-status.py --event opsx.apply --change add-tilesfst-command-governance --sprint auto` | 通过，解析 Sprint 为 `sprint-001`。 |
| `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change add-tilesfst-command-governance --sprint sprint-001 --json` | 通过，`usage_mode=summary`，`warning_count=0`。 |

## 学习对象只读保护

学习对象仅执行读取、搜索和 `git status --short` 复核；未对学习对象执行写入、安装、格式化、迁移、测试修复、清理、提交、分支或重置命令。复核时学习对象存在既有工作区变更，但这些变更属于学习对象自身状态，未由本次命令写入。

## 后续建议

- 后续如需量化 Sprint/命令 token 成本，再单独学习应用 AI Usage 未观测矩阵语义。
