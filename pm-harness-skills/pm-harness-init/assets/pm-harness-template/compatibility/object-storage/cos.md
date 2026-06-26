---
purpose: 腾讯 COS 对象存储兼容适配说明
content: COS 使用范围、Bucket、Region、权限、签名 URL、生命周期、测试矩阵和初始化生成规则
source: Harness compatibility/object-storage/cos.md 抽象模板
update_method: COS Region、Bucket、权限、生命周期或上传下载策略变化时更新
owner: {OBJECT_STORAGE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/object-storage/cos.md 模块
---

# 腾讯 COS 适配说明

> **[通用]** 默认保留结构；**[个性化]** 根据项目生成；**[条件启用]** 仅在使用腾讯 COS 时保留。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 使用腾讯 COS 时的 Region、Bucket、Key、签名 URL、权限、生命周期和测试要求。

## 1. 初始化参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{COS_REGION}` | Region | 待确认 |
| `{COS_BUCKET}` | Bucket | 待确认 |
| `{COS_APP_ID}` | AppID | 待确认 |
| `{SIGNED_URL_POLICY}` | 签名 URL 策略 | 待确认 |
| `{COS_TEST_COMMAND}` | 测试命令 | 待确认 |

## 2. 兼容重点 `[通用]`

- COS SDK 与 S3 兼容模式必须二选一并记录。
- 签名 URL、跨域、Content-Type、中文文件名、生命周期和权限策略必须测试。
- 密钥不得进入前端或模板默认值。

## 3. 初始化生成规则 `[通用]`

启用 COS 时保留本文；否则删除或标记为不适用。不得编造腾讯云账号、Bucket 或测试结果。
