---
name: /requirement-to-opsx
id: requirement-to-opsx
category: Workflow
description: 从 issues/requirements 生成 OpenSpec Change（CLI 驱动），解决视觉原型/验收冲突与 fix-* 二次变更问题
---

将 `issues/requirements/REQ-*` 转为可执行的 OpenSpec Change，并接入 `opsx-propose` → `opsx-apply` → `opsx-archive` 闭环。

**本命令解决的核心问题**（来自 REQ-0001 / fix-login-css-port 教训）：

1. 需求已有原型（HTML/PNG），但实现仍按 Tailwind/shadcn 拼装 → 视觉不达标需补 `fix-*` change
2. `acceptance.md` 与 `user-login.html` 冲突（如 eye icon、版权 footer）→ 归档 delta spec 失败或实现跑偏
3. `requirement-to-change` 手写 change 目录，未走 `openspec new change` / `openspec instructions` → 与 CLI 归档不同步
4. 视觉验收只有 checklist 数字，无 PNG golden reference gate → 「结构对了、看起来不对」

---

**Input**：`REQ-xxxx` 或 `REQ-xxxx-name`（如 `REQ-0001-user-login`）

可选 flags（用户可在同一条消息中说明）：

| Flag | 含义 |
|------|------|
| `--type add\|fix\|update` | 强制 change 类型；省略则自动推断 |
| `--strategy <name>` | 视觉类已选定策略（如 `css-port`、`tailwind-ds`、`asset-bg`） |
| `--skip-explore` | 非 UI 或策略已明确时跳过 explore |
| `--change-name <kebab-case>` | 指定 change id，否则自动命名 |

**Output**：创建 `openspec/changes/<change-id>/`（proposal / design / specs / tasks），更新 REQ trace，提示下一步 `/opsx-apply`。

---

## 前置关系

```text
issues/requirements/REQ-*     ← 业务真相（需求、验收、原型）
        │
        ├─（文档不全时）→ /requirement-to-change REQ-*   补全 requirement/acceptance/prototype
        │
        └─（本文）→ /requirement-to-opsx REQ-*           生成 OpenSpec Change（CLI）
                │
                ├─（UI 视觉未决）→ /opsx-explore
                ├─ /opsx-apply
                └─ /opsx-archive
```

**禁止**：绕过 OpenSpec Change 直接改 `src/`（见 AGENTS.md §5）。

---

