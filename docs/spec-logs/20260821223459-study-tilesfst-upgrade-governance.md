---
purpose: TilesFST 升级治理学习应用报告
content: 记录升级路径对象、文档表达卫生和最小相关验证矩阵的采纳结果
source: /spec-study apply TilesFST upgrade-governance 文档卫生 最小相关验证矩阵
update_method: 同一次 TilesFST 治理学习应用的验证结果或修正继续更新本文
created_at: 2026-08-21 22:34:59
updated_at: 2026-08-21 22:58:30
---

# TilesFST 升级治理学习应用报告

## 学习对象与模式

- 学习对象：ProjectTilesFST。
- 学习模式：Phase 2，经用户确认应用 `upgrade-governance`、文档卫生和最小相关验证矩阵。
- 执行时间：2026-08-21 22:34:59，时区 `Asia/Shanghai`。
- 应用 Change：`add-tilesfst-upgrade-governance`。
- 承载 Sprint：`sprint-001`。

## 学习到的治理能力

- 版本升级路径对象：区分目标版本事实源与某条 `from_version -> to_version` 升级路径是否已验证。
- upgrade 命令边界：只生成和校验升级/回滚计划，不自动执行生产升级、真实 env 写入、DB restore 或对象存储写入维护。
- 跨版本支持级别：缺少中间版本事实、演练、DB/env/object storage 或回滚证据时，不能声明跨版本升级 supported。
- 文档表达卫生：长期文档避免会话推理、临时草稿、review 对话、不可解析路径和敏感片段。
- 最小相关验证矩阵：按 diff scope 选择本地最小相关校验，避免机械运行无关全量矩阵。

## 已采纳内容和采纳原因

| 内容 | 采纳原因 | 落地位置 |
|---|---|---|
| 升级路径对象与支持级别 | 补齐 release/image 之后的部署升级承诺边界 | `rules/release.md`、`scripts/validate-release-upgrade.py`、upgrade 技能 |
| `/upgrade-plan` 与 `/upgrade-validate` | 让版本升级计划和校验形成可复制命令入口 | `.agents/skills/`、`pm-harness/.agents/skills/`、init 模板 Skill |
| 通用升级校验脚本 | 将 TilesFST 实践改写为不绑定业务前缀的模板能力 | `scripts/validate-release-upgrade.py` 及模板副本 |
| 文档表达卫生标准 | 降低长期文档写入过程残留和敏感片段的风险 | `docs/standards/document-prose-hygiene.md`、`scripts/validate-doc-prose-hygiene.py` |
| 最小相关验证矩阵 | 帮助命令选择与触达面匹配的验证证据 | `docs/08-command-execution-order.md` |

## 未采纳内容和未采纳原因

- 未复制 TilesFST 业务技术栈、MinIO 前缀、瓷砖平台字段或运行时事实；这些属于学习对象业务上下文。
- 未原样复制 TilesFST 长脚本；本次改写为通用脚手架脚本，避免 `TILESFST_*` 等业务变量进入模板。
- 未自动创建 release 样例升级计划；当前 ProjectPmHarness 根项目不是具体业务发布项目，模板只提供命令和脚本能力。
- 未恢复多 Agent 入口目录；本项目继续只维护 `.agents/skills/`。

## 更新文件清单

