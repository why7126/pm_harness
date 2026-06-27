---
description: Sprint 经验复盘 - 汇总迭代过程、需求/BUG/开发经验并沉淀到知识库
created_at: 2026-06-27 10:45:00
updated_at: 2026-06-27 10:45:00
---

对整个 Sprint 做经验复盘，把可复用的流程、需求设计、文档质量、开发实现、BUG 预防、组件抽象和协作改进沉淀到 `docs/knowledge-base/`。本命令面向“以后怎么做得更好”，不是归档、不是开发、不是改范围。

**Input**：`sprint-0002`（必填或可推断唯一 `completed` / `in_progress` Sprint）

可选 flags：

| Flag | 含义 |
|------|------|
| `--dry-run` | 只输出复盘报告草稿，不写知识库文件 |
| `--focus process,requirements,docs,dev,bugs,components,testing` | 指定复盘重点 |
| `--include-open-items` | 把未完成改进项写入 Action Items |
| `--output <path>` | 指定输出文件；默认 `docs/knowledge-base/sprints/YYYY-MM-DD-<sprint-id>-experience.md` |

**Output**：一份 Sprint 经验沉淀文档，默认路径：

```text
docs/knowledge-base/sprints/YYYY-MM-DD-<sprint-id>-experience.md
```

**禁止**：写 `src/`、修改 OpenSpec Change、修改 Sprint Scope、勾选 tasks、创建或推进需求/BUG 状态。

---

## Step 0 — 必须读取

```text
AGENTS.md
rules/document-governance.md
rules/requirement-management.md
rules/bug-management.md
rules/testing.md
rules/directory-structure.md
```

Sprint 四件套：

```text
iterations/<sprint-id>/sprint.yaml
iterations/<sprint-id>/sprint.md
iterations/<sprint-id>/acceptance-report.md
iterations/<sprint-id>/release-note.md
```

关联材料（按 `sprint.yaml` 索引读取）：

```text
issues/requirements/{plan,review,archive}/<REQ-ID>/**
issues/bugs/{plan,review,archive}/<BUG-ID>/**
openspec/changes/<change-id>/**
openspec/changes/archive/**/<change-id>/**
docs/knowledge-base/**
```

允许只读扫描实现与测试，以支撑“重复 BUG 预防”和“组件/服务抽象”判断：

```text
src/**
tests/**
docs/standards/**
```

只读扫描不得修改业务代码、测试代码或 OpenSpec artifacts。

---

## Step 1 — Sprint Experience Source Map（MUST）

先输出来源地图，说明本次复盘基于哪些事实：

| 维度 | 来源 | 检查点 |
|------|------|--------|
| 范围与目标 | `sprint.yaml`、`sprint.md` | 目标是否清晰、范围是否稳定、是否存在临时插入 |
| 验收与发布 | `acceptance-report.md`、`release-note.md` | 验收是否可执行、发布说明是否可追踪 |
| 需求设计 | REQ 六件套、trace、prototype | 文档是否完整、验收是否明确、评审是否有效 |
| BUG 与回归 | BUG 包、root-cause、acceptance、trace | 重复问题、遗漏测试、预防措施 |
| 开发实现 | OpenSpec proposal/design/tasks/specs | 方案是否充分、任务拆分是否合理、抽象是否复用 |
| 代码与组件 | `src/**` 只读扫描 | 重复 UI/API/service/schema/hook/helper 是否可抽象 |
| 测试与质量 | test-plan、acceptance、CI/本地验证记录、`tests/**` 只读扫描 | 覆盖缺口、测试债务、质量门禁 |
| 知识沉淀 | `docs/knowledge-base/**` | 是否已有相关经验，避免重复沉淀 |

若关键文件缺失，仍可复盘，但必须在报告中列出“证据缺口”。

---

## Step 2 — 复盘分析维度（MUST）

至少覆盖以下维度；可按 `--focus` 缩小，但不得跳过显著风险。

### 2.1 迭代流程

- Sprint 目标是否可衡量，范围是否适合迭代周期。
- `/sprint-propose`、`/sprint-explore`、`/sprint-apply`、`/sprint-archive` 的顺序是否合理。
- 是否出现未评审项、范围漂移、依赖识别滞后、容量估算偏差。
- 哪些流程应前移、自动化或加门禁。

### 2.2 需求设计与需求文档

- `requirement.md` 是否把用户、目标、范围、非目标讲清。
- `acceptance.md` 是否可测试、可验收、可追踪。
- `business-flow.md`、`user-stories.md`、prototype 是否足够支撑开发。
- 多个需求是否存在可抽象的业务模型、共享流程、通用组件或统一 API。
- 哪些模板字段、评审问题、Readiness 规则需要优化。

