## Context

- **当前状态**：登录页功能完整（校验、提交、loading、记住我、占位入口），但样式硬编码 Hex；`PasswordInput` 自定义实现；checkbox 为原生 `<input type="checkbox">`；企业微信为文字占位「企」。
- **Design System**：`add-design-system` 已归档，正式 spec 位于 `openspec/specs/design-system/spec.md`；组件位于 `src/web/src/components/ui/` 与 `src/web/src/shared/ui/`。
- **原型来源**：`issues/requirements/REQ-0001-user-login/prototype/web/user-login.md`、`user-login.png`。
- **约束**：遵循 `rules/ui-design.md`；不修改 `src/features/auth/store`、`auth-api`、后端接口。

## Goals / Non-Goals

**Goals:**

- 登录页全部 UI 使用 Design Token（`bg-page`、`text-brand-gold`、`border-strong` 等），零裸 Hex。
- 表单控件迁移至 `IconInput`、`PasswordInput`（基于 IconInput/Input）、`Button`、`Checkbox`、`DividerText`。
- 桌面左右分屏、移动单栏布局与原型一致；间距/字号/圆角符合原型 §4。
- 保留全部现有交互：校验、Enter 提交、密码显隐、loading、占位提示、登录成功跳转。
- 测试与构建通过。

**Non-Goals:**

- 修改 auth API、JWT、路由守卫逻辑。
- 实现忘记密码、企业微信 OAuth 真实流程。
- 替换背景图为真实 JPG（可继续使用 SVG 占位，overlay 与布局对齐即可）。
- 语言切换 i18n 实现（保持「简体中文」占位）。
- 小程序 / 店主端登录页。

## Decisions

### D1：仅改 Presentation 层，Logic 层冻结

- **决策**：重构仅限 TSX className 与组件组合；`useAuth`、`login()`、`auth-store` 不改动。
- **理由**：降低回归风险；UI 与 auth 解耦符合 Path C 规划。
- **备选**：合并 auth hook 与 UI — 超出 scope，增加测试面。

### D2：PasswordInput 基于 IconInput + 右侧显隐按钮

- **决策**：`PasswordInput` 重构为组合 `IconInput`（Lock icon）+ lucide Eye/EyeOff `Button variant="ghost" size="icon"`。
- **理由**：复用 DS 复合组件；对齐原型 suffix icon 交互。

### D3：组件文件结构 — 保持 feature 目录，不迁移至 pages 级重组

- **决策**：继续放在 `src/web/src/features/auth/components/`，仅替换内部实现。
- **理由**：`add-user-login` 已建立结构；避免大规模文件移动。

### D4：AuthBrandPanel 视觉增强

- **决策**：使用 token class 替换 Hex；Feature 圆形图标边框用 `border-brand-gold/30`；gradient overlay 用 token 或 `from-page/95` 等等价 semantic 表达。
- **背景图**：保留 `/images/login-material-showcase.svg`，调整 opacity 与 gradient 对齐原型。

### D5：企业微信入口

- **决策**：使用 outline/ghost 圆形按钮 + 文字标签；点击仍调用 `onPlaceholder('功能建设中')`。
- **理由**：原型要求入口存在；OAuth 属 Non-Goal。

### D6：响应式断点

- **决策**：`lg:grid-cols-2` 显示左栏；`< lg` 隐藏 `AuthBrandPanel`；表单 `max-w-[520px]`；`< sm` 输入框可降为 `h-[52px]`（可选，对齐原型 §3.7）。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| Refactor 破坏现有测试 selector | 更新测试使用 role/label，少依赖 class |
| IconInput 与 PasswordInput 右侧 icon 布局冲突 | PasswordInput 独立 wrapper，右侧 absolute 定位 |
| 视觉主观验收 | 对照 prototype 截图与 `/design-system` token 样本 |
| 与 add-user-login web-client spec 归档顺序 | refactor-login-ui spec 作为 web-client delta ADDED/MODIFIED |

## Migration Plan

1. 逐组件替换（BrandPanel → LoginPage shell → LoginForm → PasswordInput）。
2. 每步运行 vitest；完成后 `vite build` + Docker web build。
3. 手动对照 `/admin/login` 与原型。
4. 回滚：git revert UI 文件即可，auth 逻辑未动。

## Open Questions

| 问题 | 本期决策 |
|---|---|
| 移动端输入框高度 52px vs 64px | 桌面 64px；`< sm` 可选 52px |
| 背景图换 JPG | 否，SVG 占位 + overlay 对齐 |
