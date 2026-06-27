---
purpose: OpenSpec 项目上下文
content: 项目背景、产品范围、技术栈、变更流程、规格目录、AI 执行约束、测试映射和同步关系
source: Harness openspec/project.md 抽象模板，初始化时基于用户输入、project.yaml、docs 与 rules 生成
update_method: 项目定位、能力范围、技术栈、OpenSpec 流程、规格目录或 AI 执行规则变化时同步更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {PRODUCT_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；AI 执行 OpenSpec 变更前必须先阅读本文档和目标 Change
---

# OpenSpec 项目上下文

## 0. 文档定位 `[通用]`

本文档是 `{PRODUCT_NAME}` 的 OpenSpec 项目上下文，用于告诉 AI Agent 和研发人员：

- 项目为什么存在。
- 当前产品范围和能力边界是什么。
- 技术栈、目录和规格事实源在哪里。
- 需求、缺陷、Sprint 与 OpenSpec Change 如何流转。
- AI 在执行 OpenSpec 变更前必须遵守哪些约束。

本文档不替代 `AGENTS.md`、`README.md`、`project.yaml`、`rules/` 或 `docs/`，而是 OpenSpec 体系下的项目总入口。

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{PRODUCT_OWNER}` | 产品/项目负责人 | 待确认 |
| `{PRODUCT_DESCRIPTION}` | 产品简介 | 待确认 |
| `{BUSINESS_DOMAIN}` | 业务领域 | 待确认 |
| `{TARGET_USERS}` | 目标用户 | 待确认 |
| `{PRODUCT_FORMS}` | 产品形态 | Web / Admin / API / Mobile / WeChat Miniapp / Desktop |
| `{CORE_CAPABILITIES}` | 核心能力 | 待确认 |
| `{OUT_OF_SCOPE}` | 当前不做的范围 | 待确认 |
| `{BACKEND_STACK}` | 后端技术栈 | 待确认 |
| `{FRONTEND_STACK}` | 前端技术栈 | 待确认 |
| `{DATABASE_STACK}` | 数据库技术栈 | 待确认 |
| `{OBJECT_STORAGE_STACK}` | 对象存储技术栈 | 待确认 |
| `{ASYNC_TASK_STACK}` | 异步任务技术栈 | 待确认 |
| `{ALGORITHM_STACK}` | 算法/模型技术栈 | 待确认 |
| `{DEPLOYMENT_STACK}` | 部署方式 | 待确认 |
| `{OPENSPEC_ENABLED}` | 是否启用 OpenSpec | true / false |
| `{CHANGE_ID_PATTERN}` | Change ID 规则 | add-* / fix-* / change-* |
| `{SPEC_MODULES}` | 规格模块清单 | 待确认 |
| `{PRIMARY_VERIFY_COMMAND}` | 主要验证命令 | 待确认 |

## 2. 项目背景 `[个性化]`

`{PRODUCT_NAME}` 是面向 `{TARGET_USERS}` 的 `{BUSINESS_DOMAIN}` 项目。

```text
{PRODUCT_DESCRIPTION}
```

项目代码：

```text
{PRODUCT_CODE}
```

项目负责人：

```text
{PRODUCT_OWNER}
```

## 3. 产品范围 `[通用 + 个性化]`

产品形态：

```text
{PRODUCT_FORMS}
```

核心能力：

```text
{CORE_CAPABILITIES}
```

当前不做的范围：

```text
{OUT_OF_SCOPE}
```

生成要求：

- 能力范围必须与 `docs/00-product-overview.md` 一致。
- 不确定能力必须标记为 `待确认`，不得作为已承诺规格。
- 不在当前范围内的能力不得进入 `openspec/specs/` 正式规格。

## 4. 技术栈上下文 `[通用 + 个性化]`

| 分层 | 技术栈 | OpenSpec 影响 |
|---|---|---|
| 后端 | `{BACKEND_STACK}` | API、服务、数据库、鉴权、任务、测试 |
| 前端 | `{FRONTEND_STACK}` | 页面、组件、API Client、前端测试 |
| 数据库 | `{DATABASE_STACK}` | Schema、迁移、兼容、数据测试 |
| 对象存储 | `{OBJECT_STORAGE_STACK}` | 上传、下载、权限、生命周期 |
| 异步任务 | `{ASYNC_TASK_STACK}` | 任务状态、重试、幂等、失败恢复 |
| 算法/模型 | `{ALGORITHM_STACK}` | 模型输入输出、评估、部署、回滚 |
| 部署 | `{DEPLOYMENT_STACK}` | 环境、端口、服务拓扑、发布验证 |

要求：

- 技术栈必须与 `project.yaml`、`docs/01-architecture.md`、`docs/02-deployment.md` 一致。
- 未启用技术栈不得作为 Change 的实现前提。
- 技术栈变化必须评估现有 specs、changes、测试和兼容性。

## 5. OpenSpec 目录职责 `[通用]`

| 路径 | 职责 |
|---|---|
| `openspec/project.md` | OpenSpec 项目上下文 |
| `openspec/config.yaml` | OpenSpec 配置 |
| `openspec/changes/` | 进行中的变更提案、设计、任务和规格增量 |
| `openspec/specs/` | 已归档、已生效的正式能力规格 |
| `openspec/archive/` | 已完成 Change 的归档记录 |
| `openspec/testing-mapping.md` | 需求、变更与测试映射 |

## 6. 研发事实源 `[通用]`

| 类型 | 来源 | 说明 |
|---|---|---|
| 产品背景 | `docs/00-product-overview.md` | 产品定位、角色、核心能力 |
| 架构边界 | `docs/01-architecture.md` | 模块、数据流、技术栈 |
| 部署上下文 | `docs/02-deployment.md` | 服务拓扑、环境、端口、持久化 |
| API 上下文 | `docs/03-api-index.md`、`docs/standards/api-governance.md` | API 设计和契约 |
| 数据上下文 | `docs/04-database-design.md`、`rules/database.md` | Schema、迁移和数据规则 |
| 测试上下文 | `rules/testing.md`、`docs/standards/testing-governance.md` | 测试分层和门禁 |
| 需求来源 | `issues/requirements/` | 用户输入和 PRD |
| 缺陷来源 | `issues/bugs/` | Bug 复现、根因和回归 |
| 迭代来源 | `iterations/{change,archive}/` | Sprint 计划和执行 |
| 正式规格 | `openspec/specs/` | 当前系统应满足的能力 |

## 7. Change ID 与状态规则 `[通用 + 个性化]`

Change ID 规则：

```text
{CHANGE_ID_PATTERN}
```

推荐命名：

| 类型 | Change ID | 说明 |
|---|---|---|
| 新能力 | `add-{capability}` | 新增用户可感知能力 |
| 行为修改 | `change-{capability}` | 修改既有能力行为 |
| 缺陷修复 | `fix-{bug-or-capability}` | 修复缺陷并补回归 |
| 重构 | `refactor-{module}` | 不改变外部行为的内部调整 |
| 移除 | `remove-{capability}` | 删除能力或废弃接口 |

规则：

- Change ID 必须短、可读、语义明确。
- 一个 Change 应聚焦一个业务目标。
- 不得把无关修复、重构和新功能混入同一 Change。
- Bug 转 Change 时应能追溯到 `issues/bugs/`。
- 需求转 Change 时应能追溯到 `issues/requirements/`。

## 8. 规格模块 `[通用 + 个性化]`

规格模块清单：

```text
{SPEC_MODULES}
```

推荐按能力或领域组织：

| Spec 模块 | 覆盖能力 | 来源 | 状态 |
|---|---|---|---|
| `{SPEC_MODULE_NAME}` | `{CAPABILITY}` | `{SOURCE_REQUIREMENT_OR_CHANGE}` | draft / active / deprecated |

要求：

- `openspec/specs/` 只保存已生效规格。
- 未实现、未评审或未归档的能力不得写入正式 spec。
- Change 中的 spec delta 必须能归档到对应 spec 模块。

## 9. OpenSpec 执行流程 `[通用]`

推荐流程：

1. 从需求、Bug、Sprint 或人工指令识别变更目标。
2. 创建 `openspec/changes/{change-id}/`。
3. 编写 `proposal.md`、`design.md`、`tasks.md` 和必要的 `specs/*/spec.md` delta。
4. 运行 OpenSpec 校验。
5. 评审通过后再进入实现。
6. 实现时同步测试、文档和规则。
7. 验证通过后归档 Change，并更新正式 spec。

不得跳过：

- 需求或 Bug 追溯。
- 设计和规格评审。
- 测试映射。
- 文档同步。
- 归档或状态更新。

## 10. AI 执行约束 `[通用]`

AI 执行 OpenSpec 相关任务前必须：

1. 阅读 `AGENTS.md`。
2. 阅读本文档。
3. 阅读目标 Change 或相关 spec。
4. 阅读与变更相关的 `rules/` 和 `docs/`。
5. 确认变更是否需要测试、文档、数据库、API、兼容性或部署同步。

AI 禁止：

- 未阅读 Change 就直接改代码。
- 把需求文档直接当作已批准规格。
- 修改正式 spec 而不保留 Change 追溯。
- 绕过测试或删除失败测试。
- 保留来源项目业务名、技术栈、端口、路径、角色、对象存储、表名或示例。
- 在未知信息上编造实现细节。

## 11. 测试与验收映射 `[通用 + 个性化]`

主要验证命令：

```bash
{PRIMARY_VERIFY_COMMAND}
```

要求：

- 每个 Change 必须说明对应测试类型：单元、集成、API、前端、E2E、兼容性、安全或人工验收。
- Bug 修复必须补充回归测试或说明例外。
- API Change 必须评估契约、错误码、认证授权和客户端生成。
- 数据库 Change 必须评估迁移、回滚、兼容性和测试数据。
- 部署 Change 必须评估环境变量、端口、服务拓扑和回滚。

测试映射见：

```text
openspec/testing-mapping.md
```

## 12. 与项目文档同步关系 `[通用]`

OpenSpec Change 影响以下内容时必须同步：

| 影响范围 | 同步文档 |
|---|---|
| 产品范围 | `docs/00-product-overview.md`、`README.md` |
| 架构/模块 | `docs/01-architecture.md`、`rules/coding.md` |
| 部署/环境 | `docs/02-deployment.md`、`rules/environment.md`、`docker-compose.yml` |
| API | `docs/03-api-index.md`、`rules/api.md`、`docs/standards/api-governance.md` |
| 数据库 | `docs/04-database-design.md`、`rules/database.md` |
| 兼容性 | `docs/05-compatibility-matrix.md`、`rules/compatibility.md` |
| 媒体/上传 | `docs/06-video-asset-management.md`、`docs/standards/file_upload.md` |
| 对象存储 | `docs/07-object-storage-strategy.md`、`rules/object-storage.md` |
| 测试 | `rules/testing.md`、`docs/standards/testing-governance.md` |
| 发布 | `rules/release.md`、发布说明 |

## 13. 初始化生成建议 `[通用]`

初始化生成本文档时应执行：

1. 根据用户输入替换 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_OWNER}`、`{PRODUCT_DESCRIPTION}`、`{BUSINESS_DOMAIN}`、`{TARGET_USERS}`、`{PRODUCT_FORMS}`、`{CORE_CAPABILITIES}`、`{OUT_OF_SCOPE}`。
2. 根据 BACKEND_STACK、FRONTEND_STACK、DATABASE_STACK、OBJECT_STORAGE_STACK、ASYNC_TASK_STACK、ALGORITHM_STACK、DEPLOYMENT_STACK 生成技术栈上下文。
3. 根据是否启用 OpenSpec 生成目录职责、Change ID、规格模块和执行流程；未启用 OpenSpec 时标记为“不适用”，并指向项目等价变更系统。
4. 根据需求、Bug、Sprint、API、数据库、测试和部署能力生成事实源与同步关系。
5. 未确认的信息标记为 `待确认`，不得编造规格模块、命令、技术栈或能力范围。
6. 不得保留来源项目业务名、用户角色、技术栈、路径、端口、对象存储、数据库或示例。
7. 保持本文档与 `AGENTS.md`、`project.yaml`、`README.md`、`docs/00-product-overview.md`、`docs/01-architecture.md`、`rules/document-governance.md` 一致。

## 14. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- 项目定位、目标用户、产品形态、核心能力或范围边界变化。
- 技术栈、部署方式、数据库、对象存储、算法/模型能力变化。
- OpenSpec Change 流程、目录、命名规则或规格模块变化。
- 需求、Bug、Sprint、发布或测试治理流程变化。
- AI 执行约束、验证命令或文档同步规则变化。
