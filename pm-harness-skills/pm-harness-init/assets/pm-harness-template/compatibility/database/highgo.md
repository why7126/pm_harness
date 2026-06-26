---
purpose: 海量 HighGo 数据库兼容适配说明
content: 海量数据库使用定位、版本驱动、信创适配、Schema、迁移、类型映射、SQL 差异、测试矩阵和初始化生成规则
source: Harness compatibility/database/highgo.md 抽象模板
update_method: 海量版本、驱动、部署环境、迁移策略或信创要求变化时更新
owner: {DATABASE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/database/highgo.md 模块
---

# 海量 HighGo 适配说明

> **[通用]** 默认保留结构；**[个性化]** 根据项目生成；**[条件启用]** 仅在信创数据库包含海量时保留。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 适配海量 HighGo 数据库时的驱动、方言、迁移、类型映射、部署和兼容测试要求。

## 1. 初始化参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{HIGHGO_VERSION}` | 海量版本 | 待确认 |
| `{HIGHGO_DRIVER}` | 驱动 | 待确认 |
| `{HIGHGO_DIALECT}` | ORM 方言 | 待确认 |
| `{XINCHUANG_REQUIREMENTS}` | 信创要求 | 待确认 |
| `{HIGHGO_DEPLOYMENT_ENV}` | 部署环境 | 待确认 |

## 2. 适配重点 `[通用 + 个性化]`

- 与 PostgreSQL 兼容的能力也必须实际验证，不能默认等同。
- SQL、DDL、分页、序列、时间、布尔、JSON、索引和事务行为必须进入测试矩阵。
- 方言差异应封装在 Repository、Dialect 或 migration 层。

## 3. 迁移与测试 `[通用]`

```bash
{HIGHGO_TEST_COMMAND}
```

必须覆盖初始化、迁移、CRUD、事务、分页排序、约束、索引、数据修复和回滚/补偿。

## 4. 初始化生成规则 `[通用]`

信创数据库选择海量时保留本文；未选择时删除或标记为不适用。不得编造厂商版本、客户环境、认证结果或测试通过记录。
