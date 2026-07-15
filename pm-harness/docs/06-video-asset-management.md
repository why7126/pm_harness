---
purpose: 视频与富媒体资产管理
content: 视频/图片/附件上传、存储、封面、转码、预览、端适配和测试规则
source: Harness docs Token 优化模板，初始化时基于媒体能力生成
update_method: 媒体类型、上传、转码、封面、播放、存储或端适配策略变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-07-14 00:00:00
owner: {DOCS_OWNER}
note: 启用媒体/视频能力时完整维护；未启用时保留为占位说明
---

# 视频与富媒体资产管理

## 1. 业务场景

项目可能需要管理：

```text
images
videos
audios
files
thumbnails
covers
processed assets
```

具体媒体类型由 OpenSpec 明确。

## 2. 使用端

| 端 | 能力 |
|---|---|
| Web / Admin | 上传、维护、预览、删除 |
| Mobile / H5 | 预览、播放、下载 |
| 小程序 | 轻量化预览、播放、平台能力适配 |
| Backend | 校验、存储、元数据、受控读取 |

## 3. 存储设计

媒体文件应通过后端授权上传到对象存储：

```text
bucket: {OBJECT_STORAGE_BUCKET}
key: {prefix}/{tenant}/{resource_type}/{uuid}.{ext}
```

对象前缀和 Key 规则见 [07-object-storage-strategy.md](07-object-storage-strategy.md) 与 `rules/object-storage.md`。

## 4. 元数据

媒体元数据 SHOULD 记录：

```text
media_type
object_key
mime_type
file_size
width
height
duration
cover_object_key
sort_order
created_at
```

具体表结构见 [04-database-design.md](04-database-design.md)。

## 5. 阶段建议

1. V1：上传、校验、元数据、受控读取、基础预览。
2. V2：封面、缩略图、排序、批量管理。
3. V3：转码、压缩、多清晰度、生命周期清理。

## 6. AI 更新要求

媒体需求进入开发时，必须检查：

```text
□ openspec/changes/<change-id>/
□ rules/media.md
□ rules/object-storage.md
□ .env.example
□ data/README.md
□ docs/06-video-asset-management.md
□ 后端媒体模块
□ 前端上传 / 预览模块
□ 集成测试与安全测试
```
