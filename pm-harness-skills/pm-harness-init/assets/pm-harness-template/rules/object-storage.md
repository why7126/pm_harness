---
purpose: 对象存储使用规范
content: 规定对象存储启用条件、供应商适配、Bucket 策略、对象 Key、权限、签名 URL、生命周期、环境变量、兼容性与 AI 更新要求
source: Harness object-storage.md 抽象模板，基于多项目对象存储规则沉淀
update_method: 项目初始化时按用户输入生成；对象存储供应商、Bucket 策略、上传下载权限、生命周期、文件类型或部署方式变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
note: 适用于 {PRODUCT_NAME} 项目；默认推荐一个项目一个 Bucket，桶内按对象前缀区分资源类型
template_scope: 可作为工程初始化的 object-storage.md 模块
---

# 对象存储规范

## 0. 规则定位 [通用]

本文档用于约束 `{PRODUCT_NAME}` 项目的对象存储使用方式，包括：

- 是否启用对象存储。
- 存储供应商和适配层。
- Bucket 命名与隔离策略。
- 对象 Key 前缀规范。
- 上传、下载、删除、签名 URL、健康检查接口。
- 权限、安全、生命周期、清理策略。
- 本地开发、私有化、云部署、信创适配。

AI 新增或修改文件上传、媒体管理、导入导出、备份、模型文件、报告导出等能力时，必须读取本文档。

### 0.1 初始化占位符 [通用]

| 占位符 | 含义 | 生成要求 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品中文名 | 来自用户输入 |
| `{PRODUCT_CODE}` | 项目代码名 | kebab-case |
| `{OBJECT_STORAGE_ENABLED}` | 是否启用对象存储 | 是/否 |
| `{OBJECT_STORAGE_STACK}` | 对象存储供应商 | MinIO、S3、OSS、COS、OBS、RustFS、文件系统等 |
| `{OBJECT_STORAGE_PROVIDER_MATRIX}` | 供应商兼容矩阵 | 按部署模式生成 |
| `{BUCKET_NAME}` | 默认 Bucket | 推荐 `{PRODUCT_CODE}` |
| `{BUCKET_POLICY}` | Bucket 策略 | 单 Bucket + 前缀、多 Bucket、租户隔离 |
| `{OBJECT_KEY_PREFIXES}` | 对象 Key 前缀 | 按媒体/导入导出/模型生成 |
| `{STORAGE_CLIENT_INTERFACE}` | 存储客户端接口 | 按后端技术栈生成 |
| `{SIGNED_URL_POLICY}` | 签名 URL 策略 | 有效期、权限、用途 |
| `{LIFECYCLE_POLICY}` | 生命周期策略 | 临时文件、导出文件、处理产物清理 |

生成初始化工程时，必须替换所有占位符；未知项写 `待确认`，不得保留样例项目的 Bucket、业务前缀或供应商假设。

## 1. 文档模块分类 [通用]

- `[通用]`：所有 Harness 工程默认保留，至少说明是否启用对象存储和安全边界。
- `[个性化]`：必须根据项目部署模式、供应商、媒体类型、数据策略生成。
- `[条件启用]`：仅在对象存储或对应能力启用时保留，例如 MinIO、S3、COS、OBS、RustFS、私有化、签名 URL、分片上传。

如果 `{OBJECT_STORAGE_ENABLED}=否`，初始化时应删除具体供应商、Bucket、Key、SDK、MinIO 等强制规则，仅保留“未启用对象存储，文件存储策略待确认/使用本地文件系统”的说明。

## 2. 总原则 [通用 + 个性化]

默认策略：

```text
一个项目一个 Bucket
桶内按对象前缀区分资源类型
```

推荐默认 Bucket：

```text
{BUCKET_NAME}
```

原则：

- 不推荐按资源类型拆分多个 Bucket，除非 OpenSpec、合规、安全隔离、计费或生命周期策略明确要求。
- 文件本体进入对象存储，元数据进入数据库。
- 对象 Key 必须由服务端生成。
- 前端不得绕过后端授权直接写入对象存储，除非使用后端签发的临时凭证或预签名 URL。
- 对外访问默认使用签名 URL、后端代理或受控公开策略。
- 对象存储密钥不得进入前端公开变量、日志、文档示例或代码默认值。

## 3. 启用条件与适用场景 [通用 + 条件启用]

以下能力通常需要对象存储：

