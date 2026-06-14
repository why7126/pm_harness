---
purpose: 对象存储使用规范
content: 规定 MinIO 桶、对象Key、目录前缀、权限、生命周期与AI更新要求
source: 人工编写 + AI辅助生成
update_method: 对象存储策略变化时由技术负责人确认后更新
note: V5 推荐一个项目一个 Bucket，桶内使用目录前缀区分业务资源
---

# 对象存储规范

## 1. 总原则

本项目使用 MinIO 作为对象存储。V5 采用：

```text
一个项目一个 Bucket
桶内按对象前缀区分资源类型
```

默认：

```text
MINIO_BUCKET=tile-info-platform
```

不推荐按资源拆成多个桶，例如 `tile-original`、`tile-thumbnail`、`tile-video`。

## 2. 标准对象前缀

```text
original/              原始上传文件
thumbnails/            图片缩略图
processed/             处理后的图片或文件
tmp/                   临时文件
imports/               批量导入文件
exports/               导出文件
videos/                原始视频
videos/covers/         视频封面
videos/transcoded/     转码后视频
```

## 3. AI必须遵守

AI 在新增文件上传、视频上传、图片处理、导入导出能力时：

1. 不允许新增多个业务 Bucket，除非 OpenSpec 明确要求；
2. 必须复用 `.env.example` 中的 `MINIO_BUCKET`；
3. 必须使用标准前缀；
4. 必须更新媒体资源相关 OpenSpec 和文档；
5. 必须补充对象Key生成逻辑和测试。
