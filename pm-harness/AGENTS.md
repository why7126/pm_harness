---
purpose: AI 行为入口
content: AI 开发流程、规则加载机制、OpenSpec 执行规则、需求与缺陷治理、目录结构约束、部署约束、模块边界、输出要求
source: Harness AGENTS.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；初始化后由项目团队确认；后续由 AI 辅助更新并经人工 Review
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 09:02:51
note: 适用于 {PRODUCT_NAME} 项目；AI 执行任何任务前必须优先阅读本文档
template_scope: 可作为工程初始化时的 AGENTS.md 模块
---
# AI Agent 工作指南

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如前端、算法、对象存储、私有化部署、多 Agent 工具。

## 0. 生成与维护原则 `[通用]`

AGENTS.md 是 AI Agent 进入工程后的第一入口。它不是面向用户的产品介绍，而是让 AI 在执行任何任务前明确：

- 当前项目是什么，业务边界和技术边界在哪里。
- 必须先读取哪些规则、契约、文档和任务上下文。
- 哪些目录可以修改，哪些目录禁止修改，新增目录如何审批。
- 需求、BUG、接口、数据库、UI、部署、数据、模型和文档变更分别走什么流程。
- 完成任务前需要运行什么验证，最终回复需要说明什么。

初始化生成 AGENTS.md 时，必须优先使用用户输入覆盖模板占位符。缺失信息可以保留为 `待确认`，但不得编造具体技术栈、部署地址、第三方服务、命令或业务规则。

常用占位符：

| 占位符 | 含义 | 归属 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | `[个性化]` |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | `[个性化]` |
| `{PRODUCT_DESCRIPTION}` | 产品定位与目标 | `[个性化]` |
| `{BUSINESS_DOMAIN}` | 业务领域 | `[个性化]` |
| `{TARGET_USERS}` | 目标用户或角色 | `[个性化]` |
| `{PRODUCT_FORMS}` | 产品形态，如 Web、微信小程序、移动端、桌面端、API 服务 | `[个性化]` |
| `{BACKEND_STACK}` | 后端技术栈 | `[个性化]` |
| `{FRONTEND_STACK}` | 前端技术栈 | `[个性化]` |
| `{DATABASE_STACK}` | 数据库与迁移方案 | `[个性化]` |
| `{OBJECT_STORAGE_STACK}` | 对象存储方案 | `[条件启用]` |
| `{ASYNC_TASK_STACK}` | 异步任务、消息队列、调度系统 | `[条件启用]` |
| `{ALGORITHM_STACK}` | 算法、模型、AI 服务栈 | `[条件启用]` |
| `{DEPLOYMENT_STACK}` | 部署方式，如 Docker Compose、Kubernetes、私有化部署 | `[个性化]` |
| `{ENABLED_AGENT_TOOLS}` | 启用的 Agent 工具，如 Cursor、Claude Code、Codex、OpenCode、Kiro | `[条件启用]` |
| 默认综合捕获命令 | `/capture` | `[通用]` |
| 默认需求命令集 | `/req-capture`、`/req-explore`、`/req-generate`、`/req-complete`、`/req-review`、`/req-opsx` | `[通用]` |
| 默认缺陷命令集 | `/bug-capture`、`/bug-explore`、`/bug-generate`、`/bug-complete`、`/bug-review`、`/bug-opsx` | `[通用]` |
| 默认迭代命令集 | `/sprint-propose`、`/sprint-explore`、`/sprint-apply`、`/sprint-exps`、`/sprint-archive` | `[通用]` |
| `{PRIMARY_VERIFY_COMMAND}` | 项目统一验证命令 | `[个性化]` |

## 1. 项目定位 `[个性化]`

{PRODUCT_NAME} 是一个 {BUSINESS_DOMAIN} 领域项目，采用 OpenSpec + AI Agent 规范编程方式开发。

产品定位：

```text
{PRODUCT_DESCRIPTION}
```

目标用户：

```text
{TARGET_USERS}
```

系统包含：

```text
{PRODUCT_FORMS}
{BACKEND_STACK}
{FRONTEND_STACK}
{DATABASE_STACK}
{OBJECT_STORAGE_STACK}
{ASYNC_TASK_STACK}
{ALGORITHM_STACK}
{DEPLOYMENT_STACK}
```

本仓库的核心目标是让项目状态可读、可审计、可验证：

```text
idea -> requirement/bug -> review -> sprint/change -> design/tasks -> implementation -> verification -> archive
```

项目状态不得只存在于对话中。需求、BUG、计划、规格、决策、验证结果和归档记录必须沉淀到 `issues/`、`iterations/`、`openspec/`、`docs/`、`rules/` 等可读文件中。

## 2. AGENTS.md 模块构成 `[通用]`

初始化工具生成 AGENTS.md 时，建议按下列模块组装：

