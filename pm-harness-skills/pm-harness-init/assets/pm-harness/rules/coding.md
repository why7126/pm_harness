---
purpose: 编码规范与代码质量约束
content: 架构分层、模块边界、代码风格、函数设计、错误处理、前后端规范、端能力约束、共享类型、AI 修改规则
scope: 后端、前端、移动端、小程序、算法、脚本、共享代码、测试辅助代码
source: Harness coding.md 抽象模板，基于多个项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；技术栈、代码风格、模块边界或质量门禁变化时更新
note: 适用于 {PRODUCT_NAME} 项目；AI 生成和修改代码必须遵守本规范
template_scope: 可作为工程初始化时的 rules/coding.md 模块
---

# 编码规范

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如后端、前端、小程序、算法、对象存储、异步任务。

## 0. 规则定位 [通用]

`rules/coding.md` 约束代码结构、实现方式、模块边界、复杂度、错误处理和 AI 修改代码的行为。

AI Agent 在以下场景必须读取本文件：

- 新增或修改业务代码。
- 新增或修改测试代码、脚本、生成器、SDK。
- 新增模块、目录、组件、服务、Repository、Adapter。
- 修改架构分层、调用链、共享类型或端能力边界。
- 引入新依赖、新框架、新代码生成工具。

初始化生成本文件时，必须根据项目实际技术栈替换占位符；缺失信息标记为 `待确认`，不得编造框架、目录或命令。

常用占位符：

| 占位符 | 含义 | 归属 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | [个性化] |
| `{BACKEND_STACK}` | 后端技术栈 | [个性化] |
| `{BACKEND_MODULE_STRUCTURE}` | 后端模块结构 | [个性化] |
| `{FRONTEND_STACK}` | 前端技术栈 | [条件启用] |
| `{FRONTEND_MODULE_STRUCTURE}` | 前端模块结构 | [条件启用] |
| `{MOBILE_STACK}` | 移动端/小程序技术栈 | [条件启用] |
| `{DATABASE_STACK}` | 数据库与 ORM/DAO 方案 | [条件启用] |
| `{OBJECT_STORAGE_STACK}` | 对象存储方案 | [条件启用] |
| `{ASYNC_TASK_STACK}` | 异步任务或队列方案 | [条件启用] |
| `{ALGORITHM_STACK}` | 算法/模型服务技术栈 | [条件启用] |
| `{FORMAT_COMMAND}` | 格式化命令 | [个性化] |
| `{LINT_COMMAND}` | lint 命令 | [个性化] |
| `{TYPECHECK_COMMAND}` | 类型检查命令 | [条件启用] |

## 1. 总体编码原则 [通用]

- 代码必须服务于已有架构，不为了单次任务绕过分层。
- 优先复用项目已有工具、组件、类型、client、adapter 和脚本。
- 新增抽象必须解决真实重复、复杂度或边界问题。
- 不在业务代码中硬编码环境变量、密钥、路径、端口、URL、bucket、模型文件路径。
- 不把临时调试代码、真实数据、运行时文件提交到仓库。
- 修改公共接口、共享类型或跨模块契约时，必须同步调用方、测试和文档。
- AI 不得覆盖用户未要求修改的文件或无关改动。

## 2. 架构分层 [通用 + 个性化]

推荐分层模型：

```text
Interface Layer    API / Controller / Page / CLI / Webhook
    ↓
Application Layer  Use Case / Service / Command / Workflow
    ↓
Domain Layer       Domain Model / Policy / Business Rule
    ↓
Data Access Layer  Repository / DAO / External Client / Adapter
    ↓
Infrastructure     Database / Object Storage / Queue / Filesystem / Third-party
```

通用边界：

- Interface 层负责协议适配、请求校验和响应格式化，不写复杂业务逻辑。
- Application/Service 层负责编排业务流程，不直接拼 SQL、HTTP URL 或存储 key。
- Domain 层表达核心规则，不依赖 Web 框架、数据库连接或第三方 SDK。
- Repository/DAO 层负责持久化访问，不写业务决策。
- External Client/Adapter 负责第三方或跨服务调用，不把外部 SDK 类型泄漏到核心业务层。
- Infrastructure 层实现具体技术细节，通过接口或适配层被上层使用。

项目实际分层：

```text
{BACKEND_MODULE_STRUCTURE}
{FRONTEND_MODULE_STRUCTURE}
```

## 3. 模块边界 [通用 + 个性化]

模块必须按职责聚合，禁止为单个需求随意散落文件。

推荐模块结构应在初始化时生成。例如：

```text
{BACKEND_MODULE_STRUCTURE}
```

通用要求：

- 一个业务模块内部可以包含 router/controller、schema/dto、service/use-case、repository/dao、model/entity、tests。
- 跨模块共享内容放入 `src/shared/` 或项目约定共享层。
- 媒体、文件、对象存储、导入导出、模型文件等基础能力应集中到独立模块或 adapter。
- 权限、认证、审计、配置、错误码等横切能力应集中管理。
- 不允许在页面、路由或命令入口中复制已有业务逻辑。

