---
purpose: Iterations 生命周期阶段目录规范
content: 规范 Sprint 在 change、archive 两个物理阶段目录中的准入条件、迁移时机、sprint.yaml 字段、路径解析、遗留兼容和自动化检查
source: Harness iterations-lifecycle.md 抽象模板，基于项目 iterations 两阶段目录治理规则沉淀
update_method: 项目初始化时按用户输入生成；迭代目录结构、Sprint 状态机、归档流程、OpenSpec 流程或自动化脚本变化时更新
created_at: 2026-06-27 23:45:00
updated_at: 2026-06-27 23:45:00
note: 适用于 {PRODUCT_NAME} 项目；与 issues plan/review/archive 互补；Sprint 机器事实源为 sprint.yaml
template_scope: 可作为工程初始化的 iterations-lifecycle.md 独立模块
---

# Iterations 生命周期阶段目录规范

## 0. 规则定位 `[通用]`

本文件定义 `{PRODUCT_NAME}` 中 `iterations/` 的共享物理生命周期规则。它不替代 `rules/document-governance.md` 中的迭代文档治理，也不替代 Sprint 命令说明，而是规定 Sprint 在文件系统中的阶段位置、迁移时机、`sprint.yaml` 字段、路径解析、归档闭环和自动化检查。

AI 在执行以下任务前必须读取本文件：

- 新建、规划、探索、执行、复盘、关闭或归档 Sprint。
- 执行 `/sprint-propose`、`/sprint-explore`、`/sprint-apply`、`/sprint-exps`、`/sprint-archive`。
- 修改 `iterations/` 目录结构、`sprint.yaml`、Sprint 四件套、Workflow Sync 脚本或初始化模板。
- 判断 Sprint 是否可以开发、复盘、关闭、归档或从 `change/` 移入 `archive/`。

## 1. 文档模块分类 `[通用]`

本模板将 Iterations 生命周期规则拆分为三类，工程初始化时应根据用户输入生成最终文档：

- `[通用]`：所有 Harness 项目默认保留的 Sprint 两阶段目录治理规则。
- `[个性化]`：必须根据团队迭代模式、命令族、状态机、归档策略、发布策略和外部系统替换的内容。
- `[条件启用]`：仅在项目启用对应能力时保留，例如 OpenSpec、Sprint、外部项目管理工具、遗留扁平目录兼容、自动化同步脚本等。

推荐初始化参数：

| 参数 | 用途 |
| --- | --- |
| `{PRODUCT_NAME}` | 项目或产品名称 |
| `{ITERATION_ROOT_DIR}` | 迭代根目录，默认 `iterations/` |
| `{ITERATION_PATTERN}` | 迭代目录命名，例如 `sprint-xxx` |
| `{SPRINT_FACT_SOURCE}` | 迭代事实源文件，默认 `sprint.yaml` |
| `{ITERATION_LIFECYCLE_STAGES}` | 阶段目录集合，默认 `change`、`archive` |
| `{SPRINT_STATUS_MACHINE}` | Sprint 状态机，默认 `planning`、`in_progress`、`completed` |
| `{SPRINT_STATUS_TO_STAGE}` | Sprint 状态到阶段目录的映射 |
| `{SPRINT_COMMAND_SET}` | Sprint 命令族 |
| `{SPRINT_ARCHIVE_POLICY}` | Sprint 归档策略 |
| `{SPRINT_REVIEW_POLICY}` | Sprint 关闭或验收确认策略 |
| `{SPRINT_PATH_COMPAT_POLICY}` | 遗留路径兼容策略 |
| `{WORKFLOW_SYNC_COMMAND}` | 工作流同步命令，例如 `python scripts/sync-workflow-status.py` |
| `{TASK_TRACKING_SYSTEM}` | 外部项目管理或迭代系统 |

## 2. 总原则 `[通用]`

- 阶段目录表达物理位置，`sprint.yaml` 的 `status` 表达逻辑状态；二者必须互相一致。
- 新建 Sprint 必须进入 `iterations/change/`，不得直接创建在 `iterations/archive/` 或 `iterations/` 根目录。
- 未完成归档闭环的 Sprint 必须保留在 `change/`。
- `archive/` 只保存已完成归档的 Sprint；归档后默认只读，不得继续作为开发事实源修改。
- 每个 `sprint-xxx/` 目录在任一时刻只能存在于一个阶段目录中，不得复制多份。
- 自动化脚本和命令必须递归解析 `iterations/**/sprint.yaml`，不得硬编码旧式扁平路径。
- Sprint 归档不替代 OpenSpec archive，也不替代 issues archive；三者必须在 `/sprint-archive` 中同步闭环。

## 3. 目录结构 `[通用 + 个性化]`

推荐结构：