| 模块 | 必选 | 归属 | 生成方式 |
|---|---:|---|---|
| 文档元数据 | 是 | `[通用] + [个性化]` | 固定字段 + 产品名替换 |
| 生成与维护原则 | 是 | `[通用]` | 默认保留 |
| 项目定位 | 是 | `[个性化]` | 根据用户输入生成 |
| 必读文档 | 是 | `[通用] + [个性化]` | 基础规则固定，任务路由按项目能力扩展 |
| rules 使用规则 | 是 | `[通用]` | 按实际存在的 rules 文件生成 |
| 多 Agent 工具与命令同步 | 否 | `[条件启用]` | 启用 Cursor、Claude Code、Codex、OpenCode、Kiro 等工具时保留 |
| 模块边界与子项目路由 | 否 | `[条件启用]` | monorepo、多端、多服务项目启用 |
| AI 开发流程 | 是 | `[通用]` | 默认采用需求/BUG -> Review -> OpenSpec -> 实现 -> 验证 -> 归档 |
| 需求处理流程 | 是 | `[通用] + [个性化]` | 默认保留，命令名按项目替换 |
| BUG 处理流程 | 是 | `[通用] + [个性化]` | 默认保留，命令名按项目替换 |
| Sprint 处理流程 | 否 | `[条件启用]` | 项目采用迭代治理时保留 |
| OpenSpec 约束 | 是 | `[通用]` | 默认保留 |
| 原型与视觉验收优先级 | 否 | `[条件启用]` | 有 UI 原型、截图或设计稿时启用 |
| 强制规则 | 是 | `[通用] + [个性化]` | 通用禁令固定，技术栈规则按输入生成 |
| 目录边界 | 是 | `[通用] + [个性化]` | 基础目录固定，业务目录按输入生成 |
| 部署要求 | 否 | `[条件启用]` | 有部署诉求时启用 |
| API 与契约要求 | 否 | `[条件启用]` | 有前后端、跨模块或开放接口时启用 |
| 数据、媒体、对象存储与模型文件 | 否 | `[条件启用]` | 有上传、文件、模型、数据集时启用 |
| UI 与 Design System | 否 | `[条件启用]` | 有前端、移动端、微信小程序或桌面 UI 时启用 |
| 安全规则 | 是 | `[通用]` | 默认保留，按项目补充 |
| 常用命令 | 是 | `[个性化]` | 从项目脚本和技术栈生成 |
| 输出要求 | 是 | `[通用] + [个性化]` | 默认中文，可按用户要求调整 |
| 完成任务后检查清单 | 是 | `[通用] + [条件启用]` | 按启用模块生成 |

## 3. AI 必须优先读取的文档 `[通用 + 个性化]`

AI Agent 在执行任何需求、BUG、代码修改、文档修改、部署修改前，必须按顺序读取：

```text
1. AGENTS.md
2. openspec/project.md
3. rules/global.md
4. rules/language.md
5. rules/coding.md
6. rules/testing.md
7. rules/security.md
8. rules/api.md
9. rules/database.md
10. rules/ui-design.md
11. rules/compatibility.md
12. rules/release.md
13. rules/directory-structure.md
14. rules/document-governance.md
15. rules/data-management.md
16. rules/environment.md
17. rules/media.md
18. rules/object-storage.md
19. rules/port-management.md
20. rules/requirement-management.md
21. rules/bug-management.md
22. rules/issues-lifecycle.md
23. rules/iterations-lifecycle.md
24. 当前任务对应的 issues/、iterations/ 或 openspec/changes/<change-id>/
```

如果某个 rules 文件不存在，应说明缺失并使用最接近的通用规则，不得自行假定不存在的规则内容。

任务专项读取规则：

| 任务类型 | 必须额外读取 |
|---|---|
| 需求治理 | `rules/requirement-management.md`、`rules/issues-lifecycle.md`、对应 `issues/requirements/{plan,review,archive}/REQ-*`、相关 `iterations/` |
| BUG 治理 | `rules/bug-management.md`、`rules/issues-lifecycle.md`、对应 `issues/bugs/{plan,review,archive}/BUG-*`、相关日志、截图和回归记录 |
| API/接口变更 | `rules/api.md`、API 索引、OpenAPI 来源、客户端生成配置 |
| 数据库变更 | `rules/database.md`、schema、迁移、seed、fixtures、兼容性文档 |
| 部署、环境变量或端口 | `rules/environment.md`、`rules/port-management.md`、`docs/02-deployment.md`、`deploy/`、`docker-compose.yml`、`.env.example` |
| Web UI、Design System 或前端样式 | `rules/ui-design.md`、前端 README、Design Token、组件库、视觉验收入口 |
| 媒体、文件上传、对象存储 | `rules/media.md`、`rules/object-storage.md`、`rules/data-management.md`、相关存储策略文档 |
| 样例数据、fixtures、导入导出 | `rules/data-management.md`、`data/README.md`、测试 fixtures |
| 算法、模型推理、AI 服务 | `models/`、`src/algorithm/` 或项目实际算法目录、模型版本与校验说明 |
| 兼容性、信创或私有化 | `rules/compatibility.md`、`compatibility/`、部署矩阵 |

## 4. rules 目录使用规则 `[通用]`

`rules/` 是全局研发规范目录，不是参考资料，而是强制约束。

