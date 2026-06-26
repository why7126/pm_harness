---
purpose: 数据库迁移兼容规范
content: 数据库迁移目标、事实源、命名规则、兼容策略、风险分级、执行流程、回滚策略、验证矩阵和初始化生成规则
source: Harness compatibility/database/migration-rules.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；数据库、Schema、迁移工具、兼容目标或发布策略变化时更新；后续由 AI 辅助更新并经人工 Review
owner: {DATABASE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/database/migration-rules.md 模块
---

# 数据库迁移规范

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入、数据库技术栈和发布方式生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应场景时才保留或展开，例如多数据库、信创数据库、离线部署、租户隔离、数据归档。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 的数据库迁移兼容规则，用于约束 Schema 变更如何设计、生成、执行、验证、回滚和归档。

本文重点回答：

- 哪个文件或工具是数据库结构的事实源。
- migration 如何命名、排序、评审和执行。
- 不同数据库、不同环境、不同版本之间如何保持兼容。
- 哪些变更属于高风险迁移，必须补充回滚、备份、灰度或数据修复方案。
- 工程初始化时如何根据用户输入生成项目专属迁移规范。

相关文档：

- 数据库规范：`rules/database.md`
- 数据库设计：`docs/04-database-design.md`
- 数据库兼容矩阵：`compatibility/database/test-matrix.md`
- 数据库适配说明：`compatibility/database/{DATABASE_ADAPTER_DOC}`
- 发布规范：`rules/release.md`
- 数据治理：`rules/data-management.md`
- 测试规范：`rules/testing.md`
- OpenSpec 项目说明：`openspec/project.md`

## 1. 初始化生成参数 `[个性化]`

工程初始化生成本文时，应优先使用用户输入和自动派生配置填充以下参数。缺失信息必须标记为 `待确认`，不得编造数据库版本、迁移工具或生产策略。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{DATABASE_OWNER}` | 数据库负责人或维护角色 | 待确认 |
| `{DATABASE_STACK}` | 主数据库、版本、驱动、ORM/DAO | SQLite / PostgreSQL / MySQL / 达梦 |
| `{DB_PRIMARY}` | 主关系型数据库 | SQLite |
| `{XINCHUANG_DATABASES}` | 信创或兼容数据库目标 | 无 / 达梦 / 海量 / PostgreSQL |
| `{MIGRATION_TOOL}` | 迁移工具 | Alembic / Prisma / Flyway / Liquibase / 手写 SQL |
| `{MIGRATION_STRATEGY}` | 迁移策略 | versioned migration / repeatable migration / ORM migration |
| `{SCHEMA_SOURCE}` | Schema 事实源 | migration / ORM schema / DDL / introspection |
| `{MIGRATION_DIR}` | migration 文件目录 | `src/backend/migrations` |
| `{SEED_DIR}` | seed 或初始化数据目录 | `src/backend/seeds` |
| `{ROLLBACK_POLICY}` | 回滚策略 | down migration / restore backup / forward fix |
| `{BACKUP_POLICY}` | 备份策略 | 自动备份 / 手工备份 / 不适用 |
| `{DEPLOYMENT_STACK}` | 部署方式 | docker-compose / Kubernetes / 离线包 |
| `{ENVIRONMENTS}` | 环境清单 | local / test / staging / production |
| `{TENANCY_MODEL}` | 租户模型 | 单租户 / 多租户 / 待确认 |
| `{DATA_VOLUME_LEVEL}` | 数据规模 | small / medium / large / 待确认 |
| `{DOWNTIME_TOLERANCE}` | 停机容忍度 | 可停机 / 不可停机 / 待确认 |

## 2. 迁移事实源 `[通用 + 个性化]`

当前项目迁移事实源：

```text
{SCHEMA_SOURCE}
```

当前项目迁移工具：

```text
{MIGRATION_TOOL}
```

当前项目迁移目录：

```text
{MIGRATION_DIR}
```

通用规则：

- 数据库结构变更必须通过 migration、DDL 或项目明确指定的 Schema 事实源管理。
- 禁止只在运行中数据库手工改表而不沉淀迁移文件。
- 禁止只修改 ORM Model、实体类或类型定义而不更新 Schema 事实源。
- 禁止提交运行时数据库文件替代 migration。
- 多数据库项目必须保证同一业务变更在所有声明支持的数据库上语义一致。
- 迁移事实源发生变化时，必须同步 `rules/database.md`、`docs/04-database-design.md` 和 OpenSpec。

## 3. 迁移目录与文件命名 `[通用 + 个性化]`

推荐目录：

```text
{MIGRATION_DIR}/
  versions/
  seeds/
  scripts/
  README.md
```

当项目使用框架约定目录时，以 `{MIGRATION_TOOL}` 官方约定为准，但必须在本文记录。

### 3.1 文件命名 `[通用]`

推荐命名：

```text
YYYYMMDDHHMM_<change_slug>.<ext>
```

示例：

```text
202606250930_create_user_tables.sql
202606250945_add_tile_status_index.py
202606251020_alter_asset_metadata_columns.sql
```

命名要求：

- 文件名必须体现时间顺序和变更意图。
- `change_slug` 使用英文小写、数字和下划线，不使用空格。
- 同一变更跨多个数据库方言时，必须能从路径或文件名区分数据库类型。
- 与 OpenSpec Change 关联时，建议在注释或元数据中记录 Change ID。

### 3.2 多数据库目录 `[条件启用]`

当 `{XINCHUANG_DATABASES}` 不为 `无` 或项目声明支持多数据库时，推荐目录：

```text
{MIGRATION_DIR}/
  common/
  sqlite/
  postgresql/
  mysql/
  dm/
  highgo/
```

规则：

- `common/` 只放跨数据库语义一致且语法兼容的迁移。
- 数据库专属目录只放方言差异实现，不得改变业务语义。
- 若某数据库暂不支持某迁移，必须在迁移说明中写明限制、替代方案和影响范围。

## 4. 迁移类型与风险分级 `[通用]`

| 类型 | 示例 | 风险 | 要求 |
|---|---|---:|---|
| 新增结构 | 新表、新字段、新索引 | 低/中 | 补充测试和文档 |
| 兼容扩展 | 新增 nullable 字段、双写字段 | 中 | 说明新旧版本兼容方式 |
| 约束增强 | NOT NULL、唯一约束、外键 | 中/高 | 先清洗数据，再加约束 |
| 数据修复 | 批量补数、枚举转换 | 中/高 | 提供 dry-run、备份和校验 |
| 破坏性变更 | 删除表、删除字段、字段改类型 | 高 | 必须 OpenSpec、备份、回滚或 forward fix |
| 性能变更 | 大表索引、分区、归档 | 中/高 | 评估锁表、耗时和灰度 |
| 多数据库适配 | 方言迁移、类型映射 | 中 | 更新兼容矩阵 |

高风险迁移必须满足：

- 有 OpenSpec Change 或等价设计记录。
- 有影响范围和数据规模评估。
- 有备份、回滚或 forward fix 方案。
- 有测试环境演练记录。
- 有发布窗口、执行人、审核人和验收人。

## 5. 兼容性策略 `[通用 + 条件启用]`

### 5.1 应用版本兼容 `[通用]`

迁移必须考虑应用版本与数据库版本的兼容关系。

推荐策略：

- 扩展优先：先新增兼容字段或表，再切换应用读写逻辑，最后清理旧结构。
- 避免同一发布同时做不可逆 Schema 删除和业务代码切换。
- 灰度、滚动发布或多实例部署时，旧应用和新应用必须能在迁移窗口内共同运行。
- API、Repository、Model、DTO 和前端类型必须与迁移后的结构一致。

### 5.2 多数据库兼容 `[条件启用]`

当项目支持多个数据库时，必须维护以下映射：

| 语义 | 主数据库实现 | 兼容数据库实现 | 差异说明 | 测试状态 |
|---|---|---|---|---|
| 主键 | `{PRIMARY_KEY_PRIMARY}` | `{PRIMARY_KEY_COMPAT}` | `{PRIMARY_KEY_DIFF}` | 待确认 |
| 时间字段 | `{TIME_PRIMARY}` | `{TIME_COMPAT}` | `{TIME_DIFF}` | 待确认 |
| JSON 字段 | `{JSON_PRIMARY}` | `{JSON_COMPAT}` | `{JSON_DIFF}` | 待确认 |
| 全文搜索 | `{SEARCH_PRIMARY}` | `{SEARCH_COMPAT}` | `{SEARCH_DIFF}` | 待确认 |
| 分页 | `{PAGING_PRIMARY}` | `{PAGING_COMPAT}` | `{PAGING_DIFF}` | 待确认 |

规则：

- 不得在业务层散落数据库方言判断。
- 方言差异应封装在 migration、Repository、Dialect 或数据库适配层。
- 类型、默认值、索引、约束和事务隔离级别必须在兼容矩阵中说明。

### 5.3 离线与私有化部署 `[条件启用]`

离线或私有化项目必须补充：

- 初始化空库脚本。
- 从旧版本升级到目标版本的完整迁移路径。
- 部署包内 migration 文件完整性校验。
- 运维执行说明和失败恢复说明。
- 低权限数据库账号执行迁移时的权限清单。

## 6. 迁移开发流程 `[通用]`

数据库变更必须按以下流程处理：

1. 确认需求、Bug 或 OpenSpec Change。
2. 判断是否涉及数据库结构、数据修复、兼容目标或发布风险。
3. 新增或修改 migration。
4. 更新 ORM Model、实体、Repository、DTO、API Schema 和类型生成物。
5. 更新 seed、fixtures、测试数据和示例数据。
6. 更新 `docs/04-database-design.md`、`compatibility/database/test-matrix.md` 和相关规则文档。
7. 在本地空库执行完整初始化。
8. 在已有数据的测试库执行升级迁移。
9. 验证回滚、forward fix 或恢复方案。
10. 运行单元测试、集成测试和兼容性测试。
11. 记录执行结果、风险、审核结论和验收状态。

## 7. 迁移脚本编写规则 `[通用 + 个性化]`

### 7.1 通用脚本规则 `[通用]`

- migration 应具备确定性，同一输入状态下结果一致。
- 迁移脚本不得依赖开发者本机绝对路径。
- 迁移脚本不得写入真实密钥、真实客户数据或敏感样例。
- 批量更新必须有筛选条件和影响行数预估。
- 大表变更必须考虑分批、锁表、超时和回滚。
- 创建索引前必须确认字段、排序、过滤和查询场景。
- 修改枚举或状态字段时，必须同步业务状态机和测试。

### 7.2 数据修复规则 `[条件启用]`

数据修复 migration 必须说明：

| 项 | 内容 |
|---|---|
| 修复目标 | `{DATA_FIX_GOAL}` |
| 数据范围 | `{DATA_FIX_SCOPE}` |
| 执行方式 | `{DATA_FIX_EXECUTION}` |
| 幂等策略 | `{DATA_FIX_IDEMPOTENCY}` |
| 验证 SQL/脚本 | `{DATA_FIX_VALIDATION}` |
| 回滚或补偿 | `{DATA_FIX_ROLLBACK}` |

### 7.3 Seed 与初始化数据 `[条件启用]`

Seed 数据应与 migration 分层管理。

规则：

- 系统必需的枚举、角色、权限、配置可作为 seed。
- 演示数据、测试数据和生产初始化数据必须分目录或分环境。
- Seed 必须可重复执行或有明确幂等保护。
- 生产 seed 不得包含默认弱密码、真实个人信息或敏感密钥。

## 8. 回滚、备份与恢复 `[通用 + 个性化]`

当前备份策略：

```text
{BACKUP_POLICY}
```

当前回滚策略：

```text
{ROLLBACK_POLICY}
```

通用规则：

- 低风险新增型迁移可使用 forward fix，但必须记录原因。
- 高风险迁移必须优先提供备份恢复或反向迁移说明。
- 数据删除、字段截断、类型收窄、枚举合并等不可逆变更必须先备份。
- 回滚方案必须在测试环境演练，不能只写理论步骤。
- 无法安全回滚时，必须明确“不可回滚”，并给出补偿方案、人工处理方案和发布审批要求。

回滚说明模板：

| 项 | 内容 |
|---|---|
| 迁移文件 | `{MIGRATION_FILE}` |
| 影响对象 | `{AFFECTED_TABLES_OR_DATA}` |
| 是否可自动回滚 | `{AUTO_ROLLBACK_SUPPORTED}` |
| 回滚命令 | `{ROLLBACK_COMMAND}` |
| 备份位置 | `{BACKUP_LOCATION}` |
| 验证方式 | `{ROLLBACK_VALIDATION}` |
| 风险说明 | `{ROLLBACK_RISK}` |

## 9. 环境执行规则 `[通用 + 个性化]`

| 环境 | 是否自动执行 | 执行入口 | 数据来源 | 验收要求 |
|---|---|---|---|---|
| local | `{LOCAL_AUTO_MIGRATE}` | `{LOCAL_MIGRATION_COMMAND}` | 开发数据/空库 | 初始化成功 |
| test | `{TEST_AUTO_MIGRATE}` | `{TEST_MIGRATION_COMMAND}` | 测试库/fixtures | 自动化测试通过 |
| staging | `{STAGING_AUTO_MIGRATE}` | `{STAGING_MIGRATION_COMMAND}` | 生产近似数据 | 演练记录 |
| production | `{PROD_AUTO_MIGRATE}` | `{PROD_MIGRATION_COMMAND}` | 生产数据 | 审批、备份、验收 |

生产环境规则：

- 生产迁移必须有执行窗口和责任人。
- 生产迁移前必须确认备份状态。
- 生产迁移后必须执行 smoke test 和关键数据校验。
- 自动迁移只适用于低风险场景；高风险迁移必须人工确认。

## 10. 验证与测试矩阵 `[通用 + 个性化]`

每个 migration 至少覆盖：

| 验证项 | 要求 | 状态 |
|---|---|---|
| 空库初始化 | 从零创建数据库并完成所有迁移 | 待确认 |
| 旧库升级 | 从上一稳定版本升级到当前版本 | 待确认 |
| 幂等性 | 重复执行不会破坏数据或结构 | 待确认 |
| 回滚/补偿 | 回滚、恢复或 forward fix 可执行 | 待确认 |
| 数据完整性 | 行数、约束、枚举、关联关系正确 | 待确认 |
| 应用兼容 | API、Repository、前端类型可正常运行 | 待确认 |
| 多数据库兼容 | 声明支持的数据库均通过 | 条件启用 |
| 性能影响 | 大表迁移耗时、锁表、索引效果可接受 | 条件启用 |

推荐命令：

```bash
{MIGRATION_UP_COMMAND}
{MIGRATION_DOWN_COMMAND}
{DATABASE_TEST_COMMAND}
```

测试结果应同步到 `compatibility/database/test-matrix.md`。

## 11. 评审与发布准入 `[通用]`

数据库迁移合并前必须确认：

- 迁移文件已提交，并与业务代码同一变更关联。
- 文档、测试、Schema、Model、Repository、API 类型已同步。
- 风险等级已标注。
- 兼容数据库已验证或明确不适用。
- 高风险迁移有备份、回滚、演练和审批记录。
- 生产执行命令和验收方式明确。

禁止合并：

- 无 migration 的 Schema 变更。
- 未说明风险的破坏性变更。
- 未验证的多数据库方言变更。
- 会丢失数据但无备份或补偿方案的迁移。

## 12. AI Agent 更新规则 `[通用]`

AI Agent 在处理数据库迁移时必须：

- 先读取 `rules/database.md`、`docs/04-database-design.md` 和本文。
- 识别当前 `{MIGRATION_TOOL}`、`{SCHEMA_SOURCE}` 和 `{MIGRATION_DIR}`。
- 根据变更影响同步更新 Model、Repository、API Schema、测试和文档。
- 对无法确认的数据库版本、方言能力、生产策略标记 `待确认`。
- 不得编造已执行的生产迁移、备份结果或测试结果。
- 不得删除或重写历史 migration，除非项目明确处于未发布初始化阶段。

## 13. 初始化生成规则 `[通用]`

作为工程初始化模块使用时：

- **默认保留**：文档定位、事实源、命名规则、风险分级、开发流程、脚本规则、回滚规则、验证矩阵、评审准入、AI 更新规则。
- **根据输入生成**：数据库栈、迁移工具、迁移目录、兼容数据库、部署环境、回滚策略、测试命令。
- **条件启用**：多数据库兼容、信创数据库、离线部署、多租户、数据修复、Seed 数据、大表性能迁移。
- **不得沿用来源项目内容**：表名、字段名、业务数据、数据库版本、生产命令、备份地址、执行记录。

生成完成后，本文必须与以下文件保持一致：

- `rules/database.md`
- `docs/04-database-design.md`
- `compatibility/database/test-matrix.md`
- `openspec/project.md`
- `docker-compose.yml`
- `{MIGRATION_DIR}` 下的实际 migration 文件
