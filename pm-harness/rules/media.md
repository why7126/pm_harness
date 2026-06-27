---
purpose: 媒体与文件资产管理规范
content: 规范图片、音频、视频、文档、导出文件、录制文件、转码产物、封面、对象存储、上传安全、前端采集与 AI 更新规则
source: Harness media.md 抽象模板，基于多项目媒体资产规则沉淀
update_method: 项目初始化时按用户输入生成；新增媒体类型、上传限制、录音录像、转码、封面生成、对象存储策略或播放展示能力时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
note: 适用于 {PRODUCT_NAME} 项目；没有媒体/文件上传能力时，本文件可保留为占位规则或在初始化时简化
template_scope: 可作为工程初始化的 media.md 模块
---

# 媒体与文件资产管理规范

## 0. 规则定位 [通用]

本文档用于约束 `{PRODUCT_NAME}` 项目中的媒体与文件资产，包括但不限于：

- 图片、图集、缩略图、封面图。
- 音频、录音、语音样本、转码片段。
- 视频、封面、转码文件、多清晰度版本。
- 文档、附件、导入文件、导出文件。
- 前端录制、上传、预览、播放、下载。
- 对象存储、文件元数据、访问授权、安全校验。

AI 在新增或修改上传、预览、播放、下载、转码、录音录像、文件导入导出、对象存储能力时，必须读取本文档。

### 0.1 初始化占位符 [通用]

| 占位符 | 含义 | 生成要求 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品中文名 | 来自用户输入 |
| `{PRODUCT_CODE}` | 项目代码名 | kebab-case |
| `{PRODUCT_FORMS}` | 产品形态 | Web、微信小程序、移动端、桌面端、H5 等 |
| `{MEDIA_ENABLED}` | 是否启用媒体/文件能力 | 是/否 |
| `{MEDIA_TYPES}` | 媒体类型 | image、audio、video、document、export 等 |
| `{OBJECT_STORAGE_STACK}` | 对象存储 | MinIO、S3、OSS、COS、OBS、RustFS、无 |
| `{MEDIA_BUCKET_POLICY}` | Bucket 策略 | 单 Bucket + 前缀、多 Bucket、文件系统 |
| `{MEDIA_KEY_PATTERN}` | 对象 Key 规范 | 按业务域生成 |
| `{MAX_UPLOAD_POLICY}` | 上传大小限制 | 按媒体类型生成 |
| `{MEDIA_PROCESSING_PIPELINE}` | 处理流程 | 转码、缩略图、封面、ASR、OCR 等 |
| `{FRONTEND_MEDIA_STACK}` | 前端媒体能力 | MediaRecorder、播放器、波形、裁剪等 |

生成初始化工程时，必须替换所有占位符；未知项写 `待确认`，不得保留样例项目的业务对象名。

## 1. 文档模块分类 [通用]

- `[通用]`：所有 Harness 工程默认保留，至少用于说明是否启用媒体能力。
- `[个性化]`：根据产品业务、媒体类型、端能力、存储策略生成。
- `[条件启用]`：仅在对应能力启用时保留，例如图片、音频、视频、录音、转码、对象存储、微信小程序播放。

如果 `{MEDIA_ENABLED}=否`，初始化时可保留规则定位、安全边界、禁止事项和“未启用”说明，删除具体上传/转码/播放强制规则。

## 2. 媒体能力总览 [通用 + 个性化]

初始化时必须生成当前项目的媒体能力矩阵：

```text
{MEDIA_TYPES}
```

推荐矩阵：

| 类型 | 示例 | 是否启用 | 主要用途 | 存储位置 |
|---|---|---:|---|---|
| 图片 | 主图、详情图、头像、封面 | 待确认 | 展示与预览 | 对象存储/文件系统 |
| 音频 | 录音、语音样本、音频片段 | 待确认 | 录制、识别、回放 | 对象存储 |
| 视频 | 介绍视频、演示视频、录屏 | 待确认 | 展示、播放、营销 | 对象存储 |
| 文档 | PDF、Word、规格书、报告 | 待确认 | 附件、下载、导出 | 对象存储 |
| 导入文件 | CSV、XLSX、ZIP | 待确认 | 批量导入 | 临时目录/对象存储 |
| 导出文件 | PDF、Word、Excel、ZIP | 待确认 | 结果导出 | 对象存储/临时目录 |
| 处理产物 | 缩略图、转码、封面、字幕 | 待确认 | 媒体处理结果 | 对象存储 |

未启用的媒体类型不得生成强制环境变量、目录、API 或测试要求。

## 3. 存储策略 [通用 + 个性化]

### 3.1 存储原则 [通用]

