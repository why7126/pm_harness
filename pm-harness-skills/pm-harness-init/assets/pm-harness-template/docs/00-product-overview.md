---
purpose: 产品总览
content: 产品定位、目标用户、核心场景、核心能力、产品形态、边界范围、成功指标、文档导航
source: Harness docs/00-product-overview.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；初始化后由项目团队确认；后续由 AI 辅助更新并经人工 Review
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 docs/00-product-overview.md 模块
---

# 产品总览

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如多端、管理后台、媒体、对象存储、算法模型、私有化部署。

## 0. 文档定位 `[通用]`

本文是 `{PRODUCT_NAME}` 的产品入口文档，用于让团队成员和 AI Agent 快速理解：

- 产品要解决什么问题。
- 面向哪些用户和角色。
- 当前包含哪些产品形态和核心能力。
- 哪些场景属于产品范围，哪些暂不纳入。
- 后续需求、设计、开发、测试和发布应以哪些长期文档为事实依据。

本文不替代详细需求文档。具体需求应沉淀到 `issues/requirements/{plan,review,archive}/REQ-*`，具体 BUG 应沉淀到 `issues/bugs/{plan,review,archive}/BUG-*`，架构、接口、数据库、部署、兼容性等长期规则应进入对应 `docs/` 与 `rules/` 文件。

## 1. 生成参数 `[个性化]`

