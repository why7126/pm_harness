---
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-10 23:19:03
---

# 应用 ProjectMoonBox 治理模式

## 背景

`/spec-study ProjectMoonBox` 已完成只读学习，并确认应用以下候选项：

- `git-check-security-gate`
- `issues-changelog-current-state`
- `command-execution-order`
- `prototype-ui-acceptance`
- `spec-study-log-first-learning`
- `guided-command-feedback`

这些内容属于治理扩展、命令新增、脚本校验行为和模板默认能力变化，必须通过 active OpenSpec Change 承载，并纳入 Sprint scope。

## 目标

- 为 ProjectPmHarness 根项目和新项目模板补齐推送前 Git 安全检测能力。
- 为 REQ/BUG 目录补齐当前态看板索引边界。
- 固化命令执行顺序与下一步参数规则。
- 补齐原型驱动 UI 验收专项标准。
- 强化 `/spec-study` 日志优先学习顺序。
- 为命令型 Skill 增加引导式反馈契约。

## 非目标

- 不修改学习对象 ProjectMoonBox。
- 不修改 `src/` 业务代码。
- 不直接修改 `openspec/specs/` 正式规格。
- 不复制 ProjectMoonBox 的业务事实、运行时数据或源码实现。

## 影响范围

- 根项目治理入口、规则、文档、脚本和 OpenSpec Change。
- `pm-harness/` 新项目模板。
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 初始化模板资产。
- 不影响 API、数据库、Web、小程序、管理端、Orval 或运行时代码。
