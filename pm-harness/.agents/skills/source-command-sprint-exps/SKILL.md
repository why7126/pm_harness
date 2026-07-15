---
name: "source-command-sprint-exps"
description: "Sprint 经验复盘 - 总结整迭代流程、需求、开发与质量经验，沉淀到 docs/knowledge-base"
---

# source-command-sprint-exps

Use this skill when the user asks to run the migrated source command `sprint-exps`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

**Input**：`sprint-xxx`（必填或可推断）；可选 `--dry-run`、`--focus`、`--skip-best-practices`

**Output**：Experience Analysis Report + `docs/knowledge-base/retrospectives/<sprint-id>-retrospective.md` + 可选 best-practices/incidents + 索引与 sprint.md 回链；复盘文档 MUST 包含“模型 Token 使用分析”与优化方案

**禁止**：`src/`、apply/archive、自动改 `rules/`

**推荐时机**：`/sprint-archive` 之后

---

## Steps

1. 运行或读取自动 Sprint Fact Sheet：
   ```bash
   python scripts/generate-sprint-fact-sheet.py --sprint <sprint-id> --json
   ```
2. 优先基于 Fact Sheet 构建 Sprint 概况、Scope、Change tasks、Issue 状态、验收摘要与 evidence hints。
3. 仅当 Fact Sheet 标记 `warnings`、`needs_detail`、缺失/不一致项，或用户指定 `--focus` 时，按 evidence hints 分段回读对应原文片段。
4. 构建 Token Usage Fact Sheet：优先使用自动 Fact Sheet 的 `ai_usage_snapshot`；只有当 `snapshot_status: present` 且 `ai_usage_mode: actual` 时，才按真实统计输出。若 snapshot `missing`、`stale`、`failed` 或覆盖不足，MUST 输出 `ai_usage_mode: estimated_fallback`、reason、impact 和 recommended_action，再使用 `token_risks`、四件套行数、Change/tasks 计数、warnings 与 evidence hints 做估算分析。
5. 五维分析：流程、需求设计、开发质量、可复用抽象、模型 Token 使用。
6. 聚类 → 行动项 → 写入 knowledge-base（除非 dry-run）。
7. 输出 Experience Analysis Report。

详见 `.agents/skills/source-command-sprint-exps/SKILL.md`。

---

## Fact Sheet 读取边界（MUST）

- MUST 先运行或读取 `scripts/generate-sprint-fact-sheet.py --sprint <sprint-id>` 的输出，再决定是否读取 Sprint 四件套、Issue trace、OpenSpec Change 或 tasks 原文。
- MUST NOT 默认全文读取 sprint 四件套、全部 REQ/BUG/Change trace、review/root-cause/tasks。
- MUST NOT 在复盘中复制原始 trace、tasks、acceptance-report、OpenAPI、Orval generated 或测试日志全文；需要证据时只引用路径、聚合计数或短片段。
- MAY 按 Fact Sheet 的 `warnings` / `needs_detail` / `evidence_hints` 回读对应文件片段，例如缺失 trace、状态残留、tasks 未完成、acceptance 结论不清晰。
- SHOULD 使用 `python scripts/generate-sprint-fact-sheet.py --sprint <sprint-id> --json` 做结构化核对，尤其是 `scope.counts`、`changes[].tasks`、`warnings`、`token_risks`、`evidence_hints`。

## 分析要点

- **模型 Token 使用分析（MUST）**：
  - 复盘文档 MUST 增加独立章节 `## 模型 Token 使用分析`，位置建议在“流程复盘”之后、“需求与设计”之前。
  - 优先使用 `data/ai-usage/sprints/<sprint-id>.json` 经 `scripts/generate-sprint-fact-sheet.py --sprint <sprint-id> --json` 暴露的真实统计：command run 数、模型调用、工具调用、失败重跑、input tokens、cached input tokens、output tokens、reasoning output tokens、total tokens、工具输出字符数。
  - 若 `ai_usage_snapshot.snapshot_status != present` 或 `ai_usage_snapshot.ai_usage_mode != actual`，MUST 明确输出 `ai_usage_mode: estimated_fallback`、reason（如 missing/stale/failed/coverage-missing）、impact、recommended_action；不得编造具体 token 数字，不得静默按真实统计展示。
  - 若 snapshot 过期、覆盖不足或无法判定覆盖范围，MUST 在本章节保留 warning，并提示刷新 snapshot。
  - MUST 分析高消耗来源：重复读取 `rules/` 与技能文件、宽泛 `rg/find`、全量 Sprint/Issue/Change 读取、`openspec/changes/archive/**`、OpenAPI/Orval 生成物 diff、长测试日志、Workflow Sync 全量输出、Docker/build 大日志、Harness/模板 assets 注入。
  - MUST 优先引用自动 Fact Sheet 的 `token_risks`、Change/tasks 计数、四件套行数、warnings 与 evidence hints，减少人工展开四件套、trace 与 tasks 的 token 消耗。
  - MUST 给出优化方案，至少包含：读取边界、搜索排除、输出截断、diff/stat 优先、失败日志摘要、复用已读规则摘要、按 Change 分段处理、必要时沉淀脚本或校验 gate。
  - MUST 将可执行优化项写入行动项表，建议下一命令可用 `/req-capture`、`/bug-capture`、`/opsx-propose` 或下一 Sprint 的 `/sprint-propose`。
  - SHOULD 对照 `rules/agent-context-budget.md`，指出本 Sprint 哪些行为符合预算规则、哪些行为需要修正。
- **重复 BUG**：UI 不一致、上传、登录等模式 → 预防建议 + 是否 best-practice
- **需求文档**：缺原型/acceptance 与 fix-* 数量的关联
- **组件抽象**：多 REQ 相似页面 → AdminListPage / 共享弹窗等建议
- **流程**：review/opsx/apply/archive 卡点与容量

行动项含优先级与下一命令（`/req-capture`、`/sprint-propose` 等）。

## Token 使用章节模板

```markdown
## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 / 无 | 来源：会话元数据 / 工具日志 / 无法获取 |
| AI usage mode | actual / estimated_fallback | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present / missing / stale / failed | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| 主要输入消耗 | 待填 | 例如规则重复读取、Sprint 四件套、Issue/Change trace |
| 主要输出消耗 | 待填 | 例如测试日志、Workflow Sync 报告、diff 输出 |
| 重复/浪费来源 | 待填 | 例如同一规则多次全量读取、宽泛搜索命中过多 |
| 已采用节省策略 | 待填 | 例如 `rg --files` 定位、`sed -n` 分段、`git diff --stat` |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| 待填 | high / medium / low | 文件、命令或 trace | 具体做法 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 待填 | `/req-capture` 或 `/bug-capture` | open |
```
