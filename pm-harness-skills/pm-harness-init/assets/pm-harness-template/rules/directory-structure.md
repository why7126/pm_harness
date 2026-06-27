---
purpose: 目录结构与文件归属规范
content: 约束 AI 与开发人员遵循项目目录边界、文件归属、生成代码边界、文档归属、新增目录流程和目录同步规则
source: Harness directory-structure.md 抽象模板，基于项目目录规范沉淀
update_method: 项目初始化时按用户输入生成；目录边界、产品形态、技术栈、文档治理、部署方式或模块职责变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
note: 适用于 {PRODUCT_NAME} 项目；AGENTS.md 必须引用本文档，AI 新增文件前必须先确认目录归属
template_scope: 可作为工程初始化的 directory-structure.md 模块
---

# 目录结构与文件归属规范

## 0. 规则定位 `[通用]`

本文件用于约束 `{PRODUCT_NAME}` 的目录边界、文件归属、新增目录流程和 AI 写入行为，避免：

- AI 随意创建新目录、临时目录或根目录业务文件。
- 后端、前端、移动端、算法、文档、测试、部署、数据文件混放。
- 需求、Bug、迭代、OpenSpec、长期文档混放。
- 绕过 Requirement/Bug/OpenSpec 流程直接新增业务模块。
- API、数据库、部署、兼容性、测试、UI 变更后未同步相关目录和文档。
- 生成代码、模型文件、真实数据、日志、缓存、大文件被错误提交。

AI 在新增、移动、删除文件或目录前必须先阅读本文档。

## 1. 文档模块分类 `[通用]`

本模板将目录规则拆分为三类，工程初始化时应根据用户输入生成最终文档：

- `[通用]`：所有项目默认保留的目录边界。
- `[个性化]`：必须根据产品形态、技术栈、工具链、部署方式和团队流程替换的内容。
- `[条件启用]`：仅在项目启用对应能力时保留，例如 Web、微信小程序、移动端、桌面端、算法、模型、对象存储、Kubernetes、私有化部署、外部 AI 工具目录等。

推荐初始化参数：

| 参数 | 用途 |
| --- | --- |
| `{PRODUCT_NAME}` | 项目或产品名称 |
| `{PRODUCT_CODE}` | 项目标识、包名前缀或服务标识 |
| `{PRODUCT_FORMS}` | 产品形态，例如 Web、微信小程序、移动端、桌面端、H5、API 服务 |
| `{BACKEND_STACK}` | 后端技术栈 |
| `{FRONTEND_STACK}` | 前端技术栈 |
| `{DATABASE_STACK}` | 数据库选型 |
| `{DEPLOYMENT_STACK}` | 部署方式 |
| `{ENABLED_AGENT_TOOLS}` | 启用的 AI 工具目录，例如 Claude、Codex、Cursor、Kiro、OpenCode |
| `{REQ_ROOT_DIR}` | 需求根目录 |
| `{BUG_ROOT_DIR}` | 缺陷根目录 |
| `{ITERATION_PATTERN}` | 迭代目录命名 |
| `{CHANGE_ID_PATTERN}` | OpenSpec Change 命名 |
| `{DOCS_STRUCTURE}` | docs 分层结构 |
| `{GENERATED_CODE_DIRS}` | 生成代码目录 |
| `{HAS_WEB}` | 是否启用 Web |
| `{HAS_WECHAT_MINIAPP}` | 是否启用微信小程序 |
| `{HAS_MOBILE}` | 是否启用移动端 |
| `{HAS_DESKTOP}` | 是否启用桌面端 |
| `{HAS_ALGORITHM}` | 是否包含算法模块 |
| `{HAS_OBJECT_STORAGE}` | 是否包含对象存储 |
| `{HAS_MEDIA}` | 是否包含媒体/文件处理 |

## 2. 顶层目录总览 `[通用 + 个性化]`

推荐顶层结构：

