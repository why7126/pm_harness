---
purpose: 需求管理与交付追踪规范
content: 规范需求捕获、澄清、目录结构、状态机、命令阶段、评审门禁、Readiness、原型、验收标准、OpenSpec 转换、迭代流转、变更控制和 AI 处理边界
source: Harness requirement-management.md 抽象模板，基于项目需求治理规则沉淀
update_method: 项目初始化时按用户输入生成；需求命令族、状态机、目录结构、评审门禁、迭代流程或 OpenSpec 流程变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 09:02:51
note: 适用于 {PRODUCT_NAME} 项目；AI 处理需求必须保留需求来源、决策链、验收链和交付追踪链
template_scope: 可作为工程初始化的 requirement-management.md 模块
---
# 需求管理与交付追踪规范

## 0. 规则定位 `[通用]`

本文件定义 `{PRODUCT_NAME}` 的需求生命周期、目录结构、状态机、需求包、评审门禁、Readiness、原型、验收标准、OpenSpec 转换、迭代流转和交付追踪规则。所有业务需求、产品能力、体验优化、技术型需求和交付范围变更，均应按本规范记录和流转。

AI 在执行以下任务前必须先阅读本文件：

- 捕获、澄清、补全、评审、拆分、合并、延期或关闭需求。
- 将需求转换为 OpenSpec change、迭代任务、研发任务或验收计划。
- 生成 PRD、用户故事、业务流程、验收标准、原型说明和 trace。
- 修改需求命令族、需求目录、状态机、评审门禁或 Readiness 规则。
- 判断需求是否可进入 Sprint、是否可进入实现、是否需要原型或设计评审。

## 1. 文档模块分类 `[通用]`

本模板将需求规则拆分为三类，工程初始化时应根据用户输入生成最终文档：

- `[通用]`：所有项目默认保留的需求治理基线。
- `[个性化]`：必须根据团队流程、命令族、目录结构、优先级、评审门禁和迭代方式替换的内容。
- `[条件启用]`：仅在项目启用对应能力时保留，例如 OpenSpec、原型、设计评审、外部看板、客户需求、合规需求、多端需求等。

推荐初始化参数：

| 参数 | 用途 |
| --- | --- |
| `{PRODUCT_NAME}` | 项目或产品名称 |
| `{PRODUCT_CODE}` | 项目标识、包名前缀或服务标识 |
| `{REQ_ROOT_DIR}` | 需求根目录，例如 `issues/requirements/` |
| `{REQ_ID_PATTERN}` | 需求编号规则，例如 `REQ-NNNN-slug` |
| `{REQ_REGISTRY_FILE}` | 需求登记文件，例如 `_registry.yaml` |
| 默认需求命令族 | `/req-capture`、`/req-explore`、`/req-generate`、`/req-complete`、`/req-review`、`/req-opsx` |
| `{REQ_STATUS_MACHINE}` | 需求状态机 |
| `{REQ_PRIORITY_LEVELS}` | 需求优先级定义 |
| `{REQ_TYPE_TAXONOMY}` | 需求类型分类 |
| `{REQ_REVIEW_POLICY}` | 需求评审门禁 |
| `{REQ_READINESS_POLICY}` | 需求 Readiness 规则 |
| `{REQ_SPRINT_POLICY}` | 需求进入迭代规则 |
| `{REQ_TO_CHANGE_POLICY}` | 需求转 OpenSpec change 或研发任务规则 |
| `{REQ_PROTOTYPE_POLICY}` | 原型、设计稿、交互稿规则 |
| `{REQ_ACCEPTANCE_POLICY}` | 验收标准规则 |
| `{REQ_TRACE_POLICY}` | trace 字段和追踪关系规则 |
| `{REQ_CHANGE_CONTROL_POLICY}` | 需求变更控制规则 |
| `{TASK_TRACKING_SYSTEM}` | 外部看板或任务系统 |

## 2. 需求治理总原则 `[通用]`

- 先记录，再实现：正式需求必须有可追踪的需求记录。
- 先澄清，再设计：需求不得在目标、范围、用户、验收标准不清时直接进入实现。
- 先评审，再排期：只有通过评审的需求可以进入 Sprint 或研发变更。
- 先验收，再关闭：需求关闭必须有验收结果、测试结果和交付追踪。
- 事实源明确：需求状态、优先级、范围、关联变更必须有单一事实源。
- 变更可追踪：范围变化、优先级变化、延期、拆分、合并必须记录原因和影响。
- 不混淆缺陷：Bug 修复应走 `rules/bug-management.md`，除非评审确认转为新需求。

