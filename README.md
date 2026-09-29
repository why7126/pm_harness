# Project PM Harness

Project PM Harness 是一个面向产品经理的 AI Coding Harness 工程模板。它在 OpenSpec 的基础上，补齐了产品侧最常用、也最容易断链的两块能力：**需求管理**和**迭代管理**。

这个工程的目标不是只写一份 PRD，也不是只维护一组技术规格，而是打通从「需求提出」到「进入迭代」再到「OpenSpec 设计、实现、验收、归档」的完整闭环，让产品、研发、测试和 AI Agent 都可以围绕同一套结构协作。

## 核心定位

传统 OpenSpec 更偏向工程变更管理：先定义 change，再拆 design、tasks、specs，并在实现后归档为稳定能力。Project PM Harness 在此基础上新增产品经理视角：

- 需求管理：沉淀 PRD、用户故事、业务流程、验收标准、需求状态和追踪关系。
- 迭代管理：沉淀 Sprint 目标、范围、需求列表、OpenSpec Change 列表、验收报告和发布说明。
- 状态管理：让需求、迭代、OpenSpec Change 都具备清晰的生命周期。
- 关联追踪：可以回答「某个需求在哪个迭代实现」「对应哪个 OpenSpec」「某个迭代包含哪些需求和 OpenSpec」「当前迭代状态是什么」。
- 原型协作：在需求管理中引入产品原型图、原型上下文说明和 HTML 原型，让开发可以一比一复现产品设计。

## 仓库目录

```text
.
├── .agents/skills/      # 项目级已安装 Agent Skill 入口
├── design-schemes/      # 本地设计资产库，沉淀可复用 UI/UE 与导航方案
├── docs/                # 当前脚手架工程自身的长期产品、架构、治理和维护文档
├── issues/              # 当前脚手架工程自身的需求和 BUG 池
├── iterations/          # 当前脚手架工程自身的 Sprint / 迭代记录
├── openspec/            # 当前脚手架工程自身的 OpenSpec 事实源
├── pm-harness/          # 生成新项目用的 Harness 工程模板主体
└── pm-harness-skills/   # Harness 应用 Skill，用于初始化新工程、改造存量项目和维护 Harness 工程
```

### docs 与 spec-logs

根目录 `docs/` 属于当前 ProjectPmHarness 脚手架工程自身：

- `docs/` 沉淀长期稳定的产品、架构、治理和维护文档。
- `issues/`、`iterations/`、`openspec/` 分别承载当前脚手架工程自身的需求/BUG、Sprint 和 OpenSpec 变更事实源。
- `docs/spec-logs/` 记录一次次 spec 学习、治理优化和规范迭代过程。

`pm-harness/` 是生成新项目用的模板目录，不承载当前 ProjectPmHarness 的实际项目数据。模板内的 `pm-harness/docs/` 与 `pm-harness/docs/spec-logs/` 只代表未来生成项目的默认结构。

### design-schemes

`design-schemes/` 是本地设计资产库，用于沉淀可复用的 UI/UE 设计方案、导航栏模式和可直接预览的 HTML Demo。它服务于两类场景：

- 新项目初始化：从已沉淀方案中选择整体 UI/UE、导航栏或两者组合，作为 `rules/ui-design.md`、Design Token 和原型预览的输入。
- 存量项目重构：把整体视觉语言和导航结构拆开评估，支持只替换导航栏、只替换组件风格或完整套用方案。

当前目录结构：

```text
design-schemes/
├── README.md
├── registry.json
└── schemes/
    └── tilesfst/
        ├── meta.json
        ├── design.json
        ├── navigation.json
        ├── demo.html
        └── navigation-demo.html
```

其中 `design.json` 是整体 UI/UE 事实源，`navigation.json` 是导航栏事实源，两个 HTML 文件用于让用户一眼确认方案效果。

### pm-harness

`pm-harness/` 是标准 Harness 工程模板目录结构，包含需求、Bug、迭代、OpenSpec、规则、文档、专项标准、源码、模型资产、部署配置和测试等模块。只有确认会作为新项目默认能力交付的规范、脚本、技能、目录和模板文件，才同步进入这里。

核心目录：

