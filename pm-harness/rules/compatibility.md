---
purpose: 兼容性规范
content: 浏览器、终端设备、数据库、对象存储、运行时、操作系统、CPU 架构、部署模式、第三方服务和弱网兼容规则
scope: Web、移动端、微信小程序、后端、数据库、对象存储、算法服务、部署环境、私有化与信创适配
source: Harness compatibility.md 抽象模板，基于多个项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；新增端形态、数据库、部署平台、运行时版本或兼容矩阵变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
note: 适用于 {PRODUCT_NAME} 项目；涉及平台、端、数据库、部署或第三方能力变化时必须检查兼容性
template_scope: 可作为工程初始化时的 rules/compatibility.md 模块
---

# 兼容性规范

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如 Web、移动端、微信小程序、双数据库、对象存储、信创、私有化部署。

## 0. 规则定位 [通用]

`rules/compatibility.md` 用于定义项目必须支持的运行环境、端能力、数据库、对象存储、部署模式和第三方服务边界。

AI Agent 在以下场景必须读取本文件：

- 新增或修改前端特性、Web API、CSS 能力或端能力。
- 新增或修改移动端、微信小程序、桌面端能力。
- 新增或修改数据库表、SQL、ORM 查询、迁移。
- 新增或修改对象存储、上传下载、导入导出、媒体处理。
- 新增或修改 Docker、部署脚本、基础镜像、运行时版本。
- 新增第三方服务、算法服务、异步任务或 Webhook。
- 涉及私有化、国产化、信创、离线部署或多架构支持。

初始化生成本文件时，必须根据用户输入生成兼容矩阵；未知项标记为 `待确认`，不得编造版本、平台或厂商支持范围。

常用占位符：

| 占位符 | 含义 | 归属 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | [个性化] |
| `{PRODUCT_FORMS}` | 产品形态，如 Web、微信小程序、Android、iOS、桌面端 | [个性化] |
| `{BROWSER_SUPPORT_MATRIX}` | 浏览器支持矩阵 | [条件启用] |
| `{MOBILE_SUPPORT_MATRIX}` | 移动端/微信小程序支持矩阵 | [条件启用] |
| `{DATABASE_SUPPORT_MATRIX}` | 数据库兼容矩阵 | [条件启用] |
| `{OBJECT_STORAGE_SUPPORT_MATRIX}` | 对象存储兼容矩阵 | [条件启用] |
| `{RUNTIME_VERSION_MATRIX}` | Node、Python、Java、Go 等运行时版本 | [个性化] |
| `{OS_SUPPORT_MATRIX}` | 操作系统支持矩阵 | [个性化] |
| `{CPU_ARCH_SUPPORT}` | CPU 架构支持范围 | [条件启用] |
| `{DEPLOYMENT_MODES}` | 部署模式，如本地、SaaS、私有化、离线 | [个性化] |
| `{XINCHUANG_REQUIREMENTS}` | 信创/国产化要求 | [条件启用] |

## 1. 总体兼容原则 [通用]

- 新功能必须在声明支持的环境内可用，不能只在开发者本机可用。
- 兼容范围必须可验证，不能只写“主流浏览器”或“常见系统”。
- 使用新语言特性、Web API、CSS 能力、数据库能力或平台 API 前，必须确认最低支持版本。
- 平台特异代码必须隔离在 adapter、client、driver、platform 层，业务逻辑不直接感知具体实现。
- 兼容性变更必须同步文档、测试、部署配置和 OpenSpec Change。
- 对不支持的平台或版本，必须明确降级、提示、禁用或替代方案。

## 2. 产品形态兼容范围 [个性化]

本项目产品形态：

```text
{PRODUCT_FORMS}
```

初始化时应生成每种产品形态的最低支持范围：

