# Agent 技能入口

## 使用规则

- 初始化项目只生成 `.agents/skills/`。
- 输出工程中的 `.agents/skills/<command-name>/SKILL.md` 是命令语义的唯一事实源。
- init-skill 模板资产内使用 `.agents/skills/<command-name>/SKILL.template.md` 存放模板，生成工程时必须重命名或渲染为 `SKILL.md`。
- 不生成、同步或保留 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/`。
- 新增命令时，在模板资产中新增 `.agents/skills/<command-name>/SKILL.template.md`，在输出工程中生成 `.agents/skills/<command-name>/SKILL.md`，并同步 `references/default-command-catalog.md`、`AGENTS.md`、`README.md` 和相关规则。

## 输出检查

- `.agents/skills/` 存在。
- 模板资产内不存在嵌套 `SKILL.md`；输出工程内不存在 `SKILL.template.md`。
- `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/` 不存在。
- `README.md`、`AGENTS.md`、`project.yaml`、`rules/directory-structure.md` 不再引用兼容工具目录。
