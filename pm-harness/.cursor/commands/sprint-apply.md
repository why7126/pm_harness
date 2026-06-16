---
name: /sprint-apply
id: sprint-apply
category: Workflow
description: 按 Sprint 依赖与优先级编排 OpenSpec Change 开发，自动跳过已完成/已归档项
---

按 `iterations/sprint-xxx/` 索引，**依次**对 Sprint 内 OpenSpec Change 执行 `/opsx-apply` 等价流程：读取进度、跳过已完成、尊重依赖与优先级、blocked 时暂停并汇报。

**本命令解决的核心问题**：

1. Sprint 含多个 Change，手动逐个 `/opsx-apply` 易漏项、顺序错乱（如 `fix-*` 早于父 `add-*` archive）
2. `openspec list` 只看单 change，不知 Sprint 全貌与「下一个该做谁」
3. 已 archive / tasks 全 `[x]` 的 change 仍被重复打开
4. 并行窗口（无依赖冲突）需显式提示，避免 Agent 乱序开发

---

**Input**：`sprint-002` 或 `sprint-002` 省略前缀（默认当前唯一 `in_progress` Sprint 时可推断）

可选 flags（用户可在同一条消息中说明）：

| Flag | 含义 |
|------|------|
| `--dry-run` | 只输出 Sprint Queue Report，不写 `src/`、不改 tasks |
| `--stop-after-one` | 完成当前一个 change 的全部 pending tasks 或遇 blocked 即停 |
| `--change <change-id>` | 仅处理指定 change（仍校验其在 Sprint 内且依赖已满足） |
| `--skip-archive-prompt` | change 全完成后直接建议 archive，不自动执行 `/opsx-archive` |
| `--parallel` | 输出可并行 change 分组，本命令仍**串行**执行第一个；并行需用户开多会话 |
| `--force-req-check` | 对每个 REQ 重新跑 Readiness（缺文档则跳过并告警） |

**Output**：Sprint Queue Report → 逐 change 实现进度 → Sprint 进度摘要；必要时更新 `acceptance-report.md` 中 OpenSpec Tasks 完成度。

---

## 前置关系

```text
/sprint-propose [sprint-xxx]     ← 创建迭代四件套
        │
        ▼
iterations/sprint-xxx/sprint.yaml   ← changes[] 机器索引
iterations/sprint-xxx/sprint.md     ← 依赖树、优先级、里程碑
        │
        ├─ /sprint-explore            ← 可选：范围/依赖/容量探讨
        ├─ /req-opsx / /bug-opsx       ← Change 未创建时先补
        ▼
/sprint-apply sprint-xxx            ← 编排 + 串行 opsx-apply
        │
        ├─ /opsx-apply <change>
        └─ /sprint-archive sprint-xxx ← 批量 opsx-archive + 关闭 Sprint
```

**禁止**：绕过 OpenSpec Change 直接改 `src/`（见 AGENTS.md §5）。

---

