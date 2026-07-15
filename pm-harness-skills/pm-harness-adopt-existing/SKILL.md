---
name: pm-harness-adopt-existing
description: 将 ProjectSoulKing 优化后的 PM Harness / OpenSpec + AI Agent 规范工程非破坏式接入存量项目。凡用户要把 harness 工程应用到已有代码仓库、迁移存量项目到 pm-harness、给旧项目补齐 AGENTS/rules/docs/issues/iterations/openspec/commands/skills，或把 ProjectSoulKing Harness 优化成果落到现有项目中时必须使用；重点是先盘点现状、保护业务代码、按需合并治理资产、项目化渲染文档并完成校验，而不是覆盖式初始化。
---

# PM Harness 存量项目接入技能

## 目标

把 ProjectSoulKing 优化后的 Harness 工程能力接入一个已有项目，让项目获得一致的 AI 协作入口、工程规则、需求/Bug/迭代/OpenSpec 治理、Agent 命令和质量校验，同时不破坏现有源码、构建脚本、文档、CI 和团队约定。

这个技能处理的是“存量项目改造”，不是新项目初始化。核心判断标准：

- 先理解现有项目，再迁移 Harness 结构。
- 只引入项目需要的治理能力，不把模板全量倾倒进去。
- 对已有文件做合并或补丁，避免覆盖用户已有内容。
- 所有模板痕迹、来源项目残留和不确定项都必须在交付前清理或集中管理。

## 资产来源

优先复用相邻的初始化技能资产：

| 路径 | 用途 |
|---|---|
| `../pm-harness-init/assets/pm-harness-template/` | Harness 目录、文档、规则、脚本、Agent 命令事实源 |
| `../pm-harness-init/assets/templates/` | 需求、Bug、追踪记录模板 |
| `../pm-harness-init/references/user-input-schema.md` | 项目信息、能力派生和默认值 |
| `../pm-harness-init/references/agent-tool-mapping.md` | Agent 工具目录和命令同步规则 |
| `../pm-harness-init/references/default-command-catalog.md` | 默认命令族和条件启用规则 |
| `references/adoption-checklist.md` | 存量接入执行清单 |

如果相邻初始化资产不存在，先说明缺失资产，再从当前仓库内已有 `pm-harness`、`AGENTS.md`、`rules/`、`docs/`、`.codex/`、`.claude/`、`.agents/` 等文件中提取可复用结构。

## 必读引用

在执行迁移前完整读取：

1. `references/adoption-checklist.md`
2. `../pm-harness-init/references/user-input-schema.md`
3. `../pm-harness-init/references/agent-tool-mapping.md`
4. `../pm-harness-init/references/default-command-catalog.md`

如果用户只要求“生成接入方案”而不是实际改文件，也要读取接入清单，但可以不读取全部模板文件。

## 接入原则

### 保护存量项目

- 不删除、重命名或移动现有业务源码，除非用户明确要求。
- 不覆盖已有 `README.md`、`AGENTS.md`、`project.yaml`、`docs/`、`rules/`、`.codex/`、`.claude/`、`.cursor/`、`.kiro/`、`.opencode/`、`.agents/` 内容；先读取并合并。
- 遇到命名冲突时优先补丁式合并；无法安全合并时生成 `docs/harness-adoption/conflicts.md` 记录冲突、建议处理方式和需要用户决策的点。
- 不改动真实密钥、生产配置、数据库迁移历史或 CI 发布权限。

### 保持项目真实

- Harness 文档必须基于现有代码、配置、包管理器、端口、服务、测试命令和部署方式生成。
- 不知道的信息不要编造；阻塞决策集中写入 `docs/pending-decisions.md` 或 `docs/harness-adoption/pending-decisions.md`。
- 不保留 `[通用]`、`[个性化]`、`[条件启用]`、`template_scope`、生成参数表、初始化说明、来源项目名、来源端口、来源账号、来源 bucket、来源接口或散落的 `待确认`。

### 能力裁剪

- 根据现有项目实际启用的端、服务、数据库、对象存储、算法、部署方式和 Agent 工具裁剪 Harness 资产。
- 仅生成用户已使用或明确需要的 Agent 工具目录；例如只用 Codex 就只生成 `.codex/` 和可通用的 `.agents/`，不顺手添加其他工具目录。
- OpenSpec、需求/Bug/迭代治理默认可以接入；如果项目极小或用户要求轻量模式，可以只接入 `AGENTS.md`、`rules/`、`docs/` 和基础校验。

## 执行流程

### 1. 盘点现状

先收集足够上下文，再动文件：

