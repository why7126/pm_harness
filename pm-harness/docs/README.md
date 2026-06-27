---
purpose: docs 目录总索引
content: 项目主文档、专项治理文档、知识库、需求/缺陷/迭代边界、文档维护规则和初始化生成说明
source: Harness docs/README.md 抽象模板，初始化时基于用户输入生成
update_method: 新增、删除、移动 docs 文档，或调整文档分层、命名、治理规则时同步更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {DOCS_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；作为 docs 目录的第一阅读入口
---

# 文档索引

## 0. 文档定位 `[通用]`

本文档是 `docs/` 目录的总入口，用于帮助项目成员和 AI Agent 快速理解：

- 项目主文档的阅读顺序。
- 专项治理文档的适用范围。
- 知识库、需求、缺陷、迭代文档的存放边界。
- 新增文档时的命名、编号、归档和同步规则。
- 工程初始化时如何根据用户输入生成符合项目要求的文档索引。

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{DOCS_OWNER}` | 文档负责人 | 待确认 |
| `{PRODUCT_FORMS}` | 产品形态 | Web / 管理后台 / API / 微信小程序 / 移动端 / 桌面端 |
| `{BACKEND_STACK}` | 后端技术栈 | 待确认 |
| `{FRONTEND_STACK}` | 前端技术栈 | 待确认 |
| `{DATABASE_STACK}` | 数据库技术栈 | 待确认 |
| `{OBJECT_STORAGE_ENABLED}` | 是否启用对象存储 | true / false |
| `{MEDIA_ENABLED}` | 是否启用媒体/视频能力 | true / false |
| `{DEPLOYMENT_STACK}` | 部署方式 | Docker Compose / Kubernetes / Serverless / 待确认 |
| `{DOCUMENT_GOVERNANCE_POLICY}` | 文档治理策略 | 待确认 |

## 2. 文档分层 `[通用]`

`docs/` 目录按职责分为三层：

| 层级 | 范围 | 作用 | 编号规则 |
|---|---|---|---|
| 层 1：主文档 | `docs/00-*.md` 到 `docs/99-*.md` | 项目级核心说明，按阅读顺序排列 | 使用两位数字前缀 |
| 层 2：专项治理文档 | `docs/standards/*.md` | API、测试、鉴权、上传、错误码等细则 | 不强制编号 |
| 层 3：知识库 | `docs/knowledge-base/` | 故障、经验、决策背景和复盘沉淀 | 按主题命名 |

主文档用于建立项目全局理解；专项治理文档用于约束某一类实现；知识库用于沉淀历史经验。

## 3. 主文档阅读顺序 `[通用 + 个性化]`

以下主文档按推荐阅读顺序排列。初始化时应根据项目能力保留或删除条件启用文档。

| 顺序 | 文档 | 模块属性 | 说明 | 生成条件 |
|---|---|---|---|---|
| 00 | [00-product-overview.md](00-product-overview.md) | `[通用 + 个性化]` | 产品定位、用户、场景、边界和目标 | 必须保留 |
| 01 | [01-architecture.md](01-architecture.md) | `[通用 + 个性化]` | 系统架构、模块边界、技术选型和运行链路 | 必须保留 |
| 02 | [02-deployment.md](02-deployment.md) | `[通用 + 个性化]` | 环境、部署、配置、运维和发布说明 | 必须保留 |
| 03 | [03-api-index.md](03-api-index.md) | `[条件启用 + 个性化]` | API 分组、接口清单、契约来源和错误码入口 | 存在 API 时保留 |
| 04 | [04-database-design.md](04-database-design.md) | `[条件启用 + 个性化]` | 数据库选型、表结构、迁移和数据安全 | 存在数据库时保留 |
| 05 | [05-compatibility-matrix.md](05-compatibility-matrix.md) | `[通用 + 个性化]` | 端、运行时、数据库、部署和能力兼容性矩阵 | 必须保留 |
| 06 | [06-video-asset-management.md](06-video-asset-management.md) | `[条件启用 + 个性化]` | 视频与富媒体资产管理 | 启用媒体/视频时完整保留 |
| 07 | [07-object-storage-strategy.md](07-object-storage-strategy.md) | `[条件启用 + 个性化]` | 对象存储选型、桶策略、key、生命周期和迁移 | 启用对象存储时完整保留 |

新增主文档规则：

- 新增主文档应占用下一个未使用编号，例如 `08-*.md`。
- 主文档必须服务于项目级理解，不得把具体需求、缺陷或迭代计划放入 `docs/` 根目录。
- 主文档新增、删除或改名后，必须同步更新本文档和 `DOCUMENT_METADATA_INDEX.md`。

## 4. 专项治理文档 `[通用 + 条件启用]`

专项治理文档用于约束跨需求、跨模块的工程规范。初始化时应根据项目能力和技术栈生成真实清单。

| 文档 | 模块属性 | 说明 | 生成条件 |
|---|---|---|---|
| [api-governance.md](standards/api-governance.md) | `[条件启用]` | API 风格、响应结构、分页、幂等和契约规则 | 存在 API 时保留 |
| [openapi-rules.md](standards/openapi-rules.md) | `[条件启用]` | OpenAPI 契约、客户端生成和注解规则 | 启用 OpenAPI 时保留 |
| [error-codes.md](standards/error-codes.md) | `[通用]` | 错误码分段、登记和维护规则 | 建议保留 |
| [authentication.md](standards/authentication.md) | `[条件启用]` | 登录、认证、会话和权限入口 | 存在认证时保留 |
| [file_upload.md](standards/file_upload.md) | `[条件启用]` | 文件上传、校验、存储和安全规则 | 存在上传能力时保留 |
| [testing-governance.md](standards/testing-governance.md) | `[通用]` | 测试分层、准入和治理要求 | 建议保留 |
| [unit-test-standard.md](standards/unit-test-standard.md) | `[通用]` | 单元测试边界、命名和覆盖要求 | 建议保留 |
| [frontend-test-standard.md](standards/frontend-test-standard.md) | `[条件启用]` | 前端测试范围、交互验证和视觉检查 | 存在前端时保留 |
| [test-coverage.md](standards/test-coverage.md) | `[通用]` | 覆盖率目标、例外和统计方式 | 建议保留 |

专项治理文档统一放入 `docs/standards/` 子目录。新增专项文档时，应同步更新本文档、`rules/document-governance.md` 和相关引用。

## 5. 知识库 `[通用]`

知识库目录：

```text
docs/knowledge-base/
```

用途：

- 故障复盘。
- 常见问题。
- 设计决策背景。
- Sprint 经验复盘。
- 运维经验。
- 兼容性或迁移经验。

入口文档：

- [knowledge-base/README.md](knowledge-base/README.md)

知识库文档应按主题命名，不使用主文档编号。

## 5.1 兼容性专项文档 `[通用 + 条件启用]`

兼容性专项文档不放在 `docs/` 目录，而放在根目录 `compatibility/` 下，作为可独立测试和维护的适配事实源。

| 目录 | 说明 | 启用条件 |
|---|---|---|
| `compatibility/database/` | 数据库迁移、数据库适配和兼容测试矩阵 | 使用数据库时 |
| `compatibility/devices/` | Web、微信小程序、H5、桌面端、Android、iOS 等端兼容 | 启用对应产品形态时 |
| `compatibility/object-storage/` | MinIO、S3、COS、OSS、OBS、RustFS 等对象存储适配 | 启用对象存储时 |

新增或删除 compatibility 文档时，必须同步更新 `DOCUMENT_METADATA_INDEX.md`、`docs/05-compatibility-matrix.md` 和 `rules/compatibility.md`。

## 6. 不属于 docs 根目录的内容 `[通用]`

以下内容不得放入 `docs/` 根目录：

| 类型 | 路径 | 说明 |
|---|---|---|
| 需求 | `issues/requirements/{plan,review,archive}/REQ-*` | 单个需求、用户故事、验收和追踪 |
| 缺陷 | `issues/bugs/{plan,review,archive}/BUG-*` | 缺陷记录、复现、修复和回归 |
| 迭代 | `iterations/sprint-xxx/` | Sprint 计划、验收报告和发布说明 |
| OpenSpec 变更 | `openspec/changes/<change-id>/` | 提案、设计、任务和规格变更 |
| OpenSpec 规格 | `openspec/specs/<capability>/` | 长期有效的能力规格 |

禁止为了兼容旧习惯恢复以下目录：

```text
docs/prd/
docs/bugs/
docs/iterations/
docs/requirements/
```

## 7. 文档维护规则 `[通用]`

- 新增、删除、移动或重命名文档时，必须同步更新本文档。
- 修改文档职责或路径时，必须同步更新 `rules/document-governance.md`。
- 涉及产品范围变化时，必须同步更新 `00-product-overview.md`。
- 涉及架构、部署、API、数据库、兼容性、媒体或对象存储变化时，必须同步更新对应编号文档。
- 文档中不得保留来源项目的产品名、业务场景、端名称、数据库、bucket、接口路径或命令。
- 未知信息应标记为 `待确认`，不得编造。

## 8. AI Agent 使用规则 `[通用]`

AI Agent 修改项目时应遵循：

1. 先读取本文档，确认文档入口和职责边界。
2. 再读取与任务相关的主文档和专项治理文档。
3. 修改代码、配置或测试后，检查是否需要同步更新文档。
4. 新增文档时，判断应放入主文档、专项治理、知识库、需求、缺陷、迭代还是 OpenSpec。
5. 不得把单个需求的过程材料沉淀到 `docs/` 根目录。

## 9. 初始化生成建议 `[通用]`

工程初始化生成 `docs/README.md` 时应执行：

1. 基于用户输入生成 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、技术栈和能力开关。
2. 保留所有 `[通用]` 模块。
3. 根据能力开关保留或删除 `[条件启用]` 文档条目。
4. 用用户输入替换 `[个性化]` 内容。
5. 删除来源项目业务残留。
6. 确保本文档中的路径真实存在，或明确标记为 `计划创建`。
7. 保持本文档与 `rules/document-governance.md`、`DOCUMENT_METADATA_INDEX.md`、`AGENTS.md`、主 `README.md` 一致。

## 10. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- `docs/` 下新增、删除、移动或重命名文档。
- 主文档编号、阅读顺序或职责变化。
- 专项治理文档路径或范围变化。
- 知识库分类或入口变化。
- 需求、缺陷、迭代、OpenSpec 的存放边界变化。
- 工程初始化模板新增或删除文档模块。
