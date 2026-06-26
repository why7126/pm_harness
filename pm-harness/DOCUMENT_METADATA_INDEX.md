---
purpose: 文档元数据索引
content: 文档元数据字段规范、文档资产清单、配置/脚本元数据规则、初始化生成规则、同步关系与更新触发条件
source: Harness DOCUMENT_METADATA_INDEX.md 抽象模板，初始化时基于用户输入和实际生成文件清单生成
update_method: 新增、删除、迁移、重命名或调整文档/配置/脚本时同步更新
owner: {DOCS_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；本文档是文档资产登记入口，不替代具体文档内容
---

# 文档元数据索引

## 0. 文档定位 `[通用]`

本文档用于登记 `{PRODUCT_NAME}` 项目的文档资产、配置资产和脚本资产元数据，帮助团队和 AI Agent 理解每个文档的用途、来源、维护方式和同步关系。

本文档不记录需求、Bug 或迭代的业务细节，只记录“哪些文档存在、为什么存在、何时更新、由谁维护”。

必须与以下文件保持一致：

- `README.md`
- `AGENTS.md`
- `project.yaml`
- `docs/README.md`
- `rules/document-governance.md`
- `rules/directory-structure.md`

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{DOCS_OWNER}` | 文档负责人 | 待确认 |
| `{DOCUMENT_SOURCE_POLICY}` | 文档来源策略 | AI 生成 / 人工维护 / 系统生成 |
| `{DOCUMENT_REVIEW_POLICY}` | 文档 Review 策略 | 人工 Review / PR Review / Sprint Review |
| `{DOCUMENT_UPDATE_POLICY}` | 文档更新策略 | 变更同步 / 发布同步 / 按需更新 |
| `{ENABLED_DOC_MODULES}` | 已启用文档模块 | docs / rules / standards / openspec / issues |
| `{ENABLED_PRODUCT_FORMS}` | 已启用产品形态 | Web / Admin / API / Mobile / WeChat Miniapp |
| `{ENABLED_TECH_STACKS}` | 已启用技术栈 | 待确认 |
| `{ENABLED_GOVERNANCE_FLOWS}` | 已启用治理流程 | requirement / bug / sprint / OpenSpec |
| `{DOCUMENT_METADATA_SCHEMA_VERSION}` | 元数据规范版本 | v1 |

## 2. 元数据字段规范 `[通用]`

所有 Markdown 文档必须包含 YAML Frontmatter。

```yaml
---
purpose: {文档用途}
content: {文档内容简述}
source: {内容来源}
update_method: {更新方式}
owner: {负责人或角色}
note: {适用范围或注意事项}
---
```

字段说明：

| 字段 | 是否必填 | 说明 | 示例 |
|---|---|---|---|
| `purpose` | 是 | 文档用途，一句话说明为什么存在 | 项目入口说明 |
| `content` | 是 | 文档覆盖的主要内容 | 产品简介、技术栈、启动方式 |
| `source` | 是 | 内容来源 | 用户输入 / AI 生成 / OpenSpec / 代码扫描 |
| `update_method` | 是 | 何时更新、如何更新 | 技术栈变化时同步更新 |
| `owner` | 建议 | 文档负责人或负责角色 | `{DOCS_OWNER}` |
| `note` | 建议 | 适用范围、限制或重要提醒 | 适用于 `{PRODUCT_NAME}` 项目 |

规则：

- `purpose` 和 `content` 应具体，不得只写“说明文档”。
- `source` 必须能解释内容可信度，不得默认写“已确认”。
- `update_method` 必须包含触发条件。
- 文档中的时间记录必须精确到秒，统一使用 `YYYY-MM-DD HH:mm:ss`，例如 `2026-06-25 14:30:05`。
- Frontmatter 或正文表格中的 `created_at`、`updated_at`、`reviewed_at`、`verified_at`、`archived_at`、`published_at`、`发生时间`、`创建时间`、`更新时间`、`评审时间`、`验证时间`、`归档时间` 等字段必须使用完整时间；无法确认时写 `待确认`。
- 文件名、目录名和归档分组中的日期可以继续使用 `YYYY-MM-DD` 或 `YYYY-MM`。
- 新增 Markdown 文档时必须同步登记到本文档。
- 删除、迁移或重命名 Markdown 文档时必须同步更新本文档和相关导航。

## 3. 配置与脚本元数据规则 `[通用]`

非 Markdown 文件不强制使用 YAML Frontmatter，避免破坏语法。

可使用以下方式记录元数据：

| 文件类型 | 元数据方式 | 说明 |
|---|---|---|
| YAML / TOML / INI | 顶部注释 | 不影响解析 |
| Python / Shell / JS / TS | 顶部注释块 | 保留用途、来源、更新方式 |
| JSON | 不写注释，在本文档登记 | JSON 不支持注释 |
| Dockerfile / nginx / conf | 顶部注释 | 不影响运行 |
| 生成文件 | 在本文档标记为生成产物 | 不手工维护 |

配置和脚本必须至少在本文档登记以下信息：

- 路径
- 用途
- 来源
- 更新触发条件
- 是否允许 AI 修改

## 4. 文档模块分类 `[通用]`

| 模块 | 目录/文件 | 说明 |
|---|---|---|
| 根入口 | `README.md`、`AGENTS.md`、`project.yaml`、`DOCUMENT_METADATA_INDEX.md` | 项目入口、AI 协作、元数据 |
| 工程规则 | `rules/` | 代码、目录、安全、测试、环境、发布等规则 |
| 产品与架构文档 | `docs/00-*` 到 `docs/07-*` | 产品、架构、部署、API、数据库、兼容、媒体、对象存储 |
| 专项标准 | `docs/standards/` | API、认证、错误码、上传、测试等标准 |
| 兼容模块 | `compatibility/` | 端设备、数据库、对象存储等独立兼容适配说明 |
| 需求治理 | `issues/requirements/` | 需求捕获、PRD、验收、追踪 |
| 缺陷治理 | `issues/bugs/` | Bug 捕获、复现、根因、修复、回归 |
| 迭代治理 | `iterations/` | Sprint 计划、执行、验收、归档 |
| OpenSpec | `openspec/` | Change、Spec、Archive、映射 |
| 部署配置 | `deploy/`、`docker-compose.yml`、`.env.example` | 部署、环境变量、服务拓扑 |
| 自动化脚本 | `scripts/` | 校验、启动、构建、生成脚本 |

## 5. 核心文档资产清单 `[通用 + 个性化]`

初始化时必须根据实际生成文件更新本表。

| 路径 | 模块 | 文档用途 | 内容来源 | 更新方式 | Owner | 是否必需 |
|---|---|---|---|---|---|---|
| `README.md` | 根入口 | 工程入口说明 | `{DOCUMENT_SOURCE_POLICY}` | 项目定位、启动方式或技术栈变化时更新 | `{DOCS_OWNER}` | 是 |
| `AGENTS.md` | 根入口 | AI Agent 协作规则 | `{DOCUMENT_SOURCE_POLICY}` | AI 规则、命令或目录结构变化时更新 | `{DOCS_OWNER}` | 是 |
| `project.yaml` | 根入口 | 项目元数据 | 用户输入 / 初始化生成 | 项目元数据变化时更新 | `{DOCS_OWNER}` | 是 |
| `DOCUMENT_METADATA_INDEX.md` | 根入口 | 文档资产元数据索引 | 初始化生成 / 文档扫描 | 文档资产变化时更新 | `{DOCS_OWNER}` | 是 |
| `docs/README.md` | 文档入口 | docs 目录导航 | 初始化生成 | docs 目录变化时更新 | `{DOCS_OWNER}` | 是 |
| `docs/00-product-overview.md` | 产品文档 | 产品定位和核心能力 | 用户输入 / 需求 | 产品范围变化时更新 | `{DOCS_OWNER}` | 是 |
| `docs/01-architecture.md` | 架构文档 | 系统架构和模块边界 | 用户输入 / 技术栈 | 架构变化时更新 | `{DOCS_OWNER}` | 是 |
| `docs/02-deployment.md` | 部署文档 | 部署方式和运行环境 | 配置 / 部署脚本 | 部署方式变化时更新 | `{DOCS_OWNER}` | 条件 |
| `docs/03-api-index.md` | API 文档 | API 分组和契约入口 | API 设计 / OpenAPI | API 变化时更新 | `{DOCS_OWNER}` | 条件 |
| `docs/04-database-design.md` | 数据库文档 | 数据模型和迁移策略 | Schema / ORM / 需求 | 数据模型变化时更新 | `{DOCS_OWNER}` | 条件 |
| `docs/05-compatibility-matrix.md` | 兼容文档 | 支持矩阵和验证要求 | 产品形态 / 技术栈 | 兼容承诺变化时更新 | `{DOCS_OWNER}` | 条件 |
| `docs/06-video-asset-management.md` | 媒体文档 | 视频/富媒体资产管理 | 媒体需求 | 媒体能力变化时更新 | `{DOCS_OWNER}` | 条件 |
| `docs/07-object-storage-strategy.md` | 存储文档 | 对象存储策略 | 存储需求 / 部署配置 | 存储策略变化时更新 | `{DOCS_OWNER}` | 条件 |

## 5.1 兼容性模块清单 `[通用 + 条件启用]`

初始化时必须根据实际产品形态、数据库和对象存储生成本表。

| 路径 | 模块 | 用途 | 启用条件 | 同步关系 |
|---|---|---|---|---|
| `compatibility/README.md` | 兼容入口 | 兼容性模块索引 | 建议保留 | `rules/compatibility.md` |
| `compatibility/database/migration-rules.md` | 数据库 | 数据库迁移兼容规则 | 有数据库时 | `rules/database.md`、`docs/04-database-design.md` |
| `compatibility/database/test-matrix.md` | 数据库 | 数据库兼容测试矩阵 | 有数据库时 | `rules/testing.md`、`rules/database.md` |
| `compatibility/database/sqlite.md` | 数据库 | SQLite 适配说明 | 使用 SQLite 时 | `docs/04-database-design.md` |
| `compatibility/database/postgresql.md` | 数据库 | PostgreSQL 适配说明 | 支持 PostgreSQL 时 | `docs/04-database-design.md` |
| `compatibility/database/mysql.md` | 数据库 | MySQL 适配说明 | 支持 MySQL 时 | `docs/04-database-design.md` |
| `compatibility/database/dm.md` | 数据库 | 达梦适配说明 | 信创数据库包含达梦时 | `docs/05-compatibility-matrix.md` |
| `compatibility/database/highgo.md` | 数据库 | 海量适配说明 | 信创数据库包含海量时 | `docs/05-compatibility-matrix.md` |
| `compatibility/devices/web.md` | 设备端 | Web 兼容说明 | 产品形态包含 Web 或管理后台时 | `rules/ui-design.md` |
| `compatibility/devices/wechat-miniapp.md` | 设备端 | 微信小程序兼容说明 | 产品形态包含微信小程序时 | `rules/media.md` |
| `compatibility/devices/h5.md` | 设备端 | 移动 H5 兼容说明 | 产品形态包含 H5 时 | `rules/ui-design.md` |
| `compatibility/devices/desktop.md` | 设备端 | 桌面端兼容说明 | 产品形态包含桌面端时 | `rules/release.md` |
| `compatibility/devices/android.md` | 设备端 | Android 兼容说明 | 产品形态包含 Android 时 | `rules/release.md` |
| `compatibility/devices/ios.md` | 设备端 | iOS 兼容说明 | 产品形态包含 iOS 时 | `rules/release.md` |
| `compatibility/object-storage/README.md` | 对象存储 | 对象存储兼容入口 | 启用对象存储时 | `rules/object-storage.md` |
| `compatibility/object-storage/minio.md` | 对象存储 | MinIO 适配说明 | 使用 MinIO 时 | `docs/07-object-storage-strategy.md` |
| `compatibility/object-storage/s3.md` | 对象存储 | S3 适配说明 | 使用 S3/S3 Compatible 时 | `docs/07-object-storage-strategy.md` |
| `compatibility/object-storage/cos.md` | 对象存储 | 腾讯 COS 适配说明 | 使用 COS 时 | `docs/07-object-storage-strategy.md` |
| `compatibility/object-storage/oss.md` | 对象存储 | 阿里云 OSS 适配说明 | 使用 OSS 时 | `docs/07-object-storage-strategy.md` |
| `compatibility/object-storage/obs.md` | 对象存储 | 华为 OBS 适配说明 | 使用 OBS 时 | `docs/07-object-storage-strategy.md` |
| `compatibility/object-storage/rustfs.md` | 对象存储 | RustFS 适配说明 | 使用 RustFS 时 | `docs/07-object-storage-strategy.md` |

## 6. 专项标准文档清单 `[通用 + 个性化]`

| 路径 | 标准类型 | 用途 | 启用条件 | 同步关系 |
|---|---|---|---|---|
| `docs/standards/api-governance.md` | API 治理 | API 设计、版本、响应、幂等、测试规则 | 有 API / SDK / Webhook 时 | `rules/api.md`、`docs/03-api-index.md` |
| `docs/standards/openapi-rules.md` | OpenAPI | 契约来源、Schema、生成与校验规则 | 启用 OpenAPI 时 | `docs/03-api-index.md`、API Client |
| `docs/standards/authentication.md` | 认证授权 | 登录、Token/Session、权限模型、错误码 | 有身份或权限时 | `rules/security.md`、`docs/03-api-index.md` |
| `docs/standards/error-codes.md` | 错误码 | 错误码分段、HTTP 映射、前端处理 | 有 API 或统一错误处理时 | `rules/api.md`、前端错误处理 |
| `docs/standards/file_upload.md` | 文件上传 | 上传方式、限制、安全、对象存储、测试 | 有上传/导入/附件/媒体时 | `rules/media.md`、`rules/object-storage.md` |
| `docs/standards/testing-governance.md` | 测试治理 | 测试目标、分层、CI、例外审批 | 有测试治理要求时 | `rules/testing.md` |
| `docs/standards/unit-test-standard.md` | 单元测试 | 单元测试范围、断言、Mock、Fixture | 有可自动化单元测试代码时 | `docs/standards/testing-governance.md` |
| `docs/standards/frontend-test-standard.md` | 前端测试 | 组件、页面、Mock、A11y、视觉回归 | 有前端 UI 时 | `rules/ui-design.md`、`rules/testing.md` |
| `docs/standards/test-coverage.md` | 覆盖率 | 覆盖率目标、统计范围、CI 门禁 | 启用覆盖率统计时 | `rules/testing.md` |

## 7. 规则文档清单 `[通用]`

| 路径 | 用途 | 更新方式 |
|---|---|---|
| `rules/global.md` | 全局协作与 guard 规则 | 全局 AI 行为变化时更新 |
| `rules/directory-structure.md` | 目录边界和文件归属 | 目录结构变化时更新 |
| `rules/document-governance.md` | 文档生命周期和同步规则 | 文档治理流程变化时更新 |
| `rules/requirement-management.md` | 需求治理规则 | 需求流程或命令变化时更新 |
| `rules/bug-management.md` | Bug 治理规则 | 缺陷流程或命令变化时更新 |
| `rules/coding.md` | 编码、分层和模块边界 | 技术栈或代码规范变化时更新 |
| `rules/language.md` | 语言、命名和术语治理 | 命名或术语变化时更新 |
| `rules/api.md` | API 规则 | API 风格、契约或客户端策略变化时更新 |
| `rules/database.md` | 数据库规则 | 数据库、迁移或 Schema 策略变化时更新 |
| `rules/data-management.md` | 数据资产和运行时数据规则 | 数据目录或样例数据策略变化时更新 |
| `rules/environment.md` | 环境变量和配置规则 | 环境变量或配置来源变化时更新 |
| `rules/security.md` | 安全规则 | 认证、凭据、权限或安全要求变化时更新 |
| `rules/testing.md` | 测试规则 | 测试策略、命令或门禁变化时更新 |
| `rules/release.md` | 发布规则 | 发布流程或部署策略变化时更新 |
| `rules/compatibility.md` | 兼容性规则 | 支持矩阵变化时更新 |
| `rules/media.md` | 媒体资产规则 | 媒体能力变化时更新 |
| `rules/object-storage.md` | 对象存储规则 | 存储供应商、桶策略或 Key 策略变化时更新 |
| `rules/port-management.md` | 端口规则 | 服务端口或映射策略变化时更新 |
| `rules/ui-design.md` | UI 设计规则 | UI 技术栈、设计系统或交互规则变化时更新 |

## 8. 配置与脚本资产清单 `[通用 + 个性化]`

初始化时根据实际存在的配置和脚本生成本表。

| 路径 | 类型 | 用途 | 内容来源 | 更新方式 | 是否允许 AI 修改 |
|---|---|---|---|---|---|
| `.env.example` | 配置 | 环境变量示例 | 初始化生成 / 配置扫描 | 新增或调整环境变量时更新 | 是 |
| `docker-compose.yml` | 配置 | 本地容器编排 | 部署策略 | 服务拓扑变化时更新 | 条件 |
| `deploy/` | 配置 | 部署配置 | 部署策略 | 部署方式变化时更新 | 条件 |
| `scripts/validate-directory-structure.py` | 脚本 | 目录结构校验 | 目录规则 | 目录规则变化时更新 | 是 |
| `{CUSTOM_SCRIPT_PATH}` | 脚本 | `{CUSTOM_SCRIPT_PURPOSE}` | `{CUSTOM_SCRIPT_SOURCE}` | `{CUSTOM_SCRIPT_UPDATE_METHOD}` | `{AI_EDIT_ALLOWED}` |

## 9. 条件启用模块 `[个性化]`

以下模块应根据 `{ENABLED_DOC_MODULES}`、`{ENABLED_PRODUCT_FORMS}`、`{ENABLED_TECH_STACKS}` 和 `{ENABLED_GOVERNANCE_FLOWS}` 保留、删除或标记为“不适用”。

| 条件 | 应保留/生成的文档 |
|---|---|
| 有 API / SDK / Webhook | `docs/03-api-index.md`、`docs/standards/api-governance.md`、`docs/standards/openapi-rules.md` |
| 有认证授权 | `docs/standards/authentication.md`、`docs/standards/error-codes.md` |
| 有数据库 | `docs/04-database-design.md`、`rules/database.md`、`rules/data-management.md` |
| 有 Web / Admin / UI | `rules/ui-design.md`、`docs/standards/frontend-test-standard.md` |
| 有文件上传 / 媒体 | `rules/media.md`、`docs/standards/file_upload.md`、`docs/06-video-asset-management.md` |
| 有对象存储 | `rules/object-storage.md`、`docs/07-object-storage-strategy.md` |
| 有兼容性承诺 | `compatibility/` 下对应端、数据库、对象存储适配文档 |
| 有自动化测试 | `rules/testing.md`、`docs/standards/testing-governance.md`、`docs/standards/unit-test-standard.md`、`docs/standards/test-coverage.md` |
| 有部署交付 | `docs/02-deployment.md`、`rules/environment.md`、`rules/release.md`、`rules/port-management.md` |
| 启用 OpenSpec | `openspec/`、`openspec/project.md`、`openspec/testing-mapping.md` |
| 启用需求/缺陷/Sprint 治理 | `issues/`、`iterations/`、相关 rules 和命令 |

## 10. AI 修改规则 `[通用]`

AI 新增、删除、迁移或重命名文档时必须：

- 同步更新本文档。
- 同步更新 `docs/README.md`、`README.md`、`AGENTS.md` 中相关导航。
- 检查 `rules/document-governance.md` 和 `rules/directory-structure.md` 是否需要同步。
- 不保留来源项目产品名、业务能力、路径、端口、服务、bucket、表名或历史版本说明。
- 不将临时产物、运行报告、构建产物或缓存登记为长期文档资产。
- 对未知 owner、source 或 update_method 标记 `待确认`，不得编造。

## 11. 初始化生成建议 `[通用]`

初始化生成本文档时应执行：

1. 根据实际生成文件扫描 Markdown、配置和脚本清单。
2. 用用户输入替换 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{DOCS_OWNER}`、`{DOCUMENT_SOURCE_POLICY}`、`{DOCUMENT_REVIEW_POLICY}`、`{DOCUMENT_UPDATE_POLICY}`。
3. 根据项目能力保留或删除 `[条件启用]` 模块。
4. 为每个 Markdown 文档生成 purpose、content、source、update_method、owner 和 note。
5. 为关键配置和脚本生成资产登记行。
6. 删除来源项目历史版本编号、阶段说明和历史迁移记录。
7. 不得保留来源项目业务名、技术栈、服务名、端口、bucket、表名、路径或默认账号。
8. 保持本文档与 `README.md`、`AGENTS.md`、`docs/README.md`、`rules/document-governance.md` 一致。

## 12. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- 新增、删除、迁移或重命名 Markdown 文档。
- 新增、删除或调整关键配置、脚本、部署文件、环境模板。
- 文档 frontmatter 字段规范变化。
- 文档 owner、来源策略、Review 策略或更新策略变化。
- 项目能力模块启用或停用，例如 API、认证、数据库、对象存储、媒体、测试、部署、OpenSpec、Sprint。
- 文档导航、目录结构或 AI 协作规则变化。
