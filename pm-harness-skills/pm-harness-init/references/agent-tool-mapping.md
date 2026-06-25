# Agent 工具映射

## 使用规则

- 构建 Agent 工具目录前必须完整读取本文档。
- 只生成 `ENABLED_AGENT_TOOLS` 中启用的工具目录；默认只生成 `Codex` 目录。
- 所有已启用工具必须保持同名命令的阶段、输入、输出、文档/代码边界一致。

## 名称标准化

| 用户输入 | 标准化名称 | 输出目录 |
|---|---|---|
| Claude Code、Claude、ClaudeCode | `Claude Code` | `.claude/` |
| Cursor | `Cursor` | `.cursor/` |
| Codex | `Codex` | `.codex/` |
| OpenCode、Open Code | `OpenCode` | `.opencode/` |
| Kiro | `Kiro` | `.kiro/` |

## 事实源和渲染规则

`assets/pm-harness-template/.claude/` 是命令和 OpenSpec Skill 样本的唯一模板事实源。`PRIMARY_AGENT_TOOL` 决定输出项目的主要入口；其它已选工具均从该模板语义生成，保证命令一致。

| 启用工具 | 命令生成 | OpenSpec Skill 生成 |
|---|---|---|
| Claude Code | `.claude/commands/{group}/*.md` 按项目参数更新 | 将 `.claude/skills/*/SKILL.template.md` 渲染为 `.claude/skills/*/SKILL.md` |
| Cursor | 从 `.claude/commands/` 生成 `.cursor/commands/{flat-command}.md` | 渲染为 `.cursor/skills/*/SKILL.md` |
| Codex | 从 `.claude/commands/` 生成 `.codex/prompts/{flat-command}.md` | 渲染为 `.codex/skills/*/SKILL.md` |
| OpenCode | 从 `.claude/commands/` 生成 `.opencode/commands/{flat-command}.md` | 渲染为 `.opencode/skills/*/SKILL.md` |
| Kiro | 从 `.claude/commands/` 生成 `.kiro/prompts/{flat-command}.prompt.md` | 渲染为 `.kiro/skills/*/SKILL.md` |

`flat-command` 例如 `req-capture`、`bug-review`、`opsx-apply`。允许调整目录、后缀和 frontmatter，不得改变命令语义。

## Claude Code 未启用

若 `Claude Code` 未包含在 `ENABLED_AGENT_TOOLS` 中，仍可在生成过程中使用 `.claude/` 样本；其它已启用工具生成完成后，必须从最终输出删除 `.claude/`。

## 输出检查

- `ENABLED_AGENT_TOOLS` 已写入 README、AGENTS、project.yaml 和 rules。
- 启用工具目录存在，未启用工具目录不存在。
- 非 Claude Code 目录基于 `.claude/` 语义生成。
- 输出项目中的嵌套 Skill 使用 `SKILL.md`；pm-harness-init 自身只允许存在根 `SKILL.md`。
