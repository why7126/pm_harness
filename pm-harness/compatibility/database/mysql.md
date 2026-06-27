---
purpose: MySQL 数据库兼容适配说明
content: MySQL 使用定位、版本驱动、字符集、Schema、迁移、类型映射、事务、索引、测试矩阵和初始化生成规则
source: Harness compatibility/database/mysql.md 抽象模板
update_method: MySQL 版本、驱动、字符集、ORM、迁移策略或部署方式变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {DATABASE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/database/mysql.md 模块
---

# MySQL 适配说明

> **[通用]** 默认保留结构；**[个性化]** 根据项目生成；**[条件启用]** 仅在支持 MySQL 时保留。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 支持 MySQL 时的版本、驱动、字符集、排序规则、迁移、类型映射、事务和测试要求。

## 1. 初始化参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{MYSQL_VERSION}` | MySQL 版本 | 待确认 |
| `{MYSQL_DRIVER}` | 驱动 | PyMySQL / mysqlclient / JDBC |
| `{MYSQL_CHARSET}` | 字符集 | utf8mb4 |
| `{MYSQL_COLLATION}` | 排序规则 | 待确认 |
| `{ORM_STACK}` | ORM/DAO | 待确认 |
| `{MIGRATION_TOOL}` | 迁移工具 | 待确认 |

## 2. 兼容重点 `[通用 + 个性化]`

- 字符集必须支持中文、emoji 和特殊符号。
- 时间字段、布尔字段、JSON 字段、小数字段必须有应用层映射测试。
- 分页、大小写匹配、排序规则、NULL 排序必须与其他数据库兼容验证。
- 大表 DDL、索引创建、字段类型变更必须评估锁表风险。

## 3. 类型映射 `[通用]`

| 语义 | MySQL 类型 | 说明 |
|---|---|---|
| 主键 | `{MYSQL_ID_TYPE}` | bigint / char(36) |
| 时间 | `datetime` / `timestamp` | 明确时区策略 |
| JSON | `json` | 注意版本支持 |
| 小数 | `decimal` | 金额优先 |
| 布尔 | `tinyint(1)` | 统一映射 |

## 4. 测试 `[通用]`

```bash
{MYSQL_TEST_COMMAND}
```

必须覆盖空库初始化、旧库升级、CRUD、事务、分页、排序、字符集、JSON 和回滚/补偿。

## 5. 初始化生成规则 `[通用]`

启用 MySQL 时保留本文；未启用时删除或标记为不适用。不得保留来源项目连接串、账号、密码或测试结果。
