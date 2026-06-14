# web-client Specification

## Purpose
TBD - created by archiving change add-user-login. Update Purpose after archive.
## Requirements
### Requirement: 管理端登录页

Web 客户端 MUST 提供管理端登录页，路由为 `/admin/login`，视觉 MUST 高保真对齐 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.html`（最高优先级）与 `user-login.png`（golden reference）。实现 MUST 采用 **CSS Port 策略**：自 `user-login.html` port 专用 stylesheet（`features/auth/styles/login-page.css`），React 负责 DOM 结构与 auth 交互。桌面端（1280px 视口）并排对比 PNG 时，布局、材质拼贴、氛围光感、控件形态、色彩与间距 MUST 被团队判定为一致或仅有可接受像素级偏差。颜色 MUST 引用 `globals.css` 的 `--color-*` token；TSX MUST NOT 含裸 Hex。

#### Scenario: 登录页布局

- **WHEN** 用户在桌面端（>= 1024px）访问 `/admin/login`
- **THEN** 页面 MUST 展示左右 50% 分屏：左侧 `.brand-panel`、右侧 `.form-panel`
- **AND** 页面 MUST 加载登录专用 CSS（`features/auth/styles/login-page.css`）

#### Scenario: 移动端布局

- **WHEN** 用户在移动端（< 1024px）访问 `/admin/login`
- **THEN** 页面 MUST 隐藏左侧品牌区（`display: none`）
- **AND** 登录表单 MUST 全屏居中，最大宽度 520px

#### Scenario: 登录表单元素

- **WHEN** 用户查看登录页
- **THEN** 页面 MUST 包含：`ADMIN PORTAL` 眉标、标题「登录管理端」、描述段落、账号 label + 输入框、密码 label + 输入框、记住登录状态复选框、忘记密码链接、登录按钮、企业微信全宽入口、语言切换、底部安全说明
- **AND** 表单 MUST NOT 包含 notice 横幅或页脚版权（© STONEX…）
- **AND** 密码输入框 MUST NOT 包含显隐切换 icon（对齐 HTML 原型）

#### Scenario: 左侧品牌背景

- **WHEN** 用户在桌面端查看登录页左栏
- **THEN** MUST 展示 HTML 原型等价结构：STONEX Logo、TILE DATA OPERATING SYSTEM 眉标、主标题、描述、三列统计卡、右下角 CSS 材质拼贴（`material-board` + 3 tiles）、底部 PRECISION · MATERIAL · INVENTORY
- **AND** MUST 叠加网格线与 radial glow 氛围层（对齐 `user-login.html`）
- **AND** MUST NOT 以 `/images/login-material-showcase.jpg` 全屏铺底替代材质拼贴

#### Scenario: 品牌 Logo 字体

- **WHEN** 用户查看登录页左栏 STONEX Logo
- **THEN** Logo MUST 使用衬线品牌字体（`font-brand` / Cormorant Garamond）
- **AND** MUST 保持大写字距（`tracking-brand`）与品牌金色

#### Scenario: 登录页组件结构

- **WHEN** 开发者查看登录页源码
- **THEN** 视觉样式 MUST 主要来自 port CSS class（`login-shell`、`brand-panel`、`form-panel`、`login-card` 等）
- **AND** auth 业务逻辑 MUST 保留在 `LoginForm` / hooks / store，不与 presentation CSS 耦合

### Requirement: 登录页原型静态资源

Web 客户端 MUST 在 `src/web/public/` 提供登录页原型所需静态资源，并随生产构建与 Docker Web 镜像部署。

#### Scenario: 背景图存在

- **WHEN** 构建 Web 生产包
- **THEN** `public/images/login-material-showcase.jpg` MUST 存在且可在 `/images/login-material-showcase.jpg` 访问

#### Scenario: 企业微信图标存在

- **WHEN** 渲染企业微信登录入口
- **THEN** MUST 使用 `public/icons/wecom.svg`（或等效 SVG），MUST NOT 使用纯文字「企」作为最终视觉

### Requirement: 登录页语言切换占位

Web 客户端 MUST 在登录页右栏右上角展示语言切换占位，视觉对齐 `user-login.html` `.language` 样式。

#### Scenario: 语言切换展示

- **WHEN** 用户查看登录页右栏
- **THEN** MUST 展示「简体中文⌄」文案于 `.language` 边框按钮内
- **AND** 点击 MAY noop；MUST NOT 要求完整 i18n 实现

### Requirement: 登录页 PNG 视觉验收 Gate

登录页视觉对齐 MUST 通过 PNG golden reference 验收 gate，方可标记 REQ-0001 视觉项完成。

#### Scenario: 桌面 PNG 并排验收

- **WHEN** 团队在 1280px 视口并排对比 `/admin/login` 与 `user-login.png`
- **THEN** diff checklist（背景色、50/50 分屏、Logo、材质拼贴、表单宽、输入高、focus 金边、按钮、间距、语言切换、无 notice 横幅、企微全宽按钮、安全说明）MUST 全部 pass
- **AND** 结果 MUST 记录在 change trace 与 sprint acceptance-report

#### Scenario: 构建与部署验证

- **WHEN** 执行 `vite build` 与 `docker compose build web`
- **THEN** 构建 MUST 成功且登录页 CSS、企微 SVG、字体可访问

### Requirement: 登录页控件原型形态

登录页表单控件 MUST 对齐 `user-login.html` 与 PNG 视觉；样式 MUST 来自 port CSS，MUST NOT 沿用 shadcn 默认态。

#### Scenario: 输入框默认与 focus 态

- **WHEN** 用户查看或 focus 账号/密码输入框
- **THEN** 默认边框 MUST 为 `1px solid` 且颜色等价 `--color-border-emphasis`（0.1 白）
- **AND** focus 时边框 MUST 变为纯品牌金（`--color-brand-gold`），背景 MAY 为极弱 white overlay
- **AND** MUST NOT 展示 ring-offset 或大偏移 focus ring

#### Scenario: 主按钮形态

- **WHEN** 用户查看登录按钮
- **THEN** 按钮 MUST 为 56px 高、全宽、金色实底、深色文字、2px 圆角（`.primary`）

#### Scenario: 表单控件为原生元素

- **WHEN** 开发者查看 `LoginForm` markup
- **THEN** 输入框与主按钮 MUST 为原生 `<input>` / `<button>` 并应用 port CSS class
- **AND** MUST NOT 使用 shadcn `Input` / `Button` / `Checkbox` 作为登录页最终视觉层

#### Scenario: 占位交互不破坏布局

- **WHEN** 用户点击语言切换、忘记密码或企业微信占位入口
- **THEN** 系统 MAY noop 或展示 inline/toast 弱提示
- **AND** MUST NOT 在表单区域上方插入 notice 横幅推挤布局

### Requirement: 企业微信图标视觉

企业微信登录入口 MUST 对齐 HTML `.wecom`：全宽横排按钮，非圆形 icon 卡片。

#### Scenario: 企微按钮形态

- **WHEN** 用户查看企业微信登录入口
- **THEN** MUST 展示全宽 54px 高按钮，左侧绿色企微 SVG（`/icons/wecom.svg`），文案「企业微信登录」
- **AND** MUST NOT 使用仅圆形 icon + 下方短文案的垂直布局

### Requirement: UI 设计规范登录页专章

项目 MUST 在 `rules/ui-design.md` 提供登录页设计专章，与 `user-login.html` 对齐，并说明 CSS Port 策略。

#### Scenario: 登录页规范存在

- **WHEN** 开发者查阅 `rules/ui-design.md`
- **THEN** MUST 找到登录页专章，涵盖 CSS Port 策略、色彩、字体、间距、组件态
- **AND** MUST 指向 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.html` 作为最高优先级视觉源

