# DeepSeek Harness Web Client UI/UE

## 设计定位

DeepSeek Harness 是面向 AI Agent 工作流的 Web 客户端外壳。它不是营销页，也不是传统指标后台，而是一个安静、紧凑、持续使用的对话工作台：左侧管理工作区和会话，中间承载会话流与 composer，右侧可承载详情面板。

## 适用边界

适用于 AI 工作台、开发者工具、会话管理、任务执行、工具调用审计、代码助手或需要长期驻留的生产力产品。

不适合电商、内容运营后台、品牌展示官网、重装饰数据大屏，或需要强烈营销视觉冲击的首屏。

## 核心视觉规则

- 主背景保持 `rgb(255,255,255)`，模块背景使用轻微 bluish neutral，例如 `rgb(245,246,247)` 与 `rgb(249,250,251)`。
- DeepSeek 蓝 `rgb(65,118,230)` 是业务状态和响应气泡强调，不要把整个界面做成蓝色主题。
- 大部分容器是 flat hairline surface，阴影主要留给 menu、popover 和 overlay。
- 文字以黑色主墨色和 bluish gray 层级区分，避免大面积彩色文字。
- 深色模式存在，但方案默认识别点是浅色 near-white 工作台。

## Typography

正文使用系统字体栈：Apple / Segoe UI / PingFang SC / Microsoft YaHei / Helvetica / Arial。代码块使用 SF Mono、JetBrains Mono、Fira Code、Consolas 等等宽栈。

常规 UI 文本为 `14px / 22px`，小标签和紧凑菜单为 `12px / 18px` 或 `12px / 16px`。源码注释明确 Figma 的 510 字重在 Web 中归一为 `500`。

## Layout

应用框架是三列 CSS Grid：左 sidebar、中间 conversation center、可选 details column。展开/折叠通过 `grid-template-columns` 过渡完成，细节栏的 1px 边框在收起时必须消失。

中间会话区和 composer 共享居中轴线。Transcript 比 composer 窄 32px，composer 底部 sticky，并与 todo、queue、approval、question 等 dock cards 使用同一宽度系统。

## Navigation

左侧导航是可复用核心资产。展开态是 280px 左栏，折叠态是 56px rail。rail 使用 10px 横向 padding，将 36x36 控制按钮居中。

Sidebar 展开态 padding 是 `6px 12px`，折叠态是 `18px 10px 6px`。Logo row 展开时高 60px，折叠时高 36px 并保留 12px 底部节奏。

折叠不是简单隐藏文字：源码设计为 AppFrame grid 轨道滑动，宽内容先在原位 150ms 淡出，随后 rail 布局进入。rail 上方控制从原 rail 右侧以 `translateX(49px)` 进入，使用同一 easing。

折叠 rail 中，品牌 mark 默认出现；hover 时品牌 mark 被 panel icon 替换，作为展开 affordance。这个细节不可替换成静态 hamburger。

## Components

按钮默认是胶囊形：md 高 36px、半径 18px、左右 padding 14px；sm 高 28px、半径 14px。Primary 是黑色/主墨色实心按钮，不是蓝色主按钮。

输入框高 32px、半径 8px、`1px` 语义边框，focus 时边框切到主墨色。Menu card 半径 12px、padding 4px、主菜单最小宽 218px；menu item 最小高 40px、半径 10px，紧凑菜单可降到 26px item。

Workspace rows 是导航识别点：project row 34px，session row 32px，row radius 8px，indent step 22px。Session cell 有 8px padding、16px 状态槽和 4px title gap；hover 时 action 出现、time 隐去。

## Reuse Checklist

- 保留 near-white bluish neutral 背景，不要改成通用蓝白后台。
- 保留 56px collapsed rail 和 36px rail controls。
- 保留 logo hover swap 的展开 affordance。
- 保留 sidebar 滑动 + 淡出，而不是直接 display none。
- 保留 composer 与 transcript 的共享居中轴线。
- Primary action 使用主墨色，DeepSeek blue 只作语义强调。
- Menu、input、button 尺寸应按源码 token 复用。