```text
{PRODUCT_CODE}/
├── AGENTS.md                    # AI Agent 总入口，必须引用 rules/
├── README.md                    # 面向人类的项目入口
├── project.yaml                 # 项目元信息、产品形态、技术栈事实源
├── docker-compose.yml           # 本地/开发编排，按需启用
├── .env.example                 # 环境变量样例
├── .gitignore                   # Git 忽略规则
│
├── .claude/                     # Claude 命令与技能，按需启用
├── .codex/                      # Codex 命令与配置，按需启用
├── .cursor/                     # Cursor 命令与配置，按需启用
├── .kiro/                       # Kiro 工作流配置，按需启用
├── .opencode/                   # OpenCode 配置，按需启用
│
├── rules/                       # 全局研发规范
├── docs/                        # 长期项目记忆、架构、治理、指南、知识库
├── issues/                      # 原始需求与 Bug 池
├── iterations/                  # 迭代计划、发布说明、验收报告
├── openspec/                    # 行为规格、变更和归档，按流程启用
├── compatibility/               # 兼容性矩阵与专项适配说明
├── scripts/                     # 自动化脚本、验证脚本、运维脚本
├── deploy/                      # 部署编排与环境部署材料
├── data/                        # 本地开发数据与样例数据边界
├── models/                      # 模型文件占位，不提交大文件
│
├── src/                         # 源码根目录
└── tests/                       # 测试根目录
```

顶层目录职责矩阵：

| 目录 | 职责 | 是否允许随意新增同级目录 | 生成策略 |
| --- | --- | ---: | --- |
| `rules/` | 全局研发规范 | 否 | 必须保留 |
| `docs/` | 长期项目文档、架构、治理、指南、知识库 | 否 | 必须保留 |
| `issues/` | 需求、Bug、附件、原型入口 | 否 | 必须保留 |
| `iterations/` | 迭代计划、发布说明、验收记录 | 否 | 必须保留或按流程替换 |
| `openspec/` | 行为规格、变更、归档 | 否 | 启用 OpenSpec 时保留 |
| `compatibility/` | 端、数据库、对象存储、平台兼容性 | 否 | 按能力生成子目录 |
| `scripts/` | 工程自动化脚本 | 否 | 必须保留 |
| `deploy/` | 部署编排、部署脚本、环境说明 | 否 | 按部署方式生成 |
| `data/` | 本地开发数据、脱敏样例、测试数据边界 | 否 | 仅保留可提交占位和脱敏样例 |
| `models/` | 算法/AI 模型占位 | 否 | 有算法/模型需求时启用 |
| `src/` | 全部源码 | 否 | 按产品形态生成子目录 |
| `tests/` | 单元、集成、端到端、兼容性测试 | 否 | 必须保留 |

新增顶层目录必须先创建 OpenSpec Change 或架构决策记录，并更新本文档、`AGENTS.md`、`README.md`、`project.yaml`。

## 3. Agent 与工具目录 `[条件启用]`

AI 工具目录按 `{ENABLED_AGENT_TOOLS}` 生成；未启用工具不得保留强制规则。

| 目录 | 职责 | 更新规则 |
| --- | --- | --- |
| `.claude/` | Claude Code 命令、技能、项目规则 | 命令中的产品名和路径必须参数化 |
| `.codex/` | Codex 命令、配置、任务约束 | 保持与 `AGENTS.md` 和 `rules/` 一致 |
| `.cursor/` | Cursor 命令与规则 | 不得残留样例项目业务词 |
| `.kiro/` | Kiro 工作流配置 | 按启用情况保留 |
| `.opencode/` | OpenCode 配置 | 按启用情况保留 |

工具命令中引用的规则文件、路径、命令名必须与实际工程一致。

## 4. rules/ 目录 `[通用]`

`rules/` 存放全局研发规范，不存放业务代码、运行时数据、临时记录或任务材料。

```text
rules/
├── global.md
├── language.md
├── coding.md
├── api.md
├── bug-management.md
├── compatibility.md
├── data-management.md
├── database.md
├── directory-structure.md
├── document-governance.md
├── environment.md
├── media.md
├── object-storage.md
├── port-management.md
├── release.md
├── requirement-management.md
├── security.md
├── testing.md
└── ui-design.md
```

规则：

- 规则文件之间必须保持一致。
- 目录变更时至少检查 `AGENTS.md`、`README.md`、`project.yaml`、`rules/global.md`、`rules/document-governance.md`、`rules/requirement-management.md`、`rules/bug-management.md`。
- 新增规则文件必须说明适用范围、更新方式、通用/个性化/条件启用模块。

