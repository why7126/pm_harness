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
- 业务源码目录：后端服务、前端、小程序、移动端、共享代码、脚本、迁移、配置样例
- 项目事实源：`package.json`、`pnpm-workspace.yaml`、`pyproject.toml`、`requirements*.txt`、`poetry.lock`、`uv.lock`、`go.mod`、`Cargo.toml`、`pom.xml`、`build.gradle`
- 运行与部署：`Dockerfile*`、`docker-compose*.yml`、`Makefile`、`.env.example`、`deploy/`、`helm/`、`k8s/`
- 测试与质量：`tests/`、`pytest.ini`、`vitest.config.*`、`jest.config.*`、`playwright.config.*`、`ruff.toml`、`eslint.config.*`
- AI 工具资产：`.agents/skills/`
- 治理资产：`issues/`、`iterations/`、`openspec/`、`rules/`、`compatibility/`

记录现有未提交改动。涉及已有改动的文件要读完再编辑，避免覆盖用户工作。

如果用户指定独立输出目录，而不是直接在旧项目目录内接入 Harness，必须同时规划源码复制：

| 旧源码类型 | 推荐输出路径 |
|---|---|
| Django / FastAPI / Flask / 后端服务 | `src/backend/` |
| 微信小程序 | `src/wechat-miniapp/` |
| Web 前端 | `src/web/` |
| 共享类型 / SDK / 公共库 | `src/shared/` 或 `src/sdk/` |
| 部署脚本 | `deploy/` 或 `src/infrastructure/` |

不得只生成 Harness 治理目录而留下空的 `src/`。

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

源码复制排除项：

- Python 缓存：`__pycache__/`、`*.pyc`、`.pytest_cache/`
- Node / 小程序缓存和构建产物：`node_modules/`、`miniprogram_npm/`、`dist/`、`build/`
- 虚拟环境：`.venv/`、`venv/`、`env/`
- 运行时数据：`media/`、生产上传文件、`static/` 收集产物、`db.sqlite3`、`*.sqlite3`
- 日志和临时文件：`*.log`、`nohup.out`、`.DS_Store`
- 真实环境文件：`.env`、`.env.*`，除非用户明确要求复制且已确认安全处理方式

疑似含密钥的生产配置文件必须登记到 `docs/harness-adoption/source-import.md` 和 `docs/pending-decisions.md`。需要可运行交付时可复制源码文件，但不得把其中真实密钥复述到文档；需要安全优先交付时生成脱敏文件或 `.example`。

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
- 当前项目需要的 `.agents/skills/` 命令技能

### standard

使用条件：

- 有稳定源码、测试、部署或多人协作需要。
- 用户希望把需求、缺陷、迭代、OpenSpec 纳入治理。

建议接入：

- minimal 的全部内容
- 独立输出目录场景下的业务源码复制
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
- 独立输出目录场景下必须记录：
  - `source_layout.backend`、`source_layout.wechat_miniapp` 等输出工程内路径。
  - `source_import.origins` 中的旧目录路径。
  - `source_import.excluded_patterns` 中的排除规则。
  - `source_import.sensitive_files` 中的敏感配置处理策略。

### `docs/`

如果项目已有 docs：

- 优先补充索引和缺口，不覆盖现有长文档。
- 新增文档要引用现有文档，不复制矛盾内容。
- Harness 接入过程记录放在 `docs/harness-adoption/`。
- 独立输出目录场景必须新增 `docs/harness-adoption/source-import.md`，记录旧源码复制范围、目标路径、排除项、冲突、敏感配置处理和验证结果。

### `rules/`

规则必须和现有技术栈一致：

- 没有数据库就不引入数据库强制规则。
- 没有对象存储就不引入对象存储强制规则。
- 没有前端就不引入 UI 规则。
- 有多个端或服务时，规则要明确适用范围。

### Agent 目录

只接入 `.agents/skills/` 单一技能入口：

- 输出工程中的 `.agents/skills/<command-name>/SKILL.md` 是命令语义的唯一事实源。
- 模板资产内的 `.agents/skills/<command-name>/SKILL.template.md` 必须渲染为输出工程中的 `SKILL.md`。
- 不生成、同步或保留 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/`。

已有同名 `.agents/skills/<command-name>/SKILL.md` 时先比较内容；安全时合并，不能判断时保留原文件并新增冲突记录。

### 业务源码复制

独立输出目录场景必须复制旧业务源码：

1. 创建目标源码目录，如 `src/backend/`、`src/wechat-miniapp/`。
2. 使用文件级复制或同步工具复制源码，应用排除规则。
3. 保留业务入口文件、迁移、路由、模型、页面、项目配置和非敏感配置样例。
4. 不复制运行时媒体、日志、缓存、数据库、虚拟环境、构建产物。
5. 复制完成后确认目标目录不为空，并包含实际入口文件：
   - Django: `src/backend/manage.py`、`src/backend/**/settings.py`
   - 微信小程序: `src/wechat-miniapp/app.json`、`src/wechat-miniapp/project.config.json`、`src/wechat-miniapp/pages/**`
6. 更新文档和 `project.yaml`，让日常开发路径指向输出工程内源码，而不是旧只读路径。

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

`docs/harness-adoption/source-import.md` 应包含：

- 每个旧源码目录的来源路径。
- 每个目标源码目录的输出路径。
- 已复制的关键入口文件。
- 已排除的目录和文件模式。
- 疑似敏感配置文件处理策略。
- 运行时媒体、数据库、日志和缓存处理策略。
- 源码整合验证结果。

`docs/harness-adoption/pending-decisions.md` 或 `docs/pending-decisions.md` 应包含：

- 决策项
- 影响范围
- 当前默认处理
- 何时必须决策

## 6. 模板痕迹检查

交付前运行：

```bash
rg "\\[通用\\]|\\[个性化\\]|\\[条件启用\\]|【通用】|【个性化】|【条件启用】|template_scope|抽象模板|Token 优化模板|初始化参数|生成参数" .
rg "来源示例项目|待确认" README.md AGENTS.md project.yaml docs rules openspec issues iterations
```

允许 `待确认` 只出现在集中 pending decisions 文档中。允许来源示例项目名称只出现在接入说明中用于描述来源，不得出现在项目业务事实、命令、端口或配置中。

## 7. 验证顺序

优先顺序：

1. Harness 结构校验：`python scripts/validate-directory-structure.py`
2. Harness 文档校验：`python scripts/validate-generated-docs.py --strict`
3. YAML/JSON 可解析性检查
4. 现有项目 lint/test/build
5. Docker/Compose 配置检查
6. `git diff --stat` 和关键文件人工审阅

独立输出目录还必须执行：

```bash
test -d src/backend || test -d src/web || test -d src/wechat-miniapp
rg --files src
test -f docs/harness-adoption/source-import.md
```

`rg --files src` 不得只返回 `.gitkeep`；必须能看到旧项目实际源码入口。

如果验证失败，先修复再交付。确实无法修复时，说明失败命令、失败原因、影响范围和建议下一步。