## 3. 需求目录结构 `[通用 + 个性化]`

需求根目录为：`{REQ_ROOT_DIR}`。

需求编号规则为：`{REQ_ID_PATTERN}`。

需求登记文件为：`{REQ_REGISTRY_FILE}`。

推荐目录结构：

```text
{REQ_ROOT_DIR}
├── {REQ_REGISTRY_FILE}
└── {REQ_ID_PATTERN}/
    ├── capture.md
    ├── requirement.md
    ├── user-stories.md
    ├── business-flow.md
    ├── acceptance.md
    ├── trace.md
    ├── review.md
    ├── change-log.md
    ├── prototype/
    │   ├── web/
    │   ├── admin/
    │   ├── wechat-miniapp/
    │   ├── mobile/
    │   └── desktop/
    └── attachments/
```

文件职责：

| 文件 | 职责 |
| --- | --- |
| `capture.md` | 原始诉求、来源、背景、初始问题、约束 |
| `requirement.md` | 结构化需求说明、目标、范围、优先级、非目标 |
| `user-stories.md` | 用户角色、用户故事、场景、价值 |
| `business-flow.md` | 业务流程、状态流、权限流、异常流 |
| `acceptance.md` | 验收标准、Given/When/Then、验收清单 |
| `trace.md` | 状态、生命周期、迭代、OpenSpec、PR、测试、发布追踪 |
| `review.md` | 评审结论、问题清单、决策、下一步 |
| `change-log.md` | 需求变更记录、范围调整、延期、拆分、合并 |
| `prototype/` | 原型、截图、交互说明、设计稿导出 |
| `attachments/` | 访谈、调研、竞品、客户材料等脱敏附件 |

规则：

- 业务需求必须放在 `{REQ_ROOT_DIR}`，不得散落在 `docs/product/`、`docs/prd/`、聊天记录或临时文档中。
- 需求物理阶段目录、迁移时机、`lifecycle_stage` 与 registry 同步规则以 `rules/issues-lifecycle.md` 为准。
- 需求目录必须按生命周期放入 `{REQ_ROOT_DIR}/plan/`、`{REQ_ROOT_DIR}/review/`、`{REQ_ROOT_DIR}/archive/` 三个分区。
- 新捕获、探索中、草稿、补齐中或待评审的需求必须位于 `plan/`；评审通过后必须移动到 `review/`；验收关闭、拒绝或延期关闭后必须移动到 `archive/`。
- 每个需求目录必须能独立说明“为什么做、为谁做、做什么、不做什么、如何验收、何时交付”。
- `/req-capture` 接收会议纪要、反馈原文或长文本时，MUST 先评估是否包含多个独立需求；若存在多个独立用户目标、业务价值、功能边界、验收标准、优先级或交付节奏，必须拆分为多个 REQ 分别登记。
- 不应把多个可独立评审、独立排期或独立验收的需求塞进同一个 `capture.md`；同一目标下的字段、约束、边界条件和验收点可以保留在同一个 REQ 中。
- 附件必须脱敏，不得提交真实密钥、客户隐私、生产数据原文。
- 进入实现前，`requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md` 必须完整。

## 4. 需求登记表 `[条件启用]`

当项目使用集中登记文件、外部看板同步或自动化统计时启用本节。

`{REQ_REGISTRY_FILE}` 推荐记录：

```yaml
requirements:
  - id: REQ-0001-example
    title: 示例需求标题
    status: captured
    type: feature
    priority: P1
    owner: 待确认
    requester: 待确认
    target_iteration: 待确认
    related_changes: []
```

要求：

- 新增需求目录时必须同步登记表。
- 状态、优先级、负责人、目标迭代、关联变更变化时必须同步登记表。
- 登记表是索引，不替代需求目录中的详细材料。
- 以上同步必须由 `python scripts/sync-workflow-status.py --event req.<action> --req <REQ-ID> ...` 执行或校验；命令不得跳过最终 Workflow Sync。

## 5. 状态机 `[通用 + 个性化]`

需求状态机为：`{REQ_STATUS_MACHINE}`。

