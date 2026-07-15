---
purpose: 需求（REQ）生命周期、状态机、目录与评审门禁
source: 项目团队 + AI v2 定稿
update_method: 命令族变更时同步更新
updated_at: 2026-07-11 16:25:13
---

# 需求管理规范

## 1. 目录

```text
issues/requirements/
├── _registry.yaml
├── README.md
├── plan/                      # 规划中并完成评审（capture → approve 前/迁移前）
│   └── REQ-NNNN-slug/
├── review/                    # 已评审通过，开发/验收中，未 OpenSpec archive
│   └── REQ-NNNN-slug/
├── archive/                   # 已交付并归档
│   └── REQ-NNNN-slug/
└── REQ-NNNN-slug/             # [遗留] 扁平路径，deprecated；勿新建
```

单条 REQ 目录内文件（与阶段无关）：

```text
REQ-NNNN-slug/
├── capture.md
├── requirement.md
├── user-stories.md
├── business-flow.md
├── acceptance.md
├── trace.md
├── review.md
└── prototype/{web,admin,miniapp}/
```

**新建 MUST** 使用 `issues/requirements/plan/REQ-NNNN-slug/`。阶段含义、迁移时机见 `rules/issues-lifecycle.md`。

禁止在 `docs/product/`、`docs/prd/` 存放业务需求（见 `rules/document-governance.md`）。

## 2. 状态机

| status | 含义 |
|--------|------|
| `captured` | 已记录（capture.md） |
| `exploring` | 已探讨，未落 PRD |
| `draft` | 仅有 requirement.md |
| `enriching` | 六件套补齐中 |
| `pending_review` | 文档齐，待评审 |
| `approved` | **评审通过**（可 req-opsx、可进 Sprint） |
| `rejected` | 不做 |
| `deferred` | 延后 |
| `in_sprint` | 已纳入迭代 |
| `done` | 已交付验收 |

**事实源**：`trace.md` 的 `status`；`requirement.md` frontmatter **MUST** 同步。

## 3. 命令与阶段

| 命令 | 允许 status（入口） | 产出 |
|------|---------------------|------|
| `/capture` | — | 类型未决时自动分类；REQ 部分同 `/req-capture`（见 §3.2） |
| `/req-capture` | — | capture.md、trace 壳（可一次输入多条，按 §3.1 评估拆分） |

### 3.2 `/capture` 与 req-capture

用户不确定输入是需求还是缺陷时使用 `/capture`。AI **MUST** 先分类再落盘：判为需求的条目遵循 §3.1 拆分规则，产出与 `/req-capture` 相同，且 frontmatter 含 `captured_via: capture`、`classification_rationale`。一条消息可同时产生 REQ 与 BUG。

### 3.1 `/req-capture` 多条输入与拆分

用户可能在一条消息中描述多个需求。AI **MUST** 先评估再落盘：