### Requirement: 登录表单校验

前端 MUST 在提交前校验表单必填字段，不通过时不发起 API 请求。

#### Scenario: 用户名为空

- **WHEN** 用户未填写用户名并点击登录
- **THEN** 系统 MUST 展示「请输入用户名」提示
- **AND** MUST NOT 调用登录 API

#### Scenario: 密码为空

- **WHEN** 用户未填写密码并点击登录
- **THEN** 系统 MUST 展示「请输入密码」提示
- **AND** MUST NOT 调用登录 API

#### Scenario: Enter 键提交

- **WHEN** 用户在用户名或密码输入框内按下 Enter 键
- **THEN** 系统 MUST 触发登录提交（若校验通过）

### Requirement: 登录提交与状态

前端 MUST 在登录过程中展示 loading 状态，防止重复提交。

#### Scenario: 登录 loading

- **WHEN** 用户点击登录且校验通过
- **THEN** 登录按钮 MUST 进入 loading/disabled 状态
- **AND** 请求完成前 MUST NOT 允许重复提交

#### Scenario: 登录成功跳转

- **WHEN** 登录 API 返回成功且用户 role 为 `admin` 或 `employee`
- **THEN** 前端 MUST 保存 token 与用户信息
- **AND** MUST 跳转至 `/admin/dashboard`

