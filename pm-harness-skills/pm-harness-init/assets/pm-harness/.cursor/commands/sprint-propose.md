---
name: /sprint-propose
id: sprint-propose
category: Workflow
description: 提议并创建新 Sprint 迭代规划（四件套），类似 /opsx-propose 面向整迭代
---

根据当前项目中的需求（Requirement）、缺陷（Bug）和 OpenSpec Change，**提议并创建**新的 Sprint（迭代）规划。与 `/opsx-propose` 对标：单 Change 用 opsx，**整迭代**用 sprint。

**Input**：

- `sprint-003` — 指定 Sprint ID（推荐）
- 或自然语言描述本迭代目标（如「下一 Sprint 做品牌+类目+登录增强」），由 Agent 推导 `sprint-xxx` 编号

可选 flags：

| Flag | 含义 |
|------|------|
| `--req REQ-xxxx,...` | 仅纳入列出的需求 |
| `--change add-*,...` | 仅纳入列出的 Change |
| `--duration 2w` | 迭代周期（默认 2 周） |
| `--dry-run` | 只输出提议范围与估算，不写文件 |

**Output**：`iterations/sprint-xxx/` 四件套 + 各 REQ/BUG/Change trace 更新 + 提示下一步 `/sprint-explore` 或 `/sprint-apply`。

---

## 前置关系

```text
issues/requirements/** 、issues/bugs/** 、openspec/changes/**
        │
        ▼
/sprint-propose [sprint-xxx]     ← 本文：创建迭代规划
        │
        ├─ /sprint-explore         ← 范围/依赖/容量探讨（可选）
        ├─ /req-opsx / /bug-opsx       ← 缺 Change 时补建
        ├─ /sprint-apply           ← 开发
        └─ /sprint-archive         ← 迭代结束批量归档
```

---

## Step 0 — 必须读取

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/document-governance.md
rules/requirement-management.md
rules/bug-management.md
rules/directory-structure.md
```

扫描范围：

```text
project.yaml                    # 若存在：团队容量
issues/requirements/**
issues/bugs/**
openspec/changes/**             # 含 archive/
openspec list --json
iterations/**                   # 避免 sprint 编号冲突
```

---

## Step 1 — 输入与编号

1. 若无 Sprint ID：扫描 `iterations/` 取最大编号 +1 → `sprint-xxx`。
2. 若 `iterations/sprint-xxx/` 已存在：询问 **继续填充** 还是 **换编号**。
3. 若用户给自然语言目标：列出候选 REQ/BUG/Change，用 **AskUserQuestion** 确认纳入范围。

---

## Step 2 — 纳入前检查

### 评审门禁（MUST — 新 Sprint 严格执行）

纳入 `sprint.yaml` 的 **requirements[]** / **bugs[]** 每项：

```text
issues/requirements/<REQ>/trace.md  → status ∈ { approved, in_sprint }
issues/bugs/<BUG>/trace.md        → status ∈ { approved, in_sprint }
```

**未评审**（`draft`、`pending_review`、`captured` 等）→ **不得**写入 `sprint.yaml`；记入 `sprint.md`「延后项」，提示 `/req-review` 或 `/bug-review`。

**历史 Sprint 回填**（如 sprint-002 已含 draft REQ）：输出 **WARN**，建议补 `review.md` + `--approve`；不自动剔除。

**优先级**：P0 BUG > P0 REQ > P1 …

### Requirement（文档条件）

```text
requirement.md、acceptance.md、trace.md 已存在
status: approved（见上节门禁）
```

**Not Ready** → 不纳入 `sprint.yaml`，写入 sprint.md「延后项」并建议 `/req-complete`。

### Bug

```text
bug.md、root-cause.md、acceptance.md 已存在
状态：Open | Ready
```

### OpenSpec Change

```text
openspec/changes/<id>/ 存在且含 proposal、design、tasks
或用户确认先纳入 REQ，Change 待 `/req-opsx`
```

已 **archive** 的 change **不得**纳入新 Sprint（除非 fix-* 续作，须新建 change）。

---

## Step 3 — 容量与工作量

读取 `project.yaml`（若不存在则默认）：

```yaml
capacity:
  developers: 2
  testers: 1
duration: 2周
```

估算标准（与历史 sprint 一致）：

```text
XS=0.5  S=1  M=3  L=5  XL=8  XXL=13 人天
```

按前端 / 后端 / 测试分列；汇总 `estimated_story_points` 与 `estimated_person_days`。

---

## Step 4 — 优先级、依赖与归组

**优先级**：P0 BUG → P0 REQ → P1 REQ → P2 …

**依赖**（MUST 写入 `sprint.md` §依赖 ASCII 树）：

- 从 requirement 父子关系、change proposal、Admin Shell 等基座推导
- fix-* **MUST** 挂在对应 add-* 之下

**归组**：同一业务域（如 Tile Management）尽量同一 Sprint。

---

## Step 5 — 创建四件套（`--dry-run` 跳过）

目录：

```text
iterations/sprint-xxx/
├── sprint.yaml          # MUST 机器可读事实源
├── sprint.md            # 人类可读展开
├── release-note.md      # 发布说明初稿
└── acceptance-report.md # 验收报告模板
```

### sprint.yaml（MUST）

```yaml
sprint_id: sprint-xxx
status: planning          # 启动开发后改为 in_progress
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD

capacity:
  developers: <int>
  testers: <int>

requirements: []          # issues/requirements 目录名
bugs: []
changes: []               # openspec change id

estimated_story_points: <int>
estimated_person_days: <number>
```

### sprint.md（MUST 含）

- Sprint 目标
- Scope 表（REQ / BUG / Change + 优先级 + 状态）
- 工作量估算表
- 里程碑
- 风险
- **依赖** ASCII 树
- 发布计划
- 关联文档链接

### release-note.md / acceptance-report.md

按 `rules/document-governance.md` §4.1 模板生成初稿。

---

## Step 6 — 更新 Trace

对纳入的每项更新：

```text
issues/requirements/*/trace.md   → iteration: sprint-xxx
issues/bugs/*/trace.md
openspec/changes/*/trace.md      # 若 change 已存在
```

---

## Step 7 — 输出

```text
## Sprint Propose 完成

**Sprint:** sprint-xxx
**Status:** planning
**Requirements:** N
**Changes:** M
**Estimated:** XX SP / YY 人天

**Artifacts:**
- [x] sprint.yaml
- [x] sprint.md
- [x] release-note.md
- [x] acceptance-report.md

**Next:**
1. `/sprint-explore sprint-xxx` — 探讨依赖/容量/风险（可选）
2. 缺 Change 的 REQ → `/req-opsx REQ-xxxx`（须 approved）
3. `/sprint-apply sprint-xxx --dry-run` — 查看开发队列
4. `/sprint-apply sprint-xxx` — 开始开发
```

---

## Guardrails

| 规则 | 说明 |
|------|------|
| 四件套缺一不可 | 不得只写 sprint.md |
| 不得绕过 OpenSpec | 新能力须先 REQ + Change，再纳入 sprint |
| 编号唯一 | 不覆盖已有 sprint 目录（除非用户确认续写） |
| 容量透明 | 超容量须在 sprint.md 风险表标注 |
| 不写 src | 本命令只建迭代文档，实现用 `/sprint-apply` |

---

## 参考

- 原 `create-iteration` 逻辑已合并至本文
- Sprint 治理：`rules/document-governance.md` §4.1
- 单 Change 提议：`/opsx-propose`
- 开发编排：`/sprint-apply`
- 批量归档：`/sprint-archive`
