---
name: pm-harness-refactor
description: 将已优化的 PM Harness / OpenSpec + AI Agent 规范工程非破坏式接入、重构或治理化改造存量项目。凡用户要把 harness 工程应用到已有代码仓库、迁移存量项目到 pm-harness、给旧项目补齐 AGENTS/rules/docs/issues/iterations/openspec/commands/skills，或把 Harness 优化成果落到现有项目中时必须使用；重点是先盘点现状、保护业务代码、按需合并治理资产、项目化渲染文档并完成校验，而不是覆盖式初始化。
---

# PM Harness 存量项目接入技能

## 目标

把已优化的 Harness 工程能力接入一个已有项目，让项目获得一致的 AI 协作入口、工程规则、需求/Bug/迭代/OpenSpec 治理、Agent 命令和质量校验，同时不破坏现有源码、构建脚本、文档、CI 和团队约定。

当用户指定的输出目录不是旧项目源码目录本身，而是一个新的整合目录时，本技能必须把旧项目业务源码非破坏式整合到输出目录中。Harness 治理资产和旧业务源码必须同处一个可交付工程，不能只生成文档、规则和空的 `src/` 占位目录。

这个技能处理的是“存量项目改造”，不是新项目初始化。核心判断标准：

- 先理解现有项目，再迁移 Harness 结构。
- 新输出目录场景下，先复制或镜像旧业务源码，再让 Harness 文档、规则和验证命令指向复制后的项目内路径。
- 只引入项目需要的治理能力，不把模板全量倾倒进去。
- 对已有文件做合并或补丁，避免覆盖用户已有内容。
- 所有模板痕迹、来源项目残留和不确定项都必须在交付前清理或集中管理。

## 目录结构

本 skill 参照 `pm-harness-init` 组织为完整、自包含的 Harness 改造包：

```text
pm-harness-refactor/
├── SKILL.md
├── assets/
│   ├── pm-harness-template/
│   └── templates/
└── references/
    ├── adoption-checklist.md
    ├── agent-entrypoint.md
    ├── default-command-catalog.md
    └── user-input-schema.md
```

## 资产

| 路径 | 用途 |
|---|---|
| `assets/pm-harness-template/` | Harness 目录、文档、规则、脚本、Agent 命令事实源 |
| `assets/templates/` | 需求和 Bug 记录模板 |
| `references/adoption-checklist.md` | 存量接入执行清单 |
| `references/user-input-schema.md` | 项目信息、能力派生和默认值 |
| `references/agent-entrypoint.md` | `.agents/skills/` 单一 Agent 技能入口规则 |
| `references/default-command-catalog.md` | 默认命令族和条件启用规则 |

执行时必须使用本 skill 自带资产，不得从零捏造核心结构。若资产缺失，先说明缺失项，再从当前仓库内已有 `pm-harness`、`AGENTS.md`、`rules/`、`docs/`、`.agents/` 等文件中提取可复用结构。

## 必读引用

在执行迁移前完整读取：

1. `references/adoption-checklist.md`
2. `references/user-input-schema.md`
3. `references/agent-entrypoint.md`
4. `references/default-command-catalog.md`

如果用户只要求“生成接入方案”而不是实际改文件，也要读取接入清单，但可以不读取全部模板文件。

## 接入原则

### 保护存量项目

- 不删除、重命名或移动现有业务源码，除非用户明确要求。
- 可以把旧业务源码复制到用户指定的输出目录；复制动作不得改动旧目录本身。
- 不覆盖已有 `README.md`、`AGENTS.md`、`project.yaml`、`docs/`、`rules/`、`.agents/` 内容；先读取并合并。
- 遇到命名冲突时优先补丁式合并；无法安全合并时生成 `docs/harness-adoption/conflicts.md` 记录冲突、建议处理方式和需要用户决策的点。
- 不改动真实密钥、生产配置、数据库迁移历史或 CI 发布权限。

### 整合旧业务源码

当用户提供旧项目目录和独立输出目录时，必须执行源码整合：