```text
{ITERATION_ROOT_DIR}
├── change/
│   └── {ITERATION_PATTERN}/
│       ├── {SPRINT_FACT_SOURCE}
│       ├── sprint.md
│       ├── release-note.md
│       └── acceptance-report.md
└── archive/
    └── {ITERATION_PATTERN}/
        ├── {SPRINT_FACT_SOURCE}
        ├── sprint.md
        ├── release-note.md
        └── acceptance-report.md
```

阶段目录职责：

| 阶段目录 | 通用定义 | 典型 `sprint.yaml status` | 说明 |
| --- | --- | --- | --- |
| `change/` | 未归档 Sprint | `planning`、`in_progress` | 用于规划、执行、验收、复盘前后的未归档迭代 |
| `archive/` | 已归档 Sprint | `completed` | 用于已完成 Change archive、验收收尾和发布说明收尾的历史迭代 |

约束：

- 阶段目录内不得再嵌套 `change/`、`archive/`。
- Sprint 四件套的字段、marker、时间格式和同步规则以 `rules/document-governance.md` 为准。
- Sprint 目录不存放源码、构建产物、测试日志、运行时缓存或临时文件。

## 4. 阶段准入与迁移时机 `[通用 + 个性化]`

| 事件 | 常见命令 | 目录迁移 | 要求 |
| --- | --- | --- | --- |
| 新建 Sprint | `/sprint-propose` | 无 → `change/` | 创建 Sprint 四件套，写入 `status: planning` 与 `lifecycle_stage: change`，并承接 `docs/knowledge-base/` 中未关闭行动项 |
| 范围/依赖探索 | `/sprint-explore` | 保持 `change/` | 只更新风险、依赖、容量和范围建议 |
| 执行 Sprint | `/sprint-apply` | 保持 `change/` | 只处理 `change/` 中未归档 Sprint |
| 经验复盘 | `/sprint-exps` | 通常保持原阶段 | 可读取 `change/` 或 `archive/`，输出沉淀到 `docs/knowledge-base/sprints/` |
| 单 Change 归档 | `/opsx-archive` | Sprint 保持 `change/` | 单个 Change 归档不触发 Sprint 目录迁移 |
| Sprint 归档闭环 | `/sprint-archive` | `change/` → `archive/` | 所有关联 Change、Issue、验收和发布说明完成闭环后移动整个 Sprint 目录 |

迁移要求：

- 必须移动整个 `sprint-xxx/` 目录，而不是复制单个文件。
- 迁移前必须确认目标阶段不存在同 ID 目录。
- 迁移后必须同步 `sprint.yaml` 的 `status`、`lifecycle_stage`、`updated_at` 和必要的验收/发布字段。
- 迁移后应运行 `{WORKFLOW_SYNC_COMMAND}` 或项目等价同步命令；如支持 `--check`，应执行漂移检查。
- 新建或执行 Sprint 前必须读取 `docs/knowledge-base/README.md`、最近一次 Sprint 复盘和相关 best-practices；未承接的 `open` 行动项必须在 `sprint.md` 风险或 Deferred 列表说明原因。

## 5. sprint.yaml 字段 `[通用 + 个性化]`

每个 Sprint 的 `{SPRINT_FACT_SOURCE}` 必须能表达逻辑状态和物理阶段。

推荐字段：

```yaml
sprint_id: sprint-xxx
status: planning | in_progress | completed
lifecycle_stage: change | archive
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
updated_at: YYYY-MM-DD hh:mm:ss
requirements:
  - id: REQ-xxxx
    name: 需求名称
    priority: P0 | P1 | P2
    status: approved | in_sprint | completed
    description: 需求说明
    included_at: YYYY-MM-DD hh:mm:ss
bugs:
  - id: BUG-xxxx
    severity: P0 | P1 | P2
    status: approved | in_sprint | fixed
    description: 缺陷说明
    included_at: YYYY-MM-DD hh:mm:ss
changes:
  - id: change-id
    requirement: REQ-xxxx
    status: proposed | in_progress | applied | archived
    sprint_goal: Sprint 内交付目标
    target_date: YYYY-MM-DD hh:mm:ss
milestones:
  - id: M1
    stage: 阶段名称
    deliverable: 交付物
    status: planning | in_progress | completed
    target_date: YYYY-MM-DD hh:mm:ss
knowledge_base:
  carried_actions:
    - id: A-xxx
      source: docs/knowledge-base/sprints/YYYY-MM-DD-sprint-xxx-experience.md
      status: in_sprint
      target: REQ-xxxx | BUG-xxxx | change-id | rule-update
```

要求：

- `planning`、`in_progress` 必须对应 `lifecycle_stage: change`。
- `completed` 必须对应 `lifecycle_stage: archive`。
- `status` 与 `lifecycle_stage` 不一致时，必须优先修复不一致，不得继续归档或作为事实源推进开发。
- `sprint.md` 的 Scope 模块必须包含需求的 `description`、BUG 的 `description` 和 Change 的 `sprint_goal`。
- `sprint.md` 的里程碑模块必须包含 `target_date`。
- 上述正文时间字段必须是完整 `YYYY-MM-DD hh:mm:ss`；如果只能确认日期，必须写 `待确认`，不得自动补成 `00:00:00`。
- `knowledge_base.carried_actions` 必须记录本 Sprint 承接的复盘行动项；没有承接项时必须在 `sprint.md` 说明“无适用 open 行动项”。
- `sprint.md` 或项目约定变更记录中应记录 `change -> archive` 的迁移原因和命令来源。

