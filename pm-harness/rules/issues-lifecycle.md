---
purpose: Issues 生命周期阶段目录规范
content: 规范需求与 BUG 在 plan、review、archive 三个物理阶段目录中的准入条件、迁移时机、trace 字段、registry 位置、兼容读取和自动化检查
source: Harness issues-lifecycle.md 抽象模板，基于项目 issues 三阶段目录治理规则沉淀
update_method: 项目初始化时按用户输入生成；issues 目录结构、需求/BUG 状态机、评审门禁、归档流程或自动化脚本变化时更新
created_at: 2026-06-27 22:24:39
updated_at: 2026-06-27 22:24:39
note: 适用于 {PRODUCT_NAME} 项目；REQ 与 BUG 共用；_registry.yaml 位于 issues/requirements 和 issues/bugs 根目录
template_scope: 可作为工程初始化的 issues-lifecycle.md 独立模块
---

# Issues 生命周期阶段目录规范

## 0. 规则定位 `[通用]`

本文件定义 `{PRODUCT_NAME}` 中 `issues/requirements/` 与 `issues/bugs/` 的共享物理生命周期规则。它不替代 `rules/requirement-management.md` 或 `rules/bug-management.md` 的业务状态机，而是规定需求和 BUG 在文件系统中的阶段位置、迁移时机、路径解析、registry 位置和自动化检查。

AI 在执行以下任务前必须读取本文件：

- 新建、拆分、迁移、归档、拒绝、延期或关闭需求/BUG。
- 执行 `/capture`、`/req-capture`、`/bug-capture`、`/req-review`、`/bug-review`、`/req-opsx`、`/bug-opsx`、`/sprint-propose`、`/sprint-apply`、`/sprint-archive`。
- 修改 `issues/` 目录结构、`_registry.yaml`、`trace.md`、工作流同步脚本或初始化模板。
- 判断某个 REQ/BUG 是否可以进入 Sprint、OpenSpec change、开发实现或归档。

## 1. 文档模块分类 `[通用]`

本模板将 Issues 生命周期规则拆分为三类，工程初始化时应根据用户输入生成最终文档：

- `[通用]`：所有 Harness 项目默认保留的 issues 三阶段目录治理规则。
- `[个性化]`：必须根据团队目录、命令族、状态机、评审门禁、归档策略和外部系统替换的内容。
- `[条件启用]`：仅在项目启用对应能力时保留，例如 OpenSpec、Sprint、外部看板、遗留扁平目录兼容、自动化同步脚本等。

推荐初始化参数：

| 参数 | 用途 |
| --- | --- |
| `{PRODUCT_NAME}` | 项目或产品名称 |
| `{REQ_ROOT_DIR}` | 需求根目录，例如 `issues/requirements/` |
| `{BUG_ROOT_DIR}` | BUG 根目录，例如 `issues/bugs/` |
| `{REQ_ID_PATTERN}` | 需求编号规则，例如 `REQ-NNNN-slug` |
| `{BUG_ID_PATTERN}` | BUG 编号规则，例如 `BUG-NNNN-slug` |
| `{REQ_REGISTRY_FILE}` | 需求登记文件，例如 `_registry.yaml` |
| `{BUG_REGISTRY_FILE}` | BUG 登记文件，例如 `_registry.yaml` |
| `{ISSUE_LIFECYCLE_STAGES}` | 阶段目录集合，默认 `plan`、`review`、`archive` |
| `{REQ_STATUS_TO_STAGE}` | 需求状态到阶段目录的映射 |
| `{BUG_STATUS_TO_STAGE}` | BUG 状态到阶段目录的映射 |
| `{ISSUE_REVIEW_POLICY}` | 需求/BUG 评审门禁 |
| `{ISSUE_ARCHIVE_POLICY}` | 关闭、归档和延期策略 |
| `{ISSUE_PATH_COMPAT_POLICY}` | 遗留路径兼容策略 |
| `{WORKFLOW_SYNC_COMMAND}` | 工作流同步命令，例如 `python scripts/sync-workflow-status.py` |
| `{TASK_TRACKING_SYSTEM}` | 外部需求、缺陷或迭代系统 |

## 2. 总原则 `[通用]`

- 阶段目录表达物理位置，`trace.md` 的 `status` 表达逻辑状态；二者必须互相一致。
- 新建 REQ/BUG 必须先进入 `plan/`，不得直接创建在 `review/`、`archive/` 或 issues 根目录。
- 评审通过后才能进入 `review/`，未通过评审不得进入 Sprint、不得转 OpenSpec change、不得执行开发。
- 归档闭环后才能进入 `archive/`，归档必须保留完整 trace、评审结论、验收结果和关联 change。
- 每个 `REQ-*` 或 `BUG-*` 目录在任一时刻只能存在于一个阶段目录中，不得复制多份。
- `_registry.yaml` 必须保留在 `{REQ_ROOT_DIR}` 与 `{BUG_ROOT_DIR}` 根目录，不得移入阶段目录。
- 自动化脚本和命令必须用递归或解析函数定位 Issue 目录，不得硬编码旧式扁平路径。