- 将后端源码复制到输出目录内的稳定路径，例如 `src/backend/`。
- 将小程序、Web、移动端等前端源码复制到输出目录内的稳定路径，例如 `src/wechat-miniapp/`、`src/web/`。
- 复制后，`project.yaml`、`AGENTS.md`、`docs/01-architecture.md`、`docs/02-deployment.md`、`docs/03-api-index.md`、`docs/04-database-design.md`、`rules/directory-structure.md` 必须指向输出工程内路径，而不是只指向旧目录。
- 旧目录路径只能作为 `source_import.origin_path` 或接入记录出现，用于审计来源；不应成为日常开发主路径。
- 不复制运行时产物、缓存、大体积媒体、数据库文件、日志、虚拟环境、构建产物和系统文件，例如 `__pycache__/`、`.pytest_cache/`、`node_modules/`、`.venv/`、`venv/`、`dist/`、`build/`、`static/` 收集产物、`media/` 生产素材、`*.log`、`*.sqlite3`、`db.sqlite3`、`.DS_Store`。
- 发现疑似密钥配置文件时，不得把真实密钥扩散到新增文档；是否复制原文件取决于用户目标：
  - 若用户要求可运行迁移，复制源码文件但必须额外生成安全替代方案和 `docs/pending-decisions.md` 风险项。
  - 若用户要求安全优先交付，复制为 `.example` 或在输出目录中生成脱敏版本，并把原文件处理记录写入 `docs/harness-adoption/conflicts.md`。
- 复制完成后必须生成 `docs/harness-adoption/source-import.md`，记录来源目录、目标目录、包含项、排除项、敏感配置处理、媒体/数据库文件处理和验证结果。

### 保持项目真实

- Harness 文档必须基于现有代码、配置、包管理器、端口、服务、测试命令和部署方式生成。
- 不知道的信息不要编造；阻塞决策集中写入 `docs/pending-decisions.md` 或 `docs/harness-adoption/pending-decisions.md`。
- 不保留 `[通用]`、`[个性化]`、`[条件启用]`、`template_scope`、生成参数表、初始化说明、来源项目名、来源端口、来源账号、来源 bucket、来源接口或散落的 `待确认`。

### 能力裁剪

