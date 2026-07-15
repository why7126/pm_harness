---
purpose: iterations Sprint 生命周期阶段目录规范
content: change / archive 两阶段目录职责、准入条件、迁移时机与路径解析
source: 项目团队确认
update_method: Sprint 流程或目录边界变化时同步更新
created_at: 2026-06-27 23:45:00
updated_at: 2026-07-11 16:25:13
note: 与 issues plan/review/archive 互补；机器索引仍为 sprint.yaml
---

# iterations 生命周期阶段目录

## 1. 目标

在 `iterations/` 下，用 **change / archive** 两目录表达 Sprint 在「迭代进行中 → 归档闭环」中的物理位置，与 `sprint.yaml` 的 `status` 互补：

- **status**：逻辑状态机（`planning`、`in_progress`、`completed`）
- **lifecycle_stage**（物理目录）：`change` | `archive`

## 2. 目录结构（MUST）

```text
iterations/
├── README.md
├── change/                    # 未归档：规划中或开发中
│   └── sprint-xxx/
│       ├── sprint.yaml
│       ├── sprint.md
│       ├── release-note.md
│       └── acceptance-report.md
└── archive/                   # 已完成归档
    └── sprint-xxx/
        └── （同上四件套）
```

- 每个 `sprint-xxx/` 目录 **MUST** 仅存在于 `change/` 或 `archive/` 之一（不得多份拷贝）。
- 阶段子目录内 **禁止** 再嵌套 `change/archive`。
- 四件套规范见 `rules/document-governance.md` §4.1。

### 2.1 遗留扁平路径（兼容）

历史 Sprint 可能仍在：

```text
iterations/sprint-xxx/   # 遗留，deprecated
```

- 工具链 **SHOULD** 继续可读遗留路径（见 `scripts/workflow_sync/collect.py` 的 `resolve_sprint_dir()`）。
- 新建 Sprint **MUST** 落在 `change/` 下，**MUST NOT** 在 `iterations/` 根下新建 `sprint-*`。
- 批量迁移时使用 `scripts/migrate-iterations-lifecycle-stage.py`。

## 3. 两阶段定义

| 阶段目录 | 含义 | 典型 sprint.yaml `status` |
|---|---|---|
| **change** | **未归档**：迭代规划、开发、验收进行中 | `planning`、`in_progress` |
| **archive** | **已完成归档**：Sprint 内 Change 已全部 `/opsx-archive`，迭代验收与发布说明已收尾 | `completed` |

## 3.1 Sprint 容量门禁（MUST）

`/sprint-propose` 在生成正式四件套或更新 REQ/BUG/Change trace 前 MUST 计算候选范围的容量占用率：

```text
capacity_usage = estimated_person_days / capacity_person_days
```

- 若容量或估算缺失导致无法计算，MUST 先补齐输入；不得默认通过。
- 当 `estimated_person_days > capacity_person_days * 1.2` 时，MUST 硬阻断正式规划：不得创建 `iterations/change/<sprint>/` 四件套，不得更新 `trace.md` 的 `iteration` 或 Change trace，并提示拆分 Sprint、移出低优先级项或替换范围后重新运行 `/sprint-propose`。
- 当 `capacity_person_days < estimated_person_days <= capacity_person_days * 1.2` 时，MAY 继续生成 Sprint，但 MUST 在 `sprint.md` 记录容量风险、fix 缓冲影响和延后项建议。
- 当 `estimated_person_days <= capacity_person_days` 时，按既有 Review Gate、Readiness Gate 和 Scope 规则继续。

## 3.2 opsx-apply 迭代纳入门禁（MUST）

`/opsx-apply <change-id>` 对来源于 REQ/BUG 的 Change 执行前，目标 Change **MUST** 已纳入某个 `sprint-xxx` 正式范围。门禁判定以 Sprint 四件套与 Issue trace 双向一致为准：

- `iterations/change|archive/<sprint>/sprint.yaml` 的 `changes[]` MUST 包含 `<change-id>`。
- 若 Change 关联 REQ，`requirements[]` MUST 包含对应 `REQ-*`；若关联 BUG，`bugs[]` MUST 包含对应 `BUG-*`。
- 关联 REQ/BUG `trace.md` MUST 存在 `iteration: sprint-xxx`，且状态为 `in_sprint` 或后续交付态。
- `python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto --dry-run` 或等价解析 MUST 能定位到该 Sprint；若报告 sprint skipped / unresolved，MUST 停止 `/opsx-apply`。

未通过时的修复路径：先运行 `/sprint-propose` 将 REQ/BUG/Change 纳入 `iterations/change/<sprint>/`，完成 Workflow Sync 后再重新执行 `/opsx-apply`。

## 4. 目录迁移时机（MUST）

AI 在执行下列命令并成功后 **MUST** 移动目录（`git mv` 或等价），并更新 `sprint.yaml` 的 `lifecycle_stage`：

| 事件 | 命令示例 | 自 → 至 |
|---|---|---|
| 新建 Sprint | `/sprint-propose` | — → `change/` |
| 迭代归档闭环 | `/sprint-archive`（`status: completed`） | `change/` → `archive/` |

**不迁移**：

- 仅 `/sprint-explore`、`/sprint-apply` 进行中 → 保留在 `change/`
- 单 Change `/opsx-archive` → Sprint 目录 **不** 单独迁移（整 Sprint 归档时一并迁移）

迁移后 **SHOULD** 运行 `python scripts/sync-workflow-status.py --check`。

## 5. sprint.yaml 字段

阶段目录变更时，在 `sprint.yaml` 中维护：

```yaml
lifecycle_stage: change | archive
```

`status` 与 `lifecycle_stage` **SHOULD** 一致：

- `planning` / `in_progress` → `change`
- `completed` → `archive`

`sprint.md` 的变更记录 **SHOULD** 记录迁移，例如：`change → archive（/sprint-archive）`。

## 6. 路径引用

- 文档与脚本引用时使用完整路径，例如：
  `iterations/change/sprint-003/` 或 `iterations/archive/sprint-002/`
- Workflow Sync、Sprint 命令 **MUST** 通过 `resolve_sprint_dir()` 解析路径，**禁止** 硬编码仅根目录扁平路径。

## 7. 与 issues / OpenSpec 关系

| 层级 | 职责 |
|---|---|
| `iterations/change/` | 当前或规划中的 Sprint 四件套 |
| `iterations/archive/` | 已结束 Sprint 四件套（历史保留） |
| `issues/*/review/` | 已评审、开发中 REQ/BUG |
| `openspec/changes/` | 进行中的 Change |
| `openspec/changes/archive/` | 已归档 Change |

Sprint 归档 **MUST** 在 `/sprint-archive` 时同步：Change → `openspec/changes/archive/`，关联 REQ/BUG → `issues/*/archive/`（若尚未迁入）。

## 8. AI 检查清单

```text
□ 新建 Sprint 是否落在 change/ ？
□ sprint-archive 后是否迁入 archive/ ？
□ sprint.yaml 是否更新 lifecycle_stage ？
□ 路径引用是否使用 change/ 或 archive/ 前缀？
□ 是否运行 sync-workflow-status.py --check ？
```