## 5. docs/ 目录 `[通用 + 个性化]`

docs 分层为：`{DOCS_STRUCTURE}`。

推荐结构：

```text
docs/
├── 00-product-overview.md
├── 01-architecture.md
├── 02-deployment.md
├── 03-api-index.md
├── 04-database-design.md
├── 05-compatibility-matrix.md
├── 06-asset-management.md        # 按媒体/文件/算法能力改名或删除
├── 07-object-storage-strategy.md # 有对象存储时启用
├── standards/                    # API、错误码、测试、治理细则
├── guides/                       # 操作手册、部署手册、用户指南
├── knowledge-base/               # 故障、事故、排查经验沉淀
└── README.md                     # 文档总导航
```

归属规则：

- 主文档使用 `docs/NN-topic.md`，按阅读顺序编号。
- API、错误码、测试治理、工程治理等专项标准优先放入 `docs/standards/`。
- 需求不得放入 `docs/product/`、`docs/prd/`，必须放入 `{REQ_ROOT_DIR}`。
- Bug 分析不得放入 `docs/bugs/`，必须放入 `{BUG_ROOT_DIR}`。
- 迭代文档不得放入 `docs/iterations/`，必须放入 `iterations/`。
- 故障知识沉淀可放入 `docs/knowledge-base/`，但不得替代 Bug 目录。
- 不得在 `docs/` 中保存真实密钥、生产数据、未脱敏日志、运行时缓存或代码实现。

## 6. issues/ 目录 `[通用 + 个性化]`

`issues/` 是原始需求与 Bug 池，不等同于开发任务，也不替代 OpenSpec。REQ/BUG 共享的 `plan/`、`review/`、`archive/` 生命周期阶段目录细则以 `rules/issues-lifecycle.md` 为准。

```text
issues/
├── requirements/
│   ├── _registry.yaml
│   ├── plan/                    # 规划中、评审未完成
│   │   └── REQ-NNNN-slug/
│   ├── review/                  # 已完成评审，尚未归档
│   │   └── REQ-NNNN-slug/
│   └── archive/                 # 已验收关闭并归档
│       └── REQ-NNNN-slug/
└── bugs/
    ├── _registry.yaml
    ├── plan/                    # 规划中、评审未完成
    │   └── BUG-NNNN-slug/
    ├── review/                  # 已完成评审，尚未归档
    │   └── BUG-NNNN-slug/
    └── archive/                 # 已验收关闭并归档
        └── BUG-NNNN-slug/
```

Issue 目录内每个 `REQ-NNNN-slug/` 或 `BUG-NNNN-slug/` 仍保持独立材料包结构，包含 `capture.md`、结构化说明、验收、`trace.md`、`review.md`、附件和必要证据。

状态与目录映射：

| 分区 | 需求状态 | BUG 状态 | 说明 |
| --- | --- | --- | --- |
| `plan/` | `captured`、`exploring`、`draft`、`enriching`、`pending_review` | `captured`、`exploring`、`draft`、`enriching`、`pending_review` | 规划中，评审未完成或未形成可执行结论 |
| `review/` | `approved`、`in_sprint`、`implementing`、`delivered`、`changed` | `approved`、`in_sprint`、`fixing`、`fixed`、`reopened` | 已完成评审，未完成最终归档 |
| `archive/` | `done`、`rejected`、`deferred` | `done`、`rejected`、`wont_fix`、`deferred` | 已关闭或已归档，保留追溯 |

状态变更跨越分区时，必须移动整个 Issue 目录并同步 `_registry.yaml` 与 `trace.md`。

规则：

- 需求目录细节以 `rules/requirement-management.md` 为准。
- Bug 目录细节以 `rules/bug-management.md` 为准。
- 需求与 Bug 的阶段迁移、`lifecycle_stage`、registry 同步和遗留路径兼容以 `rules/issues-lifecycle.md` 为准。
- 需求和 Bug 附件必须脱敏。
- 已进入开发流程的能力必须能追溯到 OpenSpec Change 或任务记录。

