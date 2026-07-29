---
purpose: 对象存储策略
content: 对象存储供应商、桶策略、目录前缀、对象 Key、权限、生命周期和迁移规范
source: Harness docs Token 优化模板，初始化时基于对象存储栈生成
update_method: 对象存储供应商、桶策略、Key、权限、生命周期或迁移策略变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-07-14 00:00:00
owner: {DOCS_OWNER}
note: 启用对象存储时完整维护；未启用时保留为占位说明
---

# 对象存储策略

## 1. 当前策略

对象存储栈：

```text
{OBJECT_STORAGE_STACK}
```

默认推荐：

```text
一个项目一个 Bucket
桶内使用目录前缀区分资源类型
```

Bucket：

```text
{OBJECT_STORAGE_BUCKET}
```

## 2. 标准前缀

| 前缀 | 用途 |
|---|---|
| `images/` | 图片类上传 |
| `videos/` | 原始视频 |
| `files/` | 文档附件 |
| `audios/` | 音频 |
| `thumbnails/` | 缩略图 |
| `processed/` | 处理后资源 |
| `tmp/` | 临时文件 |
| `imports/` | 批量导入文件 |
| `exports/` | 导出文件 |
| `videos/covers/` | 视频封面 |
| `videos/transcoded/` | 转码后视频 |

## 3. Object Key

推荐形态：

```text
{prefix}/{tenant}/{resource_type}/{uuid}.{ext}
```

禁止使用用户原始文件名、真实身份信息、未经校验的路径片段或含密钥的 URL 作为对象 Key。

## 4. 访问方式

- 上传必须经过后端鉴权和校验。
- 读取通过后端受控 URL、签名 URL 或明确授权的公开策略。
- 前端不得直连未授权对象存储写入。
- 生产凭据必须通过安全渠道注入，不写入 Git。

## 5. 何时考虑多桶

只有在生命周期策略、权限隔离、合规要求、成本归集或资源规模明确要求时，才通过 OpenSpec Change 引入多桶。

## 6. 更新清单

对象存储策略变化时同步：

```text
□ rules/object-storage.md
□ docs/07-object-storage-strategy.md
□ docs/02-deployment.md
□ .env.example
□ compatibility/object-storage/
□ 上传 / 下载 / 清理测试
```
