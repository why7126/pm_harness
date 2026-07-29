---
purpose: 数据库规范
content: 数据模型、迁移、索引、审计字段、兼容性与 AI 更新规则
source: Harness Token 优化模板
update_method: 新增表、字段、索引、迁移或数据库适配策略变化时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-14 00:00:00
note: 数据库变更必须同步 docs/04-database-design.md、迁移和测试
---

# 数据库规范

## 1. 数据库定位

项目数据库栈由 `{DATABASE_STACK}` 决定。初始化后必须在 `docs/04-database-design.md` 中明确本地、测试、生产使用的数据库类型和连接方式。

生产环境不得静默回退到演示或本地数据库；连接串和凭据必须通过环境变量或密钥系统注入。

## 2. 表设计要求

- 表名、字段名、索引名使用统一命名风格。
- 业务表 SHOULD 包含 `id`、`created_at`、`updated_at`，按需包含 `deleted_at`、`created_by`、`updated_by`。
- 常用筛选、排序、唯一约束必须建立索引或约束。
- 软删除、审计、租户隔离、多语言等横切字段需在 OpenSpec 中说明。

## 3. 迁移规则

- DB 结构变更必须有 migration、schema 或等价变更脚本。
- migration 应可重复执行或有版本记录。
- 禁止在业务代码中拼接未参数化 SQL。
- 多数据库适配必须把差异写入 `compatibility/database/`。

## 4. AI 更新清单

AI 修改数据库结构时必须同步：

```text
□ docs/04-database-design.md
□ schema / migration / seed / fixture
□ Pydantic / DTO / ORM / Repository
□ API、OpenAPI、前端生成物（如受影响）
□ 单元、集成、回归或迁移测试
□ 回滚说明（高风险变更）
```
