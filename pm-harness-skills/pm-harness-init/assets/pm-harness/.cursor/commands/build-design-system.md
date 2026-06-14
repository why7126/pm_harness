# Build Design System

## 目标

基于 `rules/ui-design.md` 构建可执行的 Design System，将 UI 规范从 Markdown 文档转化为代码约束、组件资产、页面模板和自动校验脚本。

本命令适用于：

- 项目初始化阶段建设 Design System
- UI规范升级后重建设计系统
- AI生成页面前统一基础组件和视觉规则

---

## 必须读取

执行前必须读取：

```text
AGENTS.md
project.yaml
rules/ui-design.md
rules/directory-structure.md
rules/coding.md
rules/testing.md
src/web/README.md
````

如存在以下文件，也必须读取：

```text
src/web/src/styles/globals.css
src/web/tailwind.config.ts
src/shared/design-system/tokens/*
src/shared/ui/*
src/shared/business/*
src/shared/templates/*
```

---

## 禁止行为

AI 不允许：

```text
1. 硬编码 Hex 颜色
2. 在业务页面中直接写 bg-[#xxxxxx]
3. 绕过 src/shared/ui 重新写基础组件
4. 随意新增未登记的颜色、字号、间距、圆角
5. 直接在业务页面中使用原生 button/input/select/table
6. 修改业务需求逻辑
7. 删除已有组件，除非明确说明兼容替代方案
```

---

## Step 1：创建 Design System 目录

确保存在：

```text
design-system/
├── spec.md
├── prompts/
│   ├── generate-page.md
│   ├── generate-form.md
│   ├── generate-table.md
│   └── review-ui.md
├── screenshots/
└── examples/

src/shared/design-system/
├── tokens/
├── README.md

src/shared/ui/
src/shared/business/
src/shared/templates/
```

---

## Step 2：生成 design-system/spec.md

根据 `rules/ui-design.md` 提炼：

```text
设计定位
设计关键词
色彩系统
字体系统
间距系统
圆角系统
组件规范
页面布局规范
交互规则
禁止事项
```

输出：

```text
design-system/spec.md
```

要求：

* 保留 Obsidian YAML Frontmatter
* 明确该文件是 Design System 的总说明
* 明确 `rules/ui-design.md` 是上游规范来源
* 明确代码资产位置

---

## Step 3：生成 Design Tokens

生成：

```text
src/shared/design-system/tokens/
├── colors.ts
├── spacing.ts
├── radius.ts
├── typography.ts
├── shadows.ts
├── zIndex.ts
└── index.ts
```

要求：

* 所有 Token 必须来自 `rules/ui-design.md`
* 使用 TypeScript
* 使用语义化命名
* 不允许直接暴露随意命名颜色
* 必须包含暗色旗舰风所需的背景、文字、边框、品牌金、状态色
* 必须导出统一 `tokens`

示例命名：

```ts
colors.page
colors.surface
colors.footer
colors.textPrimary
colors.textSecondary
colors.brandGold
colors.divider
colors.danger
```

---

## Step 4：生成 CSS Variables

生成或更新：

```text
src/web/src/styles/globals.css
```

要求：

* 将 Design Tokens 映射为 CSS Variables
* 支持 semantic token class
* 支持 shadcn/ui 变量
* 保留 Tailwind 基础层

必须包含类似：

```css
:root {
  --color-page: #18160F;
  --color-surface: #211E16;
  --color-brand-gold: #C8A055;
}
```

---

## Step 5：生成 Tailwind Theme

生成或更新：

```text
src/web/tailwind.config.ts
```

要求：

* 从 CSS Variables 或 Token 中映射语义化颜色
* 支持以下 class：

```text
bg-page
bg-surface
bg-deep
text-primary
text-secondary
text-muted
text-brand-gold
border-subtle
border-strong
```

* 不允许业务代码使用 Hex
* 支持 shadcn/ui

---

## Step 6：生成基础 UI 组件

生成或更新：

```text
src/shared/ui/
```

第一批基础组件至少包含：

```text
Button
Input
Textarea
Select
Checkbox
Badge
Card
Dialog
Drawer
Tabs
Table
Pagination
EmptyState
SearchBar
```

每个组件建议结构：

```text
Button/
├── Button.tsx
├── Button.types.ts
├── Button.example.tsx
└── index.ts
```

要求：

* 使用 React 19 + TypeScript
* 样式必须使用 Tailwind semantic class
* 可基于 shadcn/ui 封装
* 禁止硬编码颜色
* 必须提供 example
* 必须导出 index.ts

---

## Step 7：生成业务组件

生成或更新：

```text
src/shared/business/
```

第一批业务组件至少包含：

```text
TileCard
FeaturedTileCard
TextureRow
TileGallery
TileVideoPlayer
TileFilterPanel
TileSearchBar
```

要求：

* 复用 `src/shared/ui/*`
* 不直接使用原生基础控件
* 不硬编码视觉样式
* 与瓷砖业务场景一致

---

## Step 8：生成页面模板

生成或更新：

```text
src/shared/templates/
```

至少包含：

```text
LandingPageTemplate
ListPageTemplate
DetailPageTemplate
AdminListPageTemplate
AdminEditPageTemplate
DashboardPageTemplate
```

要求：

* 复用 `src/shared/ui/*`
* 复用 `src/shared/business/*`
* 提供企业后台和店主端两类模板
* 不直接实现具体业务数据请求
* 仅承担布局和组合职责

---

## Step 9：生成 Design System Playground

生成：

```text
src/web/src/app/design-system/page.tsx
```

或根据当前路由体系生成等价页面。

该页面必须展示：

```text
颜色 Token
字体 Token
间距 Token
圆角 Token
按钮
输入框
徽章
卡片
搜索栏
产品卡
精选卡
纹理速览条
分页器
页面模板预览
```

用途：

```text
设计验收
AI生成结果校验
前端组件人工Review
```

---

## Step 10：生成 AI Prompt

生成：

```text
design-system/prompts/
├── generate-page.md
├── generate-form.md
├── generate-table.md
└── review-ui.md
```

### generate-page.md

要求说明：

```text
AI生成页面前必须读取 design-system/spec.md 和 src/shared/ui
必须优先复用组件
不得重新设计颜色、圆角、字体、间距
```

### review-ui.md

要求说明：

```text
检查是否违反 Design Token
检查是否硬编码颜色
检查是否绕过 shared/ui
检查是否与 rules/ui-design.md 冲突
```

---

## Step 11：生成自动校验脚本

生成：

```text
scripts/validate-design-system.py
```

检查范围：

```text
src/web
src/shared
```

检查项：

```text
1. 是否出现 Hex 颜色硬编码
2. 是否出现 bg-[#xxxxxx]
3. 是否直接使用原生 button/input/select/textarea
4. 是否出现未登记 Token
5. 是否绕过 src/shared/ui
```

输出：

```text
违规文件
违规行号
违规原因
建议修复方式
```

---

## Step 12：更新文档

必须更新：

```text
rules/ui-design.md
design-system/spec.md
src/shared/design-system/README.md
src/web/README.md
AGENTS.md
DOCUMENT_METADATA_INDEX.md
```

更新内容：

```text
Design System 已落地为可执行代码资产
AI生成UI前必须读取哪些文件
新增页面必须复用哪些组件
禁止硬编码哪些样式
如何运行校验脚本
```

---

## Step 13：创建或更新 OpenSpec Change

如果不存在，创建：

```text
openspec/changes/build-design-system/
```

包含：

```text
proposal.md
design.md
tasks.md
acceptance.md
test-plan.md
trace.md
specs/design-system/spec.md
```

要求：

* proposal 说明为什么要建立 Design System
* design 说明 Token、组件、模板、校验脚本设计
* tasks 拆解所有实现任务
* acceptance 定义验收标准
* test-plan 定义校验方式
* spec 定义系统 SHALL 遵守 Design System

---

## Step 14：验收标准

完成后必须满足：

```text
□ tokens 文件已生成
□ globals.css 已生成或更新
□ tailwind.config.ts 已生成或更新
□ src/shared/ui 已包含基础组件
□ src/shared/business 已包含瓷砖业务组件
□ src/shared/templates 已包含页面模板
□ /design-system 可预览
□ validate-design-system.py 可运行
□ AGENTS.md 已加入 Design System Rule
□ rules/ui-design.md 与代码资产路径一致
□ OpenSpec Change 已创建或更新
```

---

## 最终输出

执行完成后输出：

```text
1. 生成/修改文件列表
2. Design Token 摘要
3. UI组件列表
4. 业务组件列表
5. 页面模板列表
6. 校验脚本使用方式
7. 尚需人工确认的问题
```