# REQ-0000 建设 Design System

## 1. 背景

瓷砖信息管理平台包含 Web 店主端、管理端与小程序，需要统一的「工业石材 · 暗色旗舰风」视觉语言。项目初始化阶段必须先落地可执行的 Design System，作为后续业务页面的消费基础。

## 2. 目标

- 将 `rules/ui-design.md` 转化为 TS Token、CSS 变量、Tailwind 语义 class
- 建立 shadcn/ui 基础组件与复合 UI、业务组件、页面模板
- 提供 `/design-system` 预览页与自动校验脚本

## 3. 范围

| 包含 | 不包含 |
|------|--------|
| Token、globals.css、tailwind | 具体业务页面数据对接 |
| shadcn Button/Input/Checkbox 等 | 小程序端完整组件库 |
| shared/ui、business、templates | 浅色主题完整验收 |

## 4. 验收概要

- Token 与组件可在 `/design-system` 预览
- `validate-design-system.py` 可运行
- AGENTS.md 已登记 DS 应用规范

## 5. 状态

`completed` — 已通过 `add-design-system` Change 交付，Sprint-00 补登记。