| 能力 | 是否建议对象存储 | 说明 |
|---|---:|---|
| 图片/音频/视频上传 | 是 | 大文件、权限访问、预览播放 |
| 文档附件 | 是 | 下载、预览、权限控制 |
| 导入导出 | 视情况 | 小文件可本地临时，大文件建议对象存储 |
| 媒体处理产物 | 是 | 缩略图、转码、封面、字幕 |
| 模型文件 | 视情况 | 大模型可对象存储/制品仓库 |
| 备份文件 | 视情况 | 需加密、生命周期和权限策略 |
| 无上传/文件能力 | 否 | 删除对象存储强制规则 |

初始化时根据 `{OBJECT_STORAGE_ENABLED}` 和产品能力生成。

## 4. 供应商兼容矩阵 [个性化 + 条件启用]

对象存储供应商：

```text
{OBJECT_STORAGE_STACK}
```

初始化时生成：

```text
{OBJECT_STORAGE_PROVIDER_MATRIX}
```

推荐矩阵：

| 后端 | 场景 | 适配方式 | 备注 |
|---|---|---|---|
| MinIO | 本地开发、小规模私有化 | S3 Compatible SDK | 常用默认 |
| AWS S3 | AWS 云部署 | S3 SDK | 云上生产 |
| RustFS | 私有化/本地化 | S3 Compatible SDK | 按项目需要 |
| 腾讯 COS | 腾讯云客户 | COS SDK 或 S3 兼容 | 需兼容性验证 |
| 华为 OBS | 华为云/信创 | OBS SDK 或 S3 兼容 | 需兼容性验证 |
| 阿里云 OSS | 阿里云客户 | OSS SDK | 需兼容性验证 |
| 本地文件系统 | 原型/单机 | FileSystem Adapter | 不适合多实例生产 |

规则：

- 多供应商项目必须通过适配层/工厂模式切换，不得在业务代码中硬编码具体 SDK。
- 单供应商项目仍应封装最小存储接口，避免对象存储细节泄露到业务层。
- 兼容供应商差异必须同步 `compatibility/object-storage/` 和 `rules/compatibility.md`。

## 5. Bucket 策略 [通用 + 个性化]

Bucket 策略：

```text
{BUCKET_POLICY}
```

推荐：

```text
bucket: {BUCKET_NAME}
```

### 5.1 单 Bucket + 前缀 [通用]

适合大多数项目：

```text
{BUCKET_NAME}/
├── images/
├── videos/
├── audios/
├── files/
└── tmp/
```

优点：

- 环境变量简单。
- 权限与生命周期集中管理。
- 本地开发和私有化部署更容易。

### 5.2 多 Bucket [条件启用]

仅在以下场景启用：

- 不同数据类别需要完全不同的访问策略。
- 不同生命周期策略无法用前缀规则满足。
- 多租户或客户隔离要求强制 Bucket 隔离。
- 合规要求不同资源物理隔离。

启用多 Bucket 时，必须说明每个 Bucket 的用途、权限、生命周期、环境变量和迁移策略。

## 6. 对象 Key 前缀规范 [通用 + 个性化]

标准对象前缀：

```text
{OBJECT_KEY_PREFIXES}
```

推荐默认：

```text
images/                图片类对象
videos/                视频类对象
audios/                音频类对象
files/                 文档、导入、导出、模型等通用文件
tmp/                   临时处理文件
```

对象 Key 推荐结构：

```text
{prefix}/default/{resource_type}/{uuid}.{ext}
```

规则：

- Key 由服务端生成。
- 不直接使用用户原始文件名。
- `prefix` MUST 使用资源大类，不得使用 `original/`、`processed/`、`thumbnails/` 等生命周期或处理状态作为顶层前缀。
- `default` MUST 保留，作为默认租户/默认命名空间占位；未来多租户时可替换为 tenant id，但单租户项目也不得省略。
- `resource_type` MUST 表示业务资源类型，可使用多段路径，例如 `user/avatars`、`brands/logos`、`products/images`、`imports/source`、`exports/reports`。
- 原图、缩略图、转码、处理产物等状态不得改变顶层 prefix；需要区分时应体现在 `resource_type` 或数据库元数据字段中。
- 不允许路径穿越、绝对路径、URL 编码绕过。
- 扩展名应基于服务端 MIME/文件头校验结果。
- 多租户项目必须明确租户隔离策略。

## 7. 存储客户端接口 [通用 + 个性化]

存储客户端接口：

```text
{STORAGE_CLIENT_INTERFACE}
```

推荐统一接口：

```text
upload_file()
upload_stream()
download_file()
download_stream()
delete_file()
file_exists()
get_file_url()
get_presigned_upload_url()
get_presigned_download_url()
copy_object()
move_object()
list_objects()
get_object_metadata()
ping()
```

