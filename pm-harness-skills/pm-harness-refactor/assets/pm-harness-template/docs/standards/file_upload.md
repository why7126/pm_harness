---
purpose: 文件上传治理
content: 文件上传入口、认证授权、格式大小限制、安全校验、对象存储、元数据、响应结构、错误码、测试与维护规则
source: Harness docs/standards/file_upload.md 抽象模板，初始化时基于用户输入生成
update_method: 上传类型、上传方式、对象存储、元数据、错误码、安全限制或前端上传流程变化时同步更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {MEDIA_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；无文件上传能力时可保留为未来启用规范并标记不适用
---

# 文件上传规范

## 0. 文档定位 `[通用]`

本文档定义项目文件上传能力的治理规则，覆盖上传入口、认证授权、上传方式、文件类型、大小限制、MIME 与文件头校验、对象存储、对象 Key、元数据、响应结构、错误码、前端交互、测试验收和 AI 修改边界。

本文档是 `rules/media.md`、`rules/object-storage.md`、`rules/security.md` 中上传规则的落地细则，应与 `docs/standards/api-governance.md`、`docs/standards/error-codes.md`、`docs/06-video-asset-management.md`、`docs/07-object-storage-strategy.md` 保持一致。

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{MEDIA_OWNER}` | 媒体与上传负责人 | 待确认 |
| `{UPLOAD_ENABLED}` | 是否启用上传 | true / false |
| `{UPLOAD_SCENARIOS}` | 上传业务场景 | 头像、附件、导入文件、视频等 |
| `{UPLOAD_METHOD}` | 上传方式 | multipart / presigned-url / chunked / mixed |
| `{API_PREFIX}` | API 基础前缀 | `/api/v1` |
| `{UPLOAD_ENDPOINTS}` | 上传接口清单 | 待确认 |
| `{AUTH_STRATEGY}` | 鉴权策略 | Token / Session / API Key / none |
| `{OBJECT_STORAGE_ENABLED}` | 是否启用对象存储 | true / false |
| `{OBJECT_STORAGE_STACK}` | 对象存储或文件存储方案 | S3 compatible / OSS / COS / OBS / local filesystem / none |
| `{BUCKET_POLICY}` | 桶/容器策略 | 单桶 + 前缀 / 多桶 / 按租户隔离 |
| `{OBJECT_KEY_PATTERN}` | 对象 Key 规则 | 待确认 |
| `{UPLOAD_ALLOWED_TYPES}` | 文件类型白名单 | 待确认 |
| `{UPLOAD_MAX_SIZE_POLICY}` | 大小限制 | 待确认 |
| `{UPLOAD_SECURITY_POLICY}` | 上传安全策略 | MIME、文件头、扫描、隔离等 |
| `{UPLOAD_RESPONSE_SCHEMA}` | 上传响应结构 | 待确认 |
| `{UPLOAD_ERROR_CODES}` | 上传错误码 | 待确认 |
| `{UPLOAD_TEST_COMMAND}` | 上传测试命令 | 待确认 |

## 2. 启用条件 `[通用]`

满足以下任一条件时，应完整启用本文档：

- 项目支持图片、音频、视频、文档、附件、导入文件、导出文件或压缩包上传。
- 项目需要对象存储、临时文件、预签名 URL、分片上传或文件元数据管理。
- 前端、移动端、微信小程序、SDK、开放 API 或第三方调用方需要提交文件。
- 项目需要限制文件类型、大小、权限、访问范围、安全扫描或生命周期。

当 `{UPLOAD_ENABLED}=false` 且项目无任何上传、导入、附件、媒体或对象存储写入能力时，可保留本文档为未来启用规范，并删除强制接口、环境变量、存储和测试要求。

## 3. 上传总原则 `[通用]`

| 原则 | 说明 |
|---|---|
| 后端授权 | 上传必须由后端或可信服务授权 |
| 默认私有 | 上传文件默认不可公开访问 |
| 服务端校验 | 文件大小、扩展名、MIME、文件头、业务归属必须由服务端校验 |
| 元数据分离 | 文件本体进入对象存储或运行时目录，元数据进入数据库或业务记录 |
| Key 服务端生成 | 对象 Key 不得直接使用用户原始文件名 |
| 失败可追踪 | 上传失败必须返回受控错误码，并可通过 trace 排查 |
| 不进 Git | 上传文件、导入文件、导出文件、临时文件不得提交 Git |

## 4. 上传方式 `[通用 + 个性化]`

当前上传方式：

```text
{UPLOAD_METHOD}
```

| 方式 | 适用场景 | 生成要求 |
|---|---|---|
| `multipart/form-data` | 小中型文件、常规图片/附件 | 后端接收、校验、写入存储 |
| 预签名 URL | 大文件、弱网、直传对象存储 | 后端签发短期 URL，前端仅使用授权写入 |
| 分片上传 | 大视频、大文件、断点续传 | 需要分片初始化、上传、合并、取消和清理 |
| 后端流式上传 | 大文件代理、需要强校验 | 避免整文件加载内存 |
| 异步上传处理 | 转码、扫描、OCR、导入解析 | 上传成功不等于处理完成 |

规则：

- 未启用的上传方式不得出现在强制实现要求中。
- 前端不得绕过后端授权直接写入对象存储或文件系统。
- 如果启用预签名 URL，必须说明签名有效期、允许方法、对象 Key、文件大小、文件类型和回调/确认流程。
- 如果启用分片上传，必须说明分片大小、最大分片数、合并策略、失败清理和幂等规则。

## 5. 上传接口 `[通用 + 个性化]`

上传接口事实源：

```text
{UPLOAD_ENDPOINTS}
```

multipart 上传模板：

```http
POST {API_PREFIX}/uploads/{resource_type}
{AUTH_HEADER}
Content-Type: multipart/form-data

file: <binary>
metadata: <json string or form fields>
```

预签名上传模板：

```http
POST {API_PREFIX}/uploads/{resource_type}/presign
{AUTH_HEADER}
Content-Type: application/json

{
  "filename": "{ORIGINAL_FILENAME}",
  "mime_type": "{MIME_TYPE}",
  "size": 0,
  "business_ref": "{BUSINESS_REF}"
}
```

要求：

- 上传接口必须声明认证、权限、业务归属、请求字段、响应字段和错误码。
- 每类上传必须有明确 `resource_type`、业务对象、文件类型、大小限制和生命周期。
- 上传接口不得把客户端传入的文件名、路径、MIME 或对象 Key 当作可信输入。
- 对导入、转码、扫描、解析等异步处理场景，上传响应必须区分“文件已接收”和“业务处理已完成”。

## 6. 认证、授权与访问控制 `[通用 + 个性化]`

当前认证策略：

```text
{AUTH_STRATEGY}
```

要求：

- 上传入口默认必须鉴权。
- 上传前必须校验用户、租户、组织、资源归属、配额和业务状态。
- 管理端、用户端、内部服务、开放 API 的上传权限必须分开说明。
- 下载、预览、删除、替换、重新处理必须与上传使用一致的权限模型。
- 公开上传必须有明确业务理由，并具备限流、验证码、签名、临时凭证或其他保护机制。
- 对象 Key、URL 或文件 ID 不得成为访问授权的唯一依据。

## 7. 文件类型与大小限制 `[通用 + 个性化]`

初始化时生成：

```text
{UPLOAD_ALLOWED_TYPES}
{UPLOAD_MAX_SIZE_POLICY}
```

推荐矩阵：

| 类型 | 允许格式 | MIME 白名单 | 大小限制 | 额外限制 | 是否启用 |
|---|---|---|---:|---|---|
| 图片 | JPEG、PNG、WebP | `{IMAGE_MIME_TYPES}` | `{IMAGE_MAX_SIZE}` | 分辨率、EXIF、压缩 | 待确认 |
| 音频 | MP3、WAV、M4A、WebM | `{AUDIO_MIME_TYPES}` | `{AUDIO_MAX_SIZE}` | 时长、采样率 | 待确认 |
| 视频 | MP4、MOV、WebM | `{VIDEO_MIME_TYPES}` | `{VIDEO_MAX_SIZE}` | 时长、分辨率、封面 | 待确认 |
| 文档 | PDF、DOCX、XLSX | `{DOCUMENT_MIME_TYPES}` | `{DOCUMENT_MAX_SIZE}` | 预览、病毒扫描 | 待确认 |
| 导入文件 | CSV、XLSX、ZIP | `{IMPORT_MIME_TYPES}` | `{IMPORT_MAX_SIZE}` | 行数、压缩包安全 | 待确认 |

要求：

- 文件类型必须同时校验扩展名、MIME 和文件头。
- 大小限制必须同步 `.env.example`、`rules/environment.md` 和部署配置。
- 未启用的媒体类型不得生成强制上传接口、环境变量或测试要求。
- 客户端限制只用于体验优化，服务端限制才是准入事实源。

## 8. 安全校验 `[通用 + 个性化]`

上传安全策略：

```text
{UPLOAD_SECURITY_POLICY}
```

必须校验：

- 文件大小、扩展名、MIME、文件头。
- 文件名长度、字符集、控制字符和路径穿越。
- 业务类型、业务对象、用户/租户/组织归属。
- 上传频率、总配额、单用户配额、单业务对象配额。
- 压缩包层级、解压后体积、路径穿越和炸弹文件风险。

条件启用：

- 病毒扫描、内容审核、DLP、OCR、转码、缩略图、封面生成。
- 临时隔离区，扫描通过后再进入正式存储。
- 文件哈希去重、秒传、幂等上传。

禁止：

- 信任客户端 MIME、文件名、路径或对象 Key。
- 将用户文件名直接拼接为服务端路径或对象 Key。
- 把上传文件存入源码目录、公开静态目录或 Git 跟踪目录。
- 在错误信息中暴露临时目录、bucket、对象 Key、签名参数或内部栈。

## 9. 存储与对象 Key `[通用 + 个性化]`

存储方案：

```text
{OBJECT_STORAGE_STACK}
{BUCKET_POLICY}
```

对象 Key 规则：

```text
{OBJECT_KEY_PATTERN}
```

推荐结构：

```text
{prefix}/default/{resource_type}/{uuid}.{ext}
images/default/user/avatars/{uuid}.{ext}
images/default/brands/logos/{uuid}.{ext}
files/default/imports/source/{uuid}.{ext}
files/default/exports/result/{uuid}.{ext}
tmp/{upload_id}/{part_id}
```

规则：

- 正式业务对象 Key MUST 使用 `{prefix}/default/{resource_type}/{uuid}.{ext}`。
- `prefix` MUST 是资源大类，例如 `images`、`videos`、`files`、`audios`；不得使用 `original`、`processed`、`thumbnails` 作为顶层前缀。
- `default` MUST 保留为默认租户/命名空间占位。
- `resource_type` MUST 是业务资源路径，例如 `user/avatars`、`brands/logos`、`imports/source`。
- 对象 Key 必须由服务端生成。
- 扩展名必须来自服务端校验结果。
- 多租户项目必须明确租户隔离策略。
- 临时文件、导入文件、导出文件、处理产物必须有生命周期或清理策略。
- 对象存储策略必须与 `rules/object-storage.md` 和 `docs/07-object-storage-strategy.md` 一致。

## 10. 元数据与数据库 `[条件启用 + 个性化]`

当上传文件需要业务引用、下载、预览、审计或生命周期管理时启用。

推荐元数据字段：

| 字段 | 说明 | 是否必须 |
|---|---|---|
| `{FILE_ID_FIELD}` | 文件或媒体 ID | 是 |
| `{OWNER_FIELD}` | 所属用户、租户或组织 | 是 |
| `{BUSINESS_REF_FIELD}` | 业务对象引用 | 条件启用 |
| `{OBJECT_KEY_FIELD}` | 对象 Key | 是 |
| `{ORIGINAL_NAME_FIELD}` | 原始文件名 | 条件启用，需脱敏/清洗 |
| `{MIME_TYPE_FIELD}` | MIME 类型 | 是 |
| `{SIZE_FIELD}` | 文件大小 | 是 |
| `{HASH_FIELD}` | 文件哈希 | 条件启用 |
| `{STATUS_FIELD}` | 上传/处理状态 | 条件启用 |
| `{CREATED_AT_FIELD}` | 创建时间 | 是 |

要求：

- 数据库只存对象 Key、元数据和业务引用，不直接存大文件本体。
- 删除业务对象时必须明确文件保留、软删除、延迟清理或立即删除策略。
- 替换文件时必须明确旧文件处理策略。
- 元数据表、字段和关联关系必须与 `docs/04-database-design.md` 一致。

## 11. 响应结构 `[通用 + 个性化]`

上传响应结构：

```json
{UPLOAD_RESPONSE_SCHEMA}
```

推荐成功响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "file_id": "{FILE_ID}",
    "object_key": "{OBJECT_KEY}",
    "url": "{ACCESS_URL}",
    "mime_type": "{MIME_TYPE}",
    "size": 0,
    "status": "{UPLOAD_STATUS}"
  }
}
```

要求：

- `url` 如为临时访问地址，必须说明有效期。
- 不需要前端直接访问时，可以只返回 `file_id` 和必要元数据。
- 异步处理场景必须返回 `status`、`job_id` 或查询入口。
- 响应结构必须与 `rules/api.md`、`docs/standards/api-governance.md` 和 OpenAPI 契约一致。

## 12. 错误码 `[通用 + 个性化]`

上传错误码事实源：

```text
{UPLOAD_ERROR_CODES}
```

推荐错误场景：

| 场景 | HTTP | 错误类型 | 说明 |
|---|---|---|---|
| 未认证 | 401 | auth | 上传入口需要登录或凭证 |
| 权限不足 | 403 | auth | 无权向目标业务对象上传 |
| 文件缺失 | 400 | parameter | 未提交文件字段 |
| 文件类型不允许 | 400 | upload | 扩展名、MIME 或文件头不符合白名单 |
| 文件大小超限 | 400 / 413 | upload | 超过单文件或总量限制 |
| 配额不足 | 409 / 429 | upload | 用户、租户或业务对象配额不足 |
| 存储不可用 | 502 / 503 | dependency | 对象存储或文件系统不可用 |
| 处理失败 | 500 / 422 | media | 扫描、转码、解析或导入失败 |

要求：

- 具体错误码必须登记到 `docs/standards/error-codes.md`。
- 前端必须基于错误码处理重新登录、权限不足、类型错误、大小超限、配额不足和可重试失败。
- 错误 message 不得暴露 bucket、对象 Key、临时路径、签名参数、堆栈或第三方原始错误。

## 13. 前端上传体验 `[条件启用 + 个性化]`

当前端存在上传能力时启用。

要求：

- 前端应在选择文件时提示格式、大小、数量和业务限制。
- 前端校验不得替代后端校验。
- 上传中应展示进度、取消、失败重试和明确错误提示。
- 大文件、弱网或移动端场景应支持断点续传、重试或后台任务查询。
- 上传成功后应使用后端返回的 `file_id` 或业务引用，不应依赖本地临时路径。
- 前端不得保存对象存储访问密钥，不得把 Token、签名 URL 或敏感元数据写入日志。

## 14. 测试与验收 `[通用 + 个性化]`

上传测试命令：

```bash
{UPLOAD_TEST_COMMAND}
```

测试要求：

- 正常上传、未认证、权限不足、类型不允许、大小超限必须覆盖。
- MIME 与文件头不一致、伪造扩展名、路径穿越文件名必须覆盖。
- 对象 Key 生成、元数据落库、下载/预览权限必须覆盖。
- 对象存储不可用、超时、写入失败必须有受控错误。
- 大文件、分片、预签名 URL、扫描、转码、导入解析等条件启用能力必须有测试或人工验收步骤。
- 测试文件必须使用 `tests/fixtures/` 或临时目录，不得提交真实用户文件、生产文件或大体积样本。

## 15. AI 修改规则 `[通用]`

AI 修改文件上传相关内容时必须同步检查：

```text
rules/media.md
rules/object-storage.md
rules/security.md
rules/api.md
docs/03-api-index.md
docs/04-database-design.md
docs/standards/file_upload.md
docs/standards/error-codes.md
docs/standards/api-governance.md
docs/06-video-asset-management.md
docs/07-object-storage-strategy.md
tests/
```

要求：

- 不得新增未鉴权或未授权的上传入口。
- 不得让前端直连未授权对象存储。
- 不得绕过 MIME、文件头、大小、权限、配额和业务归属校验。
- 不得把上传文件写入源码目录、Git 跟踪目录或公开静态目录。
- 不得新增未登记的上传错误码。
- 不得保留来源项目 bucket、路径、业务资源、对象 Key、错误码或存储供应商假设。

## 16. 初始化生成建议 `[通用]`

初始化生成本文档时应执行：

1. 根据用户输入替换 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{UPLOAD_ENABLED}`、`{UPLOAD_SCENARIOS}`、`{UPLOAD_METHOD}`、`{UPLOAD_ENDPOINTS}`、`{OBJECT_STORAGE_STACK}`、`{BUCKET_POLICY}`、`{OBJECT_KEY_PATTERN}`。
2. 保留所有 `[通用]` 模块。
3. 根据项目能力保留或删除 `[条件启用]` 模块，例如图片、音频、视频、文档、导入文件、预签名 URL、分片上传、扫描、转码、对象存储。
4. 用真实上传场景、接口、文件类型、大小限制、错误码和元数据字段替换占位；未知信息标记为 `待确认`。
5. 不得编造对象存储供应商、bucket、上传路径、文件大小限制、错误码或元数据表。
6. 保持本文档与 `rules/media.md`、`rules/object-storage.md`、`rules/security.md`、`docs/standards/error-codes.md`、`docs/07-object-storage-strategy.md` 一致。

## 17. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- 新增、删除或调整上传接口、上传方式或上传场景。
- 文件类型、大小限制、MIME 白名单、扫描、转码或安全策略变化。
- 对象存储供应商、bucket 策略、对象 Key、签名 URL 或生命周期变化。
- 上传元数据表、业务对象关联、删除/替换策略变化。
- 上传错误码、前端上传体验、测试命令或验收标准变化。