## 4. 代码风格与复杂度 [通用]

通用代码质量要求：

- 函数单一职责，一个函数只做一类事情。
- 优先使用 guard clause，减少深层嵌套。
- 嵌套层级建议不超过 3 层。
- 参数过多时使用对象、数据类、DTO 或配置结构封装。
- 复杂条件应提取为具名函数或策略对象。
- 公共函数必须有清晰输入输出，不依赖隐藏全局状态。
- 魔法数字、魔法字符串应提取为常量或配置。
- 删除无用代码、无用 import、无用注释。
- 注释解释“为什么”和边界，不复述代码“做了什么”。

格式化与静态检查命令：

```bash
{FORMAT_COMMAND}
{LINT_COMMAND}
{TYPECHECK_COMMAND}
```

如果项目未配置命令，初始化时标记为 `待确认`，不得生成虚假命令。

## 5. 错误处理 [通用]

错误处理必须可定位、可测试、可转换为用户或调用方可理解的信息。

要求：

- 不裸抛泛化异常，例如无上下文的 `Exception`、`Error`。
- 不吞异常；捕获后必须处理、转换、记录或重新抛出。
- 外部服务错误必须转换为项目内部错误类型或错误码。
- 用户输入错误、权限错误、业务状态错误、外部服务错误、内部错误应区分。
- 日志不得记录密钥、token、真实敏感数据。
- 面向用户的错误信息不得泄露 SQL、堆栈、内部路径或第三方凭据。

错误码与 API 响应详见：

```text
rules/api.md
docs/error-codes.md
```

## 6. 后端编码规范 [条件启用]

后端技术栈：

```text
{BACKEND_STACK}
```

通用后端规则：

- 路由/API 层不得直接访问数据库或对象存储。
- Service/Use Case 层不得包含 HTTP 路由细节。
- Repository/DAO 层不得包含业务策略。
- Schema/DTO 与数据库模型应分离，除非项目明确采用同一模型。
- 所有输入必须通过 Schema 或等价机制校验。
- I/O 操作应遵循技术栈推荐的同步/异步模型，不混用造成阻塞。
- 数据库访问必须通过 Repository、DAO、ORM Session 或统一数据访问层。
- 事务边界必须清晰，跨多个写操作时明确提交和回滚策略。
- 外部 HTTP、对象存储、队列、模型服务调用必须经 client/adapter 封装。

Python/FastAPI 项目可采用：

```text
API Layer       app/api/          -> 路由、依赖注入、请求校验、响应格式化
Service Layer   app/services/     -> 业务逻辑、事务编排、外部服务调用
Repository      app/repositories/ -> 数据库 CRUD
Model/Schema    app/models/、app/schemas/
Core            app/core/         -> 配置、错误、日志、安全
```

Python 风格建议：

- 使用类型提示。
- 使用 `str | None`、`list[str]` 等现代类型写法，除非项目版本不支持。
- import 顺序：标准库、第三方、本地模块。
- I/O 密集接口优先使用 async/await，但必须与数据库 driver、HTTP client 匹配。
- 包管理器、Python 版本、格式化工具按项目配置执行。

## 7. 前端编码规范 [条件启用]

前端技术栈：

```text
{FRONTEND_STACK}
```

推荐分层：

```text
UI Layer          页面、组件、布局，仅展示和交互
State/Hook Layer  状态、组合逻辑、副作用
Service Layer     API client、WebSocket、缓存、端能力适配
Shared Layer      共享类型、工具函数、Design Token、基础组件
```

通用前端规则：

- UI 组件不直接拼接 API URL，不直接处理底层鉴权细节。
- API 类型和客户端优先从 OpenAPI 或契约生成。
- 组件优先组合已有组件、模板和 Design System。
- 状态管理只放必要状态，避免复制服务端数据造成不一致。
- 条件渲染优先清晰表达，避免过深三元表达式。
- 副作用集中管理，避免在组件多处重复请求。
- className 合并、主题 token、图标库、组件库使用项目既有约定。

组件文件建议结构：

```text
1. imports
2. types / props
3. constants
4. component
5. hooks / state / derived values
6. handlers
7. render
```

自定义 Hook 或 composable 仅在以下情况创建：

- 3 个以上组件复用。
- 包含复杂状态、副作用或订阅。
- 逻辑足够独立，能被测试或单独理解。

## 8. 移动端与小程序规范 [条件启用]

移动端/小程序技术栈：

```text
{MOBILE_STACK}
```

规则：

- 端目录仅承载对应端代码，不混入 Web 浏览器专属 API。
- 文件上传、视频播放、图片预览、定位、相机、通知等能力必须走端能力适配层。
- API、鉴权、缓存、错误处理应与其他端保持契约一致。
- 需要考虑端版本、平台权限、离线、弱网和兼容性。
- 不在端代码中硬编码生产服务地址或密钥。

