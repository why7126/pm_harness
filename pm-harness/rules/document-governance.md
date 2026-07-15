---
purpose: 文档治理规范
content: docs、issues、iterations、openspec 的生成、更新、同步与归档规则
source: AI自动生成初稿，项目团队确认
update_method: 研发流程变化时由AI辅助更新，人工Review后合并
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-11 16:25:13
note: AI执行需求、BUG、技术改造前必须读取；优先级高于普通文档说明
---

# 文档治理规范

## 1. 总原则

研发链路：用户输入 → `issues/` → `iterations/` → `openspec/changes/` → `src/ + tests/` → `docs/` 同步 → `openspec/specs/` 合并 → 归档。

除拼写、注释、格式化、无行为变化的小修外，AI 不得从一句话直接跳到代码实现；必须先判断是否需要 Issue、Sprint 或 OpenSpec Change。

## 2. docs 目录

`docs/` 只沉淀长期产品、架构、部署、接口、数据库、兼容性和治理信息；需求、BUG、迭代不得放入 `docs/`。

```text
docs/
├── NN-topic.md              # 主文档，有序号
├── standards/<topic>.md     # 治理细则
├── knowledge-base/**        # incidents / retrospectives / best-practices
└── README.md                # 导航
```

| 变更 | 必须同步 |
|---|---|
| 产品/模块边界 | `docs/00-product-overview.md` |
| 架构 | `docs/01-architecture.md` |
| Docker/端口/环境变量 | `docs/02-deployment.md`、README、`.env.example` |
| API | `docs/03-api-index.md`、`docs/standards/api-governance.md`、客户端生成配置/生成物 |
| 数据库 | `docs/04-database-design.md`、迁移、测试 |
| 兼容性 | `docs/05-compatibility-matrix.md` |
| 媒体/对象存储 | 对应 standards、兼容性、部署文档 |
| 故障/复盘/最佳实践 | `docs/knowledge-base/{incidents,retrospectives,best-practices}/` |

规则：保留 YAML Frontmatter；不确定内容标 `待确认`；产品范围、验收、架构边界、上线策略需人工确认。

## 3. 时间与元数据（MUST）

所有项目维护的时间属性字段使用：

```text
YYYY-MM-DD HH:mm:ss
```

默认时区 `Asia/Shanghai`。适用于 Frontmatter、lifecycle、评审/归档/发布记录、Sprint 里程碑、OpenSpec trace、docs/rules 表格中的项目时间。目录名、文件名、版本号、REQ/BUG 编号日期片段可保持原格式；外部引用可保留原文格式，但项目新增记录必须补标准时间。

AI 新建 Markdown（含 Frontmatter）MUST 包含：

```yaml
created_at: YYYY-MM-DD HH:mm:ss
updated_at: YYYY-MM-DD HH:mm:ss
```

更新文档时不得改 `created_at`，MUST 刷新 `updated_at`。Legacy 字段如 `recorded_at` 不再用于新文档。

## 4. issues 目录

生命周期阶段见 `rules/issues-lifecycle.md`。禁止在 `issues/requirements/` 或 `issues/bugs/` 根下新建扁平 `REQ-*` / `BUG-*`。

```text
issues/requirements/{plan,review,archive}/REQ-xxxx-slug/
issues/bugs/{plan,review,archive}/BUG-xxxx-slug/
```

需求至少包含编号、来源、目标用户、价值、描述、优先级、状态、关联迭代、关联 Change、验收要点。BUG 至少包含编号、来源、严重程度、影响范围、复现步骤、实际/期望结果、日志/截图、状态、关联迭代、关联 Change、回归测试。

Issue 状态在 capture、review、opsx、sprint-propose、apply、archive/promote 时通过 workflow sync 或对应命令同步；同步 MUST 覆盖 trace Frontmatter 与 fenced `yaml` 中的 `status`、`iteration`、`openspec_changes[].status`，并在 `## 变更记录` 追加幂等 workflow event 行。

`trace.md` 的 `## 变更记录` MUST 使用标准 Markdown 表格，且表头必须紧跟章节标题之后：

```markdown
## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| YYYY-MM-DD HH:mm:ss | /command | 说明 |
```