## Step 0 — 必须读取

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/ui-design.md          # 若 impact.web 或存在 prototype/web
rules/testing.md
rules/directory-structure.md
```

读取 REQ 目录（全部存在则读，缺失则标记 Not Ready）：

```text
issues/requirements/<REQ-ID>/requirement.md
issues/requirements/<REQ-ID>/user-stories.md
issues/requirements/<REQ-ID>/business-flow.md
issues/requirements/<REQ-ID>/acceptance.md
issues/requirements/<REQ-ID>/trace.md
issues/requirements/<REQ-ID>/prototype/**/*
```

读取 OpenSpec 现状：

```bash
openspec list --json
openspec list --specs          # 或 openspec spec list（视 CLI 版本）
```

若 `openspec/specs/` 中已有相关 capability，**MUST** 打开对应 `spec.md`，供 delta spec 的 MODIFIED 标题对齐。

---

## Step 1 — Requirement Readiness

输出 **Requirement Readiness Report**：

| 字段 | 说明 |
|------|------|
| `readiness` | Ready / Partially Ready / Not Ready |
| `missing_docs` | 缺失文件列表 |
| `has_prototype_web` | 是否存在 `prototype/web/*.html` 或 `*.png` |
| `has_prototype_context` | 是否存在 `*-context.md` |

**Not Ready** 时：先执行 `/requirement-to-change <REQ-ID>` 补文档，**停止**本命令，不要创建 change。

---

## Step 2 — 影响分析与 Change 分类

解析 requirement / acceptance / prototype，填写：

```yaml
impact:
  backend: bool
  web: bool
  miniapp: bool
  admin: bool
  database: bool
  storage: bool
  api: bool

capabilities:
  new: []           # 新 capability → specs/<name>/spec.md ADDED
  modified: []      # 已有 capability → delta MODIFIED（标题必须与 openspec/specs 一致）
```

### Change 类型自动推断（关键）

| 条件 | 推荐 `change_type` | 命名示例 |
|------|-------------------|----------|
| `openspec/specs` 无相关能力，且无 archived add-* | `add` | `add-user-login` |
| 已有实现或 archived change，但验收/视觉未过 | `fix` | `fix-login-css-port` |
| 仅规范、文案、非行为变更 | `update` | `update-login-acceptance-sync` |
| 用户明确 `--type` | 覆盖推断 | — |

**fix-* 触发信号**（满足任一即建议 fix，并在 proposal Why 中写明）：

- 用户描述「与原型/HTML/PNG 不一致」「像素」「视觉差太多」
- `acceptance.md` 视觉项未勾选，但代码已存在
- 已有 archived `add-*` / `align-*`，且本次为 fidelity 专项
- explore 结论为「当前实现策略不足，需换路径（如 CSS Port）」

---

## Step 3 — 原型与验收冲突检测（MUST）

当 `prototype/web/` 存在时，**MUST** 对比三源并输出 **Conflict Report**：

```text
优先级（写入 design.md，不可省略）：
  1. prototype/*.html
  2. prototype/*.png（Golden Reference）
  3. prototype/*-context.md
  4. issues/.../acceptance.md
  5. rules/ui-design.md
  6. openspec/specs（已归档能力）
```

对比项示例（登录页类）：

| 检查项 | HTML | PNG | acceptance.md | 决议 |
|--------|------|-----|---------------|------|
| 密码 eye icon | 无 | 无 | 有 | REMOVED requirement / 以 HTML 为准 |
| 页脚 | security 文案 | security | © 版权 | 以 HTML 为准 |
| 左栏背景 | CSS 拼贴 | 拼贴 | JPG 全屏 | 以 HTML 为准，MODIFIED spec |
| 企微入口 | 全宽 .wecom | 全宽 | 圆形 icon | 以 HTML 为准 |

**MUST** 在 `design.md` 增加 **Conflict Resolution** 小节；在 delta spec 中用 `REMOVED` / `MODIFIED` 消化冲突，**禁止** 只在代码里改、spec 不更新。

---

## Step 4 — UI 视觉：Explore Gate（MUST 条件）

当 `impact.web === true` 且存在 `prototype/web/*.png` 或 `*.html` 时：

**若未提供 `--strategy` 且非 `--skip-explore`：**

1. 告知用户：「UI 类需求 MUST 先选实现策略，再写 design」
2. 执行 `/opsx-explore` 或在本命令内完成同等分析，至少对比：
   - 结构还原（Tailwind 拼装）vs CSS Port vs Asset 背景
3. 将选定策略写入 `design.md` Decisions（如 **D1：CSS Port**）
4. 在用户确认策略前，**MAY** 创建 change 骨架，但 `design.md` MUST 标注 `Pending strategy confirmation` 或等待用户回复

**登录页类推荐策略表**（可写入 design 备选）：

| 策略 | 适用 | 风险 |
|------|------|------|
| A CSS Port | HTML 有完整 `<style>`，像素级 fidelity | 专用 CSS 与 Tailwind 分叉 |
| B DS Primitives | 无 HTML，仅 PNG + token | shadcn 默认态泄漏 |
| C Asset 左栏 | 摄影背景为主 | 与 HTML 拼贴原型不符 |

---

## Step 5 — 创建 Change（OpenSpec CLI）

```bash
openspec new change "<change-id>"
openspec status --change "<change-id>" --json
```

**change-id 规则**：

```text
add-<short-name>
fix-<area>-<strategy>    # 例：fix-login-css-port
update-<area>-<topic>
```

若目录已存在：询问继续填充还是换名。

---

## Step 6 — 按 CLI 顺序生成 Artifacts

对每个 `status: ready` 的 artifact：

```bash
openspec instructions <artifact-id> --change "<change-id>" --json
```

读取返回的 `template`、`instruction`、`dependencies`；**禁止** 把 `context`/`rules` 块复制进 artifact 正文。

### proposal.md — 必须包含

- **Why**：链接 `REQ-ID`；若为 fix-*，说明前序实现不足根因（如「结构参数 ≠ 视觉 port」）
- **What Changes**：按 impact 列 Backend/Web/DB/规范
- **Capabilities**：`new` / `modified` 与 Step 2 一致
- **Impact**：含是否影响 Docker、Orval、Design System

### design.md — 必须包含

- **原型优先级**（Step 3 决议）
- **Conflict Resolution**（若有冲突）
- **实现策略 Decision**（UI 类：CSS Port / 等，含备选与理由）
- **Goals / Non-Goals**
- **Auth/API 冻结**（若仅 UI：明确 store/hooks/API 不改）
- **验收 gate**：UI 类 MUST 定义 PNG diff checklist（≥15 项）与视口（1280×1024）

### specs/**/*.md — Delta 规范（避免 archive 失败）

**MODIFIED**：

1. 在 `openspec/specs/<capability>/spec.md` 中 **精确查找** `### Requirement: <标题>`
2. 复制 **整段** requirement（含所有 scenario）到 `## MODIFIED Requirements` 再改
3. 标题 whitespace-insensitive 但必须一致；**不得** MODIFIED 主 spec 中不存在的 requirement 名

**ADDED**：新 capability 或主 spec 无对应条目时

**REMOVED**：必须含 **Reason** + **Migration**（如移除「密码显隐」）