#### Scenario: 登录失败提示

- **WHEN** 登录 API 返回 401
- **THEN** 前端 MUST 展示「账号或密码错误」
- **AND** MUST NOT 清空用户名输入

#### Scenario: 账号被禁用

- **WHEN** 登录 API 返回 403 且错误码为 `AUTH_USER_DISABLED`
- **THEN** 前端 MUST 展示「账号已停用，请联系管理员」

#### Scenario: 网络异常

- **WHEN** 登录 API 请求因网络错误失败
- **THEN** 前端 MUST 展示「网络异常，请稍后重试」

### Requirement: 登录态保持

前端 MUST 支持登录态持久化，刷新页面后可恢复已登录状态。

#### Scenario: 刷新后恢复登录

- **WHEN** 用户已登录且 token 仍有效，刷新页面
- **THEN** 前端 MUST 从本地存储读取 token 并调用 `/auth/me` 恢复用户信息
- **AND** 用户 MUST 保持已登录状态

#### Scenario: remember_me 持久化

- **WHEN** 用户勾选「记住我」并登录成功
- **THEN** 前端 MUST 将 token 持久化至 localStorage

#### Scenario: 未勾选 remember_me

- **WHEN** 用户未勾选「记住我」并登录成功
- **THEN** 前端 MUST 将 token 存储至 sessionStorage

### Requirement: 管理端路由守卫

Web 客户端 MUST 对管理端路由实施鉴权，除 `/admin/login` 外均为受保护路由。

#### Scenario: 未登录访问受保护路由

- **WHEN** 未登录用户访问 `/admin/*`（非 login）
- **THEN** 前端 MUST 跳转至 `/admin/login`

#### Scenario: 已登录访问登录页

- **WHEN** 已登录用户访问 `/admin/login`
- **THEN** 前端 MUST 自动跳转至 `/admin/dashboard`

#### Scenario: Token 过期

- **WHEN** 已登录用户访问受保护路由但 token 已过期（API 返回 401）
- **THEN** 前端 MUST 清除本地登录态
- **AND** MUST 跳转至 `/admin/login` 并提示「登录已过期，请重新登录」

### Requirement: 角色权限前端拦截

前端 MUST 根据用户角色限制管理端访问。

#### Scenario: 店主角色拒绝管理端

- **WHEN** 角色为 `store_owner` 的用户登录成功
- **THEN** 前端 MUST NOT 进入管理端受保护页面
- **AND** MUST 展示无权限提示或跳转无权限页

#### Scenario: 非管理员访问管理员页面

- **WHEN** 角色为 `employee` 的用户访问管理员专属页面
- **THEN** 前端 MUST 展示无权限提示

### Requirement: 退出登录

Web 客户端 MUST 提供退出登录能力。

#### Scenario: 退出操作

- **WHEN** 用户在管理端点击退出登录
- **THEN** 前端 MUST 调用 logout API（可选）、清除本地 token 与用户态
- **AND** MUST 跳转至 `/admin/login`

#### Scenario: 退出后再访问

- **WHEN** 用户退出后访问管理端受保护页面
- **THEN** 前端 MUST 跳转至 `/admin/login`

### Requirement: 占位功能

