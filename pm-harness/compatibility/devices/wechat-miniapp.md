---
purpose: 微信小程序兼容适配说明
content: 微信小程序支持范围、基础库版本、机型系统、分包体积、平台 API、网络域名、授权登录、上传下载、媒体、缓存、安全、审核、测试矩阵和初始化生成规则
source: Harness compatibility/devices/wechat-miniapp.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；产品形态、微信基础库、端能力、平台 API、上传下载、登录授权或发布审核策略变化时更新；后续由 AI 辅助更新并经人工 Review
owner: {WECHAT_MINIAPP_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/devices/wechat-miniapp.md 独立模块
---

# 微信小程序兼容说明

> 模块标记说明：
>
> - **[通用]**：适用于大多数微信小程序 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入、端能力、技术栈和目标用户生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应场景时才保留或展开，例如微信登录、订阅消息、上传下载、图片/音视频、定位、扫码、支付、WebView、分包。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 微信小程序端的兼容范围、基础库版本、设备系统、平台 API、网络请求、授权登录、上传下载、媒体能力、缓存、安全、审核和测试要求。

本文重点回答：

- 微信小程序需要支持哪些基础库版本、微信版本、iOS/Android 系统和设备范围。
- 哪些能力依赖微信平台 API、用户授权、后台配置或域名白名单。
- 小程序包体积、分包、资源加载、缓存和弱网策略如何约束。
- 上传下载、图片、音频、视频、扫码、定位、订阅消息、支付等能力如何兼容。
- 工程初始化时如何根据用户输入生成项目专属微信小程序兼容说明。

相关文档：

- 兼容性规范：`rules/compatibility.md`
- UI 设计规范：`rules/ui-design.md`
- 媒体规范：`rules/media.md`
- API 规范：`rules/api.md`
- 安全规范：`rules/security.md`
- 测试规范：`rules/testing.md`
- 微信小程序源码：`src/wechat-miniapp/`
- 前端测试标准：`docs/standards/frontend-test-standard.md`

## 1. 初始化生成参数 `[个性化]`

工程初始化生成本文时，应优先使用用户输入和自动派生配置填充以下参数。缺失信息必须标记为 `待确认`，不得编造基础库版本、审核结果或平台能力。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{WECHAT_MINIAPP_OWNER}` | 微信小程序负责人或维护角色 | 待确认 |
| `{HAS_WECHAT_MINIAPP}` | 是否启用微信小程序 | true / false |
| `{WECHAT_MINIAPP_APPID}` | 小程序 AppID | 待确认 |
| `{WECHAT_MINIAPP_USAGE_SCOPE}` | 小程序使用范围 | 展示端 / 业务办理 / 管理辅助 |
| `{WECHAT_MINIAPP_STACK}` | 小程序技术栈 | 原生 / Taro / uni-app / Remax |
| `{WECHAT_BASE_LIBRARY_MIN_VERSION}` | 最低基础库版本 | 待确认 |
| `{WECHAT_VERSION_RANGE}` | 微信客户端版本范围 | 待确认 |
| `{MOBILE_OS_SUPPORT_MATRIX}` | iOS/Android 支持矩阵 | 待确认 |
| `{WECHAT_MINIAPP_FEATURES}` | 小程序能力清单 | 登录、上传、扫码、订阅消息 |
| `{WECHAT_DOMAIN_CONFIG}` | request/upload/download/socket 合法域名 | 待确认 |
| `{WECHAT_AUTH_STRATEGY}` | 微信登录与授权策略 | code2session / 手机号授权 / SSO |
| `{UPLOAD_ENABLED}` | 是否启用上传 | true / false |
| `{MEDIA_ENABLED}` | 是否启用媒体预览 | true / false |
| `{OBJECT_STORAGE_STACK}` | 对象存储方案 | MinIO / COS / OSS / S3 |
| `{WECHAT_PACKAGE_POLICY}` | 包体积与分包策略 | 主包 + 分包 |
| `{WECHAT_RELEASE_POLICY}` | 体验版、审核、发布策略 | 待确认 |
| `{WECHAT_MINIAPP_TEST_COMMAND}` | 小程序测试命令 | 待确认 |

## 2. 小程序使用范围 `[通用 + 个性化]`

当前小程序使用范围：

```text
{WECHAT_MINIAPP_USAGE_SCOPE}
```

能力范围：

| 能力 | 是否启用 | 入口/页面 | 依赖 | 兼容重点 |
|---|---|---|---|---|
| 展示浏览 | `{WECHAT_FEATURE_VIEW}` | `{WECHAT_VIEW_PAGES}` | API/媒体 | 首屏、图片、弱网 |
| 表单提交 | `{WECHAT_FEATURE_FORM}` | `{WECHAT_FORM_PAGES}` | API/登录态 | 校验、错误提示、重复提交 |
| 微信登录 | `{WECHAT_FEATURE_LOGIN}` | `{WECHAT_LOGIN_PAGES}` | 微信 API/后端 | code、session、授权 |
| 文件上传 | `{WECHAT_FEATURE_UPLOAD}` | `{WECHAT_UPLOAD_PAGES}` | uploadFile/对象存储 | 大小、格式、失败重试 |
| 媒体预览 | `{WECHAT_FEATURE_MEDIA}` | `{WECHAT_MEDIA_PAGES}` | 图片/音视频 API | 格式、缓存、播放限制 |
| 扫码 | `{WECHAT_FEATURE_SCAN}` | `{WECHAT_SCAN_PAGES}` | scanCode | 权限、异常、识别失败 |
| 订阅消息 | `{WECHAT_FEATURE_SUBSCRIBE}` | `{WECHAT_SUBSCRIBE_PAGES}` | 模板消息 | 用户授权、频控 |
| 支付 | `{WECHAT_FEATURE_PAY}` | `{WECHAT_PAY_PAGES}` | 微信支付 | 签名、失败、回调 |
| WebView | `{WECHAT_FEATURE_WEBVIEW}` | `{WECHAT_WEBVIEW_PAGES}` | 业务域名 | 白名单、登录态、回退 |

未启用的能力不得保留强制测试项、环境变量或 API 要求。

## 3. 基础库、微信版本与系统矩阵 `[通用 + 个性化]`

当前最低基础库版本：

```text
{WECHAT_BASE_LIBRARY_MIN_VERSION}
```

支持矩阵：

| 平台 | 运行环境 | 最低版本 | 支持级别 | 验证方式 | 说明 |
|---|---|---|---|---|---|
| 微信基础库 | Mini Program Base Library | `{WECHAT_BASE_LIBRARY_MIN_VERSION}` | 必须支持 | `{WECHAT_BASE_VERIFY}` | 平台 API 基线 |
| 微信客户端 | WeChat | `{WECHAT_VERSION_RANGE}` | 必须支持 | `{WECHAT_CLIENT_VERIFY}` | iOS/Android 均需验证 |
| iOS | iPhone / iPad | `{IOS_MIN_VERSION}` | 条件支持 | `{IOS_VERIFY}` | 目标用户使用时启用 |
| Android | Android Phone | `{ANDROID_MIN_VERSION}` | 条件支持 | `{ANDROID_VERIFY}` | 低端机性能需验证 |
| 微信开发者工具 | DevTools | `{WECHAT_DEVTOOLS_VERSION}` | 开发验证 | `{DEVTOOLS_VERIFY}` | 不能替代真机验证 |

规则：

- 兼容范围必须写明确版本，不能只写“微信最新版”。
- 使用新微信 API 前必须确认最低基础库版本和降级方式。
- 开发者工具通过不代表真机通过，关键流程必须真机验证。
- iOS 与 Android 在授权、文件、音视频、WebView、输入法和键盘行为上必须分别验证。

## 4. 技术栈与构建发布 `[通用 + 个性化]`

当前小程序技术栈：

```text
{WECHAT_MINIAPP_STACK}
```

构建与发布配置：

| 配置项 | 当前值 | 说明 |
|---|---|---|
| AppID | `{WECHAT_MINIAPP_APPID}` | 项目真实 AppID，模板中可为待确认 |
| 技术栈 | `{WECHAT_MINIAPP_STACK}` | 原生 / 跨端框架 |
| 源码目录 | `src/wechat-miniapp/` | 小程序源码目录 |
| 构建命令 | `{WECHAT_BUILD_COMMAND}` | 待确认 |
| 预览命令 | `{WECHAT_PREVIEW_COMMAND}` | 待确认 |
| 上传命令 | `{WECHAT_UPLOAD_COMMAND}` | 待确认 |
| 发布策略 | `{WECHAT_RELEASE_POLICY}` | 体验版 / 审核 / 灰度 / 全量 |

规则：

- 小程序配置、AppID、合法域名、隐私协议、类目和插件必须与微信公众平台后台一致。
- 构建产物不得提交到模板，除非项目明确采用提交产物策略。
- 发布流程必须区分开发版、体验版、审核版和线上版。

## 5. 包体积、分包与资源加载 `[通用 + 个性化]`

包体积策略：

```text
{WECHAT_PACKAGE_POLICY}
```

规则：

- 主包只保留首屏、公共组件、公共样式和必要能力。
- 低频页面、管理页面、媒体处理、图表等应考虑分包。
- 大图片、视频、文档、模型文件不得打入小程序包，应使用对象存储或 CDN。
- 静态资源必须压缩，图标优先复用组件库或统一图标资产。
- 分包页面的路由、预加载和登录态必须测试。

推荐记录：

| 包 | 内容 | 体积目标 | 验证方式 |
|---|---|---:|---|
| 主包 | `{WECHAT_MAIN_PACKAGE_CONTENT}` | `{WECHAT_MAIN_PACKAGE_SIZE_TARGET}` | 待确认 |
| 分包 A | `{WECHAT_SUBPACKAGE_A_CONTENT}` | `{WECHAT_SUBPACKAGE_A_SIZE_TARGET}` | 待确认 |
| 分包 B | `{WECHAT_SUBPACKAGE_B_CONTENT}` | `{WECHAT_SUBPACKAGE_B_SIZE_TARGET}` | 待确认 |

## 6. 网络、域名与弱网 `[通用 + 个性化]`

合法域名配置：

```text
{WECHAT_DOMAIN_CONFIG}
```

必须记录：

| 类型 | 域名 | 用途 | 环境 |
|---|---|---|---|
| request | `{WECHAT_REQUEST_DOMAIN}` | API 请求 | dev/test/prod |
| uploadFile | `{WECHAT_UPLOAD_DOMAIN}` | 文件上传 | 条件启用 |
| downloadFile | `{WECHAT_DOWNLOAD_DOMAIN}` | 文件下载 | 条件启用 |
| socket | `{WECHAT_SOCKET_DOMAIN}` | 实时通信 | 条件启用 |
| web-view | `{WECHAT_WEBVIEW_DOMAIN}` | WebView 页面 | 条件启用 |

规则：

- 小程序网络请求必须使用 HTTPS 和平台配置的合法域名。
- API 请求必须有超时、错误提示、重试或手工刷新策略。
- 非幂等写操作不得盲目重试。
- 弱网、断网、接口 4xx/5xx、登录过期、域名配置错误必须有测试。
- 开发环境、测试环境和生产环境域名不得混用。

## 7. 登录、授权与隐私 `[通用 + 条件启用]`

微信授权策略：

```text
{WECHAT_AUTH_STRATEGY}
```

规则：

- 微信登录必须由后端完成 code/session 交换和业务用户绑定。
- 小程序端不得保存 session_key、后端密钥或长期敏感凭证。
- 手机号、头像、昵称、位置、相册、摄像头、麦克风等能力必须按需授权。
- 用户拒绝授权时必须有可理解的降级路径。
- 隐私协议、用户信息收集、数据用途必须与微信平台配置和 `rules/security.md` 一致。
- 登录态过期、账号解绑、多端登录、重复绑定必须有明确处理。

## 8. 页面、交互与移动端适配 `[通用 + 个性化]`

小程序 UI 适配规则：

- 页面必须适配常见手机宽度、刘海屏、安全区、底部导航和键盘弹出。
- 表单、弹窗、选择器、上传、图片预览、Toast、Loading 必须符合移动端触控习惯。
- 不得照搬桌面 Web 的密集表格和 hover 交互。
- 长列表应考虑分页、虚拟列表或懒加载。
- 空状态、加载态、失败态、无权限态必须完整。
- 文案、按钮和输入框不得在小屏设备上溢出或遮挡。

推荐验证设备：

| 设备类型 | 示例 | 验证重点 |
|---|---|---|
| 小屏 iPhone | `{SMALL_IOS_DEVICE}` | 宽度、安全区、键盘 |
| 大屏 iPhone | `{LARGE_IOS_DEVICE}` | 图片、表单、底部操作 |
| 常见 Android | `{ANDROID_DEVICE}` | 输入法、授权、性能 |
| 低端 Android | `{LOW_END_ANDROID_DEVICE}` | 启动、滚动、图片加载 |

## 9. 上传、下载与媒体 `[条件启用]`

当 `{UPLOAD_ENABLED}` 或 `{MEDIA_ENABLED}` 为 true 时启用。

| 能力 | 小程序 API | 兼容要求 | 验证重点 |
|---|---|---|---|
| 图片选择 | chooseMedia / chooseImage | 数量、大小、来源、压缩 | 相册/拍摄/取消 |
| 文件上传 | uploadFile | 进度、失败、重试、鉴权 | 弱网/超时/格式 |
| 文件下载 | downloadFile | 临时文件、保存、预览 | 权限/空间/失败 |
| 图片预览 | previewImage | 大图、长图、失败占位 | 滑动/加载 |
| 音频播放 | InnerAudioContext | 后台、暂停、错误 | iOS/Android 差异 |
| 视频播放 | video 组件 | 格式、全屏、控制条 | 自动播放限制 |
| 扫码 | scanCode | 权限、识别失败、异常值 | 不同光照和码类型 |

规则：

- 前端文件限制必须与后端、对象存储和 `rules/media.md` 一致。
- 大文件和媒体文件不得进入小程序包。
- 临时文件生命周期、缓存清理和失败重试必须明确。
- 图片、音频、视频格式必须结合微信小程序实际支持范围验证。

## 10. 缓存、离线与本地存储 `[通用 + 条件启用]`

规则：

- 本地缓存只保存可缓存、可恢复、低敏数据。
- 不得在本地存储明文密码、密钥、session_key、长期 Token 或高敏业务数据。
- 缓存必须有版本、过期、清理或覆盖策略。
- 断网时必须明确哪些页面可查看缓存，哪些操作需要联网。
- 本地草稿、上传队列、离线任务存在时，必须有冲突处理和重试机制。

## 11. 订阅消息、支付、定位与 WebView `[条件启用]`

### 11.1 订阅消息

- 必须按场景触发授权，不能强制或诱导用户授权。
- 模板 ID、消息内容和跳转页面必须与后台配置一致。
- 用户拒绝授权时必须有业务降级。

### 11.2 微信支付

- 支付参数必须由后端生成和签名。
- 支付成功必须以后端回调或订单查询为准，不能只信任前端结果。
- 取消、失败、重复支付、超时和补偿查询必须测试。

### 11.3 定位

- 定位必须说明用途，并处理拒绝授权、精度不足、系统关闭定位。
- 不需要定位的业务不得请求定位权限。

### 11.4 WebView

- WebView 域名必须在微信后台配置。
- WebView 与小程序登录态、返回路径、分享、支付、文件下载必须单独验证。
- 不得把 WebView 当作普通浏览器环境。

## 12. 审核、合规与发布 `[通用 + 个性化]`

发布策略：

```text
{WECHAT_RELEASE_POLICY}
```

规则：

- 小程序类目、隐私协议、用户数据收集说明必须与实际功能一致。
- 审核版本不得连接未授权生产数据或暴露测试入口。
- 新增授权、支付、订阅消息、定位、内容发布、用户生成内容时，必须评估审核要求。
- 发布前必须完成体验版验证、真机验证和关键路径回归。
- 审核驳回原因、修复方案和重新提交记录应归档。

## 13. 兼容测试矩阵 `[通用 + 个性化]`

推荐测试矩阵：

| 测试域 | iOS 微信 | Android 微信 | 开发者工具 | 低端设备 | 状态 |
|---|---|---|---|---|---|
| 启动与首屏 | 必测 | 必测 | 必测 | 条件启用 | 待确认 |
| 登录与授权 | 必测 | 必测 | 条件启用 | 条件启用 | 待确认 |
| 核心流程 | 必测 | 必测 | 必测 | 条件启用 | 待确认 |
| 表单与键盘 | 必测 | 必测 | 条件启用 | 条件启用 | 待确认 |
| 网络弱网 | 必测 | 必测 | 条件启用 | 条件启用 | 待确认 |
| 上传下载 | 条件启用 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 图片/音视频 | 条件启用 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 分包跳转 | 条件启用 | 条件启用 | 必测 | 条件启用 | 待确认 |
| 订阅消息/支付 | 条件启用 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 审核前回归 | 必测 | 必测 | 必测 | 条件启用 | 待确认 |

推荐命令：

```bash
{WECHAT_MINIAPP_TEST_COMMAND}
{WECHAT_BUILD_COMMAND}
{WECHAT_PREVIEW_COMMAND}
```

测试结果不得在模板中伪造，未验证项必须保留 `待确认`。

## 14. 不支持范围与降级策略 `[通用 + 个性化]`

不支持范围：

```text
{WECHAT_MINIAPP_UNSUPPORTED_RANGE}
```

降级策略：

| 不支持能力 | 用户提示 | 替代方案 | 负责人 |
|---|---|---|---|
| `{UNSUPPORTED_FEATURE}` | `{USER_MESSAGE}` | `{FALLBACK}` | `{OWNER}` |

规则：

- 不支持范围必须明确到基础库、微信版本、系统版本、设备类型或平台能力。
- 用户提示不得暴露内部实现细节。
- 关键能力无降级方案时，应在产品范围和发布说明中标注。

## 15. AI Agent 更新规则 `[通用]`

AI Agent 在处理微信小程序兼容变更时必须：

- 先读取 `rules/compatibility.md`、`rules/ui-design.md`、`rules/media.md`、本文和相关测试标准。
- 确认当前 `{WECHAT_MINIAPP_STACK}`、`{WECHAT_BASE_LIBRARY_MIN_VERSION}`、`{WECHAT_DOMAIN_CONFIG}` 和测试命令。
- 使用新微信 API 前，必须确认最低基础库版本、授权要求和降级策略。
- 涉及登录、授权、上传下载、媒体、订阅消息、支付、WebView、包体积、审核时，必须同步更新本文和测试矩阵。
- 对无法确认的基础库版本、真机测试结果、审核结果、后台配置标记 `待确认`。
- 不得编造微信审核通过、真机通过或平台后台配置结果。

## 16. 初始化生成规则 `[通用]`

作为工程初始化模块使用时：

- **默认保留**：文档定位、使用范围、基础库与设备矩阵、技术栈、包体积、网络域名、登录授权、移动端适配、缓存安全、审核发布、测试矩阵、AI 更新规则。
- **根据输入生成**：产品形态、小程序能力、技术栈、基础库版本、AppID、域名配置、授权策略、上传/媒体能力、发布策略、测试命令。
- **条件启用**：上传下载、图片/音视频、扫码、定位、订阅消息、支付、WebView、分包、离线缓存、低端设备适配。
- **不得沿用来源项目内容**：业务页面名、真实 AppID、真实域名、审核记录、测试结果、来源项目特定页面和平台配置。

生成完成后，本文必须与以下文件保持一致：

- `rules/compatibility.md`
- `rules/ui-design.md`
- `rules/media.md`
- `rules/security.md`
- `docs/05-compatibility-matrix.md`
- `src/wechat-miniapp/`
- 微信小程序项目配置、构建配置和测试配置
