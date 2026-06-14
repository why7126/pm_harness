---
purpose: 对象存储策略说明
content: 说明 MinIO 单桶策略、目录前缀、资源类型、迁移与维护规范
source: AI自动生成，人工确认
update_method: 对象存储策略或媒体资源类型变化时更新
note: V5 从多桶策略调整为单桶 + 前缀策略
---

# 对象存储策略

## 1. 当前策略

本项目使用 MinIO，采用：

```text
一个项目一个 Bucket
桶内使用二级目录/前缀区分资源类型
```

默认：

```text
MINIO_BUCKET=tile-info-platform
```

## 2. 目录前缀

| 前缀 | 用途 |
|---|---|
| `original/` | 原始图片、文件 |
| `thumbnails/` | 缩略图 |
| `processed/` | 处理后的资源 |
| `tmp/` | 临时文件 |
| `imports/` | 批量导入文件 |
| `exports/` | 导出文件 |
| `videos/` | 原始视频 |
| `videos/covers/` | 视频封面 |
| `videos/transcoded/` | 转码后视频 |

## 3. 适用原因

瓷砖信息管理平台的媒体资源主要围绕同一个业务域，单桶便于部署、迁移、备份和权限管理。

## 4. 何时考虑多桶

只有在生命周期策略、权限隔离、合规要求或资源规模明确要求时，才通过 OpenSpec Change 引入多桶。