| 文件 | AI 使用方式 | 归属 |
|---|---|---|
| `rules/global.md` | 判断是否允许执行当前任务、全局禁止行为 | `[通用]` |
| `rules/language.md` | 控制输出语言、文档语言、代码命名 | `[通用]` |
| `rules/coding.md` | 控制代码结构、命名、复杂度、架构分层 | `[通用]` |
| `rules/testing.md` | 判断是否需要新增或更新测试 | `[通用]` |
| `rules/security.md` | 检查认证、上传、输入、权限、敏感信息 | `[通用]` |
| `rules/directory-structure.md` | 控制新增文件位置和目录边界 | `[通用]` |
| `rules/document-governance.md` | 控制 docs、issues、iterations、openspec 的生成、更新、归档 | `[通用]` |
| `rules/requirement-management.md` | 控制 REQ 捕获、六件套、评审、状态机和 trace | `[通用]` |
| `rules/bug-management.md` | 控制 BUG 捕获、复现、根因、评审、回归和知识沉淀 | `[通用]` |
| `rules/issues-lifecycle.md` | 控制 REQ/BUG 在 plan、review、archive 三阶段目录中的迁移和同步 | `[通用]` |
| `rules/iterations-lifecycle.md` | 控制 Sprint 在 change、archive 两阶段目录中的迁移和同步 | `[通用]` |
| `rules/api.md` | 控制 API 路径、参数、响应、错误码、OpenAPI | `[条件启用]` |
| `rules/database.md` | 控制 schema、迁移、查询、Repository 或 DAO 规范 | `[条件启用]` |
| `rules/compatibility.md` | 控制浏览器、终端、数据库、部署环境兼容性 | `[条件启用]` |
| `rules/release.md` | 控制发布、回滚、变更说明 | `[条件启用]` |
| `rules/environment.md` | 控制 `.env.example`、环境变量和密钥安全 | `[条件启用]` |
| `rules/data-management.md` | 控制 `data/`、样例数据、运行时数据和提交边界 | `[条件启用]` |
| `rules/media.md` | 控制图片、音视频、文档等媒体资产上传、存储和展示 | `[条件启用]` |
| `rules/object-storage.md` | 控制对象存储 bucket、前缀、权限和存储客户端 | `[条件启用]` |
| `rules/port-management.md` | 控制服务端口分配和冲突处理 | `[条件启用]` |
| `rules/ui-design.md` | 控制 Web、移动端、微信小程序、桌面端 UI 一致性 | `[条件启用]` |

AI 生成代码或文档时，必须遵循与当前任务相关的 `rules/` 文件，并在最终回复中说明使用了哪些关键规则。

## 5. 多 Agent 工具与命令同步 `[条件启用]`

当项目启用多个 AI 工具或 slash command 时，必须明确命令事实源和同步方式。

```text
启用工具：{ENABLED_AGENT_TOOLS}
命令事实源：{AGENT_COMMAND_SOURCE}
同步命令：{AGENT_COMMAND_SYNC_COMMAND}
```

推荐约定：

| 工具 | 路径 | 说明 |
|---|---|---|
| Cursor | `.cursor/commands/*.md` | 可作为 slash 命令事实源 |
| Claude Code | `.claude/commands/{group}/*.md` | 可按分组同步 |
| Codex | `.codex/skills/` 或 `.codex/prompts/*.md` | 推荐技能承载复杂流程 |
| OpenCode | `.opencode/commands/*.md` | 扁平命令文件 |
| Kiro | `.kiro/prompts/*.prompt.md` | prompt 文件 |

新增、删除或修改命令后必须同步到启用工具，并检查：

- 命令名称是否与 AGENTS.md、rules、README 和 Skill 文档一致。
- 旧命令是否已标记废弃或移除。
- 命令是否引用了存在的目录、脚本、模板和规则文件。
- 命令同步脚本是否通过验证。

### 5.1 Workflow 状态同步（MUST）`[通用]`

执行 `/capture` 或任何 `req-*`、`bug-*`、`opsx-*`、`sprint-*` 命令后，必须调用共享 `workflow-sync` skill，并运行：

```bash
python scripts/sync-workflow-status.py --event <event> [--req REQ-xxxx] [--bug BUG-xxxx] [--change change-id] [--sprint sprint-xxx|auto]
```

执行 `/opsx-archive` 或 `/sprint-archive` 后，必须在 workflow sync 之后继续运行 Issue 物理阶段归档：

```bash
python scripts/promote-issue-stage.py --to archive [--change change-id] [--sprint sprint-xxx] --reason "<event>"
```

该脚本只会移动所有关联 Change 均已归档的 REQ/BUG；如报告 Blocked，必须保留条目在 `review/` 并说明阻塞的 Change。

禁止仅手工编辑 `sprint.md` Scope 表、`acceptance-report.md` 状态段、`release-note.md` 发布状态或 issue `trace.md` 的 OpenSpec 状态。若同步脚本报告 drift 或以 `--check` 失败，当前命令不得视为完成，必须修复后重新运行同步，并在最终输出保留 `## Workflow Sync` 报告。

### 5.2 Knowledge Base 复用门禁（MUST）`[通用]`

`docs/knowledge-base/` 是后续迭代的输入源，不只是 Sprint 结束后的输出。执行以下命令时必须先读取 `docs/knowledge-base/README.md`，并按场景读取 `docs/knowledge-base/sprints/`、`docs/knowledge-base/incidents/`、`docs/knowledge-base/best-practices/` 中相关条目：

- `/sprint-propose`：必须读取最近一次 Sprint 复盘和所有 `open` / `in_sprint` 行动项，并在 `sprint.md` 写入「知识库承接项」。
- `/req-complete`：必须把相关 best-practice 转成 `acceptance.md` checklist；不适用时写明原因。
- `/opsx-apply` 与 `/sprint-apply`：实现前必须输出 Knowledge Gate，列出已读取条目、适用约束和未承接原因。

禁止只在 `/sprint-exps` 写入知识库，而在下一次规划、需求完善或实现中不读取。复盘行动项不得长期停留在 `open`；进入 Sprint 后必须标记或登记为 `in_sprint`，完成后标记为 `done`。