登录页中的非本期功能 MUST 以占位方式呈现，不阻塞主登录流程。

#### Scenario: 忘记密码占位

- **WHEN** 用户点击「忘记密码？」
- **THEN** 系统 MUST 展示「功能建设中」提示
- **AND** MUST NOT 跳转至完整找回密码流程

#### Scenario: 企业微信占位

- **WHEN** 用户点击「企业微信」
- **THEN** 系统 MUST 展示「功能建设中」提示

### Requirement: Auth Feature 模块封装

前端登录逻辑 MUST 封装在独立 `src/web/src/features/auth/` 模块中，不散落在页面组件内。

#### Scenario: 模块边界

- **WHEN** 实现登录相关功能
- **THEN** API 调用、状态管理、token 工具 MUST 位于 `features/auth/` 目录
- **AND** 页面组件 MUST 通过 hooks 或 store 消费 auth 能力

### Requirement: Orval 客户端集成

前端 MUST 通过 Orval 生成的 API 客户端调用认证接口，不得手写 `/api/generated/` 目录代码。

#### Scenario: API 客户端来源

- **WHEN** 前端调用 auth 相关 API
- **THEN** MUST 使用 Orval 生成的类型化客户端
- **AND** auth API 变更后 MUST 运行 `./scripts/generate-openapi-client.sh`

### Requirement: 可访问性

登录页 MUST 满足基础可访问性要求。

#### Scenario: 键盘导航

- **WHEN** 用户使用 Tab 键导航
- **THEN** Tab 顺序 MUST 为：用户名 → 密码 → 记住我 → 忘记密码 → 登录 → 企业微信

#### Scenario: 表单标签

- **WHEN** 屏幕阅读器访问表单
- **THEN** 输入框 MUST 具备可访问 label（可视觉隐藏）
- **AND** 错误提示 MUST 通过 `aria-describedby` 关联对应字段

### Requirement: 管理端登录页 Design System 实现

Web 客户端管理端登录页（`/admin/login`）MUST 通过 port CSS 引用 Design Token（`--color-*`），MUST 对齐 `user-login.html` 布局与视觉；登录页 presentation MUST NOT 依赖 shadcn 表单 primitive 的默认皮相。

#### Scenario: Token 引用

- **WHEN** 开发者查看 `login-page.css`
- **THEN** 颜色 MUST 通过 `var(--color-*)` 引用 `globals.css`
- **AND** TSX 组件 MUST NOT 包含 `#18160F`、`#C8A055` 等裸 Hex

#### Scenario: 桌面分屏与右栏背景

- **WHEN** 视口宽度 >= 1024px
- **THEN** 页面 MUST 展示左右 50% 分屏
- **AND** 右栏背景 MUST 为 `--color-page` 加 radial glow（对齐 HTML `.form-panel`）

#### Scenario: 精确间距

- **WHEN** 视口为桌面端
- **THEN** 表单 max-width MUST 为 420px
- **AND** 输入框高度 MUST 为 64px（<640px 为 52px）
- **AND** 表单项间距 MUST 为 28px；标题到表单 MUST 为 48px；主按钮到第三方区域 MUST 为 56px

#### Scenario: 登录按钮 loading

- **WHEN** 登录请求进行中
- **THEN** 按钮 MUST 展示 loading 文案或状态且 `disabled`
- **AND** MUST 设置 `aria-busy="true"`

#### Scenario: 占位功能行为不变

- **WHEN** 用户点击「忘记密码？」或「企业微信」
- **THEN** MAY noop 或展示弱提示
- **AND** MUST NOT 发起 OAuth 或跳转外部流程

### Requirement: 登录页 refactor 不改变认证逻辑

登录页 UI 重构 MUST NOT 修改 auth store、login API 调用、token 持久化策略、路由守卫与角色分流逻辑。

#### Scenario: Auth 逻辑冻结

- **WHEN** refactor-login-ui 实现完成
- **THEN** `src/web/src/features/auth/store/`、`hooks/useAuth.ts`、`api/auth-api.ts` MUST 无行为变更
- **AND** 现有登录成功/失败/记住我行为 MUST 与 refactor 前一致

