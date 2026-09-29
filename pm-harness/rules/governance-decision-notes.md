---
purpose: 治理决策记录规范
content: 记录非平凡治理变更的动机、取舍、状态和归档边界
created_at: 2026-08-19 11:25:48
updated_at: 2026-08-19 11:25:48
---

# 治理决策记录规范

治理决策记录用于沉淀项目中非平凡治理变更的长期理由，包括规范、脚本、Skill、目录边界、模板能力和校验策略。它记录“为什么这样做、放弃了什么、何时重新评估”，不替代 Issue、Sprint、OpenSpec Change、spec-study 报告或提交记录。

## 适用范围

以下变更 SHOULD 新增或更新治理决策记录：

- 新增、删除或重构治理流程、命令 Skill、校验脚本或目录边界。
- 改变模板同步、安全检查、OpenSpec 校验、Sprint 编排或上下文预算策略。
- 引入会影响多个命令、多个目录或未来生成项目的长期规范。
- 拒绝一个有诱惑力但不适合当前项目的治理方案，且后续可能被再次提出。

纯错别字、单文件局部说明、一次性学习报告、已由 active Change 充分覆盖且没有长期取舍的修改 MAY 不写治理决策记录。

## 目录结构

治理决策记录存放在：

```text
docs/decision-notes/
├── proposed/
├── implemented/
├── rejected/
└── archived/
```

每条记录路径使用：

```text
docs/decision-notes/<lifecycle>/<class>/YYYY-MM-DD-topic.md
```

`lifecycle` 取值：

| 生命周期 | 含义 |
|---|---|
| `proposed` | 已提出但未落地的治理方案 |
| `implemented` | 已落地并仍是当前事实的治理决策 |
| `rejected` | 已明确不采纳、但值得保留原因的方案 |
| `archived` | 已实现但长期指导价值较低的冻结历史 |

`class` 取值：

| 分类 | 适用内容 |
|---|---|
| `process` | 命令顺序、工作流、Sprint/OpenSpec 编排、发布流程 |
| `documentation` | 文档层级、事实归属、报告、索引、公开安全 |
| `scripts` | 校验脚本、同步脚本、生成脚本和聚合检查 |
| `skills` | `.agents/skills/` 命令行为和 Skill 契约 |
| `template` | 模板默认能力 |
| `security` | 密钥、环境、本地路径、客户数据和推送前安全边界 |

## 文件格式

每条记录 MUST 包含 Frontmatter，并按生命周期使用对应结构。

`proposed`：

```markdown
# Decision Note: <标题>

Status: proposed

## Problem
## Proposal
## Alternatives considered
## Acceptance criteria
## Risks
```

`implemented`：

```markdown
# Decision Note: <标题>

Status: implemented

## Problem
## Decision
## Alternatives considered
## Consequences
```

`rejected`：

```markdown
# Decision Note: <标题>

Status: rejected - <一句话原因>

## Problem
## Proposal
## Alternatives considered
## Consequences
```

## 边界

- 决策记录描述当前项目治理决策，不得包含学习对象源码、用户隐私、客户数据、密钥、未脱敏日志或本机绝对路径。
- `archived/` 下记录视为冻结历史，除修复索引链接或归档元信息外不做内容现代化。
- 同一事实只保留一个长期事实源。决策记录保存理由和取舍；执行状态在 OpenSpec Change、Sprint、Issue 或 spec-study 报告中维护。
