---
purpose: RustFS 对象存储兼容适配说明
content: RustFS 使用范围、S3 兼容能力、Bucket、Key、权限、签名 URL、生命周期、测试矩阵和初始化生成规则
source: Harness compatibility/object-storage/rustfs.md 抽象模板
update_method: RustFS 版本、Endpoint、权限、生命周期或上传下载策略变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {OBJECT_STORAGE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/object-storage/rustfs.md 模块
---

# RustFS 适配说明

> **[通用]** 默认保留结构；**[个性化]** 根据项目生成；**[条件启用]** 仅在使用 RustFS 时保留。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 使用 RustFS 时的 S3 兼容能力、Bucket、Key、签名 URL、权限、生命周期和测试要求。

## 1. 初始化参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{RUSTFS_VERSION}` | RustFS 版本 | 待确认 |
| `{RUSTFS_ENDPOINT}` | Endpoint | 待确认 |
| `{RUSTFS_BUCKET}` | Bucket | 待确认 |
| `{SIGNED_URL_POLICY}` | 签名 URL 策略 | 待确认 |
| `{RUSTFS_TEST_COMMAND}` | 测试命令 | 待确认 |

## 2. 兼容重点 `[通用]`

- RustFS 的 S3 兼容能力必须按项目实际使用 API 验证。
- 分片上传、签名 URL、生命周期、元数据和权限策略不得默认等同 MinIO 或 AWS S3。
- 私有化部署必须记录备份、恢复、监控和容量策略。

## 3. 初始化生成规则 `[通用]`

启用 RustFS 时保留本文；否则删除或标记为不适用。不得编造版本、Endpoint、Bucket 或测试结果。