初始化生成本文时，应优先使用用户输入填充以下参数。缺失信息可以标记为 `待确认`，不得编造业务事实。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{BUSINESS_DOMAIN}` | 业务领域 | 待确认 |
| `{PRODUCT_DESCRIPTION}` | 产品一句话定位 | 待确认 |
| `{TARGET_USERS}` | 目标用户、使用角色、管理角色 | 待确认 |
| `{USER_PAIN_POINTS}` | 用户痛点和业务问题 | 待确认 |
| `{PRODUCT_FORMS}` | 产品形态，如 Web、管理后台、微信小程序、移动端、API 服务 | 待确认 |
| `{CORE_SCENARIOS}` | 核心业务场景 | 待确认 |
| `{CORE_CAPABILITIES}` | 核心能力清单 | 待确认 |
| `{OUT_OF_SCOPE}` | 当前阶段不做的事项 | 待确认 |
| `{SUCCESS_METRICS}` | 成功指标或验收指标 | 待确认 |
| `{STAKEHOLDERS}` | 业务、产品、技术、运营、客户等干系人 | 待确认 |

## 2. 产品定位 `[个性化]`

`{PRODUCT_NAME}` 是一个面向 `{BUSINESS_DOMAIN}` 的产品，核心定位如下：

```text
{PRODUCT_DESCRIPTION}
```

产品目标：

- 帮助 `{TARGET_USERS}` 完成 `{CORE_SCENARIOS}` 中的关键任务。
- 统一沉淀业务数据、流程、内容、权限和操作记录。
- 为后续需求迭代、接口设计、测试验证、发布部署提供稳定的产品上下文。

如果项目仍处于初始化阶段，应在本节明确哪些信息已经确认，哪些仍为 `待确认`。

## 3. 目标用户与角色 `[个性化]`

初始化时应根据实际项目生成角色表。每个角色应包含目标、主要场景、权限边界和关注指标。

| 角色 | 主要目标 | 核心场景 | 权限/边界 | 关注指标 |
|---|---|---|---|---|
| `{USER_ROLE_1}` | `{ROLE_1_GOAL}` | `{ROLE_1_SCENARIOS}` | `{ROLE_1_BOUNDARY}` | `{ROLE_1_METRICS}` |
| `{USER_ROLE_2}` | `{ROLE_2_GOAL}` | `{ROLE_2_SCENARIOS}` | `{ROLE_2_BOUNDARY}` | `{ROLE_2_METRICS}` |
| `{ADMIN_ROLE}` | `{ADMIN_GOAL}` | `{ADMIN_SCENARIOS}` | `{ADMIN_BOUNDARY}` | `{ADMIN_METRICS}` |

角色拆分原则：

- 面向最终用户、运营人员、管理员、开发者、外部系统等不同使用者时，应分别建模。
- 不同权限、不同端、不同操作目标的角色不得混写。
- 如果角色尚未确认，应保留占位并在 `issues/requirements/` 中补充调研需求。

## 4. 用户痛点与机会 `[个性化]`

本节说明为什么需要建设该产品。

| 痛点/问题 | 影响对象 | 当前影响 | 产品机会 | 关联需求 |
|---|---|---|---|---|
| `{PAIN_POINT_1}` | `{AFFECTED_USER_1}` | `{CURRENT_IMPACT_1}` | `{PRODUCT_OPPORTUNITY_1}` | `{REQ_ID_OR_PENDING}` |
| `{PAIN_POINT_2}` | `{AFFECTED_USER_2}` | `{CURRENT_IMPACT_2}` | `{PRODUCT_OPPORTUNITY_2}` | `{REQ_ID_OR_PENDING}` |

编写要求：

- 优先描述真实业务问题，而不是直接罗列功能。
- 能量化的影响应给出数据来源；不能量化时标记 `待确认`。
- 每个重要痛点应能追踪到后续需求或 OpenSpec Change。

## 5. 产品形态 `[个性化 + 条件启用]`

根据 `{PRODUCT_FORMS}` 生成本节，只保留项目实际具备或计划具备的形态。

| 产品形态 | 面向对象 | 主要职责 | 入口/路径 | 状态 |
|---|---|---|---|---|
| Web 端 | `{WEB_USERS}` | `{WEB_RESPONSIBILITY}` | `{WEB_ENTRY}` | `{WEB_STATUS}` |
| 管理后台 | `{ADMIN_USERS}` | `{ADMIN_RESPONSIBILITY}` | `{ADMIN_ENTRY}` | `{ADMIN_STATUS}` |
| 微信小程序 | `{WECHAT_MINIAPP_USERS}` | `{WECHAT_MINIAPP_RESPONSIBILITY}` | `{WECHAT_MINIAPP_ENTRY}` | `{WECHAT_MINIAPP_STATUS}` |
| 移动端 App | `{MOBILE_USERS}` | `{MOBILE_RESPONSIBILITY}` | `{MOBILE_ENTRY}` | `{MOBILE_STATUS}` |
| 桌面端 | `{DESKTOP_USERS}` | `{DESKTOP_RESPONSIBILITY}` | `{DESKTOP_ENTRY}` | `{DESKTOP_STATUS}` |
| API / SDK | `{API_USERS}` | `{API_RESPONSIBILITY}` | `{API_ENTRY}` | `{API_STATUS}` |
| 算法/模型服务 | `{ALGORITHM_USERS}` | `{ALGORITHM_RESPONSIBILITY}` | `{ALGORITHM_ENTRY}` | `{ALGORITHM_STATUS}` |

未启用的产品形态应从初始化后的文档中删除，不要保留无效占位。

## 6. 核心场景 `[个性化]`

核心场景应描述用户如何完成业务目标，而不是只列功能名。

| 场景 | 参与角色 | 触发条件 | 用户目标 | 关键步骤 | 成功结果 | 关联需求 |
|---|---|---|---|---|---|---|
| `{SCENARIO_1}` | `{SCENARIO_1_ROLES}` | `{SCENARIO_1_TRIGGER}` | `{SCENARIO_1_GOAL}` | `{SCENARIO_1_STEPS}` | `{SCENARIO_1_RESULT}` | `{REQ_ID_OR_PENDING}` |
| `{SCENARIO_2}` | `{SCENARIO_2_ROLES}` | `{SCENARIO_2_TRIGGER}` | `{SCENARIO_2_GOAL}` | `{SCENARIO_2_STEPS}` | `{SCENARIO_2_RESULT}` | `{REQ_ID_OR_PENDING}` |
| `{SCENARIO_3}` | `{SCENARIO_3_ROLES}` | `{SCENARIO_3_TRIGGER}` | `{SCENARIO_3_GOAL}` | `{SCENARIO_3_STEPS}` | `{SCENARIO_3_RESULT}` | `{REQ_ID_OR_PENDING}` |

场景编写规则：

- 每个场景应至少能回答“谁在什么情况下要完成什么”。
- 涉及多端协同时，应说明端与端之间的数据流或操作边界。
- 涉及管理、审核、发布、权限、数据同步时，应明确角色边界。

## 7. 核心能力 `[个性化]`

核心能力应从业务场景抽象而来，并能映射到后续需求、规格、接口、测试和发布。

| 能力域 | 能力说明 | 主要用户 | 当前阶段 | 关联文档 |
|---|---|---|---|---|
| `{CAPABILITY_DOMAIN_1}` | `{CAPABILITY_DESCRIPTION_1}` | `{CAPABILITY_USERS_1}` | `{CAPABILITY_STATUS_1}` | `{RELATED_DOCS_1}` |
| `{CAPABILITY_DOMAIN_2}` | `{CAPABILITY_DESCRIPTION_2}` | `{CAPABILITY_USERS_2}` | `{CAPABILITY_STATUS_2}` | `{RELATED_DOCS_2}` |
| `{CAPABILITY_DOMAIN_3}` | `{CAPABILITY_DESCRIPTION_3}` | `{CAPABILITY_USERS_3}` | `{CAPABILITY_STATUS_3}` | `{RELATED_DOCS_3}` |

常见能力分类可按项目实际选择：

- 用户、组织、权限、认证。
- 业务对象管理。
- 搜索、筛选、推荐、统计。
- 内容、媒体、文件、对象存储。
- 数据导入导出、同步、备份。
- 工作流、审批、通知、任务。
- API、SDK、Webhook、外部系统集成。
- 算法、模型、推理、自动化 Agent。

## 8. 当前范围与非范围 `[通用 + 个性化]`

### 8.1 当前范围 `[个性化]`

```text
{IN_SCOPE}
```

### 8.2 当前不做 `[个性化]`

```text
{OUT_OF_SCOPE}
```

范围管理规则：

- 当前不做的能力不代表永远不做，但必须通过新需求或 OpenSpec Change 进入开发。
- 不得在没有需求记录的情况下把非范围能力直接做进代码。
- 如果范围变化会影响架构、接口、数据库、部署或权限，必须同步更新对应文档。

## 9. 数据与内容对象 `[个性化 + 条件启用]`

本节用于说明产品围绕哪些核心数据对象运转。

| 对象 | 含义 | 主要来源 | 主要使用方 | 生命周期 | 关联文档 |
|---|---|---|---|---|---|
| `{DATA_OBJECT_1}` | `{DATA_OBJECT_DESC_1}` | `{DATA_SOURCE_1}` | `{DATA_CONSUMER_1}` | `{DATA_LIFECYCLE_1}` | `{RELATED_DOCS_1}` |
| `{DATA_OBJECT_2}` | `{DATA_OBJECT_DESC_2}` | `{DATA_SOURCE_2}` | `{DATA_CONSUMER_2}` | `{DATA_LIFECYCLE_2}` | `{RELATED_DOCS_2}` |

如果项目涉及媒体、对象存储、模型文件或样例数据，应同步阅读：

- `rules/data-management.md`
- `rules/media.md`
- `rules/object-storage.md`
- `docs/04-database-design.md`
- `docs/07-object-storage-strategy.md`

## 10. 成功指标 `[个性化]`

初始化时应根据产品目标生成可验证指标。没有量化数据时可以先写定性指标，并标注数据来源待补充。

| 指标 | 说明 | 目标值 | 数据来源 | 关联场景 |
|---|---|---|---|---|
| `{METRIC_1}` | `{METRIC_DESCRIPTION_1}` | `{METRIC_TARGET_1}` | `{METRIC_SOURCE_1}` | `{RELATED_SCENARIO_1}` |
| `{METRIC_2}` | `{METRIC_DESCRIPTION_2}` | `{METRIC_TARGET_2}` | `{METRIC_SOURCE_2}` | `{RELATED_SCENARIO_2}` |

指标类型示例：

- 使用效率：完成任务时间、步骤数、自动化率。
- 质量：错误率、缺陷率、数据完整率、审核通过率。
- 业务：转化率、活跃度、留存、成交、成本降低。
- 技术：接口成功率、响应时间、可用性、兼容性通过率。

## 11. 约束与假设 `[通用 + 个性化]`

| 类型 | 内容 | 影响 | 处理方式 |
|---|---|---|---|
| 业务约束 | `{BUSINESS_CONSTRAINTS}` | `{BUSINESS_CONSTRAINT_IMPACT}` | `{BUSINESS_CONSTRAINT_ACTION}` |
| 技术约束 | `{TECH_CONSTRAINTS}` | `{TECH_CONSTRAINT_IMPACT}` | `{TECH_CONSTRAINT_ACTION}` |
| 合规/安全约束 | `{SECURITY_CONSTRAINTS}` | `{SECURITY_CONSTRAINT_IMPACT}` | `{SECURITY_CONSTRAINT_ACTION}` |
| 交付约束 | `{DELIVERY_CONSTRAINTS}` | `{DELIVERY_CONSTRAINT_IMPACT}` | `{DELIVERY_CONSTRAINT_ACTION}` |
| 未确认假设 | `{ASSUMPTIONS}` | `{ASSUMPTION_IMPACT}` | `{ASSUMPTION_VALIDATION}` |

重要约束必须能追踪到 `rules/`、`docs/`、`issues/` 或 `openspec/` 中的具体文档。

## 12. 文档导航 `[通用]`

建议按以下顺序阅读项目文档：

| 文档 | 用途 |
|---|---|
| `AGENTS.md` | AI Agent 行为入口和任务执行规则 |
| `README.md` | 面向人类读者的项目入口 |
| `docs/00-product-overview.md` | 产品定位、用户、场景和能力总览 |
| `docs/01-architecture.md` | 系统架构和模块关系 |
| `docs/02-deployment.md` | 部署方式、环境变量、服务地址 |
| `docs/03-api-index.md` | API 索引和接口导航 |
| `docs/04-database-design.md` | 数据库设计、核心对象、迁移说明 |
| `docs/05-compatibility-matrix.md` | 兼容性矩阵 |
| `docs/06-video-asset-management.md` | 媒体或视频资产治理，未启用时可删除或标记不适用 |
| `docs/07-object-storage-strategy.md` | 对象存储策略，未启用时可删除或标记不适用 |
| `docs/knowledge-base/` | 长期知识沉淀、故障复盘、经验记录 |
| `docs/standards/` | API、测试、错误码等治理细则，若项目采用 standards 分层则启用 |
| `rules/` | 全局研发规范和 AI 强制约束 |
| `issues/requirements/{plan,review,archive}/` | 需求记录和需求包 |
| `issues/bugs/{plan,review,archive}/` | BUG 记录和缺陷包 |
| `iterations/` | 迭代计划、验收和发布说明 |
| `openspec/` | 能力规格、变更和归档 |

## 13. 更新触发条件 `[通用]`

发生以下情况时，必须更新本文：

- 产品定位、目标用户或业务范围变化。
- 新增或移除产品形态。
- 核心场景、核心能力或成功指标变化。
- 业务边界、非范围、角色权限发生变化。
- 新增重要数据对象、媒体对象、模型对象或外部集成。
- 初始化模板参数变化，导致生成后的产品概览不再准确。

更新本文时，应同步检查：

- `AGENTS.md`
- `README.md`
- `project.yaml`
- `docs/01-architecture.md`
- `docs/03-api-index.md`
- `docs/04-database-design.md`
- `rules/global.md`
- `rules/document-governance.md`
- `rules/directory-structure.md`
- `issues/requirements/`
- `openspec/project.md`

## 14. 初始化生成建议 `[通用]`

工程初始化工具生成本文时应遵循：

1. 保留所有 `[通用]` 模块。
2. 用用户输入替换所有 `[个性化]` 占位符。
3. 根据项目能力保留或删除 `[条件启用]` 模块。
4. 未启用 Web、微信小程序、移动端、媒体、对象存储、算法模型时，删除对应产品形态和能力说明。
5. 对缺失但重要的信息标记 `待确认`。
6. 不得保留来源项目的业务名、用户角色、能力名称、服务地址或技术假设。
7. 生成后检查本文是否能回答：
   - 产品是什么？
   - 谁在使用？
   - 解决什么问题？
   - 当前做什么，不做什么？
   - 后续需求和设计应该看哪些文档？