```text
pm-harness/
├── deploy/              # 部署配置、部署脚本和环境编排文件
├── docs/                # 产品、架构、部署、接口、数据库、测试治理等项目文档
│   └── standards/       # API、认证、错误码、上传、测试、覆盖率等专项标准
├── issues/
│   ├── requirements/    # 需求管理
│   └── bugs/            # Bug 管理
├── iterations/          # 迭代管理
├── models/              # 模型文件、模型权重和模型相关资产
├── openspec/            # OpenSpec project、changes、specs、archive
├── rules/               # AI Agent 与工程协作规则
├── scripts/             # 工程脚本
├── src/                 # 业务源码目录占位
└── tests/               # 单元、集成、E2E、兼容性测试目录
```

### pm-harness-skills

`pm-harness-skills/` 用于存放该 Harness 工程的应用 Skill。`pm-harness-init` 面向新项目初始化，`pm-harness-refactor` 面向存量项目的非破坏式接入、重构和治理化改造，`pm-harness-uidesign` 面向真实项目 UI/UE 设计资产提炼，`pm-prd-position`、`pm-prd-plan`、`pm-prd-mvp`、`pm-prd-design` 共同覆盖从产品定位、产品规划、MVP 收敛到 PRD 与可点击原型交付的产品设计链路，`tool-info-lookup` 面向工具信息调研与结构化信息卡片输出。

项目根目录的 `.agents/skills/` 是当前仓库的已安装 Skill 入口；需要让本项目直接使用某个 Skill 时，从 `pm-harness-skills/` 同步到 `.agents/skills/`。

```text
pm-harness-skills/
├── pm-harness-init/
│   ├── SKILL.md
│   ├── assets/
│   └── references/
├── pm-harness-refactor/
│   ├── SKILL.md
│   ├── assets/
│   └── references/
├── pm-harness-uidesign/
│   ├── SKILL.md
│   └── references/
├── pm-prd-position/
│   ├── SKILL.md
│   └── README.md
├── pm-prd-plan/
│   ├── SKILL.md
│   ├── assets/
│   └── references/
├── pm-prd-mvp/
│   ├── SKILL.md
│   ├── assets/
│   ├── references/
│   └── scripts/
├── pm-prd-design/
│   ├── SKILL.md
│   ├── prompts/
│   ├── schemas/
│   ├── templates/
│   └── validators/
└── tool-info-lookup/
    └── SKILL.md
```

## 闭环模型

Project PM Harness 关注三个核心对象：

| 对象 | 目录 | 作用 |
|---|---|---|
| 需求 Requirement | `issues/requirements/{REQ-ID}/` | 描述产品目标、用户故事、业务流程、验收标准和原型资产 |
| 迭代 Sprint | `iterations/{sprint-id}/` | 管理一段时间内承诺交付的需求、Bug、OpenSpec Changes 和验收结果 |
| OpenSpec Change | `openspec/changes/{change-id}/` | 将需求转化为可实现、可验收、可归档的工程变更 |

三者之间通过 `trace.md`、`sprint.md`、`sprint.yaml` 和 OpenSpec Change 中的追踪文档互相关联。

```text
产品需求
  ↓
issues/requirements/REQ-xxxx/
  ↓ 关联 iteration 与 change_id
iterations/sprint-XXX/
  ↓ 纳入 changes 列表
openspec/changes/{change-id}/
  ↓ 实现、验收、归档
openspec/specs/ 或 openspec/archive/
```

通过这个模型，可以持续追踪：

- 一个需求属于哪个迭代。
- 一个需求对应哪个或哪些 OpenSpec Change。
- 一个迭代包含哪些需求、Bug 和 OpenSpec Change。
- 一个 OpenSpec Change 来源于哪个需求，并在哪个迭代完成。
- 需求、迭代、OpenSpec Change 当前分别处于什么状态。

## 需求管理

每个需求建议使用独立目录管理：

```text
issues/requirements/REQ-0001-user-login/
├── requirement.md       # 需求文档 / PRD
├── user-stories.md      # 用户故事
├── business-flow.md     # 业务流程
├── acceptance.md        # 验收标准
├── trace.md             # 需求追踪：状态、迭代、OpenSpec、实现路径
└── prototype/           # 产品原型资产，可按端或页面继续分层
```

需求文档不仅描述功能，还需要明确：

- 业务背景与目标。
- 目标用户和使用场景。
- 页面范围、端范围和不包含范围。
- 用户故事与验收标准。
- 字段、控件、交互和视觉约束。
- 接口、数据、权限、埋点、非功能需求。
- 待确认事项和风险。

### 需求状态

推荐需求状态流转：

