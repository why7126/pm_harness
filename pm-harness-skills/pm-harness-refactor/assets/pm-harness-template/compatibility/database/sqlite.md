---
purpose: SQLite 数据库兼容适配说明
content: SQLite 定位、适用场景、版本与驱动、连接配置、Schema 差异、类型映射、迁移策略、并发限制、测试矩阵和初始化生成规则
source: Harness compatibility/database/sqlite.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；SQLite 版本、驱动、ORM、部署方式、迁移策略或数据库兼容目标变化时更新；后续由 AI 辅助更新并经人工 Review
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {DATABASE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/database/sqlite.md 模块
---

# SQLite 适配说明

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 中 SQLite 的使用边界、适配规则、兼容差异和测试要求。

本文重点回答：

- SQLite 在当前项目中用于本地开发、测试、轻量部署、桌面端还是生产环境。
- SQLite 数据库文件、连接参数、迁移脚本和初始化数据如何管理。
- SQLite 与 PostgreSQL、MySQL、达梦、海量等数据库之间有哪些类型、SQL、事务和约束差异。
- 使用 SQLite 时需要避免哪些并发、锁、文件权限和数据安全问题。
- 工程初始化时如何根据用户输入生成项目专属 SQLite 适配说明。

相关文档：

- 数据库规范：`rules/database.md`
- 数据库设计：`docs/04-database-design.md`
- 迁移规范：`compatibility/database/migration-rules.md`
- 数据库测试矩阵：`compatibility/database/test-matrix.md`
- 数据治理：`rules/data-management.md`
- 安全规范：`rules/security.md`
- 环境规范：`rules/environment.md`

## 1. 初始化生成参数 `[个性化]`

工程初始化生成本文时，应优先使用用户输入和自动派生配置填充以下参数。缺失信息必须标记为 `待确认`，不得编造 SQLite 版本、驱动或生产策略。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{DATABASE_OWNER}` | 数据库负责人或维护角色 | 待确认 |
| `{DB_PRIMARY}` | 主关系型数据库 | SQLite |
| `{DATABASE_STACK}` | 数据库技术栈 | SQLite + SQLAlchemy |
| `{SQLITE_VERSION}` | SQLite 版本 | 待确认 |
| `{SQLITE_DRIVER}` | SQLite 驱动 | sqlite3 / aiosqlite / better-sqlite3 |
| `{ORM_STACK}` | ORM 或 DAO 技术栈 | SQLAlchemy / Prisma / Drizzle / 手写 SQL |
| `{SQLITE_USAGE_SCOPE}` | SQLite 使用范围 | local / test / desktop / edge / production |
| `{SQLITE_DATABASE_PATH}` | 数据库文件路径 | `data/{PRODUCT_CODE}.db` |
| `{SQLITE_TEST_DATABASE_PATH}` | 测试数据库路径 | `data/test.db` / in-memory |
| `{MIGRATION_TOOL}` | 迁移工具 | Alembic / Prisma / 手写 SQL |
| `{MIGRATION_DIR}` | 迁移目录 | `src/backend/migrations` |
| `{BACKUP_POLICY}` | 备份策略 | 文件备份 / 快照 / 不适用 |
| `{CONCURRENCY_MODEL}` | 并发模型 | 单进程 / 多进程 / 多实例 |
| `{DEPLOYMENT_STACK}` | 部署方式 | docker-compose / 桌面端 / 离线包 |
| `{XINCHUANG_DATABASES}` | 兼容数据库目标 | 无 / 达梦 / 海量 / PostgreSQL |
| `{DATA_VOLUME_LEVEL}` | 数据规模 | small / medium / large / 待确认 |

## 2. SQLite 使用定位 `[通用 + 个性化]`

当前 SQLite 使用范围：

```text
{SQLITE_USAGE_SCOPE}
```

当前 SQLite 技术栈：

```text
{DATABASE_STACK}
```

推荐定位：

| 场景 | 是否推荐 | 说明 |
|---|---|---|
| 本地开发 | 推荐 | 零依赖、启动快、适合个人开发 |
| 自动化测试 | 推荐 | 可使用临时文件或内存库，便于隔离 |
| 桌面端/单机应用 | 推荐 | 数据随应用本地存储 |
| 轻量私有化部署 | 条件推荐 | 低并发、小数据量、明确备份策略时可用 |
| 多实例服务端生产 | 谨慎 | 需要评估锁、备份、文件系统和并发写入 |
| 高并发写入 | 不推荐 | 应考虑 PostgreSQL、MySQL 或项目指定生产库 |

初始化生成规则：

- 当用户选择主数据库为 `SQLite` 时，本文作为主数据库适配说明保留。
- 当 SQLite 仅用于测试或本地开发时，本文必须明确生产数据库另行适配。
- 当项目同时选择信创数据库或 PostgreSQL/MySQL 时，本文必须记录 SQLite 与兼容目标的差异。

## 3. 版本、驱动与连接配置 `[通用 + 个性化]`

| 项 | 当前配置 | 说明 |
|---|---|---|
| SQLite 版本 | `{SQLITE_VERSION}` | 需记录开发、测试、部署环境实际版本 |
| 驱动 | `{SQLITE_DRIVER}` | 与后端语言和 ORM 保持一致 |
| ORM / DAO | `{ORM_STACK}` | 与 `rules/database.md` 一致 |
| 数据库文件 | `{SQLITE_DATABASE_PATH}` | 运行时文件不得提交 Git |
| 测试数据库 | `{SQLITE_TEST_DATABASE_PATH}` | 推荐独立文件或内存库 |
| 迁移工具 | `{MIGRATION_TOOL}` | 与迁移规范一致 |

连接配置建议：

```text
{SQLITE_CONNECTION_CONFIG}
```

通用要求：

- 数据库文件必须位于项目约定的数据目录，例如 `data/`、用户数据目录或部署卷。
- 运行时 `.db`、`.sqlite`、`.sqlite3`、WAL、SHM 文件不得提交到 Git。
- 连接字符串、文件路径和测试库路径应通过环境变量或配置文件管理。
- 桌面端或离线部署场景必须记录数据库文件备份和迁移位置。

## 4. 文件、目录与备份 `[通用 + 个性化]`

推荐目录：

```text
data/
  .gitkeep
  README.md
```

推荐忽略：

```gitignore
*.db
*.sqlite
*.sqlite3
*.db-wal
*.db-shm
*.sqlite-wal
*.sqlite-shm
```

备份策略：

```text
{BACKUP_POLICY}
```

规则：

- 备份必须复制数据库主文件及其 WAL/SHM 相关文件，或在安全检查点后执行。
- 生产或准生产使用 SQLite 时，必须明确备份频率、保留周期、恢复演练和存储位置。
- 文件权限必须限制为应用运行账号可读写，不得暴露到静态资源目录。
- 如果数据库文件含个人信息、业务敏感数据或认证信息，必须纳入安全和数据治理范围。

## 5. Schema 与类型映射 `[通用 + 个性化]`

SQLite 使用动态类型系统，项目必须用应用层校验、ORM Schema、迁移脚本和测试共同保证数据一致性。

推荐类型映射：

| 语义类型 | SQLite 类型 | 应用层类型 | 说明 |
|---|---|---|---|
| 主键 ID | `{SQLITE_ID_TYPE}` | `{APP_ID_TYPE}` | 自增整数、UUID 字符串或项目统一 ID |
| 文本 | `TEXT` | `string` | 必须设置长度或业务校验 |
| 整数 | `INTEGER` | `int` | 注意布尔值通常以 0/1 存储 |
| 小数 | `NUMERIC` / `TEXT` | `Decimal` | 金额类字段不得使用浮点误差不可控方案 |
| 布尔 | `INTEGER` | `boolean` | 约定 `0=false`、`1=true` |
| 时间 | `TEXT` / `INTEGER` | `datetime` | 明确 ISO 8601、Unix timestamp 或统一格式 |
| JSON | `TEXT` | `object` | 必须由应用层或 JSON 函数校验 |
| 二进制 | `BLOB` | `bytes` | 大文件不建议入库 |

规则：

- 字段语义必须写入 `docs/04-database-design.md`。
- 金额、计量、排序权重等精度敏感字段必须明确存储策略。
- 时间字段必须记录时区和序列化格式。
- JSON 字段必须有结构说明，不得承载未建模的核心业务数据。
- 大文件、媒体、模型文件和导入导出文件应进入对象存储或文件目录，数据库只保存元数据。

## 6. 约束、索引与外键 `[通用]`

SQLite 适配规则：

- 必须显式启用外键约束，除非项目明确不使用数据库外键。
- 唯一性、非空、默认值、枚举约束必须同时在数据库和应用层验证。
- 索引命名与 `rules/database.md` 保持一致。
- 大表新增索引前必须评估锁表和执行时间。
- 使用软删除时，唯一约束必须考虑 `deleted_at` 或替代策略。

推荐连接初始化：

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = {SQLITE_BUSY_TIMEOUT_MS};
```

是否启用 WAL、busy timeout、synchronous 等配置必须根据部署和并发模型确认，不得无说明地硬编码。

## 7. SQL 与方言兼容 `[通用 + 条件启用]`

当项目需要从 SQLite 迁移到其他数据库，或同时支持多数据库时，必须避免滥用 SQLite 独有行为。

兼容差异：

| 能力 | SQLite 特点 | 兼容风险 | 处理策略 |
|---|---|---|---|
| 类型系统 | 动态类型 | 与强类型数据库行为不同 | 应用层和测试补强 |
| 布尔值 | 通常为 0/1 | 与 BOOLEAN 类型映射不同 | 统一 ORM 映射 |
| 时间 | 无原生 datetime 类型 | 排序和时区风险 | 统一序列化格式 |
| JSON | 依赖 JSON1 扩展 | 部署环境能力不一 | 测试验证或应用层处理 |
| ALTER TABLE | 能力有限 | 复杂迁移需重建表 | 使用迁移工具封装 |
| 并发写 | 单写多读 | 高并发写入受限 | 控制写入模型或更换数据库 |
| 全文搜索 | FTS 扩展 | 与其他数据库差异大 | 抽象搜索能力 |

规则：

- Repository/DAO 层不得散落数据库方言判断。
- 多数据库差异必须封装在适配层或迁移层。
- 分页、排序、大小写匹配、模糊搜索和 NULL 排序必须有兼容测试。
- 如果 SQLite 只是本地测试库，测试不得掩盖生产库方言差异。

## 8. 事务、锁与并发 `[通用 + 个性化]`

当前并发模型：

```text
{CONCURRENCY_MODEL}
```

SQLite 并发规则：

- 适合读多写少、单进程或低并发写入。
- 多进程、多线程、多实例写入必须谨慎评估锁竞争。
- 长事务会阻塞写入，应缩短事务范围。
- 批量导入、批量更新、索引创建和数据修复必须在维护窗口或低峰执行。
- API 请求内不得持有长时间数据库事务等待外部服务。

需要高并发写入、复杂权限隔离、跨服务共享数据库或严格在线扩容时，应评估迁移到项目指定生产数据库。

## 9. 迁移与初始化 `[通用 + 个性化]`

迁移工具：

```text
{MIGRATION_TOOL}
```

迁移目录：

```text
{MIGRATION_DIR}
```

初始化流程：

1. 创建数据库文件所在目录。
2. 确认数据库文件不存在或版本可升级。
3. 执行所有 migration。
4. 执行必要 seed。
5. 验证表、索引、约束、默认值和外键。
6. 执行 smoke test。

SQLite 迁移注意事项：

- 复杂字段类型变更、删除字段、修改约束时，可能需要创建新表、复制数据、替换旧表。
- 数据修复 migration 必须可验证，且不得依赖未排序查询结果。
- SQLite 文件升级前必须备份。
- 已发布版本不得重写历史 migration，除非项目明确处于初始化阶段。
- 迁移规则必须与 `compatibility/database/migration-rules.md` 一致。

## 10. 测试矩阵 `[通用 + 个性化]`

每次涉及 SQLite 的数据库变更必须至少验证：

| 验证项 | 要求 | 状态 |
|---|---|---|
| 空库初始化 | 从零创建 SQLite 数据库并完成迁移 | 待确认 |
| 旧库升级 | 从上一版本 SQLite 数据库升级 | 待确认 |
| 外键约束 | 外键启用且约束行为符合预期 | 待确认 |
| 索引与查询 | 分页、筛选、排序、模糊搜索通过 | 待确认 |
| 数据类型 | 布尔、时间、小数、JSON 映射正确 | 待确认 |
| 事务回滚 | 失败时事务可回滚 | 待确认 |
| 并发写入 | 符合项目并发模型 | 条件启用 |
| 备份恢复 | 可从备份恢复并继续迁移 | 条件启用 |
| 多数据库一致性 | 与声明支持的数据库语义一致 | 条件启用 |

推荐命令：

```bash
{SQLITE_MIGRATION_TEST_COMMAND}
{DATABASE_TEST_COMMAND}
{COMPATIBILITY_TEST_COMMAND}
```

测试结果应同步到 `compatibility/database/test-matrix.md`。

## 11. 安全与数据治理 `[通用 + 条件启用]`

SQLite 数据文件可能直接包含完整业务数据，因此必须按数据文件治理。

规则：

- 数据库文件、备份文件、导出文件不得提交 Git。
- 测试库不得包含生产敏感数据，除非完成脱敏。
- 含账号、Token、密钥、个人信息、商业数据的 SQLite 文件不得通过公开渠道分发。
- 桌面端或离线包使用 SQLite 时，必须明确本地数据存储位置、清理策略和用户数据导出/删除机制。
- 需要加密 SQLite 文件时，必须记录加密方案、密钥管理和恢复策略。

## 12. 生产使用准入 `[条件启用]`

当 `{SQLITE_USAGE_SCOPE}` 包含 production、私有化轻量部署或桌面端正式数据时，必须完成以下准入：

| 准入项 | 要求 | 状态 |
|---|---|---|
| 数据规模 | 预估数据量和增长速度可接受 | 待确认 |
| 并发模型 | 写入并发可控 | 待确认 |
| 文件系统 | 持久卷、权限和锁行为可靠 | 待确认 |
| 备份恢复 | 已演练备份和恢复 | 待确认 |
| 迁移演练 | 已验证版本升级路径 | 待确认 |
| 监控告警 | 文件大小、磁盘、错误日志可观察 | 待确认 |
| 替代方案 | 高并发或规模增长时有迁移路径 | 待确认 |

如无法满足准入要求，应将 SQLite 限定为 local/test/desktop 单机场景，并选择其他数据库作为服务端生产库。

## 13. AI Agent 更新规则 `[通用]`

AI Agent 在处理 SQLite 相关变更时必须：

- 先读取 `rules/database.md`、`docs/04-database-design.md`、本文和 `compatibility/database/migration-rules.md`。
- 确认 SQLite 是主库、测试库、开发库还是兼容库。
- 识别当前 `{SQLITE_DRIVER}`、`{ORM_STACK}`、`{MIGRATION_TOOL}` 和 `{SQLITE_DATABASE_PATH}`。
- 同步更新迁移、Model、Repository、API Schema、测试和文档。
- 对无法确认的 SQLite 版本、扩展能力、生产备份策略标记 `待确认`。
- 不得把运行时数据库文件、备份文件或测试生成文件提交为模板资产。
- 不得使用来源项目的业务表、数据路径、生产命令或执行记录污染新项目模板。

## 14. 初始化生成规则 `[通用]`

作为工程初始化模块使用时：

- **默认保留**：文档定位、使用定位、版本驱动、文件治理、类型映射、约束索引、SQL 兼容、事务并发、迁移初始化、测试矩阵、安全治理、AI 更新规则。
- **根据输入生成**：产品名称、数据库栈、SQLite 版本、驱动、ORM、文件路径、迁移工具、部署范围、并发模型、备份策略、测试命令。
- **条件启用**：生产准入、多数据库兼容、桌面端/离线部署、数据库加密、备份恢复、多实例并发、信创数据库差异。
- **不得沿用来源项目内容**：业务表名、真实数据路径、真实数据库文件、生产备份位置、执行结果、来源项目特有部署命令。

生成完成后，本文必须与以下文件保持一致：

- `rules/database.md`
- `docs/04-database-design.md`
- `compatibility/database/migration-rules.md`
- `compatibility/database/test-matrix.md`
- `docker-compose.yml`
- `.gitignore`
- `{MIGRATION_DIR}` 下的实际 migration 文件
