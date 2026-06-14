## ADDED Requirements

### Requirement: 管理端登录页

Web 客户端 MUST 提供管理端登录页，路由为 `/admin/login`，视觉风格 MUST 对齐 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.png` 暗色工业风设计。

#### Scenario: 登录页布局

- **WHEN** 用户在桌面端（>= 1024px）访问 `/admin/login`
- **THEN** 页面 MUST 展示左右分屏布局：左侧品牌视觉区、右侧登录表单区
- **AND** 页面底色 MUST 为 `#18160F`，品牌强调色 MUST 为 `#C8A055`

#### Scenario: 移动端布局

- **WHEN** 用户在移动端（< 1024px）访问 `/admin/login`
- **THEN** 页面 MUST 隐藏左侧品牌区，登录表单全屏居中展示

#### Scenario: 登录表单元素

- **WHEN** 用户查看登录页
- **THEN** 页面 MUST 包含：用户名输入框、密码输入框（含显隐切换）、记住我复选框、忘记密码链接、登录按钮、企业微信入口、语言切换占位、页脚版权

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

### Requirement: 密码显隐切换

密码输入框 MUST 支持明文/密文切换。

#### Scenario: 切换密码可见性

- **WHEN** 用户点击密码框右侧眼睛图标
- **THEN** 密码字段 MUST 在 `password` 与 `text` 类型间切换

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