## 7. iterations/ 目录 `[通用 + 个性化]`

迭代目录命名为：`{ITERATION_PATTERN}`。Sprint 共享的 `change/`、`archive/` 生命周期阶段目录细则以 `rules/iterations-lifecycle.md` 为准。

推荐结构：

```text
iterations/
├── change/                     # 未归档迭代
│   └── sprint-xxx/
│       ├── sprint.yaml
│       ├── sprint.md
│       ├── release-note.md
│       └── acceptance-report.md
└── archive/                    # 已完成归档迭代
    └── sprint-xxx/
        ├── sprint.yaml
        ├── sprint.md
        ├── release-note.md
        └── acceptance-report.md
```

规则：

- 新建、规划中、执行中或验收未闭环的迭代必须放入 `iterations/change/`。
- 已完成归档的迭代必须整体移动到 `iterations/archive/`，不得继续在 `change/` 中修改。
- Sprint 阶段迁移、`lifecycle_stage`、遗留路径兼容和自动化解析以 `rules/iterations-lifecycle.md` 为准。
- `sprint.yaml` 是推荐机器可读事实源。
- `sprint.md` 是人类可读迭代说明。
- `release-note.md` 是发布说明初稿。
- `acceptance-report.md` 是验收报告。
- 迭代目录不存放源码、构建产物、测试日志或临时文件。
- 需求、Bug、Change 进出迭代时必须同步对应 trace。
- 自动化脚本查找迭代时必须递归扫描 `iterations/**/sprint.yaml`，不得只查找 `iterations/*/sprint.yaml`。

如项目采用 Kanban、季度计划或外部任务系统，应在初始化时替换本目录结构并保留本地追踪索引。

## 8. openspec/ 目录 `[条件启用]`

当项目启用 OpenSpec 或等价行为规格系统时启用本节。

```text
openspec/
├── project.md
├── config.yaml
├── specs/                      # 已生效规格
├── changes/                    # 进行中的变更
│   └── <change-id>/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       ├── trace.md
│       ├── acceptance.md
│       ├── test-plan.md
│       ├── specs/
│       └── implementation/
└── archive/                    # 已完成变更归档
    └── YYYY-MM/
```

规则：

- 新增业务能力、模块边界调整、接口契约变化，应先进入 `openspec/changes/`。
- 已确认并生效的能力归入 `openspec/specs/`。
- 完成后的变更归档到 `openspec/archive/YYYY-MM/<change-id>/`。
- AI 不得绕过 OpenSpec 直接新增业务能力目录。
- AI 不得直接修改 `openspec/specs/` 作为开发中草稿。

## 9. compatibility/ 目录 `[通用 + 条件启用]`

```text
compatibility/
├── database/
├── devices/
├── object-storage/
├── os/
└── runtime/
```

生成规则：

- 启用 Web 时生成 `compatibility/devices/web.md`。
- 启用微信小程序时生成 `compatibility/devices/wechat-miniapp.md`。
- 启用 Android、iOS、桌面端、H5 时生成对应设备文档。
- 使用数据库时生成 `compatibility/database/{database}.md`、`migration-rules.md`、`test-matrix.md`。
- 使用对象存储时生成 `compatibility/object-storage/{provider}.md`。
- 有信创 OS、CPU 架构、浏览器、运行时要求时生成对应专项文档。

## 10. scripts/ 与 deploy/ 目录 `[通用 + 条件启用]`

### 10.1 scripts/

```text
scripts/
├── validate-docs.*             # 文档结构/元数据校验
├── validate-env.*              # 环境变量校验
├── validate-ports.*            # 端口占用校验
├── docker/                     # Docker 辅助脚本
└── README.md
```

规则：

- `scripts/` 只存放可重复执行的工具脚本。
- 一次性临时脚本不得长期留在 `scripts/`；确需保留必须补 README 和用途说明。
- 业务代码不得放入 `scripts/`。
- 运行日志、输出文件、缓存不得提交到 `scripts/`。

### 10.2 deploy/

```text
deploy/
├── docker-compose/
├── k8s/
├── private/
├── helm/
└── README.md
```

