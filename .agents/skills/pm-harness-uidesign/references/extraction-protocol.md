# UI/UE 真实项目提炼协议

## 模式

`Mode A+ — Real Project High-Fidelity Extraction`

用于从真实项目代码中高保真提炼设计资产，并沉淀到 `design-schemes/`。

## 输入协议

执行前按 `user-input-schema.md` 收集输入。必须至少具备一个代码事实源：本地项目代码库目录、GitHub 代码库链接或本地代码压缩包。辅助输入可以提升保真度，但不能替代代码事实源。

## 扫描清单

使用 `rg --files` 优先扫描：

- `tokens`、`theme`、`variables`、`design-system`。
- `*.css`、`*.scss`、`*.less`、`tailwind.config.*`。
- `components`、`layouts`、`pages`、`routes`、`router`。
- `navigation`、`sidebar`、`topbar`、`tabbar`、`menu`。
- `app.json`、移动端自定义导航、custom tab bar。
- `README`、`rules/ui-design.md`、设计规范文档。
- package manager 文件，用于识别框架和 UI/icon 库。

## 必读源码类别

先读这些事实源，再生成产物：

1. Design tokens：颜色、字体、间距、圆角、阴影。
2. 全局 CSS：CSS variables、主题、响应式断点。
3. App shell：后台布局、页面容器、主导航结构。
4. Navigation components：侧边栏、顶栏、tabbar、菜单数据。
5. Navigation behavior：展开/收起、localStorage key、权限过滤、aria label。
6. 关键页面样式：login、dashboard、列表页、详情页、表单页。
7. 组件实现：button、card、input、badge、table、modal、empty/loading/error。

## design.json 内容

提取：

- `schema_version`
- `scheme_id`
- `scheme_name`
- `source_project`
- `source_repo`
- `source_files`
- `inferred`
- `category`
- `colors`
- `typography`
- `spacing`
- `components`
- `layout`
- `interaction`
- `animation`
- `style_profile`

`style_profile` 必须包含：

- `keywords`
- `primary_aesthetic`
- `density`
- `dark_mode_support`
- `avoid`

## navigation.json 内容

当导航可复用时提取：

- `scheme_id`
- `scheme_name`
- `source_files`
- `nav_type`
- Web、Miniapp、Mobile、Desktop 等 surface 拆分。
- 布局宽度、高度、sticky/fixed 行为。
- 背景、边框、文字、active、hover、collapsed 状态。
- 图标库、图标名称、特殊 glyph。
- 版本号展示。
- 用户菜单结构、字号、chevron、dropdown。
- 权限过滤。
- 状态持久化 key。
- aria 和可访问性规则。
- 集成注意事项。

如果导航仅是普通顶部链接且没有独立复用价值，可以不生成导航资产，但必须在 `meta.json` 说明。

## demo.html 要求

`demo.html` 用于一眼判断整体 UI/UE 效果：

- 单文件、自包含、可直接浏览器打开。
- CSS 内联，不依赖构建系统。
- 允许少量原生 JS 展示交互。
- 展示真实项目的核心视觉密度和关键组件。
- Dashboard 类项目应展示侧边栏、指标卡、表格、快捷入口、状态和色板。
- Landing 类项目应展示首屏、内容区、CTA 和品牌视觉。
- Mobile/Miniapp 类项目应展示手机壳内的真实导航和 tabbar 形态。

## navigation-demo.html 要求

当生成导航资产时，必须提供导航专项 demo：

- 单独展示侧边栏、顶栏、tabbar、移动导航等。
- 展示展开/收起、active、hover、角色过滤说明。
- 对可交互状态用原生 JS 模拟。
- 和 `navigation.json` 保持一致。

## ui-design.md 要求

`ui-design.md` 是人读版，不要复刻完整 JSON。它应覆盖：

- 设计定位。
- 适用产品和不适用场景。
- 核心视觉规则。
- Typography 规则。
- Layout 规则。
- Navigation 规则。
- User menu、version badge、sidebar toggle 等关键 affordance。
- Component 规则。
- Reuse checklist。

## meta.json 要求

必须记录：

- `id`
- `name`
- `source_project`
- `source_repo`
- `source_type`
- `source_files`
- `category`
- `tags`
- `created_at` 或 `updated_at`
- `demo_path`
- `navigation_demo_path`
- `design_summary`
- `inferred`
- `navigation_applicability`

## registry.json 更新

注册表条目应包含：

- `id`
- `name`
- `source_repo`
- `category`
- `tags`
- `created_at`
- `demo_path`
- `navigation_demo_path`
- `design_summary`

更新已有方案时保留 ID，更新 `updated_at`。

## 校验

交付前必须执行：

```bash
python3 -m json.tool design-schemes/registry.json
python3 -m json.tool design-schemes/schemes/<scheme-id>/meta.json
python3 -m json.tool design-schemes/schemes/<scheme-id>/design.json
python3 -m json.tool design-schemes/schemes/<scheme-id>/navigation.json
```

若没有 `navigation.json`，跳过该文件但检查 `meta.json` 是否写明原因。

同时搜索用户强调过的关键细节。例如：

```bash
rg -n "sidebar|collapsed|version|user menu|chevron|⌃|admin-sidebar-collapsed" design-schemes/schemes/<scheme-id>
```

## 交付说明

最终回复应包含：

- 方案路径。
- 生成/更新了哪些资产。
- 使用的真实源码关键文件。
- 已执行的校验。
- 没有生成的资产及原因。
- 仍需人工确认的视觉风险。