## 6. 模块边界与子项目规则路由 `[条件启用]`

当项目是 monorepo、多端应用或多服务系统时，必须启用本节。根目录治理层只统筹，不替代子项目自有规则。

| 模块 | 路径 | 职责 | 子项目规则入口 | 技术栈 |
|---|---|---|---|---|
| 后端 | `src/backend/` | API、Service、Repository、DB、后台任务 | `src/backend/README.md` 或 `src/backend/AGENTS.md` | `{BACKEND_STACK}` |
| 前端 Web | `src/web/` | Web 页面、交互、状态管理、前端请求 | `src/web/README.md` 或 `src/web/AGENTS.md` | `{FRONTEND_STACK}` |
| 微信小程序 | `src/wechat-miniapp/` | 微信小程序页面与端能力 | `src/wechat-miniapp/README.md` | `{WECHAT_MINIAPP_STACK}` |
| 移动端 | `src/mobile/`、`src/android/`、`src/ios/` | 移动端 App | 对应 README 或 AGENTS | `{MOBILE_STACK}` |
| 桌面端 | `src/desktop/` | 桌面客户端 | 对应 README 或 AGENTS | `{DESKTOP_STACK}` |
| 算法 | `src/algorithm/` | 模型推理、算法服务、音视频或数据处理 | `src/algorithm/README.md` | `{ALGORITHM_STACK}` |
| Agent | `src/agent/` | Agent 工作流、工具调用、自动化实验 | `src/agent/README.md` 或 `src/agent/AGENTS.md` | `{AGENT_STACK}` |
| 共享层 | `src/shared/` | 类型、契约、工具、Design Token | `src/shared/README.md` | `{SHARED_STACK}` |
| 基础设施 | `src/infrastructure/`、`deploy/` | 部署、环境、脚本、观测 | `deploy/README.md` | `{DEPLOYMENT_STACK}` |

跨模块改动必须先明确影响面：

- 是否改变接口契约、数据格式、事件协议或文件格式。
- 是否需要同步更新多个模块的类型、客户端、测试和文档。
- 是否需要新增或修改 `openspec/specs/` 或 `openspec/changes/`。
- 是否需要补充兼容性、迁移、部署或回滚说明。

## 7. AI 开发流程 `[通用]`

正式需求、BUG 和高影响变更必须进入可追踪流程：

```text
需求 / BUG / 变更意图
↓
issues/requirements/ 或 issues/bugs/
↓
需求评审 / BUG 评审
↓
iterations/（仅纳入 approved REQ/BUG）
↓
openspec/changes/（proposal / design / specs / tasks / trace）
↓
实现：src/、deploy/、docs/、tests/
↓
验证命令与验收记录
↓
openspec archive / sprint archive
```

轻量文档修订、注释修正、拼写修正、无行为变化的小改动可以不新建 OpenSpec Change；但如果改变业务能力、接口契约、数据结构、部署拓扑、权限边界、工作流语义或团队流程，必须走 OpenSpec Change。

评审门禁是硬边界：需求或 BUG 未完成评审、评审未通过或状态不是 `approved`/`in_sprint` 时，不得执行 `/req-opsx`、`/bug-opsx`、`/opsx-apply`、`/sprint-apply` 或等价开发流程；也不得写入 `iterations/change/<sprint-id>/` 下的 Sprint 规划文件。此类条目只能在命令输出中列为 Blocked/Deferred，并提示先执行 `/req-review` 或 `/bug-review`。

## 8. 默认自定义命令入口 `[通用]`

除 OpenSpec 原生命令外，Harness 默认提供以下自定义命令。`.cursor`、`.claude`、`.codex`、`.kiro`、`.opencode` 均应支持同一组命令语义，只允许因工具目录结构差异调整文件路径，不允许改变命令输入、输出和是否开发的边界。

### 8.0 综合捕获 `/capture`

| 命令 | 阶段 | 输入 | 输出 | 是否生成文档 | 是否生成代码 |
|---|---|---|---|---|---|
| `/capture` | 综合记录与分类拆分 | 需求/BUG 未分类原文、反馈、会议纪要、测试记录 | 一个或多个 REQ/BUG 的 `capture.md`、`trace.md` | 是 | 否 |

规则：

- 用户不知道内容属于需求还是 BUG 时，优先使用 `/capture`。
- `/capture` 必须先分析输入，区分 Requirement、Bug、Ambiguous、Not Actionable，再按 `/req-capture` 或 `/bug-capture` 等价流程创建记录。
- 同一输入可拆分为多个需求和多个 BUG；不确定且风险较高时先向用户澄清。
- `/capture` 不得创建 `requirement.md`、`bug.md`、OpenSpec Change、Sprint 规划或业务代码。

### 8.1 需求域 `req-*`

| 命令 | 阶段 | 输入 | 输出 | 是否生成文档 | 是否生成代码 |
|---|---|---|---|---|---|
| `/req-capture` | 需求记录与必要拆分 | 一个或多个需求描述 | 一个或多个 `capture.md`、`trace.md` | 是 | 否 |
| `/req-explore` | 需求探索 | `REQ-ID` | 分析结论 | 默认否 | 否 |
| `/req-generate` | PRD 生成 | `REQ-ID` | `requirement.md` | 是 | 否 |
| `/req-complete` | 需求完善 | `REQ-ID` | 需求六件套补齐 | 是 | 否 |
| `/req-review` | 需求评审 | `REQ-ID` | `review.md`、状态变更 | 是 | 否 |
| `/req-opsx` | 转 OpenSpec | `REQ-ID` | OpenSpec Change | 是 | 否 |