大文件场景可增加：

```text
create_multipart_upload()
upload_part()
complete_multipart_upload()
abort_multipart_upload()
```

规则：

- 业务层只能依赖统一接口，不直接依赖具体供应商 SDK。
- SDK 异常必须转换为项目统一错误。
- 上传、下载、删除、签名 URL、健康检查必须有测试。
- 供应商差异必须在 adapter 内部处理。

## 8. 上传、下载与访问控制 [通用]

上传：

- 必须鉴权。
- 必须校验业务归属、权限、大小、MIME、文件头。
- 大文件上传应支持流式或分片。
- 上传成功后必须写入元数据。

下载：

- 默认需要鉴权。
- 对外访问使用后端代理、签名 URL 或受控公开策略。
- 签名 URL 不得用于敏感资源的长期公开访问。

删除：

- 删除对象前必须确认业务权限。
- 软删除业务数据时，应明确对象是否同步删除。
- 删除失败必须可重试或记录待清理任务。

## 9. 签名 URL 策略 [条件启用]

签名 URL 策略：

```text
{SIGNED_URL_POLICY}
```

推荐：

```text
MEDIA_SIGNED_URL_EXPIRE_SECONDS=900
UPLOAD_SIGNED_URL_EXPIRE_SECONDS=600
```

规则：

- 签名 URL 有效期必须可配置。
- 上传签名 URL 只能用于指定 Bucket、Key、Content-Type、大小范围。
- 下载签名 URL 必须在鉴权后生成。
- 权限变更、删除、禁用后，应避免旧 URL 长期可用。
- 前端不得持久保存签名 URL 作为长期凭证。

## 10. 生命周期与清理策略 [通用 + 条件启用]

生命周期策略：

```text
{LIFECYCLE_POLICY}
```

推荐规则：

| 前缀 | 生命周期 |
|---|---|
| `tmp/` | 短期自动清理 |
| `images/` | 跟随业务对象或媒体元数据策略 |
| `videos/` | 跟随业务对象或媒体元数据策略 |
| `audios/` | 跟随业务对象或媒体元数据策略 |
| `files/` | 按 `resource_type` 区分导入、导出、文档、模型等生命周期 |

清理策略必须与业务数据状态一致，避免数据库元数据指向已删除对象。

## 11. 环境变量 [通用 + 个性化]

对象存储变量必须同步 `rules/environment.md` 和 `.env.example`。

推荐变量：

```ini
OBJECT_STORAGE_ENABLED=true
STORAGE_TYPE=minio
STORAGE_ENDPOINT=localhost:9000
STORAGE_PUBLIC_ENDPOINT=http://localhost:9000
STORAGE_ACCESS_KEY=example_access_key
STORAGE_SECRET_KEY=example_secret_key
STORAGE_BUCKET={BUCKET_NAME}
STORAGE_REGION=us-east-1
STORAGE_SECURE=false
STORAGE_SIGNED_URL_EXPIRE_SECONDS=900
```

MinIO 兼容变量可使用：

```ini
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=example_access_key
MINIO_SECRET_KEY=example_secret_key
MINIO_BUCKET={BUCKET_NAME}
MINIO_SECURE=false
```

示例密钥必须明显不可用于生产，真实密钥禁止提交。

## 12. 本地开发配置 [条件启用]

本地开发常用 MinIO：

```text
API:     http://localhost:9000
Console: http://localhost:9001
Bucket:  {BUCKET_NAME}
```

规则：

- 本地默认账号只能用于开发，不得用于生产。
- `minio-init` 或初始化脚本可自动创建 Bucket。
- 默认 Bucket 权限应保持私有，除非明确需要公开只读资源。
- Docker Compose 中的端口必须与 `rules/port-management.md` 一致。

## 13. 部署与私有化 [条件启用]

### 13.1 Docker Compose [条件启用]

- Compose 使用的对象存储变量必须在 `.env.example` 中说明。
- `env_file` 不得指向不存在文件。
- 容器内 endpoint 与宿主机 endpoint 必须区分。

### 13.2 Kubernetes / 云部署 [条件启用]

- ConfigMap 仅放非敏感配置。
- Access Key、Secret Key 必须放 Secret 或密钥管理系统。
- Helm values 示例不得包含真实密钥。

### 13.3 私有化部署 [条件启用]

- 支持客户提供 S3 兼容存储时，必须写明兼容测试范围。
- 客户环境密钥不进入仓库。
- 供应商差异和限制写入 `compatibility/object-storage/`。