### 2.3 开发阶段与技术实现

- OpenSpec proposal/design/tasks 是否帮助减少返工。
- tasks 拆分是否过粗或过细，是否遗漏测试、迁移、兼容、回滚。
- 多个需求中重复出现的 UI、API、服务、数据访问或校验逻辑，是否应抽象为组件、hook、service、schema、fixture 或测试 helper。
- 若发现重复实现，必须列出证据路径和抽象边界建议；不得直接改代码。
- 是否出现跨 Change 冲突、依赖顺序错误、重复实现或过度耦合。

### 2.4 BUG、质量与预防

- 多次出现或同类出现的 BUG 是什么。
- 根因属于需求不清、设计遗漏、实现习惯、测试缺口、环境差异、数据兼容还是发布流程。
- 后续如何避免：新增验收项、测试用例、静态检查、组件封装、代码模板、review checklist、监控告警或知识库条目。

### 2.5 协作与工具链

- Agent 命令是否足够清晰，是否有重复手工同步。
- Workflow Sync、OpenSpec CLI、测试命令、截图/日志等工具链是否顺畅。
- 哪些命令说明、规则文档、模板需要更新。

---

## Step 3 — 生成经验条目

为每条经验生成结构化记录：

```markdown
### EXP-<NN> <经验标题>

- **类型**：process | requirement | docs | dev | bug-prevention | component | testing | tooling
- **证据**：关联 REQ/BUG/Change/Sprint 文档
- **观察**：发生了什么
- **根因**：为什么会发生
- **经验**：下次应如何处理
- **行动项**：可执行改进，含 owner/建议时机（未知则 `待确认`）
- **沉淀位置**：规则、模板、组件、测试、知识库或后续需求
```

经验必须来自证据或明确标记为推断；不得编造不存在的问题。

---

## Step 4 — 输出知识库文档

`--dry-run` 时只输出草稿，不写文件。

默认创建目录和文件：

```text
docs/knowledge-base/sprints/YYYY-MM-DD-<sprint-id>-experience.md
```

文档模板：

```markdown
---
title: <sprint-id> 经验复盘
purpose: 沉淀 Sprint 流程、需求、开发、BUG 与组件抽象经验
source: /sprint-exps
sprint_id: <sprint-id>
created_at: YYYY-MM-DD hh:mm:ss
updated_at: YYYY-MM-DD hh:mm:ss
---

# <sprint-id> 经验复盘

## 1. Sprint 概览

| 项 | 内容 |
| --- | --- |
| Sprint | <sprint-id> |
| 状态 | planning / in_progress / completed |
| 需求 | ... |
| BUG | ... |
| Change | ... |

## 2. 证据与缺口

## 3. 核心经验

## 4. 需求与文档改进

## 5. 开发与组件抽象

## 6. BUG 预防与质量门禁

## 7. 流程与工具链优化

## 8. 行动项

| Action | 类型 | 建议落点 | Owner | 时机 |
| --- | --- | --- | --- | --- |

## 9. 后续同步建议

- 是否需要更新 rules / templates / command docs。
- 是否需要创建新的 REQ/BUG/OpenSpec Change。
- 是否需要新增组件、测试 helper、review checklist 或 CI gate。
```

---

## Step 5 — 输出总结

```text
## Sprint Experience Complete

**Sprint:** sprint-xxx
**Knowledge Base:** docs/knowledge-base/sprints/YYYY-MM-DD-sprint-xxx-experience.md
**Experiences:** N
**Action Items:** M

### Suggested follow-up
1. ...
```

---

## Guardrails

| 规则 | 说明 |
|------|------|
| 基于证据 | 先读 Sprint、REQ、BUG、Change、验收与发布资料 |
| 不写代码 | 只沉淀经验，不修改 `src/` |
| 不改范围 | 不修改 `sprint.yaml` Scope、不新增 Change、不勾选 tasks |
| 不替代事故复盘 | 线上事故仍应单独沉淀到 `docs/knowledge-base/incidents/` |
| 可产生改进建议 | 规则、模板、组件、测试、CI 的改进只作为行动项列出 |
| 避免重复沉淀 | 写入前检查已有 `docs/knowledge-base/**` 相关条目 |

---

## Final Step — Workflow Sync (MUST)

Run the shared `workflow-sync` step before reporting this command as complete:

```bash
python scripts/sync-workflow-status.py --event sprint.exps --sprint "<sprint-id>"
```

If the script exits non-zero, read the drift report, fix inconsistent workflow documents if this command changed them, rerun the sync, and include the final `## Workflow Sync` report in the command output.
