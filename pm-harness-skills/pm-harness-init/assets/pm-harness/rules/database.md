---
purpose: 数据库设计与数据访问规范
content: 数据库选型、Schema 管理、迁移策略、表设计、通用字段、索引、Repository、查询、安全、兼容性、测试和 AI 更新规则
scope: 数据库 schema、migration、seed、ORM/Model、Repository/DAO、SQL、索引、事务、测试数据和数据库兼容
source: Harness database.md 抽象模板，基于多个项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；新增表、字段、索引、迁移、数据库类型或数据访问策略变化时更新
note: 适用于 {PRODUCT_NAME} 项目；数据库结构变更必须同步文档、迁移、模型、测试和 OpenSpec
template_scope: 可作为工程初始化时的 rules/database.md 模块
---

# 数据库规范

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如多数据库、ORM、媒体表、审计、软删除、信创数据库。

## 0. 规则定位 [通用]

`rules/database.md` 约束数据库选型、表设计、迁移、索引、查询、事务、Repository、兼容性和测试。

AI Agent 在以下场景必须读取本文件：

- 新增或修改表、字段、索引、约束、视图。
- 新增或修改 migration、DDL、seed、初始化脚本。
- 新增或修改 ORM Model、Schema、Repository、DAO。
- 修改查询、分页、排序、筛选、事务。
- 修改数据库类型、驱动、连接池、部署配置。
- 涉及媒体元数据、审计日志、软删除、租户隔离、数据权限。

初始化生成本文件时，必须根据项目实际数据库和数据访问方式替换占位符；未知项标记为 `待确认`，不得编造数据库版本、驱动或迁移工具。

常用占位符：

| 占位符 | 含义 | 归属 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | [个性化] |
| `{DATABASE_STACK}` | 主数据库、版本、驱动、ORM/DAO | [个性化] |
| `{DATABASE_SUPPORT_MATRIX}` | 多数据库兼容矩阵 | [条件启用] |
| `{MIGRATION_STRATEGY}` | 迁移策略，如 Alembic、Prisma、手写 SQL | [个性化] |
| `{SCHEMA_FILES}` | DDL/schema 文件路径 | [个性化] |
| `{MODEL_PATHS}` | ORM/Model 路径 | [条件启用] |
| `{REPOSITORY_PATTERN}` | Repository/DAO 规则 | [个性化] |
| `{CORE_TABLES}` | 核心表清单 | [个性化] |
| `{TENANCY_STRATEGY}` | 租户隔离策略 | [条件启用] |
| `{AUDIT_STRATEGY}` | 审计策略 | [条件启用] |

## 1. 数据库定位 [个性化]

当前数据库策略：

```text
{DATABASE_STACK}
```

初始化时必须明确：

- 主数据库。
- 最低版本和推荐版本。
- 驱动或 ORM。
- 连接字符串格式。
- 本地开发数据库。
- 测试数据库。
- 是否支持多数据库或信创数据库。
- 数据库结构事实源是 migration、DDL 文件、ORM schema 还是数据库 introspection。

数据库类型或迁移策略变化属于高影响变更，必须创建 OpenSpec Change。

## 2. 数据库兼容矩阵 [条件启用]

多数据库、信创或私有化项目必须启用本节。

```text
{DATABASE_SUPPORT_MATRIX}
```

推荐矩阵：

| 数据库 | 版本 | 驱动/ORM | Schema/DDL | 场景 |
|---|---|---|---|---|
| SQLite | `待确认` | `待确认` | `待确认` | 本地/轻量部署 |
| PostgreSQL | `待确认` | `待确认` | `待确认` | 生产 |
| MySQL | `待确认` | `待确认` | `待确认` | 可选 |
| 达梦 DM | `待确认` | `待确认` | `待确认` | 信创 |

规则：

- Service 层不得感知具体数据库类型。
- 数据库差异必须封装在 Repository、DAO、Dialect、Migration 或兼容层。
- 多套 DDL 或 migration 必须保持语义一致。
- 不得使用某数据库独有能力，除非提供兼容实现或明确限制支持范围。

## 3. Schema 与迁移管理 [通用 + 个性化]

迁移策略：

```text
{MIGRATION_STRATEGY}
```

Schema 文件：

```text
{SCHEMA_FILES}
```

通用流程：

1. 创建或更新 OpenSpec Change。
2. 更新 schema / migration / DDL。
3. 更新 ORM Model 或数据库访问模型。
4. 更新 Repository/DAO 和业务代码。
5. 更新 seed、fixtures、测试数据。
6. 更新 `docs/04-database-design.md`。
7. 运行 migration、回滚或初始化验证。
8. 运行集成测试和兼容性测试。

