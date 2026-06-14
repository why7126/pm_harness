## Context

- **前置 Change**：`refactor-login-ui` 已归档；登录页已使用 Design Token + shadcn，auth 功能完整。
- **差距根因**：`refactor-login-ui` design 将真实背景图列为 Non-Goal；验收误将「token 化」等同于「原型一致」。
- **原型来源**：`prototype/web/user-login.png`、`user-login.md` §3–§4、§7.3 静态资源表。
- **规范**：`rules/ui-design.md`、`openspec/specs/design-system/spec.md`。

## Goals / Non-Goals

**Goals:**

- 桌面端 `/admin/login` 与 `user-login.png` 视觉高度一致（背景、布局、间距、图标、字体层级）。
- 静态资源可随 Docker Web 镜像部署。
- 继续禁止登录页 TSX 裸 Hex；使用 Design Token。
- 视觉验收清单可执行、可勾选。

**Non-Goals:**

- 企业微信 OAuth、忘记密码、i18n 真实切换逻辑。
- 修改 auth API / store / 路由守卫。
- 小程序或店主端登录页。
- 引入 Storybook；沿用页面直验 + acceptance checklist。

## Decisions

### D1：背景图来源

- **决策**：在 `src/web/public/images/` 放置 `login-material-showcase.jpg`；若团队无摄影素材，从原型图左栏裁切/export 生成 Web 用 JPG（≤500KB），并在 `data/samples/images/` 保留源文件引用说明。
- **理由**：原型 §7.3 明确要求 JPG；SVG 占位无法还原材质摄影感。
- **备选**：Unsplash 石材图 — 色调可能偏离，需 color grade。

### D2：AuthBrandPanel 背景层

```text
[ JPG bg-cover opacity-80 ]
  → [ gradient from-page/95 via-page/65 to-page/25 ]
    → [ Logo + Hero + Features z-10 ]
```

与 `user-login.md` §3.3 一致，JPG 路径 `/images/login-material-showcase.jpg`。

### D3：LanguageSwitcher

- **决策**：独立组件 `LanguageSwitcher.tsx`：`简体中文` + `ChevronDown`（lucide），点击触发 `onPlaceholder('功能建设中')` 或 noop；样式 `text-secondary text-sm`。
- **位置**：右栏 `absolute right-6 top-6`。

### D4：WeCom 入口

- **决策**：`public/icons/wecom.svg`（绿色气泡风格简化 SVG）；圆形 `border-border-strong` 按钮内嵌 24px 图标 + 下方「企业微信」文案。
- **行为**：点击仍 `onPlaceholder('功能建设中')`。

### D5：Spacing 精修（对照 §4.4）

| 项目 | 值 | Tailwind |
|---|---|---|
| 标题到表单 | 48px | `mb-12` |
| 表单项间距 | 28px | `space-y-7` |
| 主按钮到第三方 | 56px | `pt-14` 或等效 |
| 表单最大宽度 | 520px | `max-w-[520px]` |
| 左栏 padding | 56px 64px | `px-14 py-14 lg:px-16` |

### D6：验收方式

- **决策**：更新 `issues/requirements/REQ-0001-user-login/acceptance.md` 视觉项；Sprint acceptance-report 仅在实际对比通过后勾选。
- **检查点**：背景图、语言切换、企微图标、分屏比例、输入框高度 64px、按钮金色 CTA。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| JPG 体积过大 | 压缩至 <300KB；Docker 构建验证 |
| 裁切图与原型仍有差异 | 以 PNG 为 golden reference，迭代 overlay |
| 组件拆分过度 | 仅拆 LanguageSwitcher、WeComLoginButton，其余保持 feature 目录 |

## Migration Plan

1. 添加静态资源 → 更新 AuthBrandPanel 背景。
2. 新增 LanguageSwitcher、WeCom 图标 → 更新 LoginPage/LoginForm。
3. Spacing pass → vitest + build + Docker。
4. 人工对比 PNG → 更新 acceptance。

## Open Questions

| 问题 | 本期决策 |
|---|---|
| 是否使用 prototype PNG 直接导出 JPG | 可接受，优先快速对齐 |
| Logo 是否换 SVG | 否，文字 Logo + tracking-brand 足够 |
