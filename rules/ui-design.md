---
purpose: UI 设计规范
content: Design Token、组件复用、Prototype 驱动验收和视觉证据要求
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-10 23:19:03
---

# UI 设计规范

## 基本原则

- UI 任务必须先确认产品形态、目标用户和品牌方向。
- 管理端/运营工具强调效率、扫描、筛选、表格、表单和重复操作。
- 官网/展示端强调首屏识别、内容层级、视觉资产和转化路径。
- 新增或修改 UI SHOULD 使用 semantic token，避免散落硬编码颜色。

## Prototype-driven UI Gate

当 Change 包含 `prototype/`、`prototype_refs`、Golden Reference、UI Skeleton 或明确视觉参照时，MUST 追加读取 `docs/standards/prototype-ui-acceptance.md`。

实现与归档阶段 SHOULD 记录：

```text
□ UI Contract 是否明确事实源优先级、页面入口、信息架构、视觉 token、交互状态和 Mock/API 边界
□ 是否完成 Skeleton 首轮确认或说明豁免原因
□ 是否记录 1440px 桌面首屏截图或等价视觉证据
□ 是否对高风险差异记录 computed style 或等价断言
□ 是否回填最终文档一致性和验收结论
```

证据 stale、Mock/API 边界未声明、原型差异未解释时，不应归档 UI Change。

## UI 返修附件截图对照

UI 型 `/opsx-modify` 若验收反馈包含附件截图、标注图、原型截图或实际截图，MUST 在返修前建立逐项视觉对照表。对照表至少包含：

| 字段 | 要求 |
|---|---|
| 截图编号 | 能对应用户附件或验收证据 |
| 页面/状态 | 路由、弹窗、列表、空态、交互状态或响应式断点 |
| 期望表现 | 来自原型、截图标注、验收标准或用户反馈 |
| 实际表现 | 当前实现或截图中可观察结果 |
| 偏差项 | 尺寸、颜色、间距、层级、文案、状态、交互或数据边界 |
| 检查方式 | 目视、Playwright、computed style、DOM 断言或用户补证 |
| 处置结论 | 修复、无需修复、超出范围或需补证 |
| 证据入口 | 截图、日志、测试、Change trace 或验收记录的脱敏引用 |

对照表证据不足时先补证，不得直接返修。返修完成后 SHOULD 复验对应截图项，并在 Change `tasks.md` 或 `trace.md` 记录结果。
