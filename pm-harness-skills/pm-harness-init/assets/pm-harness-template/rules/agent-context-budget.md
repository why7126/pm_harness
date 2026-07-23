---
purpose: Agent 上下文预算治理
content: 约束 AI 读取范围、搜索排除、Harness/模板工程噪音、生成物与大输出处理
source: 实际项目 Token 复盘后迁移为 Harness 模板规则
update_method: Agent 工作流、Harness 模板、技能命令或上下文预算策略变化时更新
created_at: 2026-07-08 09:26:36
updated_at: 2026-07-14 00:00:00
note: 所有 Agent 命令与普通开发任务均应遵守，优先级高于单个技能中的宽泛读取建议
---

# Agent 上下文预算治理

## 1. 目标

降低 AI 在需求、BUG、Sprint、OpenSpec 与 Harness 相关任务中的无效 token 消耗，避免重复读取大规则、大目录、历史归档、生成物和模板工程资产。

核心原则：先定位，再摘要，再片段读取；只有证据不足或任务明确要求时才扩大范围。

## 2. 默认读取边界

AI 执行任务时 MUST：

- 已在同一会话读取过且无变更的规则文件，用摘要承接，不重复全量读取。
- 先用 `rg -l`、`rg --files`、`find ... -maxdepth`、`git diff --name-only` 或 `git diff --stat` 定位，再读取必要片段。
- 对 Markdown、Spec、代码文件优先使用 `sed -n '<start>,<end>p'` 或 `nl -ba ... | sed -n` 分段读取。
- 命令输出默认控制在合理范围；预期更大时先输出文件清单、命中数、失败摘要或 diff stat。
- 不默认全量读取 `docs/**`、`issues/**`、`iterations/**`、`openspec/specs/**`、`openspec/changes/archive/**`。

AI 执行任务时 MUST NOT：

- 默认运行 `cat rules/*.md`、`cat docs/**`、`ls -R` 或无边界 `rg <keyword> .`。
- 为确认一个字段或状态读取整个目录或整个历史归档。
- 在成功路径中输出完整测试日志、完整 Workflow Sync 派生块或完整 generated 文件。

## 3. 默认搜索排除

大范围搜索和文件清单默认排除：

```text
--glob '!pm-harness*/**'
--glob '!**/assets/**'
--glob '!**/.git/**'
--glob '!**/node_modules/**'
--glob '!**/dist/**'
--glob '!**/coverage/**'
--glob '!openspec/changes/archive/**'
--glob '!src/**/generated/**'
--glob '!.agents/**'
```

如当前任务明确要求分析 Harness、模板工程、agent 资产、历史归档或生成物，MAY 放开对应排除项，但 MUST 先说明原因，并优先输出清单或命中数。

## 4. Harness 与模板工程

- `pm-harness*/`、Harness 模板 assets、`.agents/skills/` 默认视为高噪音上下文。
- 非 Harness 任务不得读取 Harness 模板资产全文。
- 需要清理或校验 Harness 资产时，先限定具体路径与文件类型，再分段读取。
- 不应把长脚本、长批准命令或模板资产内容复制进技能文件；应引用脚本路径或规则文档。

## 5. 生成物与大文件

- API 变更仍 MUST 同步 OpenAPI / 客户端生成物 / docs / tests，但复核方式应节制。
- 默认使用 `git diff --stat`、`git diff --name-only` 或目标 schema 片段。
- 不默认输出 OpenAPI JSON、客户端 generated 文件、bundle、coverage、日志全文。
- 需要确认生成类型时，只读取相关接口、Schema 或导出函数片段。

## 6. Git Diff 与测试输出

- 普通复核优先 `git diff --stat` 与 focused diff。
- 大 diff 先看文件列表；只对手写源码、文档或任务文件展开必要片段。
- 测试通过时只报告命令与摘要；测试失败时只展开失败用例、堆栈关键段和相关文件片段。
- Workflow Sync 成功时只报告摘要；失败时按报告定位具体 marker 或文件片段。

## 7. 技能文件要求

Agent 命令技能 SHOULD：

- 引用本文件或内置等价上下文预算章节。
- 保留命令特定的 Must Read 与业务门禁，但不得要求默认宽泛读取整目录。
- 对 apply/archive/sprint 类高消耗命令，明确要求先读取 OpenSpec CLI `contextFiles`、任务文件、trace/status 片段，再按需扩展。

## 8. 校验

如项目提供上下文预算校验脚本，推荐命名为：

```bash
python scripts/validate-agent-context-budget.py
```

该脚本用于检查 Agent 技能是否引用本规则，并阻止常见宽泛读取模式回退。