### 8.2 缺陷域 `bug-*`

| 命令 | 阶段 | 输入 | 输出 | 是否生成文档 | 是否生成代码 |
|---|---|---|---|---|---|
| `/bug-capture` | 缺陷记录与必要拆分 | 一个或多个缺陷描述 | 一个或多个 `capture.md`、`trace.md` | 是 | 否 |
| `/bug-explore` | 缺陷分析 | `BUG-ID` | 分析结论 | 默认否 | 否 |
| `/bug-generate` | 缺陷生成 | `BUG-ID` | `bug.md` | 是 | 否 |
| `/bug-complete` | 缺陷完善 | `BUG-ID` | 根因分析包 | 是 | 否 |
| `/bug-review` | 缺陷评审 | `BUG-ID` | `review.md`、状态变更 | 是 | 否 |
| `/bug-opsx` | 转 OpenSpec | `BUG-ID` | `fix-*` Change | 是 | 否 |

### 8.3 Change 级 `opsx-*`

| 阶段 | 命令 | 说明 |
|---|---|---|
| 探索策略 | `/opsx-explore` | UI、架构、算法或迁移策略未决时使用 |
| 快速提案 | `/opsx-propose` | 无 REQ/BUG 的小型或探索性变更 |
| 实现 | `/opsx-apply` | 按 tasks 实现并补测试 |
| 归档 | `/opsx-archive` | 变更完成后同步 specs 并归档 |

### 8.4 Sprint 级 `sprint-*` `[条件启用]`

| 命令 | 阶段 | 输入 | 输出 | 是否开发 |
|---|---|---|---|---|
| `/sprint-propose` | Sprint 规划 | `Sprint-ID` | Sprint 四件套 | 否 |
| `/sprint-explore` | Sprint 分析 | `Sprint-ID` | 依赖分析、风险分析 | 否 |
| `/sprint-apply` | Sprint 执行 | `Sprint-ID` | 自动编排开发 | 是 |
| `/sprint-exps` | Sprint 经验复盘 | `Sprint-ID` | 知识库经验沉淀 | 否 |
| `/sprint-archive` | Sprint 归档 | `Sprint-ID` | 批量归档 | 否 |

### 8.5 基础设施 Bootstrap `[条件启用]`

| 命令 | 作用 | 输出 |
|---|---|---|
| `/initialize-project` | 初始化项目 | 项目基线文档 |
| `/build-design-system` | 建立 Design System | Design System Spec |
| `/build-api-standard` | 建立 API 标准 | API Governance |
| `/build-test-framework` | 建立测试体系 | Testing Governance |

治理扩展应新建 REQ 或 OpenSpec Change；不得重复创建已经归档的 bootstrap change。

## 9. Change 类型与命名 `[通用]`

| 场景 | 类型 | 命名示例 |
|---|---|---|
| 新能力 | `add-*` | `add-user-login` |
| BUG 修复、验收不达标、策略修正 | `fix-*` | `fix-login-timeout` |
| 规范、文案、配置或契约对齐 | `update-*` | `update-api-error-format` |
| 重构且不改变外部行为 | `refactor-*` | `refactor-user-service` |
| 移除能力或废弃契约 | `remove-*` | `remove-legacy-export` |

已有 archived `add-*` 且验收未过或策略变化时，应新建 `fix-*` 或 `update-*`，禁止在原 change 上无规格地硬改代码。

## 10. 新需求处理流程 `[通用 + 个性化]`

AI 收到新需求时必须：

1. 检查 `issues/requirements/{plan,review,archive}/` 是否已有相关需求。
2. 如没有，使用 `/req-capture` 在 `issues/requirements/plan/` 创建 `REQ-xxxx-name/`。
3. 可选使用 `/req-explore` 澄清背景、角色、边界和风险。
4. 使用 `/req-generate` 生成或更新 `requirement.md`。
5. 使用 `/req-complete` 补齐需求包：
   - `requirement.md`
   - `user-stories.md`
   - `business-flow.md`
   - `acceptance.md`
   - `trace.md`
   - `prototype/`（涉及 UI、交互、页面、端能力时启用）
6. 使用 `/req-review` 完成评审；未 approved 的需求不得进入 Sprint、不得写入 Sprint 规划、不得 `/req-opsx`、不得正式开发；approved 后将整个 REQ 目录移入 `issues/requirements/review/`。
7. 使用 `/req-opsx` 或项目约定 OpenSpec CLI 创建 `openspec/changes/<change-id>/`；执行前必须确认需求已 `approved`。
8. 使用 `/sprint-propose` 纳入迭代；若项目不启用 Sprint，则在 change 中说明开发范围和验收方式。
9. 使用 `/opsx-apply` 或 `/sprint-apply` 实现。
10. 完成验证后更新 `trace.md`、迭代状态、验收记录。
11. 使用 `/opsx-archive` 或 `/sprint-archive` 归档，并将已关闭需求移入 `issues/requirements/archive/`。
12. Sprint 结束后使用 `/sprint-exps` 复盘迭代经验，并沉淀到 `docs/knowledge-base/sprints/`。

## 11. BUG 处理流程 `[通用 + 个性化]`

