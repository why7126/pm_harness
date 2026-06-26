---
purpose: 阿里云 OSS 对象存储兼容适配说明
content: OSS 使用范围、Bucket、Region、权限、签名 URL、生命周期、测试矩阵和初始化生成规则
source: Harness compatibility/object-storage/oss.md 抽象模板
update_method: OSS Region、Bucket、权限、生命周期或上传下载策略变化时更新
owner: {OBJECT_STORAGE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/object-storage/oss.md 模块
---

# 阿里云 OSS 适配说明

> **[通用]** 默认保留结构；**[个性化]** 根据项目生成；**[条件启用]** 仅在使用阿里云 OSS 时保留。

## 0. 文档定位 `[通用]`

本文定义 `{PRODUCT_NAME}` 使用阿里云 OSS 时的 Endpoint、Bucket、Key、签名 URL、权限、生命周期和测试要求。

## 1. 初始化参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{OSS_ENDPOINT}` | Endpoint | 待确认 |
| `{OSS_REGION}` | Region | 待确认 |
| `{OSS_BUCKET}` | Bucket | 待确认 |
| `{SIGNED_URL_POLICY}` | 签名 URL 策略 | 待确认 |
| `{OSS_TEST_COMMAND}` | 测试命令 | 待确认 |

## 2. 兼容重点 `[通用]`

- OSS SDK、STS 临时凭证、签名 URL、跨域、生命周期和权限策略必须实际验证。
- 公开读写必须禁止，除非有明确业务和安全审批。
- 对象 Key 不得包含敏感信息。

## 3. 初始化生成规则 `[通用]`

启用 OSS 时保留本文；否则删除或标记为不适用。不得编造阿里云账号、Bucket 或测试结果。
