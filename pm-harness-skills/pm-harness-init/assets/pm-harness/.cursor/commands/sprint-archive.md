---
name: /sprint-archive
id: sprint-archive
category: Workflow
description: 批量归档 Sprint 内所有 OpenSpec Change，并关闭迭代（类似 /opsx-archive 面向整迭代）
---

对 `iterations/sprint-xxx/` 中 `sprint.yaml` 列出的 **全部 OpenSpec Change** 依次执行 `/opsx-archive` 等价流程：检查完成度、同步 delta spec、移入 `openspec/changes/archive/`。迭代验收文档一并收尾。

与 `/opsx-archive` 对标：**单 Change** 用 opsx-archive，**整 Sprint** 用 sprint-archive。

---

**Input**：`sprint-002`（必填或可推断唯一 `in_progress` Sprint）

可选 flags：

| Flag | 含义 |
|------|------|
| `--dry-run` | 只输出 Archive Queue Report，不移动目录、不 sync spec |
| `--change <change-id>` | 仅归档 Sprint 内指定 change |
| `--force` | 对 incomplete tasks/artifacts 仍继续（须用户确认每项） |
| `--skip-sync` | 不同步 delta spec 到 `openspec/specs/`（不推荐） |
| `--no-sprint-close` | 只归档 change，不把 `sprint.yaml` 标为 completed |

---

## 前置关系

```text
/sprint-apply 完成各 change tasks
        │
        ▼
/sprint-archive sprint-xxx    ← 本文
        │
        ├─ （内嵌）/opsx-archive 等价步骤 × N
        ├─ 更新 acceptance-report.md
        └─ sprint.yaml status: completed
```

**禁止**：在 tasks 大量未完成时默认 `--force` 归档（须显式确认）。

---

## Step 0 — 必须读取

```text
AGENTS.md
rules/document-governance.md
rules/directory-structure.md
```

```text
iterations/<sprint-id>/sprint.yaml
iterations/<sprint-id>/sprint.md          # 依赖树 → 归档顺序
iterations/<sprint-id>/acceptance-report.md
```

```bash
openspec list --json
```

---

## Step 1 — 构建 Archive Queue

对 `sprint.yaml` 的 `changes[]` 每项：

| 字段 | 判定 |
|------|------|
| `archived` | 已在 `openspec/changes/archive/*/<id>/` |
| `artifacts_done` | `openspec status --change <id> --json` 全 done |
| `tasks_incomplete` | `tasks.md` 中 `- [ ]` 计数 |
| `has_delta_specs` | `openspec/changes/<id>/specs/` 非空 |
| `deps_ok_for_archive` | 子 change（fix-*）可在父 add-* 之后；见 Step 2 |

**Skip**：已 archived。

**Block**（默认不归档，除非 `--force` + 确认）：

- `tasks_incomplete > 0`
- artifacts 非 done
- 依赖链上仍有未 archive 的**子** change 需先于父？→ 实际：**fix 应在 add 之后 archive**；顺序见 Step 2

---

## Step 2 — 归档顺序（Topological Sort）

与 `/sprint-apply` **相同依赖树**，但方向为「子节点先 archive 还是父节点先？」：

**推荐顺序**（与 spec 合并逻辑一致）：

1. **先 archive 基础 add-***（扩展主 spec）
2. **再 archive fix-*** / update-*（MODIFIED 已存在 requirement）
3. 无依赖关系的 change 按 `sprint.yaml` 顺序

解析来源：`sprint.md` §依赖 ASCII 树（与 sprint-apply 一致）。

---

## Step 3 — Archive Queue Report（MUST 先输出）

```markdown
## Sprint Archive Queue Report

**Sprint:** sprint-002
**Mode:** archive | dry-run

| # | Change | Tasks | Artifacts | Delta Specs | Archived | Action |
|---|--------|-------|-----------|-------------|----------|--------|
| 1 | add-admin-home | 25/25 | ✓ | yes | ✓ | SKIP |
| 2 | add-user-management | 36/36 | ✓ | yes | ✗ | **ARCHIVE NEXT** |
| 3 | fix-user-management-list-refine | 20/20 | ✓ | yes | ✗ | QUEUE |
...

**Warnings:** fix-* 依赖 add-user-management 已 archive
**Blocked:** add-brand-management (5 incomplete tasks) — 需 --force 或先 /opsx-apply
```

