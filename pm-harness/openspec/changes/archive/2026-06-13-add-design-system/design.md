## Context

- **背景**：`src/web` 当前 `globals.css` 仅 `@import "tailwindcss"`；无 `components/ui/`；登录页等业务组件直接硬编码 `#18160F`、`#C8A055` 等色值。
- **规范来源**：`rules/ui-design.md`（工业石材 · 暗色旗舰风 v1.0）、`issues/requirements/REQ-0001-user-login/prototype/web/user-login.md` §4 Design Token。
- **技术栈约束**：React 19、TypeScript、Tailwind CSS v4、shadcn/ui、pnpm（本地）/ npm（Docker）。
- **前置 Change**：`add-user-login` 功能已完成；本 Change 为 Path C Phase 1，后续 `refactor-login-ui` 为 Phase 2。

## Goals / Non-Goals

**Goals:**

- 将 `rules/ui-design.md` 色彩/字体/圆角/分割线映射为可执行的 CSS Design Token。
- 完成 shadcn/ui 初始化，安装 Button、Input、Checkbox、Label、Separator 并应用工业风 override。
- 提供 `cn()` 工具与组件使用约定，业务代码不再写裸 Hex 色值。
- 提供可验收的组件状态（default / hover / focus / disabled / error）与可选 `/design-system` 预览页。
- Docker 与本地 `vite build` 均可通过。

**Non-Goals:**

- 登录页 UI 重构（属于 `refactor-login-ui`）。
- 全站所有 shadcn 组件一次性安装（Table、Dialog 等留给后续 Change）。
- 小程序 Design System。
- 修改 auth API、路由或业务逻辑。
- 替换现有登录页背景图为真实材质图（Phase 2）。

## Decisions

### D1：Token 实现 — Tailwind v4 `@theme` + CSS Variables

- **决策**：在 `globals.css` 使用 `@theme` 定义 semantic colors，同时暴露 `:root` CSS variables 供非 Tailwind 场景使用。
- **理由**：项目已用 Tailwind v4；与 shadcn/ui 新模板兼容；单一来源映射 `ui-design.md`。
- **备选**：独立 `tokens.ts` 仅 JS 侧 — 无法驱动 Tailwind utility class。

**Token 命名（semantic）：**

| Token | 值 | Tailwind 示例 |
|---|---|---|
| `--color-page` | `#18160F` | `bg-page` |
| `--color-secondary` | `#211E16` | `bg-secondary` |
| `--color-deep` | `#100F0A` | `bg-deep` |
| `--color-text-primary` | `#EDE8DF` | `text-primary` |
| `--color-text-secondary` | `rgba(237,232,223,0.5)` | `text-secondary` |
| `--color-text-muted` | `rgba(237,232,223,0.3)` | `text-muted` |
| `--color-brand-gold` | `#C8A055` | `text-brand-gold` / `bg-brand-gold` |
| `--color-brand-gold-muted` | `rgba(200,160,85,0.12)` | `bg-brand-gold-muted` |
| `--color-error` | `#E07050` | `text-error` / `border-error` |
| `--color-border-default` | `rgba(255,255,255,0.07)` | `border-default` |
| `--color-border-strong` | `rgba(255,255,255,0.18)` | `border-strong` |
| `--color-border-hover` | `rgba(255,255,255,0.28)` | `border-hover` |
| `--color-border-focus` | `rgba(200,160,85,0.7)` | `border-focus` |
| `--radius-industrial` | `2px` | `rounded-industrial` |
| `--radius-card` | `3px` | `rounded-card` |
| `--tracking-brand` | `0.16em` | `tracking-brand` |

### D2：shadcn/ui 初始化 — New York 风格 + 自定义 CSS variables

- **决策**：使用 shadcn CLI 初始化，`style: new-york`，`baseColor: neutral`，再通过 CSS variables 覆盖为暗色工业风；禁用默认大圆角与 heavy shadow。
- **理由**：AGENTS.md 强制 shadcn/ui；New York 更贴近精密工业感。
- **备选**：纯手工 Radix 组件 — 重复劳动，违背项目规范。

**首期安装组件：**

```text
button, input, checkbox, label, separator
```

### D3：Button Variants

| Variant | 用途 | 样式要点 |
|---|---|---|
| `default` | 主 CTA | `bg-brand-gold text-page`，hover 亮度提升 |
| `outline` | 幽灵/次要 | 透明底，`border-strong`，弱色文字 |
| `ghost` | 图标/链接 | hover `bg-white/5` |
| `destructive` | 危险操作 | 使用 error 语义色 |

尺寸：`default` 高度对齐登录页 64px（`h-16`），`sm` 用于紧凑场景。

### D4：Input 样式 — 透明底 + 强边框 + focus 金色

- 默认：`border-strong`、`bg-transparent`、`h-16`、`rounded-industrial`
- Hover：`border-hover`
- Focus：`border-focus`，无 glow shadow
- Error：`border-error` + 下方 error 文案 slot（由业务组件处理）

### D5：Checkbox — 金色选中态

- 未选中：透明底 + `border-strong`
- 选中：`bg-brand-gold` + 深色勾（对齐 ui-design §5.6 / 原型 §4.5）
- Focus：弱金色 ring

### D6：目录结构

```text
src/web/
├── components.json              # shadcn 配置
├── src/
│   ├── components/ui/           # shadcn 生成 + override
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── checkbox.tsx
│   │   ├── label.tsx
│   │   └── separator.tsx
│   ├── shared/
│   │   ├── lib/cn.ts
│   │   └── ui/                  # 复合组件（可选）
│   │       ├── icon-input.tsx
│   │       └── divider-text.tsx
│   ├── styles/
│   │   └── globals.css          # @theme tokens
│   └── pages/dev/
│       └── DesignSystemPage.tsx # 可选预览页
```

### D7：路径别名

- **决策**：Vite/TS 配置 `@/` → `src/`，与 shadcn 默认一致。
- **文件**：`vite.config.ts` resolve.alias、`tsconfig.json` paths。

### D8：Docker 构建

- **决策**：Design System 变更后必须验证 `src/web/Dockerfile` 的 `npm run build`；不引入 pnpm-only 脚本到 Docker 层。
- **理由**：当前 Docker 已改用 npm 构建。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| Tailwind v4 + shadcn 版本兼容 | Phase 1 首任务做 spike：init shadcn + 一个 Button 验证 build |
| Token 与 ui-design.md 漂移 | spec 要求 token 值与 rules 一致；文档互链 |
| 过度安装 shadcn 组件 | 首期仅 5 个基础组件 |
| 业务页仍硬编码 Hex | spec 要求新代码禁止裸 Hex；refactor-login-ui 迁移旧代码 |
| shadcn 默认亮色主题污染 | 全部通过 CSS variables 暗色化 |

## Migration Plan

1. 建立 token + shadcn 基础（本 Change）。
2. 后续 `refactor-login-ui` 将登录页迁移到新组件，移除硬编码色值。
3. 新功能页面（tile-catalog、tile-admin）必须消费 Design System，不得新增裸 Tailwind Hex。

**回滚**：移除 `components/ui` 与 token 扩展不影响 auth 功能；业务页仍可用旧样式直至 Phase 2。

## Open Questions

| 问题 | 本期决策 | 后续 |
|---|---|---|
| 是否引入 Storybook | 否，用 `/design-system` 轻量预览页 | 可视需要再议 |
| 字体是否引入自定义 webfont | 否，沿用系统 sans | 品牌字体单独 Change |
| Icon 库 | lucide-react（已安装） | 统一全站 |
