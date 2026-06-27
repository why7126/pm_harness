---
purpose: 缺陷管理与修复闭环规范
content: 规范 Bug 捕获、分级、复现、根因分析、状态机、目录结构、评审门禁、OpenSpec 转换、回归测试、知识沉淀和 AI 处理边界
source: Harness bug-management.md 抽象模板，基于项目缺陷治理规则沉淀
update_method: 项目初始化时按用户输入生成；缺陷命令族、状态机、目录结构、迭代流程、评审门禁或测试策略变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 09:02:51
note: 适用于 {PRODUCT_NAME} 项目；AI 处理缺陷必须保留证据链、根因链、修复链和回归验证链
template_scope: 可作为工程初始化的 bug-management.md 模块
---
# 缺陷管理与修复闭环规范

## 0. 规则定位 `[通用]`

本文件定义 `{PRODUCT_NAME}` 的缺陷生命周期、目录结构、状态机、严重等级、复现证据、根因分析、修复门禁、回归验证和知识沉淀规则。所有线上问题、测试缺陷、用户反馈、回归失败、安全问题、兼容问题和数据问题，均应按本规范记录和流转。

AI 在执行以下任务前必须先阅读本文件：

- 记录、分析、补全、评审、修复或关闭 Bug。
- 将 Bug 转换为 OpenSpec change、迭代任务、修复 PR 或发布说明。
- 修改 Bug 命令族、缺陷目录、状态机、严重等级、评审门禁。
- 根据日志、截图、复现步骤、用户反馈生成根因分析或回归测试。
- 判断缺陷是否进入 Sprint、是否可延期、是否需要知识库沉淀。

## 1. 文档模块分类 `[通用]`

本模板将缺陷规则拆分为三类，工程初始化时应根据用户输入生成最终文档：

- `[通用]`：所有项目默认保留的缺陷治理基线。
- `[个性化]`：必须根据团队流程、命令族、目录结构、严重等级和迭代方式替换的内容。
- `[条件启用]`：仅在项目启用对应能力时保留，例如 OpenSpec、值班响应、线上事故、客户工单、安全漏洞、移动端崩溃、私有化客户缺陷等。

推荐初始化参数：

| 参数 | 用途 |
| --- | --- |
| `{PRODUCT_NAME}` | 项目或产品名称 |
| `{PRODUCT_CODE}` | 项目标识、包名前缀或服务标识 |
| `{BUG_ROOT_DIR}` | 缺陷根目录，例如 `issues/bugs/` |
| `{BUG_ID_PATTERN}` | 缺陷编号规则，例如 `BUG-NNNN-slug` |
| `{BUG_REGISTRY_FILE}` | 缺陷登记文件，例如 `_registry.yaml` |
| 默认缺陷命令族 | `/bug-capture`、`/bug-explore`、`/bug-generate`、`/bug-complete`、`/bug-review`、`/bug-opsx` |
| `{BUG_STATUS_MACHINE}` | 缺陷状态机 |
| `{BUG_SEVERITY_LEVELS}` | 严重等级定义 |
| `{BUG_PRIORITY_LEVELS}` | 优先级定义 |
| `{BUG_REVIEW_POLICY}` | 缺陷评审门禁 |
| `{BUG_SPRINT_POLICY}` | 缺陷进入迭代规则 |
| `{BUG_TO_CHANGE_POLICY}` | Bug 转 OpenSpec change 或修复任务的规则 |
| `{BUG_EVIDENCE_POLICY}` | 日志、截图、录屏、链路追踪等证据规则 |
| `{BUG_TEST_POLICY}` | 回归测试和验收测试规则 |
| `{BUG_KB_POLICY}` | 知识库沉淀规则 |
| `{BUG_SLA_POLICY}` | 响应时效或修复时效规则 |

## 2. 缺陷治理总原则 `[通用]`

