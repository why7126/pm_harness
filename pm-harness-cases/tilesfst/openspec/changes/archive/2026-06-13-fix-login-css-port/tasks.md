## 1. CSS Port 基础

- [x] 1.1 创建 `src/web/src/features/auth/styles/login-page.css`，从 `user-login.html` `<style>` port 全部规则
- [x] 1.2 将 HTML CSS 变量映射为 `var(--color-*)` token（见 design.md D1 映射表）
- [x] 1.3 在 `LoginPage.tsx`（或 auth feature 入口）import `login-page.css`
- [x] 1.4 新增 scoped tile 渐变 variables（若 token 组合仍不足），仅允许存在于 CSS 文件

## 2. 页面骨架重构

- [x] 2.1 重构 `LoginPage.tsx`：`<main class="login-shell">` + 左右两栏 grid
- [x] 2.2 重构 `AuthBrandPanel.tsx`：对齐 HTML 结构（brand-top / brand-content / brand-bottom / material-board）
- [x] 2.3 重构 `LoginFormPanel.tsx`：`.form-panel` + 右上 `.language` + `.login-card` 容器
- [x] 2.4 重构 `LoginHeader.tsx`：`.eyebrow` + `h1` + `.sub` 文案与 HTML 一致

## 3. 表单与交互（auth 逻辑冻结）

- [x] 3.1 重构 `LoginForm.tsx`：原生 `<input>` / `<button>` + port CSS class（`.field`、`.primary`、`.form-options`）
- [x] 3.2 移除登录页对 shadcn `Input`/`Button`/`Checkbox` 与 `PasswordInput` 的依赖
- [x] 3.3 实现 HTML 等价 checkbox markup（18px、金色选中态）或 styled native checkbox
- [x] 3.4 确认 auth submit / validation / error 行为与 refactor 前一致（不改 store/hooks/API）
- [x] 3.5 移除 notice 横幅；删除或停止引用 `LoginCopyright.tsx`

## 4. 第三方入口与页脚

- [x] 4.1 重构 `LanguageSwitcher.tsx`：`.language` 边框按钮样式
- [x] 4.2 重构 `ThirdPartyLoginSection.tsx`：`.third-party` + `.divider` 文案「或使用企业身份登录」
- [x] 4.3 重构 `WeComLoginButton.tsx`：`.wecom` 全宽 54px 横排按钮 + `/icons/wecom.svg`
- [x] 4.4 新增/保留 `LoginSecurityNotice.tsx`：`.security` 安全说明文案

## 5. 清理与规范

- [x] 5.1 删除或废弃 `login-styles.ts`（Tailwind 登录常量）
- [x] 5.2 更新 `rules/ui-design.md` §9：补充 CSS Port 策略与 HTML 优先级说明
- [x] 5.3 更新 auth 组件 vitest（文案、结构、class 断言；移除 PasswordInput/版权相关断言）

## 6. 构建与部署验证

- [x] 6.1 运行 `cd src/web && npx vitest run src/features/auth`
- [x] 6.2 运行 `cd src/web && npm run build` 确认 CSS 打包成功
- [x] 6.3 运行 `./scripts/docker-up.sh` rebuild web，访问 `http://localhost:3000/admin/login`

## 7. PNG 视觉验收 Gate

- [x] 7.1 1280×1024 视口并排对比 `user-login.png` 与 `/admin/login`，填写 diff checklist（≥15 项）
- [x] 7.2 记录验收结果至 `openspec/changes/fix-login-css-port/trace.md`
- [x] 7.3 更新 `iterations/sprint-00/acceptance-report.md`（或当前 sprint）视觉项
