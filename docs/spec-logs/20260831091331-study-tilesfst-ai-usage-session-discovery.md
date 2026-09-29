---
created_at: 2026-08-31 09:13:31
updated_at: 2026-08-31 09:13:31
type: spec-study-apply
source_project: TilesFST
change_id: add-tilesfst-ai-usage-session-discovery
sprint_id: sprint-001
---

# TilesFST AI Usage Session 自动发现学习应用

## 学习输入

- 命令：`/spec-study apply TilesFST ai-usage-session-auto-discovery`
- 学习对象：ProjectTilesFST
- 学习模式：`auto`

## 学习到的治理能力

- Workflow AI Usage hook 优先自动发现本地 session，而不是默认要求操作者传 `--session-jsonl`。
- 自动发现顺序覆盖显式参数、环境变量、`AI_USAGE_SESSIONS_DIR` 和本机默认 Codex sessions 目录。
- Hook 输出使用 compact summary，只呈现 `usage_mode`、`command_run_count`、`session_input` 类型、Sprint snapshot 和 warning 计数。
- 原始 session JSONL、本机路径、prompt、system/developer instructions、完整工具输出和密钥不得持久化。

## 已采纳内容

| 内容 | 采纳原因 |
|---|---|
| 根项目 `extract-ai-usage.py` 接入真实 `ai_usage.py` CLI | 消除 placeholder，启用已有自动发现实现。 |
| Workflow Sync / Sprint Archive / Sprint Exps 技能说明 | 让命令使用默认自动发现，失败时再提示显式 session。 |
| `rules/agent-context-budget.md` AI Usage session 发现小节 | 将脱敏输出和本机路径安全边界作为长期规则。 |
| `data/ai-usage/README.md` | 明确仓库内只保存脱敏聚合事实源，不保存原始 session。 |
| 模板资产同步 | 新项目初始化后继承同一 AI Usage hook 口径。 |

## 未采纳内容

- 未复制 TilesFST 的真实 session、usage snapshot 或 Sprint 数据。
- 未引入 TilesFST 8/30-8/31 的发布治理、环境分层证据和 release-status 面板；这些属于后续候选，不在本次用户确认范围。
- 未修改业务 `src/`、API、DB、Web、小程序、管理端、Orval 或 Docker Compose。

## 更新文件清单

| 文件 | 修改原因 |
|---|---|
| `scripts/extract-ai-usage.py` | 改为调用 `ai_usage.main()` 的真实 CLI wrapper。 |
| `.agents/skills/workflow-sync/SKILL.md` | 补充自动发现顺序和本机路径输出边界。 |
| `.agents/skills/sprint-archive/SKILL.md` | Sprint close 前刷新 usage snapshot 时优先自动发现 session。 |
| `.agents/skills/sprint-exps/SKILL.md` | 复盘刷新 usage snapshot 时优先使用 post-command hook 自动发现。 |
| `rules/agent-context-budget.md` | 增加 AI Usage session 发现与脱敏输出规则。 |
| `data/ai-usage/README.md` | 新增本地脱敏事实源边界说明。 |
| `pm-harness/` 对应文件 | 同步新项目模板默认能力。 |
| `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 对应文件 | 同步 init-skill 模板资产。 |
| `openspec/changes/add-tilesfst-ai-usage-session-discovery/` | 记录本次 Change proposal/design/tasks/spec/trace/test/acceptance。 |
| `iterations/change/sprint-001/` | 将本 Change 纳入当前 Sprint scope。 |

## 影响范围

| 层级 | 影响 |
|---|---|
| API | 不适用，未修改接口。 |
| DB | 不适用，未修改 schema、migration 或数据模型。 |
| Web | 不适用，未修改业务实现。 |
| 小程序 | 不适用，未修改业务实现。 |
| 管理端 | 不适用。 |
| Orval | 不适用。 |
| Docker Compose | 不适用。 |
| 测试 | 运行 AI Usage hook dry-run 与治理脚本校验。 |

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 本次变更触达 workflow AI Usage hook 和脱敏事实源治理，不改业务运行时产品数据采集。
  validation:
    - python scripts/validate-product-data-observability-gates.py --change add-tilesfst-ai-usage-session-discovery
```

## 校验命令

- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event explore --dry-run --json`
- `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-ai-usage-session-discovery`
- `python scripts/validate-sprint-scope.py sprint-001 --item add-tilesfst-ai-usage-session-discovery`
- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate add-tilesfst-ai-usage-session-discovery`
- `python pm-harness/scripts/validate-template-sync.py`
- `python pm-harness/scripts/validate-directory-structure.py`
- `python pm-harness/scripts/validate-skill-package.py`
- `python pm-harness/scripts/validate-agent-context-budget.py`

## 学习对象只读保护

本次只读取 ProjectTilesFST 的 spec-log、规则、技能、脚本片段和 Git 状态；未对学习对象执行写入、格式化、安装、迁移、测试修复、提交、清理或重置。

## 后续建议

- 可继续单独评估 `release-status-decision-panel`，但不与本次 AI Usage session 自动发现混合应用。