`--dry-run` 到此停止。

---

## Step 4 — 逐 Change 执行（嵌入 /opsx-archive）

对每个 `Action === ARCHIVE NEXT` 的 change，执行 `.cursor/commands/opsx-archive.md` 等价步骤：

1. `openspec status --change "<name>" --json`
2. 读 `tasks.md` 统计 incomplete；有则警告（`--force` 可继续）
3. **Delta spec 评估**：对比 `openspec/changes/<name>/specs/` 与 `openspec/specs/`
4. 若需 sync 且非 `--skip-sync`：
   ```bash
   openspec archive "<name>" -y
   ```
   若 CLI 不可用，按 opsx-archive 手动：
   ```bash
   mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
   ```
   并确保 delta 已合并到 `openspec/specs/`（归档前 MUST 自检 MODIFIED 标题存在）
5. 更新关联 REQ/BUG `trace.md`：
   - `openspec_changes[].status: archived`
   - 验收完成时 REQ/BUG `status: done`（若 acceptance 已勾选）

**Pause 条件**：

- delta spec MODIFIED 标题与主 spec 不一致 → **停止整 Sprint 归档**，报告修复方式
- archive 目标目录已存在 → 跳过该项并记录
- 用户中断

---

## Step 5 — 关闭 Sprint（除非 `--no-sprint-close`）

全部 change archived 或用户确认接受遗留 blocked 项后：

1. **`sprint.yaml`**：`status: completed`
2. **`acceptance-report.md`**：填写验收结论、日期、验收人（模板节）
3. **`release-note.md`**：`status: published`（或 draft → published）
4. **`sprint.md`**：note 更新为 Sprint 已关闭

若仍有 blocked change：**不得**自动标 completed；报告遗留清单。

---

## Step 6 — 输出模板

### 成功

```text
## Sprint Archive Complete

**Sprint:** sprint-002
**Changes archived:** 5/5
**Specs synced:** 4（1 skipped: no delta）
**Sprint status:** completed

### Archived
- add-user-management → archive/2026-06-28-add-user-management/
- fix-user-management-list-refine → ...
...

### Updated
- iterations/sprint-002/sprint.yaml
- iterations/sprint-002/acceptance-report.md
- issues/requirements/*/trace.md (N files)
```

### 部分失败

```text
## Sprint Archive Paused

**Archived:** 3/6
**Blocked:** add-brand-management (12 incomplete tasks)
**Failed:** fix-user-management-list-refine (MODIFIED title mismatch)

**Next:**
1. 完成剩余 tasks → /sprint-apply sprint-002
2. 修复 delta spec → 重试 /sprint-archive sprint-002 --change fix-user-management-list-refine
```

---

## Guardrails

| 规则 | 说明 |
|------|------|
| 先 Report | MUST 输出 Archive Queue Report |
| 顺序 | fix-* 不得早于父 add-* archive（除非主 spec 已含父能力） |
| 不猜 change | 只归档 `sprint.yaml` 列出的 change |
| 不自动 force | incomplete tasks 默认 block |
| delta 自检 | MODIFIED 标题 MUST 存在于 `openspec/specs/` |
| Sprint 外 change | 不得归档 |
| 不写 src | 本命令只归档 spec 与 move 目录 |

---

## 示例

```text
/sprint-archive sprint-002 --dry-run
/sprint-archive sprint-002
/sprint-archive sprint-002 --change add-user-management
/sprint-archive sprint-002 --force    # 仅在团队确认后
```

---

## 参考

- 单 Change 归档：`.cursor/commands/opsx-archive.md`
- 开发编排：`.cursor/commands/sprint-apply.md`
- Sprint 创建：`.cursor/commands/sprint-propose.md`
- 治理：`rules/document-governance.md` §4.2
- AGENTS.md §4.1 Sprint 命令族