AI 收到 BUG 时必须：

1. 检查 `issues/bugs/{plan,review,archive}/` 是否已有相关 BUG。
2. 如没有，使用 `/bug-capture` 在 `issues/bugs/plan/` 创建 `BUG-xxxx-name/`。
3. 可选使用 `/bug-explore` 澄清复现、影响面、严重等级和风险。
4. 使用 `/bug-generate` 生成或更新 `bug.md`。
5. 使用 `/bug-complete` 补齐缺陷包：
   - `bug.md`
   - `root-cause.md`
   - `workaround.md`
   - `acceptance.md`
   - `trace.md`
   - `logs/`
   - `screenshots/`
6. 使用 `/bug-review` 完成评审；未 approved 的 BUG 不得进入 Sprint、不得写入 Sprint 规划、不得 `/bug-opsx`、不得正式开发；approved 后将整个 BUG 目录移入 `issues/bugs/review/`。
7. 使用 `/bug-opsx` 创建 `openspec/changes/fix-*`；执行前必须确认 BUG 已 `approved`。
8. 使用 `/opsx-apply` 实现并补充回归测试。
9. 使用 `/opsx-archive` 归档，并将已关闭 BUG 移入 `issues/bugs/archive/`。
10. 如有知识沉淀价值，更新 `docs/knowledge-base/incidents/`。
11. 若缺陷经验影响整个迭代流程或多项需求，Sprint 结束后使用 `/sprint-exps` 统一沉淀。

## 12. OpenSpec 约束 `[通用]`

- `openspec/specs/` 是已生效能力，不得随意直接修改。
- 开发中的变更必须放在 `openspec/changes/`，推荐通过项目约定命令或 `openspec new change` 创建。
- 变更完成后才能归档到 `openspec/changes/archive/` 或项目约定的 archive 目录。
- 归档时才可将能力合并到 `openspec/specs/`。
- delta spec 中 `MODIFIED` 的 `### Requirement:` 标题必须与已有 spec 标题一致。
- 每条 requirement 应包含 MUST/SHALL 等强约束描述，并至少包含一个 `#### Scenario:`。
- 跨模块规格应放在根级 `openspec/`；子项目内部规格可放在子项目自己的 `openspec/`，但必须在根文档中有路由说明。

## 13. 原型与视觉验收优先级 `[条件启用]`

存在 `issues/requirements/.../prototype/`、设计稿、截图或 Golden Reference 时，相关 change 的 `design.md` 必须声明验收优先级。

推荐优先级：

```text
1. prototype/*.html（如存在）
2. prototype/*.png、*.jpg 或设计稿截图（Golden Reference）
3. prototype/*-context.md
4. issues/.../acceptance.md
5. rules/ui-design.md
6. openspec/specs/（已归档能力）
```

如果 acceptance 与原型冲突，应在 `design.md` 中记录冲突处理方式，并通过 delta spec 消化，而不是直接绕过原型修改生产代码。

视觉类 change 的 `tasks.md` 应包含截图对照、断点验收、组件复用和可访问性检查项；`trace.md` 应记录实际验证结果。

## 14. 强制规则 `[通用 + 个性化]`

通用强制规则：

- 不允许绕过 OpenSpec Change 直接开发正式功能。
- 不允许直接修改已归档 `openspec/specs/` 中的正式规范，除非是归档合并动作。
- 不允许在根目录随意新增业务代码。
- 不允许绕过 `rules/directory-structure.md` 新增目录。
- 不允许把需求、BUG、迭代计划散落到 `docs/` 根目录。
- 不允许读取、提交或输出 `.env`、token、secret、私钥、真实用户数据。
- 不允许覆盖用户未要求修改的文件。
- 不允许为了本机临时问题随意改变应用内部端口、数据库类型或部署拓扑。
- 完成前必须运行相关验证命令；无法运行时必须说明原因。

项目个性化强制规则：

```text
后端技术栈：{BACKEND_STACK}
前端技术栈：{FRONTEND_STACK}
数据库：{DATABASE_STACK}
对象存储：{OBJECT_STORAGE_STACK}
异步任务：{ASYNC_TASK_STACK}
算法/模型：{ALGORITHM_STACK}
部署：{DEPLOYMENT_STACK}
```

接口变更后必须同步 API 文档、OpenAPI、客户端类型或跨模块契约。数据库变更后必须同步 schema、迁移、测试数据和兼容性说明。UI 变更后必须同步 Design System、页面验收或视觉基准。部署变更后必须同步 `.env.example`、部署文档和验证命令。

## 15. 目录边界 `[通用 + 个性化]`

### 15.1 推荐顶层目录职责 `[通用]`