```text
draft → approved → in_progress → resolved → closed
```

| 状态 | 含义 |
|---|---|
| draft | 需求草稿，仍在补充或评审前 |
| approved | 需求已确认，可进入迭代或 OpenSpec 设计 |
| in_progress | 已进入迭代或已开始实现 |
| resolved | 实现完成，等待验收或发布确认 |
| closed | 已验收、发布或确认关闭 |

状态变化应同步更新需求目录下的 `trace.md`。

## 产品原型管理

Project PM Harness 将产品原型作为需求的一部分，而不是游离在聊天记录、网盘或设计工具截图里。

推荐结构：

```text
issues/requirements/REQ-0001-user-login/prototype/
└── web/
    ├── user-login.png   # 产品原型图，图片格式
    ├── user-login.md    # 原型上下文：组件、布局、交互、Design Token、还原要求
    └── user-login.html  # 可运行 HTML 原型，供开发一比一复现
```

三类原型资产的作用：

| 文件 | 作用 |
|---|---|
| 图片原型 | 作为视觉基准，明确最终页面应该长什么样 |
| Markdown 上下文 | 解释图片中无法表达的组件结构、交互状态、响应式规则和设计约束 |
| HTML 原型 | 给开发和 AI Agent 提供可运行、可检查、可复用的实现参考 |

建议在 `trace.md` 中显式登记原型资产路径，确保研发实现时可以从需求直接定位到视觉来源。

需要从零生成或迭代 PRD + 交互 + 可点击原型交付包时，使用 `pm-prd-design` Skill。它的标准交付物包括 `requirement.md`、`interaction.md`、`prototype.html`、`prototype-context.md`、`prototype.png`、`version-manifest.md` 和 `package.zip`；ITERATE/PATCH 场景还会补充变更、差异和回归报告。具体页面原型仍应归档到对应 `issues/requirements/**/prototype/` 下，长期复用的视觉方案才进入 `design-schemes/`。

当产品仍处于早期定义阶段时，建议先按 `pm-prd-position → pm-prd-plan → pm-prd-mvp → pm-prd-design` 顺序推进：先冻结定位，再形成规划基线，再收敛 MVP，最后进入详细 PRD 和交互原型。

## 设计资产管理

除单个需求下的原型资产外，长期复用的设计方案统一沉淀到 `design-schemes/`。

推荐将设计资产拆成两层：

| 资产 | 文件 | 作用 |
|---|---|---|
| 整体 UI/UE 方案 | `design.json`、`demo.html` | 沉淀颜色、字体、间距、组件、页面密度、响应式和整体体验预览 |
| 导航栏方案 | `navigation.json`、`navigation-demo.html` | 沉淀导航结构、菜单分组、激活态、折叠态、权限态和移动端行为 |

这类资产不替代 `issues/requirements/**/prototype/` 中的具体页面原型。它更像可复用的设计系统种子：新项目初始化或已有项目重构时，可以先选方案，再将具体页面原型绑定到对应需求。

## 迭代管理

每个迭代使用独立目录：

```text
iterations/sprint-001/
├── sprint.md            # 迭代说明：目标、范围、需求、Change、风险、后续
├── sprint.yaml          # 结构化迭代元数据，便于脚本和 AI Agent 读取
├── acceptance-report.md # 迭代验收报告
└── release-note.md      # 发布说明
```

迭代需要回答：

- 本次迭代目标是什么。
- 包含哪些需求和 Bug。
- 包含哪些 OpenSpec Change。
- 当前迭代状态是什么。
- 验收结果、遗留问题和发布范围是什么。

### 迭代状态

推荐迭代状态流转：

```text
planned → in_progress → acceptance → released → closed
```

| 状态 | 含义 |
|---|---|
| planned | 迭代已规划，范围待启动或待锁定 |
| in_progress | 需求和 OpenSpec Change 正在设计或实现 |
| acceptance | 已进入验收阶段 |
| released | 已发布或具备发布记录 |
| closed | 迭代关闭，验收报告和发布说明已归档 |

`sprint.yaml` 适合保存结构化状态，例如：

```yaml
sprint_id: sprint-001
status: in_progress
requirements:
  - REQ-0001-user-login
changes:
  - add-user-login
```

## OpenSpec 管理

OpenSpec 仍然是工程变更的核心事实源：

