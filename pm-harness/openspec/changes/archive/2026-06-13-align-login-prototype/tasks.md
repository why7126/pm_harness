## 1. 静态资源

- [x] 1.1 准备 `login-material-showcase.jpg`（暗色展厅/石材立板，对齐原型左栏）
- [x] 1.2 放置于 `src/web/public/images/login-material-showcase.jpg`
- [x] 1.3 创建 `src/web/public/icons/wecom.svg` 企业微信图标
- [x] 1.4 在 `data/samples/images/README` 或 `data/README.md` 说明样例图来源（若适用）

## 2. AuthBrandPanel 高保真

- [x] 2.1 背景改用 JPG + `bg-cover bg-center opacity-80`
- [x] 2.2 gradient overlay 对齐 `user-login.md` §3.3
- [x] 2.3 验证左栏 Logo、宣传语、Feature 列表与原型 spacing

## 3. 登录页右栏组件

- [x] 3.1 创建 `LanguageSwitcher.tsx`（简体中文 + ChevronDown）
- [x] 3.2 创建 `WeComLoginButton.tsx` 或等效组件（SVG 图标 + 文案）
- [x] 3.3 更新 `LoginPage.tsx` 集成 LanguageSwitcher、Copyright 位置
- [x] 3.4 精修 spacing：标题 mb-12、表单 space-y-7、第三方区 pt-14

## 4. LoginForm 调整

- [x] 4.1 集成 WeComLoginButton，移除「企」字占位
- [x] 4.2 确认 IconInput/PasswordInput/Button 视觉与原型 §4.5 状态一致
- [x] 4.3 auth 逻辑文件零改动（store/hooks/api 只读验证）

## 5. 响应式

- [x] 5.1 验证 lg 分屏 / 移动单栏
- [x] 5.2 可选 `< sm` 输入框 h-[52px]（对齐 §3.7）

## 6. 测试与构建

- [x] 6.1 更新/补充 LoginForm、LanguageSwitcher 相关测试
- [x] 6.2 `vitest run` 全部通过
- [x] 6.3 `vite build` + `docker compose build web` 通过

## 7. 视觉验收与文档

- [x] 7.1 桌面端与 `user-login.png` 并排对比，记录于 trace.md
- [x] 7.2 更新 `iterations/sprint-001/acceptance-report.md` 视觉项（通过后勾选）
- [x] 7.3 更新 `openspec/changes/align-login-prototype/trace.md`
- [x] 7.4 更新 `issues/requirements/REQ-0001-user-login/trace.md`
