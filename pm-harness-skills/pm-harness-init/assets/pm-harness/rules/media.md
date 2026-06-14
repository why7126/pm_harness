---
purpose: 图片与视频媒体资产管理规范
content: 瓷砖图片、视频、封面、转码、上传、MinIO存储、前端展示和安全限制
source: AI自动生成初稿，项目团队确认
update_method: 新增媒体类型、视频转码、封面生成、上传限制、对象存储策略时更新
note: 适用于Web展示端、微信小程序和管理端的媒体资产处理
---

# 媒体资产管理规范

## 1. 媒体类型

本项目支持：

- 瓷砖主图
- 瓷砖详情图
- 瓷砖铺贴效果图
- 瓷砖介绍视频
- 瓷砖工艺/质检视频
- 视频封面图
- 规格书和检测报告附件

## 2. 存储规则

媒体文件必须通过后端授权上传到 MinIO，不允许前端绕过后端直接写入未授权对象存储。

推荐存储桶：

```text
tile-images
tile-videos
tile-documents
```

推荐对象Key：

```text
tiles/{tile_id}/images/{image_id}.{ext}
tiles/{tile_id}/videos/{video_id}/source.{ext}
tiles/{tile_id}/videos/{video_id}/cover.{ext}
tiles/{tile_id}/documents/{document_id}.{ext}
```

## 3. 视频规范

- 默认推荐MP4格式。
- 管理端上传视频后，应生成或上传封面图。
- 视频文件大小必须受环境变量控制。
- 小程序端展示视频时必须考虑网络和体积限制。
- 视频转码能力可作为可选能力，不应阻塞基础上传管理流程。

## 4. 安全规则

- 必须校验MIME Type和扩展名。
- 必须限制文件大小。
- 必须防止路径穿越。
- 必须隔离原始文件名和对象存储Key。
- 对外访问应使用签名URL或受控公开策略。

## 5. AI更新规则

AI新增或修改媒体能力时，必须同步更新：

```text
.env.example
data/README.md
docs/06-video-asset-management.md
openspec/specs/media-assets/spec.md
src/backend/app/modules/media/
src/web/src/features/media/
src/miniapp/pages/tile-detail/
tests/integration/media/
```