**Scenario 格式**：`#### Scenario:`（4 个 `#`），WHEN/THEN 列表

**UI 登录页类**：modified capability 通常为 `web-client`；勿创建与主 spec 重复的 requirement 名（如单独「登录表单元素」除非主 spec 已有该标题）

### tasks.md — 必须包含

分组建议：

```text
1. 实现（按 design 策略）
2. 测试（vitest / backend）
3. 构建（vite build / docker compose build web）
4. 视觉验收（PNG 并排 + trace.md checklist）
5. 文档（rules/ui-design.md、REQ trace、acceptance-report）
```

**UI fidelity 任务模板**（fix-* 必含）：

```text
- [ ] 创建/更新 port CSS（自 user-login.html）
- [ ] 重构组件为 HTML class 结构
- [ ] 移除与原型冲突的 shadcn 默认态
- [ ] npx vitest run <feature>
- [ ] npm run build
- [ ] ./scripts/docker-up.sh
- [ ] 1280×1024 并排 user-login.png，填写 trace.md checklist
```

Checkbox 格式：`- [ ] X.Y 描述`（供 `opsx-apply` 解析）

---

## Step 7 — 追溯（Traceability）

更新 **REQ trace**：

```text
issues/requirements/<REQ-ID>/trace.md
```

追加：

```yaml
openspec_changes:
  - change_id: fix-login-css-port
    type: fix
    status: proposed | applied | archived
    requirement_id: REQ-0001-user-login
```

创建 **Change trace**（UI 类强烈推荐）：

```text
openspec/changes/<change-id>/trace.md
```

含：REQ 链接、策略、PNG checklist 表、验证命令、已知可接受偏差。

---

## Step 8 — 输出与下一步

```text
## Requirement → OpenSpec 完成

**REQ:** REQ-0001-user-login
**Change:** fix-login-css-port
**Type:** fix
**Readiness:** Ready
**Strategy:** css-port（路径 A）
**Conflicts resolved:** 3（eye icon / footer / left panel bg）

**Artifacts:**
- [x] proposal.md
- [x] design.md
- [x] specs/web-client/spec.md
- [x] tasks.md

**Next:**
1. /opsx-apply fix-login-css-port
2. 完成后 /opsx-archive fix-login-css-port
```

---

## Step 9 — 与归档联动（提醒写入 tasks 末项）

归档时：

```bash
openspec archive <change-id> -y
```

**归档前自检**：

- [ ] delta spec 中 MODIFIED 标题均存在于 `openspec/specs/`
- [ ] 每条 MODIFIED requirement 正文含 MUST/SHALL
- [ ] 每个 requirement 至少一个 `#### Scenario:`
- [ ] tasks.md 全部 `[x]`

归档成功后：更新 REQ `trace.md` 中 change `status: archived`。

---

## Guardrails

| 规则 | 说明 |
|------|------|
| 不替代 requirement-to-change | 文档不全时先补 REQ，再 opsx |
| 不跳过 OpenSpec CLI | 禁止手写 `openspec/changes/` 而无 `.openspec.yaml` |
| UI 有 HTML 时禁止仅对 PNG 猜布局 | 必须读 `*.html` + `*-context.md` |
| fix-* 必须写清前序不足 | proposal Why 写根因，避免重复犯错 |
| 不 MODIFIED 不存在的 requirement | 否则 `openspec archive` 会 abort |
| 视觉类必须有 trace checklist | 禁止仅「spacing 数字验收」 |
| 代码实现 | 本命令 **不** 写 `src/`；实现用 `/opsx-apply` |

---

## 示例：REQ-0001 登录页（fix-login-css-port 正序）

```text
/requirement-to-opsx REQ-0001-user-login --type fix --strategy css-port
```

期望产出：

- `fix-login-css-port` change
- design：HTML > PNG > acceptance；D1 CSS Port；auth 冻结
- delta spec：MODIFIED `管理端登录页` 等（非虚构标题）；REMOVED `密码显隐切换`
- tasks：port CSS → 组件 → vitest → build → docker → PNG checklist

然后：

```text
/opsx-apply fix-login-css-port
/opsx-archive fix-login-css-port
```

---

## 示例：全新能力

```text
/requirement-to-opsx REQ-0002-tile-catalog
```

推断 `add-tile-catalog` → 无 explore 强制（无 fidelity 投诉）→ specs ADDED 新 capability → `/opsx-apply`。

---

## 参考

- 需求文档治理：`.cursor/commands/requirement-to-change.md`
- 缺陷修复：`.cursor/commands/bug-to-change.md`（BUG 用 fix-*，REQ 用本文）
- OpenSpec 执行：`.cursor/commands/opsx-propose.md`、`opsx-apply.md`、`opsx-archive.md`
- 视觉探讨：`.cursor/commands/opsx-explore.md`
- 归档样例：`openspec/changes/archive/2026-06-13-fix-login-css-port/`