部署目录按 `{DEPLOYMENT_STACK}` 生成。未启用 Kubernetes、Helm、私有化部署时，不得生成对应强制规则。

## 11. data/ 与 models/ 目录 `[通用 + 条件启用]`

### 11.1 data/

```text
data/
├── samples/
├── fixtures/
├── imports/
├── exports/
└── .gitkeep
```

规则：

- `data/` 默认只提交目录占位、README、脱敏样例和测试 fixtures。
- 真实用户数据、生产导出、日志、缓存、临时文件不得提交。
- 具体提交边界以 `rules/data-management.md` 和 `.gitignore` 为准。

### 11.2 models/

```text
models/
├── README.md
└── .gitkeep
```

规则：

- 有算法、AI、推理或模型依赖时启用。
- 大模型文件、权重、训练产物默认不提交 Git。
- 模型下载、校验、版本锁定方式必须写入 `models/README.md` 或相关文档。

## 12. src/ 源码目录 `[通用 + 个性化]`

`src/` 是唯一源码根目录。所有业务代码、应用代码、SDK、基础设施适配都必须放在 `src/` 下。

```text
src/
├── backend/
├── web/
├── wechat-miniapp/
├── android/
├── ios/
├── desktop/
├── h5/
├── algorithm/
├── shared/
├── sdk/
└── infrastructure/
```

生成规则：

- 根据 `{BACKEND_STACK}` 生成 `src/backend/` 的入口、依赖文件、分层目录。
- 根据 `{HAS_WEB}` 和 `{FRONTEND_STACK}` 生成 `src/web/`；无 Web 前端时删除 Web 强制规则。
- 根据 `{HAS_WECHAT_MINIAPP}`、`{HAS_MOBILE}`、`{HAS_DESKTOP}` 生成对应端目录。
- 根据 `{HAS_ALGORITHM}` 生成 `src/algorithm/` 和 `models/` 规则。
- 跨端共享定义放入 `src/shared/`，不得复制到多个端中。
- SDK 不得反向依赖具体应用层。
- 基础设施适配不得包含业务流程。

### 12.1 后端目录 `[个性化]`

```text
src/backend/
├── README.md
├── Dockerfile
├── .env.example
├── app/
│   ├── main.*
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   └── integrations/
└── migrations/
```

非 Python/FastAPI 项目必须按 `{BACKEND_STACK}` 替换入口、依赖和分层名称，不得保留不适用框架描述。

### 12.2 Web 前端目录 `[条件启用]`

```text
src/web/
├── README.md
├── package.json
├── Dockerfile
├── nginx.conf
├── src/
│   ├── app/
│   ├── pages/
│   ├── features/
│   ├── components/
│   ├── services/
│   ├── generated/
│   ├── stores/
│   ├── hooks/
│   ├── styles/
│   └── lib/
└── public/
```

`generated/` 目录只能由生成工具写入，AI 不得手工修改。前端 API 调用规则必须与 `rules/api.md` 一致，UI 组件归属必须与 `rules/ui-design.md` 一致。

### 12.3 微信小程序、移动端、桌面端 `[条件启用]`

```text
src/wechat-miniapp/
src/android/
src/ios/
src/desktop/
src/h5/
```

未启用对应端时，不得生成强制开发规则；如保留占位目录，必须写明 `未启用，仅占位`。

### 12.4 算法目录 `[条件启用]`

```text
src/algorithm/
├── README.md
├── inference/
├── training/
├── evaluation/
├── preprocessing/
└── configs/
```

模型权重默认放在根目录 `models/` 或对象存储，不直接放入 Git。训练数据归属以 `rules/data-management.md` 为准。

## 13. tests/ 测试目录 `[通用 + 个性化]`

```text
tests/
├── unit/
├── integration/
├── e2e/
├── compatibility/
├── fixtures/
└── README.md
```

生成规则：

- 有 Web 时可生成 `tests/e2e/web/` 或项目约定目录。
- 有微信小程序、移动端、桌面端时生成对应兼容性测试占位。
- 有数据库兼容要求时生成 `tests/compatibility/{database}/`。
- 有对象存储时生成 `tests/compatibility/object-storage/` 或 provider 子目录。
- 测试数据必须遵循 `rules/data-management.md`。

