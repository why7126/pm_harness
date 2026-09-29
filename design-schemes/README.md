# 本地设计方案库

`design-schemes/` 用于存放可复用的本地 UI/UX 设计资产，服务于新项目初始化和已有项目重构。

每个方案都应该同时便于人工查看，也便于自动化工具消费：

- `design.json`：整体 UI/UX 设计令牌（Design Token）和组件规则。
- `navigation.json`：独立导航结构与交互规则。
- `demo.html`：整体 UI/UX 方案的自包含预览页面。
- `navigation-demo.html`：导航方案的自包含预览页面。
- `meta.json`：方案元数据和适用性说明。

## 当前方案

| 方案 | 路径 | 用途 |
|---|---|---|
| TilesFST | `schemes/tilesfst/` | 沉淀 TilesFST 的整体 UI/UX 风格和导航资产。 |
| DeepSeek Harness | `schemes/deepseek-harness/` | 沉淀 DeepSeek Harness Web Client 的 Agent 工作台视觉语言和可折叠侧边栏导航资产。 |

## 使用方式

用于新项目初始化：

1. 从 `registry.json` 中选择一个 UI 方案。
2. 将 `design.json` 复制到目标项目，作为设计令牌（Design Token）事实源。
3. 如果目标项目需要复用导航模式，同步复制 `navigation.json`。
4. 将 HTML demo 文件复制或链接到目标项目的原型或设计预览目录。
5. 将选中的方案渲染到 `rules/ui-design.md` 和相关前端设计文档中。

用于已有项目重构：

1. 将当前前端 Token 和导航结构与选中方案进行对比。
2. 如果要调整全局视觉语言，优先应用 `design.json`。
3. 如果只调整应用外壳、菜单、路由或布局，可独立应用 `navigation.json`。
4. 保留可视化预览页面，用于人工验收。

## 质量规则

- HTML demo 必须自包含，并可直接用浏览器打开。
- `design.json` 和 `navigation.json` 是设计资产事实源。
- 从真实源码提取的方案应标记 `inferred: false`；人工重建或占位值应标记 `inferred: true`。
- 不要从来源项目复制仅业务内部使用的名称、密钥、接口地址、账号或生产数据。