```text
openspec/
├── project.md
├── config.yaml
├── changes/             # 正在设计或实现的变更
├── specs/               # 已生效的稳定规格
└── archive/             # 已完成并归档的变更
```

每个 Change 建议包含：

```text
openspec/changes/add-user-login/
├── proposal.md
├── design.md
├── tasks.md
├── test-plan.md
├── acceptance.md
└── trace.md
```

其中 `trace.md` 应记录：

- `change_id`
- 来源需求 `requirement`
- 所属迭代 `iteration`
- 当前状态 `status`
- 关联的 OpenSpec、实现路径、测试和归档信息

## 三方追踪关系

建议在三个位置同时维护追踪关系，形成互相校验：

| 位置 | 应记录内容 |
|---|---|
| `issues/requirements/{REQ-ID}/trace.md` | 需求状态、所属迭代、关联 OpenSpec Change、原型资产、实现路径、测试范围 |
| `iterations/{sprint-id}/sprint.md` / `sprint.yaml` | 迭代状态、需求列表、Bug 列表、Change 列表、验收与发布信息 |
| `openspec/changes/{change-id}/trace.md` | Change 来源需求、所属迭代、状态、归档位置、关联实现 |

这样既方便人读，也方便 AI Agent 和脚本做一致性检查。

## 推荐工作流

1. 新建需求目录：在 `issues/requirements/` 下创建 `REQ-xxxx-name/`。
2. 编写需求文档：补齐 `requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`。
3. 补充产品原型：添加图片原型、原型上下文 Markdown 和 HTML 原型。
4. 建立需求追踪：在 `trace.md` 中登记状态、优先级、目标端、迭代和候选 OpenSpec Change。
5. 纳入迭代：在 `iterations/sprint-XXX/` 中登记需求和计划交付范围，例如 `iterations/sprint-001/`。
6. 创建 OpenSpec Change：在 `openspec/changes/` 下编写 proposal、design、tasks、test-plan、acceptance。
7. 实现与验收：研发按 OpenSpec 和原型资产实现，测试按 acceptance 与 test-plan 验收。
8. 状态回写：同步更新需求、迭代、OpenSpec Change 的状态。
9. 归档发布：完成后归档 OpenSpec，更新迭代验收报告和 release note。

## Skill 应用

本仓库提供以下 Harness 应用 Skill：

| Skill | 适用对象 | 典型用途 |
|---|---|---|
| `pm-harness-init` | 新项目 | 基于模板初始化新的 PM Harness 工程 |
| `pm-harness-refactor` | 存量项目 | 将 PM Harness / OpenSpec + AI Agent 规范工程非破坏式接入已有代码仓库 |
| `pm-harness-uidesign` | 设计资产库 | 从真实项目提炼 UI/UE、导航栏和 HTML Demo 设计资产 |
| `pm-prd-position` | 产品定位 | 通过反问、假设挑战和决策记录生成产品定位基线包 |
| `pm-prd-plan` | 产品规划 | 承接定位基线，生成产品架构、里程碑、功能清单、边界和规划基线包 |
| `pm-prd-mvp` | MVP 收敛 | 将完整规划收敛为可验证、可交付、可进入详细设计的 MVP 基线包 |
| `pm-prd-design` | 产品需求与原型 | 工程化生成或迭代 PRD、交互说明、可点击原型和版本化交付包 |
| `tool-info-lookup` | 工具调研 | 联网调研工具基本情况，输出固定字段的信息卡片或对比表 |

### pm-harness-init

典型使用场景：

- 为一个新产品创建标准 PM Harness 工程。
- 生成 OpenSpec + AI Agent 规范编程项目结构。
- 根据产品名称、项目代码、产品简介、产品形态、技术栈、能力开关、治理流程、部署方式、测试策略等信息生成可复制的工程骨架。

Skill 入口：

```text
pm-harness-skills/pm-harness-init/SKILL.md
```

### pm-harness-refactor

典型使用场景：

- 将已有项目接入 PM Harness 目录、规则、文档、需求/Bug/迭代和 OpenSpec 治理。
- 在不破坏旧项目源码、配置、CI 和文档的前提下合并 Harness 资产。
- 将旧业务源码复制或整合到新的 Harness 输出目录，并生成 `docs/harness-adoption/` 接入记录。
- 给存量项目补齐 `.agents/skills/` 单一 Agent 技能入口和校验脚本。

Skill 入口：

```text
pm-harness-skills/pm-harness-refactor/SKILL.md
```

