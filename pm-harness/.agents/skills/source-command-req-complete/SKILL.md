---
name: "source-command-req-complete"
description: "需求完善 - 基于 requirement.md 补齐六件套（不含 OpenSpec）"
---

# source-command-req-complete

Use this skill when the user asks to run the migrated source command `req-complete`.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 检索先定位再分段读取；大范围 `rg/find` 默认排除 Harness、模板 assets、历史 agent 目录、archive、generated、node_modules、dist、coverage。
- 命令输出优先 `max_output_tokens <= 8000`；大 diff、OpenAPI/Orval 生成物、测试日志、Workflow Sync 输出先给摘要或命中数。


## Command Template

替代原 `/requirement-to-change` 的**文档部分**。不创建 `openspec/changes/`。

**Input**：`REQ-xxxx`（须存在 `requirement.md`）

**Output**：user-stories、business-flow、acceptance、trace（扩写）、prototype（UI 类）；Readiness Report + Knowledge-base Cross-cutting Report

---

## Step 0 — 读取

```text
AGENTS.md
rules/requirement-management.md
rules/ui-design.md          # UI 类
docs/knowledge-base/README.md
issues/requirements/<REQ-ID>/requirement.md
issues/requirements/<REQ-ID>/capture.md
```

### Step 0.1 — 知识库读库与 REQ 类型判定（MUST）

1. 根据 `requirement.md` / `capture.md` 判定本 REQ 涉及的 **UI 场景标签**（可多选）：

| 标签 | 触发条件（任一命中即选） |
|------|--------------------------|
| `admin-list` | 管理端 CRUD **列表页**、表格 + 分页 + 行内操作 |
| `admin-form` | 管理端**表单页/设置页**（非弹窗）、Tab 面板、页内保存 |
| `admin-modal` | 管理端**弹窗**新建/编辑（含宽弹窗 880px 类） |
| `media-upload` | 图片/视频/头像/Logo **上传**与回显 |

2. 按标签 **MUST** 读取对应 best-practices（路径均相对 `docs/knowledge-base/`）：

| 标签 | 文档 |
|------|------|
| `admin-list` | `best-practices/admin-list-page-consistency.md` |
| `admin-form` | `best-practices/admin-form-page-consistency.md` |
| `admin-modal` | `best-practices/admin-modal-width-css-cascade.md` |
| `media-upload` | `best-practices/admin-media-upload-chain.md` |

3. **SHOULD** 读取最近一期 `retrospectives/*-retrospective.md`，检索与本 REQ 同域的复发模式（列表/confirm/toast/上传等），写入 trace 变更记录摘要。

4. 输出 **Knowledge-base Cross-cutting Report**（表格：标签 / 引用文档 / 将写入 acceptance 的 AC 条数）。

5. **无匹配标签**（纯 API/后端/非 UI）：在 Report 注明「无横切 AC」；跳过 Step 1.1。

---

## Step 1 — 生成/补齐文档

| 文件 | 内容要点 |
|------|----------|
| `user-stories.md` | US-xxx、验收要点 |
| `business-flow.md` | 流程 ASCII、与父 REQ 差异 |
| `acceptance.md` | AC-xxx 可勾选清单 + **§横切 AC（knowledge-base）**（见 Step 1.1） |
| `trace.md` | 扩写 yaml、关联、变更记录；**MUST** 含 `knowledge_base_refs:` 列表 |
| `prototype/web/*` | UI 类：html、context.md；PNG 可标待导出 |

`status` → `enriching`（补齐中）→ 文档齐后 `pending_review`

### Step 1.1 — 横切 AC 嵌入 acceptance.md（MUST — 有 UI 标签时）

在 `acceptance.md` 末尾追加固定章节（不得与功能 AC 混编号，使用 **AC-XCUT-xxx**）：

```markdown
## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/<doc>.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 …（从 best-practices「验收 gate」逐条转化，措辞 MUST 可测试）
- [ ] AC-XCUT-002 …
```

**转化规则**：

| 来源文档 | MUST 写入的横切 AC 要点（至少） |
|----------|--------------------------------|
| `admin-list-page-consistency.md` | 分页 DOM 对齐用户管理基准；fixed toast 无 layout shift；状态变更 DS confirm；无 `window.confirm` |
| `admin-form-page-consistency.md` | 全页单保存 CTA（footer）；无页头重复保存；恢复默认/dirty 切换 DS modal；成功反馈 fixed toast |
| `admin-modal-width-css-cascade.md` | TSX 禁止 `modal-card` 与专属类并存；Computed width 验收；矮视口 body scroll |
| `admin-media-upload-chain.md` | 上传状态机 idle→uploading→done/failed；同会话即时回显；Docker `:3000` 边界文件验收 |

- 若 best-practices 某 gate 与本 REQ 无关（如无上传），**MUST** 在 AC 行注释 `N/A — <理由>`，不得删除整节。
- `design.md` 尚未创建时：在 `trace.md` `knowledge_base_refs` 列出文档路径，供后续 `/req-opsx` 写入 change design。

### trace.md 扩展字段示例

```yaml
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
cross_cutting_tags:
  - admin-list
  - admin-modal
```

---

## Step 2 — Readiness Report

| readiness | 条件 |
|-------------|------|
| Ready | 五件套齐（+ UI 有 prototype 策略）+ **有 UI 标签时 §横切 AC 已写入** |
| Partially Ready | 缺 PNG 等非阻塞；或横切 AC 已写但 best-practices 为 draft |
| Not Ready | 缺 acceptance 等；或有 UI 标签但缺 §横切 AC |

| knowledge-base gate | 条件 |
|---------------------|------|
| Pass | 所有命中标签的 best-practices 已读且 AC-XCUT 已转化 |
| N/A | 纯后端/API REQ |
| Fail | 有 UI 标签但未读库或未写 §横切 AC |

---

## Step 3 — 输出

```text
## Req Complete

**REQ:** REQ-xxxx
**Readiness:** Ready | Partially Ready | Not Ready
**Knowledge-base gate:** Pass | N/A | Fail
**Cross-cutting tags:** admin-list, admin-modal, …
**Refs:** docs/knowledge-base/best-practices/…

**Added AC-XCUT:** N 条（见 acceptance.md §横切 AC）

**Next:**
1. /req-review REQ-xxxx --approve
2. 通过后 /req-opsx REQ-xxxx（design.md MUST 引用 knowledge_base_refs）
3. 纳入 Sprint 前确认 sprint.md §横切预防清单 已覆盖本 REQ
```

## Guardrails

- 不写 `src/`、不 `openspec new change`
- 不替代 `/req-generate`（若无 requirement.md 先 generate）
- **不得跳过 Step 0.1**（UI 类 REQ）；不得省略 §横切 AC 仅写功能 AC
- 横切 AC **MUST NOT** 复制整份 best-practices 正文，只写可勾选、可测试条目 + 来源链接

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event req.complete --req <REQ-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- Print the summary **Workflow Sync Report** to the user; use `--output detail` only for debugging.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).
