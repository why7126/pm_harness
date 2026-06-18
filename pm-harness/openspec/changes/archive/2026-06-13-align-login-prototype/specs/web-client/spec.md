## MODIFIED Requirements

### Requirement: 管理端登录页

Web 客户端 MUST 提供管理端登录页，路由为 `/admin/login`，视觉风格 MUST 高保真对齐 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.png` 暗色工业风设计；桌面端并排对比时，布局、背景材质摄影、色彩、间距与控件样式 MUST 与原型一致。

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
- **THEN** MUST 展示 `/images/login-material-showcase.jpg` 作为背景（非 SVG 几何占位）
- **AND** MUST 叠加 dark gradient overlay，品牌 Logo、宣传语、能力卖点可见

## ADDED Requirements

### Requirement: 登录页原型静态资源

Web 客户端 MUST 在 `src/web/public/` 提供登录页原型所需静态资源，并随生产构建与 Docker Web 镜像部署。

#### Scenario: 背景图存在

- **WHEN** 构建 Web 生产包
- **THEN** `public/images/login-material-showcase.jpg` MUST 存在且可在 `/images/login-material-showcase.jpg` 访问

#### Scenario: 企业微信图标存在

- **WHEN** 渲染企业微信登录入口
- **THEN** MUST 使用 `public/icons/wecom.svg`（或等效 SVG），MUST NOT 使用纯文字「企」作为最终视觉

### Requirement: 登录页语言切换占位

Web 客户端 MUST 在登录页右栏右上角展示语言切换占位，视觉对齐原型。

#### Scenario: 语言切换展示

- **WHEN** 用户查看登录页右栏
- **THEN** MUST 展示「简体中文」文案与下拉箭头图标
- **AND** 点击 MAY 展示「功能建设中」或 noop；MUST NOT 要求完整 i18n 实现

### Requirement: 登录页原型视觉验收

登录页高保真对齐 MUST 通过可执行的视觉验收，方可标记 REQ-0001 / Sprint 001 视觉项完成。

#### Scenario: 桌面视觉对比

- **WHEN** 团队在桌面端对比 `/admin/login` 与 `user-login.png`
- **THEN** 结构（左右分屏）、背景图、表单控件、间距、企微入口、语言切换 MUST 判定为一致或仅有可接受的像素级偏差
- **AND** 验收 MUST 记录在 `iterations/sprint-001/acceptance-report.md`
