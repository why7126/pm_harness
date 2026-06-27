---
description: 综合捕获 - 自动区分需求与 BUG，并路由到 req-capture / bug-capture 等价流程
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 10:30:00
---

用于用户只提供原始想法、反馈、会议纪要、客服记录或线上现象，且不确定应归为需求还是 BUG 的场景。命令先分析内容，再拆分并分别创建需求或缺陷的最小捕获记录。

**Input**：一句话、长文本、会议纪要、客户反馈、测试反馈、截图/日志路径说明。输入可同时包含多个需求和多个 BUG。

可选：

| Flag | 含义 |
|------|------|
| `--priority P0|P1|P2` | 默认应用到拆分出的需求 |
| `--severity blocker|critical|high|medium|low` | 默认应用到拆分出的 BUG |
| `--parent REQ-xxxx` | 默认应用到拆分出的需求 |
| `--dry-run` | 只输出分类与拆分计划，不创建文件 |

**Output**：

- 需求项：一个或多个 `issues/requirements/plan/REQ-NNNN-slug/capture.md` + `trace.md`，更新需求 `_registry.yaml`
- BUG 项：一个或多个 `issues/bugs/plan/BUG-NNNN-slug/capture.md` + `trace.md`，更新缺陷 `_registry.yaml`

**禁止**：创建 `requirement.md`、`bug.md`、写 `src/`、写 `openspec/`、写 Sprint 规划文件。

---

## Step 0 — 必须读取

```text
AGENTS.md
rules/requirement-management.md
rules/bug-management.md
issues/requirements/_registry.yaml
issues/bugs/_registry.yaml
```

---

## Step 1 — 内容分类（MUST）

先输出 **Capture Classification Report**，把输入拆成原子条目并标记类型：

| 类型 | 判定标准 | 后续流程 |
|------|----------|----------|
| Requirement | 表达新能力、体验改进、业务规则、流程变化、报表/字段/权限/集成诉求、验收期望 | `/req-capture` 等价流程 |
| Bug | 描述已有能力不符合预期、报错、崩溃、数据错误、性能异常、视觉错位、兼容问题、复现步骤或实际/期望差异 | `/bug-capture` 等价流程 |
| Ambiguous | 同时可能是需求或 BUG，缺少“已有预期行为”或“新能力目标”判断依据 | 输出澄清问题；若可根据上下文合理判断，写明假设后继续 |
| Not Actionable | 只有情绪、背景或无法落地的信息 | 不创建文件，列入“未捕获信息” |

分类原则：

- 如果用户描述“应该怎样但现在不是这样”，优先视为 BUG，除非该能力从未承诺或从未实现。
- 如果用户描述“希望新增/支持/优化/允许/配置/管理”，优先视为需求。
- 一个输入可以同时产生多个 REQ 和多个 BUG。
- 分类不确定且创建错误会造成明显治理成本时，先问用户；否则基于假设继续，并在 capture.md 记录假设。

---

## Step 2 — 拆分评估（MUST）

分别对需求候选和 BUG 候选执行拆分：

### 需求拆分规则

- 若输入包含多个独立用户目标、角色、业务价值、功能边界、验收标准、优先级或交付节奏，MUST 拆分为多个 REQ。
- 若只是同一目标下的多个细节、约束、字段、边界条件或验收点，保留为一个 REQ。
- `--priority` 和 `--parent` 默认应用到拆分出的所有 REQ；用户输入中对单项另有说明时，以单项说明为准。

### BUG 拆分规则

- 若输入包含多个独立现象、不同模块/页面/接口、不同触发路径、不同期望行为、不同严重等级，或可独立修复和验证，MUST 拆分为多个 BUG。
- 若多个表现明显来自同一根因、同一操作路径、同一修复点，或只是不同环境/账号下的同一现象，保留为一个 BUG，并记录影响范围。
- `--severity` 默认应用到拆分出的所有 BUG；用户输入中对单项另有说明时，以单项说明为准。

输出 **Capture Plan**：

```markdown
## Capture Plan

### Requirements
| # | Title | Reason | Priority | Parent |
|---|-------|--------|----------|--------|

### Bugs
| # | Title | Reason | Severity | Environment |
|---|-------|--------|----------|-------------|

### Not Captured / Need Clarification
- ...
```

`--dry-run` 到此停止。

---

## Step 3 — 创建需求捕获记录

对每个 Requirement，执行 `/req-capture` 等价流程：

1. 分配连续的 `REQ-NNNN-kebab-slug`。
2. 创建 `issues/requirements/plan/<REQ-ID>/capture.md`。
3. 创建 `issues/requirements/plan/<REQ-ID>/trace.md`，`status: captured`，`lifecycle.captured` 填完整时间（`YYYY-MM-DD hh:mm:ss`）。
4. 更新 `issues/requirements/_registry.yaml` entries + `next_id`。

`capture.md` 必须记录：

- 原始输入摘录
- 被归类为 Requirement 的理由
- 拆分理由
- 若来自 Ambiguous 判断，记录分类假设
- 待澄清问题

---

## Step 4 — 创建 BUG 捕获记录

对每个 Bug，执行 `/bug-capture` 等价流程：

1. 分配连续的 `BUG-NNNN-kebab-slug`。
2. 创建 `issues/bugs/plan/<BUG-ID>/capture.md`。
3. 创建 `issues/bugs/plan/<BUG-ID>/trace.md`，`status: captured`，`lifecycle.captured` 填完整时间（`YYYY-MM-DD hh:mm:ss`）。
4. 更新 `issues/bugs/_registry.yaml` entries + `next_id`。

`capture.md` 必须记录：

- 原始输入摘录
- 被归类为 Bug 的理由
- 现象、复现线索、期望 vs 实际、环境、附件
- 拆分理由
- 若来自 Ambiguous 判断，记录分类假设

---

## Step 5 — 输出

```text
## Capture 完成

**Created Requirements:** REQ-....
**Created Bugs:** BUG-....
**Not Captured:** ...

**Next:**
1. 需求：/req-explore REQ-xxxx 或 /req-generate REQ-xxxx
2. BUG：/bug-explore BUG-xxxx 或 /bug-generate BUG-xxxx
```

---

## Guardrails

| 规则 | 说明 |
|------|------|
| 先分类再创建 | 必须输出分类和拆分计划 |
| 可混合输出 | 同一输入可创建多个 REQ 和多个 BUG |
| 不升级阶段 | 只创建 capture/trace，不创建 PRD、bug.md、OpenSpec 或 Sprint |
| 不写代码 | 捕获命令不得修改 `src/` |
| 不吞掉模糊项 | 模糊内容必须写明假设或向用户澄清 |

---

## Final Step — Workflow Sync (MUST)

Run the shared `workflow-sync` step before reporting this command as complete.

若创建了需求：

```bash
python scripts/sync-workflow-status.py --event req.capture --req "<REQ-ID-1>" [--req "<REQ-ID-2>" ...]
```

若创建了 BUG：

```bash
python scripts/sync-workflow-status.py --event bug.capture --bug "<BUG-ID-1>" [--bug "<BUG-ID-2>" ...]
```

若同时创建 REQ 和 BUG，分别运行两条同步命令。若任一脚本退出非零，读取 drift 报告，修复不一致后重新同步，并在最终输出保留 `## Workflow Sync` 报告。