### pm-harness-uidesign

典型使用场景：

- 从本地项目代码库、GitHub 仓库或代码压缩包中提炼真实 UI/UE 设计方案。
- 将整体视觉方案、导航栏/侧边栏、Design Token 和关键交互拆分沉淀到 `design-schemes/`。
- 生成 `design.json`、`navigation.json`、`ui-design.md`、`demo.html` 和 `navigation-demo.html`。
- 为后续新项目初始化或存量项目重构提供可预览、可复用的设计资产。

Skill 入口：

```text
pm-harness-skills/pm-harness-uidesign/SKILL.md
```

### pm-prd-position

典型使用场景：

- 从一句产品想法开始建立完整产品定位。
- 对现有产品做重新定位或局部定位 Patch。
- 明确产品定义、目标用户、核心问题、价值主张、市场、竞争、商业交付和产品边界。
- 输出可交接给 `pm-prd-plan` 的产品定位基线包。

Skill 入口：

```text
pm-harness-skills/pm-prd-position/SKILL.md
```

### pm-prd-plan

典型使用场景：

- 承接产品定位基线，规划产品域、功能模块和核心能力。
- 生成产品里程碑、功能清单、范围边界、依赖风险和设计交接说明。
- 对已有规划做重新规划或局部 Patch。
- 输出可交接给 `pm-prd-mvp` 或 `pm-prd-design` 的规划基线包。

Skill 入口：

```text
pm-harness-skills/pm-prd-plan/SKILL.md
```

### pm-prd-mvp

典型使用场景：

- 将完整产品规划收敛为首个可验证版本。
- 明确 MVP 目标、核心假设、最小业务闭环、范围取舍、递进版本和验证方案。
- 重新评估 MVP 或对 MVP 范围做局部 Patch。
- 输出可交接给 `pm-prd-design` 的 MVP 基线包。

Skill 入口：

```text
pm-harness-skills/pm-prd-mvp/SKILL.md
```

### pm-prd-design

典型使用场景：

- 从零创建企业级产品的 PRD、交互说明和可点击高保真原型。
- 在已有交付包基础上做整体迭代，并产出变更说明、差异报告和回归报告。
- 对现有原型做小范围 PATCH，明确保留未授权修改区域，避免布局和设计系统漂移。
- 生成可版本化的 `package.zip`，作为需求评审、研发实现和后续迭代的事实源。

Skill 入口：

```text
pm-harness-skills/pm-prd-design/SKILL.md
```

### tool-info-lookup

典型使用场景：

- 快速调研一个软件、工具或产品的基本情况。
- 查询工具是否开源、GitHub 地址、星数、官网、文档、Demo、适用平台、价格和所属公司。
- 生成包含 17 个固定字段的工具信息卡片。
- 多工具选型时输出同字段对比表。

Skill 入口：

```text
pm-harness-skills/tool-info-lookup/SKILL.md
```

## 适用场景

Project PM Harness 适合以下团队或项目：

- 产品经理希望把需求、原型、迭代和研发实现放在同一套工程结构中管理。
- 团队使用 OpenSpec 管理工程变更，但需要补齐产品需求和迭代闭环。
- AI Coding 项目需要清晰的上下文、规则、验收标准和可追踪文档。
- 研发需要从产品原型图、原型上下文和 HTML 原型中一比一复现产品设计。
- 产品经理需要稳定生成、迭代或小范围修补 PRD + 交互 + 原型交付包。
- 项目需要长期沉淀可复用的需求模板、迭代模板、OpenSpec 模板和 Agent Skill。
- 项目需要沉淀可复用的 UI/UE、导航栏和 HTML 视觉预览，用于后续初始化或重构。

## 维护原则

- 需求是业务来源，OpenSpec 是工程变更来源，迭代是交付节奏来源。
- 任何需求进入实现前，都应明确所属迭代和对应 OpenSpec Change。
- 任何 OpenSpec Change 都应能追溯到需求或基础设施建设目标。
- 任何迭代都应能列出其包含的需求、Bug、OpenSpec Change、验收结果和发布说明。
- 产品原型资产应和需求一起版本化，避免视觉、交互和实现上下文丢失。
- 可复用设计资产应进入 `design-schemes/`，并同时提供结构化 JSON 和可直接打开的 HTML Demo。
- 状态变化必须回写到追踪文档，保证人、脚本和 AI Agent 读取到同一事实。