## 14. 安全要求 [通用]

- 对象存储默认私有。
- Secret 不得进入前端变量、日志、错误信息、文档示例。
- 上传必须防 MIME 伪造、路径穿越、超大文件、压缩包炸弹。
- 对象 Key 不得包含真实身份证号、手机号、邮箱、客户名等敏感信息。
- 访问对象前必须校验业务权限。
- 预览、下载、导出 URL 必须可过期。
- 多租户项目必须防止跨租户访问对象。

## 15. 兼容性与测试 [通用 + 条件启用]

对象存储能力必须补充测试：

- 上传成功。
- 下载成功。
- 流式下载。
- 删除成功。
- 文件不存在。
- 签名 URL 生成。
- 权限不足。
- 大文件或分片上传。
- provider ping/health check。

多供应商项目必须维护兼容性矩阵：

```text
compatibility/object-storage/
```

至少覆盖 API 差异、签名 URL、分片上传、ACL、生命周期、区域/endpoint、路径风格/虚拟主机风格。

## 16. AI 更新规则 [通用]

AI 在新增文件上传、视频上传、图片处理、音频处理、导入导出、模型文件、对象存储适配时：

1. 不允许新增多个业务 Bucket，除非 OpenSpec 明确要求。
2. 必须复用 `.env.example` 中的 Bucket 和存储配置变量。
3. 必须使用标准前缀或同步更新本文档。
4. 不得硬编码具体存储后端实现，应使用统一接口/适配层。
5. 必须更新媒体、数据管理、安全、环境变量和部署文档。
6. 必须补充对象 Key 生成逻辑和测试。
7. 必须同步 `compatibility/object-storage/` 中的供应商差异。

重点同步：

```text
rules/object-storage.md
rules/media.md
rules/data-management.md
rules/environment.md
rules/security.md
docs/07-object-storage-strategy.md
docs/standards/file_upload.md
docs/05-compatibility-matrix.md
compatibility/object-storage/
.env.example
docker-compose.yml
src/backend/**/storage*
tests/compatibility/
tests/integration/
```

具体路径必须根据项目实际目录生成，不得保留不存在的样例路径。

## 17. 禁止事项 [通用]

- 禁止前端绕过后端授权直接写入对象存储。
- 禁止业务代码直接依赖具体供应商 SDK。
- 禁止使用用户原始文件名直接作为对象 Key。
- 禁止把对象存储密钥写入前端公开变量。
- 禁止公开敏感对象的永久 URL。
- 禁止新增 Bucket、前缀、环境变量后不同步文档和测试。
- 禁止保留样例项目的 Bucket、Key 前缀、供应商假设。

## 18. 初始化生成建议 [通用]

将本文档作为工程初始化模块时，生成器应按以下步骤处理：

1. 根据 `{OBJECT_STORAGE_ENABLED}` 决定生成完整对象存储规范或未启用占位说明。
2. 根据 `{OBJECT_STORAGE_STACK}` 生成供应商兼容矩阵、环境变量和 adapter 规则。
3. 根据 `{BUCKET_POLICY}` 决定单 Bucket、多 Bucket、租户隔离策略。
4. 根据 `{OBJECT_KEY_PREFIXES}` 生成项目专属对象前缀，删除样例业务前缀。
5. 根据 `{STORAGE_CLIENT_INTERFACE}` 和 `{BACKEND_STACK}` 生成客户端接口描述。
6. 根据 `{SIGNED_URL_POLICY}` 生成签名 URL 有效期、用途和安全约束。
7. 根据 `{LIFECYCLE_POLICY}` 生成 tmp、imports、exports、processed、models 等清理策略。
8. 删除未启用供应商、分片上传、Kubernetes、私有化等条件章节。
9. 检查本文档与 `media.md`、`data-management.md`、`environment.md`、`security.md`、`compatibility.md`、`port-management.md` 一致。

## 19. 完成任务后检查清单 [通用]

```text
□ 是否明确对象存储是否启用
□ [通用]、[个性化]、[条件启用] 模块标识完整
□ 供应商矩阵、Bucket 策略、对象 Key 前缀已参数化
□ 存储客户端接口与后端技术栈一致
□ 上传下载、签名 URL、权限、安全、生命周期规则完整
□ 环境变量与 .env.example、deployment、port-management 一致
□ 兼容性与测试要求覆盖供应商差异
□ AI 更新规则覆盖 docs、OpenSpec、代码、测试、部署
□ 未保留样例项目 Bucket、Key 前缀或供应商硬编码
```
