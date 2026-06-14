# design-system Specification

## Purpose
TBD - created by archiving change add-design-system. Update Purpose after archive.
## Requirements
### Requirement: Design Token 层

Web 客户端 MUST 在 `src/web/src/styles/globals.css` 定义 Design Token，映射 `rules/ui-design.md` 色彩、圆角与字距规范，并通过 Tailwind `@theme` 暴露为 semantic utility classes。

#### Scenario: 页面底色 token 可用

- **WHEN** 开发者需要设置页面背景
- **THEN** MUST 使用 semantic class（如 `bg-page`）或 CSS variable `--color-page`
- **AND** 值 MUST 为 `#18160F`

#### Scenario: 品牌金 token 可用

- **WHEN** 开发者需要设置主 CTA 或强调色
- **THEN** MUST 使用 `bg-brand-gold` 或 `text-brand-gold`
- **AND** 值 MUST 为 `#C8A055`

#### Scenario: 边框 token 分级

- **WHEN** 开发者需要设置分割线或输入框边框
- **THEN** MUST 可使用 `border-default`（`rgba(255,255,255,0.07)`）、`border-strong`（`0.18`）、`border-hover`（`0.28`）、`border-focus`（`rgba(200,160,85,0.7)`）

#### Scenario: 圆角 token

- **WHEN** 开发者设置按钮或输入框圆角
- **THEN** MUST 使用 `rounded-industrial`（2px）或 `rounded-card`（3px）
- **AND** MUST NOT 使用 shadcn 默认大圆角（如 `rounded-md`/`rounded-lg`）作为生产组件默认

### Requirement: 禁止裸 Hex 色值（新代码）

Design System 落地后，新增或修改的 Web UI 代码 MUST NOT 在 JSX/TSX 中硬编码 `#18160F`、`#C8A055` 等 design token 对应 Hex 值，MUST 使用 semantic token class 或 CSS variable。

#### Scenario: 新组件使用 token

- **WHEN** 开发者新增 UI 组件
- **THEN** 样式 MUST 引用 Design Token semantic class
- **AND** MUST NOT 内联 `#18160F` 等 Hex 字符串

### Requirement: shadcn/ui 基础组件

Web 客户端 MUST 初始化 shadcn/ui，并在 `src/web/src/components/ui/` 提供以下基础组件：Button、Input、Checkbox、Label、Separator。

#### Scenario: 组件目录存在

- **WHEN** Design System Change 实现完成
- **THEN** `src/web/src/components/ui/button.tsx` 等文件 MUST 存在
- **AND** `components.json` MUST 存在并配置正确

#### Scenario: Button 主 CTA 样式

- **WHEN** 使用 Button `variant="default"`
- **THEN** 按钮 MUST 为金色实底（`bg-brand-gold`）、深色文字（`text-page`）
- **AND** 圆角 MUST 为 2px
- **AND** hover 态 MUST 可感知（亮度或透明度变化）

#### Scenario: Input 工业风样式

- **WHEN** 渲染 Input 组件
- **THEN** 背景 MUST 为透明
- **AND** 默认边框 MUST 使用 `border-strong`
- **AND** focus 态边框 MUST 使用 `border-focus`
- **AND** 默认高度 MUST 支持 `h-16`（64px）尺寸 variant 或 class

#### Scenario: Checkbox 选中态

- **WHEN** Checkbox 被选中
- **THEN** 背景 MUST 为品牌金填充
- **AND** 勾选图标 MUST 为深色，符合 `rules/ui-design.md` §5.6

### Requirement: cn 工具函数

Web 客户端 MUST 提供 `cn()` 工具（clsx + tailwind-merge），供 shadcn 组件与业务组件合并 className。

#### Scenario: cn 可用

- **WHEN** UI 组件需要合并 Tailwind class
- **THEN** MUST 从 `src/web/src/shared/lib/cn.ts` 导入 `cn`
- **AND** 冲突 class MUST 按 tailwind-merge 规则解析

### Requirement: 路径别名

Web 项目 MUST 配置 `@/` 路径别名指向 `src/`，与 shadcn/ui 默认 import 路径一致。

#### Scenario: 别名解析

- **WHEN** 代码 import `@/components/ui/button`
- **THEN** TypeScript 与 Vite MUST 正确解析到 `src/components/ui/button`

### Requirement: 复合 UI 组件（最小集）

Web 客户端 MUST 提供可复用复合组件：`IconInput`（带左侧图标的输入框封装）与 `DividerText`（居中分割文案），供后续登录页与其他表单复用。

#### Scenario: IconInput 结构

- **WHEN** 使用 IconInput
- **THEN** MUST 支持左侧 icon slot、placeholder、error 态
- **AND** MUST 基于 shadcn Input 构建，而非裸 `<input>`

#### Scenario: DividerText 结构

- **WHEN** 使用 DividerText 渲染「其他登录方式」类文案
- **THEN** MUST 展示左右分割线 + 居中弱色文字
- **AND** 分割线 MUST 使用 `border-default` 语义

### Requirement: Design System 预览与验收

Web 客户端 MUST 提供 Design System 预览入口（开发环境路由 `/design-system` 或等效页面），展示 Token 样本与基础组件的全部交互状态。

#### Scenario: 预览页可访问

- **WHEN** 开发环境启动 Web 应用
- **THEN** 用户 MUST 可访问 `/design-system`
- **AND** 页面 MUST 展示 Button、Input、Checkbox 的 default / hover / focus / disabled / error 状态样本

### Requirement: 构建与 Docker 兼容

Design System 实现 MUST 不破坏现有 Web 生产构建与 Docker 镜像构建。

#### Scenario: 本地构建通过

- **WHEN** 运行 `npm run build`（在 `src/web`）
- **THEN** 构建 MUST 成功完成

#### Scenario: Docker Web 构建通过

- **WHEN** 运行 `docker compose build web`
- **THEN** Web 镜像构建 MUST 成功

### Requirement: 文档同步

Design System 落地后 MUST 同步更新相关文档。

#### Scenario: Web README 更新

- **WHEN** Change 完成
- **THEN** `src/web/README.md` MUST 说明 token 位置、shadcn 添加组件命令、禁止裸 Hex 约定

#### Scenario: ui-design 互链

- **WHEN** Change 完成
- **THEN** `rules/ui-design.md` MUST 补充指向 `src/web/src/styles/globals.css` 的 token 实现说明（或互链段落）

