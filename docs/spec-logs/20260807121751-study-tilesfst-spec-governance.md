---
created_at: 2026-08-07 12:17:51
updated_at: 2026-08-07 12:17:51
---

# TilesFST Spec Governance Study

## 学习对象

- 学习对象：`<local-project>/ProjectTilesFST`
- 学习模式：`auto`
- 重点范围：`.agents/skills/spec-opt`、`.agents/skills/spec-study`、`AGENTS.md`、`rules/`、`scripts/`
- 执行时间：2026-08-07 12:17:51

## 学习到的治理能力

- `spec-study` 两阶段跨项目学习流程：先只读学习并输出候选清单，用户确认后再应用到本项目治理资产。
- 学习对象只读保护：禁止对学习对象执行写入、格式化、安装、迁移、清理、提交、分支或重置。
- `spec-opt` 治理日志机制：规范、技能、脚本、目录边界或校验规则迭代后统一沉淀到 `docs/spec-logs/`。
- `spec-study` 与 `spec-opt` 日志分流：学习报告使用 `YYYYMMDDhhmmss-study-xxx.md`，治理迭代日志使用 `YYYYMMDDhhmmss-governance-xxx.md`。
- Agent 目录转写原则：外部项目存在多种 Agent 入口时，应用到本项目必须转写到 `.agents/skills/`、`rules/`、`docs/` 或 `scripts/`，不得恢复其他 Agent 目录。

## 已采纳内容

- 新增 `/spec-study` 技能，作为 PmHarness 跨项目 Harness 学习应用入口。
- 扩展 `/spec-opt`，要求治理优化落盘 `docs/spec-logs/YYYYMMDDhhmmss-governance-xxx.md`。
- 新增 `docs/spec-logs/`，用于规范学习报告和治理迭代日志。
- 更新 `AGENTS.md`、目录规范、文档治理规范和上下文预算规范，使 `spec-study`、`spec-opt` 与日志目录进入项目入口和校验边界。
- 更新目录结构与上下文预算校验脚本，使 `docs/spec-logs/` 和 `spec-study` 进入自动校验。
- 同步更新 init-skill 模板资产和默认命令目录，确保后续初始化项目保持一致。

## 未采纳内容

- 未恢复 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/` 等外部 Agent 目录；本项目继续只保留 `.agents/skills/` 作为唯一技能入口。
- 未复制学习对象的业务实现、业务文档、正式规格或项目专有流程；本次只迁移通用 Harness 治理能力。
- 未新增重复的 governance 日志；本次是跨项目学习应用流程，正式记录使用本 study 报告。

## 更新文件

- `pm-harness/.agents/skills/spec-study/SKILL.md`：新增跨项目学习应用命令。
- `pm-harness/.agents/skills/spec-opt/SKILL.md`：补齐治理日志和 Sprint 编号约束。
- `pm-harness/AGENTS.md`：登记 `/spec-study` 命令和 `docs/spec-logs/` 日志位置。
- `pm-harness/rules/directory-structure.md`：登记 `docs/spec-logs/` 归属边界。
- `pm-harness/rules/document-governance.md`：补充规范学习/治理迭代日志的 docs 治理规则。
- `pm-harness/rules/agent-context-budget.md`：补充 `spec-study` 与 `spec-opt` 的聚焦读取和日志落盘要求。
- `pm-harness/scripts/validate-directory-structure.py`：新增 `docs/spec-logs` 必备目录。
- `pm-harness/scripts/validate-agent-context-budget.py`：新增 `spec-study` 命令技能识别。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/**`：同步模板资产。
- `pm-harness-skills/pm-harness-init/references/default-command-catalog.md`：同步默认命令目录。

## 影响范围

- API：无业务 API 影响。
- 数据库：无 schema、migration 或运行时数据影响。
- Web：无业务页面或构建产物影响。
- 小程序：无发布包、配置或业务实现影响。
- 管理端：无业务实现影响。
- Orval：无客户端生成影响。
- Docker Compose：无编排行为影响。
- 测试：仅涉及治理校验脚本。

## 校验计划

- `python pm-harness/scripts/validate-template-sync.py`
- `python pm-harness/scripts/validate-directory-structure.py`
- `python pm-harness/scripts/validate-skill-package.py`
- `python pm-harness/scripts/validate-agent-context-budget.py`
- `python pm-harness/scripts/validate-release.py`
- `python pm-harness/scripts/validate-mintlify-site.py`
- `python -m py_compile pm-harness/scripts/validate-directory-structure.py pm-harness/scripts/validate-agent-context-budget.py`

## 学习对象只读保护

- 本次对学习对象只执行只读文件检索、读取和 Git diff 检查。
- 未在学习对象路径下执行写入、格式化、安装、迁移、清理、提交、分支、重置或测试修复命令。
- 复核时发现学习对象工作树存在未提交 diff；本次未对其进行修改或回滚。

## 后续建议

- 后续执行 `/spec-study <path> --focus <topic>` 时，先输出候选学习项并等待确认，再应用到本项目。
- 后续执行 `/spec-opt` 时，若完成治理资产修改，应更新或新增 `docs/spec-logs/YYYYMMDDhhmmss-governance-xxx.md`。