## 14. Docker 与部署文件归属 `[通用 + 条件启用]`

| 文件/目录 | 归属 | 规则 |
| --- | --- | --- |
| `docker-compose.yml` | 根目录 | 仅项目级编排 |
| `src/backend/Dockerfile` | 后端目录 | 后端镜像构建 |
| `src/web/Dockerfile` | Web 目录 | Web 镜像构建，按需启用 |
| `src/web/nginx.conf` | Web 目录 | Web 静态服务或反向代理，按需启用 |
| `deploy/` | 根目录 | 部署材料、环境差异说明 |
| `scripts/docker/` | 脚本目录 | Docker 辅助脚本 |

禁止把部署脚本散落在业务源码目录；禁止把环境变量、密钥、生产配置硬编码到 Dockerfile 或应用代码中。

## 15. 生成代码目录 `[条件启用]`

生成代码目录为：`{GENERATED_CODE_DIRS}`。

规则：

- OpenAPI、SDK、ORM、GraphQL、protobuf、CSS token 等生成产物必须放入约定目录。
- AI 不得手工修改生成代码目录中的文件。
- 生成源变化时应修改源文件和生成命令，而不是直接 patch 产物。
- 若必须修复生成产物，应先记录原因，并同步修复生成器或源定义。

## 16. 文件归属决策表 `[通用]`

| 文件类型 | 应放目录 | 禁止目录 |
| --- | --- | --- |
| 后端业务代码 | `src/backend/` | 根目录、`scripts/`、`docs/` |
| 前端页面/组件 | `src/web/` 或对应端目录 | 根目录、`docs/` |
| 微信小程序代码 | `src/wechat-miniapp/` | `src/web/`、根目录 |
| 移动端代码 | `src/android/`、`src/ios/` | 根目录 |
| 算法推理代码 | `src/algorithm/` | `models/`、`data/` |
| 共享类型/常量 | `src/shared/` | 多端重复复制 |
| API 生成代码 | `{GENERATED_CODE_DIRS}` | 手写目录 |
| 数据库迁移 | `src/backend/migrations/` 或约定目录 | `docs/`、根目录 |
| 部署编排 | `deploy/`、根 `docker-compose.yml` | 业务源码目录 |
| 自动化脚本 | `scripts/` | 根目录临时脚本 |
| 长期文档 | `docs/` | `data/`、`logs/` |
| 需求材料 | `{REQ_ROOT_DIR}` | `docs/prd/`、`docs/product/` |
| Bug 材料 | `{BUG_ROOT_DIR}` | `docs/bugs/` |
| 迭代材料 | `iterations/` | `docs/iterations/` |
| OpenSpec 变更 | `openspec/changes/` | `docs/` 临时散放 |
| 测试代码 | `tests/` 或模块内 `tests/` | 临时目录 |
| 测试 fixtures | `tests/fixtures/`、`data/fixtures/` | 生产数据目录 |
| 本地导入导出 | `data/imports/`、`data/exports/` | Git 可提交路径 |
| 模型权重 | `models/` 占位或对象存储 | Git 仓库大文件 |

## 17. 新增目录流程 `[通用]`

需要新增顶层目录或调整模块边界时，必须：

1. 创建 OpenSpec Change 或架构决策记录。
2. 说明为什么现有目录无法承载。
3. 明确新目录职责、所有者和生命周期。
4. 列出影响范围：文档、测试、脚本、部署、CI、兼容性。
5. 更新 `rules/directory-structure.md`、`AGENTS.md`、`README.md`、`project.yaml`。
6. 同步 `rules/document-governance.md`、`rules/requirement-management.md`、`rules/bug-management.md` 中相关路径。
7. 获得团队确认后再执行。

AI 只能提出目录调整建议，不得擅自放宽目录边界。

## 18. 禁止事项 `[通用]`