## 6. 遗留路径兼容 `[条件启用]`

如果项目历史上存在扁平路径：

```text
iterations/{ITERATION_PATTERN}/
```

兼容策略：

- 工具链可以继续读取遗留路径，但新建 Sprint 不得写入遗留路径。
- 自动化查找必须同时支持阶段路径与遗留路径，或使用 `iterations/**/sprint.yaml` 递归搜索。
- 当遗留 Sprint 发生执行、复盘或归档迁移时，应顺带移动到 `change/` 或 `archive/`。
- 迁移遗留目录前必须确认目标阶段不存在同 ID 目录，避免覆盖。

## 7. 与 Issues、OpenSpec、知识库的关系 `[通用 + 条件启用]`

| 文档或流程 | 与本文件关系 |
| --- | --- |
| `rules/issues-lifecycle.md` | 定义 REQ/BUG 的 plan、review、archive 阶段；Sprint 只能纳入已评审条目 |
| `rules/document-governance.md` | 定义 Sprint 四件套字段、marker、时间格式、同步和归档要求 |
| `rules/directory-structure.md` | 定义 `iterations/` 的目录边界；阶段目录细则引用本文 |
| `iterations/change/` | 当前或未归档 Sprint 四件套 |
| `iterations/archive/` | 已归档 Sprint 四件套 |
| `openspec/changes/` | Sprint 执行期间推进的 Change |
| `openspec/changes/archive/` | Sprint 归档时应同步完成的 Change archive |
| `issues/*/review/` | 已评审、开发中 REQ/BUG |
| `issues/*/archive/` | Sprint 归档后应同步闭环的 REQ/BUG |
| `docs/knowledge-base/sprints/` | Sprint 经验沉淀，不替代 Sprint 四件套 |

如项目不启用 Sprint，应将本文替换为项目等价迭代、里程碑、版本或外部看板流程，但仍必须保留“未归档 / 已归档”的物理阶段或等价状态门禁。

## 8. 自动化与脚本要求 `[通用 + 条件启用]`

脚本和命令必须满足：

- 目录结构校验必须检查 `iterations/change/` 与 `iterations/archive/` 是否存在。
- Workflow Sync 必须能递归发现 `iterations/**/sprint.yaml`。
- `/sprint-propose` 必须写入 `iterations/change/<sprint-id>/`。
- `/sprint-apply` 默认只处理 `iterations/change/<sprint-id>/`。
- `/sprint-exps` 必须能读取 `iterations/change/<sprint-id>/` 或 `iterations/archive/<sprint-id>/`。
- `/sprint-archive` 必须在完成闭环后将 Sprint 目录移动到 `iterations/archive/<sprint-id>/`。

禁止：

- 在 `iterations/` 根目录直接新建 `sprint-xxx/`。
- 只查找 `iterations/*/sprint.yaml`。
- Sprint 未完成归档闭环时移动到 `archive/`。
- 归档后继续把 `archive/` 中的 Sprint 作为开发执行事实源。

## 9. 初始化生成建议 `[通用]`

工程初始化时应：

1. 默认创建 `iterations/change/` 与 `iterations/archive/`。
2. 默认将新 Sprint 输出到 `iterations/change/{ITERATION_PATTERN}/`。
3. 默认将完成归档的 Sprint 移动到 `iterations/archive/{ITERATION_PATTERN}/`。
4. 将本文件加入 AGENTS.md 必读规则、rules 清单和初始化校验脚本。
5. 将 `rules/document-governance.md`、`rules/directory-structure.md`、Sprint 命令和 `sync-workflow-status.py` 中涉及 iterations 生命周期的内容与本文保持一致。
6. 如果用户项目已有外部项目管理系统，应在本文中增加外部状态与阶段目录的映射，不得覆盖 Harness 基线门禁。

## 10. AI 检查清单 `[通用]`

```text
□ 新建 Sprint 是否落在 iterations/change/？
□ sprint.yaml 是否包含或能推导 lifecycle_stage？
□ sprint-apply 是否只处理未归档 Sprint？
□ sprint-exps 是否可读取 change/archive 两个分区？
□ sprint-archive 后是否移动到 iterations/archive/？
□ Sprint archive 是否同步 OpenSpec change archive？
□ Sprint archive 是否同步关联 REQ/BUG 的 trace 和必要归档？
□ Workflow Sync 是否递归解析 iterations/**/sprint.yaml？
□ 本文件是否与 document-governance、directory-structure、AGENTS 和 Sprint 命令保持一致？
```