| 目录 | 职责 | 备注 |
|---|---|---|
| `AGENTS.md` | AI Agent 全局入口 | 必须优先读取 |
| `README.md` | 面向人类读者的项目入口 | 不替代 AGENTS.md |
| `project.yaml` | 项目结构化元数据 | 初始化和自动化工具可读取 |
| `rules/` | 全局研发规范 | 强制约束 |
| `docs/` | 长期项目记忆 | 架构、部署、接口、数据库、测试、知识库 |
| `issues/requirements/{plan,review,archive}/` | 需求管理 | 每个需求独立目录，按评审/归档状态分区 |
| `issues/bugs/{plan,review,archive}/` | BUG 管理 | 每个 BUG 独立目录，按评审/归档状态分区 |
| `iterations/{change,archive}/` | 迭代管理 | sprint 目标、范围、验收、发布说明；按归档状态分区 |
| `openspec/` | OpenSpec 项目、changes、specs、archive | 能力变更治理 |
| `src/` | 源码目录 | 按模块分层 |
| `tests/` | 测试目录 | unit、integration、e2e、compatibility |
| `scripts/` | 工程脚本 | 验证、生成、部署辅助 |
| `deploy/` | 部署编排、环境模板、发布脚本 | `[条件启用]` |
| `data/` | 本地样例数据、fixtures、演示数据 | 不提交真实数据 |
| `models/` | 模型文件、模型说明、模型校验信息 | 不提交大模型权重 |
| `compatibility/` | 兼容性矩阵和适配规则 | `[条件启用]` |

### 15.2 禁止目录与投放规则 `[个性化]`

项目可以在初始化时定义禁止目录。例如：

```text
{FORBIDDEN_DIRECTORIES}
```

默认建议：

```text
docs/product/
docs/prd/
docs/bugs/
docs/iterations/
```

如需要产品需求，放入：

```text
issues/requirements/plan/REQ-xxxx-name/
```

如需要 BUG 记录，放入：

```text
issues/bugs/plan/BUG-xxxx-name/
```

如需要故障知识沉淀，放入：

```text
docs/knowledge-base/incidents/
```

若需要新增顶层目录或调整模块边界，必须先创建 OpenSpec Change，并说明：

- 为什么现有目录无法承载。
- 新目录职责是什么。
- 会影响哪些文档、测试、脚本和部署文件。

推荐执行目录校验：

```bash
{DIRECTORY_VALIDATE_COMMAND}
```

## 16. 部署与环境要求 `[条件启用]`

本项目部署方式：

```text
{DEPLOYMENT_STACK}
```

如果项目提供脚本，应替换为项目脚本：

```bash
{DOCKER_UP_COMMAND}
{DOCKER_DOWN_COMMAND}
```

服务地址：

```text
{SERVICE_URLS}
```

AI 修改部署时，必须同步检查：

```text
docker-compose.yml
deploy/
.env.example
docs/02-deployment.md
README.md
```

根目录必须保留 `.env.example`，用于说明本项目运行所需环境变量。新增或修改环境变量时，必须同步更新 `.env.example` 和部署文档。`.env` 文件禁止提交。

## 17. API 与跨模块契约 `[条件启用]`

涉及 API、事件、Webhook、SDK、前后端类型或跨模块数据格式时，必须：

- 先读取 `rules/api.md` 和相关契约文档。
- 明确请求、响应、错误码、鉴权、分页、幂等、兼容性。
- 同步更新 OpenAPI 或项目使用的接口描述文件。
- 同步生成或更新客户端类型。
- 补充契约测试、集成测试或兼容性验证。
- 在回复中说明是否影响前端、后端、SDK、移动端、微信小程序或第三方集成。

## 18. 数据、媒体、对象存储与模型文件 `[条件启用]`

`data/` 用于本地开发、演示、测试样例和运行时数据承载。`models/` 用于模型说明、轻量样例、校验信息和下载指引。

AI 涉及以下任务时必须读取并更新相关规则：

- 数据库本地数据文件。
- 样例数据、测试 fixtures、导入导出。
- 图片、音频、视频、文档等媒体上传。
- 对象存储 bucket、目录前缀、访问权限。
- 模型文件、模型权重、模型版本、推理配置。
- 本地运行日志或缓存。

禁止提交：

- 真实客户数据。
- 真实生产素材。
- 运行时数据库文件。
- 临时处理文件。
- 未经确认可入库的大模型权重、商业模型文件或敏感训练数据。

模型文件如体积较大，应在 `models/README.md` 中说明获取方式、版本、校验和、许可和放置路径，而不是直接提交到 Git。

## 19. UI 与 Design System `[条件启用]`

有 Web、移动端、微信小程序或桌面 UI 时，必须启用本节。

### 19.1 资源地图 `[个性化]`

| 层级 | 路径 | 职责 |
|---|---|---|
| 设计规范 | `rules/ui-design.md` | 色彩、字体、间距、组件与页面结构 |
| Design Token | `{DESIGN_TOKEN_PATH}` | 跨端 Token 或主题变量 |
| 基础组件 | `{BASE_COMPONENT_PATH}` | Button、Input、Dialog、Form 等 |
| 复合组件 | `{COMPOSITE_COMPONENT_PATH}` | Search、Table、Sidebar、Pagination 等 |
| 业务组件 | `{BUSINESS_COMPONENT_PATH}` | 领域组件 |
| 页面模板 | `{PAGE_TEMPLATE_PATH}` | 页面骨架和布局 |
| 设计验收 | `{DESIGN_SYSTEM_PREVIEW_URL}` | Token、组件、页面预览 |

### 19.2 AI 执行 UI 任务前必须 `[通用]`

1. 读取 `rules/ui-design.md`。
2. 确认是否已有 Design Token、组件库、页面模板或业务组件。
3. 优先复用现有组件和模板，再考虑新增。
4. 涉及视觉验收时，对照原型、截图、设计稿或验收页。

组件选用优先级应按项目实际生成。例如：

```text
1. 页面模板
2. 业务组件
3. 复合 UI 组件
4. 基础组件
5. 新增组件
```

