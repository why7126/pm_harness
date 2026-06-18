## Why

Sprint 001 已完成 `align-login-prototype`（23/23 任务），但 `/admin/login` 与 `user-login.png` 并排对比时，普通人仍可一眼识别差异：STONEX Logo 缺少品牌衬线气质、企业微信图标颜色/形态不对、右栏副标题金色范围不符、shadcn 默认 focus ring/ghost 按钮与原型控件形态不一致、占位交互弹出 notice 横幅破坏页面观感。根因是前序 Change 验收的是 **checklist（有无 JPG、spacing 数字）**，而非 **以 PNG 为 golden reference 的像素级 fidelity**。REQ-0001 验收项「页面视觉与原型一致」仍未真正通过，需在 Sprint 001 内做最后一轮视觉专项。

## What Changes

- 以 `user-login.png` 为 golden reference，建立可执行的视觉 diff 清单与验收 gate（并排截图 + 团队 sign-off）。
- 引入登录页品牌衬线字体（STONEX Logo 专用），对齐原型高端品牌字气质。
- 替换企业微信图标为官方绿色风格 SVG，修正当前蓝色 bubble 偏差。
- 精修右栏副标题、输入框/按钮/Checkbox 控件形态，按 `user-login.md` §3.4–§4.5  override shadcn 登录页默认态（focus ring、eye 按钮等）。
- 占位交互（语言/企微/忘记密码）改为不破坏布局的 inline/toast 或 noop，移除页面级 notice 横幅。
- 按 `user-login.md` §2 拆分 presentation 组件：`LoginFormPanel`、`LoginHeader`、`ThirdPartyLoginSection`（auth 逻辑冻结）。
- 在 `rules/ui-design.md` 补充登录页专章（从 `user-login.md` 提炼），统一规范来源。
- **不修改** auth store、hooks、API、路由守卫与表单提交逻辑；不实现企微 OAuth / i18n / 忘记密码真实流程。

## Capabilities

### New Capabilities

（无新增独立 capability。）

### Modified Capabilities

- `web-client`：管理端登录页 MUST 通过 PNG 并排视觉验收；补充字体、图标、控件形态与验收 gate 要求。

## Impact

| 影响面 | 说明 |
|---|---|
| 静态资源 | `src/web/public/icons/wecom.svg` 替换；可选 `public/fonts/` 品牌字体 |
| 前端 UI | `AuthBrandPanel`、`LoginPage`、`LoginForm` 及拆分后的 presentation 组件 |
| 样式 | `globals.css` 登录页字体 token；登录页 scoped override（仍禁止裸 Hex） |
| Auth 逻辑 | **无影响** |
| 规范文档 | `rules/ui-design.md` 登录页专章 |
| Sprint 001 | `iterations/sprint-001/sprint.md`、`acceptance-report.md` |
| Docker | Web 镜像需包含更新静态资源 |