- 上传必须经过后端授权，不允许前端绕过后端直接写入未授权对象存储。
- 文件本体存储在对象存储或运行时文件目录，元数据存储在数据库。
- 原始文件名不得直接作为对象 Key 的可信组成部分。
- 对外访问必须使用签名 URL、受控公开策略或后端代理。
- 对象 Key 不得泄露租户、客户、用户隐私或内部路径。
- 上传、处理、导出产生的运行时文件不得提交 Git。

### 3.2 Bucket 策略 [个性化]

对象存储策略：

```text
{OBJECT_STORAGE_STACK}
{MEDIA_BUCKET_POLICY}
```

推荐默认：

```text
一个项目一个 Bucket
桶内按对象前缀区分资源类型
```

示例：

```text
bucket: {PRODUCT_CODE}
```

仅在合规、生命周期、访问策略、成本计费或客户隔离明确要求时，才允许拆分多个 Bucket。

### 3.3 对象 Key 规范 [个性化]

对象 Key 必须由服务端生成，推荐结构：

```text
{domain}/{entity_id}/{media_type}/{media_id}/original.{ext}
{domain}/{entity_id}/{media_type}/{media_id}/thumbnail.{ext}
{domain}/{entity_id}/{media_type}/{media_id}/cover.{ext}
{domain}/{entity_id}/{media_type}/{media_id}/processed/{variant}.{ext}
exports/{job_id}/{filename}.{ext}
tmp/{job_id}/{filename}.{ext}
```

项目初始化时根据业务域生成：

```text
{MEDIA_KEY_PATTERN}
```

规则：

- 不使用用户上传的原始文件名直接拼接路径。
- 不允许 `../`、绝对路径、URL 编码路径穿越。
- Key 中的扩展名应来自服务端校验结果，而不是用户输入。
- 需要多租户时，应加入租户隔离前缀或通过 Bucket/权限隔离。

## 4. 上传规范 [通用 + 个性化]

### 4.1 上传入口 [通用]

- 上传入口必须经过鉴权。
- 上传前必须校验权限、业务归属、配额和大小限制。
- 上传后必须记录文件元数据。
- 大文件上传应使用分片、流式处理或直传授权机制。
- 前端直传对象存储仅允许使用后端签发的临时凭证或预签名 URL。

### 4.2 格式与大小限制 [个性化]

初始化时生成：

```text
{MAX_UPLOAD_POLICY}
```

推荐示例：

| 类型 | 格式 | 大小限制 | 说明 |
|---|---|---:|---|
| 图片 | JPEG、PNG、WebP | 待确认 | 需校验 MIME 和扩展名 |
| 音频 | WAV、MP3、M4A、FLAC、OGG、WebM | 待确认 | 录音和算法处理按需转码 |
| 视频 | MP4、MOV、WebM | 待确认 | 微信小程序/移动端需控制体积 |
| 文档 | PDF、DOCX、XLSX | 待确认 | 需病毒扫描或安全检查 |
| 压缩包 | ZIP | 待确认 | 必须防 Zip Slip 和炸弹文件 |

所有限制必须同步 `rules/environment.md` 中的环境变量，例如：

```ini
MAX_UPLOAD_SIZE_MB=100
ALLOWED_IMAGE_TYPES=image/jpeg,image/png,image/webp
ALLOWED_VIDEO_TYPES=video/mp4,video/webm
```

## 5. 图片规范 [条件启用]

启用图片能力时：

- 必须生成缩略图或明确不生成的原因。
- 必须校验真实 MIME、扩展名、文件头。
- 应剥离或限制 EXIF 中的定位、设备等敏感信息。
- 前端展示应使用合适尺寸，不直接加载超大原图。
- 图片裁剪、压缩、格式转换必须保留原始文件或说明覆盖策略。

推荐对象前缀：

```text
images/{entity_id}/original/{image_id}.{ext}
images/{entity_id}/thumbnails/{image_id}.{ext}
images/{entity_id}/processed/{image_id}-{variant}.{ext}
```

## 6. 音频与录音规范 [条件启用]

启用音频、录音、语音样本或 ASR 能力时：

- 上传音频必须校验 MIME、扩展名、大小、时长。
- 在线录音必须使用安全上下文，例如 HTTPS 或 localhost。
- Web 录音可使用 `navigator.mediaDevices.getUserMedia()` 与 MediaRecorder API。
- 本地临时录音可使用 IndexedDB 或应用私有存储，不得提交 Git。
- 算法处理格式必须在文档中明确，例如 `WAV 16kHz mono`。
- 声纹、语音、会议录音等通常属于敏感数据，必须遵循 `rules/data-management.md`。

推荐对象前缀：

```text
audio/{entity_id}/original/{audio_id}.{ext}
audio/{entity_id}/segments/{segment_id}.wav
audio/{entity_id}/transcoded/{audio_id}.wav
voice/{user_id}/samples/{sample_id}.wav
```

