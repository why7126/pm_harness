---
purpose: AI 行为入口
content: AI 开发流程入口、规则加载路由、OpenSpec 红线、目录与验证边界
source: Harness AGENTS.md Token 优化模板
update_method: 项目初始化时由用户输入参数生成；初始化后由项目团队确认；后续由 AI 辅助更新并经人工 Review
created_at: 2026-06-27 08:44:18
updated_at: 2026-07-14 00:00:00
note: 适用于 {PRODUCT_NAME} 项目；AI 执行任何任务前必须优先阅读本文档
template_scope: 可作为工程初始化时的 AGENTS.md 模块
---

# AI Agent 工作指南

## 1. 项目定位

{PRODUCT_NAME} 是一个 {BUSINESS_DOMAIN} 领域项目，采用 OpenSpec + AI Agent 规范编程方式开发。

- 产品定位：{PRODUCT_DESCRIPTION}
- 目标用户：{TARGET_USERS}
- 产品形态：{PRODUCT_FORMS}
- 技术栈：后端 `{BACKEND_STACK}`；前端 `{FRONTEND_STACK}`；数据库 `{DATABASE_STACK}`；对象存储 `{OBJECT_STORAGE_STACK}`；异步任务 `{ASYNC_TASK_STACK}`；算法/模型 `{ALGORITHM_STACK}`；部署 `{DEPLOYMENT_STACK}`

项目状态不得只存在于对话中。需求、BUG、迭代、规格、验证结果和归档记录必须沉淀到 `issues/`、`iterations/`、`openspec/`、`docs/`、`rules/` 等可审计位置。

## 2. 执行前读取路由

所有任务先读最小入口：

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/language.md
rules/agent-context-budget.md
```

按任务类型追加读取；只读相关章节，避免无差别读取整目录。

| 任务类型 | 追加读取 |
|---|---|
| REQ / BUG 流程 | `rules/requirement-management.md`、`rules/bug-management.md`、`rules/issues-lifecycle.md`、对应 `issues/**/<REQ|BUG-*` |
| Sprint 流程 | `rules/iterations-lifecycle.md`、相关 `iterations/change|archive/<sprint>/` 片段 |
| OpenSpec Change | 当前 `openspec/changes/<change-id>/`、`rules/document-governance.md` |
| 代码实现 | `rules/coding.md`、`rules/testing.md`、相关模块 README/AGENTS；涉及契约时追加 API/DB/UI 等专项规则 |
| API 变更 | `rules/api.md`、`docs/03-api-index.md`、OpenAPI 来源、客户端生成配置 |
| DB / 数据模型 | `rules/database.md`、`docs/04-database-design.md` 相关表段、schema / migration 文件 |
| UI / Design System | `rules/ui-design.md`、前端 README、Design Token、组件库、视觉验收入口 |
| Docker / 发布部署 | `rules/environment.md`、`rules/port-management.md`、`rules/release.md`、`docs/02-deployment.md`、`docker-compose*.yml` |
| data / media / object storage | `rules/data-management.md`、`rules/media.md`、`rules/object-storage.md`、相关存储策略文档 |
| 安全 / 权限 / 敏感数据 | `rules/security.md`，以及 API、数据、部署相关规则 |
| 兼容性 / 私有化 | `rules/compatibility.md`、`compatibility/`、部署矩阵 |
| 文档 / 目录 / 模板变更 | `rules/document-governance.md`、`rules/directory-structure.md`；若改模板，同步 `pm-harness/` 与 `pm-harness-skills/pm-harness-init/assets/pm-harness-template/` |

若文件不存在，应说明缺失并使用最接近的已有规则；不得编造不存在的规则内容。

## 3. Agent 工具入口

模板默认以 `.agents/skills/` 作为低噪声统一命令入口：

```text
.agents/skills/
```

历史工具目录（如 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/`）如需保留，必须与 `.agents/skills/` 的输入、输出、是否允许生成代码和状态同步语义一致。新增或移除工具入口时，必须同步更新 `rules/directory-structure.md`、`scripts/validate-directory-structure.py` 和模板同步校验。

## 4. 开发流程总览

```text
idea / bug / change
-> issues/requirements 或 issues/bugs
-> review
-> openspec/changes
-> iterations/change（可选但 REQ/BUG 来源的 Change 在 apply 前必须纳入 Sprint）
-> implementation
-> verification
-> archive
```