禁止行为：

- 不更新 schema/migration 就直接修改运行中数据库。
- 只改 ORM Model，不更新数据库结构事实源。
- 只改一个数据库的 DDL，遗漏声明支持的其他数据库。
- 提交运行时数据库文件代替 migration。
- 在无备份、无回滚说明的情况下做破坏性数据变更。

## 4. 表设计规则 [通用 + 个性化]

核心表清单：

```text
{CORE_TABLES}
```

表设计要求：

- 表名使用项目约定命名风格，推荐 `snake_case`。
- 表职责单一，避免万能表。
- 字段类型必须表达真实语义，不用字符串承载所有内容。
- 必填、默认值、唯一性、枚举、状态机必须明确。
- 大文本、JSON、二进制、媒体文件应说明存储边界。
- 业务状态字段必须有状态流转约束和测试。
- 删除策略必须明确：物理删除、软删除或归档。

通用业务字段建议：

```text
id
created_at
updated_at
deleted_at
created_by
updated_by
```

是否启用这些字段应根据业务生成，不得无脑添加。

## 5. 主键、时间、软删除与审计 [通用 + 条件启用]

主键规则：

- 主键类型必须全项目一致或有明确例外。
- 对外暴露 ID 时需考虑可枚举性、安全性和兼容性。
- 批量导入和跨系统同步应明确外部 ID 与内部 ID 的关系。

时间规则：

- 时间字段必须明确时区策略。
- 推荐存储 UTC 或项目统一时区，并在 API 文档中说明。
- `created_at`、`updated_at` 应由服务端或数据库统一维护。

软删除：

- 启用软删除时，查询默认过滤已删除数据。
- 唯一索引与软删除的组合必须设计清楚。
- 删除恢复、彻底清理和审计要求必须明确。

审计：

```text
{AUDIT_STRATEGY}
```

涉及管理端、权限、财务、导入导出、数据删除时，必须考虑审计日志。

## 6. 索引与约束 [通用]

索引规则：

- 常用筛选、排序、关联字段必须考虑索引。
- 唯一性必须尽量由数据库约束保证。
- 外键是否使用数据库约束必须在项目中统一。
- 多租户项目的索引应考虑 `tenant_id`。
- 大表新增索引必须评估锁表、耗时和回滚。

命名建议：

```text
idx_<table>_<fields>
uq_<table>_<fields>
fk_<from_table>_<to_table>
```

约束规则：

- 不依赖前端保证数据合法。
- 数据库约束、后端校验、API Schema 应互相一致。
- 枚举值和状态机变更必须同步代码和文档。

## 7. Repository / DAO 规范 [通用 + 个性化]

数据访问模式：

```text
{REPOSITORY_PATTERN}
```

通用要求：

- Controller/API 层不得直接访问数据库。
- Service/Use Case 层不得拼接裸 SQL。
- Repository/DAO 层负责查询和持久化，不包含业务策略。
- 复杂查询封装为具名方法，避免散落在业务代码中。
- 数据库特异 SQL 必须封装在 dialect、adapter 或特定 repository 实现中。
- 多数据库项目通过工厂、依赖注入或配置选择实现。

常见方法：

```text
get_by_id
list/filter
count
create
update
delete/soft_delete
bulk_create
exists
```

项目应根据实际语言和 ORM 生成方法命名。

## 8. 查询、分页与事务 [通用]

查询规则：

- 必须使用参数化查询或 ORM 参数绑定。
- 禁止拼接用户输入形成 SQL。
- 分页参数必须有默认值和最大值。
- 列表查询必须明确排序，避免结果不稳定。
- 批量查询避免 N+1。
- 大数据导出必须采用流式、分页或异步任务。

事务规则：

- 写操作必须明确事务边界。
- 多表写入必须考虑一致性和回滚。
- 外部服务调用与数据库事务组合时必须考虑补偿或 outbox。
- 不在长事务中执行耗时网络请求。

## 9. 安全、权限与多租户 [条件启用]

租户策略：

```text
{TENANCY_STRATEGY}
```

规则：

- 后端必须从可信上下文获取用户、租户和权限。
- 查询必须包含必要的数据权限条件。
- 管理端、普通用户端、内部任务的数据访问边界必须区分。
- 敏感字段应考虑加密、脱敏、隐藏或单独授权。
- SQL 错误不得直接暴露给用户。