- **拆分**：不同业务能力/模块/端、独立优先级、独立 OpenSpec Change 或验收闭环，或用户显式并列枚举 → 每条独立 `REQ-NNNN-slug/`。
- **合并**：同一功能域的一个交付单元，或将在同一份 `requirement.md` 展开的细节 → 单条 REQ。
- **父需求 refinement**：对已有 REQ 的体验/策略补充 → 优先 `parent_requirement` 或更新原 REQ，而非随意新建 peer REQ。
- **实为缺陷** → `/bug-capture`，不要 req-capture。
- **禁止** umbrella REQ；创建多条时 Workflow Sync 对**每条**执行 `req.capture`。
| `/req-explore` | captured, exploring | 默认无文件 |
| `/req-generate` | captured, exploring | requirement.md → draft |
| `/req-complete` | draft, enriching | 六件套 → pending_review |
| `/req-review` | pending_review | review.md → approved/rejected/deferred |
| `/req-opsx` | **approved** | openspec/changes/* |

## 4. 门禁

### 4.1 评审门禁（统一，MUST）

以下动作 **MUST** 在 REQ `trace.md`（或 `requirement.md` frontmatter）`status ∈ { approved, in_sprint }` 后方可执行：

| 动作 | 命令 |
|------|------|
| 创建 OpenSpec Change | `/req-opsx` |
| 纳入 Sprint 规划 | `/sprint-propose` |
| 迭代内开发 | `/sprint-apply` |

**未评审**（`draft`、`pending_review`、`captured`、`enriching`、`exploring` 等）时：

- **不得**写入 `sprint.yaml` 的 `requirements[]` / `bugs[]`
- **不得**写入 `sprint.md` 的 Sprint 目标编号列表、§Scope 表、里程碑、工作量合计
- **不得**写入 `release-note.md` / `acceptance-report.md` 的「关联需求/BUG」正式范围
- **不得**将 REQ `trace.md` 的 `iteration` 设为 sprint-xxx
- **仅可**记入 `sprint.md`「延后项（待评审）」并提示 `/req-review REQ-xxxx --approve`
- 用户显式要求纳入 Sprint 时也 **MUST** 先拒绝写入规划，完成评审后再 `/sprint-propose`

`in_sprint` 表示已评审通过且已纳入迭代；**不得**用 `in_sprint` 绕过 `approved` 评审。

### 4.2 opsx-apply 迭代纳入门禁（统一，MUST）

来源于 REQ 的 OpenSpec Change 在 `/opsx-apply` 前 **MUST** 已正式纳入某个 `sprint-xxx`：

- REQ `trace.md` MUST 满足 `status: in_sprint`（或后续交付态）且 `iteration: sprint-xxx` 非空。
- 对应 `iterations/change|archive/<sprint>/sprint.yaml` MUST 在 `requirements[]` 与 `changes[]` 中包含该 REQ 与 Change。
- `/opsx-apply` MUST 先用 `--sprint auto` 或等价检查确认能解析到 Sprint；解析失败时必须停止，提示先执行 `/sprint-propose`。

`approved` 只表示已评审通过，可 `/req-opsx` 与进入 Sprint 规划；不得仅凭 `approved` 直接 `/opsx-apply`。

### 4.3 其他门禁

- `/req-opsx`：**仅** `approved` 或已评审后的 `in_sprint`
- 旧命令 `/requirement-to-opsx` 已删除 → `/req-opsx`

## 5. Readiness（req-opsx / req-complete）

| 级别 | 条件 |
|------|------|
| Ready | requirement + user-stories + business-flow + acceptance + trace 齐全 |
| Partially Ready | 缺 prototype 或非阻塞项 |
| Not Ready | 缺 requirement 或 acceptance |

## 6. trace.md 最小字段

Frontmatter **MUST** 含 `created_at`、`updated_at`（格式见 `rules/document-governance.md` §2.3–§2.4）。

```yaml
requirement_id: REQ-NNNN-slug
status: captured
priority: P1
created_at: YYYY-MM-DD HH:mm:ss
updated_at: YYYY-MM-DD HH:mm:ss
lifecycle:
  captured: YYYY-MM-DD HH:mm:ss
  generated: null
  completed: null
  reviewed: null
  approved: null
iteration: null
openspec_changes: []
related_requirements: []
```

每次命令结束追加 `## 变更记录`（条目时间 MUST 为 `YYYY-MM-DD HH:mm:ss`）。

## 7. 需求 ↔ BUG 反向关联

当 BUG 文档中的 `related_requirement` 指向某个需求时，该需求的 `trace.md` MUST 维护索引级 `## 关联缺陷` 章节。该章节只记录缺陷索引，不重复 BUG 全文。

推荐格式：

```markdown
## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0003-brand-image-display-layout-shift | high | done | fix-brand-image-display-layout-shift | 品牌 Logo 展示与提示布局修复 |
```

同步时机：

- BUG 创建或完善后确定 `related_requirement` 时，MUST 在父需求 `trace.md` 增加或更新对应行。
- BUG 进入 Sprint、完成 `/opsx-apply`、完成 `/opsx-archive` 或状态变化时，MUST 同步更新父需求 `trace.md` 中该 BUG 的 `状态` 与 `关联 Change`。
- 若 BUG 的 `related_requirement` 为 `null`，不得强行写入需求 trace；除非后续评审明确补齐父需求。

`lifecycle` 与 `## 变更记录` 中所有时间记录 MUST 遵守 `rules/document-governance.md` 的秒级格式：`YYYY-MM-DD HH:mm:ss`（默认 `Asia/Shanghai`）。

状态变更后 MUST 运行 `python scripts/sync-workflow-status.py`（见 `rules/document-governance.md`；如项目提供 Agent 技能，参照对应 `workflow-sync` 说明）。同步脚本会刷新 `updated_at` 并补全缺失的 `created_at`。

## 8. 参考命令

对应 Agent 工具入口中的 `source-command-req-*` 技能说明。
