---
purpose: 对象存储兼容模块入口
content: 说明 object-storage 目录下各供应商适配文档的职责、启用条件、通用边界和初始化生成规则
source: Harness compatibility/object-storage/README.md 抽象模板
update_method: 新增对象存储供应商、上传下载策略、生命周期或部署模式时更新
owner: {OBJECT_STORAGE_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/object-storage/README.md 模块
---

# 对象存储兼容模块

> **[通用]** 默认保留；**[个性化]** 根据项目生成；**[条件启用]** 仅保留启用供应商。

## 0. 目录定位 `[通用]`

本目录保存对象存储供应商级兼容说明。通用策略见 `rules/object-storage.md` 和 `docs/07-object-storage-strategy.md`。

## 1. 模块清单 `[条件启用]`

| 供应商 | 文件 | 启用条件 |
|---|---|---|
| MinIO | `minio.md` | 本地开发、测试、私有化或 S3 兼容存储 |
| AWS S3 / S3 Compatible | `s3.md` | 云 S3 或通用 S3 兼容 |
| 腾讯 COS | `cos.md` | 腾讯云对象存储 |
| 阿里云 OSS | `oss.md` | 阿里云对象存储 |
| 华为 OBS | `obs.md` | 华为云对象存储 |
| RustFS | `rustfs.md` | 私有化 RustFS |

## 2. 通用生成规则 `[通用]`

- 业务代码不得直接依赖供应商 SDK，必须通过 Storage Adapter 封装。
- Bucket、Key、签名 URL、权限、生命周期和测试结果必须按供应商记录。
- 未启用供应商不得保留强制配置和测试要求。
- 不得写入真实 Access Key、Secret Key、生产 Endpoint 或 Bucket。
