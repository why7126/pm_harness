---
purpose: 对象存储策略说明
content: 对象存储选型、桶/容器策略、目录前缀、资源类型、访问控制、生命周期、迁移、备份、测试和维护规范
source: Harness docs/07-object-storage-strategy.md 抽象模板，初始化时基于用户输入生成
update_method: 对象存储服务、桶策略、资源类型、访问控制、生命周期、备份或迁移策略变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {OBJECT_STORAGE_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；未启用对象存储时保留启用条件和替代方案说明
---

# 对象存储策略

## 0. 文档定位 `[通用]`

本文档用于定义项目中对象存储的整体策略，包括服务选型、桶或容器划分、对象 key 命名、资源前缀、访问控制、生命周期、迁移备份、成本治理、测试验收和 AI 修改规则。

本文档可作为工程初始化模板使用。初始化时应根据用户输入判断是否启用对象存储，并替换所有 `{...}` 占位符。

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{OBJECT_STORAGE_ENABLED}` | 是否启用对象存储 | true / false |
| `{OBJECT_STORAGE_OWNER}` | 对象存储负责人 | 待确认 |
| `{OBJECT_STORAGE_PROVIDER}` | 对象存储服务 | S3-compatible / OSS / COS / OBS / 本地文件系统 / 待确认 |
| `{OBJECT_STORAGE_MODE}` | 桶策略 | 单桶 + 前缀 / 多桶 / 按环境隔离 / 按租户隔离 |
| `{DEFAULT_BUCKET}` | 默认 bucket 或 container | 待确认 |
| `{BUCKET_NAMING_RULE}` | bucket 命名规则 | `{product_code}-{env}-{purpose}` |
| `{OBJECT_KEY_PATTERN}` | 对象 key 命名规则 | `{resource_type}/{business_id}/{object_id}/{filename}` |
| `{PUBLIC_ACCESS_POLICY}` | 公开访问策略 | 禁止公开 / 允许公开只读 / 待确认 |
| `{SIGNED_URL_TTL}` | 签名 URL 有效期 | 待确认 |
| `{CDN_ENABLED}` | 是否启用 CDN | true / false |
| `{MEDIA_TYPES}` | 存储资源类型 | 图片 / 视频 / 文档 / 导入导出 / 处理产物 |
| `{BACKUP_POLICY}` | 备份策略 | 待确认 |
| `{LIFECYCLE_POLICY}` | 生命周期策略 | 待确认 |
| `{OBJECT_STORAGE_TEST_COMMAND}` | 对象存储测试命令 | 待确认 |

## 2. 启用条件 `[通用]`

满足以下任一条件时，应启用对象存储策略：

- 系统需要保存图片、视频、音频、文档、附件、导入文件、导出文件或处理产物。
- 文件需要独立于应用实例持久化。
- 文件需要通过签名 URL、CDN、异步处理、跨服务访问或批量迁移进行管理。
- 部署方式包含容器化、集群、多实例或云环境，不能依赖单机本地目录。

未启用对象存储时，应说明替代方案，例如本地文件系统、数据库二进制字段或外部文件服务，并明确未来迁移到对象存储的触发条件。

## 3. 当前策略概览 `[通用 + 个性化]`

| 项 | 策略 |
|---|---|
| 是否启用 | `{OBJECT_STORAGE_ENABLED}` |
| 服务提供方 | `{OBJECT_STORAGE_PROVIDER}` |
| 桶策略 | `{OBJECT_STORAGE_MODE}` |
| 默认 bucket / container | `{DEFAULT_BUCKET}` |
| 公开访问 | `{PUBLIC_ACCESS_POLICY}` |
| 签名 URL 有效期 | `{SIGNED_URL_TTL}` |
| CDN | `{CDN_ENABLED}` |
| 主要资源类型 | `{MEDIA_TYPES}` |
| 备份策略 | `{BACKUP_POLICY}` |
| 生命周期策略 | `{LIFECYCLE_POLICY}` |

初始化时不得保留来源项目的 bucket、前缀或业务资源类型；未知信息必须标记为 `待确认`。

## 4. 桶 / 容器划分策略 `[通用 + 个性化]`

### 4.1 单桶 + 前缀策略 `[条件启用]`

适用于资源规模较小、权限边界简单、部署和迁移成本优先的项目。

```text
bucket: {DEFAULT_BUCKET}
key: {resource_type}/{business_scope}/{object_id}/{filename}
```

优点：

- 初始化简单，环境变量少。
- 本地开发、备份、迁移和权限配置更容易。
- 适合单业务域或早期 MVP。

限制：

- 不同资源类型生命周期和权限差异较大时会变复杂。
- 合规、租户隔离或成本核算要求较强时不够清晰。

### 4.2 多桶策略 `[条件启用]`

适用于生命周期、权限、合规、资源规模或成本核算存在明显差异的项目。

| bucket / container | 用途 | 访问级别 | 生命周期 | 备注 |
|---|---|---|---|---|
| `{PRIVATE_BUCKET}` | 私有业务文件 | 私有 | `{PRIVATE_LIFECYCLE}` | 待确认 |
| `{PUBLIC_BUCKET}` | 公开资源 | 公开只读 / CDN | `{PUBLIC_LIFECYCLE}` | 待确认 |
| `{TEMP_BUCKET}` | 临时上传、导入、转码中间文件 | 私有 | 短期清理 | 待确认 |
| `{EXPORT_BUCKET}` | 导出文件 | 私有 / 签名下载 | `{EXPORT_LIFECYCLE}` | 待确认 |
| `{ARCHIVE_BUCKET}` | 归档资源 | 私有 | 长期保存 | 条件启用 |

### 4.3 环境隔离 `[通用]`

不同环境的对象必须隔离，禁止开发、测试、生产共用同一存储命名空间。

推荐规则：

```text
{product_code}-{env}-{purpose}
```

示例用途：

- `dev`：本地或开发环境。
- `test` / `staging`：测试或预发环境。
- `prod`：生产环境。

## 5. 资源前缀与类型 `[通用 + 个性化]`

初始化时应根据 `{MEDIA_TYPES}` 生成实际前缀，不启用的资源类型必须删除。

| 前缀 | 资源类型 | 说明 | 是否条件启用 |
|---|---|---|---|
| `original/` | 原始文件 | 上传原始文件 | 按需 |
| `thumbnails/` | 缩略图 | 图片或视频封面缩略图 | 按需 |
| `processed/` | 处理产物 | 压缩、裁剪、转码、结构化产物 | 按需 |
| `tmp/` | 临时文件 | 上传、导入、处理中的短期文件 | 按需 |
| `imports/` | 导入文件 | 批量导入源文件 | 按需 |
| `exports/` | 导出文件 | 报表、批量导出、离线任务结果 | 按需 |
| `images/` | 图片 | 图片资源 | 按需 |
| `videos/` | 视频 | 原始视频 | 按需 |
| `videos/covers/` | 视频封面 | 视频封面图 | 按需 |
| `videos/transcoded/` | 转码视频 | 多清晰度或压缩后视频 | 按需 |
| `documents/` | 文档 | PDF、Office、文本附件 | 按需 |
| `avatars/` | 头像 | 用户或组织头像 | 按需 |
| `audit/` | 审计附件 | 需要保留的审计材料 | 条件启用 |
| `archive/` | 归档文件 | 冷数据或历史资源 | 条件启用 |

前缀要求：

- 前缀必须反映资源类型或生命周期，不得直接使用临时业务命名。
- 临时文件必须有过期清理策略。
- 可公开资源与私有资源应通过 bucket、前缀或访问策略明确隔离。
- 视频相关前缀必须与 `docs/06-video-asset-management.md` 一致。

## 6. 对象 Key 命名规范 `[通用 + 个性化]`

推荐 key 结构：

```text
{resource_type}/{business_type}/{business_id}/{object_id}/{variant}.{ext}
```

示例模板：

```text
images/{business_type}/{business_id}/{media_id}/original.{ext}
images/{business_type}/{business_id}/{media_id}/thumbnail.{ext}
videos/{business_type}/{business_id}/{media_id}/source.{ext}
videos/{business_type}/{business_id}/{media_id}/cover.{ext}
exports/{job_id}/{file_id}.{ext}
tmp/{upload_session_id}/{part_id}
```

命名要求：

- 不得使用用户上传的原始文件名作为唯一 key。
- key 中不得包含敏感信息、手机号、邮箱、身份证、token 或明文用户名。
- key 必须可以追踪到业务对象或任务上下文。
- 需要覆盖写入时必须有版本或幂等策略。
- 删除、替换、转码、缩略图生成必须保持原始资源和派生资源关系可追踪。

## 7. 访问控制 `[通用 + 个性化]`

| 资源类型 | 默认访问级别 | URL 策略 | 权限来源 |
|---|---|---|---|
| 私有业务文件 | 私有 | 签名 URL / 后端代理 | 登录态 + 业务权限 |
| 公开资源 | 公开只读 / CDN | 公共 URL / CDN URL | 发布状态 |
| 导出文件 | 私有 | 短期签名 URL | 发起人或授权角色 |
| 临时文件 | 私有 | 不对外暴露 | 上传会话 |
| 归档文件 | 私有 | 内部访问 | 管理权限 |

要求：

- 默认策略必须是私有优先。
- 公开访问必须有明确业务理由和发布流程。
- 签名 URL 必须有过期时间，不得长期有效。
- 对象存储权限不得绕过应用层权限模型。
- 管理后台和用户端的访问能力必须与 `rules/security.md` 保持一致。

## 8. 上传与下载策略 `[通用 + 个性化]`

| 项 | 策略 |
|---|---|
| 上传方式 | 后端中转 / 预签名直传 / 分片上传 / 待确认 |
| 下载方式 | 后端代理 / 签名 URL / CDN / 待确认 |
| 大文件支持 | 分片上传 / 断点续传 / 待确认 |
| 文件校验 | 扩展名、MIME、文件头、大小、hash |
| 上传失败处理 | 不生成可用元数据，清理临时对象 |
| 下载失败处理 | 区分权限不足、对象不存在、URL 过期、服务不可用 |

上传和下载策略必须与 `rules/media.md`、`rules/api.md`、`docs/03-api-index.md` 保持一致。

## 9. 元数据与数据库关联 `[通用 + 个性化]`

对象存储只保存文件内容，业务系统必须保存可查询、可审计的元数据。

建议元数据字段：

| 字段 | 说明 |
|---|---|
| `id` | 文件或媒体 ID |
| `business_type` | 绑定业务类型 |
| `business_id` | 绑定业务对象 ID |
| `resource_type` | 图片、视频、文档、导入文件、导出文件等 |
| `bucket` | bucket 或 container |
| `object_key` | 对象 key |
| `mime_type` | MIME 类型 |
| `file_size` | 文件大小 |
| `checksum` | 文件摘要 |
| `status` | 上传中、可用、处理中、失败、归档、删除 |
| `visibility` | 私有、公开、内部 |
| `created_by` | 上传或创建人 |
| `created_at` / `updated_at` | 时间戳 |

数据库表和字段必须与 `docs/04-database-design.md` 保持一致。

## 10. 生命周期与清理 `[通用 + 个性化]`

| 资源类型 | 生命周期策略 | 清理方式 |
|---|---|---|
| 临时上传文件 | `{TEMP_OBJECT_TTL}` | 定时清理 |
| 导出文件 | `{EXPORT_OBJECT_TTL}` | 到期删除或归档 |
| 处理失败产物 | `{FAILED_OBJECT_TTL}` | 到期清理 |
| 已删除业务文件 | `{DELETED_OBJECT_RETENTION}` | 延迟硬删除 |
| 归档文件 | `{ARCHIVE_RETENTION}` | 长期保存或冷存储 |

要求：

- 数据库软删除和对象硬删除必须有明确顺序。
- 临时文件必须可重复清理，清理任务应具备幂等性。
- 删除对象前应确认没有其他业务对象引用。
- 生产数据清理必须可审计。

## 11. 备份、迁移与恢复 `[通用]`

备份策略应覆盖：

- bucket 配置、访问策略和生命周期规则。
- 对象文件本身。
- 数据库中与对象相关的元数据。
- 加密密钥、访问密钥和环境变量的安全备份。

迁移策略应覆盖：

- 同服务跨 bucket 迁移。
- 不同对象存储服务之间迁移。
- 本地文件系统迁移到对象存储。
- 单桶迁移到多桶。
- 多桶合并或按前缀重组。

恢复验证必须同时校验对象存在、元数据一致、访问权限正确和业务页面可用。

## 12. 成本与容量治理 `[条件启用]`

当项目存在大量文件、大视频、导出任务、长期归档或云存储计费时启用本节。

治理项：

- bucket 或前缀级别容量统计。
- 大文件、冷文件、长期未访问文件识别。
- CDN 流量、请求次数、存储容量成本监控。
- 自动清理临时文件和过期导出文件。
- 按租户、业务线或环境统计资源占用。

## 13. 本地开发与测试替代方案 `[通用]`

本地开发可选择：

- 使用 S3-compatible 本地服务。
- 使用云对象存储的开发 bucket。
- 使用本地文件系统模拟对象存储。
- 使用 mock 或 fake storage client 进行单元测试。

要求：

- 本地环境不得连接生产 bucket。
- `.env.example` 必须说明对象存储相关变量。
- 测试数据和临时对象必须可清理。
- CI 中不得依赖不可控的生产外部资源。

## 14. 测试与验收 `[通用 + 个性化]`

| 测试类型 | 验证内容 | 是否必需 |
|---|---|---|
| 单元测试 | key 生成、URL 生成、权限判断、生命周期规则 | 是 |
| API 测试 | 上传、下载、删除、签名 URL、错误处理 | 是 |
| 集成测试 | 对象存储服务、数据库元数据一致性 | 条件启用 |
| 安全测试 | 越权访问、公开策略、URL 过期、非法文件 | 是 |
| 迁移测试 | bucket 迁移、前缀迁移、元数据修复 | 条件启用 |
| 清理测试 | 临时文件、导出文件、删除文件清理 | 条件启用 |

验收标准：

- 上传成功后，对象存在且数据库元数据一致。
- 下载或预览时权限控制生效。
- 签名 URL 到期后不可继续访问。
- 删除、替换和归档操作不会造成孤儿对象或失效引用。
- `{OBJECT_STORAGE_TEST_COMMAND}` 可以覆盖项目声明的关键验证路径；无法自动化时必须补充人工验证步骤。

## 15. 何时调整桶策略 `[通用]`

以下情况必须通过需求或 OpenSpec Change 调整对象存储策略：

- 需要不同资源类型使用不同生命周期。
- 需要更严格的权限、租户、客户或合规隔离。
- 单 bucket 容量、性能、权限配置或成本统计难以管理。
- 新增视频、导入导出、归档、公开 CDN 等资源类型。
- 从本地文件系统迁移到对象存储。
- 从开发单环境扩展到多环境、多租户或私有化部署。

## 16. AI 修改要求 `[通用]`

涉及对象存储的需求进入开发时，AI 必须检查并按需更新：

```text
rules/object-storage.md
rules/media.md
rules/security.md
rules/api.md
rules/data-management.md
docs/03-api-index.md
docs/04-database-design.md
docs/05-compatibility-matrix.md
docs/06-video-asset-management.md
docs/07-object-storage-strategy.md
.env.example
docker-compose.yml
tests/integration/media/
tests/compatibility/object-storage/
```

修改要求：

- 不得只修改 bucket 或 key，而不更新数据库元数据、API、权限和测试。
- 新增公开访问必须说明业务理由、权限边界和缓存失效策略。
- 新增生命周期清理必须说明数据保留、恢复和审计策略。
- 修改对象存储服务提供方时，必须同步环境变量、部署文档和兼容性矩阵。

## 17. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- 对象存储服务、bucket、container、前缀或 key 命名变化。
- 新增或删除资源类型。
- 上传、下载、签名 URL、CDN 或公开访问策略变化。
- 数据库元数据、媒体表或业务对象绑定变化。
- 生命周期、清理、备份、迁移或恢复策略变化。
- 本地开发、CI、部署或私有化环境的对象存储配置变化。
- 安全、合规、审计或成本治理要求变化。