- 先记录，再修复：除阻断级紧急修复外，所有 Bug 必须先有可追踪记录。
- 先复现，再归因：根因分析不得只写猜测，必须说明复现路径、证据和影响范围。
- 先定级，再排期：严重等级和优先级决定响应策略、评审门禁和迭代优先级。
- 先验收，再关闭：Bug 关闭必须有修复说明、验证结果和回归测试。
- 证据链完整：截图、日志、环境、版本、数据样例、请求响应、错误码必须尽量可追溯。
- 不混淆需求和缺陷：新需求、体验优化、技术债和误报不得伪装为 Bug。
- 不绕过测试：Bug 修复必须补充或更新回归测试；无法自动化时必须记录人工验证。

## 3. 缺陷目录结构 `[通用 + 个性化]`

缺陷根目录为：`{BUG_ROOT_DIR}`。

缺陷编号规则为：`{BUG_ID_PATTERN}`。

缺陷登记文件为：`{BUG_REGISTRY_FILE}`。

推荐目录结构：

```text
{BUG_ROOT_DIR}
├── {BUG_REGISTRY_FILE}
└── {BUG_ID_PATTERN}/
    ├── capture.md
    ├── bug.md
    ├── root-cause.md
    ├── workaround.md
    ├── acceptance.md
    ├── trace.md
    ├── review.md
    ├── regression.md
    ├── logs/
    ├── screenshots/
    └── attachments/
```

文件职责：

| 文件 | 职责 |
| --- | --- |
| `capture.md` | 原始反馈、现象、发现人、发现时间、环境、版本 |
| `bug.md` | 结构化缺陷描述、严重等级、优先级、影响范围 |
| `root-cause.md` | 根因分析、触发条件、直接原因、深层原因 |
| `workaround.md` | 临时规避方案、风险、适用范围、失效条件 |
| `acceptance.md` | 修复验收标准、回归验证项、关闭条件 |
| `trace.md` | 与需求、OpenSpec、迭代、PR、测试、发布的追踪关系 |
| `review.md` | 缺陷评审结论、状态变更、责任人、下一步 |
| `regression.md` | 回归测试记录、自动化测试、人工验证、残余风险 |
| `logs/` | 脱敏日志、错误栈、请求响应样例、链路追踪 |
| `screenshots/` | 截图、录屏、对比图、视觉缺陷证据 |
| `attachments/` | 其他脱敏附件 |

规则：

- 缺陷记录必须放在 `{BUG_ROOT_DIR}`，不得散落到 `docs/bugs/`、聊天记录、临时文档或代码注释中。
- 缺陷物理阶段目录、迁移时机、`lifecycle_stage` 与 registry 同步规则以 `rules/issues-lifecycle.md` 为准。
- 缺陷目录必须按生命周期放入 `{BUG_ROOT_DIR}/plan/`、`{BUG_ROOT_DIR}/review/`、`{BUG_ROOT_DIR}/archive/` 三个分区。
- 新捕获、复现分析中、草稿、补齐中或待评审的 BUG 必须位于 `plan/`；评审通过后必须移动到 `review/`；验收关闭、拒绝、不修或延期关闭后必须移动到 `archive/`。
- 每个 Bug 目录必须可独立理解问题、原因、修复、验证和状态。
- 附件必须脱敏，不得提交真实密钥、Token、客户隐私、生产数据原文。
- 关闭 Bug 前，`bug.md`、`root-cause.md`、`acceptance.md`、`trace.md`、`regression.md` 必须完整。
- `/bug-capture` 接收日志、反馈合集或长文本时，MUST 先评估是否包含多个独立缺陷；若存在多个独立现象、模块/页面/接口、触发路径、期望行为、严重等级，或可独立修复和验证，必须拆分为多个 BUG 分别登记。
- 不应把多个可独立定位、独立修复或独立回归的缺陷塞进同一个 `capture.md`；同一根因、同一操作路径或同一修复点的多种表现可以保留在同一个 BUG 中并记录影响范围。

## 4. 缺陷登记表 `[条件启用]`

当项目使用集中登记文件、看板同步或自动化统计时启用本节。

`{BUG_REGISTRY_FILE}` 推荐记录：

