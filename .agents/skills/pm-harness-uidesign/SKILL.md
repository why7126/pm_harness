---
name: pm-harness-uidesign
description: 从真实本地项目代码库、GitHub 代码库或本地代码压缩包中高保真提炼 UI/UE 设计资产，并沉淀到 pm-harness 的 design-schemes 设计资产库。凡用户要沉淀设计方案、提取 UI 风格、拆分导航栏/侧边栏资产、生成 design.json/navigation.json/ui-design.md/demo.html，或为新项目初始化和存量项目重构复用真实项目视觉方案时必须使用。
---

# PM Harness UI Design Extraction

## 目标

把真实项目中的 UI/UE 视觉语言、导航结构和关键交互提炼为可复用、可预览、可被工程初始化消费的设计资产，而不是凭印象生成一套相似风格。

本技能面向 `pm-harness` 工程的 `design-schemes/` 本地设计资产库，产物服务两类场景：

- 新项目初始化：选用已有方案，快速建立统一设计语言。
- 存量项目重构：用真实项目沉淀出的方案作为改造目标和验收基准。

## 必读引用

在执行任何提炼、更新或校验前，完整读取：

1. `references/user-input-schema.md`
2. `references/extraction-protocol.md`

## 输入要求

按 `references/user-input-schema.md` 收集输入。用户必须提供至少一个代码事实源：本地项目代码库目录、GitHub 代码库链接或本地代码压缩包。辅助输入可以提升保真度，但不能替代代码事实源。

如果没有代码事实源，先要求用户补充，不要直接生成方案。

## 产物结构

默认沉淀到当前工程根目录的 `design-schemes/`：

```text
design-schemes/
├── registry.json
└── schemes/
    └── <scheme-id>/
        ├── meta.json
        ├── design.json
        ├── navigation.json
        ├── ui-design.md
        ├── demo.html
        ├── navigation-demo.html
        └── README.md
```

当项目没有可复用导航资产时，可以不生成 `navigation.json` 和 `navigation-demo.html`，但必须在 `meta.json` 中写明 `navigation_applicability: "not_extracted"` 及原因。

## 执行流程

1. 解析输入源，确认本地目录、GitHub 仓库或压缩包可读取。
2. 用 `rg --files` 扫描 tokens、CSS、主题、布局、组件、路由、菜单、导航和设计文档。
3. 优先读取真实源码事实源，再生成任何 JSON、Markdown 或 HTML demo。
4. 提取整体 UI/UE 到 `design.json`。
5. 当导航具有复用价值时，单独提取到 `navigation.json`。
6. 生成可直接打开的 `demo.html` 和必要的 `navigation-demo.html`。
7. 生成面向人阅读的 `ui-design.md`，说明设计定位、复用边界和不可随意替换的细节。
8. 更新 `meta.json`、scheme `README.md` 和 `design-schemes/registry.json`。
9. 校验 JSON 语法，并搜索用户强调的关键细节是否同步出现在 JSON、demo 和文档中。

## 保真规则

- 源码事实优先于截图、Figma、记忆和常见 UI 默认值。
- 不得把真实项目提炼成通用蓝白后台、通用 SaaS 卡片或占位视觉。
- unusual but intentional 的细节必须沉淀，例如侧边栏收起、版本号、用户菜单字号、chevron 字符和旋转状态。
- Demo 中修正过的细节，如果具备复用价值，必须同步检查并更新 `design.json`、`navigation.json`、`ui-design.md` 或 README。
- 不复制密钥、生产账号、客户数据、接口凭证、真实业务敏感数据。
- `inferred: false` 只用于源码事实明确的内容；推断内容必须标记为 `inferred: true` 或在字段级说明。

## TilesFST 校准经验

执行同类任务时要主动避免 TilesFST 提炼过程中暴露的问题：

- 第一版不得脱离真实项目效果。
- 导航栏和侧边栏适合独立沉淀，尤其是有展开/收起、权限过滤、持久化状态时。
- 版本号展示属于可复用导航资产。
- 用户菜单字号、邮箱字号和右侧图标都可能是方案识别点。
- 真实项目使用的 `⌃` chevron、默认 `rotate(180deg)`、展开 `rotate(0deg)` 这类 affordance 不应被替换成通用图标。
