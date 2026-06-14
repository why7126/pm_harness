# 验收标准

## 功能

- [x] `src/shared/design-system/tokens/` 包含颜色、间距、圆角、字体、阴影
- [x] `src/web/src/styles/globals.css` 映射 semantic CSS 变量
- [x] `src/web/tailwind.config.ts` 引用共享 Token
- [x] shadcn 基础组件已主题化（Button、Input、Checkbox、Label、Separator）
- [x] 复合 UI：SearchBar、IconInput、Pagination、Card、Badge 等
- [x] 业务组件：ProductCard、FeaturedCard、ProductGrid、TextureRow
- [x] 页面模板：Landing、List、Detail、AdminList、AdminEdit
- [x] 开发环境 `/design-system` 可访问

## 治理

- [x] `scripts/validate-design-system.py` 可运行
- [x] `src/shared/design-system/spec.md` 与 README 已创建
- [x] AGENTS.md Design System 应用规范已登记

## 测试

- [x] `cn()` 与 DS 组件 smoke 测试存在