- 根据现有项目实际启用的端、服务、数据库、对象存储、算法、部署方式和 Agent 工具裁剪 Harness 资产。
- 只保留 `.agents/skills/` 作为 Agent 技能入口；不得生成 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/` 等兼容工具目录。
- OpenSpec、需求/Bug/迭代治理默认可以接入；如果项目极小或用户要求轻量模式，可以只接入 `AGENTS.md`、`rules/`、`docs/` 和基础校验。

## 执行流程

### 1. 盘点现状

先收集足够上下文，再动文件：

- 查看 `git status --short`，识别用户已有未提交改动。
- 用 `rg --files` 找到入口文档、包管理器文件、源码目录、测试目录、CI、Docker、部署配置、Agent 目录和已有规范文档。
- 阅读关键文件：`README*`、`AGENTS.md`、`package.json`、`pyproject.toml`、`requirements*.txt`、`go.mod`、`Cargo.toml`、`docker-compose*.yml`、`.github/workflows/*`、现有 `.agents/` 资产。
- 识别项目名称、业务域、目标用户、产品形态、核心能力、技术栈、本地命令、测试命令、部署方式、端口、数据存储和 AI 工具。
- 如果用户给出独立输出目录，判断旧源码应映射到哪些输出路径，并记录复制排除规则、敏感配置处理策略和目标目录是否已有冲突文件。

输出或内部形成一份接入摘要：现有能力、建议接入范围、冲突风险、需要用户确认的阻塞项。

### 2. 选择接入模式

根据用户意图和项目规模选择一种模式：

| 模式 | 适用场景 | 交付重点 |
|---|---|---|
| `minimal` | 小项目、试点、用户想先轻量接入 | `AGENTS.md`、核心 `rules/`、`docs/harness-adoption/`、基础脚本 |
| `standard` | 大多数存量业务项目 | `AGENTS.md`、`project.yaml`、`rules/`、`docs/`、`issues/`、`iterations/`、`openspec/`、`.agents/skills/` |
| `full` | 准备长期以 Harness 治理项目 | 标准模式 + compatibility、standards、workflow sync、完整校验和命令同步 |

用户未指定时默认 `standard`，但如果仓库很小或缺少测试/部署结构，可降级为 `minimal` 并说明原因。

### 3. 生成接入计划

实施前建立清晰计划，至少覆盖：

- 将新增哪些目录和文件。
- 将复制哪些旧业务源码目录到输出工程内的哪些路径。
- 将排除哪些运行时、缓存、媒体、数据库、日志和构建产物。
- 如何处理疑似密钥配置文件、生产配置和 `.env`。
- 将合并哪些已有文件。
- 哪些模板资产会被裁剪。
- 哪些命令、端口、测试和部署信息来自现有项目。
- 哪些冲突或未知项会进入集中决策文档。
- 验证命令和预期结果。

如果用户要求直接执行，可以把计划作为简短工作说明后继续实施；不必反复追问非阻塞细节。

### 4. 应用 Harness 资产

按计划迁移：

- 如果输出目录不是旧源码目录本身，先把旧业务源码复制到输出目录内的 `src/` 子目录；不得只创建空 `src/` 占位。
- 复制源码时保留相对结构、业务代码、迁移文件、配置样例和项目配置，排除运行时产物、缓存、大文件媒体、数据库、日志、虚拟环境和构建产物。
- 复制源码后生成 `docs/harness-adoption/source-import.md`，并把 `project.yaml` 的 `source_layout` / `source_import` 字段更新为输出工程内路径。
- 创建缺失的治理目录：`rules/`、`docs/`、`issues/`、`iterations/`、`openspec/`、`scripts/`、`compatibility/`、`tests/` 中必要部分。
- 合并或生成 `AGENTS.md`，让它成为 AI 执行入口，指向现有项目事实源和新增 Harness 规则。
- 生成或更新 `project.yaml`，用结构化字段记录实际项目事实；布尔值必须为 true/false。
- 生成或补齐 `docs/README.md`、产品概览、架构、部署、API、数据库、测试、兼容性等文档，内容必须来自现有项目。
- 接入 `rules/`，并删除不适用技术栈的规则或章节。
- 接入 `issues/requirements`、`issues/bugs`、`iterations`、`openspec` 目录和模板，保留 `.gitkeep` 与 registry。
- 根据 `agent-entrypoint.md` 和 `default-command-catalog.md` 同步 `.agents/skills/` 中实际启用的命令技能；模板资产内的 `SKILL.template.md` 在输出工程中必须渲染为 `SKILL.md`。
- 添加 `docs/harness-adoption/`，记录接入摘要、冲突、裁剪项、后续任务和未决策项。

### 5. 清理模板痕迹

交付前检查并修复：

- 删除模板标记：`[通用]`、`[个性化]`、`[条件启用]`、`【通用】`、`【个性化】`、`【条件启用】`。
- 删除模板元信息：生成参数、初始化参数、初始化说明、模板模块构成、抽象模板、Token 优化模板。
- 删除来源项目痕迹，尤其是具体示例项目名、服务名、端口、账号、路径、bucket、表名和 API 示例。
- 删除不适用能力的整节、整表行、测试矩阵、命令和规则。
- 把真实阻塞项集中到 pending decisions 文档，不让 `待确认` 散落在 README、AGENTS、YAML、规则或命令中。

### 6. 验证

至少执行：

```bash
python scripts/validate-directory-structure.py
python scripts/validate-generated-docs.py --strict
```

如果项目没有这些脚本，优先从 Harness 资产接入脚本；如果接入模式过轻而没有脚本，要用 `rg` 手动检查模板痕迹和散落待确认。

独立输出目录场景还必须验证源码已整合：

```bash
test -d src/backend || test -d src/web || test -d src/wechat-miniapp
rg --files src
test -f docs/harness-adoption/source-import.md
```

验证 `src/` 不应只包含 `.gitkeep`；至少应包含旧项目入口文件，例如 Django `manage.py`、`settings.py`、小程序 `app.json`、`project.config.json`、`pages/**` 等实际源码文件。

还要运行现有项目最可信的验证命令，例如：

- Node 项目：`npm test`、`pnpm test`、`npm run lint`、`pnpm run build`
- Python 项目：`pytest`、`ruff check`、`mypy`
- Docker 项目：`docker compose config`

无法运行时说明原因，不把未验证说成已通过。

## 交付格式

完成后用简短中文说明：

- 接入模式。
- 新增/更新的关键文件。
- 旧业务源码复制到了哪些输出目录。
- 排除了哪些运行时/敏感/大文件内容。
- 已保留的存量项目事实。
- 验证结果。
- 仍需用户决策的事项。

如果只生成方案，不改文件，则输出“接入计划 + 风险清单 + 推荐执行顺序”，不要假装已经完成迁移。