## 7. 视频规范 [条件启用]

启用视频能力时：

- 默认推荐 MP4/H.264 或项目明确支持格式。
- 上传视频后应支持封面上传或封面生成。
- 视频大小、时长、分辨率必须受环境变量或配置控制。
- 移动端、微信小程序、弱网场景必须控制视频体积和首屏加载。
- 转码、多清晰度、截图、压缩可作为阶段性能力，不应阻塞基础上传管理流程，除非需求明确要求。
- 播放 URL 必须受权限控制，不得暴露未授权资源。

推荐对象前缀：

```text
videos/{entity_id}/{video_id}/source.{ext}
videos/{entity_id}/{video_id}/cover.{ext}
videos/{entity_id}/{video_id}/transcoded/{profile}.{ext}
videos/{entity_id}/{video_id}/thumbnails/{timestamp}.jpg
```

推荐阶段：

1. V1：上传、封面、播放、删除。
2. V2：自动截帧、压缩、元数据提取。
3. V3：转码、多清晰度、字幕、异步处理。

## 8. 文档、附件与导出文件 [条件启用]

启用文档、附件、导入导出时：

- 必须校验 MIME、扩展名、大小。
- 必须防止路径穿越、宏病毒、压缩包炸弹、Zip Slip。
- 导出文件应设置过期时间或清理策略。
- 敏感导出文件必须鉴权下载，不得长期公开。
- 预览转换产物应按处理产物管理。

推荐对象前缀：

```text
documents/{entity_id}/{document_id}.{ext}
imports/{job_id}/source.{ext}
exports/{job_id}/result.{ext}
exports/{job_id}/preview/{page}.png
```

## 9. 媒体处理流水线 [条件启用]

媒体处理流水线：

```text
{MEDIA_PROCESSING_PIPELINE}
```

常见处理：

| 类型 | 处理能力 | 说明 |
|---|---|---|
| 图片 | 缩略图、压缩、裁剪、格式转换 | 可同步或异步 |
| 音频 | 转码、切片、降噪、ASR、声纹 | 通常异步 |
| 视频 | 封面、转码、压缩、多清晰度 | 通常异步 |
| 文档 | 预览图、文本抽取、OCR | 按需启用 |

规则：

- 处理任务必须可追踪状态。
- 失败应记录错误码和可重试策略。
- 原始文件与处理产物的关系必须写入元数据。
- 异步任务不得阻塞上传接口太久。
- 处理产物不得直接提交 Git。

## 10. 数据库元数据 [通用 + 个性化]

媒体文件必须有元数据记录。推荐字段：

```text
id
owner_type / owner_id
media_type
storage_provider
bucket
object_key
original_filename
safe_filename
mime_type
file_ext
file_size
checksum
duration
width
height
cover_object_key
status
sort_order
created_by
created_at
updated_at
deleted_at
```

字段是否启用根据媒体类型裁剪：

- 图片启用 `width`、`height`、缩略图字段。
- 音频/视频启用 `duration`。
- 视频启用 `cover_object_key`。
- 文档启用页数、预览状态等扩展字段。

数据库设计必须同步 `rules/database.md` 和 `docs/04-database-design.md`。

## 11. 前端媒体能力 [条件启用]

前端媒体能力：

```text
{FRONTEND_MEDIA_STACK}
```

启用前端上传、录音、播放、预览时：

- 上传组件必须显示大小、格式、进度、失败原因。
- 大文件上传必须支持取消、重试或恢复策略。
- 播放器必须处理加载失败、权限失效、签名 URL 过期。
- Web 录音/录像必须检查浏览器权限和安全上下文。
- 微信小程序/移动端必须考虑网络、缓存、文件大小和平台限制。
- 前端不得持久保存未授权访问凭证。

## 12. 访问控制与 URL [通用]

- 默认使用私有对象存储。
- 对外访问使用后端鉴权代理、签名 URL 或受控公开策略。
- 签名 URL 有效期必须可配置。
- 删除或权限变更后，旧 URL 应尽快失效或不可访问。
- 不得把永久公开 URL 用于敏感媒体。
- 多租户项目必须校验租户归属。

## 13. 安全规则 [通用]

必须防护：

- MIME 伪造。
- 扩展名伪造。
- 路径穿越。
- 超大文件和资源耗尽。
- 压缩包炸弹和 Zip Slip。
- 未授权上传、下载、预览。
- 公开 URL 泄漏。
- EXIF、音频、视频、文档中的敏感元数据泄漏。
- 上传可执行脚本或危险文件。

高风险文件类型默认拒绝，除非业务明确要求且有隔离处理。

