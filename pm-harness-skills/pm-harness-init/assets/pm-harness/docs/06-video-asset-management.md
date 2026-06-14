---
purpose: 视频资产管理说明
content: 瓷砖视频上传、存储、封面、转码、预览、前端展示、小程序适配和测试规则
source: AI自动生成初稿，项目团队确认
update_method: 视频上传、转码、封面、播放、存储策略变化时更新
note: 本文档用于指导视频相关需求、开发、测试和验收
---

# 视频资产管理说明

## 1. 业务场景

瓷砖信息管理平台可能需要通过视频展示：

- 瓷砖铺贴效果
- 产品细节纹理
- 生产工艺
- 防滑、耐磨等测试过程
- 门店营销素材

## 2. 使用端

| 端 | 视频能力 |
|---|---|
| Web展示端 | 查看瓷砖介绍视频 |
| 微信小程序 | 查看轻量化视频、封面预览 |
| 管理端Web | 上传、维护、排序、删除视频 |

## 3. 存储设计

视频原文件存储在 MinIO：

```text
bucket: tile-videos
key: tiles/{tile_id}/videos/{video_id}/source.mp4
```

视频封面存储在：

```text
bucket: tile-videos
key: tiles/{tile_id}/videos/{video_id}/cover.jpg
```

## 4. 数据库元数据

视频应作为 `tile_media` 的一种类型记录：

```text
media_type = video
duration
cover_object_key
mime_type
file_size
sort_order
```

## 5. 初始化阶段建议

V4模板默认只提供视频管理目录和规范，不强制接入真实转码服务。

推荐阶段：

1. V1：支持视频上传、封面上传、播放。
2. V2：支持自动截帧生成封面。
3. V3：支持转码、压缩、多清晰度。

## 6. AI更新要求

视频需求进入开发时，AI必须创建或更新：

```text
openspec/changes/<change-id>/
openspec/specs/media-assets/spec.md
rules/media.md
.env.example
data/README.md
src/backend/app/modules/media/
src/web/src/features/media/
tests/integration/media/
```
