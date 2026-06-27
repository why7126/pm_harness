---
purpose: 文档治理与研发追溯规范
content: 规范 docs、issues、requirements、bugs、iterations、openspec、compatibility、rules 的生成、更新、同步、评审与归档规则
source: Harness document-governance.md 抽象模板，基于项目文档治理规则沉淀
update_method: 项目初始化时按用户输入生成；研发流程、目录结构、需求/Bug 生命周期、OpenSpec 流程、迭代流程或文档分层变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 09:56:14
note: 适用于 {PRODUCT_NAME} 项目；AI 执行需求、Bug、技术改造、架构调整前必须读取本文档
template_scope: 可作为工程初始化的 document-governance.md 模块
---
# 文档治理与研发追溯规范

## 0. 规则定位 `[通用]`

本文件定义 `{PRODUCT_NAME}` 的文档生命周期、研发链路、目录职责、同步矩阵、归档规则和 AI 执行边界，确保需求、Bug、迭代、OpenSpec、代码、测试、长期文档之间可追踪、可审计、可验收。

AI 在执行以下任务前必须先阅读本文件：

- 新增、修改或关闭需求、Bug、OpenSpec Change、迭代、发布、架构设计。
- 修改 `docs/`、`issues/`、`iterations/`、`openspec/`、`rules/`、`compatibility/`。
- 变更 API、数据库、权限、安全、部署、环境变量、端口、兼容性、测试、UI、媒体或对象存储。
- 判断是否可以走轻量修订、是否必须创建 OpenSpec Change、是否可以归档。

除拼写、格式、链接、注释等无行为变化的小修外，AI 不得从用户一句话直接跳到代码实现，必须先判断是否需要创建或更新 Requirement、Bug、Iteration、OpenSpec Change 和相关长期文档。

## 1. 文档模块分类 `[通用]`

本模板将文档治理规则拆分为三类，工程初始化时应根据用户输入生成最终文档：

- `[通用]`：所有项目默认保留的文档治理基线。
- `[个性化]`：必须根据项目形态、研发流程、目录结构、技术栈、外部工具和团队约定替换的内容。
- `[条件启用]`：仅在项目启用对应能力时保留，例如 OpenSpec、Sprint、外部看板、知识库、合规审计、客户交付、移动端、算法、对象存储等。

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
| `{PROJECT_GOVERNANCE_LEVEL}` | 治理强度，例如 prototype、solo、team、enterprise、regulated |
| `{DOCS_STRUCTURE}` | docs 分层结构 |
| `{ISSUE_WORKFLOW}` | Issue 状态流 |
| `{REQ_ROOT_DIR}` | 需求目录 |
| `{BUG_ROOT_DIR}` | 缺陷目录 |
| `{ITERATION_PATTERN}` | 迭代目录命名 |
| `{SPRINT_FACT_SOURCE}` | 迭代事实源文件，例如 `sprint.yaml` |
| `{CHANGE_ID_PATTERN}` | OpenSpec Change 命名 |
| `{TASK_TRACKING_SYSTEM}` | 外部任务系统，例如 Jira、Linear、GitHub Issues、飞书 |
| `{DOC_REVIEW_POLICY}` | 文档评审策略 |
| `{ARCHIVE_POLICY}` | 归档策略 |

## 2. 研发文档链路 `[通用 + 个性化]`

`{PRODUCT_NAME}` 默认采用以下研发文档链路：

```text
需求 / Bug / 技术改造 / 架构调整
↓
issues/                         # 原始业务输入、缺陷输入和追踪壳
↓
iterations/                     # 迭代范围、排期、发布与验收
↓
openspec/changes/               # 行为变更提案、设计、任务、规格增量
↓
src/ + tests/                   # 实现与验证
↓
docs/ + compatibility/ + rules/ # 长期文档、兼容性和规则同步
↓
openspec/specs/                 # 已生效系统行为
↓
openspec/archive/               # 已完成变更归档
```

可裁剪策略：

| 项目阶段/规模 | 可简化内容 | 不可省略内容 |
| --- | --- | --- |
| 原型探索 | 可暂缓迭代四件套和完整归档 | 来源、范围、验收口径、变更说明 |
| 小型单人项目 | 可简化状态流和评审角色 | 行为变更判断、测试与 docs 同步 |
| 团队协作项目 | 不建议简化主链路 | Issue、Iteration、OpenSpec、Review、归档 |
| 企业/合规项目 | 必须强化审批与归档 | 来源、状态、验收、审计、变更历史 |