禁止把记录行写在表头之前；Workflow Sync SHOULD 自动整理历史错位表格，但新增或手工修复时仍须保持表头优先。

## 5. iterations 目录

生命周期阶段见 `rules/iterations-lifecycle.md`。Sprint 创建必须通过 `/sprint-propose` 或等价流程生成四件套：

```text
iterations/change/sprint-xxx/
├── sprint.yaml
├── sprint.md
├── release-note.md
└── acceptance-report.md
```

`sprint.yaml` 是机器事实源，MUST 包含：

```yaml
sprint_id: sprint-xxx
status: planning | in_progress | completed
lifecycle_stage: change | archive
start_date: YYYY-MM-DD HH:mm:ss
end_date: YYYY-MM-DD HH:mm:ss
capacity: { developers: <int>, testers: <int> }
requirements: []
bugs: []
changes: []
estimated_story_points: <number>
estimated_person_days: <number>
```

范围、状态、日期、估算变化时同步 `sprint.yaml` 与 `sprint.md`。Sprint 归档后目录迁入 `iterations/archive/sprint-xxx/`。

## 6. OpenSpec 目录

- `openspec/specs/`：已生效能力；开发中不得直接修改。
- `openspec/changes/`：开发中的需求、BUG 修复、技术改造。
- `openspec/changes/archive/`：已完成变更。

以下变化必须创建 Change：新功能、行为性 BUG 修复、API/数据库/权限/Docker/环境变量/UI/上传存储/测试验收发布治理变化。

来源于 REQ/BUG 的 Change 在执行 `/opsx-apply` 前 **MUST** 已纳入某个 `sprint-xxx` 正式范围：

- `iterations/change|archive/<sprint>/sprint.yaml` 的 `requirements[]` / `bugs[]` / `changes[]` MUST 能同时追溯到目标 REQ/BUG 与 Change。
- 关联 REQ/BUG `trace.md` 的 `iteration` MUST 指向同一个 `sprint-xxx`，且 `status` MUST 为 `in_sprint` 或后续交付态。
- 若 `python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto --dry-run` 无法解析到 Sprint，MUST 视为门禁失败；先运行 `/sprint-propose` 纳入迭代并完成同步，不得继续实现。
- 仅非 REQ/BUG 来源的纯技术治理 Change 可豁免此门禁；豁免原因 MUST 写入执行输出。

Change 推荐结构：

```text
proposal.md
design.md
tasks.md
trace.md
acceptance.md
test-plan.md
specs/
implementation/
```

归档时合并 delta spec 到 `openspec/specs/`，更新 Issue/Sprint 状态，并移动 Change；不得删除归档内容。正式 spec 正文使用中文，OpenSpec 关键字可保留英文；归档后清理脚手架占位文案。

## 7. Workflow Sync（MUST）

执行 `req-*`、`bug-*`、`opsx-*`、`sprint-*` 后运行：

```bash
python scripts/sync-workflow-status.py --event <event> [--sprint auto] [--change|--req|--bug <id>]
```

- Skill：对应 Agent 工具入口中的 `workflow-sync` 说明（如项目提供）
- 本地校验：`python scripts/sync-workflow-status.py --sprint auto --check`
- 禁止手工编辑 `sprint.md` 的 `<!-- workflow-sync:* -->` 标记块与派生 Scope 表。
- Scope 表、里程碑、archived 时间戳 MUST 使用 `YYYY-MM-DD HH:mm:ss` 且时分秒为实际值；不得使用 `00:00:00` 占位。
- `sprint.yaml` 中正式纳入的 REQ/BUG MUST 同步出现在 `sprint.md` 的 Sprint 目标列表和对应要点小节；未评审项只能列「延后项（待评审）」。

常用事件：`req.capture`…`req.opsx`、`bug.capture`…`bug.opsx`、`opsx.propose|apply|archive`、`sprint.propose|apply|archive`。

## 8. 禁止行为

- 绕过 Issue / OpenSpec Change 直接开发需求或行为性 BUG。
- 只改代码不改对应文档、trace、测试或验收记录。
- 开发中直接修改 `openspec/specs/`。
- 把需求、BUG、迭代、Spec 混在同一文档。
- 生成无来源、无状态、无验收标准的需求或 BUG 文档。
