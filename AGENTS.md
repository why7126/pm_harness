---
purpose: AI 行为入口
content: ProjectPmHarness 脚手架工程自身的规则加载路由、治理边界、模板同步和执行红线
source: /spec-opt add-root-agents-entrypoint
update_method: 当前脚手架工程自身治理流程、模板同步规则或技能入口变化时更新
created_at: 2026-08-07 15:23:44
updated_at: 2026-08-07 15:23:44
note: 适用于 ProjectPmHarness 仓库根目录；不得与 pm-harness/ 模板入口混用
---

# ProjectPmHarness AI Agent 工作指南

## 1. 项目定位

ProjectPmHarness 是 PM Harness 脚手架工程，用于维护：

- 生成新项目的 `pm-harness/` 模板。
- 初始化、重构和设计资产相关 Skill。
- 当前脚手架工程自身的规范、脚本、技能、文档和 OpenSpec 治理资产。

当前仓库自身也走 Harness 工程治理闭环，但必须区分“当前项目运行态数据”和“生成新项目的模板资产”。

## 2. 执行前读取路由

所有任务先读：

```text
AGENTS.md
README.md
docs/00-project-governance.md
openspec/project.md
```

按任务类型追加读取：

| 任务类型 | 追加读取 |
|---|---|
| 根项目治理变更 | `docs/README.md`、`docs/spec-logs/README.md`、相关 `openspec/changes/<change-id>/` |
| 需求 / BUG | `issues/` 相关条目；必要时参考 `pm-harness/rules/requirement-management.md`、`pm-harness/rules/bug-management.md` |
| Sprint | `rules/iterations-lifecycle.md`、`iterations/change|archive/<sprint>/`；必要时参考 `pm-harness/rules/iterations-lifecycle.md` |
| OpenSpec | `openspec/config.yaml`、`openspec/testing-mapping.md`、目标 Change 片段 |
| 命令顺序 / 工作流编排 | `docs/08-command-execution-order.md`、相关 `.agents/skills/<command>/SKILL.md` |
| 安全 / Git 检查 | `rules/security.md`、`.agents/skills/git-check/SKILL.md`、`scripts/git-check.py` |
| UI / Prototype 验收 | `rules/ui-design.md`、`docs/standards/prototype-ui-acceptance.md` |
| 问题排查 / 根因 / 返修 | `rules/root-cause-evidence.md`、相关 Change/Issue trace、验收反馈和补证材料 |
| 文档治理 / 表达卫生 | `docs/standards/document-prose-hygiene.md`、`rules/document-governance.md`、`docs/spec-logs/README.md` |
| 产品数据采集 / 链路观测 | `docs/standards/product-data-collection-observability.md`、相关 REQ/BUG/Change/Sprint 中的 `product_data_collection_observability` 声明 |
| 脚手架模板变更 | `pm-harness/` 相关文件、`pm-harness-skills/pm-harness-init/assets/pm-harness-template/` 对应文件、`pm-harness/scripts/validate-template-sync.py` |
| Skill 变更 | `.agents/skills/<command>/SKILL.md`、`pm-harness/.agents/skills/<command>/SKILL.md`、init-skill 模板中对应 `SKILL.template.md` |
| 设计资产 | `.agents/skills/pm-harness-uidesign/SKILL.md`、`design-schemes/README.md`、相关方案目录 |

读取必须遵守上下文预算：先定位文件和片段，再分段读取；不得为普通任务全量读取 `docs/**`、`issues/**`、`iterations/**`、`openspec/archive/**` 或模板 assets。

## 3. Agent 技能入口

当前仓库只维护根目录 `.agents/skills/` 作为实际可用 AI 技能入口。

