---
purpose: MinIO 对象存储兼容适配说明
content: MinIO 适用范围、版本与部署、Bucket 策略、对象 Key、S3 兼容能力、上传下载、签名 URL、安全权限、生命周期、备份迁移、测试矩阵和初始化生成规则
source: Harness compatibility/object-storage/minio.md 抽象模板，基于项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；对象存储启用状态、MinIO 版本、部署方式、Bucket 策略、上传下载、签名 URL 或生命周期策略变化时更新；后续由 AI 辅助更新并经人工 Review
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {OBJECT_STORAGE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/object-storage/minio.md 独立模块
---

# MinIO 适配说明

> 模块标记说明：
>
> - **[通用]**：适用于大多数使用 MinIO 或 S3 兼容对象存储的 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入、资源类型、部署方式和安全策略生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应场景时才保留或展开，例如上传下载、媒体预览、分片上传、私有化部署、多租户、CDN、备份迁移。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 使用 MinIO 作为对象存储时的兼容范围、部署配置、Bucket 策略、对象 Key 规范、上传下载方式、签名 URL、安全权限、生命周期、备份迁移和测试要求。

本文重点回答：

- MinIO 在当前项目中用于本地开发、测试、私有化部署还是生产对象存储。
- Bucket、对象 Key、元数据、签名 URL 和访问权限如何设计。
- MinIO 与 S3 兼容存储、云厂商对象存储之间有哪些行为差异。
- 上传下载、图片/音视频、导入导出、模型文件和临时文件如何治理。
- 工程初始化时如何根据用户输入生成项目专属 MinIO 适配说明。

相关文档：

- 对象存储规范：`rules/object-storage.md`
- 媒体规范：`rules/media.md`
- 数据治理：`rules/data-management.md`
- 安全规范：`rules/security.md`
- API 规范：`rules/api.md`
- 兼容性规范：`rules/compatibility.md`
- 对象存储策略：`docs/07-object-storage-strategy.md`
- Docker 编排：`docker-compose.yml`

## 1. 初始化生成参数 `[个性化]`

工程初始化生成本文时，应优先使用用户输入和自动派生配置填充以下参数。缺失信息必须标记为 `待确认`，不得编造 MinIO 版本、Endpoint、Bucket、密钥或测试结果。

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码，建议 kebab-case | 待确认 |
| `{OBJECT_STORAGE_OWNER}` | 对象存储负责人或维护角色 | 待确认 |
| `{OBJECT_STORAGE_ENABLED}` | 是否启用对象存储 | true / false |
| `{OBJECT_STORAGE_STACK}` | 对象存储技术栈 | MinIO / S3-compatible |
| `{MINIO_USAGE_SCOPE}` | MinIO 使用范围 | local / test / private / production |
| `{MINIO_VERSION}` | MinIO 版本 | 待确认 |
| `{MINIO_ENDPOINT}` | MinIO Endpoint | 待确认 |
| `{MINIO_CONSOLE_ENDPOINT}` | MinIO Console 地址 | 待确认 |
| `{MINIO_REGION}` | Region | `us-east-1` / 待确认 |
| `{MINIO_BUCKET}` | 默认 Bucket | `{PRODUCT_CODE}` |
| `{BUCKET_POLICY}` | Bucket 策略 | 单 Bucket + 前缀 / 多 Bucket / 租户隔离 |
| `{OBJECT_KEY_PREFIXES}` | 对象 Key 前缀 | images/ documents/ exports/ tmp/ |
| `{MEDIA_TYPES}` | 存储资源类型 | 图片 / 视频 / 文档 / 导入导出 |
| `{SIGNED_URL_POLICY}` | 签名 URL 策略 | 私有读写 + 短期 URL |
| `{UPLOAD_STRATEGY}` | 上传策略 | 后端中转 / 预签名直传 / 分片上传 |
| `{DOWNLOAD_STRATEGY}` | 下载策略 | 后端代理 / 签名 URL / CDN |
| `{LIFECYCLE_POLICY}` | 生命周期策略 | 临时文件 7 天清理 |
| `{BACKUP_POLICY}` | 备份策略 | mc mirror / 快照 / 待确认 |
| `{OBJECT_STORAGE_TEST_COMMAND}` | 对象存储测试命令 | 待确认 |

## 2. MinIO 使用定位 `[通用 + 个性化]`

当前 MinIO 使用范围：

```text
{MINIO_USAGE_SCOPE}
```

当前对象存储技术栈：

```text
{OBJECT_STORAGE_STACK}
```

推荐定位：

| 场景 | 是否推荐 | 说明 |
|---|---|---|
| 本地开发 | 推荐 | 可通过 docker-compose 快速启动，便于上传下载联调 |
| 自动化测试 | 推荐 | 可用容器或测试实例隔离数据 |
| 私有化部署 | 推荐 | 适合作为 S3 兼容对象存储 |
| 云上生产 | 条件推荐 | 需评估高可用、备份、监控、运维能力 |
| 大规模跨地域对象存储 | 谨慎 | 需评估云厂商对象存储、CDN 和容灾方案 |

如果 `{OBJECT_STORAGE_ENABLED}=false`，本文应简化为“未启用 MinIO”，并删除强制 Bucket、Endpoint、SDK 和测试要求。

## 3. 版本、Endpoint 与环境配置 `[通用 + 个性化]`

| 项 | 当前配置 | 说明 |
|---|---|---|
| MinIO 版本 | `{MINIO_VERSION}` | 开发、测试、生产需记录实际版本 |
| API Endpoint | `{MINIO_ENDPOINT}` | 后端访问地址 |
| Console Endpoint | `{MINIO_CONSOLE_ENDPOINT}` | 管理控制台地址 |
| Region | `{MINIO_REGION}` | S3 SDK 通常需要 |
| 默认 Bucket | `{MINIO_BUCKET}` | 不得沿用来源项目 Bucket |
| 使用范围 | `{MINIO_USAGE_SCOPE}` | local/test/private/production |

推荐环境变量：

```ini
OBJECT_STORAGE_TYPE=minio
MINIO_ENDPOINT={MINIO_ENDPOINT}
MINIO_REGION={MINIO_REGION}
MINIO_ACCESS_KEY=CHANGE_ME
MINIO_SECRET_KEY=CHANGE_ME
MINIO_BUCKET={MINIO_BUCKET}
MINIO_SECURE=true
SIGNED_URL_TTL_SECONDS={SIGNED_URL_TTL_SECONDS}
```

规则：

- Access Key、Secret Key、Root Password 不得提交 Git。
- 示例配置只能使用占位值，不得出现真实密钥。
- 开发、测试、生产必须使用不同 Bucket、前缀或实例隔离。
- 生产环境必须启用 TLS 或通过受控内网/网关访问。

## 4. 部署模式与高可用 `[通用 + 条件启用]`

部署模式：

```text
{MINIO_DEPLOYMENT_MODE}
```

| 模式 | 场景 | 要求 |
|---|---|---|
| 单节点容器 | 本地开发/测试 | 数据卷隔离，便于清理 |
| 单节点持久化 | 小规模私有化 | 备份、监控、磁盘告警必须明确 |
| 分布式 MinIO | 生产/高可用 | 多磁盘、多节点、纠删码、监控 |
| 外部托管 MinIO | 客户环境 | 需记录 Endpoint、权限和运维边界 |

规则：

- 本地开发可以使用 docker-compose，但生产不得默认复用开发配置。
- 生产使用 MinIO 时必须明确数据卷、备份、恢复、监控和容量扩展策略。
- 多实例应用不得依赖本地文件系统替代 MinIO。

## 5. Bucket 与环境隔离 `[通用 + 个性化]`

Bucket 策略：

```text
{BUCKET_POLICY}
```

推荐默认：

```text
bucket: {MINIO_BUCKET}
```

环境隔离建议：

| 环境 | Bucket / Prefix | 说明 |
|---|---|---|
| local | `{PRODUCT_CODE}-local` | 本地开发 |
| test | `{PRODUCT_CODE}-test` | 自动化测试 |
| staging | `{PRODUCT_CODE}-staging` | 预发验证 |
| production | `{PRODUCT_CODE}-prod` | 生产数据 |

规则：

- 开发、测试、生产不得共享同一命名空间。
- 默认使用私有 Bucket。
- 公开读 Bucket 必须有明确业务理由、审核流程和安全边界。
- 多租户项目必须明确按 Bucket、Prefix 或元数据权限隔离。

## 6. 对象 Key 与资源前缀 `[通用 + 个性化]`

对象 Key 前缀：

```text
{OBJECT_KEY_PREFIXES}
```

推荐前缀：

| 前缀 | 资源类型 | 生命周期 | 是否条件启用 |
|---|---|---|---|
| `images/` | 图片 | 长期/业务删除 | 按需 |
| `videos/` | 视频源文件 | 长期/业务删除 | 按需 |
| `videos/covers/` | 视频封面 | 跟随视频 | 按需 |
| `documents/` | 文档附件 | 跟随业务对象 | 按需 |
| `imports/` | 导入文件 | 短期/审计保留 | 按需 |
| `exports/` | 导出文件 | 短期清理 | 按需 |
| `tmp/` | 临时文件 | 自动清理 | 按需 |
| `processed/` | 处理产物 | 跟随原始资源 | 按需 |
| `models/` | 模型文件 | 版本化管理 | 条件启用 |

推荐 Key 结构：

```text
{prefix}/{business_type}/{business_id}/{object_id}/original.{ext}
{prefix}/{business_type}/{business_id}/{object_id}/{variant}.{ext}
tmp/{upload_session_id}/{part_id}
exports/{job_id}/{file_id}.{ext}
```

规则：

- Key 必须由服务端生成。
- 不直接使用用户上传的原始文件名。
- Key 中不得包含手机号、邮箱、身份证、Token、密钥、真实姓名等敏感信息。
- 扩展名必须来自服务端校验结果，而不是用户输入。
- 删除业务对象时必须定义对象保留、软删除或清理策略。

## 7. 上传、下载与签名 URL `[通用 + 个性化]`

上传策略：

```text
{UPLOAD_STRATEGY}
```

下载策略：

```text
{DOWNLOAD_STRATEGY}
```

签名 URL 策略：

```text
{SIGNED_URL_POLICY}
```

规则：

- 默认私有读写，前端访问通过后端代理或短期签名 URL。
- 预签名上传必须由后端校验权限、文件类型、大小和业务归属后签发。
- 签名 URL 必须设置有效期，不得长期有效。
- 上传完成后必须由后端确认对象存在、大小、MIME、checksum 和业务状态。
- 下载必须区分权限不足、对象不存在、URL 过期和对象存储不可用。
- 大文件或弱网场景应考虑分片上传、重试、断点续传或后台任务。

## 8. S3 兼容能力与差异 `[通用 + 条件启用]`

MinIO 提供 S3 兼容接口，但项目仍需验证实际使用能力。

| 能力 | 是否使用 | 兼容风险 | 验证要求 |
|---|---|---|---|
| PutObject/GetObject | 必选 | 基础能力 | 必测 |
| Presigned URL | 条件启用 | URL、Header、过期策略差异 | 必测 |
| Multipart Upload | 条件启用 | 分片大小、失败清理 | 条件启用 |
| Bucket Policy | 条件启用 | 公开读/私有策略差异 | 条件启用 |
| Object Metadata | 条件启用 | Header 大小与保留字段 | 条件启用 |
| Lifecycle | 条件启用 | MinIO/云厂商支持差异 | 条件启用 |
| Versioning | 条件启用 | 存储成本和删除语义 | 条件启用 |
| SSE 加密 | 条件启用 | 密钥管理和兼容性 | 条件启用 |

规则：

- 不得假设所有 S3 SDK 高级能力在目标环境都可用。
- 若项目未来需要迁移到 S3/COS/OSS/OBS，应避免业务层依赖 MinIO 专有行为。
- 存储差异必须封装在 Storage Adapter 中。

## 9. 元数据、数据库与状态机 `[通用 + 个性化]`

MinIO 保存文件本体，数据库保存元数据和业务关系。

推荐元数据：

| 字段 | 说明 |
|---|---|
| `id` | 文件或媒体 ID |
| `bucket` | Bucket 名称 |
| `object_key` | 对象 Key |
| `resource_type` | 图片、视频、文档、导入、导出等 |
| `business_type` | 关联业务类型 |
| `business_id` | 关联业务对象 |
| `mime_type` | MIME 类型 |
| `file_size` | 文件大小 |
| `checksum` | 文件摘要 |
| `status` | 上传中、可用、处理中、失败、删除 |
| `created_by` | 上传人 |
| `created_at` | 创建时间 |

规则：

- 数据库不得只保存裸 URL，必须保存可迁移的 bucket 和 object_key。
- 对象状态必须能表达上传中、上传失败、可用、处理中、删除等生命周期。
- 对象删除、替换、转码、缩略图生成必须保持原始资源和派生资源关系可追踪。

## 10. 安全、权限与审计 `[通用]`

安全规则：

- 默认 Bucket 私有。
- MinIO 管理控制台不得暴露到公网，除非有明确的认证、网络隔离和审计。
- 应用使用最小权限账号，不得使用 root 账号作为业务访问凭证。
- 密钥必须通过环境变量、密钥管理或部署平台注入。
- 上传文件必须校验大小、MIME、扩展名、文件头和业务权限。
- 下载、预览、复制、删除必须校验登录态和业务权限。
- 管理操作、删除对象、批量导出、公开访问变更必须记录审计日志。

## 11. 生命周期、清理与成本 `[通用 + 条件启用]`

生命周期策略：

```text
{LIFECYCLE_POLICY}
```

建议：

| 对象类型 | 清理策略 | 说明 |
|---|---|---|
| `tmp/` | 短期自动清理 | 上传会话、处理中间文件 |
| `exports/` | 过期清理 | 导出结果短期可下载 |
| `imports/` | 按审计要求保留 | 导入源文件可能需追溯 |
| `processed/` | 跟随原始文件 | 缩略图、转码产物 |
| `models/` | 版本化保留 | 本地模型启用时 |

规则：

- 清理任务必须与数据库元数据状态一致。
- 不能只删除对象而不更新数据库状态。
- 生产环境需监控 Bucket 容量、对象数量、错误率和清理任务结果。

## 12. 备份、恢复与迁移 `[通用 + 条件启用]`

备份策略：

```text
{BACKUP_POLICY}
```

规则：

- 生产 MinIO 必须有备份和恢复演练。
- 备份必须覆盖对象内容、Bucket 策略、生命周期配置和必要元数据。
- 数据库元数据与对象存储内容必须能一致恢复。
- 迁移到其他 S3 兼容存储时，必须验证对象 Key、签名 URL、权限策略和元数据。

推荐迁移检查：

| 检查项 | 要求 | 状态 |
|---|---|---|
| 对象数量 | 源和目标一致 | 待确认 |
| 对象大小 | 源和目标一致 | 待确认 |
| checksum | 抽样或全量一致 | 待确认 |
| 元数据 | Content-Type、Metadata 保留 | 待确认 |
| 访问权限 | 私有/公开策略符合预期 | 待确认 |
| 业务验证 | 预览、下载、删除可用 | 待确认 |

## 13. 兼容测试矩阵 `[通用 + 个性化]`

推荐测试矩阵：

| 测试域 | local MinIO | test MinIO | private/prod MinIO | S3-compatible 替代 | 状态 |
|---|---|---|---|---|---|
| 连接健康检查 | 必测 | 必测 | 必测 | 条件启用 | 待确认 |
| Bucket 初始化 | 必测 | 必测 | 条件启用 | 条件启用 | 待确认 |
| 上传文件 | 必测 | 必测 | 必测 | 条件启用 | 待确认 |
| 下载文件 | 必测 | 必测 | 必测 | 条件启用 | 待确认 |
| 删除文件 | 必测 | 必测 | 必测 | 条件启用 | 待确认 |
| 签名 URL | 条件启用 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 上传限制 | 必测 | 必测 | 必测 | 条件启用 | 待确认 |
| 权限隔离 | 必测 | 必测 | 必测 | 条件启用 | 待确认 |
| 大文件/分片 | 条件启用 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 生命周期清理 | 条件启用 | 条件启用 | 条件启用 | 条件启用 | 待确认 |
| 备份恢复 | 条件启用 | 条件启用 | 必测 | 条件启用 | 待确认 |

推荐命令：

```bash
{OBJECT_STORAGE_TEST_COMMAND}
{MEDIA_TEST_COMMAND}
{COMPATIBILITY_TEST_COMMAND}
```

测试结果不得在模板中伪造，未验证项必须保留 `待确认`。

## 14. 故障处理与降级 `[通用 + 个性化]`

常见故障：

| 故障 | 用户表现 | 系统处理 | 运维处理 |
|---|---|---|---|
| MinIO 不可用 | 上传/下载失败 | 返回明确错误，可重试 | 检查服务和磁盘 |
| Bucket 不存在 | 上传失败 | 阻止写入并报警 | 初始化 Bucket |
| 签名 URL 过期 | 下载失败 | 重新申请 URL | 检查 TTL |
| 权限不足 | 403 | 提示无权限 | 检查策略和账号 |
| 磁盘满 | 上传失败 | 阻止上传并报警 | 扩容或清理 |
| 元数据不一致 | 文件不可访问 | 标记异常并修复 | 对账任务 |

降级策略：

```text
{OBJECT_STORAGE_FALLBACK_POLICY}
```

若文件能力是核心路径，必须优先恢复对象存储，不得静默丢弃上传内容。

## 15. AI Agent 更新规则 `[通用]`

AI Agent 在处理 MinIO 或对象存储变更时必须：

- 先读取 `rules/object-storage.md`、`rules/media.md`、本文和 `docs/07-object-storage-strategy.md`。
- 确认 `{OBJECT_STORAGE_ENABLED}`、`{OBJECT_STORAGE_STACK}`、`{MINIO_BUCKET}`、`{UPLOAD_STRATEGY}` 和测试命令。
- 涉及上传、下载、预览、删除、签名 URL、Bucket、Key、生命周期时，必须同步更新本文和相关 API/测试文档。
- 对无法确认的 Endpoint、版本、Bucket、凭证、测试结果标记 `待确认`。
- 不得写入真实密钥、真实 Bucket、真实生产 Endpoint 或伪造测试通过记录。
- 不得让业务代码直接依赖 MinIO SDK 细节，除非项目明确不需要存储适配层。

## 16. 初始化生成规则 `[通用]`

作为工程初始化模块使用时：

- **默认保留**：文档定位、使用定位、版本配置、部署模式、Bucket 策略、Key 规范、上传下载、S3 兼容、安全权限、生命周期、测试矩阵、AI 更新规则。
- **根据输入生成**：产品名称、对象存储启用状态、资源类型、MinIO 版本、Endpoint、Bucket、前缀、上传下载策略、签名 URL、生命周期、测试命令。
- **条件启用**：分片上传、媒体预览、CDN、公开读、多租户、备份恢复、生产高可用、S3 兼容迁移、本地模型文件。
- **不得沿用来源项目内容**：业务资源名、真实 Bucket、真实 Endpoint、真实密钥、生产备份路径、来源项目特定前缀和测试结果。

生成完成后，本文必须与以下文件保持一致：

- `rules/object-storage.md`
- `rules/media.md`
- `docs/07-object-storage-strategy.md`
- `docs/05-compatibility-matrix.md`
- `docker-compose.yml`
- `rules/environment.md`
- 对象存储 Adapter、API、测试和环境变量配置