## 3. 目录结构 `[通用 + 个性化]`

推荐结构：

```text
{REQ_ROOT_DIR}
├── {REQ_REGISTRY_FILE}
├── plan/
│   └── {REQ_ID_PATTERN}/
├── review/
│   └── {REQ_ID_PATTERN}/
└── archive/
    └── {REQ_ID_PATTERN}/

{BUG_ROOT_DIR}
├── {BUG_REGISTRY_FILE}
├── plan/
│   └── {BUG_ID_PATTERN}/
├── review/
│   └── {BUG_ID_PATTERN}/
└── archive/
    └── {BUG_ID_PATTERN}/
```

阶段目录职责：

| 阶段目录 | 通用定义 | 需求典型状态 | BUG 典型状态 |
| --- | --- | --- | --- |
| `plan/` | 规划中，评审未完成或未形成可执行结论 | `captured`、`exploring`、`draft`、`enriching`、`pending_review` | `captured`、`exploring`、`draft`、`enriching`、`pending_review` |
| `review/` | 已完成评审，尚未完成最终归档 | `approved`、`in_sprint`、`implementing`、`delivered`、`changed` | `approved`、`in_sprint`、`fixing`、`fixed`、`reopened` |
| `archive/` | 已关闭、已拒绝、已延期关闭或已归档 | `done`、`rejected`、`deferred` | `done`、`rejected`、`wont_fix`、`deferred` |

约束：

- 阶段目录内不得再嵌套 `plan/`、`review/`、`archive/`。
- 阶段目录内只能放对应类型的 `REQ-*` 或 `BUG-*` 目录，不得直接散放临时文档。
- 具体需求包和 BUG 包的文件清单分别以 `rules/requirement-management.md` 与 `rules/bug-management.md` 为准。

## 4. 阶段准入与迁移时机 `[通用 + 个性化]`

| 事件 | 常见命令 | 目录迁移 | 要求 |
| --- | --- | --- | --- |
| 新建需求/BUG | `/capture`、`/req-capture`、`/bug-capture` | 无 → `plan/` | 生成最小 `capture.md` 与 `trace.md`，更新对应 `_registry.yaml` |
| 补齐材料 | `/req-complete`、`/bug-complete` | 保持 `plan/` | 不因文档补齐自动进入 `review/` |
| 评审通过 | `/req-review --approve`、`/bug-review --approve` | `plan/` → `review/` | 写入 `review.md`，更新 `status: approved` 与 `lifecycle_stage: review` |
| 评审拒绝/延期/不修 | `/req-review --reject`、`/bug-review --reject`、`--defer`、`--wont-fix` | `plan/` → `archive/` | 必须记录原因；关闭后不得进入 Sprint 或开发 |
| 纳入迭代 | `/sprint-propose` | 保持 `review/` | 只允许 `review/` 中已 approved 的 REQ/BUG 写入 Sprint 规划 |
| 开发实现 | `/sprint-apply`、`/opsx-apply` | 保持 `review/` | 仅处理已评审且已纳入范围的条目 |
| 归档闭环 | `/opsx-archive`、`/sprint-archive` | `review/` → `archive/` | 更新验收、发布、OpenSpec archive 与 trace |
| 重新打开 BUG | `/bug-review` 或团队约定命令 | `archive/` → `review/` | 必须记录 reopened 原因、影响面和回归策略 |

迁移要求：

- 必须移动整个 `REQ-*` 或 `BUG-*` 目录，而不是复制单个文件。
- 迁移后必须同步 `_registry.yaml` 中的路径、阶段或状态字段。
- 迁移后必须更新 `trace.md` 的 `status`、`lifecycle_stage` 和变更记录。
- 迁移后应运行 `{WORKFLOW_SYNC_COMMAND}` 或项目等价同步命令。

## 5. trace.md 字段 `[通用 + 个性化]`

每个 REQ/BUG 的 `trace.md` 必须能表达逻辑状态和物理阶段。

推荐字段：

```yaml
status: captured | pending_review | approved | in_sprint | done | rejected | deferred
lifecycle_stage: plan | review | archive
current_path: issues/<type>/<stage>/<id>/
updated_at: YYYY-MM-DD hh:mm:ss
```

要求：

- `status` 与 `lifecycle_stage` 不一致时，必须优先修复不一致，不得继续开发或归档。
- `lifecycle_stage` 变更必须记录原因、命令、操作者或来源。
- `current_path` 如启用，必须在目录移动后同步更新。
- 外部看板字段如启用，必须与 `trace.md` 和 `_registry.yaml` 保持一致。

## 6. registry 规则 `[通用]`

`{REQ_REGISTRY_FILE}` 与 `{BUG_REGISTRY_FILE}` 是编号、索引和去重入口，不是阶段目录的一部分。

规则：

