## Context

- **现状**：`/admin/login` 由 Tailwind class + shadcn `Input`/`Checkbox`/`Button` 拼装，左栏用 token 渐变近似材质拼贴；与 `user-login.html` 并排时材质、光感、控件皮相差异明显。
- **根因**：「结构参数对齐」≠「CSS 视觉 port」；shadcn 默认边框（0.18 opacity）、focus ring、Checkbox 形态与 HTML 原型持续冲突。
- **原型来源**（优先级）：`user-login.html` > `user-login.png` > `user-login-context.md`。
- **约束**：auth store / hooks / API / 路由守卫冻结；颜色 MUST 引用 `globals.css` `--color-*`，TSX/CSS 中禁止裸 Hex；登录页允许专用 stylesheet（scoped）。
- **规范**：`rules/ui-design.md` §9、`openspec/specs/web-client/spec.md`。

## Goals / Non-Goals

**Goals:**

- 桌面端 `/admin/login` 与 `user-login.png` 并排对比，团队判定为「一致或仅有可接受像素偏差」。
- 将 `user-login.html` 的 `<style>` port 为登录专用 CSS，React 仅负责 DOM 结构与 auth 交互。
- 左栏完整还原：三区 flex 布局、统计卡、CSS 材质拼贴、网格 overlay、radial glow。
- 右栏完整还原：420px 表单、64px 输入、56px 主按钮、全宽企微、安全说明、右上语言切换。
- 建立 ≥15 项 PNG diff checklist，写入 change `trace.md` 与 sprint acceptance。

**Non-Goals:**

- 企微 OAuth、忘记密码、i18n 真实逻辑。
- 修改 auth API / store / 路由守卫。
- 自动化 Percy/Storybook 视觉回归（本期手工并排 + checklist）。
- 店主端 / 小程序登录页。

## Decisions

### D1：CSS Port 为主策略（路径 A）

- **决策**：新增 `src/web/src/features/auth/styles/login-page.css`，从 `user-login.html` 逐段 port CSS；class 命名保留 HTML 语义（`login-shell`、`brand-panel`、`form-panel`、`login-card` 等）。
- **颜色映射**：HTML 变量映射到 Design Token：

  | HTML 变量 | Token CSS 变量 |
  |-----------|----------------|
  | `--page` | `--color-page` |
  | `--deep` | `--color-deep` |
  | `--card` | `--color-surface` |
  | `--text` | `--color-text-primary` |
  | `--muted` | `--color-text-secondary` |
  | `--weak` | `--color-text-muted` |
  | `--ghost` | `--color-text-subtle` |
  | `--gold` | `--color-brand-gold` |
  | `--line` | `--color-border-default` |
  | `--line-strong` | `--color-border-emphasis` |
  | `--line-hover` | `--color-border-strong` |

- **材质 tile 渐变**：HTML 中 hex stop 允许在 CSS 文件内通过 `var(--color-*)` 组合近似；若仍不足，在 `:root` 内新增 **登录页 scoped** 自定义 property（如 `--login-tile-calacatta-mid`），值仍来自 token 或 ui-design 规范，不写进 TSX。
- **理由**：HTML 已是最高保真源；Tailwind 拼装无法还原多层渐变与 0.5px 边框细节。
- **备选**：继续 Tailwind override — 已验证 fidelity 不足。

### D2：登录页停用 shadcn 表单 primitive

- **决策**：`LoginForm` 使用原生 `<input type="text/password">`、`<button>`、自定义 checkbox markup（或 styled native checkbox），class 来自 `login-page.css`；**不**使用 shadcn `Input`/`Checkbox`/`Button`。
- **理由**：消除组件默认态泄漏；HTML 原型即为 plain elements。
- **备选**：shadcn + heavy className override — 已证明不稳定。

### D3：左栏视觉 — CSS 材质拼贴，非 JPG 背景

- **决策**：按 HTML 实现 `material-board` + 3 tile 渐变；**不**使用 `/images/login-material-showcase.jpg` 全屏铺底（与当前 `web-client` spec 冲突，本 change 修正 spec）。
- **理由**：`user-login.html` / PNG golden reference 左栏为 CSS 拼贴，非摄影背景。
- **备选**：JPG 背景 — 与 HTML/PNG 不符。

