---
created_at: 2026-08-07 15:10:22
updated_at: 2026-08-07 15:10:22
---

# TilesFST Spec Opt And Study Refresh

## 学习对象

- 学习对象：`<local-project>/ProjectTilesFST`
- 学习模式：`auto`
- 重点范围：`.agents/skills/spec-opt`、`.agents/skills/spec-study`、`docs/spec-logs/README.md`、相关规则和校验脚本。
- 执行时间：2026-08-07 15:10:22

## 学习到的治理能力

- `docs/spec-logs/README.md` 应作为规范工程日志目录说明，集中描述命名、去重和隐私边界。
- 模板同步校验应同步 `docs/spec-logs/README.md`，但不应把时间戳开头的实际 `study` 或 `governance` 日志同步进脚手架模板。
- `/spec-study` 的学习应用结果应汇总到同一份 `study` 报告，避免重复生成内容相近的 `governance` 日志。

## 已采纳内容

- 为当前 ProjectPmHarness 新增 `docs/spec-logs/README.md`。
- 为 `pm-harness/` 脚手架模板新增 `docs/spec-logs/README.md`。
- 调整模板同步脚本，使其只忽略 `docs/spec-logs/YYYYMMDDhhmmss-(study|governance)-*.md` 运行日志，不再忽略 `README.md`。
- 同步更新 init-skill 模板资产中的模板同步脚本。

## 未采纳内容

- 未复制 TilesFST 的具体业务日志、业务规格或项目专有内容。
- 未改变 ProjectPmHarness 已确定的根级 `docs/spec-logs/` 位置。
- 未恢复任何非 `.agents/skills/` 的 Agent 入口目录。

## 更新文件

- `docs/spec-logs/README.md`：新增当前项目规范工程日志说明。
- `pm-harness/docs/spec-logs/README.md`：新增新项目模板中的规范工程日志说明。
- `pm-harness/scripts/validate-template-sync.py`：调整运行日志忽略规则。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/scripts/validate-template-sync.py`：同步模板资产校验规则。

## 影响范围

- API：无影响。
- 数据库：无影响。
- Web：无影响。
- 小程序：无影响。
- 管理端：无影响。
- Orval：无影响。
- Docker Compose：无影响。
- 测试：仅影响治理校验脚本。

## 校验计划

- `python pm-harness/scripts/validate-template-sync.py`
- `python pm-harness/scripts/validate-directory-structure.py`
- `python pm-harness/scripts/validate-skill-package.py`
- `python pm-harness/scripts/validate-agent-context-budget.py`

## 学习对象只读保护

- 本次对学习对象只执行只读文件检索和读取。
- 未在学习对象路径下执行写入、格式化、安装、迁移、清理、提交、分支、重置或测试修复命令。

## 后续建议

- 后续新增 spec 日志目录规则时，优先更新 `docs/spec-logs/README.md`、`spec-opt`、`spec-study` 和模板同步脚本。