| 产品形态 | 支持范围 | 不支持范围 | 验证方式 |
|---|---|---|---|
| Web | `{WEB_SUPPORT_RANGE}` | `{WEB_UNSUPPORTED_RANGE}` | `{WEB_VERIFY_METHOD}` |
| 微信小程序 | `{WECHAT_MINIAPP_SUPPORT_RANGE}` | `{WECHAT_MINIAPP_UNSUPPORTED_RANGE}` | `{WECHAT_MINIAPP_VERIFY_METHOD}` |
| Android | `{ANDROID_SUPPORT_RANGE}` | `{ANDROID_UNSUPPORTED_RANGE}` | `{ANDROID_VERIFY_METHOD}` |
| iOS | `{IOS_SUPPORT_RANGE}` | `{IOS_UNSUPPORTED_RANGE}` | `{IOS_VERIFY_METHOD}` |
| 桌面端 | `{DESKTOP_SUPPORT_RANGE}` | `{DESKTOP_UNSUPPORTED_RANGE}` | `{DESKTOP_VERIFY_METHOD}` |

未启用的产品形态不得保留强制兼容要求。

## 3. Web 浏览器兼容 [条件启用]

Web 端存在时启用本节。

最低支持浏览器应写入项目配置，例如 `browserslist`、构建工具配置或文档：

```text
{BROWSER_SUPPORT_MATRIX}
```

示例矩阵：

| 浏览器 | 最低版本 | 说明 |
|---|---|---|
| Chrome | `待确认` | 桌面端 |
| Edge | `待确认` | 桌面端 |
| Safari | `待确认` | macOS / iOS WebView 如适用 |
| Firefox | `待确认` | 桌面端 |

规则：

- 使用新 Web API 前必须确认最低浏览器支持。
- 新 CSS 能力必须确认构建链和目标浏览器支持。
- 新于最低浏览器版本的能力必须使用 feature detection、`@supports` 或降级方案。
- 依赖安全上下文的 API，例如 Clipboard、Web Crypto、`crypto.randomUUID()`，必须考虑 HTTPS 或 localhost 限制。
- 不支持的浏览器必须给出用户提示或文档说明。
- WebView、内嵌浏览器、微信小程序 WebView 与桌面浏览器不得混为同一兼容范围。

## 4. 移动端、微信小程序与弱网兼容 [条件启用]

移动端或微信小程序存在时启用本节。

支持矩阵：

```text
{MOBILE_SUPPORT_MATRIX}
```

规则：

- 微信小程序必须遵守平台 API、包体积、分包、上传下载、视频播放、缓存和权限限制。
- 移动端必须考虑系统版本、设备权限、离线、弱网、后台切换和低性能设备。
- 接口调用必须具备超时、重试、取消、错误提示和幂等设计。
- 上传下载必须支持失败恢复或明确失败处理。
- 不允许直接复用 Web 浏览器专属 API 到微信小程序或原生端。
- 端特异能力必须通过 platform adapter 封装。

## 5. API 与协议兼容 [通用]

- API 变更必须遵守 `rules/api.md`。
- 新增响应字段通常兼容；删除字段、修改字段类型、修改语义、修改必填性通常不兼容。
- 移动端、微信小程序、第三方集成、SDK 或私有化客户存在时，必须考虑旧客户端兼容。
- Webhook、事件、消息队列、文件格式和导入导出模板都属于协议兼容范围。
- 破坏性变更必须通过 OpenSpec Change 说明迁移策略。

## 6. 数据库兼容 [条件启用]

项目存在数据库时启用本节。

数据库兼容矩阵：

```text
{DATABASE_SUPPORT_MATRIX}
```

示例：

| 数据库 | 版本 | 驱动/ORM | Schema 文件 | 说明 |
|---|---|---|---|---|
| SQLite | `待确认` | `待确认` | `待确认` | 本地开发/轻量部署 |
| PostgreSQL | `待确认` | `待确认` | `待确认` | 生产推荐 |
| MySQL | `待确认` | `待确认` | `待确认` | 可选 |
| 达梦 DM | `待确认` | `待确认` | `待确认` | 信创场景 |

规则：

