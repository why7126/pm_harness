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
├── pm-harness/          # Harness 工程模板主体，后续持续迭代该工程结构
├── pm-harness-cases/    # Harness 使用案例，用真实或示例项目验证模板可用性
└── pm-harness-skills/   # Harness 应用 Skill，用于初始化、生成、维护 Harness 工程
```

### pm-harness

`pm-harness/` 是标准 Harness 工程目录结构，包含需求、Bug、迭代、OpenSpec、规则、文档、专项标准、源码、模型资产、部署配置和测试等模块。后续对 Harness 能力的增强，优先在这里沉淀。

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

### pm-harness-cases

`pm-harness-cases/` 用于存放该 Harness 工程的使用案例。案例项目应尽量保留完整闭环，包括需求、迭代、OpenSpec、实现目录、测试目录和相关文档，方便验证模板是否真正可用于产品研发流程。

当前示例：

```text
pm-harness-cases/
└── tilesfst/
```

### pm-harness-skills

`pm-harness-skills/` 用于存放该 Harness 工程的应用 Skill。例如 `pm-harness-init` 可基于模板快速初始化一个新的 PM Harness 工程。

```text
pm-harness-skills/
└── pm-harness-init/
    ├── SKILL.md
    └── assets/
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

本仓库提供 `pm-harness-init` Skill，用于基于模板初始化新的 Harness 工程。

典型使用场景：

- 为一个新产品创建标准 PM Harness 工程。
- 生成 OpenSpec + AI Agent 规范编程项目结构。
- 根据产品名称、项目代码、产品简介、产品形态、技术栈、能力开关、治理流程、部署方式、测试策略等信息生成可复制的工程骨架。

Skill 位置：

```text
pm-harness-skills/pm-harness-init/SKILL.md
```

## 适用场景

Project PM Harness 适合以下团队或项目：

- 产品经理希望把需求、原型、迭代和研发实现放在同一套工程结构中管理。
- 团队使用 OpenSpec 管理工程变更，但需要补齐产品需求和迭代闭环。
- AI Coding 项目需要清晰的上下文、规则、验收标准和可追踪文档。
- 研发需要从产品原型图、原型上下文和 HTML 原型中一比一复现产品设计。
- 项目需要长期沉淀可复用的需求模板、迭代模板、OpenSpec 模板和 Agent Skill。

## 维护原则

- 需求是业务来源，OpenSpec 是工程变更来源，迭代是交付节奏来源。
- 任何需求进入实现前，都应明确所属迭代和对应 OpenSpec Change。
- 任何 OpenSpec Change 都应能追溯到需求或基础设施建设目标。
- 任何迭代都应能列出其包含的需求、Bug、OpenSpec Change、验收结果和发布说明。
- 产品原型资产应和需求一起版本化，避免视觉、交互和实现上下文丢失。
- 状态变化必须回写到追踪文档，保证人、脚本和 AI Agent 读取到同一事实。
