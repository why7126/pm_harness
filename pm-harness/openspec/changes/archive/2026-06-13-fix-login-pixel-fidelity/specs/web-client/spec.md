## MODIFIED Requirements

### Requirement: 管理端登录页

Web 客户端 MUST 提供管理端登录页，路由为 `/admin/login`，视觉风格 MUST 高保真对齐 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.png` 暗色工业风设计。桌面端（1280px 视口）并排对比 PNG 时，布局、品牌字体、背景材质、控件形态、色彩与间距 MUST 被团队判定为一致或仅有可接受像素级偏差。页面 MUST 使用 Design Token semantic class，MUST NOT 依赖 JSX 裸 Hex。

#### Scenario: 登录页布局

- **WHEN** 用户在桌面端（>= 1024px）访问 `/admin/login`
- **THEN** 页面 MUST 展示左右分屏布局：左侧品牌视觉区、右侧登录表单区
- **AND** 页面 MUST 使用 Design Token semantic class（如 `bg-page`、`text-brand-gold`），MUST NOT 依赖 JSX 裸 Hex

#### Scenario: 移动端布局

- **WHEN** 用户在移动端（< 1024px）访问 `/admin/login`
- **THEN** 页面 MUST 隐藏左侧品牌区，登录表单全屏居中展示

#### Scenario: 登录表单元素

- **WHEN** 用户查看登录页
- **THEN** 页面 MUST 包含：用户名输入框、密码输入框（含显隐切换）、记住我复选框、忘记密码链接、登录按钮、企业微信入口（含品牌图标）、语言切换（含下拉箭头占位）、页脚版权

#### Scenario: 左侧品牌背景

- **WHEN** 用户在桌面端查看登录页左栏
- **THEN** MUST 展示 `/images/login-material-showcase.jpg` 作为背景
- **AND** MUST 叠加 dark gradient overlay，品牌 Logo、宣传语、能力卖点可见

#### Scenario: 品牌 Logo 字体

- **WHEN** 用户查看登录页左栏 STONEX Logo
- **THEN** Logo MUST 使用衬线/高端品牌字体（非系统 sans-serif 默认栈）
- **AND** MUST 保持 `tracking-brand` 与 `text-brand-gold` 品牌强调

#### Scenario: 登录页组件结构

- **WHEN** 开发者查看登录页源码
- **THEN** presentation 层 MUST 包含与 `user-login.md` §2 等价的组件：`LoginFormPanel`、`LoginHeader`、`ThirdPartyLoginSection`
- **AND** auth 业务逻辑 MUST 保留在 `LoginForm` / hooks / store，不与 presentation 耦合

## ADDED Requirements

### Requirement: 登录页控件原型形态

登录页表单控件 MUST 对齐 `user-login.md` §4.5 与 PNG 视觉，MUST NOT 沿用 shadcn 默认态若与原型冲突。

#### Scenario: 输入框 focus 态

- **WHEN** 用户 focus 用户名或密码输入框
- **THEN** 边框 MUST 变为金色 focus border（`border-border-focus`）
- **AND** MUST NOT 展示大偏移 focus ring（ring-offset）破坏原型细边框感

#### Scenario: 密码显隐按钮

- **WHEN** 用户查看密码输入框
- **THEN** 右侧显隐控制 MUST 为轻量 icon 按钮（透明底、muted 图标）
- **AND** MUST NOT 使用明显 ghost 方块按钮形态

#### Scenario: 占位交互不破坏布局

- **WHEN** 用户点击语言切换、忘记密码或企业微信占位入口
- **THEN** 系统 MAY 展示 noop 或短暂弱提示
- **AND** MUST NOT 在表单区域上方插入 notice 横幅块推挤布局

### Requirement: 企业微信图标视觉

企业微信登录入口 MUST 使用与原型一致的官方绿色风格图标。

#### Scenario: 企微图标颜色与形态

- **WHEN** 用户查看企业微信登录入口
- **THEN** MUST 使用绿色系企微品牌图标（非蓝色 messenger bubble）
- **AND** 图标 MUST 置于圆形 `border-border-strong` 容器内，下方展示「企业微信」文案

### Requirement: 登录页 PNG 视觉验收 Gate

登录页视觉对齐 MUST 通过 PNG golden reference 验收 gate，方可标记 REQ-0001 / Sprint 001 视觉项完成。

#### Scenario: 桌面 PNG 并排验收

- **WHEN** 团队在 1280px 视口并排对比 `/admin/login` 与 `user-login.png`
- **THEN** diff checklist（Logo 字体、背景、副标题、输入框、按钮、企微、语言切换、版权、间距）MUST 全部 pass
- **AND** 结果 MUST 记录在 `openspec/changes/fix-login-pixel-fidelity/trace.md` 与 `iterations/sprint-001/acceptance-report.md`

#### Scenario: 构建与部署验证

- **WHEN** 执行 `vite build` 与 `docker compose build web`
- **THEN** 构建 MUST 成功且登录页静态资源（JPG、企微 SVG、字体）可访问

### Requirement: UI 设计规范登录页专章

项目 MUST 在 `rules/ui-design.md` 提供登录页设计专章，与 `user-login.md` 对齐。

#### Scenario: 登录页规范存在

- **WHEN** 开发者查阅 `rules/ui-design.md`
- **THEN** MUST 找到登录页专章，涵盖色彩、字体、间距、组件态引用
- **AND** MUST 指向 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.md` 作为详细 spec