- 禁止在根目录新增业务代码文件。
- 禁止在 `rules/` 中存放代码实现、运行时数据或临时记录。
- 禁止在 `docs/` 中存放需求、Bug、迭代材料、运行时数据、真实生产数据或代码实现。
- 禁止把测试代码放入未经约定的临时目录。
- 禁止手工修改生成代码目录。
- 禁止在未更新 Requirement/Bug/OpenSpec 的情况下新增业务能力。
- 禁止把 Docker 环境变量、密钥、生产配置硬编码到代码中。
- 禁止用临时目录替代正式目录结构。
- 禁止提交 `logs/`、真实导入导出数据、模型大文件、缓存文件。
- 禁止保留样例项目的业务目录名、业务表名、接口资源名。

## 19. AI 新增文件前检查清单 `[通用]`

AI 在新增或移动文件前必须回答：

```text
□ 是否已有对应 Requirement、Bug、OpenSpec Change 或任务记录？
□ 新文件是否属于已有目录职责？
□ 是否需要新增目录？如需要，是否已完成新增目录流程？
□ 是否需要更新 rules/directory-structure.md？
□ 是否需要更新 AGENTS.md、README.md、project.yaml？
□ 是否需要更新 docs/、issues/、iterations/、openspec/、compatibility/？
□ 是否需要同步 requirement-management.md 或 bug-management.md？
□ 是否涉及 API 生成代码、数据库迁移、部署文件或测试 fixtures？
□ 是否需要同步 rules/api.md、rules/database.md、rules/data-management.md、rules/testing.md？
□ 是否包含真实数据、密钥、大文件、日志或缓存？
□ 是否需要补充测试或验证脚本？
```

## 20. 初始化生成建议 `[通用]`

用于工程初始化生成 `directory-structure.md` 时，建议按以下步骤处理：

1. 根据 `{PRODUCT_NAME}`、`{PRODUCT_CODE}` 替换文档元数据与顶层目录。
2. 根据 `{PRODUCT_FORMS}`、`{HAS_WEB}`、`{HAS_WECHAT_MINIAPP}`、`{HAS_MOBILE}`、`{HAS_DESKTOP}` 决定 `src/` 下端目录和 `compatibility/devices/` 文档。
3. 根据 `{BACKEND_STACK}` 生成 `src/backend/` 的入口、依赖文件和分层描述。
4. 根据 `{FRONTEND_STACK}` 生成 `src/web/` 或删除前端强制目录。
5. 根据 `{DATABASE_STACK}` 生成数据库目录、迁移目录和兼容性文档。
6. 根据 `{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{ITERATION_PATTERN}`、`{CHANGE_ID_PATTERN}` 对齐文档治理、需求治理和缺陷治理路径。
7. 根据 `{DOCS_STRUCTURE}` 生成 docs 分层；未知时使用主文档、standards、guides、knowledge-base、README 分层。
8. 根据 `{GENERATED_CODE_DIRS}` 生成生成代码目录规则；未知时标记 `待确认`。
9. 根据 `{HAS_ALGORITHM}` 决定是否生成 `src/algorithm/` 和根 `models/` 的模型规则。
10. 根据 `{HAS_OBJECT_STORAGE}`、`{HAS_MEDIA}` 决定是否生成对象存储兼容文档、文件上传文档和媒体规则。
11. 根据 `{DEPLOYMENT_STACK}` 生成 `deploy/` 子目录和 Docker/Kubernetes/私有化部署约束。
12. 删除未启用能力的强制性目录描述，避免文档要求与实际工程不一致。
13. 检查本文档与 `AGENTS.md`、`README.md`、`project.yaml`、`rules/global.md`、`rules/document-governance.md`、`rules/requirement-management.md`、`rules/bug-management.md` 一致。

## 21. 完成任务后检查清单 `[通用]`

```text
□ 顶层目录职责已覆盖且没有样例项目业务词
□ 每个目录都能说明职责、边界和是否可新增
□ [通用]、[个性化]、[条件启用] 模块标识完整
□ src/ 目录结构与产品形态、技术栈一致
□ docs/issues/iterations/openspec 的文档归属清晰
□ requirement-management.md 与 bug-management.md 中路径一致
□ scripts/deploy/data/models/generated 的边界清晰
□ 禁止事项覆盖根目录业务代码、生成代码、真实数据、大文件、临时目录
□ 新增目录流程明确要求同步 AGENTS.md、README.md、project.yaml
□ 初始化生成建议可被工程生成器直接使用
```