## 14. 本地开发、测试与数据边界 [通用]

- 本地上传文件进入 `data/uploads/` 或对象存储，不提交 Git。
- 处理产物进入 `data/processed/` 或对象存储，不提交 Git。
- 临时文件进入 `data/tmp/`，可清理。
- 测试 fixtures 放入 `tests/fixtures/`，必须脱敏、可公开、体积可控。
- 大型媒体样例使用生成脚本、下载说明或小体积 dummy 文件。
- 真实用户图片、音频、视频、文档不得作为测试数据提交。

相关规则以 `rules/data-management.md` 为准。

## 15. 环境变量 [通用 + 条件启用]

媒体相关环境变量必须同步 `rules/environment.md` 和 `.env.example`。

推荐变量：

```ini
MEDIA_ENABLED=true
STORAGE_TYPE=minio
MINIO_BUCKET={PRODUCT_CODE}
MAX_UPLOAD_SIZE_MB=100
MAX_IMAGE_SIZE_MB=20
MAX_AUDIO_SIZE_MB=500
MAX_VIDEO_SIZE_MB=1024
MEDIA_SIGNED_URL_EXPIRE_SECONDS=900
MEDIA_PROCESSING_ENABLED=false
VIDEO_TRANSCODE_ENABLED=false
VIDEO_THUMBNAIL_ENABLED=true
```

未启用媒体能力时，不得生成强制必填的媒体环境变量。

## 16. AI 更新规则 [通用]

AI 新增或修改媒体能力时，必须同步检查：

```text
rules/media.md
rules/object-storage.md
rules/data-management.md
rules/environment.md
rules/security.md
rules/api.md
docs/06-*-asset-management.md
docs/standards/file_upload.md
docs/04-database-design.md
docs/05-compatibility-matrix.md
openspec/changes/<change-id>/
openspec/specs/<media-or-domain>/spec.md
.env.example
docker-compose.yml
src/backend/**/media*
src/backend/**/storage*
src/web/**/media*
src/wechat-miniapp/**/*
tests/integration/media/
tests/fixtures/
```

具体路径必须根据项目实际目录生成，不得保留不存在的样例路径。

## 17. 禁止事项 [通用]

- 禁止前端绕过后端授权直接写入对象存储。
- 禁止使用用户原始文件名直接生成对象 Key。
- 禁止只校验扩展名，不校验 MIME 和文件头。
- 禁止将真实媒体文件、生产上传文件、转码产物提交 Git。
- 禁止公开敏感媒体的永久 URL。
- 禁止把对象存储密钥放入前端公开变量。
- 禁止在未更新 `.env.example`、docs、OpenSpec、测试的情况下新增媒体能力。
- 禁止保留样例项目业务媒体类型、Bucket、Key 前缀。

## 18. 初始化生成建议 [通用]

将本文档作为工程初始化模块时，生成器应按以下步骤处理：

1. 根据 `{MEDIA_ENABLED}` 决定保留完整媒体规则或生成未启用占位说明。
2. 根据 `{MEDIA_TYPES}` 保留图片、音频、视频、文档、导入导出、处理产物章节。
3. 根据 `{OBJECT_STORAGE_STACK}` 生成对象存储、Bucket、Key、签名 URL 规则；无对象存储时改为文件系统策略。
4. 根据 `{PRODUCT_FORMS}` 生成 Web、微信小程序、移动端、桌面端的上传、预览、播放限制。
5. 根据 `{MEDIA_PROCESSING_PIPELINE}` 生成转码、缩略图、封面、ASR、OCR、异步任务规则。
6. 根据 `{MAX_UPLOAD_POLICY}` 生成大小、格式、时长、分辨率限制。
7. 根据 `{FRONTEND_MEDIA_STACK}` 生成前端录音、播放器、波形、上传组件规则。
8. 删除未启用能力的强制变量、路径、测试和 OpenSpec 要求。
9. 检查本文档与 `object-storage.md`、`data-management.md`、`environment.md`、`api.md`、`database.md`、`security.md` 一致。

## 19. 完成任务后检查清单 [通用]

```text
□ 媒体能力矩阵已按项目实际生成
□ [通用]、[个性化]、[条件启用] 模块标识完整
□ 存储策略、Bucket 策略、对象 Key 规范清晰
□ 上传格式、大小、MIME、文件头、安全校验明确
□ 图片、音频、视频、文档章节已按启用能力裁剪
□ 媒体处理流水线、元数据、访问控制、签名 URL 规则完整
□ 环境变量与 .env.example、object-storage、data-management 保持一致
□ AI 更新规则覆盖 docs、OpenSpec、代码、测试、部署
□ 未保留样例项目业务媒体类型、Bucket 或 Key 前缀
```