推荐状态：

| status | 含义 | 下一步 |
| --- | --- | --- |
| `captured` | 已记录原始诉求 | 澄清背景、目标、范围 |
| `exploring` | 探索中，尚未落结构化需求 | 生成 `requirement.md` |
| `draft` | 已有 `requirement.md`，材料不完整 | 补用户故事、流程、验收 |
| `enriching` | 需求包补齐中 | 进入评审 |
| `pending_review` | 文档齐全，待评审 | 批准、拒绝、延期 |
| `approved` | 评审通过 | 转变更或进入 Sprint |
| `rejected` | 不做或不是有效需求 | 记录原因并关闭 |
| `deferred` | 延后 | 记录重评条件和目标时间 |
| `in_sprint` | 已纳入迭代 | 跟踪实现 |
| `implementing` | 实现中 | 关联任务、PR、测试 |
| `delivered` | 已交付，待验收 | 执行验收 |
| `done` | 已验收关闭 | 归档和沉淀 |
| `changed` | 范围发生重大变化 | 重新评审 |

状态事实源：

- `trace.md` 的 `status` 是推荐事实源。
- `requirement.md` frontmatter、登记表、外部看板必须与事实源同步。
- 每次状态变更必须在 `trace.md` 或 `change-log.md` 追加记录。
- 状态跨越生命周期分区时，必须移动整个 `REQ-NNNN-slug/` 目录：
  - `captured`、`exploring`、`draft`、`enriching`、`pending_review` → `{REQ_ROOT_DIR}/plan/`
  - `approved`、`in_sprint`、`implementing`、`delivered`、`changed` → `{REQ_ROOT_DIR}/review/`
  - `done`、`rejected`、`deferred` → `{REQ_ROOT_DIR}/archive/`

## 6. 需求类型与优先级 `[通用 + 个性化]`

需求类型为：`{REQ_TYPE_TAXONOMY}`。

推荐类型：

| type | 含义 |
| --- | --- |
| `feature` | 新功能或新能力 |
| `enhancement` | 体验、效率、可用性增强 |
| `tech` | 技术型需求、架构、治理、工程化 |
| `compliance` | 合规、安全、审计、政策要求 |
| `integration` | 第三方、客户系统或平台集成 |
| `operation` | 运维、部署、监控、数据治理 |

优先级为：`{REQ_PRIORITY_LEVELS}`。

推荐优先级：

| priority | 处理策略 |
| --- | --- |
| `P0` | 必须立即处理，通常与重大交付、安全、合规或阻断相关 |
| `P1` | 当前或下一迭代优先处理 |
| `P2` | 常规排期，进入近期规划 |
| `P3` | 待资源或批量处理 |

规则：

- 优先级必须说明业务价值、时效、风险或依赖。
- P0/P1 需求必须明确负责人、目标时间、验收方式和风险。
- 技术型需求也必须有价值、范围、验收标准和交付物。

## 7. 需求捕获与澄清 `[通用]`

`capture.md` 必须包含：

- 需求来源：用户、客户、运营、销售、研发、合规、事故复盘等。
- 背景和问题：当前痛点、触发场景、影响对象。
- 目标用户和使用场景。
- 期望结果和成功标准。
- 约束：时间、技术、合规、数据、部署、兼容、预算。
- 已知非目标、争议点、待确认问题。

澄清要求：

- 不清楚用户、目标、范围、验收标准的需求不得进入 `approved`。
- 需求探索阶段可以记录假设，但假设必须标记 `待确认`。
- AI 不得凭空补充业务结论、用户反馈、客户承诺或优先级依据。

## 8. 需求包六件套 `[通用 + 个性化]`

推荐需求包：

| 文档 | 必须回答的问题 |
| --- | --- |
| `capture.md` | 需求从哪里来，为什么出现 |
| `requirement.md` | 做什么、不做什么、约束是什么 |
| `user-stories.md` | 谁在什么场景下获得什么价值 |
| `business-flow.md` | 用户、系统、数据、权限如何流转 |
| `acceptance.md` | 怎样证明做完且做对 |
| `trace.md` | 状态、迭代、变更、测试、发布如何追踪 |

可选补充：

- `prototype/`：涉及 UI、流程、交互或客户演示时启用。
- `review.md`：所有进入实现的需求必须启用。
- `change-log.md`：需求发生范围变更、延期、拆分、合并时启用。