```yaml
bugs:
  - id: BUG-0001-example
    title: 示例缺陷标题
    status: captured
    severity: medium
    priority: P2
    owner: 待确认
    reporter: 待确认
    found_at: 待确认
    target_release: 待确认
    related_change: 待确认
```

要求：

- 新增 Bug 目录时必须同步登记表。
- 状态、严重等级、负责人、目标版本变更时必须同步登记表。
- 登记表是索引，不替代 Bug 目录中的详细材料。
- 以上同步必须由 `python scripts/sync-workflow-status.py --event bug.<action> --bug <BUG-ID> ...` 执行或校验；命令不得跳过最终 Workflow Sync。

## 5. 状态机 `[通用 + 个性化]`

缺陷状态机为：`{BUG_STATUS_MACHINE}`。

推荐状态：

| status | 含义 | 下一步 |
| --- | --- | --- |
| `captured` | 已记录原始反馈 | 补充复现、环境、证据 |
| `exploring` | 复现和影响分析中 | 生成结构化缺陷 |
| `draft` | 已有 `bug.md`，材料不完整 | 补根因、验收、追踪 |
| `enriching` | 缺陷包补齐中 | 进入评审 |
| `pending_review` | 待评审 | 批准、拒绝、延期或不修 |
| `approved` | 确认为缺陷且同意修复 | 转修复变更或进入迭代 |
| `rejected` | 非缺陷、误报或无法复现 | 记录原因并关闭 |
| `wont_fix` | 确认为问题但决定不修 | 记录业务/技术原因 |
| `deferred` | 延后修复 | 记录触发条件和重评时间 |
| `in_sprint` | 已纳入迭代或修复计划 | 跟踪实现和验证 |
| `fixing` | 修复中 | 关联 PR、测试和变更 |
| `fixed` | 已修复，待验收 | 执行回归测试 |
| `done` | 已验收关闭 | 必要时沉淀知识库 |
| `reopened` | 验收失败或复现 | 重新分析根因 |

状态流转规则：

- 只有 `approved`、`in_sprint`、`fixing` 状态的 Bug 可以进入正式修复实施。
- `rejected`、`wont_fix`、`deferred` 必须有评审理由。
- `done` 必须有关联修复、验收结果和回归记录。
- 重新复现的问题不得直接覆盖旧记录，应使用 `reopened` 或创建关联 Bug。
- 状态跨越生命周期分区时，必须移动整个 `BUG-NNNN-slug/` 目录：
  - `captured`、`exploring`、`draft`、`enriching`、`pending_review` → `{BUG_ROOT_DIR}/plan/`
  - `approved`、`in_sprint`、`fixing`、`fixed`、`reopened` → `{BUG_ROOT_DIR}/review/`
  - `done`、`rejected`、`wont_fix`、`deferred` → `{BUG_ROOT_DIR}/archive/`

## 6. 严重等级与优先级 `[通用 + 个性化]`

严重等级为：`{BUG_SEVERITY_LEVELS}`。

推荐严重等级：

| severity | 判定标准 |
| --- | --- |
| `blocker` | 系统不可用、核心链路阻断、严重数据损坏、安全高危 |
| `critical` | 核心功能大面积不可用、客户交付受阻、明显数据错误 |
| `high` | 重要功能异常、有规避方案但影响效率或体验 |
| `medium` | 普通功能缺陷、局部体验问题、影响有限 |
| `low` | 文案、样式、轻微兼容、低频边界问题 |

优先级为：`{BUG_PRIORITY_LEVELS}`。

推荐优先级：

| priority | 处理策略 |
| --- | --- |
| `P0` | 立即响应，优先于功能需求，必要时进入热修 |
| `P1` | 当前迭代优先处理，阻塞发布时必须修复 |
| `P2` | 排入近期迭代或常规修复 |
| `P3` | 可延期，批量处理或随相关模块优化 |

规则：

- 严重等级描述影响程度，优先级描述处理顺序，两者不得混用。
- P0/P1 Bug 必须明确负责人、响应时间、验证方式和发布策略。
- 安全、数据损坏、权限越权、支付计费、客户交付阻断类问题应提高等级。

