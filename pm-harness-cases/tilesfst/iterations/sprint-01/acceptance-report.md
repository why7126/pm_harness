---
title: Sprint 01 验收报告
purpose: 记录 Sprint 01 验收结果与遗留项
content: 基于 REQ-0001 acceptance.md 及全部登录相关 OpenSpec Change
source: AI根据迭代范围生成，Sprint 结束时由团队填写
update_method: Sprint 验收完成后更新
owner: 产品负责人
status: pending
note: 核心 Change 已实现，待团队逐项验收
---

# Sprint 01 验收报告

## 验收概况

| 字段 | 内容 |
|---|---|
| Sprint | sprint-01 |
| 关联需求 | REQ-0001 用户登录 |
| 关联 Change | 前序已归档 + **`fix-login-pixel-fidelity`（已实现，待归档）** |
| 验收日期 | 待定 |
| 验收结论 | 待定（Pending） |
| 验收人 | 待定 |

## 功能验收

> 来源：`issues/requirements/REQ-0001-user-login/acceptance.md`

### 登录页访问与展示

- [ ] 用户可通过 `/admin/login` 打开 Web 管理端登录页
- [ ] 登录页左右分屏布局（桌面端）与移动端单栏布局正确
- [ ] 页面视觉与原型一致 — **待团队 PNG sign-off**（对照 `user-login.png`）
- [ ] 登录表单元素完整（用户名、密码、记住我、忘记密码、登录按钮、企业微信、语言切换、版权）

### 表单校验与提交

- [ ] 用户名/密码为空时不能提交并展示对应提示
- [ ] 登录按钮 loading 防重复提交
- [ ] 密码显隐切换与 Enter 提交

### 登录成功与失败

- [ ] 正确凭证登录成功并跳转 `/admin/dashboard`
- [ ] 错误凭证展示「账号或密码错误」
- [ ] 禁用账号展示「账号已停用，请联系管理员」
- [ ] 记住我勾选后刷新保持登录态

### 角色与权限

- [ ] 登录返回用户 ID、显示名、角色、状态
- [ ] `admin` / `employee` 可进入管理端受保护页面
- [ ] `store_owner` 访问管理端被拒绝
- [ ] 非管理员访问管理员专属页面被拒绝

### 路由守卫

- [ ] 管理端除 login 外均为受保护路由
- [ ] 未登录跳转 `/admin/login`
- [ ] 已登录访问 login 跳转 dashboard
- [ ] Token 过期跳转 login 并提示

### 退出登录

- [ ] 顶部菜单可退出登录
- [ ] 退出后清除登录态并跳转 login
- [ ] 退出后访问受保护页跳转 login

### 占位功能

- [ ] 忘记密码、企业微信展示「功能建设中」

## Design System 验收

> 来源：`openspec/changes/add-design-system/specs/design-system/spec.md`

### Token 层

- [x] `globals.css` 定义 semantic colors（page、secondary、deep、brand-gold、border-*、error）
- [x] 圆角 token：`rounded-industrial`（2px）、`rounded-card`（3px）
- [x] 字距 token：`tracking-brand`（0.16em）
- [x] 文字色 token：`text-primary`、`text-secondary`、`text-muted`
- [x] Token 值与 `rules/ui-design.md` 色彩表一致

### shadcn/ui 基础组件

- [x] `components.json` 存在，style: new-york
- [x] Button — default 金色 CTA、outline、ghost、destructive
- [x] Input — 透明底、border-strong、focus 金色、h-16
- [x] Checkbox — 金色选中态、深色勾
- [x] Label、Separator 可用
- [x] 工业风 2px 圆角 override，无默认大圆角/shadow

### 工具与复合组件

- [x] `cn()` 工具（clsx + tailwind-merge）
- [x] Vite/TS `@/` 路径别名
- [x] `IconInput` — 左侧 icon + error slot
- [x] `DividerText` — 居中分割文案

### 预览与构建

- [x] `/design-system` 预览页可访问
- [x] 预览页展示 Button/Input/Checkbox 多状态样本
- [x] `vite build` 生产构建通过
- [x] `docker compose build web` 通过
- [x] `src/web/README.md`、`rules/ui-design.md` 已同步

## 接口验收

- [ ] `POST /api/v1/auth/login` — 成功/401/403/400 场景
- [ ] `GET /api/v1/auth/me` — 有效/无效 token
- [ ] `POST /api/v1/auth/logout` — 成功响应
- [ ] 错误码与前端提示一致

## 数据验收

- [ ] `users` 表结构正确，密码哈希存储
- [ ] 角色与状态枚举正确
- [ ] `login_logs` 表结构已预留

## 技术验收

- [ ] Pydantic Schema 校验
- [ ] auth feature 模块封装
- [ ] Orval 客户端生成，无手写 generated 代码
- [ ] `docs/03-api-index.md` 已更新
- [ ] `docs/04-database-design.md` 已更新
- [ ] 后端认证接口测试通过
- [ ] 前端登录与路由守卫测试通过
- [x] Design System 单元/smoke 测试通过（18 tests）

