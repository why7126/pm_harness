---
created_at: 2026-08-19 11:28:41
updated_at: 2026-08-19 11:28:41
---

# DeepSeek Harness 治理模式学习应用报告

## 学习对象与模式

- 学习对象：`https://github.com/deepseek-ai/deepseek-harness`
- 学习模式：`auto`
- 执行时间：2026-08-19 11:28:41
- 应用命令：`/spec-study apply Agent Decision Notes + 文档层级与一事实一归属 + 治理检查聚合器`

## 学习到的治理能力

- Agent Notes：用轻量决策记录承载非平凡治理变更的动机、取舍、状态和归档边界。
- 文档层级：入口、规则、长期文档、一次性报告、决策记录和变更事实源分层管理。
- 一事实一归属：同一长期事实只保留一个事实源，其他位置通过链接或短路由引用。
- 检查聚合器：用一个只读入口编排常用治理校验，降低执行遗漏。

## 已采纳内容

| 内容 | 采纳原因 |
|---|---|
| 治理决策记录规范 | 当前 `docs/spec-logs/` 更适合记录一次命令结果，缺少长期记录治理取舍的位置。 |
| 文档层级与一事实一归属 | 能减少 `AGENTS.md`、`README.md`、`rules/`、Skill 和 Change 之间的重复漂移。 |
| 治理检查聚合器 | 复用现有校验脚本，以只读聚合方式提供稳定入口。 |

## 未采纳内容

| 内容 | 未采纳原因 |
|---|---|
| Cordis 插件运行时架构 | 属于 DeepSeek Harness 产品实现架构，不适合直接应用到 PM Harness 治理模板。 |
| 多 Agent 入口目录 | 当前项目明确只使用 `.agents/skills/`，不得恢复 `.claude`、`.codex`、`.cursor`、`.kiro`、`.opencode` 等入口。 |
| 大规模双语配对与 TypeScript 文档类型校验 | 当前项目以中文治理文档和 Python 校验脚本为主，维护成本高于当前收益。 |

## 更新文件清单

| 文件 | 修改原因 |
|---|---|
| `openspec/changes/add-deepseek-governance-patterns/*` | 承载本次治理学习应用 Change。 |
| `iterations/change/sprint-001/sprint.yaml` | 将纯治理 Change 纳入 Sprint scope。 |
| `rules/governance-decision-notes.md` | 新增治理决策记录规范。 |
| `rules/document-governance.md` | 补充文档层级、一事实一归属和决策记录入口。 |
| `docs/decision-notes/**/.gitkeep` | 建立当前项目治理决策记录目录占位。 |
| `scripts/run-governance-checks.py` | 新增根项目治理检查聚合器。 |
| `scripts/validate-directory-structure.py` | 将 `docs/decision-notes` 纳入目录校验。 |
| `pm-harness/**` | 同步新项目模板规则、目录和脚本。 |
| `pm-harness-skills/pm-harness-init/assets/pm-harness-template/**` | 同步 init-skill 模板资产。 |
| 本机安装版 `pm-harness-init` 模板资产 | 同步本次新增/更新的模板规则、目录占位和脚本。 |
| `docs/spec-logs/CHANGELOG.md` | 更新规范工程变更历史总账。 |

## 影响评估

- API：无影响。
- 数据库：无影响。
- Web：无影响。
- 小程序：无影响。
- 管理端：无影响。
- Orval：无影响。
- Docker Compose：无影响。
- 测试：新增治理聚合脚本；业务测试不适用。

## 校验命令和结果

已执行：

```bash
python scripts/run-governance-checks.py
python pm-harness/scripts/validate-template-sync.py
python pm-harness/scripts/validate-directory-structure.py
python pm-harness/scripts/validate-skill-package.py
python pm-harness/scripts/validate-agent-context-budget.py
openspec validate add-deepseek-governance-patterns
python scripts/sync-workflow-status.py --event opsx.apply --change add-deepseek-governance-patterns --sprint auto
python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change add-deepseek-governance-patterns --sprint sprint-001 --json
```

结果：

| 命令 | 结果 |
|---|---|
| `python scripts/run-governance-checks.py` | 通过 |
| `python pm-harness/scripts/validate-template-sync.py` | 通过 |
| `python pm-harness/scripts/validate-directory-structure.py` | 通过 |
| `python pm-harness/scripts/validate-skill-package.py` | 通过 |
| `python pm-harness/scripts/validate-agent-context-budget.py` | 通过 |
| `openspec validate add-deepseek-governance-patterns` | 通过 |
| `python scripts/sync-workflow-status.py --event opsx.apply --change add-deepseek-governance-patterns --sprint auto` | 通过，解析 Sprint 为 `sprint-001` |
| `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change add-deepseek-governance-patterns --sprint sprint-001 --json` | 通过，warning 0 |
| 本机安装版模板资产抽样比对 | 通过，关键文件字节一致，`docs/decision-notes` 占位完整 |

## 学习对象只读保护结果

学习对象以临时只读快照读取。应用阶段未对学习对象路径执行写入、格式化、安装、生成、提交、清理或重置命令；`git status --short` 为空。

## 后续建议

- 后续可新增轻量 `validate-decision-notes.py`，检查决策记录路径、状态和必要章节。
- 若文档重复继续增多，可再引入文档预算 manifest；本次先不增加额外门禁成本。