- 轻量文档修订、注释、拼写、无行为变化的小改动可不新建 OpenSpec Change。
- 改变业务能力、接口契约、数据结构、部署拓扑、权限边界、工作流语义或团队流程时，必须走 OpenSpec Change。
- `openspec/specs/` 是已生效能力；除归档合并动作外不得直接修改。

## 5. 命令族速查

| 域 | 命令链 |
|---|---|
| 智能收集 | `/capture` |
| 需求 | `/req-capture` -> `/req-generate` -> `/req-complete` -> `/req-review --approve` -> `/req-opsx` |
| 缺陷 | `/bug-capture` -> `/bug-generate` -> `/bug-complete` -> `/bug-review --approve` -> `/bug-opsx` |
| Change | `/opsx-propose`、`/opsx-explore`、`/opsx-apply`、`/opsx-archive` |
| Sprint | `/sprint-propose`、`/sprint-explore`、`/sprint-apply`、`/sprint-archive`、`/sprint-exps` |
| Bootstrap | `/initialize-project`、`/build-design-system`、`/build-api-standard`、`/build-test-framework` |

工作流状态变化后运行：

```bash
python scripts/sync-workflow-status.py --event <event> [--req REQ-xxxx] [--bug BUG-xxxx] [--change change-id] [--sprint sprint-xxx|auto]
```

归档涉及 Issue 物理阶段迁移时继续运行：

```bash
python scripts/promote-issue-stage.py --to archive [--change change-id] [--sprint sprint-xxx] --reason "<event>"
```

## 6. 强制红线

- 不允许绕过 OpenSpec Change 直接开发正式功能。
- 不允许直接修改 `openspec/specs/`，除归档合并动作外。
- 未评审的 REQ/BUG 不得进入 Sprint 正式规划，不得 `/req-opsx`、`/bug-opsx`、`/sprint-apply`。
- 来源于 REQ/BUG 的 OpenSpec Change 在 `/opsx-apply` 前必须先纳入某个 `sprint-xxx`。
- 新建业务代码不得放根目录；目录边界以 `rules/directory-structure.md` 为准。
- 禁止把需求、BUG、迭代计划散落到 `docs/` 根目录。
- `.env`、真实密钥、真实客户数据、运行时数据库文件、临时大文件不得提交。
- API 变更必须同步 OpenAPI / 客户端生成物 / docs / tests。
- DB 结构变更必须同步 schema、数据库文档和测试。
- UI 变更必须遵守 Design System token 与组件复用规则。
- 完成前必须运行相关验证命令；无法运行时必须说明原因。

## 7. 文档与时间规范

新增或更新 Markdown：

- Frontmatter 必须含 `created_at` 与 `updated_at`。
- 时间字段统一 `YYYY-MM-DD HH:mm:ss`，默认 `Asia/Shanghai`。
- 更新文档只改 `updated_at`，不得改 `created_at`。

详见 `rules/document-governance.md`。

## 8. 目录边界速查

| 内容 | 位置 |
|---|---|
| 需求 | `issues/requirements/{plan,review,archive}/REQ-*` |
| BUG | `issues/bugs/{plan,review,archive}/BUG-*` |
| Sprint | `iterations/{change,archive}/sprint-*` |
| OpenSpec 变更 | `openspec/changes/<change-id>/` |
| 正式规格 | `openspec/specs/<capability>/spec.md` |
| 复盘 / 事故知识 | `docs/knowledge-base/` |
| 发布对象 | `releases/vX.Y.Z/`（如项目启用） |
| 本地数据 | `data/`（不得提交真实客户数据和运行时数据库） |

## 9. 输出要求

回复默认中文。涉及代码必须说明：

- 文件路径与修改原因。
- 是否影响 API、数据库、UI、部署、安全或跨模块契约。
- 是否需要客户端生成、Docker Compose 验证或人工确认。
- 是否补充或更新测试。
- 遵循了哪些 `rules/` 文件。

## 10. 完成检查清单

```text
□ 是否遵守 OpenSpec Change 流程
□ 来源于 REQ/BUG 的 Change 是否已纳入 sprint-xxx 后再 opsx-apply
□ 是否更新 issues / openspec / iterations / docs / releases（按需）
□ 是否运行 Workflow Sync（状态变化时）
□ 是否补充或更新 tests
□ 是否同步 API / DB / 客户端生成物 / .env.example（按需）
□ 是否遵守目录结构与禁止目录
□ 是否完成必要校验：目录结构、OpenSpec、Agent 上下文预算、测试、Docker（按需）
```