`pm-harness/.agents/skills/` 是新项目模板内的技能集合。模板技能变化后，如需当前仓库立即使用，必须同步到根目录 `.agents/skills/`；不得恢复 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/` 等多入口目录。

常用治理命令：

| 域 | 命令 |
|---|---|
| 跨项目学习 | `/spec-study` |
| 治理优化 | `/spec-opt` |
| Git 安全 | `/git-check` |

## 4. 目录边界

| 路径 | 职责 |
|---|---|
| `docs/` | 当前 ProjectPmHarness 长期产品、架构、治理和维护文档 |
| `docs/spec-logs/` | 当前 ProjectPmHarness 的 spec 学习、治理优化和规范迭代日志 |
| `issues/` | 当前 ProjectPmHarness 的需求和 BUG 池 |
| `iterations/` | 当前 ProjectPmHarness 的 Sprint / 迭代记录 |
| `openspec/` | 当前 ProjectPmHarness 的 OpenSpec Change、Specs 和 Archive |
| `.agents/skills/` | 当前仓库实际可用技能入口 |
| `design-schemes/` | 可复用 UI/UE 与导航方案资产库 |
| `pm-harness/` | 生成新项目用的脚手架模板，不承载当前项目运行态数据 |
| `pm-harness-skills/` | 初始化、重构、设计资产等 Skill 源码和模板资产 |

## 5. 治理流程

当前脚手架工程自身的普通需求、缺陷或较大治理变更 SHOULD 走：

```text
/capture -> /req-* 或 /bug-* -> /sprint-propose -> /opsx-propose -> /opsx-apply -> /opsx-archive -> /sprint-archive
```

纯规范、脚本、技能或命令优化 MAY 走：

```text
/spec-opt <治理优化目标>
```

跨项目学习应用 MAY 走：

```text
/spec-study <学习对象>
/spec-study apply <已确认候选项>
```

`/spec-opt` 和 `/spec-study apply` 产生的日志统一写入 `docs/spec-logs/`。

命令下一步推荐 MUST 遵守 `docs/08-command-execution-order.md`。当命令需要用户选择、确认、补充信息或处理阻塞时，SHOULD 使用“结构化选项 + 推荐项 + 可补充说明”的引导式反馈；每轮聚焦 1-3 个关键决策。

## 6. 模板同步规则

当变更会影响未来生成的新 PM Harness 项目时，必须同步：

- `pm-harness/`
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/`
- 必要时更新 `pm-harness-skills/pm-harness-init/references/`
- 本机安装版 `/Users/why7126/.codex/skills/pm-harness-init`

同步后运行：

```bash
python pm-harness/scripts/validate-template-sync.py
python pm-harness/scripts/validate-directory-structure.py
python pm-harness/scripts/validate-skill-package.py
python pm-harness/scripts/validate-agent-context-budget.py
```

## 7. 强制红线

- 不得把当前 ProjectPmHarness 的实际 Issue、Sprint、OpenSpec Change、spec 日志、验证报告或归档证据写入 `pm-harness/` 模板目录。
- 不得把根目录 `issues/`、`iterations/`、`openspec/` 同步进 `pm-harness/` 或 init-skill 模板资产。
- 不得把真实 `.env`、密钥、访问令牌、本机绝对路径、客户数据、运行时数据库、依赖目录或构建产物同步进模板。
- 提交或推送前 SHOULD 运行 `python scripts/git-check.py`；发现真实 env、运行时数据、密钥、连接串或本机路径阻断项时不得继续提交。
- 不得恢复多 Agent 入口目录；只使用 `.agents/skills/`。
- 不得绕过 OpenSpec Change 直接修改正式规格 `openspec/specs/`。
- 不得修改 ProjectTilesFST 等学习对象的文件、Git 状态、依赖、缓存或生成物。
- 问题排查、BUG 完善、实现返修或效果不如预期时，必须遵守证据化根因分析治理；证据不足不得确认根因，必须输出人工补证步骤。
- 涉及 API、DB、日志审计、行为埋点、Task Trace、Web / 小程序 / App 请求封装或工作流治理的数据采集变更，MUST 按 `docs/standards/product-data-collection-observability.md` 声明 `product_data_collection_observability`、`affected_layers`、`reason`、`validation`；不适用时 MUST 写明 N/A 或 `not_applicable` 原因。

## 8. 输出契约

命令型任务完成时，最终回复必须包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <需要用户选择、确认、补充或处理的事项；若没有则写“无”>
```