- Service 层不得感知具体数据库类型。
- 数据库差异必须封装在 Repository、DAO、Dialect、Migration 或兼容层。
- 多数据库支持时，DDL、索引、约束、默认值和查询语义必须保持一致。
- 新增表、字段、索引、迁移时，必须同步所有声明支持的数据库。
- 不得使用某数据库独有能力，除非提供兼容实现或明确限制支持范围。
- SQL、ORM 查询、事务、分页、布尔值、JSON 字段、时间类型都必须纳入兼容性检查。

## 7. 对象存储与文件系统兼容 [条件启用]

项目涉及文件、媒体、对象存储、导入导出或模型文件时启用本节。

对象存储兼容矩阵：

```text
{OBJECT_STORAGE_SUPPORT_MATRIX}
```

示例：

| 后端 | 场景 | 切换方式 | 说明 |
|---|---|---|---|
| 本地文件系统 | 开发/测试 | `STORAGE_TYPE=local` | 不适合生产 |
| MinIO | 开发/私有化 | `STORAGE_TYPE=minio` | S3 兼容 |
| S3/COS/OBS/RustFS | 云或私有化 | `STORAGE_TYPE=<type>` | 通过 adapter 切换 |

规则：

- 业务代码不得直接依赖某个对象存储 SDK。
- bucket、region、endpoint、prefix、签名 URL 逻辑必须集中在 storage adapter。
- 上传下载、预览、删除、复制、生命周期策略应有统一接口。
- 不同存储后端的权限、URL 有效期、Content-Type、分片上传差异必须测试。
- 本地开发存储和生产对象存储不得共享真实生产数据。

## 8. 运行时、包管理器与基础镜像兼容 [个性化]

运行时版本矩阵：

```text
{RUNTIME_VERSION_MATRIX}
```

示例：

| 组件 | 最低版本 | 推荐版本 | 说明 |
|---|---|---|---|
| Python | `待确认` | `待确认` | 后端/算法 |
| Node.js | `待确认` | `待确认` | 前端构建 |
| pnpm/npm/yarn | `待确认` | `待确认` | 前端包管理 |
| Java/Go/Rust | `待确认` | `待确认` | 如适用 |

规则：

- 语言版本、包管理器版本和锁文件必须一致。
- Docker 基础镜像必须满足运行时版本要求。
- 使用新语言特性前必须确认最低版本支持。
- 本地开发、CI、Docker、部署环境的版本应尽量一致。
- 版本升级必须更新文档、CI、Dockerfile、依赖锁文件和验证命令。

## 9. 操作系统与 CPU 架构兼容 [条件启用]

操作系统支持矩阵：

```text
{OS_SUPPORT_MATRIX}
```

CPU 架构：

```text
{CPU_ARCH_SUPPORT}
```

规则：

- 明确支持 Linux、macOS、Windows、国产 OS 或服务器发行版范围。
- 明确支持 `x86_64`、`arm64/aarch64` 或其他架构。
- 原生依赖、算法库、数据库驱动、浏览器依赖和系统包必须检查架构支持。
- Docker 镜像需要考虑 multi-arch 构建或明确单架构限制。
- 文件路径、大小写敏感、换行符、shell 脚本兼容性必须注意。

## 10. 部署模式兼容 [个性化 + 条件启用]

部署模式：

```text
{DEPLOYMENT_MODES}
```

示例：

| 模式 | 入口 | 特殊处理 | 验证 |
|---|---|---|---|
| 本地开发 | `docker compose up` | 调试配置 | 健康检查 |
| SaaS | `待确认` | 多租户/云资源 | CI/CD |
| 私有化 | `待确认` | License、离线包、客户环境 | 离线部署验证 |
| 信创 | `待确认` | 国产 OS/数据库/CPU | 兼容矩阵测试 |

规则：

- 不同部署模式的入口、配置、镜像、环境变量、license、存储和网络必须明确。
- 私有化或离线部署不得依赖公网下载运行时资源。
- SaaS 与私有化代码路径差异必须隔离在配置或启动入口，不得散落业务逻辑。
- 修改部署配置时必须同步 `rules/environment.md`、部署文档和 `.env.example`。

