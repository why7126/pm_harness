---
purpose: 原型驱动 UI 验收标准
content: UI Contract、Skeleton、截图证据、computed style、Mock/API 边界和归档门禁
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-10 23:19:03
---

# 原型驱动 UI 验收标准

本标准适用于包含 `prototype/`、`prototype_refs`、UI Skeleton、Golden Reference 或明确视觉参照的 UI Change。

## UI Contract

`/req-opsx` 或等价 Change 设计阶段 SHOULD 在 `design.md` 写入 UI Contract：

| 项 | 内容 |
|---|---|
| 事实源优先级 | prototype、截图、context、acceptance、Design Token 和既有页面的冲突处理 |
| 页面与入口 | 路由、导航入口、默认落点、登录态和权限态 |
| 信息架构 | 侧边栏、顶部区、主内容、列表、表单、弹窗、空态和错误态 |
| 视觉 token | 字体、字号、颜色、边框、间距、圆角、阴影和滚动规则 |
| 交互状态 | hover、active、focus、disabled、loading、展开收起和键盘可达性 |
| Mock/API 边界 | Mock 字段、真实接口、非目标和后续接入计划 |

## Skeleton 首轮确认

带 prototype 的 UI Change SHOULD 先完成布局 Skeleton，再进入细节实现。Skeleton 至少覆盖页面壳、导航结构、主要状态容器、稳定选择器和 1440px 桌面首屏证据。

## 视觉证据

完成 UI 任务前 SHOULD 记录 1440px 桌面视口截图或等价视觉证据。关键交互包含弹窗、菜单、折叠、筛选、空态、错误态或响应式要求时，应补交互状态证据。

## 附件截图逐项对照

验收返修包含附件截图、标注图、原型截图或实际截图时，`/opsx-modify` MUST 先建立逐项视觉对照表，再修改实现。对照表必须覆盖截图编号、页面/状态、期望表现、实际表现、偏差项、检查方式、处置结论和证据入口。

如果附件无法定位页面、状态、断点或期望表现，返修应先阻断并请求补证。补证可包括更清晰截图、标注说明、浏览器视口、操作路径、原型链接或当前实现截图。

## Computed Style

对风险高或验收反馈明确指出的视觉点，SHOULD 使用浏览器 computed style、Playwright 断言或等价工具记录关键属性：字体、尺寸、间距、颜色、边框、层级、定位和交互状态。

## 归档门禁

`/opsx-archive` 前 SHOULD 复核 UI Contract、Skeleton、截图或等价视觉证据、computed style、Mock/API 边界和最终文档一致性。证据缺失时必须记录豁免原因。