## 10. 媒体、文件与对象存储元数据 [条件启用]

涉及文件、图片、音频、视频、文档或对象存储时启用本节。

媒体/文件元数据建议：

```text
file_id / media_id
storage_type
bucket_name
object_key
mime_type
file_size
checksum
width
height
duration
cover_object_key
created_at
created_by
```

规则：

- 数据库存储元数据，不直接存储大文件本体。
- 对象 key、bucket、URL 有效期必须与对象存储规则一致。
- 删除数据库记录和删除对象存储文件的顺序、补偿和幂等必须明确。
- 文件权限必须可通过数据库元数据判断。

## 11. Seed、Fixtures 与测试数据库 [通用]

seed 数据：

- 不含真实用户信息。
- 说明用途、执行方式、是否幂等。
- 修改 seed 必须同步文档和测试。

fixtures：

- 只使用脱敏或假数据。
- 不依赖真实外部服务。
- 测试执行后不污染开发数据库。

测试数据库：

- 单元测试优先隔离、可重复、可回滚。
- 集成测试必须说明依赖的数据库类型和初始化方式。
- 多数据库项目应有兼容性测试矩阵。

## 12. 数据库变更文档 [通用]

数据库结构变化必须同步：

```text
docs/04-database-design.md
openspec/changes/<change-id>/specs/**/spec.md
tests/integration/
tests/fixtures/
data/README.md（如涉及数据资产）
rules/data-management.md（如涉及数据边界）
```

高风险变更还应补充：

- 迁移步骤。
- 回滚步骤。
- 数据备份要求。
- 兼容性影响。
- 预计耗时和停机影响。

## 13. 数据库类型专项规则 [条件启用]

### SQLite

- 适合本地开发、演示、小规模或单机部署。
- 必须使用参数化查询。
- 注意并发写入限制。
- 运行时 `.db`、`.sqlite` 文件不得提交。
- migration 必须有版本记录或幂等策略。

### PostgreSQL

- 注意 schema、extension、JSONB、时区、索引和事务隔离级别。
- 使用连接池，避免泄漏连接。
- 大表 migration 需评估锁表风险。

### MySQL / MariaDB

- 注意字符集、排序规则、时区、JSON、索引长度和事务引擎。
- 必须明确 `utf8mb4` 等字符集策略。

### 信创数据库

- 达梦、人大金仓等数据库必须有单独兼容说明。
- 差异 SQL 必须封装，不得散落在 Service 层。
- 不能未验证就声称兼容。

## 14. AI 更新规则 [通用]

AI 修改数据库相关内容时必须说明：

- 修改了哪些表、字段、索引、约束。
- 是否影响 API、前端、导入导出、对象存储或权限。
- 是否需要 migration、seed、fixtures。
- 是否影响已有数据和回滚。
- 是否涉及多数据库兼容。
- 执行了哪些数据库验证和测试。

AI 不得：

- 直接修改运行时数据库替代代码变更。
- 提交运行时数据库文件。
- 忽略迁移和回滚。
- 用真实数据构造测试。
- 在业务代码中拼接用户输入 SQL。

## 15. 完成任务后检查清单 [通用 + 条件启用]

```text
□ 是否创建或更新 OpenSpec Change
□ 是否更新 schema / migration / DDL
□ 是否更新 ORM Model / Schema / Repository / DAO
□ 是否更新 docs/04-database-design.md
□ 是否更新 seed、fixtures、测试数据
□ 是否补充数据库测试或集成测试
□ 是否考虑索引、约束、分页、排序和 N+1
□ 是否明确事务边界和回滚策略
□ 是否确认未提交运行时数据库文件
□ 多数据库项目：是否同步所有数据库实现
□ 媒体/文件项目：是否同步元数据与对象存储策略
□ 权限/租户项目：是否校验数据访问边界
```

## 16. 初始化生成建议 [通用]

工程初始化工具生成 `rules/database.md` 时应：

1. 保留 [通用] 模块。
2. 用用户输入替换 [个性化] 占位符。
3. 根据数据库选型保留或删除 [条件启用] 模块。
4. 单数据库项目只生成该数据库规则，多数据库项目生成兼容矩阵。
5. 根据信创数据库要求生成专项规则。
6. 根据后端技术栈生成 ORM/Repository/DAO 规则。
7. 根据文件上传、媒体、对象存储能力生成元数据规则。
8. 未知版本、驱动、迁移工具标记为 `待确认`。
9. 保持 database.md 与 api.md、coding.md、data-management.md、compatibility.md、testing.md、environment.md 一致。