| 文件 | 修改原因 |
|---|---|
| `openspec/changes/add-tilesfst-upgrade-governance/` | 承载本次学习应用的 proposal、design、tasks 和 delta spec。 |
| `iterations/change/sprint-001/` | 将纯治理 Change 纳入 Sprint scope。 |
| `.agents/skills/upgrade-plan/SKILL.md`、`.agents/skills/upgrade-validate/SKILL.md` | 新增当前仓库可用 upgrade 命令入口。 |
| `scripts/validate-release-upgrade.py` | 新增通用升级计划生成与校验脚本。 |
| `docs/standards/document-prose-hygiene.md`、`scripts/validate-doc-prose-hygiene.py` | 新增长期文档表达卫生标准和轻量扫描入口。 |
| `docs/08-command-execution-order.md`、`docs/README.md`、`AGENTS.md` | 同步读取路由、文档索引和最小相关验证矩阵。 |
| `pm-harness/` 对应规则、脚本、技能和文档 | 同步未来生成项目默认模板能力。 |
| `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 对应规则、脚本、技能模板和文档 | 同步初始化模板资产。 |
| `<local-codex-skill>/pm-harness-init` | 同步本机安装版初始化 Skill，避免本仓库模板能力与当前可用 Skill 漂移。 |
| `pm-harness-skills/pm-harness-init/references/default-command-catalog.md` | 将 upgrade 治理加入默认命令目录。 |
| `docs/spec-logs/CHANGELOG.md`、本文 | 登记本次跨项目学习应用。 |

## 影响评估

- API：不影响。
- 数据库：不修改 schema；升级计划会要求 DB 影响时补充 drift/smoke、备份或回滚证据。
- Web：不影响业务页面。
- 小程序：不影响。
- 管理端：不影响。
- Orval：不需要。
- Docker Compose：不修改 Compose 拓扑；发布升级计划会读取部署和镜像证据。
- 测试：新增治理脚本级校验；业务测试不适用。

## 校验命令和结果

- 通过：`python -m py_compile scripts/validate-release-upgrade.py scripts/validate-doc-prose-hygiene.py`。
- 通过：`python scripts/validate-release-upgrade.py --help`。
- 通过：`python scripts/validate-release-upgrade.py env-diff`；根项目没有 env 示例，输出 `manual_review` 摘要。
- 通过并返回 warning：`python scripts/validate-doc-prose-hygiene.py docs/standards/document-prose-hygiene.md docs/08-command-execution-order.md AGENTS.md --json`；warning 来自规则文档中的示例词和 `AGENTS.md` 既有本机安装路径说明，不阻断本次治理变更。
- 通过：`python scripts/validate-agent-context-budget.py`。
- 通过：`python scripts/validate-openspec-language.py`。
- 通过：`python scripts/validate-directory-structure.py`。
- 通过：`openspec validate add-tilesfst-upgrade-governance`。
- 通过：`python pm-harness/scripts/validate-template-sync.py`。
- 通过：`python pm-harness/scripts/validate-directory-structure.py`。
- 首次未通过后已修复并通过：`python pm-harness/scripts/validate-skill-package.py`；新增 upgrade 技能后文件数为 262，将包体预算从 260 调整到 270。
- 通过：`python pm-harness/scripts/validate-agent-context-budget.py`。
- 通过：`python scripts/sync-workflow-status.py --event opsx.apply --change add-tilesfst-upgrade-governance --sprint auto`；解析 Sprint 为 `sprint-001`，Errors 0。
- 通过：`python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change add-tilesfst-upgrade-governance --sprint sprint-001 --json`；`usage_mode=summary`，`warning_count=0`。
- 通过：`git diff --name-only -- src`；无业务 `src/` 文件变更。
- 完成：本机安装版 `pm-harness-init` 已从仓库 skill 包同步；报告中使用脱敏占位符记录，不写入本机绝对路径。
- 归档通过：`openspec archive add-tilesfst-upgrade-governance -y` 已将 3 条 `project-governance` requirements 合并至正式 spec，并归档到 `openspec/archive/2026-08-21-add-tilesfst-upgrade-governance/`；归档证据目录已补齐 proposal、design、tasks 和 delta spec。
- 归档后通过：`python scripts/validate-directory-structure.py`、`python scripts/sync-workflow-status.py --event opsx.archive --change add-tilesfst-upgrade-governance --sprint auto`、`python scripts/promote-issues-for-archive.py --change add-tilesfst-upgrade-governance --reason "/opsx-archive add-tilesfst-upgrade-governance"`、`python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.archive --change add-tilesfst-upgrade-governance --sprint sprint-001 --json`。
- 归档后通过：`openspec validate project-governance --strict`、`python scripts/validate-openspec-language.py`、`git diff --name-only -- src`。

## 学习对象只读保护结果

对 ProjectTilesFST 仅执行只读扫描、片段读取和 Git 状态查询；未在学习对象路径中执行写入、安装、生成、格式化、迁移、测试修复、清理、提交、切换分支或修改 Git 状态的操作。完成前复核 `git status --short` 为空。

## 后续建议

- 后续可为 `validate-release-upgrade.py` 增加聚焦单测，覆盖 cross-version 支持级别和敏感信息扫描。
- 后续若项目需要更严格文档门禁，可将 `validate-doc-prose-hygiene.py` 从 warning 级升级为聚焦 blocker 规则。
