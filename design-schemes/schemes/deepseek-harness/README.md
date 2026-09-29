# DeepSeek Harness Design Scheme

从 `https://github.com/deepseek-ai/deepseek-harness` 提炼的 DeepSeek Harness Web Client UI/UE 设计资产。

## 文件

- `meta.json`：方案元数据、来源文件和适用范围。
- `design.json`：整体 UI/UE token、组件、布局和交互规则。
- `navigation.json`：可复用左侧导航、折叠 rail、工作区/会话列表和菜单规则。
- `demo.html`：整体工作台预览。
- `navigation-demo.html`：导航专项预览。
- `ui-design.md`：人读版设计说明和复用检查清单。

## 来源重点

关键事实来自 `ui-theme` 的 CSS 变量、`ui-layout` 的三列 AppFrame、`ui-sidebar` 的折叠 rail 和 `ui-primitives` 的 Button/Input/Menu 模块。

## 复用提示

该方案适合 agent workbench、聊天 IDE、开发者工具和会话型生产力产品。不要将其泛化成蓝色 SaaS dashboard；DeepSeek 蓝在源码里主要是状态/气泡强调，primary action 仍然是主墨色。
