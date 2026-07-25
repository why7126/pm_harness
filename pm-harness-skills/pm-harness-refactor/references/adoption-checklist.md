# Harness 存量项目接入清单

这份清单用于把 PM Harness 工程非破坏式接入已有代码仓库。执行时按顺序推进；用户明确要求只输出方案时，把清单转成项目化计划即可。

## 1. 初始盘点

先确认工作区状态：

```bash
git status --short
rg --files
```

重点识别：

- 入口文档：`README*`、`AGENTS.md`、`CONTRIBUTING*`、`docs/`
- 项目事实源：`package.json`、`pnpm-workspace.yaml`、`pyproject.toml`、`requirements*.txt`、`poetry.lock`、`uv.lock`、`go.mod`、`Cargo.toml`、`pom.xml`、`build.gradle`
- 运行与部署：`Dockerfile*`、`docker-compose*.yml`、`Makefile`、`.env.example`、`deploy/`、`helm/`、`k8s/`
- 测试与质量：`tests/`、`pytest.ini`、`vitest.config.*`、`jest.config.*`、`playwright.config.*`、`ruff.toml`、`eslint.config.*`
- AI 工具资产：`.codex/`、`.claude/`、`.cursor/`、`.kiro/`、`.opencode/`、`.agents/`
- 治理资产：`issues/`、`iterations/`、`openspec/`、`rules/`、`compatibility/`

记录现有未提交改动。涉及已有改动的文件要读完再编辑，避免覆盖用户工作。

## 2. 项目事实提取

从现有文件提取这些字段，用于渲染 `project.yaml`、`AGENTS.md` 和文档：

| 字段 | 来源优先级 |
|---|---|
| 项目名与代码 | README、包管理器文件、仓库名 |
| 产品定位 | README、docs、页面标题、API 描述 |
| 目标用户 | README、产品文档、路由/页面/接口命名 |
| 产品形态 | 目录结构、前端框架、后端服务、移动端或桌面端配置 |
| 后端技术栈 | 依赖文件、入口文件、Dockerfile |
| 前端技术栈 | package.json、src 结构、构建配置 |
| 数据库 | ORM 配置、迁移目录、env 示例、compose |
| 对象存储 | env 示例、SDK 依赖、storage 目录、compose |
| 测试命令 | package scripts、pytest.ini、Makefile、CI |
| 部署方式 | compose、Dockerfile、CI、deploy/ |
| Agent 工具 | 已存在的 AI 工具目录和用户指定 |

不确定但不阻塞接入的信息放入 pending decisions；阻塞信息可以向用户追问。

## 3. 模式判定

### minimal

使用条件：

- 项目很小，或用户只想先试运行 Harness。
- 缺少清晰测试/部署结构。
- 已有文档很多，不适合一次大改。

建议接入：

- `AGENTS.md`
- `rules/global.md`、`rules/coding.md`、`rules/testing.md`、`rules/directory-structure.md`
- `docs/harness-adoption/`
- 必要校验脚本
- 当前工具对应的 `.codex/` 或 `.claude/` 命令

### standard

使用条件：

- 有稳定源码、测试、部署或多人协作需要。
- 用户希望把需求、缺陷、迭代、OpenSpec 纳入治理。

建议接入：

- minimal 的全部内容
- `project.yaml`
- `docs/README.md`、`docs/00-product-overview.md`、`docs/01-architecture.md`、`docs/02-deployment.md`
- `issues/requirements/`、`issues/bugs/`
- `iterations/`
- `openspec/`
- Agent 命令与 Skills

### full

使用条件：

- 项目要长期作为 Harness 标准工程维护。
- 需要兼容性矩阵、标准文档、workflow sync、完整校验。

建议接入：

- standard 的全部内容
- `compatibility/`
- `docs/standards/`
- `scripts/workflow_sync/`
- `validate-template-sync.py`、`validate-generated-docs.py`、`validate-agent-context-budget.py`
- 完整命令族

## 4. 文件合并规则

### `AGENTS.md`

如果不存在，基于 Harness 模板生成。

如果已存在：

- 保留原项目的构建命令、测试命令、架构约束和安全红线。
- 添加 Harness 的读取路由、需求/Bug/迭代/OpenSpec 入口、规则索引、验证要求。
- 删除重复、过时或互相冲突的说明。
- 如果冲突无法判断，写入 `docs/harness-adoption/conflicts.md`。

### `README.md`

默认不大改根 README。只在必要时补一个短小的 Harness 入口段，链接到：

- `AGENTS.md`
- `docs/README.md`
- `rules/`
- `issues/`
- `openspec/`

不要把模板化长文档塞进根 README。

### `project.yaml`

如果不存在，创建一个真实事实源。

如果已存在：

- 保留已有字段。
- 只补充 Harness 需要的结构化字段。
- 不写 `待确认` 作为布尔值、路径或命令。
- 不能确定的字段删除或放入 pending decisions。

### `docs/`

如果项目已有 docs：

- 优先补充索引和缺口，不覆盖现有长文档。
- 新增文档要引用现有文档，不复制矛盾内容。
- Harness 接入过程记录放在 `docs/harness-adoption/`。

### `rules/`

规则必须和现有技术栈一致：

- 没有数据库就不引入数据库强制规则。
- 没有对象存储就不引入对象存储强制规则。
- 没有前端就不引入 UI 规则。
- 有多个端或服务时，规则要明确适用范围。

### Agent 目录

只接入实际启用工具：

- Codex: `.codex/prompts/`、`.codex/skills/`
- Claude: `.claude/commands/`、`.claude/skills/`
- Cursor: `.cursor/commands/`、`.cursor/skills/`
- Kiro: `.kiro/prompts/`、`.kiro/skills/`
- Opencode: `.opencode/commands/`、`.opencode/skills/`
- 通用技能事实源: `.agents/skills/`

已有同名命令时先比较内容；安全时合并，不能判断时保留原文件并新增冲突记录。

## 5. 必备接入文档

`docs/harness-adoption/summary.md` 应包含：

- 接入日期
- 接入模式
- 现有项目事实摘要
- 新增文件和目录
- 合并过的文件
- 裁剪掉的 Harness 能力
- 验证结果
- 后续建议

`docs/harness-adoption/conflicts.md` 应包含：

- 冲突文件
- 冲突类型
- 当前处理方式
- 推荐人工决策

没有冲突时可以不创建该文件，或创建并写明“暂无冲突”。

`docs/harness-adoption/pending-decisions.md` 或 `docs/pending-decisions.md` 应包含：

- 决策项
- 影响范围
- 当前默认处理
- 何时必须决策

## 6. 模板痕迹检查

交付前运行：

```bash
rg "\\[通用\\]|\\[个性化\\]|\\[条件启用\\]|【通用】|【个性化】|【条件启用】|template_scope|抽象模板|Token 优化模板|初始化参数|生成参数" .
rg "ProjectSoulKing|待确认" README.md AGENTS.md project.yaml docs rules openspec issues iterations
```

允许 `待确认` 只出现在集中 pending decisions 文档中。允许 ProjectSoulKing 只出现在接入说明中用于描述来源，不得出现在项目业务事实、命令、端口或配置中。

## 7. 验证顺序

优先顺序：

1. Harness 结构校验：`python scripts/validate-directory-structure.py`
2. Harness 文档校验：`python scripts/validate-generated-docs.py --strict`
3. YAML/JSON 可解析性检查
4. 现有项目 lint/test/build
5. Docker/Compose 配置检查
6. `git diff --stat` 和关键文件人工审阅

如果验证失败，先修复再交付。确实无法修复时，说明失败命令、失败原因、影响范围和建议下一步。
