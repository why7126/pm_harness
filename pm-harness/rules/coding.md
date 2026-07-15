---
purpose: 编码规范
content: 后端、前端、跨端共享、模块边界与代码质量规则
source: Harness Token 优化模板
update_method: 技术栈、代码风格、模块边界或质量门禁变化时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-14 00:00:00
note: AI 生成或修改代码必须遵守本规范
---

# 编码规范

## 1. 通用原则

- 遵循项目既有技术栈：`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`。
- 业务代码必须放在 `src/` 下对应模块，不得落到根目录、`docs/` 或 `scripts/`。
- 路由/Controller、Schema、Service、Repository、Model 等分层边界应清晰。
- 不在接口层堆复杂业务逻辑；不绕过统一数据访问、鉴权、对象存储或配置层。
- 共享类型、常量、SDK、生成代码放入 `src/shared/` 或 `src/sdk/`。

## 2. 后端

推荐结构：

```text
src/backend/app/
├── api/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
├── services/
└── main.py
```

- 数据库访问必须参数化，并通过统一数据访问层。
- 配置读取集中管理，不在业务代码硬编码环境变量默认值。
- 文件/对象存储访问必须通过适配层。

## 3. 前端与跨端

- 前端接口类型 SHOULD 由 OpenAPI 或等价契约生成。
- 页面、features、通用组件、业务组件、样式和生成代码需分层放置。
- 多端项目必须区分 Web、移动端、小程序、桌面端能力边界，不复用平台专属 API。
- 样式和组件遵守 `rules/ui-design.md`。

## 4. AI 修改输出

AI 修改代码时必须说明：

```text
□ 修改了哪些文件
□ 是否影响 API / DB / UI / 部署 / 权限
□ 是否需要更新 OpenSpec、docs、tests
□ 是否需要运行生成命令或迁移命令
□ 执行了哪些验证
```
