# TilesFST / STONEX 设计资产

本方案将 TilesFST 拆分为可独立复用的设计资产：

- `design.json`：整体 STONEX 工业暗色旗舰 UI/UX 语言。
- `navigation.json`：Web 后台可折叠侧边栏，以及小程序自定义顶部/底部导航。
- `ui-design.md`：面向人阅读的 UI/UE 复用指南。

当前版本提取自本地真实 TilesFST 项目，来源路径已脱敏：

```text
local-source-redacted:tilesfst
```

此前的占位方案已被替换。真实项目不是通用蓝白后台，而是使用暗色工业石材色盘、品牌金强调色、近直角圆角、半透明暗色表面，并且 Web 与小程序拥有相互独立的导航系统。

## 预览

- 打开 `demo.html` 查看整体 UI/UX 风格。
- 打开 `navigation-demo.html` 查看导航模式。
- 在新项目或重构项目中应用该方案前，先阅读 `ui-design.md`。

## 来源重点

- 设计系统：`src/shared/design-system/tokens/`
- Web CSS 变量：`src/web/src/styles/globals.css`
- Web 后台外壳：`src/web/src/features/admin/styles/admin-home.css`
- Web 导航：`src/web/src/features/admin/components/AdminSidebar.tsx`
- Web 菜单数据：`src/web/src/features/admin/data/admin-nav.ts`
- 小程序自定义导航：`src/miniapp/components/custom-navigation/`
- 小程序 tabbar：`src/miniapp/custom-tab-bar/`

## 复用注意事项

1. 保留暗色旗舰色盘：`#18160F`、`#211E16`、`#100F0A`、`#EDE8DF`、`#C8A055`。
2. 保留工业化圆角系统：徽标 `1px`，控件 `2px`，卡片 `3px`。
3. 保留 Web 后台侧边栏行为：展开 `264px`，收起 `72px`，通过 `admin-sidebar-collapsed` 持久化。
4. 保留侧边栏用户菜单的交互暗示：真实项目使用 `⌃` 字符，默认旋转 `180deg`，展开时为 `0deg`，不要替换成通用图标。
5. 将小程序顶部导航和 tabbar 视为独立于 Web 后台侧边栏的导航资产。
