## Why

当前 `/admin/login` 虽已按 Tailwind + shadcn 组件拼装布局参数，但与 `user-login.html` / `user-login.png` 并排对比时，左栏材质拼贴、氛围光感、表单控件皮相仍一眼可辨差异。根因是前序实现做了「结构还原 + Token 近似」，未做「CSS 视觉 port」；shadcn 默认态与 HTML 原型在边框、focus、checkbox、企微按钮形态上持续冲突。REQ-0001 视觉验收仍未通过，需采用 **路径 A：CSS Port** 将 `user-login.html` 样式几乎原样落地，以 PNG 为 golden reference 做最后一轮 fidelity 专项。

## What Changes

- 从 `issues/requirements/REQ-0001-user-login/prototype/web/user-login.html` 提取 `<style>`，落地为登录页专用 stylesheet（如 `login-page.css` 或 CSS Module），颜色引用 `globals.css` 的 `--color-*` token，**禁止**在 TSX 中硬编码 Hex。
- React 组件仅负责 DOM 结构与 auth 交互；登录页表单控件改用 **原生 `<input>` / `<button>` + port CSS class**，不再依赖 shadcn `Input`/`Checkbox`/`Button` 默认皮相（auth 逻辑仍走 `LoginForm` / hooks / store）。
- 左栏按 HTML 还原：品牌三区布局、统计卡、CSS 材质拼贴（非 JPG 全屏背景）；氛围层（网格线、radial glow）与 HTML 一致。
- 右栏按 HTML 还原：420px 表单宽、64px 输入框、56px 金色主按钮、全宽企微入口、安全说明文案；**移除** notice 横幅与旧版权 footer。
- 建立 PNG 并排 diff checklist 与验收 gate；更新 `rules/ui-design.md` §9 与 `user-login.html` 对齐说明。
- **不修改** auth store、hooks、API、路由守卫、token 持久化策略。

## Capabilities

### New Capabilities

（无新增独立 capability。）

### Modified Capabilities

- `web-client`：管理端登录页视觉实现策略改为 CSS Port；左栏材质拼贴、右栏控件形态、页脚文案、企微入口、验收 gate 等 requirement 与 `user-login.html` / PNG 对齐，并明确 **MUST NOT** 因 shadcn 默认态偏离原型。

## Impact

| 影响面 | 说明 |
|---|---|
| 前端样式 | 新增 `src/web/src/features/auth/styles/login-page.css`（或等效路径） |
| 前端组件 | `LoginPage`、`AuthBrandPanel`、`LoginFormPanel`、`LoginHeader`、`LoginForm`、`ThirdPartyLoginSection`、`WeComLoginButton`、`LanguageSwitcher` 重构为 HTML 结构 + CSS class |
| shadcn 使用 | 登录页 presentation 层停用 shadcn Input/Checkbox/Button；其他页面不受影响 |
| Auth 逻辑 | **无影响**（`store/`、`hooks/`、`api/` 冻结） |
| 规范文档 | `rules/ui-design.md` §9 补充 CSS Port 策略说明 |
| 静态资源 | 继续使用 `/icons/wecom.svg`；左栏不强制 JPG 背景 |
| 测试 | 更新 auth 组件测试断言（文案、结构、class）；补充视觉 checklist 文档 |
| Docker | Web 镜像 rebuild 后验收 `/admin/login` |
