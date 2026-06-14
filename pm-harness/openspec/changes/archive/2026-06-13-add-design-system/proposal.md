## Why

`add-user-login` 已交付认证功能，但 Web 前端仍使用硬编码 Tailwind 色值、缺少 shadcn/ui 与 Design Token 层，导致登录页与 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.md`、`rules/ui-design.md` 的「工业石材 · 暗色旗舰风」差距较大。AGENTS.md 强制要求 Tailwind + shadcn/ui，且后续 tile-catalog、tile-admin 等页面需要统一视觉语言。必须先建立可复用的 Design System，再作为各业务页面的消费基础。

## What Changes

- 建立 Web 端 Design Token 层（CSS variables + Tailwind `@theme`），映射 `rules/ui-design.md` 色彩、字体、间距、圆角、分割线规范。
- 初始化 shadcn/ui（Tailwind v4 + Vite 兼容配置），安装并主题化基础组件：Button、Input、Checkbox、Label、Separator。
- 新增共享 UI 工具：`cn()`（clsx + tailwind-merge）、组件 variant 约定（工业风 2px 圆角、金色主 CTA、透明输入框）。
- 新增复合表单组件（可选最小集）：带图标 Input 封装、DividerText，供后续登录页重构与其他表单复用。
- 新增 Design System 文档索引：在 `src/web/README.md` 说明 token 与组件使用方式；`rules/ui-design.md` 补充 token 文件路径引用。
- 新增可选 Demo/预览页或 Story 入口（`/design-system` 路由，仅开发环境），用于验收 token 与组件状态。

## Capabilities

### New Capabilities

- `design-system`：Design Token、shadcn/ui 基础组件、工业风主题 override、共享 UI 工具与使用规范。

### Modified Capabilities

（`openspec/specs/` 当前为空；本 Change 不修改既有正式 spec。登录页 UI 重构由后续 `refactor-login-ui` Change 消费本能力。）

## Impact

| 影响面 | 说明 |
|---|---|
| 前端依赖 | 新增 shadcn/ui、@radix-ui 相关包、class-variance-authority（已有）、tailwind-merge（已有） |
| 样式 | `src/web/src/styles/globals.css` 扩展 token；可能新增 `components.json` |
| 目录 | `src/web/src/components/ui/`、`src/web/src/shared/lib/cn.ts` |
| 构建 | 需验证 `npm run build` 与 Docker Web 镜像构建 |
| 文档 | `rules/ui-design.md`、`src/web/README.md` |
| 业务页面 | 本期**不修改**登录页布局；仅提供可被 `refactor-login-ui` 消费的基础能力 |
| API / 后端 | 无影响 |
