---
purpose: Web 端兼容适配说明
content: Web 端支持范围、浏览器矩阵、响应式断点、Web API、构建目标、网络与弱网、上传下载、安全、可访问性、测试矩阵和初始化生成规则
source: Harness compatibility/devices/web.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；产品形态、浏览器范围、前端技术栈、UI 规范、Web API 或部署策略变化时更新；后续由 AI 辅助更新并经人工 Review
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {FRONTEND_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/devices/web.md 独立模块
---

# Web 端兼容说明

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 的 Web 端兼容范围、浏览器支持、响应式策略、Web API 使用边界、构建目标、网络容错、安全约束、可访问性和测试要求。

本文重点回答：

- Web 端需要支持哪些浏览器、系统、屏幕尺寸和 WebView。
- 前端构建目标、Polyfill、CSS 能力和运行时特性如何约束。
- 哪些 Web API 可以使用，哪些能力必须做降级或 feature detection。
- 管理后台、展示端、移动 H5、PWA 或嵌入页的兼容边界是什么。
- 工程初始化时如何根据用户输入生成项目专属 Web 兼容说明。

相关文档：

- 兼容性规范：`rules/compatibility.md`
- UI 设计规范：`rules/ui-design.md`
- 前端编码规范：`rules/coding.md`
- 测试规范：`rules/testing.md`
- API 规范：`rules/api.md`
- 安全规范：`rules/security.md`
- Web 端源码：`src/frontend/`
- 前端测试标准：`docs/standards/frontend-test-standard.md`

## 1. 初始化生成参数 `[个性化]`

工程初始化生成本文时，应优先使用用户输入和自动派生配置填充以下参数。缺失信息必须标记为 `待确认`，不得编造浏览器版本、测试结果或客户环境。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{FRONTEND_OWNER}` | Web 端负责人或维护角色 | 待确认 |
| `{PRODUCT_FORMS}` | 产品形态 | Web、管理后台、H5 |
| `{WEB_USAGE_SCOPE}` | Web 使用范围 | 展示端 / 管理后台 / 控制台 / H5 |
| `{FRONTEND_STACK}` | 前端技术栈 | React + TypeScript + Tailwind + Shadcn/UI |
| `{FRONTEND_FRAMEWORK}` | 前端框架 | React / Vue / Next.js |
| `{STYLE_SYSTEM}` | 样式系统 | Tailwind / CSS Modules / Sass |
| `{COMPONENT_LIBRARY}` | 组件库 | Shadcn/UI / Ant Design |
| `{BROWSER_SUPPORT_MATRIX}` | 浏览器支持矩阵 | Chrome、Edge、Safari、Firefox |
| `{BROWSERSLIST_TARGET}` | 构建目标 | `last 2 Chrome versions` |
| `{RESPONSIVE_POLICY}` | 响应式策略 | desktop-first / mobile-first |
| `{WEB_BREAKPOINTS}` | 断点 | 360 / 768 / 1024 / 1440 |
| `{ACCESSIBILITY_TARGET}` | 可访问性目标 | WCAG 2.1 AA / 待确认 |
| `{WEB_API_REQUIREMENTS}` | 关键 Web API | Clipboard、WebSocket、File API |
| `{UPLOAD_ENABLED}` | 是否启用上传 | true / false |
| `{MEDIA_ENABLED}` | 是否启用媒体预览 | true / false |
| `{AUTH_STRATEGY}` | 认证策略 | Cookie Session / JWT / SSO |
| `{WEB_TEST_COMMAND}` | Web 兼容测试命令 | 待确认 |
| `{FRONTEND_CHECK_COMMAND}` | 前端检查命令 | 待确认 |
| `{E2E_TEST_COMMAND}` | E2E 测试命令 | 待确认 |

## 2. Web 使用范围 `[通用 + 个性化]`

当前 Web 使用范围：

```text
{WEB_USAGE_SCOPE}
```

支持的 Web 形态：

| 形态 | 是否启用 | 入口 | 主要用户 | 兼容重点 |
|---|---|---|---|---|
| 展示端 | `{HAS_WEB_PORTAL}` | `{WEB_PORTAL_ENTRY}` | `{WEB_PORTAL_USERS}` | 首屏、SEO、媒体、响应式 |
| 管理后台 | `{HAS_WEB_ADMIN}` | `{WEB_ADMIN_ENTRY}` | `{WEB_ADMIN_USERS}` | 表格、表单、权限、高频操作 |
| 控制台/工作台 | `{HAS_WEB_CONSOLE}` | `{WEB_CONSOLE_ENTRY}` | `{WEB_CONSOLE_USERS}` | 数据密度、图表、快捷操作 |
| 移动 H5 | `{HAS_H5}` | `{H5_ENTRY}` | `{H5_USERS}` | 小屏、触控、弱网、WebView |
| 嵌入页/WebView | `{HAS_WEBVIEW}` | `{WEBVIEW_ENTRY}` | `{WEBVIEW_HOST}` | 宿主限制、登录态、尺寸适配 |
| PWA | `{HAS_PWA}` | `{PWA_ENTRY}` | `{PWA_USERS}` | 离线、缓存、安装、更新 |

未启用的形态不得保留强制要求。

## 3. 浏览器支持矩阵 `[通用 + 个性化]`

当前浏览器支持矩阵：

```text
{BROWSER_SUPPORT_MATRIX}
```

推荐矩阵：

| 平台 | 浏览器/运行环境 | 最低版本 | 支持级别 | 验证方式 | 说明 |
|---|---|---|---|---|---|
| Windows | Chrome | `{CHROME_MIN_VERSION}` | 必须支持 | `{CHROME_VERIFY}` | 主力浏览器 |
| Windows | Edge | `{EDGE_MIN_VERSION}` | 必须支持 | `{EDGE_VERIFY}` | 企业环境常见 |
| macOS | Safari | `{SAFARI_MIN_VERSION}` | 条件支持 | `{SAFARI_VERIFY}` | 目标用户使用时启用 |
| macOS/Linux | Firefox | `{FIREFOX_MIN_VERSION}` | 条件支持 | `{FIREFOX_VERIFY}` | 声明支持时启用 |
| iOS | Safari / WKWebView | `{IOS_SAFARI_MIN_VERSION}` | 条件支持 | `{IOS_VERIFY}` | H5/WebView 启用 |
| Android | Chrome / WebView | `{ANDROID_CHROME_MIN_VERSION}` | 条件支持 | `{ANDROID_VERIFY}` | H5/WebView 启用 |
| 微信内置浏览器 | WeChat WebView | `{WECHAT_WEBVIEW_MIN_VERSION}` | 条件支持 | `{WECHAT_WEBVIEW_VERIFY}` | 分享页/H5 启用 |

规则：

- 兼容范围必须写明确版本，不能只写“主流浏览器”。
- 使用新 Web API、CSS 能力或 JavaScript 语法前，必须确认最低支持版本。
- 不支持的浏览器必须有提示、降级方案或文档说明。
- WebView、微信小程序、桌面浏览器不得混为同一兼容范围。

## 4. 构建目标与 Polyfill `[通用 + 个性化]`

当前构建目标：

```text
{BROWSERSLIST_TARGET}
```

构建配置必须与浏览器支持矩阵一致：

| 配置项 | 当前值 | 说明 |
|---|---|---|
| browserslist | `{BROWSERSLIST_TARGET}` | 浏览器编译目标 |
| TypeScript target | `{TYPESCRIPT_TARGET}` | JS 输出版本 |
| bundler target | `{BUNDLER_TARGET}` | Vite/Webpack/Next 构建目标 |
| CSS 处理 | `{CSS_COMPAT_TOOL}` | autoprefixer / postcss |
| Polyfill 策略 | `{POLYFILL_POLICY}` | 按需 / 禁用 / 手工 |

规则：

- 构建目标不能高于声明支持的最低浏览器能力。
- 新增 Polyfill 必须评估体积、加载顺序和浏览器副作用。
- 不能依赖开发浏览器默认支持来判断生产兼容性。
- 版本升级必须同步 `package.json`、构建配置、测试配置和本文。

## 5. 响应式与布局兼容 `[通用 + 个性化]`

响应式策略：

```text
{RESPONSIVE_POLICY}
```

断点：

```text
{WEB_BREAKPOINTS}
```

推荐验证视口：

| 类型 | 宽度 | 场景 |
|---|---:|---|
| small mobile | 360px | H5、小屏手机 |
| mobile | 390px / 414px | 主流手机 |
| tablet | 768px | 平板、窄屏 |
| laptop | 1280px | 常规桌面 |
| desktop | 1440px | 主力桌面 |
| wide | 1920px | 大屏展示/后台 |

规则：

- 管理后台应优先保证 1280px 以上的高效操作，同时给出窄屏处理策略。
- 展示端和 H5 必须覆盖小屏、触控、横竖屏和长文本。
- 表格、工具栏、卡片、弹窗和上传组件不得因动态内容挤压变形。
- 长文本必须有换行、截断、Tooltip 或展开策略。
- 不得出现文本重叠、按钮溢出、浮层被裁切、内容被固定头尾遮挡。

## 6. Web API 能力边界 `[通用 + 个性化]`

当前关键 Web API：

```text
{WEB_API_REQUIREMENTS}
```

能力矩阵：

| 能力 | API | 使用场景 | 兼容要求 | 降级策略 |
|---|---|---|---|---|
| 剪贴板 | Clipboard API | `{CLIPBOARD_SCENARIO}` | HTTPS/localhost | 手动复制提示 |
| 文件选择 | File API | `{FILE_SCENARIO}` | 浏览器支持 | 普通 input |
| 拖拽 | Drag and Drop | `{DND_SCENARIO}` | 桌面端优先 | 点击上传 |
| 下载 | Blob / Object URL | `{DOWNLOAD_SCENARIO}` | 文件名兼容 | 服务端下载 |
| 实时通信 | WebSocket / SSE | `{REALTIME_SCENARIO}` | 网络与代理 | 轮询 |
| 本地缓存 | localStorage / IndexedDB | `{CACHE_SCENARIO}` | 容量和隐私模式 | 内存缓存 |
| 加密随机 | Web Crypto | `{CRYPTO_SCENARIO}` | 安全上下文 | 服务端生成 |
| 媒体 | audio/video/canvas | `{MEDIA_SCENARIO}` | 格式与自动播放限制 | 下载或静态预览 |

规则：

- 所有非基础 Web API 必须有 feature detection 或明确支持范围。
- 依赖安全上下文的能力必须考虑 HTTPS、localhost 和 WebView 限制。
- 浏览器禁用第三方 Cookie、隐私模式、存储清理时，认证和缓存必须有可预期表现。

## 7. 网络、API 与弱网兼容 `[通用]`

Web 端网络规则：

- API 请求必须有超时、错误处理和用户可理解的反馈。
- 重试必须具备幂等性判断，不能对非幂等写操作盲目重试。
- 上传、下载、导入导出、长任务必须有进度、失败、重试或恢复策略。
- 弱网、断网、接口 4xx/5xx、超时、取消请求必须有测试。
- 前端错误码、API 响应结构和认证过期处理必须与 `rules/api.md`、`rules/security.md` 一致。

## 8. 上传、下载与媒体 `[条件启用]`

当 `{UPLOAD_ENABLED}` 或 `{MEDIA_ENABLED}` 为 true 时启用。

| 能力 | 兼容要求 | 验证重点 |
|---|---|---|
| 文件上传 | 文件类型、大小、进度、取消、失败重试 | input、拖拽、移动端选择 |
| 文件下载 | 文件名、Content-Disposition、Blob、跨域 | 中文文件名、失败提示 |
| 图片预览 | 格式、尺寸、懒加载、错误占位 | WebP/PNG/JPEG |
| 音视频预览 | 编码、控制条、自动播放限制 | mp4、音频、移动端 |
| 大文件 | 分片、断点、超时、并发数 | 对象存储后端一致 |

规则：

- 前端文件限制必须与后端和对象存储策略一致。
- 不能只依赖前端限制文件类型和大小。
- 媒体预览失败必须有占位、下载或错误说明。

## 9. 认证、安全与隐私 `[通用 + 个性化]`

认证策略：

```text
{AUTH_STRATEGY}
```

Web 安全兼容规则：

- 登录态、Cookie、Token、刷新机制必须兼容目标浏览器隐私策略。
- 跨域、SameSite、Secure、HttpOnly、CSRF、CSP 必须与部署域名一致。
- 前端不得持久化明文密码、密钥、长效 Token 或敏感业务数据。
- 敏感字段必须脱敏展示，复制、导出、截图场景需遵守安全规范。
- XSS、路径跳转、文件预览、富文本、Markdown、iframe 必须有防护策略。

## 10. 可访问性与输入设备 `[通用 + 个性化]`

可访问性目标：

```text
{ACCESSIBILITY_TARGET}
```

规则：

- 表单、按钮、链接、菜单、弹窗、Toast、上传、分页必须有可理解的名称和状态。
- 键盘可达性应覆盖核心流程，尤其是后台管理和表单场景。
- 焦点状态、错误提示、加载状态、禁用状态必须清晰。
- 文本与背景对比度应符合项目可访问性目标。
- 触控目标尺寸、hover 依赖、右键操作必须考虑移动端和触控设备。

## 11. 兼容测试矩阵 `[通用 + 个性化]`

推荐测试矩阵：

| 测试域 | Chrome | Edge | Safari | Firefox | Mobile/WebView | 状态 |
|---|---|---|---|---|---|---|
| 首屏渲染 | 必测 | 必测 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 登录与认证 | 必测 | 必测 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 核心流程 | 必测 | 必测 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 表单校验 | 必测 | 必测 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 表格/列表 | 必测 | 必测 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 上传下载 | 条件启用 | 条件启用 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 媒体预览 | 条件启用 | 条件启用 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 响应式布局 | 必测 | 必测 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 弱网错误 | 必测 | 必测 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 可访问性 | 必测 | 必测 | 条件启用 | 条件启用 | 条件启用 | 待确认 |

推荐命令：

```bash
{FRONTEND_CHECK_COMMAND}
{WEB_TEST_COMMAND}
{E2E_TEST_COMMAND}
```

测试结果不得在模板中伪造，未验证项必须保留 `待确认`。

## 12. 不支持范围与降级策略 `[通用 + 个性化]`

不支持范围：

```text
{WEB_UNSUPPORTED_RANGE}
```

降级策略：

| 不支持能力 | 用户提示 | 替代方案 | 负责人 |
|---|---|---|---|
| `{UNSUPPORTED_FEATURE}` | `{USER_MESSAGE}` | `{FALLBACK}` | `{OWNER}` |

规则：

- 不支持范围必须明确，不能含糊写“低版本浏览器不支持”。
- 关键功能无法降级时，应在产品、部署或客户交付文档中说明。
- 用户提示不得暴露内部实现细节。

## 13. AI Agent 更新规则 `[通用]`

AI Agent 在处理 Web 兼容变更时必须：

- 先读取 `rules/compatibility.md`、`rules/ui-design.md`、本文和相关测试标准。
- 确认当前 `{FRONTEND_STACK}`、`{BROWSER_SUPPORT_MATRIX}`、`{RESPONSIVE_POLICY}` 和测试命令。
- 使用新 Web API、CSS 能力、浏览器特性前，必须检查支持范围并写入降级策略。
- 涉及页面、组件、布局、上传、媒体、认证、网络错误处理时，必须同步更新兼容测试矩阵。
- 对无法确认的浏览器版本、WebView 能力、客户环境、测试结果标记 `待确认`。
- 不得编造浏览器测试通过结果或客户环境支持范围。

## 14. 初始化生成规则 `[通用]`

作为工程初始化模块使用时：

- **默认保留**：文档定位、使用范围、浏览器矩阵、构建目标、响应式、Web API、网络弱网、安全、可访问性、测试矩阵、AI 更新规则。
- **根据输入生成**：产品形态、Web 入口、前端技术栈、组件库、浏览器范围、断点、认证策略、上传/媒体能力、测试命令。
- **条件启用**：管理后台、H5、WebView、PWA、上传下载、媒体预览、SEO、可访问性强化、私有化客户浏览器要求。
- **不得沿用来源项目内容**：业务页面名、真实客户浏览器版本、测试结果、来源项目特定入口和部署域名。

生成完成后，本文必须与以下文件保持一致：

- `rules/compatibility.md`
- `rules/ui-design.md`
- `rules/testing.md`
- `docs/05-compatibility-matrix.md`
- `docs/standards/frontend-test-standard.md`
- `package.json`
- 前端构建配置和测试配置
