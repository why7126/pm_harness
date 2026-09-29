---
created_at: 2026-08-21 08:24:48
updated_at: 2026-08-21 08:24:48
---

# ProjectMoonBox 增量治理学习应用报告

## 学习对象

- 学习对象：`ProjectMoonBox`
- 学习模式：`auto`
- 执行时间：2026-08-21 08:24:48，Asia/Shanghai
- 应用 Change：`apply-projectmoonbox-governance-increments`
- Sprint：`sprint-001`

## 学习到的治理能力

- 证据化根因分析：根因状态分级、证据链、人工补证和校验脚本。
- 命令执行复盘 Hook：workflow 命令完成后输出链路状态、问题证据、规范优化建议和 follow-up 状态。
- UI 返修视觉对照：带附件截图的 UI 型返修先做逐项对照再修改实现。
- REQ 子文档扫尾：REQ 来源返修完成前检查实际存在的子文档是否需同步。
- Workflow Sync 输出与下一步：Issue 子文档 apply 输出更明确，req/bug opsx 后下一步推导到 `/opsx-apply <REQ|BUG-full-id>`。

## 已采纳内容和原因

| 采纳项 | 原因 |
|---|---|
| 证据化根因分析 | 降低无证据确认根因的风险，适合沉淀为通用治理规则 |
| 执行链路复盘 Hook | 让每次命令结果可复盘，便于发现可沉淀的规范优化点 |
| UI 返修附件截图对照 | 让 UI 返修先对齐验收证据，减少盲改 |
| REQ 子文档扫尾 | 避免实现返修后遗漏 PRD、验收、原型上下文等事实源 |
| Workflow Sync 输出与下一步说明 | 当前根项目脚本较轻，先落地输出契约和说明边界 |

## 未采纳内容和原因

- 未复制 ProjectMoonBox 的业务源码、API、DB、部署、产品事实和运行时数据：与本次治理学习无关。
- 未迁移 ProjectMoonBox 完整 Workflow Sync 引擎：当前 ProjectPmHarness 根项目使用轻量同步脚本，完整引擎迁移成本和范围超出本次增量治理。
- 未恢复多 Agent 入口目录：本项目统一使用 `.agents/skills/`。

## 更新文件清单

| 文件 | 修改原因 |
|---|---|
| `AGENTS.md` | 增加根因/返修读取路由和执行红线 |
| `rules/root-cause-evidence.md` | 新增证据化根因分析长期规则 |
| `rules/agent-context-budget.md` | 增加执行链路复盘中央契约 |
| `rules/ui-design.md` | 增加 UI 返修附件截图对照门禁 |
| `docs/08-command-execution-order.md` | 增加 workflow 命令执行复盘 Hook |
| `docs/standards/prototype-ui-acceptance.md` | 增加附件截图逐项对照要求 |
| `docs/README.md` | 索引根因证据规则 |
| `.agents/skills/opsx-modify/SKILL.md` | 接入根因证据、UI 截图对照和 REQ 子文档扫尾 |
| `.agents/skills/workflow-sync/SKILL.md` | 增加 Issue 输出、下一步推导和执行复盘说明 |
| `scripts/validate-root-cause-evidence.py` | 新增轻量根因证据校验入口 |
| `scripts/sync-workflow-status.py` | 补充轻量 Issue 输出摘要 |
| `pm-harness/**` | 同步新项目模板规则、脚本和 Skill 契约 |
| `pm-harness-skills/pm-harness-init/assets/pm-harness-template/**` | 同步 init-skill 模板资产 |
| `openspec/changes/apply-projectmoonbox-governance-increments/**` | 记录本次治理变更事实源 |
| `iterations/change/sprint-001/sprint.yaml` | 纳入 Sprint scope |
| `docs/spec-logs/CHANGELOG.md` | 更新规范工程变更历史 |

## 影响评估

- API：不影响。
- 数据库：不影响。
- Web：不影响运行时代码。
- 小程序：不影响。
- 管理端：不影响运行时代码。
- Orval：不影响。
- Docker Compose：不影响。
- 测试：新增治理脚本校验；业务测试不适用。

## 校验命令和结果

| 命令 | 结果 | 摘要 |
|---|---|---|
| `python scripts/validate-root-cause-evidence.py --all-active --json` | 通过 | `finding_count: 0` |
| `python scripts/validate-agent-context-budget.py` | 通过 | 根项目上下文预算和执行链路复盘契约通过 |
| `python scripts/validate-openspec-language.py` | 通过 | OpenSpec 中文优先校验通过 |
| `python scripts/validate-directory-structure.py` | 通过 | 根项目目录结构通过 |
| `openspec validate apply-projectmoonbox-governance-increments` | 通过 | 目标 Change 有效 |
| `python pm-harness/scripts/validate-template-sync.py` | 通过 | 模板同步校验通过 |
| `python pm-harness/scripts/validate-directory-structure.py` | 通过 | 模板目录结构通过 |
| `python pm-harness/scripts/validate-skill-package.py` | 通过 | Skill 包校验通过 |
| `python pm-harness/scripts/validate-agent-context-budget.py` | 通过 | 模板 Skill 上下文预算通过 |
| `python scripts/sync-workflow-status.py --event opsx.apply --change apply-projectmoonbox-governance-increments --sprint auto` | 通过 | 解析到 `sprint-001`，Errors 0 |
| `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change apply-projectmoonbox-governance-increments --sprint sprint-001 --json` | 通过 | `warning_count: 0` |
| `git diff --check` | 通过 | 无 whitespace 错误 |
| `git diff --name-only -- src pm-harness/src pm-harness-skills/pm-harness-init/assets/pm-harness-template/src` | 通过 | 本次未修改业务源码路径 |

## 学习对象只读保护结果

学习对象只执行只读扫描、文本读取和 `git status --short` 复核；未在学习对象路径下执行写入、安装、格式化、生成、迁移、测试修复、提交、分支、清理或重置命令。复核时学习对象存在既有未提交/未跟踪变更，本次未处理、未修改。

## 后续建议

- 后续可评估是否将根因证据校验接入 `/bug-review`、`/bug-opsx` 或归档 readiness。
- 后续可评估是否迁移更完整的 Workflow Sync Issue 派生引擎。