## 9. 原型与设计评审 `[条件启用]`

原型策略为：`{REQ_PROTOTYPE_POLICY}`。

当需求涉及 UI、交互、多端适配、流程重构、客户演示或视觉验收时启用本节。

- 原型应放在 `prototype/` 下，并按端类型拆分，例如 `web/`、`admin/`、`wechat-miniapp/`、`mobile/`、`desktop/`。
- 原型必须说明目标用户、核心路径、页面状态、异常状态和验收重点。
- 有 Golden Reference、截图、HTML 原型或设计稿时，必须在 `trace.md` 中记录来源。
- UI 需求必须与 `rules/ui-design.md`、`rules/compatibility.md`、`rules/testing.md` 保持一致。

## 10. 验收标准 `[通用 + 个性化]`

验收策略为：`{REQ_ACCEPTANCE_POLICY}`。

`acceptance.md` 必须包含：

- 功能验收：核心能力、边界条件、异常路径。
- 权限验收：角色、租户、资源范围、不可见数据。
- 数据验收：字段、状态、迁移、导入导出、审计。
- 接口验收：请求、响应、错误码、兼容性。
- UI 验收：布局、交互、loading、empty、error、响应式。
- 测试验收：单元、集成、E2E、人工验证或截图验证。
- 发布验收：配置、部署、回滚、监控、文档。

推荐使用 Given/When/Then：

```text
Given 前置条件
When 用户或系统执行动作
Then 应得到明确可验证结果
```

规则：

- 验收标准必须可测试、可观察、可判定。
- 不得使用“体验良好”“尽量完善”“支持常见场景”等不可验收表述。
- 验收标准变更必须同步测试和 trace。

## 11. Readiness 门禁 `[通用 + 个性化]`

Readiness 规则为：`{REQ_READINESS_POLICY}`。

推荐分级：

| 级别 | 条件 |
| --- | --- |
| `Ready` | `requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md` 齐全且无阻塞问题 |
| `Partially Ready` | 主体齐全，缺原型、设计细节或非阻塞项 |
| `Not Ready` | 缺 `requirement.md`、`acceptance.md`、核心范围或关键决策 |

规则：

- 进入 `approved` 前必须达到 `Ready`，或明确记录可接受的 `Partially Ready` 风险。
- 进入实现前必须明确范围、验收标准、接口/数据影响、测试策略。
- `Not Ready` 不得转 OpenSpec change 或进入 Sprint。

## 12. 评审门禁 `[通用 + 个性化]`

需求评审策略为：`{REQ_REVIEW_POLICY}`。

进入 `approved` 前必须检查：

- 需求是否真实存在，是否与产品目标一致。
- 用户、场景、目标、范围、非目标是否清楚。
- 验收标准是否可测试。
- 是否有 UI、接口、数据库、安全、兼容、部署、数据迁移影响。
- 是否需要拆分为多个需求或多个 OpenSpec change。
- 是否存在依赖、风险、未决问题和资源约束。
- 是否需要原型、技术设计、方案评审或客户确认。

评审结论：

| 结论 | 要求 |
| --- | --- |
| `approved` | 可进入研发变更或迭代 |
| `rejected` | 写明不做原因 |
| `deferred` | 写明延期原因、重评条件、目标时间 |
| `needs_changes` | 写明需要补充的材料 |

## 13. 命令族与阶段 `[通用]`

需求命令族默认由 `.cursor`、`.claude`、`.codex`、`.kiro`、`.opencode` 同步支持，命令语义不得因工具不同而改变。

推荐命令阶段：

| 命令 | 阶段 | 输入 | 产出 | 是否生成文档 | 是否生成代码 |
| --- | --- | --- | --- | --- | --- |
| `/req-capture` | 需求记录与必要拆分 | 一个或多个需求描述 | 一个或多个 `capture.md`、`trace.md` | 是 | 否 |
| `/req-explore` | 需求探索 | `REQ-ID` | 分析结论 | 默认否 | 否 |
| `/req-generate` | PRD 生成 | `REQ-ID` | `requirement.md` | 是 | 否 |
| `/req-complete` | 需求完善 | `REQ-ID` | 六件套补齐 | 是 | 否 |
| `/req-review` | 需求评审 | `REQ-ID` | `review.md`、状态变更 | 是 | 否 |
| `/req-opsx` | 转 OpenSpec | `REQ-ID` | OpenSpec Change | 是 | 否 |

