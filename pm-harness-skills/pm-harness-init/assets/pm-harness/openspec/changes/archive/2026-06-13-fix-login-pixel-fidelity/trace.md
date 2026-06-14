---
title: Change 追踪
purpose: 记录 fix-login-pixel-fidelity 与 Sprint 01、REQ-0001 的追踪关系
source: align-login-prototype 视觉差距分析
status: implemented
---

# Change 追踪

## 基本信息

```yaml
change_id: fix-login-pixel-fidelity
requirement_id: REQ-0001
priority: P0
status: implemented
iteration: sprint-01
depends_on:
  - align-login-prototype
source: user-login.png golden reference 像素级验收
```

## PNG Diff Checklist（1280px 并排验收）

| # | 检查点 | Pass |
|---|---|---|
| 1 | 左栏 STONEX Logo 衬线字体气质（font-brand） | ✓ |
| 2 | 左栏 JPG 背景 + gradient | ✓ |
| 3 | 左栏宣传语 / Feature 列表 spacing | ✓ |
| 4 | 右栏 `bg-deep` 背景 | ✓ |
| 5 | 语言切换 简体中文 + Chevron | ✓ |
| 6 | 欢迎登录标题 36px | ✓ |
| 7 | 副标题 STONEX 金色 + 其余 primary | ✓ |
| 8 | 输入框 64px + 细边框 + 金色 icon + border-only focus | ✓ |
| 9 | 登录按钮金色 CTA | ✓ |
| 10 | 企微绿色官方风格图标（#2BAD13） | ✓ |
| 11 | 版权 footer 弱化居中 | ✓ |
| 12 | 占位交互无 notice 横幅（noop） | ✓ |

**验收说明**：基于代码实现与 `user-login.md` §3–§4 对照；建议团队在 http://localhost:3000/admin/login 与 PNG 并排最终 sign-off。

## Auth 逻辑隔离

以下文件在本 Change 中**未修改**：

- `src/web/src/features/auth/store/`
- `src/web/src/features/auth/hooks/useAuth.ts`
- `src/web/src/features/auth/api/`

## 实现摘要

| 类别 | 路径 |
|---|---|
| 品牌字体 | `index.html` Google Fonts + `globals.css` `--font-brand` |
| 登录样式 override | `login-styles.ts` |
| 组件拆分 | `LoginFormPanel`, `LoginHeader`, `ThirdPartyLoginSection` |
| 企微图标 | `public/icons/wecom.svg`（绿色） |
| 规范 | `rules/ui-design.md` §9 登录页 |

## 测试与构建

| 命令 | 结果 |
|---|---|
| `vitest run` | 18 passed |
| `vite build` | ✓ |
| `docker compose build web` | ✓ |

## 下一步

- `/opsx:archive fix-login-pixel-fidelity`
- Sprint 01 团队 PNG sign-off
