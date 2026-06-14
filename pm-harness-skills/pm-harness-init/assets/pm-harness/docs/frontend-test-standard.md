---
purpose: 前端测试标准
content: Vitest + Testing Library 组件测试约定
source: build-test-framework
update_method: 前端测试规范变更时同步更新
---

# 前端测试标准

## 工具栈

- Vitest
- React Testing Library
- jsdom

## 必须验证

- 组件渲染不抛错
- 用户事件（click、input）与状态变化
- Design System 组件 variant（smoke）

## 位置

```text
src/web/src/**/*.test.tsx
src/web/src/**/*.test.ts
```

## 运行

```bash
cd src/web && pnpm test
```

## 与 E2E 分工

- 组件级：Vitest
- 跨页面流程：Playwright（`tests/e2e/`）

## Design System

`design-system.test.tsx` 覆盖 Button/Input 等基础组件 smoke。