规则：

- 默认命令不得直接生成业务代码，除非后续进入 `/opsx-apply` 或 `/sprint-apply`。
- 旧命令、迁移命令或团队别名必须写清楚当前有效入口。

## 14. OpenSpec 与迭代流转 `[条件启用]`

需求进入迭代规则为：`{REQ_SPRINT_POLICY}`。

需求转变更规则为：`{REQ_TO_CHANGE_POLICY}`。

当项目启用 OpenSpec、Sprint、外部看板或研发任务系统时启用本节。

通用要求：

- 只有 `approved` 或 `in_sprint` 的需求可以进入 Sprint 或正式实现。
- 只有完成 `/req-review` 且结论为 `approved` 的需求可以执行 `/req-opsx` 转 OpenSpec change，除非团队明确允许技术探索型 Spike。
- 未完成评审或评审未通过的需求（如 `captured`、`draft`、`enriching`、`pending_review`、`rejected`、`deferred`）MUST 停止在评审前置步骤：不得执行 `/req-opsx`，不得被 `/sprint-propose` 写入 Sprint 规划文件，且不得被 `/sprint-apply`、`/opsx-apply` 或等价开发流程实现。
- 发现未评审需求被用户要求纳入 Sprint 时，只能在命令输出中列为 Blocked/Deferred，并提示 `/req-review` 或 `/req-complete`；不得写入 `iterations/change/<sprint-id>/sprint.yaml`、`sprint.md`、`release-note.md` 或 `acceptance-report.md`。
- OpenSpec change 必须能追踪回 REQ ID。
- Sprint 任务、PR、测试、发布说明必须能追踪回 REQ ID。
- 需求拆分为多个 change 时，`trace.md` 必须列出全部关联。

推荐链路：

```text
Requirement
  -> User Stories
  -> Business Flow
  -> Acceptance
  -> OpenSpec Change / Task
  -> Implementation
  -> Test
  -> Release
  -> Archive
```

## 15. trace.md 最小字段 `[通用 + 个性化]`

trace 策略为：`{REQ_TRACE_POLICY}`。

推荐最小字段：

```yaml
requirement_id: REQ-NNNN-slug
status: captured
type: feature
priority: P1
owner: 待确认
requester: 待确认
lifecycle:
  captured: null
  generated: null
  completed: null
  reviewed: null
  approved: null
  in_sprint: null
  delivered: null
  done: null
iteration: null
openspec_changes: []
related_requirements: []
related_bugs: []
related_prs: []
test_artifacts: []
release_notes: []
```

`trace.md` 必须包含「关联缺陷」章节，用于记录需求与 BUG 的索引级关系：

```markdown
## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0003-brand-image-display-layout-shift | high | done | fix-brand-image-display-layout-shift | 品牌 Logo 展示与提示布局修复 |
```

规则：

- 本节只记录 BUG ID、严重等级、状态、关联 Change 和一句话说明，不重复 `bug.md`、`root-cause.md`、`regression.md`、日志、截图或验收全文。
- 详细缺陷内容必须以 `{BUG_ROOT_DIR}/{BUG_ID}/` 为事实源。
- 当 BUG 状态、严重等级、关联 Change 或修复结论变化时，必须同步更新相关需求的 `trace.md`。
- 一个需求关联多个 BUG 时，每个 BUG 一行；一个 BUG 影响多个需求时，每个相关需求的 `trace.md` 都应保留索引级关联。

每次命令或人工更新结束后，必须追加：

```markdown
## 变更记录

- YYYY-MM-DD hh:mm:ss：变更内容、原因、操作者、影响范围。
```

## 16. 需求变更控制 `[通用 + 个性化]`

需求变更控制策略为：`{REQ_CHANGE_CONTROL_POLICY}`。

必须记录的变更：

- 范围扩大、范围缩小、拆分、合并。
- 优先级变化、目标迭代变化、负责人变化。
- 验收标准变化、非目标变化、技术约束变化。
- UI 原型、接口契约、数据模型、权限规则变化。
- 从需求转 Bug、从 Bug 转需求、从功能转技术任务。

规则：

