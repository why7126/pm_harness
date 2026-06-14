# fix-login-css-port — Trace

## 变更摘要

- 自 `user-login.html` port `login-page.css`（CSS Port 路径 A）
- React 组件改用 HTML class 结构；表单使用原生 input/button
- 移除 shadcn 登录表单 primitive、`login-styles.ts`、`LoginCopyright.tsx`

## PNG 视觉 Diff Checklist（1280×1024）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | 页面背景色 `#18160F` + shell 渐变 | pass | `.login-shell` radial + linear-gradient |
| 2 | 左右 50% / 50% 分屏 | pass | `grid-template-columns: 1fr 1fr` |
| 3 | Logo 金色 + 0.16em 字距 + 左上 | pass | `.logo` |
| 4 | 左栏统计卡 + 材质拼贴 | pass | `.stats-card` + `.material-board` |
| 5 | 右栏 radial glow + page 背景 | pass | `.form-panel` |
| 6 | 表单 max-width 420px | pass | `.login-card` |
| 7 | 输入框高度 64px | pass | `.field-input` |
| 8 | focus 纯金色边框 | pass | `.field-input:focus` |
| 9 | 主按钮 56px 金色实底 | pass | `.primary` |
| 10 | 表单项间距 28px | pass | `.field` margin-bottom |
| 11 | 标题到表单 48px | pass | `.login-form` margin-top |
| 12 | 主按钮到企微 56px | pass | `.third-party` padding-top |
| 13 | 语言切换右上角 | pass | `.language` absolute |
| 14 | 无 notice 横幅 | pass | 已移除 |
| 15 | 企微全宽横排按钮 | pass | `.wecom` |
| 16 | 安全说明页脚 | pass | `.security` |
| 17 | 无大圆角/卡片阴影表单区 | pass | 无 login-card 背景/shadow |
| 18 | 移动端 <1024px 隐藏左栏 | pass | media query |

## 验证命令

```bash
cd src/web && npx vitest run src/features/auth   # 15 passed
cd src/web && npm run build                       # success
./scripts/docker-up.sh                            # web :3000
```

## 已知可接受偏差

| 项 | 说明 |
|----|------|
| 材质 tile 色值 | 使用 scoped CSS variables + color-mix 近似 HTML hex，非 1:1 hex |
| 企微 SVG 绿色 | 项目 `/icons/wecom.svg` 与 HTML inline `#28C445` 略有差异 |
| Logo 字体 | Cormorant Garamond vs HTML Georgia — 均为衬线品牌字 |

## 遵循规范

- `rules/ui-design.md` §9（CSS Port）
- `rules/directory-structure.md`
- `openspec/changes/fix-login-css-port/design.md`
