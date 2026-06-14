## ADDED Requirements

### Requirement: 管理端登录页 Design System 实现

Web 客户端管理端登录页（`/admin/login`）MUST 使用 `openspec/specs/design-system/spec.md` 定义的 Design Token 与 shadcn/ui 基础组件实现，MUST NOT 在登录页相关组件中使用硬编码 Hex 色值，MUST 对齐 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.md` 布局与视觉规范。

#### Scenario: 登录页使用 Design Token

- **WHEN** 开发者查看登录页相关 TSX 组件（LoginPage、AuthBrandPanel、LoginForm、PasswordInput）
- **THEN** 样式 MUST 使用 semantic token class（如 `bg-page`、`bg-deep`、`text-brand-gold`、`border-strong`）
- **AND** MUST NOT 包含 `#18160F`、`#C8A055`、`#EDE8DF` 等裸 Hex 字符串

#### Scenario: 表单控件使用 shadcn 组件

- **WHEN** 用户与登录表单交互
- **THEN** 用户名输入 MUST 基于 `IconInput` 或 shadcn `Input` 构建
- **AND** 登录按钮 MUST 使用 shadcn `Button` `variant="default"`
- **AND** 记住我 MUST 使用 shadcn `Checkbox` 与 `Label`
- **AND** 第三方分割文案 MUST 使用 `DividerText`

#### Scenario: 桌面分屏布局

- **WHEN** 视口宽度 >= 1024px
- **THEN** 页面 MUST 展示左右 50% 分屏：左侧品牌视觉区、右侧登录表单区
- **AND** 左栏 MUST 展示品牌 Logo、宣传语、能力卖点列表与材质背景
- **AND** 右栏背景 MUST 使用 `bg-deep`

#### Scenario: 移动端单栏布局

- **WHEN** 视口宽度 < 1024px
- **THEN** 左侧品牌区 MUST 隐藏
- **AND** 登录表单 MUST 全屏居中，最大宽度 520px

#### Scenario: 输入框交互状态

- **WHEN** 用户 hover、focus 或触发校验错误
- **THEN** 输入框边框 MUST 分别使用 `border-hover`、`border-focus`、`border-error` 语义
- **AND** 错误文案 MUST 使用 `text-error`

#### Scenario: 登录按钮 loading

- **WHEN** 登录请求进行中
- **THEN** 按钮 MUST 展示 loading 文案或状态且 `disabled`
- **AND** MUST 设置 `aria-busy="true"`

#### Scenario: 占位功能行为不变

- **WHEN** 用户点击「忘记密码？」或「企业微信」
- **THEN** MUST 展示「功能建设中」提示
- **AND** MUST NOT 发起 OAuth 或跳转外部流程

### Requirement: 登录页 refactor 不改变认证逻辑

登录页 UI 重构 MUST NOT 修改 auth store、login API 调用、token 持久化策略、路由守卫与角色分流逻辑。

#### Scenario: Auth 逻辑冻结

- **WHEN** refactor-login-ui 实现完成
- **THEN** `src/web/src/features/auth/store/`、`hooks/useAuth.ts`、`api/auth-api.ts` MUST 无行为变更
- **AND** 现有登录成功/失败/记住我行为 MUST 与 refactor 前一致