### D4：右栏页脚 — 安全说明，非版权

- **决策**：表单下方展示 HTML `.security` 文案；移除 `LoginCopyright`（© 2025…）。
- **理由**：HTML/PNG 原型为安全审计说明。

### D5：企微入口 — 全宽横排按钮

- **决策**：`.wecom` 全宽 54px 高，inline SVG/icon + 「企业微信登录」文案；**非**圆形 icon + 下方短文案。
- **理由**：对齐 HTML `.wecom` 与 PNG。

### D6：密码框 — 无显隐切换

- **决策**：密码输入为 plain `<input type="password">`，**不**提供 eye icon（HTML 原型无此控件）。
- **理由**：用户明确以 HTML 为最高优先级；与旧 `acceptance.md` 冲突项以 HTML 为准，并更新 web-client spec。
- **备选**：保留 PasswordInput — 偏离 golden reference。

### D7：组件树（presentation / logic 分离）

```text
LoginPage
├── import login-page.css
├── AuthBrandPanel          (.brand-panel)
└── LoginFormPanel          (.form-panel)
    ├── LanguageSwitcher    (.language)
    └── .login-card
        ├── LoginHeader     (.eyebrow + h1 + .sub)
        ├── LoginForm       (<form> — auth logic)
        │   ├── fields
        │   ├── .form-options
        │   ├── .primary
        │   └── ThirdPartyLoginSection (.third-party)
        └── LoginSecurityNotice (.security)
```

- **决策**：删除或废弃 `login-styles.ts` Tailwind 常量，样式归 CSS 文件；`LoginForm` 保留 submit/validation/auth 调用。
- **理由**：单一视觉事实源（CSS file）。

### D8：响应式 — 直接 port HTML media queries

- **决策**：CSS 内保留 `@media (max-width: 1023px)` 与 `(max-width: 639px)` 规则，与 HTML 一致。
- **理由**：避免 Tailwind breakpoint 与 HTML 数值漂移。

### D9：验收 gate

- **决策**：1280×1024 视口并排截图；≥15 项 checklist（背景色、50/50 分屏、Logo、表单宽、输入高、focus 金边、按钮、间距、语言切换、无 notice 横幅等）；全部 pass 方可归档。
- **理由**：参数 checklist 无法保证「看起来像」。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 登录页专用 CSS 与全站 Tailwind 策略分叉 | 限定在 `features/auth/styles/`；ui-design §9 文档化 |
| 材质 tile hex 与「禁止裸 Hex」冲突 | hex 仅存在于 port CSS，且映射为 token 或 scoped CSS variables；TSX 无 hex |
| 移除密码显隐与旧 acceptance 冲突 | 本 change 更新 web-client spec + REQ trace |
| CSS 文件与 HTML 漂移 | port 时注释对应 HTML 行号；变更必须同步 HTML 原型 |
| 废弃 login-styles.ts 导致测试 class 断言失败 | tasks 含测试更新 |

## Migration Plan

1. 创建 `login-page.css`，port HTML styles + token 映射
2. 重构 presentation 组件为 HTML class 结构
3. `LoginForm` 改用 native elements，保留 auth logic
4. 删除 notice 横幅、LoginCopyright、PasswordInput 在登录页的使用
5. 更新 vitest + vite build + docker compose build web
6. PNG 并排验收 → trace.md + acceptance-report
7. 更新 `rules/ui-design.md` §9 CSS Port 说明
8. 归档 change

## Open Questions

| 问题 | 本期决策 |
|------|----------|
| 材质 tile 是否允许登录 scoped hex | 允许仅在 CSS 中，优先 token 组合；仍不足时用 scoped `--login-tile-*` variables |
| Cormorant vs Georgia Logo | HTML 用 Georgia；项目已有 Cormorant via index.html — Logo 继续 `font-brand`，若 PNG diff fail 再换 |
| 占位交互（忘记密码/企微/语言） | noop 或 inline 弱提示；**禁止** notice 横幅 |