## 7. 捕获与复现 `[通用]`

`capture.md` 和 `bug.md` 必须包含：

- 缺陷标题和一句话摘要。
- 发现人、发现时间、来源渠道。
- 环境、版本、分支、设备、浏览器、数据库、部署模式。
- 前置条件、复现步骤、实际结果、期望结果。
- 影响范围、影响用户、影响数据、业务影响。
- 截图、日志、请求响应、错误码、链路追踪或录屏。
- 是否稳定复现、偶现、仅特定环境复现或暂无法复现。

复现规则：

- 复现步骤必须足够具体，其他成员可以按步骤重现。
- 偶现问题必须记录频率、触发条件、可疑时间窗口和相关日志。
- 无法复现的问题不得直接关闭，应先进入 `exploring` 或标记缺失信息。

## 8. 根因分析 `[通用]`

`root-cause.md` 必须说明：

- 直接原因：哪段逻辑、配置、数据、依赖或环境导致问题。
- 触发条件：为什么在这个场景下出现。
- 深层原因：测试缺口、设计缺口、监控缺口、流程缺口或兼容性缺口。
- 影响范围：是否影响同类接口、同类页面、同类数据、历史版本或客户环境。
- 修复策略：短期修复、长期改进和风险。

禁止：

- 只写“已修复”“代码问题”“配置问题”。
- 无证据地归因给外部服务、用户操作或环境。
- 只修表象，不解释为什么测试、监控或流程未提前发现。

## 9. 临时规避方案 `[条件启用]`

当 Bug 影响线上、交付、演示、客户使用或核心流程时启用本节。

`workaround.md` 必须说明：

- 临时规避步骤。
- 适用环境和适用用户。
- 风险、副作用和数据影响。
- 失效条件和撤销方式。
- 最终修复计划。

规避方案不得替代正式修复；若决定不修，必须进入 `wont_fix` 并记录评审结论。

## 10. 评审门禁 `[通用 + 个性化]`

缺陷评审策略为：`{BUG_REVIEW_POLICY}`。

进入 `approved` 前必须检查：

- 是否为真实缺陷，而不是新需求、误报、配置错误或使用问题。
- 是否有复现步骤或足够证据。
- 严重等级、优先级、影响范围是否合理。
- 根因是否可验证，修复方向是否明确。
- 验收标准和回归测试是否可执行。
- 是否需要 OpenSpec change、迭代任务、热修或发布说明。

评审结论：

| 结论 | 要求 |
| --- | --- |
| `approved` | 可进入修复流程 |
| `rejected` | 写明非缺陷或误报原因 |
| `wont_fix` | 写明不修原因和风险接受方 |
| `deferred` | 写明延期原因、重评条件、目标版本 |

## 11. 迭代与修复流转 `[通用 + 个性化]`

缺陷进入迭代规则为：`{BUG_SPRINT_POLICY}`。

Bug 转修复变更规则为：`{BUG_TO_CHANGE_POLICY}`。

通用要求：

- P0 Bug 优先于普通功能需求。
- P1 Bug 若阻塞发布，必须在发布前修复或获得明确风险接受。
- 进入 Sprint 的 Bug 必须至少达到 `approved` 或 `in_sprint`。
- 只有完成 `/bug-review` 且结论为 `approved` 的 Bug 可以执行 `/bug-opsx` 转 OpenSpec fix change；未完成评审或评审未通过的 Bug 不得进入 Sprint 规划、不得执行 `/sprint-apply`、`/opsx-apply` 或等价开发流程。
- 发现未评审 Bug 被用户要求纳入 Sprint 时，只能在命令输出中列为 Blocked/Deferred，并提示 `/bug-review` 或 `/bug-complete`；不得写入 `iterations/<sprint-id>/sprint.yaml`、`sprint.md`、`release-note.md` 或 `acceptance-report.md`。
- 转 OpenSpec change、修复任务或 PR 前，必须完成 Bug 完整性检查。
- 修复任务必须能追踪回 Bug ID。
- Bug 关联一个或多个需求时，必须在对应需求 `trace.md` 的「关联缺陷」章节维护索引级关联；不得把 Bug 全文复制进需求 trace。