## 11. 信创与国产化适配 [条件启用]

信创/国产化要求：

```text
{XINCHUANG_REQUIREMENTS}
```

涉及信创时必须明确：

- 国产操作系统。
- 国产数据库。
- CPU 架构。
- 中间件、对象存储、浏览器或办公套件。
- GPU/NPU 或 AI 加速硬件。
- 不能使用的国外云服务、闭源依赖或在线资源。

规则：

- 信创适配必须有单独兼容文档或矩阵。
- 数据库、驱动、系统包、镜像、算法依赖必须逐项验证。
- 不得在未验证情况下声称支持国产化或信创环境。

## 12. 第三方服务、算法服务与 Webhook 兼容 [条件启用]

涉及外部服务时启用本节。

规则：

- 第三方服务必须通过 client/adapter 调用。
- 必须定义超时、重试、熔断、降级和错误码转换。
- 外部 API 版本必须记录。
- Webhook 必须保证幂等、签名校验、重试和失败补偿。
- 算法服务或模型推理必须声明模型版本、输入输出格式、硬件要求和资源限制。
- 第三方服务不可用时，应有用户可理解的错误提示或后台补偿机制。

## 13. 兼容性测试要求 [通用 + 条件启用]

兼容性测试应覆盖声明支持范围，而不是只覆盖默认开发环境。

测试类型：

- 浏览器兼容测试。
- 移动端/微信小程序端能力测试。
- API 向后兼容测试。
- 数据库兼容测试。
- 对象存储兼容测试。
- Docker/部署模式验证。
- OS/CPU 架构验证。
- 第三方服务 mock、超时、失败和重试测试。

测试目录建议：

```text
tests/compatibility/
compatibility/
docs/05-compatibility-matrix.md
```

## 14. AI 修改规则 [通用]

AI 涉及兼容性相关修改时必须说明：

- 影响哪些端、浏览器、数据库、对象存储或部署模式。
- 是否引入新版本要求。
- 是否需要更新兼容矩阵。
- 是否需要新增兼容性测试。
- 是否有降级或替代方案。

AI 不得：

- 未验证就声称兼容某平台。
- 为了解决本机问题随意提高最低版本要求。
- 在业务代码中写死平台特定逻辑。
- 只更新一个数据库或一个存储后端，而遗漏声明支持的其他后端。

## 15. 完成任务后检查清单 [通用 + 条件启用]

```text
□ 是否确认本次变更影响的端、浏览器、数据库、对象存储、部署模式
□ 是否使用了超过最低支持版本的新特性
□ 是否需要 feature detection、降级或用户提示
□ API 变更是否考虑旧客户端兼容
□ 数据库变更是否同步所有支持数据库
□ 对象存储变更是否通过 adapter 并覆盖所有支持后端
□ 部署变更是否同步 Docker、.env.example、部署文档
□ 移动端/微信小程序是否考虑弱网、权限、平台 API 限制
□ 信创/国产化要求是否有明确验证证据
□ 是否更新 compatibility/ 或 docs/05-compatibility-matrix.md
□ 是否补充 tests/compatibility/ 相关测试
```

## 16. 初始化生成建议 [通用]

工程初始化工具生成 `rules/compatibility.md` 时应：

1. 保留 [通用] 模块。
2. 用用户输入替换 [个性化] 占位符。
3. 根据产品形态保留 Web、移动端、微信小程序、桌面端等 [条件启用] 模块。
4. 根据数据库、对象存储、算法、部署模式、信创要求生成兼容矩阵。
5. 从实际技术栈生成运行时版本和基础镜像要求。
6. 未知平台或版本标记为 `待确认`，不得编造。
7. 删除指向不存在端、数据库、存储后端、部署模式或测试命令的内容。
8. 保持 compatibility.md 与 api.md、database.md、environment.md、object-storage.md、port-management.md、directory-structure.md 一致。
