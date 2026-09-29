---
created_at: 2026-08-19 11:25:48
updated_at: 2026-08-19 11:25:48
---

# Design

## 治理决策记录

新增 `rules/governance-decision-notes.md`，将 DeepSeek Harness 的 Agent Notes 思路转写为 PM Harness 的治理决策记录。该规则只承载“为什么这样治理、放弃了什么、后续如何判断是否仍成立”，不替代 Issue、Sprint、OpenSpec Change 或 spec-study 报告。

决策记录采用 `docs/decision-notes/{proposed|implemented|rejected|archived}/<class>/YYYY-MM-DD-topic.md` 结构，应用到模板时只交付目录规范和 `.gitkeep`，不交付当前项目实际决策记录。

## 文档层级与事实归属

更新 `rules/document-governance.md`，补充：

- 每类事实只有一个长期事实源。
- 入口文档只放站立规则和路由。
- 规则文档放可执行约束。
- spec logs 放一次命令的证据和结果。
- OpenSpec Change 放待实施或实施中的变更事实。
- 冗余说明改为链接，不复制整段规则。

## 治理检查聚合器

新增 `scripts/run-governance-checks.py`，提供根项目只读校验聚合入口，默认运行：

- `validate-agent-context-budget.py`
- `validate-openspec-language.py`
- `validate-directory-structure.py`

脚本只编排现有校验，不改变校验语义，不写入治理资产。

## 模板同步

会影响未来生成项目的规范和脚本同步到：

- `pm-harness/`
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/`

当前项目运行态报告、Change、Sprint 不同步进模板。