- `approved` 后发生范围变化，必须重新评估 Readiness 和评审结论。
- 已进入 Sprint 的需求发生重大变化，必须同步 Sprint、OpenSpec、测试和发布计划。
- 变更不得只改实现代码，必须同步需求包和 trace。

## 17. 客户需求、合规需求与外部看板 `[条件启用]`

当项目存在客户工单、销售承诺、合规审计、外部任务系统或跨团队需求时启用本节。

- 外部需求必须记录来源系统、外部 ID、联系人、承诺时间和验收方。
- 客户承诺不得由 AI 推断，必须有明确来源。
- 合规需求必须记录法规、审计、数据、安全、留痕和验收依据。
- 外部看板状态与本地 trace 必须保持同步，冲突时以项目约定事实源为准。
- 外部附件必须脱敏后进入仓库。

## 18. AI 处理需求规则 `[通用]`

AI 处理需求时必须：

- 先读取需求目录、登记表、相关规则、相关 OpenSpec、相关代码和相关测试。
- 不得凭空补充用户反馈、客户承诺、业务价值、优先级依据或评审结论。
- 不得将缺陷、技术债、探索任务伪装为已批准需求。
- 不得跳过 `acceptance.md` 或用不可验证描述替代验收标准。
- 不得在未确认的情况下扩大范围、修改目标用户、改变优先级。
- 转实现前必须明确接口、数据、安全、兼容、UI、测试和发布影响。
- 完成变更后必须更新 `trace.md`、测试、文档和相关规则。
- 信息不足时标记 `待确认`，并列出需要用户或团队补充的材料。

## 19. 与其他规则的同步关系 `[通用]`

| 变更类型 | 必须同步 |
| --- | --- |
| 需求转 OpenSpec | `openspec/changes/*`、`trace.md`、迭代任务 |
| API 新增或变更 | `rules/api.md`、OpenAPI、接口测试 |
| 数据库或数据模型 | `rules/database.md`、迁移、数据管理文档 |
| 权限、安全、隐私 | `rules/security.md`、安全测试 |
| UI、原型、多端体验 | `rules/ui-design.md`、`rules/compatibility.md` |
| 上传、媒体、对象存储 | `rules/media.md`、`rules/object-storage.md` |
| 测试和验收 | `rules/testing.md`、测试计划、验收报告 |
| 发布和回滚 | `rules/release.md`、发布说明、回滚策略 |
| 文档治理 | `rules/document-governance.md`、目录和元数据 |
| 缺陷转需求或需求关联缺陷 | `rules/bug-management.md`、需求 `trace.md` 的「关联缺陷」索引、关联 Bug trace |

## 20. 初始化生成建议 `[通用]`

用于工程初始化生成 `requirement-management.md` 时，建议按以下步骤处理：

1. 根据用户输入替换 `{PRODUCT_NAME}`、`{REQ_ROOT_DIR}`、`{REQ_ID_PATTERN}`、`{REQ_STATUS_MACHINE}`、优先级、评审门禁和 Readiness 策略。
2. 保留所有 `[通用]` 章节，并将模板语气改为项目确定性约束。
3. 对 `[个性化]` 章节填入项目真实目录、看板、迭代流转、原型策略和验收策略；默认需求命令族保持 `/req-*`，信息不足时标记 `待确认`。
4. 对 `[条件启用]` 章节按项目能力裁剪；未启用 OpenSpec、原型、外部看板、合规、客户工单等能力时删除或标记“不适用”。
5. 不得保留其他项目的命令名、需求编号、业务模块、客户名称、原型路径或看板名称。
6. 与 `document-governance.md`、`directory-structure.md`、`testing.md`、`bug-management.md`、`release.md` 保持一致。

## 21. 完成任务后检查清单 `[通用]`

- 是否已在 `{REQ_ROOT_DIR}` 创建或更新对应需求目录。
- 是否记录需求来源、目标用户、背景、范围、非目标和约束。
- 是否补充用户故事、业务流程、验收标准和 trace。
- 是否明确状态、优先级、负责人、目标迭代和评审结论。
- 是否需求状态流转符合 `{REQ_STATUS_MACHINE}`。
- 是否达到 `{REQ_READINESS_POLICY}` 后才进入实现或转变更。
- 是否同步 OpenSpec、Sprint、测试、发布和相关规则文档。
- 是否没有提交真实密钥、客户隐私、生产数据或未脱敏附件。