## 9. 数据库与数据访问代码 [条件启用]

数据库技术栈：

```text
{DATABASE_STACK}
```

规则：

- 所有数据库访问通过 Repository、DAO、ORM 或统一数据访问层。
- 不在 Controller、页面或任务入口直接拼 SQL。
- 查询必须考虑索引、分页、排序和过滤边界。
- 写操作必须明确事务边界。
- migration、schema、model、repository、测试数据必须同步。
- 不在测试或本地脚本中依赖真实生产数据。

详见：

```text
rules/database.md
rules/data-management.md
```

## 10. 文件、媒体、对象存储与模型代码 [条件启用]

对象存储：

```text
{OBJECT_STORAGE_STACK}
```

算法/模型：

```text
{ALGORITHM_STACK}
```

规则：

- 文件、媒体、导入导出、对象存储访问必须集中在 adapter/client/service 中。
- 不在业务模块中散落 bucket、object key、签名 URL 拼接逻辑。
- 上传必须校验大小、MIME、权限和存储路径。
- 模型文件、模型权重、训练数据默认不提交到 Git；只提交说明、校验和和下载指引。
- 推理代码必须明确输入输出 Schema、模型版本、资源要求和错误处理。

## 11. 异步任务与后台作业 [条件启用]

异步任务技术栈：

```text
{ASYNC_TASK_STACK}
```

规则：

- 长耗时任务不得阻塞请求线程或 UI 主线程。
- 任务必须有状态、进度、结果、失败原因和可追踪 ID。
- 任务应具备幂等或去重策略。
- 重试必须有上限和退避策略。
- 任务失败应可观测、可补偿、可重新执行。
- 定时任务、队列任务、Webhook 处理必须记录关键日志和关联 ID。

## 12. 共享类型与代码生成 [条件启用]

涉及前后端共享类型、SDK、OpenAPI 客户端、GraphQL、protobuf 或其他生成代码时启用本节。

规则：

- 生成产物必须有明确源文件和生成命令。
- 不手写会被生成工具覆盖的文件。
- 生成代码与手写封装分目录管理。
- 修改契约后必须重新生成并运行类型检查。
- 共享类型不得引入某一端运行时依赖，除非项目明确允许。

## 13. 依赖管理 [通用]

- 新增依赖必须说明用途、替代方案和影响范围。
- 优先使用项目已有依赖和标准库。
- 不引入重型依赖解决小问题。
- 不引入无人维护、许可不明或安全风险明显的依赖。
- 前端依赖、后端依赖、算法依赖、工具依赖应放在各自模块的依赖文件中。
- 新增依赖后必须更新锁文件或项目约定的依赖快照。

## 14. AI 修改代码规则 [通用]

AI 修改代码时必须：

- 先阅读相关上下文和现有模式。
- 保持修改范围最小，避免无关重构。
- 保护用户已有无关改动。
- 同步更新测试、文档、OpenSpec、类型或生成产物。
- 删除临时调试输出。
- 运行与改动范围匹配的验证命令。
- 在回复中说明影响 API、数据库、UI、部署、安全、对象存储或模型的情况。

AI 不得：

- 为了通过当前任务复制粘贴大段重复代码。
- 绕过项目分层直接调用底层实现。
- 在生产代码中留下 mock、stub、TODO 作为最终实现。
- 静默改变公共接口、环境变量、数据结构或权限逻辑。

## 15. 完成任务后检查清单 [通用 + 条件启用]

```text
□ 是否遵守架构分层和模块边界
□ 是否复用已有工具、组件、client、adapter、类型
□ 是否避免无关重构和大范围格式化
□ 是否保护用户已有无关改动
□ 是否处理错误、权限、输入校验和边界情况
□ 是否同步测试、文档、OpenSpec 或生成产物
□ 后端变更：是否遵守 API / Service / Repository / DB 边界
□ 前端变更：是否遵守组件、状态、服务分层
□ 数据库变更：是否同步 schema、migration、repository、测试
□ 文件/媒体变更：是否集中在 adapter/service 并校验权限和 MIME
□ 异步任务变更：是否有状态、重试、幂等和失败记录
□ 依赖变更：是否说明原因并更新锁文件
□ 是否运行格式化、lint、类型检查和相关测试
```

## 16. 初始化生成建议 [通用]

工程初始化工具生成 `rules/coding.md` 时应：

1. 保留 [通用] 模块。
2. 用用户输入替换 [个性化] 占位符。
3. 根据项目技术栈保留或删除 [条件启用] 模块。
4. 根据后端框架生成实际分层和模块结构。
5. 根据前端、移动端、小程序、算法、对象存储、异步任务能力生成对应规则。
6. 从实际项目脚本生成格式化、lint、类型检查命令；未知时标记 `待确认`。
7. 删除指向不存在目录、命令、框架或模块的内容。
8. 保持 coding.md 与 language.md、api.md、database.md、testing.md、directory-structure.md 一致。
