---
purpose: 文件上传规范
content: 图片/视频/附件上传流程与返回结构
source: rules/media.md / build-api-standard
update_method: 上传能力变更时同步更新
---

# 文件上传规范

## 原则

- 前端 **禁止** 直连未授权 MinIO
- 上传 MUST 经后端 `multipart/form-data` 接口
- 存储：单桶 `tile-info-platform` + 前缀（见 `project.yaml`）

## 请求

```http
POST /api/v1/uploads/images
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <binary>
```

## 成功响应

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "media_id": "uuid",
    "object_key": "original/...",
    "url": "https://...",
    "mime_type": "image/jpeg",
    "size": 102400
  }
}
```

视频上传额外可含 `duration`、`cover_url`（若已实现）。

## 限制

- MIME 白名单：见 `.env.example`
- 大小上限：见 `MAX_UPLOAD_SIZE_MB`
- 错误码：`50002`、`50003`、`50001`

## 相关

- `rules/object-storage.md`
- `rules/media.md`
- `docs/06-video-asset-management.md`
