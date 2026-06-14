## 1. 环境与配置

- [x] 1.1 在 `src/web` 配置 Vite `@/` 路径别名（`vite.config.ts`、`tsconfig.json`）
- [x] 1.2 运行 shadcn CLI 初始化，生成 `components.json`（style: new-york，Tailwind v4 兼容）
- [x] 1.3 验证 Tailwind v4 + shadcn 兼容性（安装 Button 后 `npm run build` 通过）

## 2. Design Token

- [x] 2.1 在 `src/web/src/styles/globals.css` 定义 `@theme` semantic colors（page、secondary、deep、brand-gold、border-*、error 等）
- [x] 2.2 定义圆角 token（`rounded-industrial` 2px、`rounded-card` 3px）与字距 token（`tracking-brand` 0.16em）
- [x] 2.3 定义文字色 token（text-primary、text-secondary、text-muted）
- [x] 2.4 创建 `src/web/src/shared/lib/cn.ts`（clsx + tailwind-merge）

## 3. shadcn/ui 基础组件

- [x] 3.1 安装并主题化 `button`（default/outline/ghost variants，主 CTA 金色实底）
- [x] 3.2 安装并主题化 `input`（透明底、border-strong、focus 金色、支持 h-16）
- [x] 3.3 安装并主题化 `checkbox`（金色选中态、深色勾）
- [x] 3.4 安装 `label` 与 `separator`
- [x] 3.5 移除或 override shadcn 默认大圆角/shadow，统一工业风 2px 圆角

## 4. 复合组件

- [x] 4.1 创建 `src/web/src/shared/ui/icon-input.tsx`（左侧 icon + Input + error slot）
- [x] 4.2 创建 `src/web/src/shared/ui/divider-text.tsx`（居中分割文案）

## 5. 预览与验收

- [x] 5.1 创建 `src/web/src/pages/dev/DesignSystemPage.tsx`，展示 token 样本与组件状态
- [x] 5.2 注册开发路由 `/design-system`（仅 dev 或始终可访问）
- [x] 5.3 对照 `rules/ui-design.md` 色彩/圆角表逐项验收
- [x] 5.4 运行 `npm run build` 验证生产构建
- [x] 5.5 运行 `docker compose build web` 验证 Docker 构建

## 6. 文档

- [x] 6.1 更新 `src/web/README.md`：token 位置、shadcn 添加命令、使用约定
- [x] 6.2 更新 `rules/ui-design.md`：补充 token 实现文件互链
- [x] 6.3 创建 `openspec/changes/add-design-system/trace.md` 关联 Sprint 与后续 `refactor-login-ui`

## 7. 测试（可选最小集）

- [x] 7.1 为 `cn()` 编写单元测试（class 合并冲突解析）
- [x] 7.2 为 Button/Input 编写 smoke 测试（渲染 default variant）
