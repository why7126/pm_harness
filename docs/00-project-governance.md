---
created_at: 2026-08-07 13:13:52
updated_at: 2026-08-07 13:13:52
---

# ProjectPmHarness 工程治理边界

ProjectPmHarness 既是一个可持续演进的 Harness 工程，也是用于生成新 PM Harness 项目的脚手架。因此它的自身迭代必须走 Harness 工程闭环，但必须区分当前项目运行态数据和可交付给新项目的模板资产。

## 核心原则

1. ProjectPmHarness 自身的规范、脚本、技能、命令和模板能力变更，必须走 Harness 工程治理闭环。
2. `pm-harness/` 是脚手架模板目录，不承载当前 ProjectPmHarness 的实际项目数据。
3. 当前 ProjectPmHarness 的长期产品、架构、治理和维护说明放入根目录 `docs/`。
4. 当前 ProjectPmHarness 的需求/BUG、Sprint 和 OpenSpec 分别放入根目录 `issues/`、`iterations/`、`openspec/`。
5. 当前 ProjectPmHarness 的 spec 学习、治理优化和规范迭代日志放入根目录 `docs/spec-logs/`。
6. 只有确认应作为新项目默认能力交付的规范、脚本、技能、目录和模板文件，才同步进入 `pm-harness/` 与 init-skill 模板资产。
7. 当前项目运行中产生的过程数据、学习报告、验证日志、归档证据和本地环境信息，不得进入 `pm-harness/` 模板目录。

## 目录职责

| 路径 | 职责 | 是否承载当前项目数据 |
|---|---|---:|
| `docs/` | 当前 ProjectPmHarness 的长期产品、架构、治理和维护文档 | 是 |
| `issues/` | 当前 ProjectPmHarness 的需求和 BUG 池 | 是 |
| `iterations/` | 当前 ProjectPmHarness 的 Sprint / 迭代记录 | 是 |
| `openspec/` | 当前 ProjectPmHarness 的 OpenSpec Change、Specs 和 Archive | 是 |
| `docs/spec-logs/` | 当前 ProjectPmHarness 的 spec 学习、治理优化和规范迭代日志 | 是 |
| `.agents/skills/` | 当前仓库可直接使用的项目级技能入口 | 是 |
| `pm-harness/` | 生成新项目用的脚手架模板 | 否 |
| `pm-harness/docs/` | 新项目模板内的长期文档目录 | 否 |
| `pm-harness/docs/spec-logs/` | 新项目模板内的空 spec 日志目录 | 否 |
| `pm-harness-skills/pm-harness-init/` | 初始化新项目的 Skill 包和模板资产 | 否，除 Skill 自身维护数据外 |

## 迭代路径

普通需求、缺陷或较大治理变更 SHOULD 走完整 Harness 闭环：

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

## 同步规则

当变更只影响当前 ProjectPmHarness 自身时，更新根目录治理资产即可。

当变更会影响未来生成的新 PM Harness 项目时，MUST 同步更新：

- `pm-harness/`
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/`
- 必要时更新 `pm-harness-skills/pm-harness-init/references/`
- 本机安装版 `pm-harness-init`

同步后 SHOULD 运行：

```bash
python pm-harness/scripts/validate-template-sync.py
python pm-harness/scripts/validate-directory-structure.py
python pm-harness/scripts/validate-skill-package.py
python pm-harness/scripts/validate-agent-context-budget.py
```

## 禁止事项

- 不得把当前 ProjectPmHarness 的实际 spec 日志写入 `pm-harness/`。
- 不得把当前 ProjectPmHarness 的 Issue、Sprint、OpenSpec Change、验证报告或归档证据写入 `pm-harness/`，除非它们是新项目模板必须携带的示例或占位结构。
- 不得把根目录 `issues/`、`iterations/`、`openspec/` 同步进 `pm-harness/` 或 init-skill 模板资产。
- 不得把真实 `.env`、密钥、访问令牌、本地绝对路径、客户数据、运行时数据库或构建产物同步进模板。
- 不得恢复 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/` 等多入口 Agent 目录；本项目统一使用 `.agents/skills/`。