- 查看 `git status --short`，识别用户已有未提交改动。
- 用 `rg --files` 找到入口文档、包管理器文件、源码目录、测试目录、CI、Docker、部署配置、Agent 目录和已有规范文档。
- 阅读关键文件：`README*`、`AGENTS.md`、`package.json`、`pyproject.toml`、`requirements*.txt`、`go.mod`、`Cargo.toml`、`docker-compose*.yml`、`.github/workflows/*`、现有 `.codex/` / `.claude/` / `.agents/` 资产。
- 识别项目名称、业务域、目标用户、产品形态、核心能力、技术栈、本地命令、测试命令、部署方式、端口、数据存储和 AI 工具。

输出或内部形成一份接入摘要：现有能力、建议接入范围、冲突风险、需要用户确认的阻塞项。

### 2. 选择接入模式

根据用户意图和项目规模选择一种模式：

| 模式 | 适用场景 | 交付重点 |
|---|---|---|
| `minimal` | 小项目、试点、用户想先轻量接入 | `AGENTS.md`、核心 `rules/`、`docs/harness-adoption/`、基础脚本 |
| `standard` | 大多数存量业务项目 | `AGENTS.md`、`project.yaml`、`rules/`、`docs/`、`issues/`、`iterations/`、`openspec/`、Agent 命令 |
| `full` | 准备长期以 Harness 治理项目 | 标准模式 + compatibility、standards、workflow sync、完整校验和命令同步 |

用户未指定时默认 `standard`，但如果仓库很小或缺少测试/部署结构，可降级为 `minimal` 并说明原因。

### 3. 生成接入计划

实施前建立清晰计划，至少覆盖：

- 将新增哪些目录和文件。
- 将合并哪些已有文件。
- 哪些模板资产会被裁剪。
- 哪些命令、端口、测试和部署信息来自现有项目。
- 哪些冲突或未知项会进入集中决策文档。
- 验证命令和预期结果。

如果用户要求直接执行，可以把计划作为简短工作说明后继续实施；不必反复追问非阻塞细节。

### 4. 应用 Harness 资产

按计划迁移：

- 创建缺失的治理目录：`rules/`、`docs/`、`issues/`、`iterations/`、`openspec/`、`scripts/`、`compatibility/`、`tests/` 中必要部分。
- 合并或生成 `AGENTS.md`，让它成为 AI 执行入口，指向现有项目事实源和新增 Harness 规则。
- 生成或更新 `project.yaml`，用结构化字段记录实际项目事实；布尔值必须为 true/false。
- 生成或补齐 `docs/README.md`、产品概览、架构、部署、API、数据库、测试、兼容性等文档，内容必须来自现有项目。
- 接入 `rules/`，并删除不适用技术栈的规则或章节。
- 接入 `issues/requirements`、`issues/bugs`、`iterations`、`openspec` 目录和模板，保留 `.gitkeep` 与 registry。
- 根据 `agent-tool-mapping.md` 同步 `.codex/`、`.claude/`、`.cursor/`、`.kiro/`、`.opencode/`、`.agents/skills/` 中实际启用的命令和技能。
- 添加 `docs/harness-adoption/`，记录接入摘要、冲突、裁剪项、后续任务和未决策项。

### 5. 清理模板痕迹

交付前检查并修复：

- 删除模板标记：`[通用]`、`[个性化]`、`[条件启用]`、`【通用】`、`【个性化】`、`【条件启用】`。
- 删除模板元信息：生成参数、初始化参数、初始化说明、模板模块构成、抽象模板、Token 优化模板。
- 删除来源项目痕迹，尤其是 ProjectSoulKing 示例名、服务名、端口、账号、路径、bucket、表名和 API 示例。
- 删除不适用能力的整节、整表行、测试矩阵、命令和规则。
- 把真实阻塞项集中到 pending decisions 文档，不让 `待确认` 散落在 README、AGENTS、YAML、规则或命令中。

### 6. 验证

至少执行：

```bash
python scripts/validate-directory-structure.py
python scripts/validate-generated-docs.py --strict
```

如果项目没有这些脚本，优先从 Harness 资产接入脚本；如果接入模式过轻而没有脚本，要用 `rg` 手动检查模板痕迹和散落待确认。

还要运行现有项目最可信的验证命令，例如：

- Node 项目：`npm test`、`pnpm test`、`npm run lint`、`pnpm run build`
- Python 项目：`pytest`、`ruff check`、`mypy`
- Docker 项目：`docker compose config`

无法运行时说明原因，不把未验证说成已通过。

## 交付格式

完成后用简短中文说明：

- 接入模式。
- 新增/更新的关键文件。
- 已保留的存量项目事实。
- 验证结果。
- 仍需用户决策的事项。

如果只生成方案，不改文件，则输出“接入计划 + 风险清单 + 推荐执行顺序”，不要假装已经完成迁移。