新增 Design Token、主题、组件、页面模板或交互模式时，必须通过 OpenSpec Change 或项目约定的设计变更流程进入开发。

### 19.3 Token 与样式规则 `[个性化]`

```text
{UI_TOKEN_POLICY}
{UI_COMPONENT_POLICY}
{UI_VISUAL_ACCEPTANCE_POLICY}
```

默认建议：

- 不在业务页面中硬编码可抽象为 token 的颜色、字号、间距、阴影和圆角。
- className、style、主题变量和组件变体应遵守项目 UI 规范。
- 视觉变更必须有可复核的截图、预览页或验收记录。

## 20. 安全规则 `[通用]`

- 不读取或提交 `.env`、token、secret、私钥文件。
- 文档和示例不写真实密钥、真实用户数据或内部凭据。
- 认证、授权、文件上传、输入校验、对象存储访问必须按 `rules/security.md` 执行。
- 涉及权限边界、管理端、租户隔离、审计日志、license 或私有化部署时，必须记录风险和验证方式。
- 不执行破坏性删除、强制 push、重置历史等操作，除非用户明确要求并批准。

## 21. 常用命令 `[个性化]`

初始化时应根据项目实际脚本生成本节。示例：

| 用途 | 命令 |
|---|---|
| 统一验证 | `{PRIMARY_VERIFY_COMMAND}` |
| 目录结构校验 | `{DIRECTORY_VALIDATE_COMMAND}` |
| OpenSpec 校验 | `{OPENSPEC_VALIDATE_COMMAND}` |
| 测试 | `{TEST_COMMAND}` |
| 类型检查 | `{TYPECHECK_COMMAND}` |
| 构建 | `{BUILD_COMMAND}` |
| 本地启动 | `{DEV_COMMAND}` |
| Docker 启动 | `{DOCKER_UP_COMMAND}` |
| Docker 停止 | `{DOCKER_DOWN_COMMAND}` |
| API 客户端生成 | `{API_CLIENT_GENERATE_COMMAND}` |
| Design Token 同步 | `{TOKEN_SYNC_COMMAND}` |

如果命令不存在，应删除或替换，不得保留虚假命令。

## 22. 输出要求 `[通用 + 个性化]`

AI 回复默认使用中文，除非用户明确要求其他语言。

涉及代码修改时必须说明：

- 文件路径。
- 修改原因。
- 是否影响接口契约。
- 是否影响数据库 schema 或迁移。
- 是否影响前端、移动端、微信小程序、算法或部署。
- 是否需要更新文档、OpenAPI、客户端类型或 Design System。
- 执行了哪些验证命令，结果如何。

涉及接口时必须说明请求、响应、错误码和兼容性影响。

涉及数据模型时必须说明表结构、索引、迁移、回滚和测试数据影响。

涉及部署时必须说明服务、端口、环境变量、镜像、volume、网络和回滚影响。

涉及需求或 BUG 时必须说明对应 REQ/BUG、状态、评审结论、关联 change 和验收记录。

## 23. 完成任务后检查清单 `[通用 + 条件启用]`

```text
□ 是否已读取 AGENTS.md 与相关 rules
□ 是否遵守目录结构
□ 是否需要 OpenSpec Change；如需要，是否已创建或更新
□ 是否更新 issues/requirements 或 issues/bugs
□ 是否完成 REQ/BUG 评审状态校验
□ 是否更新 iterations（如项目启用 Sprint）
□ 是否补充或更新 tests
□ 是否更新 docs 长期文档
□ 是否更新 .env.example
□ 是否未提交真实密钥、真实用户数据或运行时文件
□ 是否未覆盖用户未要求修改的文件
□ 是否运行相关验证命令并记录结果
□ API 变更：是否同步 OpenAPI、客户端类型和契约测试
□ 数据库变更：是否同步 schema、迁移、回滚说明和兼容性文档
□ UI 变更：是否复用组件、遵守 Design Token，并完成视觉验收
□ UI 有 prototype：是否声明 HTML / PNG / context / acceptance 优先级
□ 部署变更：是否同步 docker-compose、deploy、端口和部署文档
□ 媒体/对象存储变更：是否遵守 bucket、前缀、权限和上传限制
□ 模型/算法变更：是否说明模型版本、获取方式、校验和与推理验证
□ 完成的 change 是否需要归档到 openspec/specs
□ 多 Agent 命令变更：是否同步到启用工具目录
```

## 24. 初始化生成建议 `[通用]`

工程初始化工具可按以下策略生成项目专属 AGENTS.md：

1. 收集用户输入：产品名称、定位、目标用户、产品形态、技术栈、数据库、部署方式、是否有算法、是否有对象存储、是否有 UI、是否有信创或私有化要求、启用的 Agent 工具。
2. 保留所有 `[通用]` 模块。
3. 用用户输入替换所有 `[个性化]` 占位符。
4. 根据能力开关保留、删除或简化 `[条件启用]` 模块。
5. 根据实际文件生成必读文档清单，不得保留不存在的文档路径。
6. 根据实际命令生成命令表，不得保留不存在的 slash command 或脚本。
7. 扫描生成后的工程目录，删除指向不存在文件或命令的条目。
8. 将缺失但需要人工确认的信息标记为 `待确认`。
9. 输出前检查 AGENTS.md 是否能回答三个问题：
   - AI 任务开始前应该先读什么？
   - 这个项目的目录、模块和命令边界是什么？
   - 改完以后如何验证和汇报？
