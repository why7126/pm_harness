## 1. 基线与 diff 清单

- [x] 1.1 在 1280px 视口并排打开 `/admin/login` 与 `user-login.png`，建立 ≥12 项 diff checklist
- [x] 1.2 将 checklist 写入 `openspec/changes/fix-login-pixel-fidelity/trace.md`
- [x] 1.3 确认 auth 逻辑文件只读边界（store/hooks/api 不改动）

## 2. 品牌字体

- [x] 2.1 引入 STONEX Logo 衬线字体（woff2 自托管或 npm，如 Cormorant Garamond）
- [x] 2.2 在 `globals.css` 增加 `--font-brand` token 与 utility class
- [x] 2.3 更新 `AuthBrandPanel` Logo 与右栏 STONEX 强调使用品牌字体

## 3. 静态资源与图标

- [x] 3.1 替换 `src/web/public/icons/wecom.svg` 为官方绿色风格
- [x] 3.2 验证 JPG 背景 `/images/login-material-showcase.jpg` 质量可接受（必要时重新 export）
- [x] 3.3 更新 `data/samples/images/README.md`（若资源变更）

## 4. 组件拆分与布局

- [x] 4.1 创建 `LoginFormPanel.tsx`（右栏容器）
- [x] 4.2 创建 `LoginHeader.tsx`（欢迎登录 + 副标题）
- [x] 4.3 创建 `ThirdPartyLoginSection.tsx`（DividerText + WeComLoginButton）
- [x] 4.4 重构 `LoginPage.tsx` 使用新组件树，移除 notice 横幅
- [x] 4.5 精修右栏副标题金色范围（对齐 PNG 并排确认结果）

## 5. 控件形态 override

- [x] 5.1 登录页 Input focus：border-only，无 ring-offset
- [x] 5.2 PasswordInput eye 按钮改为轻量 icon 控制
- [x] 5.3 登录主按钮、Checkbox 态对齐 `user-login.md` §4.5
- [x] 5.4 占位交互（语言/企微/忘记密码）改为 noop 或 inline 弱提示，不推挤布局

## 6. 规范文档

- [x] 6.1 在 `rules/ui-design.md` 新增登录页专章
- [x] 6.2 更新 `src/web/README.md` 登录页视觉说明（若适用）

## 7. 测试、构建与 PNG 验收

- [x] 7.1 更新/补充登录页组件测试（字体 class、WeCom、无 notice 横幅）
- [x] 7.2 `vitest run` 全部通过
- [x] 7.3 `vite build` + `docker compose build web` 通过
- [x] 7.4 PNG 并排验收：diff checklist 全部 pass，记录于 trace.md
- [x] 7.5 更新 `iterations/sprint-01/acceptance-report.md` 视觉项（通过后勾选）
- [x] 7.6 更新 `issues/requirements/REQ-0001-user-login/trace.md`