## UI 与交互验收

- [x] Design Token 与 `rules/ui-design.md` 一致（Design System 层）
- [ ] 登录页 UI 与原型一致 — **实现完成**（衬线 Logo、绿色企微、组件拆分、无 notice 横幅），待 PNG sign-off
- [ ] 键盘导航与 ARIA 基础可访问性

## 集成验收

- [ ] Docker Compose：种子 admin → 登录 → dashboard → 退出
- [ ] 错误账号、禁用账号、store_owner 拒绝场景验证通过
- [ ] `python scripts/validate-directory-structure.py` 通过

## OpenSpec Tasks 完成度

### add-user-login

> 来源：`openspec/changes/add-user-login/tasks.md`

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 数据库与种子 | 4 | 4 | ✓ 完成 |
| §2 后端 Security | 4 | 4 | ✓ 完成 |
| §3 后端 Auth 模块 | 6 | 6 | ✓ 完成 |
| §4 后端测试 | 4 | 4 | ✓ 完成 |
| §5 前端 Auth Feature | 8 | 8 | ✓ 完成 |
| §6 前端登录页与路由 | 8 | 8 | ✓ 完成 |
| §7 前端测试 | 3 | 3 | ✓ 完成 |
| §8 集成验证与文档 | 4 | 4 | ✓ 完成 |
| **合计** | **41** | **41** | **100%** |

### add-design-system

> 来源：`openspec/changes/add-design-system/tasks.md`

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 环境与配置 | 3 | 3 | ✓ 完成 |
| §2 Design Token | 4 | 4 | ✓ 完成 |
| §3 shadcn/ui 基础组件 | 5 | 5 | ✓ 完成 |
| §4 复合组件 | 2 | 2 | ✓ 完成 |
| §5 预览与验收 | 5 | 5 | ✓ 完成 |
| §6 文档 | 3 | 3 | ✓ 完成 |
| §7 测试 | 2 | 2 | ✓ 完成 |
| **合计** | **24** | **24** | **100%** |

### refactor-login-ui

> 来源：`openspec/changes/refactor-login-ui/tasks.md`

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 准备与基线 | 2 | 2 | ✓ 完成 |
| §2 AuthBrandPanel | 3 | 3 | ✓ 完成 |
| §3 LoginPage 容器 | 3 | 3 | ✓ 完成 |
| §4 LoginForm | 6 | 6 | ✓ 完成 |
| §5 PasswordInput | 2 | 2 | ✓ 完成 |
| §6 响应式与可访问性 | 3 | 3 | ✓ 完成 |
| §7 测试与构建 | 3 | 3 | ✓ 完成 |
| §8 文档与 Sprint | 2 | 2 | ✓ 完成 |
| **合计** | **24** | **24** | **100%** |

### align-login-prototype

> 来源：`openspec/changes/align-login-prototype/tasks.md`

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 静态资源 | 4 | 4 | ✓ 完成 |
| §2 AuthBrandPanel 高保真 | 3 | 3 | ✓ 完成 |
| §3 登录页右栏组件 | 4 | 4 | ✓ 完成 |
| §4 LoginForm 调整 | 3 | 3 | ✓ 完成 |
| §5 响应式 | 2 | 2 | ✓ 完成 |
| §6 测试与构建 | 3 | 3 | ✓ 完成 |
| §7 视觉验收与文档 | 4 | 4 | ✓ 完成 |
| **合计** | **23** | **23** | **100%** |

### fix-login-pixel-fidelity

> 来源：`openspec/changes/fix-login-pixel-fidelity/tasks.md`

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 基线与 diff 清单 | 3 | 3 | ✓ 完成 |
| §2 品牌字体 | 3 | 3 | ✓ 完成 |
| §3 静态资源与图标 | 3 | 3 | ✓ 完成 |
| §4 组件拆分与布局 | 5 | 5 | ✓ 完成 |
| §5 控件形态 override | 4 | 4 | ✓ 完成 |
| §6 规范文档 | 2 | 2 | ✓ 完成 |
| §7 测试、构建与 PNG 验收 | 6 | 6 | ✓ 完成 |
| **合计** | **26** | **26** | **100%** |

### fix-login-pixel-fidelity（续）

> 来源：`openspec/changes/archive/2026-06-13-fix-login-pixel-fidelity/tasks.md`  
> 状态：已实现，待团队 PNG 并排 sign-off

## 遗留项

| 编号 | 描述 | 优先级 | 计划处理 |
|---|---|---|---|
| L-01 | 登录页与原型视觉 sign-off | P0 | 团队并排对比 `user-login.png` |
| L-02 | `docs/03-api-index.md`、`docs/04-database-design.md` 待同步 | P1 | Sprint 验收期间补齐 |
| L-03 | `fix-login-pixel-fidelity` 待归档 | P2 | `/opsx:archive fix-login-pixel-fidelity` |

## 验收结论

- **结论**：待定
- **备注**：视觉 golden reference 为 `user-login.png`；`rebuild-login-from-html-prototype` 已取消