- 需求 registry 必须位于 `{REQ_ROOT_DIR}/{REQ_REGISTRY_FILE}`。
- BUG registry 必须位于 `{BUG_ROOT_DIR}/{BUG_REGISTRY_FILE}`。
- registry 中如记录路径，必须使用完整阶段路径，例如 `issues/requirements/review/REQ-0001-login/`。
- registry 中如记录阶段，字段建议为 `lifecycle_stage`。
- 移动目录后必须同步 registry，不得保留失效路径。

## 7. 遗留路径兼容 `[条件启用]`

如果项目历史上存在扁平路径：

```text
{REQ_ROOT_DIR}/{REQ_ID_PATTERN}/
{BUG_ROOT_DIR}/{BUG_ID_PATTERN}/
```

兼容策略：

- 工具链可以继续读取遗留路径，但新建条目不得写入遗留路径。
- 自动化查找必须同时支持阶段路径与遗留路径，或使用递归搜索。
- 当遗留条目发生评审、纳入迭代或归档迁移时，应顺带移动到对应阶段目录。
- 迁移遗留目录前必须确认目标阶段不存在同 ID 目录，避免覆盖。

## 8. 与需求、BUG、Sprint、OpenSpec 的关系 `[通用 + 条件启用]`

| 文档或流程 | 与本文件关系 |
| --- | --- |
| `rules/requirement-management.md` | 定义需求状态机、需求包、评审门禁和验收规则；阶段目录映射引用本文 |
| `rules/bug-management.md` | 定义 BUG 状态机、复现、根因、回归和关闭规则；阶段目录映射引用本文 |
| `rules/directory-structure.md` | 定义 `issues/` 的目录边界；阶段目录细则引用本文 |
| `rules/document-governance.md` | 定义文档维护、归档和同步规则；issues 迁移规则引用本文 |
| `rules/iterations-lifecycle.md` | 定义 Sprint 的 change、archive 阶段；Sprint 只能纳入 `review/` 中已 approved 的 REQ/BUG |
| `iterations/{change,archive}/` | 迭代四件套位置；与 issues 阶段在 `/sprint-archive` 中同步闭环 |
| `openspec/changes/` | 与 `review/` 阶段并行推进；归档后同步 Issue 进入 `archive/` |
| `openspec/changes/archive/` | OpenSpec change 的归档位置，不替代 `issues/*/archive/` |

如果项目不启用 Sprint 或 OpenSpec，应将对应章节改为团队实际研发任务或外部看板流程，但仍必须保留“先评审、再实现、后归档”的阶段门禁。

## 9. 自动化与脚本要求 `[通用 + 条件启用]`

脚本和命令必须满足：

- 目录结构校验必须检查 `plan/`、`review/`、`archive/` 是否存在。
- workflow sync 必须能递归发现 `issues/requirements/**/trace.md` 与 `issues/bugs/**/trace.md`。
- `/sprint-propose` 必须只把已评审通过的条目写入 Sprint 规划。
- `/req-opsx` 与 `/bug-opsx` 必须优先从 `review/` 查找条目。
- `/sprint-archive` 或 `/opsx-archive` 必须将完成闭环的条目移动到 `archive/`。

禁止：

- 只查找 `{REQ_ROOT_DIR}/{REQ_ID_PATTERN}/trace.md` 或 `{BUG_ROOT_DIR}/{BUG_ID_PATTERN}/trace.md`。
- 在 `issues/requirements/` 或 `issues/bugs/` 根目录直接新建 REQ/BUG 目录。
- 在未完成评审时写入 Sprint 规划、创建 OpenSpec change 或执行开发。

## 10. 初始化生成建议 `[通用]`

工程初始化时应：

1. 根据用户输入生成 `{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{REQ_ID_PATTERN}`、`{BUG_ID_PATTERN}`。
2. 默认创建 `plan/`、`review/`、`archive/` 三个阶段目录。
3. 默认将 `_registry.yaml` 放在需求与 BUG 根目录。
4. 将本文件加入 AGENTS.md 必读规则、rules 清单和初始化校验脚本。
5. 将 `rules/requirement-management.md`、`rules/bug-management.md`、`rules/directory-structure.md`、`rules/document-governance.md` 中涉及 issues 生命周期的内容与本文保持一致。
6. 如果用户项目已有外部看板，应在本文件中增加外部状态与阶段目录的映射，不得覆盖 Harness 基线门禁。

## 11. AI 检查清单 `[通用]`

```text
□ 新建 REQ/BUG 是否落在 plan/？
□ 评审通过后是否移动到 review/？
□ 拒绝、延期、不修或关闭后是否移动到 archive/？
□ Sprint 规划是否只纳入 review/ 中已 approved 的条目？
□ req-opsx/bug-opsx 是否只处理已 approved 的条目？
□ 归档闭环后 Issue 是否移动到 archive/？
□ _registry.yaml 是否仍在 issues 类型根目录？
□ trace.md 是否同步 status、lifecycle_stage、current_path 和变更记录？
□ 自动化脚本是否递归解析阶段目录，而不是硬编码旧扁平路径？
□ 本文件是否与 requirement-management、bug-management、directory-structure、document-governance 保持一致？
```
