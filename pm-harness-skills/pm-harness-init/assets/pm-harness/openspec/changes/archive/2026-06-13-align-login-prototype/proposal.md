## Why

Sprint 001 已完成 `add-user-login`、`add-design-system`、`refactor-login-ui` 三阶段交付，但 `/admin/login` 与 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.png` 仍存在明显视觉差距：左侧背景为抽象 SVG 占位而非展厅实拍、企业微信为「企」字占位、语言切换缺少下拉箭头、间距与原型 §4.4 未精修。`refactor-login-ui` 解决的是 Design Token + shadcn 组件化，**不是**像素级原型还原。REQ-0001 验收项「页面视觉与原型一致」尚未真正通过，需在 Sprint 001 内补齐高保真视觉层。

## What Changes

- 引入登录页左侧真实背景图（`login-material-showcase.jpg`），替换 SVG 占位，overlay gradient 对齐原型。
- 新增 `LanguageSwitcher` 组件（简体中文 + Chevron 下拉占位，无 i18n 逻辑）。
- 新增企业微信 SVG 图标（`/icons/wecom.svg`），替换「企」字圆形占位。
- 按 `user-login.md` §3–§4 精修 spacing、字号、右栏布局（标题区 48px、表单项 28px、第三方区 56px 等）。
- 拆分/整理登录页 presentation 组件（`LoginFormPanel`、`LoginHeader`、`Copyright` 等，可选最小集）。
- 视觉验收：桌面端与 `user-login.png` 并排对比通过（结构、背景、控件、间距）。
- **不修改** auth store、hooks、API、路由守卫与表单业务逻辑。

## Capabilities

### New Capabilities

（无新增独立 capability。）

### Modified Capabilities

- `web-client`：管理端登录页视觉 MUST 高保真对齐 `user-login.png`；补充静态资源与 UI 组件规范。

## Impact

| 影响面 | 说明 |
|---|---|
| 静态资源 | `src/web/public/images/login-material-showcase.jpg`、`src/web/public/icons/wecom.svg` |
| 前端 UI | `AuthBrandPanel`、`LoginPage`、`LoginForm` 及新增 presentation 组件 |
| 样例数据 | 可选 `data/samples/images/` 存放源图（遵循 data-management 规范） |
| Auth 逻辑 | **无影响** |
| Docker | Web 镜像需包含新静态资源 |
| 文档 | Sprint 001 迭代文档、REQ-0001 acceptance |
