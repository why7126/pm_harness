## 1. 准备与基线

- [x] 1.1 对照 `prototype/web/user-login.md` 与当前 `/admin/login` 列出 UI 差距清单
- [x] 1.2 确认 auth store/hooks/API 文件为只读边界，refactor 不修改

## 2. AuthBrandPanel

- [x] 2.1 替换所有裸 Hex 为 Design Token class
- [x] 2.2 对齐 Logo 字距（`tracking-brand`）、宣传语与 Feature 列表间距
- [x] 2.3 优化背景 overlay gradient（token 化）

## 3. LoginPage 容器

- [x] 3.1 重构 `LoginPage.tsx` 布局 shell（grid、bg-deep 右栏、语言切换、版权）
- [x] 3.2 替换 notice 提示框样式为 token + `rounded-industrial`
- [x] 3.3 对齐标题区字号与品牌金强调（`text-brand-gold`）

## 4. LoginForm

- [x] 4.1 用户名改用 `IconInput`（User icon）
- [x] 4.2 记住我改用 shadcn `Checkbox` + `Label`
- [x] 4.3 忘记密码改用 `Button variant="link"` 或 token 化 text link
- [x] 4.4 登录按钮改用 shadcn `Button`，保留 loading / aria-busy
- [x] 4.5 第三方区改用 `DividerText` + 企业微信 outline 入口
- [x] 4.6 错误提示改用 `text-error`

## 5. PasswordInput

- [x] 5.1 重构为基于 `IconInput` + Eye/EyeOff 显隐按钮
- [x] 5.2 对齐 focus/hover/error 态与 Enter 提交行为

## 6. 响应式与可访问性

- [x] 6.1 验证 lg 分屏 / 移动单栏断点
- [x] 6.2 确认 sr-only label、aria-invalid、aria-describedby 保留
- [x] 6.3 验证 Tab 顺序与 Enter 提交

## 7. 测试与构建

- [x] 7.1 更新 `LoginForm.test.tsx`、`PasswordInput` 相关测试
- [x] 7.2 运行 `vitest run` 全部通过
- [x] 7.3 运行 `vite build` 与 `docker compose build web`

## 8. 文档与 Sprint

- [x] 8.1 更新 `openspec/changes/refactor-login-ui/trace.md`
- [x] 8.2 确认 Sprint 01 acceptance-report 登录页 UI 验收项可勾选