## Step 0 — 必须读取

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/document-governance.md   # sprint 四件套
rules/directory-structure.md
```

Sprint 目录（MUST 四件套齐全，缺一则 **Not Ready**，停止并提示 `/sprint-propose` 或补文件）：

```text
iterations/<sprint-id>/sprint.yaml
iterations/<sprint-id>/sprint.md
iterations/<sprint-id>/release-note.md
iterations/<sprint-id>/acceptance-report.md
```

CLI 现状：

```bash
openspec list --json
```

对每个 `sprint.yaml` 中的 `changes[]` 项，若目录仍在 `openspec/changes/<id>/`：

```bash
openspec status --change "<id>" --json
openspec instructions apply --change "<id>" --json
```

---

## Step 1 — 解析 Sprint 与 Change 状态

从 `sprint.yaml` 读取：

```yaml
sprint_id
status          # planning | in_progress | completed
requirements[]
bugs[]
changes[]
```

对每个 `changes[]` 条目构建 **ChangeStatus**：

| 字段 | 来源 |
|------|------|
| `change_id` | sprint.yaml |
| `req_id` | sprint.md Scope 表或 change proposal Why 链接 |
| `priority` | sprint.md Scope 表 P0/P1；缺省 P1 |
| `archived` | 存在 `openspec/changes/archive/*/<change_id>/` 或不在 active list |
| `artifacts_complete` | `openspec status --change` 全 done |
| `tasks_total` / `tasks_done` | `openspec list --json` 或 `instructions apply` |
| `state` | `done` \| `in_progress` \| `not_started` \| `blocked` \| `archived` |
| `blocked_reason` | artifacts 缺 / REQ Not Ready / 依赖未满足 |

**Skip 规则**（满足任一即 **跳过**，不调用 apply）：

1. `archived === true`
2. `tasks_done === tasks_total` 且 `tasks_total > 0`（提示用户 `/opsx-archive`）
3. `sprint.yaml` 中 change 不在磁盘且已在 archive（同上）

**Blocked 规则**（不满足则不可进入 apply，排队靠后）：

1. 关联 REQ/BUG `status ∉ { approved, in_sprint }` → `blocked: not_reviewed`（提示 `/req-review` 或 `/bug-review`）
2. `openspec status` 有 artifact 非 done → `blocked: artifacts`
3. 关联 REQ Readiness 为 Not Ready → `blocked: req_docs`（`--force-req-check` 时严格）
4. **依赖未满足**（见 Step 2）

---

## Step 2 — 依赖解析与排队（Topological Sort）

### 2.1 依赖来源（按优先级）

1. **`sprint.md` §依赖**  ASCII 树（MUST 解析）— 子节点依赖父路径上所有 change
2. **`sprint.md` Scope 表**「说明」列显式「依赖 REQ-xxxx / add-*」
3. **Change proposal/design** 中 `Depends on` / 父 REQ（如 fix-* 依赖 add-*）
4. **`sprint.yaml` `changes[]` 顺序** — 仅作同层 tie-break，**不得**覆盖显式依赖

### 2.2 优先级排序（同层可并行）

```text
P0 > P1 > P2
同优先级：sprint.yaml changes[] 声明顺序
fix-* 同父 add-*：add-* 必须先 done/archived，fix-* 才可 apply
```

### 2.3 并行提示（`--parallel` 或 Queue Report 末尾）

无依赖边相连的 change 可标记 `parallel_group`；输出示例：

```text
可并行（建议多 Agent 会话）：
  - add-login-remember-autofill
  - add-brand-management
  - add-tile-category-management
串行约束：
  - add-user-management → fix-user-management-list-refine
```

本命令默认 **串行** 处理队列中第一个 `eligible` change；`--parallel` 不自动多进程。

### 2.4 可选增强（非必须）

若未来 `sprint.yaml` 扩展：

```yaml
changes:
  - id: fix-user-management-list-refine
    depends_on: [add-user-management]
    priority: P1
```

则 **MUST** 优先于 prose 依赖树。

---

## Step 3 — Sprint Queue Report（MUST 先输出）

在任何代码修改前，输出：

```markdown
## Sprint Queue Report

**Sprint:** sprint-002
**Status:** in_progress
**Mode:** apply | dry-run

| # | Change | REQ | P | Tasks | State | Deps OK | Action |
|---|--------|-----|---|-------|-------|---------|--------|
| 1 | add-admin-home | REQ-0004 | P0 | 25/25 | archived | ✓ | SKIP |
| 2 | add-user-management | REQ-0005 | P0 | 31/36 | in_progress | ✓ | **APPLY NEXT** |
| 3 | fix-user-management-list-refine | ... | P1 | 0/20 | not_started | ✗ | WAIT (add-user-management) |
...

**Next action:** /opsx-apply add-user-management（via sprint-apply）
**Parallel hint:** add-login-remember-autofill, add-brand-management, ...
```

`--dry-run` 到此 **停止**。

---

## Step 4 — 执行循环（嵌入 /opsx-apply）

对队列中第一个 `Action === APPLY NEXT` 的 change（或 `--change` 指定且 eligible）：

1. 宣告：`Using change: <name> (sprint-apply orchestration)`

2. 执行 `/opsx-apply` 等价步骤（见 `.cursor/commands/opsx-apply.md`）：
   - `openspec status --change "<name>" --json`
   - `openspec instructions apply --change "<name>" --json`
   - 读取 `contextFiles` 全部路径
   - 仅处理 **pending** tasks（`- [ ]`）
   - 每完成一项即标记 `- [x]`

3. **Pause 条件**（停在本 change，不自动切下一个）：
   - 任务描述不清
   - 实现暴露 design/spec 问题 → 建议更新 artifacts
   - 测试/构建失败需人工决策
   - `--stop-after-one` 且本 change 无剩余 pending task
   - 用户中断

4. **本 change 全部 tasks `[x]`**：
   - 输出：建议 `/opsx-archive <change-id>` 或 Sprint 收尾时用 `/sprint-archive sprint-xxx`
   - **不自动 archive**（除非用户在同一条消息明确要求）
   - 更新 `iterations/<sprint-id>/acceptance-report.md` 对应 change 任务组完成度
   - 若无 `--stop-after-one`，重新跑 Step 1–3，继续下一个 eligible change

5. **Sprint 全部 change done/archived**：
   - 输出 Sprint Complete 摘要
   - 提示更新 `sprint.yaml` `status: completed`（仅用户确认后改）
   - 提示填写 `acceptance-report.md` 验收结论

---

## Step 5 — REQ Readiness Gate（`--force-req-check` 或 change 首次 apply 前）

对 change 关联的 `issues/requirements/<REQ-ID>/`：

| 文件 | 必须 |
|------|------|
| requirement.md | ✓ |
| acceptance.md | ✓ |
| trace.md | ✓ |
| user-stories.md | 推荐 |
| business-flow.md | 推荐 |

**Not Ready** → 该 change 标记 `blocked: req_docs`，跳过并建议 `/req-complete` 或 `/req-opsx`。

UI 类额外检查：`prototype/web/*.html` 存在但无 strategy 且 design 标 `Pending` → 建议 `/opsx-explore`。

---

## Step 6 — 追溯更新

每完成一个 change 的 apply 阶段（非 archive）：

- 更新 `iterations/<sprint-id>/acceptance-report.md` OpenSpec Tasks 表
- 若 REQ `trace.md` 含 `openspec_changes[].status`，改为 `applied`（archive 后改为 `archived`）

---

## Step 7 — 输出模板

### 单 Change 会话结束

```text
## Sprint Apply — Paused / Progress

**Sprint:** sprint-002
**Current change:** add-user-management
**Change progress:** 34/36 tasks
**Sprint progress:** 2/6 changes complete (1 archived, 1 in progress)

### Completed this session
- [x] 7.1 ...
- [x] 7.2 ...

### Next steps
1. 继续：`/sprint-apply sprint-002` 或 `/opsx-apply add-user-management`
2. 若 36/36： `/opsx-archive add-user-management` 后再 `/sprint-apply sprint-002`
```

### Sprint 全部 eligible 已处理

```text
## Sprint Apply — Queue Exhausted

**Sprint:** sprint-002
**Archived / Done:** add-admin-home, add-user-management, ...
**Waiting on deps:** fix-user-management-list-refine (needs add-user-management archive)
**Blocked:** add-tile-category-management (REQ Partially Ready)

Run `/sprint-apply sprint-002 --dry-run` to refresh queue.
```

---

## Guardrails

| 规则 | 说明 |
|------|------|
| 先 Report 后代码 | MUST 输出 Sprint Queue Report；`--dry-run` 不得改 src |
| 不跳过依赖 | fix-* / 子 REQ 不得早于父 change archive（或 tasks 全完） |
| 不自动 archive | 全完成后 **建议** `/opsx-archive`，不默认执行 |
| 不并行写同一 change | 单会话串行；并行由用户开多 Agent |
| 不替代 opsx-apply | 编排层；单 change 实现逻辑与 opsx-apply 一致 |
| 不绕过 OpenSpec | 无 change 目录 → 告警 `/req-opsx`，不直接开发 |
| Sprint 外 change | 不在 `sprint.yaml` 的 change **不得**被本命令 apply |
| 容量告警 | 若连续 3 个 change blocked，输出风险摘要并停止 |

---

## 示例：sprint-002

```text
/sprint-apply sprint-002 --dry-run
```

期望 Queue（示意，以 CLI 实时为准）：

```text
SKIP     add-admin-home          (archived)
APPLY    add-user-management     (31/36)
WAIT     fix-user-management-list-refine → depends add-user-management
ELigible add-login-remember-autofill     (parallel)
ELigible add-brand-management            (parallel)
ELigible add-tile-category-management   (parallel, check REQ readiness)
```

开始开发：

```text
/sprint-apply sprint-002 --stop-after-one
```

仅收尾 user-management 后暂停 → archive → 再：

```text
/sprint-apply sprint-002
```

---

## 参考

- 单 Change 实现：`.cursor/commands/opsx-apply.md`
- 单 Change 归档：`.cursor/commands/opsx-archive.md`
- Sprint 创建：`.cursor/commands/sprint-propose.md`
- Sprint 探索：`.cursor/commands/sprint-explore.md`
- Sprint 批量归档：`.cursor/commands/sprint-archive.md`
- REQ → Change：`.cursor/commands/req-opsx.md`
- Sprint 治理：`rules/document-governance.md` §4.1
- 流程总览：`AGENTS.md` §4.1
