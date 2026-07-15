---
purpose: 缺陷（BUG）生命周期、状态机、目录与评审门禁
source: 项目团队 + AI v2 定稿
update_method: 命令族变更时同步更新
updated_at: 2026-07-11 16:25:13
---

# 缺陷管理规范

## 1. 目录

```text
issues/bugs/
├── _registry.yaml
├── README.md
├── plan/                      # 规划中并完成评审
│   └── BUG-NNNN-slug/
├── review/                    # 已评审通过，修复/验收中，未 OpenSpec archive
│   └── BUG-NNNN-slug/
├── archive/                   # 已修复并归档
│   └── BUG-NNNN-slug/
└── BUG-NNNN-slug/             # [遗留] 扁平路径，deprecated；勿新建
```

单条 BUG 目录内文件：

```text
BUG-NNNN-slug/
├── capture.md
├── bug.md
├── root-cause.md
├── workaround.md
├── acceptance.md
├── trace.md
├── review.md
├── logs/
└── screenshots/
```

**新建 MUST** 使用 `issues/bugs/plan/BUG-NNNN-slug/`。阶段含义、迁移时机见 `rules/issues-lifecycle.md`。

禁止在 `docs/bugs/` 存放缺陷记录。

## 2. 状态机

| status | 含义 |
|--------|------|
| `captured` | 已记录 |
| `exploring` | 复现/影响分析中 |
| `draft` | 仅有 bug.md |
| `enriching` | 缺陷包补齐中 |
| `pending_review` | 待评审 |
| `approved` | **确认修复**（可 bug-opsx、可进 Sprint） |
| `rejected` | 非缺陷/误报 |
| `wont_fix` | 不修 |
| `deferred` | 延后 |
| `in_sprint` | 已纳入迭代 |
| `done` | 已修复验收 |

## 3. 命令与阶段

| 命令 | 产出 |
|------|------|
| `/capture` | 类型未决时自动分类；BUG 部分同 `/bug-capture`（见 §3.2） |
| `/bug-capture` | capture.md、trace 壳（可一次输入多条，按 §3.1 评估拆分） |

### 3.2 `/capture` 与 bug-capture

用户不确定输入是需求还是缺陷时使用 `/capture`。AI **MUST** 先分类再落盘：判为缺陷的条目遵循 §3.1 拆分规则，产出与 `/bug-capture` 相同，且 frontmatter 含 `captured_via: capture`、`classification_rationale`。一条消息可同时产生 REQ 与 BUG。

### 3.1 `/bug-capture` 多条输入与拆分

用户可能在一条消息中描述多个缺陷。AI **MUST** 先评估再落盘：

- **拆分**：不同界面/层级、缺陷类型、修复面、严重度、交付优先级，或用户显式并列枚举 → 每条独立 `BUG-NNNN-slug/`。
- **合并**：同一页面/弹窗且一次修复可闭环，或同一根因不可分割 → 单条 BUG；回复中一句话说明不拆理由。
- **禁止** umbrella BUG（总记录 + 子 bullet）；每条 MUST 可独立走 explore → opsx → archive。
- 创建多条时，`next_id` 连续递增；Workflow Sync 对**每条**执行 `bug.capture`。
| `/bug-explore` | 默认无文件 |
| `/bug-generate` | bug.md |
| `/bug-complete` | root-cause、workaround、acceptance、trace |
| `/bug-review` | review.md、status |
| `/bug-opsx` | openspec/changes/fix-* |

## 4. 门禁

### 4.1 评审门禁（统一，MUST）

与 `rules/requirement-management.md` §4.1 一致。BUG `trace.md` `status ∈ { approved, in_sprint }` 后方可：

- `/bug-opsx`
- 纳入 Sprint 规划（`/sprint-propose`）
- `/sprint-apply`

未评审 BUG **不得**写入 Sprint 四件套正式范围；仅可记入 `sprint.md`「延后项（待评审）」并提示 `/bug-review BUG-xxxx --approve`。

### 4.2 opsx-apply 迭代纳入门禁（统一，MUST）

来源于 BUG 的 OpenSpec Change 在 `/opsx-apply` 前 **MUST** 已正式纳入某个 `sprint-xxx`：

- BUG `trace.md` MUST 满足 `status: in_sprint`（或后续交付态）且 `iteration: sprint-xxx` 非空。
- 对应 `iterations/change|archive/<sprint>/sprint.yaml` MUST 在 `bugs[]` 与 `changes[]` 中包含该 BUG 与 Change。
- `/opsx-apply` MUST 先用 `--sprint auto` 或等价检查确认能解析到 Sprint；解析失败时必须停止，提示先执行 `/sprint-propose`。

`approved` 只表示已评审通过，可 `/bug-opsx` 与进入 Sprint 规划；不得仅凭 `approved` 直接 `/opsx-apply`。

### 4.3 其他门禁

- `/bug-opsx`：**仅** `approved` 或已评审后的 `in_sprint`
- Sprint：**P0 BUG** 优先于功能 REQ
- 旧命令 `/bug-to-change` 已删除 → `/bug-opsx`

## 5. 严重等级

```text
blocker | critical | high | medium | low
```

## 6. 知识沉淀

修复后若有复用价值，可更新 `docs/knowledge-base/incidents/`（由 bug-opsx tasks 提醒）。

## 7. 父需求反向追溯

BUG 的 `related_requirement` 不只是单向引用。若 `related_requirement` 非空，AI 在以下阶段 MUST 同步更新父需求 `issues/requirements/<REQ-ID>/trace.md` 的 `## 关联缺陷` 索引表：

- `/bug-complete` 或 `/bug-review` 确认父需求后。
- `/bug-opsx` 创建或确认修复 Change 后。
- BUG 纳入 Sprint、完成 `/opsx-apply`、完成 `/opsx-archive` 或状态变化后。

父需求 trace 中只记录索引级信息：`BUG`、`严重等级`、`状态`、`关联 Change`、`说明`。MUST NOT 在需求 trace 中复制 BUG 复现步骤、根因全文、日志或截图。

`trace.md` 的 `lifecycle` 与 `## 变更记录` 中所有时间记录 MUST 遵守 `rules/document-governance.md` §2.3（`YYYY-MM-DD HH:mm:ss`）。

Frontmatter **MUST** 含 `created_at`、`updated_at`；更新 trace 时刷新 `updated_at`，不得修改 `created_at`。

状态变更后 MUST 运行 `python scripts/sync-workflow-status.py`（见 `rules/document-governance.md`；如项目提供 Agent 技能，参照对应 `workflow-sync` 说明）。

## 8. 参考命令

对应 Agent 工具入口中的 `source-command-bug-*` 技能说明。
