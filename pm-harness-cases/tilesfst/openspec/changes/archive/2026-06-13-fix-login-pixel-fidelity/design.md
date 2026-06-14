## Context

- **前置 Change**：`align-login-prototype` 已实现（JPG 背景、LanguageSwitcher、WeCom SVG、spacing 数字），但视觉 fidelity 未达 PNG golden reference。
- **差距根因**：DS/shadcn 抽象层 + checklist 验收，未做 PNG 并排像素对比；`align-login-prototype` design D4 企微图标、D6 验收方式执行不足。
- **原型来源**：`issues/requirements/REQ-0001-user-login/prototype/web/user-login.png`、`user-login.md` §2–§4。
- **规范**：`rules/ui-design.md`（将补充登录页专章）、`openspec/specs/design-system/spec.md`。
- **约束**：auth store / hooks / API / 路由守卫冻结；继续禁止登录页 TSX 裸 Hex。

## Goals / Non-Goals

**Goals:**

- 桌面端 `/admin/login` 与 `user-login.png` 并排对比，团队判定为「一致或仅有可接受像素偏差」。
- 修复已识别的高感知差距：Logo 字体、企微图标、副标题金色、控件形态、占位交互不破坏布局。
- 组件树对齐 `user-login.md` §2（LoginFormPanel / LoginHeader / ThirdPartyLoginSection）。
- 验收 gate：1280px 截图 diff 清单 + acceptance-report 视觉项勾选。
- `rules/ui-design.md` 增加登录页专章，与 `user-login.md` 对齐。

**Non-Goals:**

- 企微 OAuth、忘记密码、i18n 真实逻辑。
- 修改 auth API / store / 路由守卫。
- 引入 Storybook / Percy 等自动化视觉回归基础设施（本期手工并排 + 清单）。
- 小程序 / 店主端登录页。

## Decisions

### D1：Golden Reference 验收法

- **决策**：以 `user-login.png` 为唯一视觉 golden reference；建立 ≥12 项 diff checklist（见 tasks §7），每项 MUST 在 trace.md 记录 pass/fail；Sprint acceptance 视觉项 MUST 全部 pass 方可关闭。
- **理由**：前序 checklist 验收无法保证「看起来像」。
- **备选**：自动化 screenshot diff — 本期成本过高，延后。

### D2：品牌 Logo 字体

- **决策**：为 STONEX Logo 引入衬线/高端品牌字体（推荐 Google Fonts `Cormorant Garamond` 或 `Playfair Display`，via `@font-face` 或 npm 自托管）；仅用于左栏 Logo 与右栏 STONEX 强调，正文仍用系统 sans。
- **理由**：PNG 中 Logo 为衬线气质，sans + letter-spacing 无法还原。
- **备选**：SVG Logo — 原型为文字 Logo，字体方案更贴近。

### D3：企业微信图标

- **决策**：替换 `wecom.svg` 为官方绿色风格（`#2BAD13` 或原型取样），圆形边框内 24–28px；MUST NOT 使用蓝色 messenger bubble。
- **理由**：当前 `#2F8FF4` 蓝色与原型差异极大，用户一眼可辨。

### D4：右栏副标题金色范围

- **决策**：`欢迎登录` 下副标题整行 `STONEX 瓷砖信息管理平台` 中，**STONEX** 使用 `text-brand-gold`，其余使用 `text-primary`（与 user-login.md §1.3 及 PNG 一致）；若 PNG 整行金色则按 PNG 调整为整行 `text-brand-gold`（实现前并排确认一次）。
- **理由**：消除副标题层级偏差。

### D5：登录页 shadcn override

- **决策**：在登录 feature 组件内通过 `className` / `login-*` variant 覆盖，不修改全局 shadcn 默认：
  - Input/Button：移除或弱化 `focus-visible:ring-offset-2`，对齐 §4.5 focus border only
  - Password eye：改用 `IconButton` 风格（透明底、muted icon），非 ghost Button 方块
  - Checkbox：登录页使用 `size-[18px]` 若原型偏大
- **理由**：全局 DS 组件需保持通用性；登录页 fidelity 通过 scoped override 实现。

### D6：占位交互不破坏布局

- **决策**：语言/企微/忘记密码点击改用以下之一（按视觉影响最小）：
  1. noop（无 UI 反馈），或
  2. 字段下方 inline 弱提示 2s 消失，或
  3. 固定位置 toast（不推挤表单）
- **MUST NOT** 在表单上方插入 notice 横幅块。
- **理由**：当前 `LoginPage` notice 横幅不在原型中，严重破坏观感。

### D7：组件拆分

```text
LoginPage
├── AuthBrandPanel (BrandVisualPanel)
└── LoginFormPanel
    ├── LanguageSwitcher
    ├── LoginHeader
    ├── LoginForm (logic frozen)
    ├── ThirdPartyLoginSection
    │   ├── DividerText
    │   └── WeComLoginButton
    └── LoginCopyright
```

- **决策**：按上树拆分/重命名；`LoginForm` 仅保留表单逻辑与字段。
- **理由**：对齐 user-login.md §2，便于 fidelity 逐区验收。

### D8：rules/ui-design.md 登录页专章

- **决策**：在 `rules/ui-design.md` 新增 §登录页，提炼色彩/字体/间距/组件态，引用 `user-login.md` 为详细 spec。
- **理由**：消除「ui-design.md 不管登录页」的规范真空。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| 字体加载增加 FOUT | 仅 1 款 woff2 子集；font-display: swap |
| 衬线字体与系统 sans 混排 | 严格限定 Logo/品牌名使用范围 |
| override 与 DS 漂移 | override 限定在 `features/auth/components/` |
| PNG vs user-login.md 细节冲突 | 以 PNG 为准，冲突项记录于 trace.md |

## Migration Plan

1. 建立 diff checklist → 字体 + 企微图标 + 副标题
2. 组件拆分 + shadcn override pass
3. 移除 notice 横幅 → 占位交互调整
4. vitest + vite build + docker compose build web
5. PNG 并排验收 → 更新 acceptance-report + ui-design.md
6. 归档 `align-login-prototype`（若尚未）→ 归档本 Change

## Open Questions

| 问题 | 本期决策 |
|---|---|
| 副标题整行金色还是仅 STONEX | 实现前 PNG 并排确认，默认 STONEX 金色 + 其余 primary |
| 品牌字体选型 | Cormorant Garamond 600，可替换但 MUST 衬线 |
| align-login-prototype 是否先归档 | 建议本 Change apply 前或并行归档，避免双 active change 混淆 |
