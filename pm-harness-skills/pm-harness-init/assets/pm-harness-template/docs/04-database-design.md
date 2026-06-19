---
purpose: 数据库设计
content: 数据库选型、Schema 来源、表清单、字段规范、关系约束、索引、迁移、种子数据、数据安全和维护规则
source: Harness docs/04-database-design.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；Schema、迁移、ORM、Seed、数据对象或存储策略变化时更新；后续由 AI 辅助更新并经人工 Review
owner: {DATABASE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 docs/04-database-design.md 模块
---

# 数据库设计

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如认证用户、审计日志、对象存储元数据、媒体、租户、多数据库兼容。

## 0. 文档定位 `[通用]`

本文是 `{PRODUCT_NAME}` 的数据库设计入口，用于说明结构化数据如何建模、存储、迁移、初始化、测试和维护。

本文重点回答：

- 项目使用什么数据库和迁移方式。
- Schema、ORM/Model、Repository/DAO、Seed 的事实来源在哪里。
- 核心业务对象如何映射到表、字段、关系和索引。
- 哪些数据放数据库，哪些放对象存储、`data/` 或 `models/`。
- Schema 变更时需要同步哪些代码、文档、测试和 OpenSpec。

相关规则：

- 数据库强制规则：`rules/database.md`
- 数据治理：`rules/data-management.md`
- API 对应关系：`docs/03-api-index.md`
- 架构关系：`docs/01-architecture.md`
- 对象存储：`rules/object-storage.md`
- 测试要求：`rules/testing.md`

## 1. 生成参数 `[个性化]`

初始化生成本文时，应优先使用用户输入填充以下参数。缺失信息可以标记为 `待确认`，不得编造数据库事实。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{DATABASE_STACK}` | 数据库技术栈 | 待确认 |
| `{MIGRATION_STRATEGY}` | 迁移策略或工具 | 待确认 |
| `{SCHEMA_SOURCE}` | Schema 事实来源 | 待确认 |
| `{ORM_STACK}` | ORM / Model 技术栈 | 待确认 |
| `{REPOSITORY_PATTERN}` | Repository / DAO 模式 | 待确认 |
| `{CORE_DATA_OBJECTS}` | 核心数据对象 | 待确认 |
| `{AUTH_STRATEGY}` | 认证与用户模型策略 | 待确认 |
| `{AUDIT_POLICY}` | 审计日志策略 | 待确认 |
| `{OBJECT_STORAGE_STACK}` | 对象存储方案 | 待确认 |
| `{MEDIA_ENABLED}` | 是否启用媒体资产 | 待确认 |
| `{TENANCY_MODEL}` | 租户模型 | 待确认 |
| `{DATABASE_OWNER}` | 数据库文档负责人 | 待确认 |

## 2. 数据库概述 `[通用 + 个性化]`

| 项 | 说明 |
|---|---|
| 数据库 | `{DATABASE_STACK}` |
| Schema 来源 | `{SCHEMA_SOURCE}` |
| 迁移策略 | `{MIGRATION_STRATEGY}` |
| ORM / Model | `{ORM_STACK}` |
| Repository / DAO | `{REPOSITORY_PATTERN}` |
| 本地数据目录 | `{LOCAL_DATABASE_PATH}` |
| 测试数据库 | `{TEST_DATABASE_STRATEGY}` |
| 备份策略 | `{DATABASE_BACKUP_POLICY}` |
| 回滚策略 | `{DATABASE_ROLLBACK_POLICY}` |

设计原则：

- 结构化业务数据放数据库。
- 文件二进制、媒体文件、模型文件、大体积导入导出文件不直接放数据库，优先放对象存储、文件服务或外部存储，数据库只保存元数据和引用。
- 运行时数据库文件、真实客户数据和敏感数据不得提交到 Git。
- Schema 变更必须有迁移、测试、回滚或兼容说明。

## 3. 数据对象与 ER 关系 `[通用 + 个性化]`

初始化时应根据 `{CORE_DATA_OBJECTS}` 生成真实 ER 关系。

```text
{ER_DIAGRAM}
```

ER 编写要求：

- 每个核心业务对象必须能追踪到产品场景或需求。
- 外键、唯一约束、软删除、状态字段、审计字段必须明确。
- 多对多关系应说明中间表职责。
- 如果暂未确认业务表，应写 `业务表待需求明确后填充`，不得保留来源项目业务表。

## 4. 表清单 `[通用 + 个性化]`

| 表 | 类型 | 状态 | 说明 | 关联对象 | 关联 API/功能 |
|---|---|---|---|---|---|
| `{TABLE_NAME_1}` | `{TABLE_TYPE_1}` | `{TABLE_STATUS_1}` | `{TABLE_DESCRIPTION_1}` | `{DATA_OBJECT_1}` | `{RELATED_API_OR_FEATURE_1}` |
| `{TABLE_NAME_2}` | `{TABLE_TYPE_2}` | `{TABLE_STATUS_2}` | `{TABLE_DESCRIPTION_2}` | `{DATA_OBJECT_2}` | `{RELATED_API_OR_FEATURE_2}` |

表类型建议：

- `core`：核心业务表。
- `auth`：认证与权限表。
- `audit`：审计、日志、追踪表。
- `metadata`：文件、媒体、对象存储、模型等元数据表。
- `join`：多对多关系表。
- `config`：业务配置表。
- `temporary`：临时表，不建议长期保留。

## 5. 通用字段规范 `[通用]`

除非项目另有约定，业务表建议包含以下字段：

| 字段 | 用途 | 说明 |
|---|---|---|
| `id` | 主键 | UUID、雪花 ID、自增 ID 或数据库原生 ID，需统一 |
| `created_at` | 创建时间 | 使用统一时区和格式 |
| `updated_at` | 更新时间 | 更新时同步 |
| `deleted_at` | 软删除时间 | 启用软删除时使用 |
| `created_by` | 创建人 | 启用审计时使用 |
| `updated_by` | 更新人 | 启用审计时使用 |
| `version` | 乐观锁 | 并发更新场景使用 |
| `status` | 状态 | 必须有枚举说明 |
| `tenant_id` | 租户隔离 | 多租户场景使用 |

字段命名、类型、时间、枚举、JSON 字段、索引必须与 `rules/database.md` 和 `rules/language.md` 一致。

## 6. 表结构模板 `[通用]`

每张表应按以下结构维护。

### 6.1 `{TABLE_NAME}` `[个性化]`

用途：

```text
{TABLE_PURPOSE}
```

关联能力：

```text
{RELATED_CAPABILITY_OR_REQ}
```

| 字段 | 类型 | 约束 | 默认值 | 说明 | 敏感级别 |
|---|---|---|---|---|---|
| `{FIELD_NAME_1}` | `{FIELD_TYPE_1}` | `{FIELD_CONSTRAINT_1}` | `{FIELD_DEFAULT_1}` | `{FIELD_DESCRIPTION_1}` | `{SENSITIVITY_1}` |
| `{FIELD_NAME_2}` | `{FIELD_TYPE_2}` | `{FIELD_CONSTRAINT_2}` | `{FIELD_DEFAULT_2}` | `{FIELD_DESCRIPTION_2}` | `{SENSITIVITY_2}` |

索引：

| 索引 | 字段 | 类型 | 用途 |
|---|---|---|---|
| `{INDEX_NAME_1}` | `{INDEX_FIELDS_1}` | `{INDEX_TYPE_1}` | `{INDEX_PURPOSE_1}` |

约束：

| 约束 | 字段 | 规则 |
|---|---|---|
| `{CONSTRAINT_NAME_1}` | `{CONSTRAINT_FIELDS_1}` | `{CONSTRAINT_RULE_1}` |

生命周期：

```text
{TABLE_LIFECYCLE}
```

## 7. 认证与用户模型 `[条件启用]`

当 `{AUTH_STRATEGY}` 启用账号、用户、角色、权限或会话时保留本节。

### 7.1 用户表模板

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `id` | `{USER_ID_TYPE}` | PK | 用户 ID |
| `username` | `{USERNAME_TYPE}` | `{USERNAME_CONSTRAINT}` | 登录名或账号 |
| `email` | `{EMAIL_TYPE}` | `{EMAIL_CONSTRAINT}` | 邮箱，按项目启用 |
| `phone` | `{PHONE_TYPE}` | `{PHONE_CONSTRAINT}` | 手机号，按项目启用 |
| `password_hash` | `{PASSWORD_HASH_TYPE}` | `{PASSWORD_HASH_CONSTRAINT}` | 密码哈希，非密码明文 |
| `display_name` | `{DISPLAY_NAME_TYPE}` | `{DISPLAY_NAME_CONSTRAINT}` | 显示名称 |
| `role` | `{ROLE_TYPE}` | `{ROLE_CONSTRAINT}` | 角色或主角色 |
| `status` | `{STATUS_TYPE}` | `{STATUS_CONSTRAINT}` | 用户状态 |
| `last_login_at` | `{TIMESTAMP_TYPE}` | NULL | 最近登录时间 |
| `created_at` | `{TIMESTAMP_TYPE}` | NOT NULL | 创建时间 |
| `updated_at` | `{TIMESTAMP_TYPE}` | NOT NULL | 更新时间 |

角色、权限和状态必须与 `rules/security.md`、`docs/03-api-index.md` 保持一致。

### 7.2 登录/审计日志模板

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `id` | `{LOG_ID_TYPE}` | PK | 日志 ID |
| `user_id` | `{USER_ID_TYPE}` | FK/NULL | 用户 ID，失败时可为空 |
| `login_identifier` | `{IDENTIFIER_TYPE}` | NOT NULL | 脱敏登录标识 |
| `result` | `{LOGIN_RESULT_TYPE}` | CHECK | 登录结果 |
| `failure_reason` | `{FAILURE_REASON_TYPE}` | NULL | 失败原因 |
| `ip` | `{IP_TYPE}` | NULL | 客户端 IP |
| `user_agent` | `{USER_AGENT_TYPE}` | NULL | User-Agent |
| `created_at` | `{TIMESTAMP_TYPE}` | NOT NULL | 创建时间 |

日志表必须避免存储明文密码、完整 token、敏感密钥或未脱敏个人信息。

## 8. 业务表设计 `[个性化]`

初始化时根据产品需求生成真实业务表。若需求尚未明确，保留以下提示：

```text
业务表待需求明确后填充。
```

业务表生成要求：

- 表名、字段名必须符合项目命名规则。
- 每个业务表必须说明对应产品场景和需求。
- 状态字段必须有枚举说明。
- 金额、数量、时间、地理位置、文件引用等字段必须明确单位和格式。
- 涉及个人信息、客户数据、商业数据时必须标注敏感级别和脱敏策略。

## 9. 媒体、文件与对象存储元数据 `[条件启用]`

当项目启用文件上传、媒体、对象存储或导入导出时保留本节。

建议使用元数据表保存对象存储引用，二进制文件不直接入库。

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | `{MEDIA_ID_TYPE}` | 媒体或文件 ID |
| `owner_type` | `{OWNER_TYPE}` | 关联对象类型 |
| `owner_id` | `{OWNER_ID_TYPE}` | 关联对象 ID |
| `media_type` | `{MEDIA_TYPE}` | image / video / audio / document / archive 等 |
| `bucket_name` | `{BUCKET_NAME_TYPE}` | bucket 或容器 |
| `object_key` | `{OBJECT_KEY_TYPE}` | 对象 key |
| `mime_type` | `{MIME_TYPE}` | MIME 类型 |
| `file_size` | `{FILE_SIZE_TYPE}` | 文件大小 |
| `checksum` | `{CHECKSUM_TYPE}` | 校验和 |
| `metadata` | `{JSON_TYPE}` | 扩展元数据 |
| `created_at` | `{TIMESTAMP_TYPE}` | 创建时间 |

如启用视频、图片处理或转码，可增加：

- `width`
- `height`
- `duration`
- `cover_object_key`
- `transcode_status`
- `variants`

必须同步 `rules/media.md`、`rules/object-storage.md`、`docs/07-object-storage-strategy.md`。

## 10. 租户、组织与权限数据 `[条件启用]`

当项目启用多租户、组织、团队、空间或客户隔离时保留本节。

| 模型 | 表 | 隔离字段 | 说明 |
|---|---|---|---|
| `{TENANT_MODEL_1}` | `{TENANT_TABLE_1}` | `{TENANT_FIELD_1}` | `{TENANT_DESCRIPTION_1}` |

多租户规则：

- 业务表必须明确是否包含 `tenant_id` 或等价隔离字段。
- API、Repository、测试必须覆盖租户隔离。
- 导出、上传、对象存储前缀、日志审计必须按租户隔离策略设计。

## 11. Seed、Fixtures 与初始化数据 `[通用 + 个性化]`

| 数据类型 | 位置 | 用途 | 是否提交 | 备注 |
|---|---|---|---|---|
| Seed | `{SEED_PATH}` | 初始化必要数据 | 是/按策略 | 不含真实密钥 |
| Fixtures | `{FIXTURE_PATH}` | 测试样例 | 是 | 必须脱敏 |
| Demo 数据 | `{DEMO_DATA_PATH}` | 演示 | 按策略 | 不得含真实客户数据 |
| Runtime 数据 | `{RUNTIME_DATA_PATH}` | 运行时生成 | 否 | 必须进入 `.gitignore` |

Seed 规则：

- 初始管理员、默认角色、系统配置等应使用安全占位或环境变量。
- 不得提交真实账号密码、真实客户数据、真实业务素材。
- 测试 fixtures 必须可重复、可清理。

## 12. 迁移策略 `[通用 + 个性化]`

当前迁移策略：

```text
{MIGRATION_STRATEGY}
```

Schema 变更流程：

1. 创建或更新需求 / OpenSpec Change。
2. 修改 Schema 来源：`{SCHEMA_SOURCE}`。
3. 修改 ORM / Model：`{ORM_MODEL_PATH}`。
4. 修改 Repository / DAO：`{REPOSITORY_PATH}`。
5. 编写迁移脚本或迁移说明：`{MIGRATION_PATH}`。
6. 更新本文和 API 文档。
7. 更新 seed、fixtures、测试。
8. 执行迁移验证和回滚验证。

迁移记录：

| 版本/Change | 变更内容 | 迁移脚本 | 回滚方式 | 状态 |
|---|---|---|---|---|
| `{MIGRATION_CHANGE_1}` | `{MIGRATION_DESCRIPTION_1}` | `{MIGRATION_SCRIPT_1}` | `{ROLLBACK_1}` | `{MIGRATION_STATUS_1}` |

## 13. 数据安全与合规 `[通用 + 个性化]`

| 数据类别 | 示例 | 敏感级别 | 存储策略 | 脱敏/加密 | 访问控制 |
|---|---|---|---|---|---|
| `{DATA_CATEGORY_1}` | `{DATA_EXAMPLE_1}` | `{SENSITIVITY_LEVEL_1}` | `{STORAGE_POLICY_1}` | `{MASK_OR_ENCRYPT_1}` | `{ACCESS_CONTROL_1}` |

要求：

- 密码必须存哈希，禁止明文存储。
- token、secret、私钥、验证码、临时凭据不得明文长期存储。
- 日志、审计、错误信息不得泄漏敏感数据。
- 导出、备份、fixtures、demo 数据必须脱敏。

## 14. 与 API 的对应 `[通用 + 个性化]`

| 表/对象 | 主要 API | 读写方式 | 说明 |
|---|---|---|---|
| `{TABLE_OR_OBJECT_1}` | `{RELATED_API_1}` | `{READ_WRITE_1}` | `{API_DB_NOTE_1}` |
| `{TABLE_OR_OBJECT_2}` | `{RELATED_API_2}` | `{READ_WRITE_2}` | `{API_DB_NOTE_2}` |

API 变更和数据库变更必须双向同步：

- API 新增字段时检查数据库、Schema、DTO、测试。
- 数据库新增字段时检查 API 是否需要暴露。
- 删除字段必须有兼容策略和迁移说明。

## 15. 测试要求 `[通用]`

数据库变更后至少检查：

| 测试类型 | 说明 |
|---|---|
| 迁移测试 | 新库、旧库升级、回滚或兼容验证 |
| Repository/DAO 测试 | 查询、写入、事务、错误处理 |
| API 集成测试 | API 与数据库字段映射 |
| 权限/租户测试 | 数据隔离和越权访问 |
| Seed/Fixture 测试 | 初始化数据可重复创建 |
| 数据安全测试 | 敏感字段不泄漏 |

测试命令以 `rules/testing.md` 和项目脚本为准。

## 16. 维护规则 `[通用]`

Schema、ORM、表结构、索引、约束或迁移变化时必须：

1. 更新 `rules/database.md` 中相关规则（如规则变化）。
2. 更新 Schema 来源、ORM/Model、Repository/DAO。
3. 更新迁移脚本或迁移说明。
4. 更新本文。
5. 更新 `docs/03-api-index.md`、`docs/01-architecture.md`、`docs/02-deployment.md`（如受影响）。
6. 更新 seed、fixtures、测试。
7. 通过 OpenSpec Change 进入开发，除非是纯文档修正。
8. 执行数据库相关验证；无法执行时说明原因和风险。

## 17. 初始化生成建议 `[通用]`

工程初始化工具生成本文时应遵循：

1. 保留所有 `[通用]` 模块。
2. 用用户输入替换所有 `[个性化]` 占位符。
3. 根据项目能力保留或删除 `[条件启用]` 模块。
4. 根据 `{DATABASE_STACK}`、`{MIGRATION_STRATEGY}`、`{ORM_STACK}`、`{REPOSITORY_PATTERN}` 生成真实数据库概述。
5. 根据 `{CORE_DATA_OBJECTS}` 生成业务表；未知时写 `业务表待需求明确后填充`。
6. 认证、审计、媒体、对象存储、租户、多数据库兼容等能力未启用时删除对应章节。
7. 不得保留来源项目业务表、字段、角色、对象存储 bucket、运行时路径或 API 路径。
8. 生成后检查本文是否能回答：
   - 数据库是什么？
   - Schema 事实来源在哪里？
   - 有哪些表和核心字段？
   - 如何迁移、初始化、测试和回滚？
   - 哪些数据不能提交到 Git？
