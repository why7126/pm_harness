---
purpose: 兼容性矩阵
content: 产品形态兼容、能力覆盖、浏览器与设备、运行时、数据库、对象存储、部署环境、操作系统、CPU 架构、API 兼容和验证规则
source: Harness docs/05-compatibility-matrix.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；产品形态、技术栈、部署环境、数据库、运行时或兼容策略变化时更新；后续由 AI 辅助更新并经人工 Review
owner: {COMPATIBILITY_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 docs/05-compatibility-matrix.md 模块
---

# 兼容性矩阵

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如 Web、微信小程序、移动端、桌面端、数据库、对象存储、信创、私有化部署、算法服务。

## 0. 文档定位 `[通用]`

本文是 `{PRODUCT_NAME}` 的兼容性入口文档，用于说明不同产品形态、运行环境、浏览器、设备、数据库、部署方式和外部服务的支持范围。

本文重点回答：

- 哪些端、平台、浏览器、数据库、运行时和部署方式被正式支持。
- 哪些能力在不同产品形态中支持、部分支持或不支持。
- 兼容性验证由哪些测试、脚本或人工检查覆盖。
- 新增能力时应如何同步兼容性矩阵和测试。

相关规则：

- 兼容性规则：`rules/compatibility.md`
- 测试规则：`rules/testing.md`
- 部署说明：`docs/02-deployment.md`
- 架构说明：`docs/01-architecture.md`
- API 兼容：`rules/api.md`、`docs/03-api-index.md`
- 端口与环境：`rules/port-management.md`、`rules/environment.md`

## 1. 生成参数 `[个性化]`

初始化生成本文时，应优先使用用户输入填充以下参数。缺失信息可以标记为 `待确认`，不得编造兼容性事实。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{PRODUCT_FORMS}` | 产品形态，如 Web、管理后台、微信小程序、移动端、桌面端、API 服务 | 待确认 |
| `{SUPPORTED_CLIENTS}` | 支持的客户端、设备、浏览器 | 待确认 |
| `{BACKEND_STACK}` | 后端运行时和框架 | 待确认 |
| `{FRONTEND_STACK}` | 前端运行时和框架 | 待确认 |
| `{DATABASE_STACK}` | 数据库兼容范围 | 待确认 |
| `{OBJECT_STORAGE_STACK}` | 对象存储兼容范围 | 待确认 |
| `{DEPLOYMENT_STACK}` | 部署方式 | 待确认 |
| `{OS_SUPPORT_MATRIX}` | 操作系统兼容矩阵 | 待确认 |
| `{CPU_ARCH_MATRIX}` | CPU 架构兼容矩阵 | 待确认 |
| `{RUNTIME_VERSION_MATRIX}` | 语言、框架、Node、Python、JDK 等运行时版本 | 待确认 |
| `{COMPATIBILITY_OWNER}` | 兼容性文档负责人 | 待确认 |
| `{COMPATIBILITY_TEST_COMMAND}` | 兼容性验证命令 | 待确认 |

## 2. 兼容性等级 `[通用]`

| 等级 | 含义 | 要求 |
|---|---|---|
| `支持` | 正式支持，可用于目标环境 | 必须有测试或验收记录 |
| `部分支持` | 仅支持部分功能或存在限制 | 必须说明限制、规避方式和后续计划 |
| `计划支持` | 已规划但尚未完成 | 必须关联需求或 OpenSpec Change |
| `不支持` | 当前明确不支持 | 必须说明原因或替代方案 |
| `待确认` | 信息不足 | 初始化或评审后补齐 |

矩阵中不得使用含糊描述，例如“应该可以”“大概支持”。未知时统一写 `待确认`。

## 3. 产品形态与能力矩阵 `[通用 + 个性化]`

初始化时应根据 `{PRODUCT_FORMS}` 与 `{CORE_CAPABILITIES}` 生成真实矩阵。未启用产品形态必须删除。

| 能力 | Web | 管理后台 | 微信小程序 | 移动端 | 桌面端 | API/SDK | 说明 |
|---|---|---|---|---|---|---|---|
| `{CAPABILITY_1}` | `{WEB_SUPPORT_1}` | `{ADMIN_SUPPORT_1}` | `{WECHAT_MINIAPP_SUPPORT_1}` | `{MOBILE_SUPPORT_1}` | `{DESKTOP_SUPPORT_1}` | `{API_SUPPORT_1}` | `{NOTE_1}` |
| `{CAPABILITY_2}` | `{WEB_SUPPORT_2}` | `{ADMIN_SUPPORT_2}` | `{WECHAT_MINIAPP_SUPPORT_2}` | `{MOBILE_SUPPORT_2}` | `{DESKTOP_SUPPORT_2}` | `{API_SUPPORT_2}` | `{NOTE_2}` |

生成要求：

- 能力名称必须来自 `docs/00-product-overview.md` 或需求文档。
- 不同端支持差异必须能追踪到权限、交互、设备能力或业务范围。
- `部分支持` 必须说明限制。

## 4. 浏览器与 Web 兼容 `[条件启用]`

当项目包含 Web、管理后台、H5 或浏览器端能力时保留本节。

| 浏览器 | 最低版本 | 支持等级 | 验证方式 | 备注 |
|---|---:|---|---|---|
| `{BROWSER_1}` | `{BROWSER_MIN_VERSION_1}` | `{BROWSER_SUPPORT_1}` | `{BROWSER_VERIFY_1}` | `{BROWSER_NOTE_1}` |
| `{BROWSER_2}` | `{BROWSER_MIN_VERSION_2}` | `{BROWSER_SUPPORT_2}` | `{BROWSER_VERIFY_2}` | `{BROWSER_NOTE_2}` |

Web 兼容要求：

- 关键页面必须覆盖主流浏览器和响应式断点。
- UI 变更必须同步 `rules/ui-design.md` 与相关视觉验收。
- 如果项目不支持某浏览器或旧版本，应明确说明。

## 5. 移动端 / 微信小程序 / 桌面端兼容 `[条件启用]`

| 客户端 | 平台/系统 | 最低版本 | 支持等级 | 验证方式 | 备注 |
|---|---|---:|---|---|---|
| 微信小程序 | `{WECHAT_MINIAPP_PLATFORM}` | `{WECHAT_MINIAPP_MIN_VERSION}` | `{WECHAT_MINIAPP_SUPPORT}` | `{WECHAT_MINIAPP_VERIFY}` | `{WECHAT_MINIAPP_NOTE}` |
| Android | `{ANDROID_TARGET}` | `{ANDROID_MIN_VERSION}` | `{ANDROID_SUPPORT}` | `{ANDROID_VERIFY}` | `{ANDROID_NOTE}` |
| iOS | `{IOS_TARGET}` | `{IOS_MIN_VERSION}` | `{IOS_SUPPORT}` | `{IOS_VERIFY}` | `{IOS_NOTE}` |
| 桌面端 | `{DESKTOP_TARGET}` | `{DESKTOP_MIN_VERSION}` | `{DESKTOP_SUPPORT}` | `{DESKTOP_VERIFY}` | `{DESKTOP_NOTE}` |

端能力差异应明确记录，例如摄像头、文件选择、扫码、推送、离线缓存、系统分享、支付、定位等。

## 6. API 与协议兼容 `[通用 + 个性化]`

| 项 | 策略 | 验证方式 | 关联文档 |
|---|---|---|---|
| API 版本 | `{API_VERSION_POLICY}` | `{API_VERSION_VERIFY}` | `docs/03-api-index.md` |
| 响应结构 | `{RESPONSE_COMPAT_POLICY}` | `{RESPONSE_COMPAT_VERIFY}` | `rules/api.md` |
| 字段兼容 | `{FIELD_COMPAT_POLICY}` | `{FIELD_COMPAT_VERIFY}` | `rules/api.md` |
| 错误码 | `{ERROR_CODE_COMPAT_POLICY}` | `{ERROR_CODE_VERIFY}` | `{ERROR_CODE_DOC_PATH}` |
| Webhook | `{WEBHOOK_COMPAT_POLICY}` | `{WEBHOOK_VERIFY}` | `{WEBHOOK_DOC_PATH}` |
| SDK | `{SDK_COMPAT_POLICY}` | `{SDK_VERIFY}` | `{SDK_DOC_PATH}` |

破坏性 API 变更必须通过 OpenSpec Change，并说明调用方影响和迁移窗口。

## 7. 后端运行时兼容 `[通用 + 个性化]`

| 运行时/框架 | 支持版本 | 支持等级 | 验证方式 | 备注 |
|---|---|---|---|---|
| `{BACKEND_RUNTIME}` | `{BACKEND_RUNTIME_VERSION}` | `{BACKEND_RUNTIME_SUPPORT}` | `{BACKEND_RUNTIME_VERIFY}` | `{BACKEND_RUNTIME_NOTE}` |
| `{BACKEND_FRAMEWORK}` | `{BACKEND_FRAMEWORK_VERSION}` | `{BACKEND_FRAMEWORK_SUPPORT}` | `{BACKEND_FRAMEWORK_VERIFY}` | `{BACKEND_FRAMEWORK_NOTE}` |

要求：

- 运行时版本必须与依赖管理文件、Dockerfile、CI 和部署文档一致。
- 版本升级必须同步测试、镜像构建、兼容性记录和发布说明。

## 8. 前端运行时兼容 `[条件启用]`

| 运行时/工具 | 支持版本 | 支持等级 | 验证方式 | 备注 |
|---|---|---|---|---|
| `{FRONTEND_RUNTIME}` | `{FRONTEND_RUNTIME_VERSION}` | `{FRONTEND_RUNTIME_SUPPORT}` | `{FRONTEND_RUNTIME_VERIFY}` | `{FRONTEND_RUNTIME_NOTE}` |
| `{PACKAGE_MANAGER}` | `{PACKAGE_MANAGER_VERSION}` | `{PACKAGE_MANAGER_SUPPORT}` | `{PACKAGE_MANAGER_VERIFY}` | `{PACKAGE_MANAGER_NOTE}` |
| `{BUILD_TOOL}` | `{BUILD_TOOL_VERSION}` | `{BUILD_TOOL_SUPPORT}` | `{BUILD_TOOL_VERIFY}` | `{BUILD_TOOL_NOTE}` |

前端构建和客户端生成工具必须与 `docs/03-api-index.md`、`docs/02-deployment.md` 一致。

## 9. 数据库兼容 `[条件启用]`

| 数据库 | 支持版本 | 支持等级 | 迁移策略 | 测试覆盖 | 备注 |
|---|---|---|---|---|---|
| `{DATABASE_1}` | `{DATABASE_VERSION_1}` | `{DATABASE_SUPPORT_1}` | `{DATABASE_MIGRATION_1}` | `{DATABASE_TEST_1}` | `{DATABASE_NOTE_1}` |
| `{DATABASE_2}` | `{DATABASE_VERSION_2}` | `{DATABASE_SUPPORT_2}` | `{DATABASE_MIGRATION_2}` | `{DATABASE_TEST_2}` | `{DATABASE_NOTE_2}` |

数据库兼容要求：

- 数据库类型、版本、迁移策略必须与 `docs/04-database-design.md` 和 `rules/database.md` 一致。
- 如支持多数据库，必须说明 SQL 方言、索引、事务、分页、JSON 字段、时区和迁移差异。
- 信创数据库或国产数据库必须有单独兼容性验证记录。

## 10. 对象存储与文件兼容 `[条件启用]`

| 存储服务 | 支持版本/协议 | 支持等级 | 兼容要求 | 验证方式 | 备注 |
|---|---|---|---|---|---|
| `{OBJECT_STORAGE_1}` | `{OBJECT_STORAGE_VERSION_1}` | `{OBJECT_STORAGE_SUPPORT_1}` | `{OBJECT_STORAGE_REQUIREMENT_1}` | `{OBJECT_STORAGE_VERIFY_1}` | `{OBJECT_STORAGE_NOTE_1}` |

对象存储兼容要求：

- Bucket、前缀、签名 URL、生命周期、权限策略必须与 `rules/object-storage.md` 一致。
- 文件上传、媒体处理和下载必须与 `rules/media.md` 一致。
- S3 兼容服务不得默认认为完全等价，必须验证签名、URL、region、ACL、metadata 行为。

## 11. 操作系统与 CPU 架构兼容 `[通用 + 条件启用]`

| 环境 | OS/发行版 | CPU 架构 | 支持等级 | 验证方式 | 备注 |
|---|---|---|---|---|---|
| 本地开发 | `{LOCAL_OS}` | `{LOCAL_CPU_ARCH}` | `{LOCAL_SUPPORT}` | `{LOCAL_VERIFY}` | `{LOCAL_NOTE}` |
| CI | `{CI_OS}` | `{CI_CPU_ARCH}` | `{CI_SUPPORT}` | `{CI_VERIFY}` | `{CI_NOTE}` |
| 服务器/容器 | `{SERVER_OS}` | `{SERVER_CPU_ARCH}` | `{SERVER_SUPPORT}` | `{SERVER_VERIFY}` | `{SERVER_NOTE}` |
| 信创环境 | `{XC_OS}` | `{XC_CPU_ARCH}` | `{XC_SUPPORT}` | `{XC_VERIFY}` | `{XC_NOTE}` |

启用信创、ARM、国产 OS 或离线私有化时，必须保留本节并补充专项验证。

## 12. 部署方式兼容 `[通用 + 个性化]`

| 部署方式 | 支持等级 | 适用环境 | 验证方式 | 关联文档 |
|---|---|---|---|---|
| Docker Compose | `{COMPOSE_SUPPORT}` | `{COMPOSE_ENV}` | `{COMPOSE_VERIFY}` | `docs/02-deployment.md` |
| Kubernetes / Helm | `{K8S_SUPPORT}` | `{K8S_ENV}` | `{K8S_VERIFY}` | `deploy/` |
| SaaS / PaaS | `{SAAS_SUPPORT}` | `{SAAS_ENV}` | `{SAAS_VERIFY}` | `{SAAS_DOC}` |
| 私有化 / 离线部署 | `{PRIVATE_SUPPORT}` | `{PRIVATE_ENV}` | `{PRIVATE_VERIFY}` | `{PRIVATE_DOC}` |

未启用的部署方式应删除或标记为 `不支持`，不得在部署文档中保留强制要求。

## 13. 外部服务兼容 `[条件启用]`

| 外部服务 | 用途 | 协议/版本 | 支持等级 | 超时/重试 | 降级策略 |
|---|---|---|---|---|---|
| `{EXTERNAL_SERVICE_1}` | `{EXTERNAL_PURPOSE_1}` | `{EXTERNAL_PROTOCOL_1}` | `{EXTERNAL_SUPPORT_1}` | `{EXTERNAL_RETRY_1}` | `{EXTERNAL_FALLBACK_1}` |

外部服务兼容必须与 `docs/01-architecture.md`、`docs/03-api-index.md`、`rules/security.md` 一致。

## 14. 兼容性测试矩阵 `[通用 + 个性化]`

| 维度 | 测试内容 | 命令/方式 | 负责人 | 频率 |
|---|---|---|---|---|
| 端能力 | `{CLIENT_COMPAT_TEST}` | `{CLIENT_COMPAT_COMMAND}` | `{CLIENT_COMPAT_OWNER}` | `{CLIENT_COMPAT_FREQUENCY}` |
| API 兼容 | `{API_COMPAT_TEST}` | `{API_COMPAT_COMMAND}` | `{API_COMPAT_OWNER}` | `{API_COMPAT_FREQUENCY}` |
| 数据库 | `{DB_COMPAT_TEST}` | `{DB_COMPAT_COMMAND}` | `{DB_COMPAT_OWNER}` | `{DB_COMPAT_FREQUENCY}` |
| 部署 | `{DEPLOY_COMPAT_TEST}` | `{DEPLOY_COMPAT_COMMAND}` | `{DEPLOY_COMPAT_OWNER}` | `{DEPLOY_COMPAT_FREQUENCY}` |
| 对象存储 | `{STORAGE_COMPAT_TEST}` | `{STORAGE_COMPAT_COMMAND}` | `{STORAGE_COMPAT_OWNER}` | `{STORAGE_COMPAT_FREQUENCY}` |
| OS/CPU | `{OS_CPU_COMPAT_TEST}` | `{OS_CPU_COMPAT_COMMAND}` | `{OS_CPU_COMPAT_OWNER}` | `{OS_CPU_COMPAT_FREQUENCY}` |

统一兼容性验证命令：

```bash
{COMPATIBILITY_TEST_COMMAND}
```

如果无法自动化验证，应明确人工验证步骤和验收证据。

## 15. 已知限制与规避方案 `[通用 + 个性化]`

| 限制 | 影响范围 | 原因 | 规避方案 | 后续计划 |
|---|---|---|---|---|
| `{LIMITATION_1}` | `{LIMITATION_SCOPE_1}` | `{LIMITATION_REASON_1}` | `{WORKAROUND_1}` | `{FOLLOW_UP_1}` |
| `{LIMITATION_2}` | `{LIMITATION_SCOPE_2}` | `{LIMITATION_REASON_2}` | `{WORKAROUND_2}` | `{FOLLOW_UP_2}` |

## 16. AI 修改兼容性规则 `[通用]`

AI Agent 修改兼容性相关内容时必须：

1. 先读取 `rules/compatibility.md`、`rules/testing.md`、`docs/01-architecture.md`、`docs/02-deployment.md` 和本文。
2. 判断是否影响产品形态、API、数据库、对象存储、部署、OS、CPU、浏览器或外部服务。
3. 同步更新相关测试、部署文档、API 文档、数据库文档和发布说明。
4. 不得凭空宣称某平台支持；没有验证时标记为 `待确认` 或 `计划支持`。
5. 完成后说明验证方式和剩余风险。

## 17. 更新触发条件 `[通用]`

发生以下情况时，必须更新本文：

- 新增或移除产品形态。
- 新增核心能力或改变不同端支持范围。
- 升级浏览器、移动端、微信小程序、桌面端、运行时、框架、数据库或对象存储要求。
- 新增部署方式、操作系统、CPU 架构或信创要求。
- API 版本、响应结构、错误码、SDK、Webhook 兼容策略变化。
- 兼容性测试命令、验证范围或验收标准变化。

同步检查：

- `docs/00-product-overview.md`
- `docs/01-architecture.md`
- `docs/02-deployment.md`
- `docs/03-api-index.md`
- `docs/04-database-design.md`
- `rules/compatibility.md`
- `rules/testing.md`
- `rules/release.md`

## 18. 初始化生成建议 `[通用]`

工程初始化工具生成本文时应遵循：

1. 保留所有 `[通用]` 模块。
2. 用用户输入替换所有 `[个性化]` 占位符。
3. 根据 `{PRODUCT_FORMS}` 删除未启用端。
4. 根据 `{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{DEPLOYMENT_STACK}` 生成真实兼容矩阵。
5. 根据是否启用 Web、微信小程序、移动端、桌面端、对象存储、外部服务、信创或私有化部署保留对应 `[条件启用]` 模块。
6. 未确认信息标记为 `待确认`。
7. 不得保留来源项目的业务能力、端名称、数据库、对象存储、浏览器版本或部署环境。
8. 生成后检查本文是否能回答：
   - 哪些端和能力被支持？
   - 支持哪些浏览器、设备、数据库、OS 和部署方式？
   - 哪些能力部分支持或不支持？
   - 兼容性如何验证？