项目初始化时应根据 `{PROJECT_GOVERNANCE_LEVEL}` 生成具体链路；未知时默认使用标准链路。

## 3. docs/ 分层与职责 `[通用 + 个性化]`

docs 分层为：`{DOCS_STRUCTURE}`。

推荐结构：

```text
docs/
├── 00-*.md                     # 层 1：主索引文档，按阅读顺序编号
├── 01-*.md
├── standards/                  # 层 2：治理细则和专项标准
├── guides/                     # 层 3：操作指南，按需
├── knowledge-base/             # 层 4：故障、事故、排查经验沉淀
└── README.md                   # 文档总导航
```

规则：

- `docs/` 根目录优先放长期主文档，推荐使用 `NN-topic.md` 编号。
- 治理细则、错误码、测试标准、API 规则等专项标准统一放入 `docs/standards/`。
- 需求、Bug、迭代不得放入 `docs/`，应分别放入 `{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`iterations/`。
- 故障复盘、事故沉淀、排查经验放入 `docs/knowledge-base/`，不得替代 Bug 目录。
- 初始化生成时必须删除不适用的示例文档，不得保留其他项目的模块名、客户名、业务资源名。

## 4. 文档分类与目录职责 `[通用 + 个性化]`

| 类型 | 推荐目录 | 生命周期 | 生成策略 |
| --- | --- | --- | --- |
| 产品概览 | `docs/00-product-overview.md` | 长期有效，按版本更新 | 必须保留 |
| 架构设计 | `docs/01-architecture.md` | 长期有效，重大变更需 ADR/OpenSpec | 必须保留 |
| 部署说明 | `docs/02-deployment.md` | 随部署方式更新 | 按 `{DEPLOYMENT_STACK}` 生成 |
| API 索引 | `docs/03-api-index.md` | 随 API 变更更新 | 有 API 时保留 |
| 数据库设计 | `docs/04-database-design.md` | 随 Schema/迁移更新 | 有数据库时保留 |
| 兼容性矩阵 | `docs/05-compatibility-matrix.md` | 随端、平台、数据库更新 | 必须保留或简化 |
| 媒体/文件资产 | `docs/06-*-asset-management.md` | 按能力更新 | 有媒体/上传/算法时启用 |
| 对象存储策略 | `docs/07-object-storage-strategy.md` | 按存储策略更新 | 有对象存储时启用 |
| API 治理 | `docs/standards/api-governance.md` | 长期有效 | 有 API 时保留 |
| 错误码 | `docs/standards/error-codes.md` | 随 API/业务错误更新 | 有 API 时保留 |
| 测试治理 | `docs/standards/testing-governance.md` | 随测试策略更新 | 必须保留 |
| 原始需求 | `{REQ_ROOT_DIR}` | 从提出到关闭 | 必须保留 |
| Bug 池 | `{BUG_ROOT_DIR}` | 从发现到关闭 | 必须保留 |
| 迭代记录 | `iterations/` | 阶段性有效，完成后只读 | 必须保留或按流程替换 |
| OpenSpec 变更 | `openspec/changes/` | 开发中 | 启用 OpenSpec 时必须保留 |
| OpenSpec 规格 | `openspec/specs/` | 当前有效行为 | 启用 OpenSpec 时必须保留 |
| OpenSpec 归档 | `openspec/archive/` | 只读追溯 | 启用 OpenSpec 时必须保留 |
| 兼容性专项 | `compatibility/` | 随平台/端/数据库变化更新 | 按能力生成 |
| 规则模板 | `rules/` | 工程约束源 | 必须保留 |

## 5. Markdown 元数据规范 `[通用]`

所有长期 Markdown 文档应包含 YAML Frontmatter：

```yaml
---
purpose: 文档用途
content: 文档内容简述
source: 信息来源
update_method: 更新方式与责任
created_at: YYYY-MM-DD hh:mm:ss
updated_at: YYYY-MM-DD hh:mm:ss
note: 使用说明或风险提示
---
```

规则：

- AI 更新文档时必须保留既有 Frontmatter。
- 新建长期文档时必须补齐 Frontmatter。
- 所有自动生成的 Markdown 文档 MUST 包含 `created_at` 和 `updated_at` 两个 Frontmatter 属性字段，字段值必须使用 `YYYY-MM-DD hh:mm:ss`。
- 创建文档时 `created_at` 与 `updated_at` 均写创建时间；后续修改文档时只更新 `updated_at`，不得覆盖原始 `created_at`。
- 临时草稿进入 `docs/`、`rules/`、`openspec/`、`iterations/`、`issues/` 后必须补齐元数据或项目约定字段。
- 不确定内容必须标记 `待确认`，不得编造事实。
- 涉及外部来源、用户访谈、截图、日志、生产问题时，必须说明来源和脱敏状态。

### 5.1 时间记录格式 `[通用]`

所有文档中的时间记录必须精确到秒，统一格式为 `YYYY-MM-DD hh:mm:ss`（24 小时制）。

适用范围：

- YAML Frontmatter、自定义元数据、表格字段和正文中的发生时间、创建时间、更新时间、评审时间、验证时间、发布时间、归档时间。
- `issues/`、`iterations/`、`openspec/`、`docs/`、`rules/`、`compatibility/` 中的 trace、review、验收记录、发布记录、审计记录。
- 无法确认完整时间时，应写 `待确认`，不得只写到日期或编造秒级时间。

例外：

- 仅用于文件名、目录名、归档分组、版本分组的日期可以继续使用 `YYYY-MM-DD` 或 `YYYY-MM`。
- 明确需要按 locale 展示给最终用户的产品文案，可按产品国际化规则展示，但治理文档中的原始记录仍需保留 `YYYY-MM-DD hh:mm:ss`。

## 6. docs/ 更新触发矩阵 `[通用 + 个性化]`

| 场景 | 必须更新的文档 |
| --- | --- |
| 新产品/新模块 | `docs/00-product-overview.md`、`docs/01-architecture.md` |
| 架构边界变化 | `docs/01-architecture.md`、必要时新增 ADR |
| 部署方式、Docker Compose、环境变量、服务端口变化 | `docs/02-deployment.md`、`.env.example`、`README.md`、`rules/environment.md` |
| API 新增、删除、参数变化 | `docs/03-api-index.md`、API 治理文档、OpenAPI |
| API 错误码变化 | 错误码文档、`rules/api.md`、测试 |
| 数据库表、字段、索引、迁移变化 | `docs/04-database-design.md`、`rules/database.md` |
| 鉴权、权限、角色变化 | 鉴权文档、`rules/security.md` |
| Web/微信小程序/移动端交互变化 | 对应 OpenSpec spec、原型、`rules/ui-design.md`、兼容性文档 |
| 对象存储、文件上传、媒体处理变化 | 文件上传文档、对象存储策略、`rules/media.md`、`rules/object-storage.md` |
| 兼容性结论变化 | `docs/05-compatibility-matrix.md`、`compatibility/*` |
| 测试策略、覆盖率、质量门禁变化 | 测试治理文档、`rules/testing.md` |
| 需求治理流程变化 | `rules/requirement-management.md`、`rules/document-governance.md` |
| 缺陷治理流程变化 | `rules/bug-management.md`、知识库规则 |
| 线上问题复盘 | `docs/knowledge-base/incidents/` |
| Sprint 经验复盘 | `docs/knowledge-base/sprints/` |

更新方式：

- AI 可以生成初稿、同步变更、补充索引。
- 涉及产品范围、验收标准、架构边界、上线策略、合规审计的内容必须人工确认。
- 文档改动应与代码改动同一任务提交，避免“只改代码不改文档”。
- 若本次任务不需要更新 docs，最终说明必须写明理由。

## 7. issues/ 治理 `[通用 + 个性化]`

`issues/` 是原始需求与 Bug 池，不等同于开发任务，也不替代 OpenSpec。

需求治理的详细规则由 `rules/requirement-management.md` 定义；Bug 治理的详细规则由 `rules/bug-management.md` 定义；REQ/BUG 共享的阶段目录、迁移时机、`lifecycle_stage` 和 registry 同步规则由 `rules/issues-lifecycle.md` 定义。本文只规定目录归属与同步边界。

推荐结构：

```text
issues/
├── requirements/
│   ├── _registry.yaml
│   ├── plan/
│   │   └── REQ-NNNN-slug/
│   ├── review/
│   │   └── REQ-NNNN-slug/
│   └── archive/
│       └── REQ-NNNN-slug/
└── bugs/
    ├── _registry.yaml
    ├── plan/
    │   └── BUG-NNNN-slug/
    ├── review/
    │   └── BUG-NNNN-slug/
    └── archive/
        └── BUG-NNNN-slug/
```

规则：

- 新需求必须进入 `{REQ_ROOT_DIR}/plan/`，不得放入 `docs/product/`、`docs/prd/`。
- 新 Bug 必须进入 `{BUG_ROOT_DIR}/plan/`，不得放入 `docs/bugs/`。
- 需求或 Bug 完成评审后，必须移动到对应 `review/`；完成验收关闭或决策关闭后，必须移动到对应 `archive/`。
- Issue 状态流为 `{ISSUE_WORKFLOW}`，具体状态机可由需求/缺陷专项规则细化。
- AI 在 Change 创建、开发开始、测试通过、验收完成、归档完成时必须同步 Issue trace。

## 8. iterations/ 治理 `[通用 + 个性化]`

迭代目录命名为：`{ITERATION_PATTERN}`。Sprint 物理阶段目录、迁移时机、`lifecycle_stage` 和路径兼容规则由 `rules/iterations-lifecycle.md` 定义。

迭代事实源为：`{SPRINT_FACT_SOURCE}`。

默认迭代目录：

```text
iterations/
├── change/
│   └── sprint-xxx/
│       ├── sprint.yaml         # 机器可读事实源
│       ├── sprint.md           # 人类可读说明
│       ├── release-note.md     # 发布说明初稿
│       └── acceptance-report.md # 验收报告
└── archive/
    └── sprint-xxx/
        ├── sprint.yaml
        ├── sprint.md
        ├── release-note.md
        └── acceptance-report.md
```

`iterations/change/` 保存未归档迭代；`iterations/archive/` 保存已完成归档迭代。Sprint 归档完成后必须移动整个 `sprint-xxx/` 目录。

`sprint.yaml` 推荐字段：

```yaml
sprint_id: sprint-xxx
status: planning | in_progress | completed
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD

capacity:
  developers: 0
  testers: 0

requirements: []
bugs: []
changes: []

estimated_story_points: 0
estimated_person_days: 0
```

`sprint.md` 时间字段规则：

- `sprint.md` 中所有表格或正文记录型时间 MUST 使用 `YYYY-MM-DD hh:mm:ss`。
- Scope / 包含需求表的「说明」列如包含纳入时间、目标时间、确认时间，MUST 使用 `YYYY-MM-DD hh:mm:ss`。
- Scope / 包含 BUG 表的「说明」列如包含发现时间、纳入时间、目标时间，MUST 使用 `YYYY-MM-DD hh:mm:ss`。
- Scope / 包含 Change 表的「Sprint 目标」列如包含目标日期、目标时间、完成窗口，MUST 使用 `YYYY-MM-DD hh:mm:ss`。
- 里程碑表的「目标日期」列 MUST 使用 `YYYY-MM-DD hh:mm:ss`，不得只写 `YYYY-MM-DD`。
- `sprint.yaml` 的 `start_date` / `end_date` 是迭代日期范围，可继续使用 `YYYY-MM-DD`。

更新时机：

| 场景 | 必须更新 |
| --- | --- |
| 新迭代创建 | `sprint.yaml`、`sprint.md`、`release-note.md`、`acceptance-report.md` |
| 需求进入或移出迭代 | `sprint.yaml`、`sprint.md`、需求 `trace.md` |
| Bug 进入或移出迭代 | `sprint.yaml`、`sprint.md`、Bug `trace.md` |
| Change 创建或纳入 | `sprint.yaml`、`sprint.md`、Change `trace.md` |
| Change 完成或归档 | `sprint.yaml`、`release-note.md`、`acceptance-report.md` |
| 发现范围、排期、质量风险 | `sprint.md` 风险章节 |
| Sprint 结束 | `sprint.yaml`、`acceptance-report.md`，完成归档后移动到 `iterations/archive/` |

### 8.1 Workflow 状态同步（MUST）

执行 `req-*`、`bug-*`、`opsx-*`、`sprint-*` 命令后，MUST 运行统一同步脚本：

```bash
python scripts/sync-workflow-status.py --event <event> [--req REQ-xxxx] [--bug BUG-xxxx] [--change change-id] [--sprint sprint-xxx|auto]
```

命令不得仅依赖 Agent 记忆手工刷新 `sprint.md`、`acceptance-report.md`、`release-note.md` 或 issue `trace.md`。如脚本以 `--check` 报告 drift，当前命令视为未完成，必须修复漂移后重新执行同步。

同步脚本必须递归扫描 `iterations/**/sprint.yaml`，以同时支持 `change/` 和 `archive/` 分区。

以下 marker 区块归 `sync-workflow-status.py` 维护，禁止手工改表格内容；如旧文档缺 marker，可先补 marker 后运行同步：

- `<!-- workflow-sync:sprint-goals:start -->` / `end`
- `<!-- workflow-sync:scope-requirements:start -->` / `end`
- `<!-- workflow-sync:scope-bugs:start -->` / `end`
- `<!-- workflow-sync:scope-changes:start -->` / `end`
- `<!-- workflow-sync:openspec-tasks:start -->` / `end`
- `<!-- workflow-sync:release-changes:start -->` / `end`

如项目采用季度迭代、Kanban 或外部项目管理工具，应在初始化时替换 `{ITERATION_PATTERN}` 并保留本地追溯索引。

## 9. OpenSpec 治理 `[条件启用]`

当项目启用 OpenSpec 或等价行为规格系统时启用本节。

### 9.1 specs、changes、archive 边界

| 目录 | 含义 | 修改规则 |
| --- | --- | --- |
| `openspec/specs/` | 当前已生效能力 | 不允许作为开发中草稿直接修改 |
| `openspec/changes/` | 开发中的需求、Bug 修复、技术改造 | 每个变更独立目录 |
| `openspec/archive/` | 已完成并验收的历史变更 | 只读，不得删除 |

### 9.2 必须创建 Change 的场景

满足任一条件必须创建或更新 `openspec/changes/<change-id>/`：

- 新功能。
- Bug 修复导致系统行为变化。
- API 变更。
- 数据库结构、迁移、索引变化。
- 权限、角色、鉴权策略变化。
- Docker Compose、部署方式、环境变量变化。
- Web、微信小程序、移动端、桌面端交互变化。
- 文件上传、对象存储、媒体处理策略变化。
- 算法、模型、推理接口变化。
- 测试、验收、发布、兼容性策略变化。
- 任何影响用户可见行为或系统契约的技术改造。

### 9.3 Change 必备结构

```text
openspec/changes/<change-id>/
├── proposal.md
├── design.md
├── tasks.md
├── trace.md
├── acceptance.md
├── test-plan.md
├── specs/
└── implementation/
```

OpenSpec Requirement 必须包含 MUST/SHALL 和至少一个 Scenario；不得只写口号或模糊目标。

### 9.4 归档规则

验收通过后：

1. 将 `changes/<change-id>/specs/*` 合并到 `openspec/specs/*`。
2. 更新相关需求、Bug 的状态和 trace。
3. 更新相关 `iterations/**/sprint.yaml`、`sprint.md`、`release-note.md`、`acceptance-report.md`。
4. 同步 `docs/`、`compatibility/`、`README.md`、`project.yaml`。
5. 将 Change 移动到 `openspec/archive/YYYY-MM/<change-id>/`。

AI 不得删除归档内容；需要修正归档内容时必须新增修订记录。

## 10. Backlog / 外部项目管理工具 `[条件启用]`

任务系统为：`{TASK_TRACKING_SYSTEM}`。

如项目启用本地 `backlog/` 或外部工具，必须建立本地追溯关系。

| 工具类型 | 本地要求 |
| --- | --- |
| 本地 `backlog/` | 任务 ID 必须写入 Issue、Iteration、Change |
| Jira/Linear | 外部链接必须写入 `trace.md` |
| 飞书/语雀/Confluence | 文档链接必须写入对应 docs 或 trace |
| GitHub Issues | PR/Commit 必须引用 Issue ID |

未启用外部工具时，删除本章节或标记为 `未启用`。

## 11. 文档自动同步矩阵 `[通用 + 个性化]`

| 变更类型 | 必须同步 |
| --- | --- |
| 需求新增/变更 | `rules/requirement-management.md`、`issues/requirements/*`、OpenSpec、Iteration |
| Bug 新增/修复 | `rules/bug-management.md`、`issues/bugs/*`、回归测试、必要时知识库 |
| API | `docs/03-api-index.md`、API 治理文档、OpenAPI、前端/SDK 客户端 |
| 错误码 | 错误码文档、`rules/api.md`、测试 |
| 数据库 | `docs/04-database-design.md`、迁移目录、`rules/database.md`、测试 |
| Docker / 部署 | `docker-compose.yml`、`docs/02-deployment.md`、`.env.example`、`README.md` |
| 环境变量 | `.env.example`、`rules/environment.md`、部署文档 |
| 对象存储 | `docs/07-object-storage-strategy.md`、`compatibility/object-storage/*`、后端配置 |
| 文件上传 / 媒体 | 文件上传文档、`rules/media.md`、测试 fixtures |
| Web 页面 | OpenSpec Web spec、原型、`rules/ui-design.md` |
| 微信小程序/移动端/桌面端 | 对应端 spec、兼容性文档、测试计划 |
| 算法 / 模型 | 架构文档、模型说明、数据管理规则、测试计划 |
| 兼容性结论 | `docs/05-compatibility-matrix.md`、`compatibility/*` |
| Change 归档 | OpenSpec specs、archive、Issue、Iteration、Release Note |

初始化时应根据 `{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{DEPLOYMENT_STACK}` 删除不适用行或标记为未启用。

## 12. 文档命名规范 `[通用 + 个性化]`

| 文档类型 | 命名规则 |
| --- | --- |
| 需求目录 | `REQ-NNNN-slug` 或需求专项规则约定 |
| Bug 目录 | `BUG-NNNN-slug` 或缺陷专项规则约定 |
| 迭代目录 | `sprint-xxx` 或 `{ITERATION_PATTERN}` |
| OpenSpec Change | `{CHANGE_ID_PATTERN}`，如 `add-user-login`、`fix-upload-timeout` |
| ADR | `ADR-NNNN-title.md` |
| 验证报告 | `YYYY-MM-DD-subject.md` |
| 事故复盘 | `YYYY-MM-DD-incident-topic.md` |
| Sprint 经验复盘 | `YYYY-MM-DD-sprint-xxx-experience.md` |
| 指南文档 | `topic-guide.md` 或领域约定 |

命名应使用英文 slug，正文可以使用中文。不得使用临时名如 `new.md`、`test.md`、`final-final.md`。

## 13. 文档质量要求 `[通用]`

所有长期技术文档至少满足：

- 有明确目的、范围、来源和更新方式。
- 能回答“为什么、是什么、怎么做、如何验证”。
- 涉及需求或 Bug 时包含来源、状态、验收标准和追溯关系。
- 涉及接口时包含请求、响应、错误码、示例或 OpenAPI 链接。
- 涉及数据库时包含表、字段、索引、迁移、兼容性说明。
- 涉及部署时包含服务、端口、环境变量、启动、停止、回滚说明。
- 涉及架构决策时包含背景、选项、决策、后果。
- 涉及 UI 时包含目标端、状态、交互、响应式、视觉验收来源。
- 内容必须可执行或可验证，不写空洞口号。

## 14. AI 执行顺序 `[通用]`

AI 接到需求、Bug、技术改造或架构调整任务后，必须按以下顺序判断：

```text
1. 阅读 AGENTS.md
2. 阅读 rules/*，特别是 document-governance.md、directory-structure.md、requirement-management.md、bug-management.md
3. 阅读 openspec/project.md（如启用 OpenSpec）
4. 判断是否已有 Requirement 或 Bug
5. 判断是否需要进入 iteration
6. 判断是否需要创建/更新 OpenSpec Change
7. 更新 proposal/design/tasks/spec/test-plan/trace/acceptance
8. 开发 src/
9. 补充 tests/
10. 同步 docs/、compatibility/、rules/、README.md、project.yaml
11. 更新 issues 和 iterations
12. 归档或说明尚不可归档
```

简单小修可以跳过部分步骤，但必须说明判断依据。

## 15. 轻量文档修订 `[通用]`

以下情况可直接编辑，不需创建 OpenSpec Change：

- 修复 typo、格式、链接、标题层级。
- 更新 README 表达，不改变流程语义。
- 补充注释或说明，不改变系统行为。
- 更新版本号引用或文档索引。
- 补充 `待确认` 标记或来源说明。

以下情况不得走轻量修订：

- 改变工作流语义、状态机、guard 策略。
- 改变 API、数据库、权限、部署、兼容性契约。
- 改变验收标准、上线策略、回滚策略。
- 删除归档记录、审批记录、验收记录或追溯关系。

## 16. 评审与人工确认 `[通用 + 个性化]`

文档评审策略为：`{DOC_REVIEW_POLICY}`。

必须人工确认的内容：

- 产品范围、目标用户、验收标准、优先级。
- 架构边界、数据模型、权限模型、安全策略。
- 发布策略、回滚策略、SLA、客户承诺。
- 需求/Bug 状态终态、拒绝、不修、延期。
- 合规、审计、隐私、客户交付相关文档。

AI 可以辅助补全结构、同步引用、生成初稿，但不得伪造评审结论。

## 17. 归档策略 `[通用 + 个性化]`

归档策略为：`{ARCHIVE_POLICY}`。

规则：

- 已归档 OpenSpec、迭代验收报告、发布说明、事故复盘不得删除。
- 归档内容如需修正，应新增修订记录，不得静默覆盖历史。
- 归档后发现问题，应创建新的 Bug、Requirement 或 Change，并关联原归档记录。
- 归档完成后必须确保 Issue、Iteration、OpenSpec、docs、tests 的追踪链闭合。

## 18. 禁止行为 `[通用]`

- 禁止绕过 Requirement/Bug 与 OpenSpec Change 直接开发需求。
- 禁止只改代码不改文档。
- 禁止直接修改 `openspec/specs/` 作为开发中变更。
- 禁止把需求、Bug、迭代、Spec 混在一个文档中。
- 禁止生成无来源、无状态、无验收标准的需求或缺陷文档。
- 禁止删除归档记录、审批记录、验收记录。
- 禁止保留样例项目业务词、业务表、接口资源名。
- 禁止在文档中写入真实密钥、生产数据、未脱敏日志或截图。
- 禁止编造未确认的版本、平台、兼容性结论、客户承诺。

## 19. 初始化生成建议 `[通用]`

用于工程初始化生成 `document-governance.md` 时，建议按以下步骤处理：

1. 根据 `{PRODUCT_NAME}`、`{PRODUCT_CODE}` 替换文档元数据与正文占位符。
2. 根据 `{PROJECT_GOVERNANCE_LEVEL}` 生成研发文档链路；未知时使用标准链路。
3. 根据 `{DOCS_STRUCTURE}` 生成 `docs/` 分层；未知时使用主文档、standards、guides、knowledge-base、README 分层。
4. 根据 `{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{ISSUE_WORKFLOW}` 与需求/缺陷专项规则生成 issues 治理。
5. 根据 `{ITERATION_PATTERN}` 与 `{SPRINT_FACT_SOURCE}` 生成迭代目录、四件套和事实源规则。
6. 根据 `{CHANGE_ID_PATTERN}` 与是否启用 OpenSpec 生成 changes/specs/archive 规则；未启用时替换为项目等价变更系统。
7. 根据 `{PRODUCT_FORMS}` 生成 Web、微信小程序、移动端、桌面端相关文档同步规则。
8. 根据 `{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}` 生成 API、数据库、前端客户端、测试治理规则。
9. 根据 `{DEPLOYMENT_STACK}` 生成部署、环境变量、端口、回滚相关文档同步规则。
10. 根据 `{TASK_TRACKING_SYSTEM}` 保留或删除外部项目管理章节。
11. 删除未启用能力的强制文档，不得保留不存在的路径、命令、模块或业务词。
12. 检查本文档与 `requirement-management.md`、`bug-management.md`、`directory-structure.md`、`global.md`、`testing.md`、`release.md` 一致。

## 20. 完成任务后检查清单 `[通用]`

```text
□ 文档链路覆盖 issues、iterations、openspec、src/tests、docs、archive
□ [通用]、[个性化]、[条件启用] 模块标识完整
□ docs 分类与实际目录结构一致
□ Requirement、Bug、Iteration、OpenSpec 的生命周期清晰
□ requirement-management.md 与 bug-management.md 的专项边界清晰
□ sprint.yaml 或项目事实源规则明确
□ 文档自动同步矩阵覆盖 API、数据库、部署、兼容性、测试、UI、安全
□ 轻量修订与必须创建 Change 的边界清晰
□ 禁止事项覆盖跳过文档、删除归档、编造事实、提交敏感信息
□ 初始化生成建议可被工程生成器直接使用
□ 未保留样例项目业务词或不适用的技术栈硬性要求
```
