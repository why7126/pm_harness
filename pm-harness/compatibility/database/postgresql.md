---
purpose: PostgreSQL 数据库兼容适配说明
content: PostgreSQL 使用定位、版本驱动、Schema、迁移、类型映射、事务、索引、测试矩阵和初始化生成规则
source: Harness compatibility/database/postgresql.md 抽象模板
update_method: PostgreSQL 版本、驱动、ORM、迁移策略或生产部署方式变化时更新
owner: {DATABASE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/database/postgresql.md 模块
---

# PostgreSQL 适配说明

> **[通用]** 默认保留结构；**[个性化]** 根据项目生成；**[条件启用]** 仅在支持 PostgreSQL 时保留。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 支持 PostgreSQL 时的版本、驱动、迁移、类型映射、SQL 方言、性能、安全和测试要求。

相关文档：`rules/database.md`、`docs/04-database-design.md`、`compatibility/database/migration-rules.md`、`compatibility/database/test-matrix.md`。

## 1. 初始化参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{POSTGRES_VERSION}` | PostgreSQL 版本 | 待确认 |
| `{POSTGRES_DRIVER}` | 驱动 | psycopg / asyncpg / JDBC |
| `{ORM_STACK}` | ORM/DAO | SQLAlchemy / Prisma / Drizzle |
| `{POSTGRES_USAGE_SCOPE}` | 使用范围 | production / test / compatible |
| `{POSTGRES_CONNECTION_CONFIG}` | 连接配置 | 待确认 |
| `{MIGRATION_TOOL}` | 迁移工具 | Alembic / Flyway / Prisma |

## 2. 兼容范围 `[通用 + 个性化]`

```text
{POSTGRES_USAGE_SCOPE}
```

必须明确最低版本、推荐版本、扩展依赖、连接池、Schema 来源和生产部署方式。

## 3. 类型与方言 `[通用 + 个性化]`

| 语义 | PostgreSQL 类型 | 应用类型 | 说明 |
|---|---|---|---|
| 主键 | `{POSTGRES_ID_TYPE}` | `{APP_ID_TYPE}` | UUID / bigint |
| 时间 | `timestamptz` | datetime | 明确时区 |
| JSON | `jsonb` | object | 建索引需说明 |
| 小数 | `numeric` | Decimal | 金额优先 |
| 布尔 | `boolean` | boolean | 与 API 保持一致 |

## 4. 迁移与测试 `[通用]`

- 所有 Schema 变更必须进入 migration。
- JSON、全文搜索、数组、枚举、扩展能力必须有兼容测试。
- 索引、锁表、长事务、大表迁移必须评估执行耗时和回滚。

推荐命令：

```bash
{POSTGRES_TEST_COMMAND}
```

## 5. 初始化生成规则 `[通用]`

启用 PostgreSQL 时保留本文；未启用时删除或标记为不适用。不得保留来源项目数据库名、账号、密码、生产地址或测试结果。
