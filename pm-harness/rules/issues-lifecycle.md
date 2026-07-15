---
purpose: issues 需求/BUG 生命周期阶段目录规范
content: plan / review / archive 三阶段目录职责、准入条件、迁移时机与路径解析
source: 项目团队确认
update_method: 需求/BUG 流程或目录边界变化时同步更新
created_at: 2026-06-27 22:24:39
updated_at: 2026-06-27 23:45:00
note: REQ 与 BUG 共用；registry 与 _registry.yaml 仍位于 issues/* 根下
---

# issues 生命周期阶段目录

## 1. 目标

在 `issues/requirements/` 与 `issues/bugs/` 下，用 **plan / review / archive** 三目录表达条目在「文档规划 → 开发交付 → 归档闭环」中的物理位置，与 `trace.md` 的 `status` 互补：

- **status**：逻辑状态机（captured、approved、done…）
- **lifecycle_stage**（物理目录）：`plan` | `review` | `archive`

## 2. 目录结构（MUST）

```text
issues/requirements/          issues/bugs/
├── _registry.yaml            ├── _registry.yaml
├── README.md                 ├── README.md
├── plan/                     ├── plan/
│   └── REQ-NNNN-slug/        │   └── BUG-NNNN-slug/
├── review/                   ├── review/
│   └── REQ-NNNN-slug/        │   └── BUG-NNNN-slug/
└── archive/                  └── archive/
    └── REQ-NNNN-slug/            └── BUG-NNNN-slug/
```

- `_registry.yaml` **MUST** 留在 `issues/requirements/`、`issues/bugs/` **根目录**，不得移入阶段子目录。
- 每个 `REQ-*` / `BUG-*` 目录 **MUST** 仅存在于三个阶段目录之一（不得多份拷贝）。
- 阶段子目录内 **禁止** 再嵌套 `plan/review/archive`。

### 2.1 遗留扁平路径（兼容）

历史条目可能仍在：

```text
issues/requirements/REQ-NNNN-slug/   # 遗留，deprecated
issues/bugs/BUG-NNNN-slug/
```

- 工具链 **SHOULD** 继续可读遗留路径。
- 新建条目 **MUST** 落在 `plan/` 下，**MUST NOT** 在根下新建 `REQ-*` / `BUG-*`。
- 触发生命周期迁移时 **SHOULD** 顺带从遗留根路径迁入对应阶段目录。

## 3. 三阶段定义

| 阶段目录 | 含义 | 典型 status |
|---|---|---|
| **plan** | **规划中并完成评审**：从 capture 到文档齐、评审通过（或 reject/defer 终止于规划态） | `captured` … `pending_review`；`approved` 在迁移前可短暂停留；`rejected` / `deferred` |
| **review** | **已完成评审但未完成归档**：已 approved，Change 已创建或开发/验收中，OpenSpec 尚未 archive | `approved`、`in_sprint`；关联 Change `proposed` / `in_progress` / `applied` |
| **archive** | **已完成归档**：交付与 OpenSpec 归档闭环 | `done`；关联 Change `archived` |

## 4. 目录迁移时机（MUST）

AI 在执行下列命令并成功后 **MUST** 移动目录（`git mv` 或等价），并更新 `trace.md` 的 `lifecycle_stage`：

| 事件 | 命令示例 | 自 → 至 |
|---|---|---|
| 新建 | `/req-capture`、`/bug-capture`、`/capture` | — → `plan/` |
| 评审通过 | `/req-review --approve`、`/bug-review --approve` | `plan/` → `review/` |
| 归档闭环 | `/opsx-archive`、`/sprint-archive`（条目 status → done） | `review/` → `archive/` |

**`/opsx-archive` / `/sprint-archive` 归档 hook（MUST）**：

1. 先 `sync-workflow-status.py`（`opsx.archive` / `sprint.archive`）→ 更新 `trace.md` `status: done`
2. 再 `python scripts/promote-issues-for-archive.py --change <id>` 或 `--sprint <id>` → 物理迁入 `archive/`

promote 门禁：issue 全部关联 Change 已 archive，且 `status ∈ { done, … }`。多 Change REQ 须**全部** Change archive 后才 promote。

**不迁移**：

- `--reject` / `--defer` / `wont_fix` → 保留在 `plan/`
- 仅 `/req-generate`、`/req-complete` → 保留在 `plan/`

迁移后 **MUST** 运行 `python scripts/sync-workflow-status.py`（路径变更不影响 event 名）。

## 5. trace.md 字段

阶段目录变更时，在 `trace.md` frontmatter 或 yaml 块中维护：

```yaml
lifecycle_stage: plan | review | archive
```

`## 变更记录` **SHOULD** 记录迁移，例如：`plan → review（/req-review --approve）`。

## 6. 路径引用

- 文档与脚本引用时使用完整路径，例如：
  `issues/requirements/archive/REQ-0012-object-storage-key-layout/`
- 父需求关联缺陷索引、Workflow Sync 等 **MUST** 通过 `scripts/workflow_sync/collect.py` 的 `resolve_issue_dir()` 解析路径，**禁止** 硬编码仅根目录扁平路径。

## 7. 与 OpenSpec / iterations 关系

| 层级 | 职责 |
|---|---|
| `issues/*/plan` | 需求/BUG 文档包 |
| `issues/*/review` | 已评审、开发中条目 |
| `issues/*/archive` | 已交付条目（文档保留） |
| `openspec/changes/` | Change 工件（与 review 阶段并行） |
| `openspec/changes/archive/` | 已归档 Change |
| `iterations/change/sprint-xxx/` | 迭代四件套（进行中） |
| `iterations/archive/sprint-xxx/` | 迭代四件套（已归档） |

阶段目录 **不替代** OpenSpec archive；二者 MUST 在 `/opsx-archive` 时同步闭环（条目 → `issues/*/archive/`，Change → `openspec/changes/archive/`）。

## 8. AI 检查清单

```text
□ 新建 REQ/BUG 是否落在 plan/ ？
□ req-review/bug-review approve 后是否迁入 review/ ？
□ opsx-archive / sprint-archive 后是否运行 promote-issues-for-archive.py ？
□ issues 是否已迁入 archive/ 且 lifecycle_stage 一致？
□ _registry.yaml 是否仍在 issues 根目录？
□ 是否运行 sync-workflow-status.py？
```