推荐追踪链路：

```text
Bug
  -> Root Cause
  -> Impact Analysis
  -> Fix Change / Task / PR
  -> Regression Test
  -> Release Note
  -> Knowledge Base
```

## 12. 命令族与阶段 `[通用]`

缺陷命令族默认由 `.cursor`、`.claude`、`.codex`、`.kiro`、`.opencode` 同步支持，命令语义不得因工具不同而改变。

推荐命令阶段：

| 命令 | 阶段 | 输入 | 产出 | 是否生成文档 | 是否生成代码 |
| --- | --- | --- | --- | --- | --- |
| `/bug-capture` | 缺陷记录与必要拆分 | 一个或多个缺陷描述 | 一个或多个 `capture.md`、`trace.md` | 是 | 否 |
| `/bug-explore` | 缺陷分析 | `BUG-ID` | 分析结论 | 默认否 | 否 |
| `/bug-generate` | 缺陷生成 | `BUG-ID` | `bug.md` | 是 | 否 |
| `/bug-complete` | 缺陷完善 | `BUG-ID` | 根因分析包 | 是 | 否 |
| `/bug-review` | 缺陷评审 | `BUG-ID` | `review.md`、状态变更 | 是 | 否 |
| `/bug-opsx` | 转 OpenSpec | `BUG-ID` | `fix-*` Change | 是 | 否 |

规则：

- 默认命令不得直接生成业务代码，除非后续进入 `/opsx-apply` 或 `/sprint-apply`。
- 命令文档必须读取本文件、`rules/testing.md`、`rules/security.md`、相关 Bug 目录和项目约定上下文。

## 13. 验收与回归测试 `[通用 + 个性化]`

回归测试策略为：`{BUG_TEST_POLICY}`。

`acceptance.md` 必须包含：

- 修复后用户可观察行为。
- 不再复现的具体步骤。
- 权限、安全、数据、兼容、性能影响。
- 自动化测试和人工验证范围。
- 发布后观察项。

`regression.md` 必须包含：

- 已运行的测试命令。
- 新增或更新的测试用例。
- 人工验证步骤和结果。
- 未覆盖风险和原因。
- 验证人、验证时间、验证环境。

规则：

- Bug 修复必须补充失败复现测试或回归测试。
- 无法自动化的视觉、交互、客户环境问题必须记录人工验证证据。
- P0/P1 Bug 修复必须评估是否补充监控、告警或知识库。

## 14. 安全、数据与隐私缺陷 `[条件启用]`

当 Bug 涉及认证、权限、数据泄露、密钥、上传、对象存储、支付、计费或隐私数据时启用本节。

- 安全缺陷不得在公开文档中暴露攻击细节、真实 Token、生产数据、客户隐私。
- 权限越权、敏感信息泄露、上传绕过、对象存储公开访问应提高严重等级。
- 安全 Bug 修复必须补充安全回归测试。
- 数据损坏或数据错乱必须记录影响数据范围、修复脚本、备份恢复和验证方式。
- 必须与 `rules/security.md`、`rules/data-management.md`、`rules/database.md` 保持一致。

## 15. 线上事故与 SLA `[条件启用]`

响应时效规则为：`{BUG_SLA_POLICY}`。

当项目有线上服务、客户交付、SLA、值班或事故响应要求时启用本节。

- P0/P1 线上 Bug 必须记录发现时间、响应时间、缓解时间、修复时间。
- 线上事故应区分止血、修复、复盘和长期预防。
- 热修必须记录发布版本、回滚方案和验证结果。
- 事故复盘可沉淀到 `docs/knowledge-base/incidents/` 或项目约定目录。

## 16. 知识沉淀 `[通用 + 个性化]`

知识库沉淀规则为：`{BUG_KB_POLICY}`。

