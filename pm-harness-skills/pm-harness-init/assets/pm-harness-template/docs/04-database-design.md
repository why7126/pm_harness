---
purpose: 数据库设计
content: 数据库选型、核心表、字段规范、迁移策略、兼容性和数据安全
source: Harness docs Token 优化模板，初始化时基于数据库栈和 schema 生成
update_method: 数据库类型、表结构、字段、索引、迁移、种子数据或兼容策略变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-07-14 00:00:00
owner: {DOCS_OWNER}
note: 本文档记录数据库摘要，具体 DDL / migration 以代码仓库为准
---

# 数据库设计

## 1. 数据库定位

| 环境 | 数据库 | 说明 |
|---|---|---|
| Local | `{LOCAL_DATABASE}` | 本地开发 |
| Test | `{TEST_DATABASE}` | 自动化测试 |
| Production | `{PRODUCTION_DATABASE}` | 生产环境 |

生产环境不得静默回退到 demo / local 数据库。

## 2. Schema 来源

| 类型 | 路径 |
|---|---|
| Schema / DDL | `{SCHEMA_PATH}` |
| Migration | `{MIGRATION_PATH}` |
| Seed | `{SEED_PATH}` |
| Fixture | `{FIXTURE_PATH}` |
| Repository / ORM | `{DATA_ACCESS_PATH}` |

## 3. 核心表清单

初始化或数据模型变更后，用真实表替换下表。

| 表 | 职责 | 关键字段 | 索引 / 约束 | 关联 Spec |
|---|---|---|---|---|
| `{table_name}` | `{purpose}` | `{fields}` | `{indexes}` | `{spec}` |

## 4. 通用字段

业务表 SHOULD 按需包含：

```text
id
created_at
updated_at
deleted_at
created_by
updated_by
tenant_id
```

是否启用软删除、审计、租户隔离、乐观锁，应由 OpenSpec 明确。

## 5. 迁移与兼容

- DB 结构变更必须有 migration、schema 或等价变更脚本。
- migration 应可重复执行或有版本记录。
- 多数据库适配写入 `compatibility/database/`。
- 高风险迁移必须有回滚说明、备份策略和验证记录。

## 6. 数据安全

- 真实用户、客户、合同、价格、密钥等敏感数据不得提交。
- 测试数据必须脱敏并放入 `tests/fixtures/` 或 `data/` 的允许区域。
- 导出、日志、错误响应不得泄露敏感字段。

## 7. 变更同步清单

数据库变更必须同步：

```text
□ openspec/changes/<change-id>/specs/
□ docs/04-database-design.md
□ rules/database.md（如规则变化）
□ schema / migration / seed / fixture
□ Repository / ORM / Schema / DTO
□ API、OpenAPI、客户端生成物（如受影响）
□ 单元、集成、迁移或回归测试
```
