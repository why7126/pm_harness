---
purpose: 项目入口说明
content: 产品简介、用户角色、核心能力、技术栈、快速启动、部署入口、目录导航、AI 约束、文档索引与初始化建议
source: Harness README.md 抽象模板，初始化时基于用户输入生成
update_method: 项目定位、技术栈、启动命令、部署方式、目录结构、端口策略或核心能力变化时同步更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {PROJECT_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；本文档是工程根入口，详细规则见 AGENTS.md、rules/ 与 docs/
---

# {PRODUCT_NAME}

## 0. 文档定位 `[通用]`

本文档是 `{PRODUCT_NAME}` 的工程根入口，用于帮助新成员、AI Agent 和自动化初始化流程快速理解项目目标、使用方式、目录结构、运行入口、治理规则和后续文档导航。

根 README 只描述项目“如何被理解和启动”，详细规则不在此展开：

- AI 协作与强制规则：`AGENTS.md`
- 工程规则：`rules/`
- 产品、架构、部署、API、数据库等长文档：`docs/`
- 需求、缺陷、迭代与 OpenSpec：`issues/`、`iterations/`、`openspec/`

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{PRODUCT_DESCRIPTION}` | 产品简介 | 待确认 |
| `{BUSINESS_DOMAIN}` | 业务领域 | 待确认 |
| `{TARGET_USERS}` | 目标用户 | 待确认 |
| `{PRODUCT_FORMS}` | 产品形态 | Web / Admin / API / Mobile / WeChat Miniapp / Desktop |
| `{CORE_CAPABILITIES}` | 核心能力 | 待确认 |
| `{BACKEND_STACK}` | 后端技术栈 | 待确认 |
| `{FRONTEND_STACK}` | 前端技术栈 | 待确认 |
| `{DATABASE_STACK}` | 数据库技术栈 | 待确认 |
| `{OBJECT_STORAGE_STACK}` | 对象存储技术栈 | 待确认 |
| `{ASYNC_TASK_STACK}` | 异步任务技术栈 | 待确认 |
| `{ALGORITHM_STACK}` | 算法/模型技术栈 | 待确认 |
| `{DEPLOYMENT_STACK}` | 部署方式 | 待确认 |
| `{LOCAL_SETUP_COMMANDS}` | 本地初始化命令 | 待确认 |
| `{DEV_COMMANDS}` | 本地开发命令 | 待确认 |
| `{TEST_COMMANDS}` | 测试命令 | 待确认 |
| `{DOCKER_UP_COMMAND}` | Docker 启动命令 | 待确认 |
| `{DOCKER_DOWN_COMMAND}` | Docker 停止命令 | 待确认 |
| `{SERVICE_URLS}` | 本地服务地址 | 待确认 |
| `{DIRECTORY_VALIDATE_COMMAND}` | 目录校验命令 | 待确认 |
| `{PRIMARY_VERIFY_COMMAND}` | 主要验证命令 | 待确认 |
| `{PROJECT_OWNER}` | 项目负责人 | 待确认 |

## 2. 项目简介 `[个性化]`

`{PRODUCT_NAME}` 是面向 `{TARGET_USERS}` 的 `{BUSINESS_DOMAIN}` 项目。

```text
{PRODUCT_DESCRIPTION}
```

项目代码：

```text
{PRODUCT_CODE}
```

产品形态：

```text
{PRODUCT_FORMS}
```

## 3. 用户角色 `[个性化]`

| 用户/角色 | 使用端 | 核心目标 | 关键能力 |
|---|---|---|---|
| `{USER_ROLE_1}` | `{CLIENT_1}` | `{USER_GOAL_1}` | `{ROLE_CAPABILITIES_1}` |
| `{USER_ROLE_2}` | `{CLIENT_2}` | `{USER_GOAL_2}` | `{ROLE_CAPABILITIES_2}` |
| `待确认` | `待确认` | `待确认` | `待确认` |

初始化时应根据用户输入生成真实角色。无多角色项目可合并为单一“用户/操作者/系统调用方”。

## 4. 核心能力 `[个性化]`

```text
{CORE_CAPABILITIES}
```

推荐按以下格式生成：

| 能力 | 面向角色 | 所属端/服务 | 说明 | 状态 |
|---|---|---|---|---|
| `{CAPABILITY_NAME}` | `{ROLE}` | `{FORM_OR_SERVICE}` | `{CAPABILITY_DESCRIPTION}` | planned / active / deprecated |

核心能力必须能追溯到 `docs/00-product-overview.md`、`issues/requirements/` 或 `openspec/changes/`。

## 5. 技术栈 `[通用 + 个性化]`

| 分层 | 技术栈 | 状态 | 说明 |
|---|---|---|---|
| 后端 | `{BACKEND_STACK}` | `{BACKEND_STATUS}` | `{BACKEND_NOTE}` |
| 前端 | `{FRONTEND_STACK}` | `{FRONTEND_STATUS}` | `{FRONTEND_NOTE}` |
| 数据库 | `{DATABASE_STACK}` | `{DATABASE_STATUS}` | `{DATABASE_NOTE}` |
| 对象存储 | `{OBJECT_STORAGE_STACK}` | `{OBJECT_STORAGE_STATUS}` | `{OBJECT_STORAGE_NOTE}` |
| 异步任务 | `{ASYNC_TASK_STACK}` | `{ASYNC_TASK_STATUS}` | `{ASYNC_TASK_NOTE}` |
| 算法/模型 | `{ALGORITHM_STACK}` | `{ALGORITHM_STATUS}` | `{ALGORITHM_NOTE}` |
| 部署 | `{DEPLOYMENT_STACK}` | `{DEPLOYMENT_STATUS}` | `{DEPLOYMENT_NOTE}` |

规则：

- 未启用的分层应标记为 `不适用` 或删除。
- 不得保留来源项目技术栈、服务名、端口、依赖或工具链假设。
- 技术栈必须与 `project.yaml`、`docs/01-architecture.md`、`docs/02-deployment.md`、`rules/environment.md` 一致。

## 6. 快速启动 `[通用 + 个性化]`

本地初始化：

```bash
{LOCAL_SETUP_COMMANDS}
```

本地开发：

```bash
{DEV_COMMANDS}
```

运行测试：

```bash
{TEST_COMMANDS}
```

主要验证：

```bash
{PRIMARY_VERIFY_COMMAND}
```

要求：

- 命令必须来自实际脚本、包管理器、Makefile、Docker Compose 或项目文档。
- 未确认命令必须标记为 `待确认`，不得编造。
- 如果项目需要 `.env`，应从 `.env.example` 复制并按 `rules/environment.md` 配置。

## 7. Docker / 部署入口 `[条件启用 + 个性化]`

当 `{DEPLOYMENT_STACK}` 包含 Docker Compose、本地容器、Kubernetes、Helm、PaaS 或私有化部署时，保留本节；否则标记为“不适用”。

启动：

```bash
{DOCKER_UP_COMMAND}
```

停止：

```bash
{DOCKER_DOWN_COMMAND}
```

本地服务地址：

| 服务 | 地址 | 说明 |
|---|---|---|
| `{SERVICE_NAME}` | `{SERVICE_URL}` | `{SERVICE_NOTE}` |

```text
{SERVICE_URLS}
```

要求：

- 服务名、端口和访问地址必须来自实际配置。
- 不得在 README 中写入真实密码、Token、Access Key 或生产凭据。
- 默认账号、默认密码只能用于本地开发，且必须明确生产环境禁止使用。
- 端口策略必须与 `rules/port-management.md`、`docs/02-deployment.md` 一致。

## 8. 目录说明 `[通用 + 个性化]`

| 目录/文件 | 说明 | 初始化策略 |
|---|---|---|
| `AGENTS.md` | AI Agent 协作入口与强制规则 | 必须保留 |
| `project.yaml` | 项目元数据与初始化参数 | 必须保留 |
| `rules/` | 工程规则、编码、安全、测试、部署等约束 | 必须保留 |
| `docs/` | 产品、架构、部署、API、数据库、标准文档 | 必须保留 |
| `docs/standards/` | API、认证、错误码、测试、上传等专项标准 | 按能力保留 |
| `issues/` | 需求与缺陷治理目录 | 必须保留 |
| `iterations/{change,archive}/` | Sprint 与迭代治理目录 | 条件启用 |
| `openspec/` | OpenSpec 变更与规格事实源 | 条件启用 |
| `releases/` | 产品版本发布对象、公开公告源文件和发布校验材料 | 必须保留 |
| `src/` | 源码目录 | 按技术栈生成 |
| `tests/` | 测试目录 | 按测试策略生成 |
| `data/` | 本地运行时数据、样例数据或缓存 | 条件启用 |
| `models/` | 模型文件、算法权重或模型资产 | 条件启用 |
| `deploy/` | 部署配置、脚本与环境模板 | 条件启用 |

目录约束见：

```text
rules/directory-structure.md
```

目录校验：

```bash
{DIRECTORY_VALIDATE_COMMAND}
```

## 9. AI 协作约束 `[通用]`

AI Agent 修改本项目时必须：

- 先阅读 `AGENTS.md`。
- 遵守 `rules/` 下的工程规则。
- 不随意新增顶层目录，不把需求、Bug、迭代、OpenSpec 文档放错位置。
- 修改技术栈、目录、端口、部署、测试、API、数据库、对象存储或安全策略时，同步更新对应文档。
- 不保留来源项目业务名、路径、端口、服务、账号、密码、bucket、表名、接口或测试示例。
- 执行必要验证，并在无法验证时说明原因。

## 10. 文档导航 `[通用]`

| 想了解 | 阅读 |
|---|---|
| AI 协作规则 | `AGENTS.md` |
| 产品定位 | `docs/00-product-overview.md` |
| 系统架构 | `docs/01-architecture.md` |
| 部署方式 | `docs/02-deployment.md` |
| API 总览 | `docs/03-api-index.md` |
| 数据库设计 | `docs/04-database-design.md` |
| 兼容矩阵 | `docs/05-compatibility-matrix.md` |
| 媒体/视频资产 | `docs/06-video-asset-management.md` |
| 对象存储策略 | `docs/07-object-storage-strategy.md` |
| 文档目录说明 | `docs/README.md` |
| API/认证/错误码/测试等标准 | `docs/standards/` |

## 11. 项目治理命令 `[通用 + 个性化]`

默认支持以下自定义命令族，具体技能入口位于 `.agents/skills/`：

| 命令族 | 命令 |
|---|---|
| 综合捕获 | `/capture` |
| 需求治理 | `/req-capture`、`/req-explore`、`/req-generate`、`/req-complete`、`/req-review`、`/req-opsx` |
| 缺陷治理 | `/bug-capture`、`/bug-explore`、`/bug-generate`、`/bug-complete`、`/bug-review`、`/bug-opsx` |
| Sprint 治理 | `/sprint-propose`、`/sprint-explore`、`/sprint-apply`、`/sprint-exps`、`/sprint-archive` |
| OpenSpec | `/opsx-explore`、`/opsx-propose`、`/opsx-apply`、`/opsx-archive` |
| 小程序发布辅助 | `/miniapp-env`、`/miniapp-check`、`/miniapp-prepare`、`/miniapp-confirm`、`/miniapp-restore` |
| 发布治理 | `/release-propose`、`/release-prepare`、`/release-publish` |
| 项目基线 | `/initialize-project`、`/build-design-system`、`/build-api-standard`、`/build-test-framework` |

项目可根据实际启用能力补充命令说明，但不得改变默认命令的阶段、输入、输出和是否生成代码边界；不得新增或恢复其它 Agent 工具目录。

## 12. 初始化建议 `[通用]`

初始化生成 README 时应执行：

1. 替换 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_DESCRIPTION}`、`{BUSINESS_DOMAIN}`、`{TARGET_USERS}`、`{PRODUCT_FORMS}`、`{CORE_CAPABILITIES}`。
2. 根据项目能力生成技术栈、目录说明、服务地址和命令。
3. 根据是否启用 Web、Admin、API、Mobile、WeChat Miniapp、Desktop、对象存储、媒体、算法/模型、Docker、Kubernetes 保留或删除 `[条件启用]` 内容。
4. 命令、端口、URL、服务名必须来自真实配置；未知时标记 `待确认`。
5. 不得保留来源项目产品名、用户角色、技术栈、端口、服务地址、默认账号密码、bucket、表名或业务能力。
6. 保持 README 与 `AGENTS.md`、`project.yaml`、`docs/00-product-overview.md`、`docs/01-architecture.md`、`docs/02-deployment.md`、`rules/directory-structure.md`、`rules/environment.md`、`rules/port-management.md` 一致。

## 13. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- 产品名称、定位、目标用户、核心能力或产品形态变化。
- 技术栈、源码目录、测试目录、部署方式或服务地址变化。
- 启动命令、测试命令、验证命令、Docker/部署命令变化。
- 端口策略、环境变量、对象存储、模型文件、运行时数据或安全策略变化。
- AI 协作规则、命令体系、目录治理或文档导航变化。