修复后若具备复用价值，应沉淀：

- 典型根因和排查路径。
- 日志特征、错误码、监控指标。
- 规避方案和最终修复方案。
- 测试补充和流程改进。
- 对同类模块的预防建议。

适合沉淀的 Bug：

- P0/P1 或客户可见问题。
- 安全、数据、权限、上传、对象存储、数据库迁移、兼容性问题。
- 排查成本高、复现困难、跨模块协作的问题。
- 曾经重复出现的问题。

## 17. AI 处理 Bug 规则 `[通用]`

AI 处理 Bug 时必须：

- 先读取 Bug 目录、登记表、相关规则、相关代码和相关测试。
- 不得凭空补全复现步骤、日志、根因、评审结论或测试结果。
- 不得把新需求伪装为 Bug 修复。
- 不得为了关闭 Bug 删除测试、跳过验证、降低安全规则或隐藏错误。
- 不得提交真实日志、密钥、客户隐私、生产数据原文。
- 修复代码前必须明确影响范围和回归测试。
- 修复完成后必须更新 `trace.md`、`regression.md`、测试和相关文档。
- 信息不足时标记 `待确认`，并列出需要用户或团队补充的材料。

## 18. 与其他规则的同步关系 `[通用]`

| 变更类型 | 必须同步 |
| --- | --- |
| Bug 转需求或变更 | OpenSpec change、Bug `trace.md`、需求 `trace.md` 的「关联缺陷」、迭代任务 |
| API 缺陷 | `rules/api.md`、接口测试、错误码文档 |
| 数据库缺陷 | `rules/database.md`、迁移测试、数据修复记录 |
| 安全缺陷 | `rules/security.md`、安全回归测试 |
| 上传、媒体、对象存储缺陷 | `rules/media.md`、`rules/object-storage.md`、上传下载测试 |
| 环境、部署、端口缺陷 | `rules/environment.md`、`rules/port-management.md`、`rules/release.md` |
| 兼容性缺陷 | `rules/compatibility.md`、兼容性测试矩阵 |
| UI 缺陷 | `rules/ui-design.md`、截图或浏览器验证 |
| 测试缺口 | `rules/testing.md`、回归测试和覆盖率记录 |
| 可复用排查经验 | `docs/knowledge-base/` 或项目约定知识库 |

## 19. 初始化生成建议 `[通用]`

用于工程初始化生成 `bug-management.md` 时，建议按以下步骤处理：

1. 根据用户输入替换 `{PRODUCT_NAME}`、`{BUG_ROOT_DIR}`、`{BUG_ID_PATTERN}`、`{BUG_STATUS_MACHINE}`、严重等级、优先级和门禁策略。
2. 保留所有 `[通用]` 章节，并将模板语气改为项目确定性约束。
3. 对 `[个性化]` 章节填入项目真实目录、看板、迭代流转和修复策略；默认缺陷命令族保持 `/bug-*`，信息不足时标记 `待确认`。
4. 对 `[条件启用]` 章节按项目能力裁剪；未启用 OpenSpec、SLA、事故、客户工单、移动端崩溃等能力时删除或标记“不适用”。
5. 不得保留其他项目的命令名、缺陷编号、业务模块、客户名称、日志路径或截图路径。
6. 与 `directory-structure.md`、`document-governance.md`、`testing.md`、`security.md`、`release.md` 保持一致。

## 20. 完成任务后检查清单 `[通用]`

- 是否已在 `{BUG_ROOT_DIR}` 创建或更新对应 Bug 目录。
- 是否记录复现步骤、环境、版本、证据和影响范围。
- 是否明确严重等级、优先级、负责人和状态。
- 是否补充根因分析、验收标准、回归测试和追踪关系。
- 是否没有提交真实密钥、生产数据、客户隐私或未脱敏日志。
- 是否 Bug 状态流转符合 `{BUG_STATUS_MACHINE}`。
- 是否修复已关联测试、变更、PR、迭代或发布说明。
- 是否有复用价值的问题已沉淀到知识库。
