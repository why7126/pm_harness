## Why

`add-user-login` 已交付认证功能，`add-design-system` 已建立 Design Token 与 shadcn/ui 基础组件，但 `/admin/login` 仍使用硬编码 Hex 色值、原生 checkbox 与自定义输入框，与 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.md` 及 `rules/ui-design.md` 存在明显视觉差距。Sprint 001 验收项「登录页视觉与原型一致」尚未通过，需在 **不改动 auth API 与业务逻辑** 的前提下完成 Path C Phase 2：登录页 UI 迁移至 Design System。

## What Changes

- 重构 `LoginPage`、`AuthBrandPanel`、`LoginForm`、`PasswordInput` 等组件，全面使用 Design Token semantic class 与 shadcn/ui / 复合组件（`IconInput`、`DividerText`、`Button`、`Checkbox`）。
- 移除登录页相关 JSX 中的裸 Hex 色值（如 `#18160F`、`#C8A055`）。
- 对齐原型布局、间距、字体层级、输入框/按钮/复选框交互状态（default / hover / focus / error / loading / disabled）。
- 优化左侧品牌区背景 overlay、Feature 图标样式、企业微信入口视觉（仍保持占位行为）。
- 保持现有 auth store、hooks、API 调用、路由守卫、表单校验逻辑 **不变**。
- 更新登录页相关前端测试，确保 refactor 后行为与测试通过。

## Capabilities

### New Capabilities

（无新增独立 capability；登录页 UI 属于 Web 客户端范畴。）

### Modified Capabilities

- `web-client`：管理端登录页视觉实现 MUST 消费 Design System，对齐产品原型；规范级要求从「硬编码色值实现」升级为「Design Token + shadcn 组件实现」。

## Impact

| 影响面 | 说明 |
|---|---|
| 前端 UI | `src/web/src/pages/admin/LoginPage.tsx`、`src/web/src/features/auth/components/*` |
| Design System | 消费 `src/web/src/components/ui/*`、`shared/ui/icon-input`、`divider-text` |
| Auth 逻辑 | **无影响** — store、hooks、API、路由守卫不修改 |
| 后端 / API | 无影响 |
| 测试 | 更新 LoginForm、PasswordInput 等组件测试 |
| 文档 | Sprint 001 迭代文档、REQ-0001 trace |
| Docker | 需验证 `npm run build` 与 Web 镜像构建 |
