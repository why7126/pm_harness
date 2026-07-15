---
purpose: 发布规范
content: 发布对象、公告、版本号、发布前门禁和回滚记录
source: Harness Token 优化模板
update_method: 发布流程、版本策略或发布命令族变化时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-14 00:00:00
note: 适用于启用 releases/ 的项目
---

# 发布规范

发布前必须完成测试、OpenSpec 校验、接口生成、变更归档和发布说明。

## 1. 产品版本发布对象

产品版本发布对象用于表达一次对外产品发版，推荐放入：

```text
releases/vX.Y.Z/release.json
```

发布对象 MUST 支持：

- 一个产品版本关联一个或多个 Sprint。
- 追踪关联 REQ、BUG 和 OpenSpec Change。
- 区分 Sprint release note 与产品版本公告。
- 阻止未评审、未纳入交付或未归档闭环的内容进入正式发布范围。

## 2. 公开发布公告

公开发布公告源文件推荐放入：

```text
releases/vX.Y.Z/announcement.md
```

公告 MUST 包含版本号、发布时间、关联 Sprint、新增功能、修复 BUG、发布注意事项、已知问题、升级步骤、回滚说明和影响范围。

公告 MUST NOT 泄露密钥、真实客户数据、内部数据库连接串、对象存储凭据、不可公开域名或敏感运维信息。

## 3. 发布前门禁

| 门禁 | 要求 |
|---|---|
| OpenSpec | 关联 Change 已 archive，相关能力已合并到 `openspec/specs/` |
| 测试 | 按变更范围执行并记录结果 |
| API / 客户端 | 涉及 API 变更时，OpenAPI 与客户端生成物已同步 |
| Docker Compose | 涉及部署变更时，Compose 配置与部署文档已同步 |
| 数据库 | 涉及数据库迁移时，迁移脚本、数据库文档和回滚说明已同步 |
| 环境变量 | 涉及环境变量时，`.env.example` 与注释已同步 |
| 产品版本 | 用户可见版本号与发布对象版本一致；如不更新，必须记录原因 |

任一必填门禁失败时，发布流程 MUST 阻断，并输出失败原因与修复建议。

## 4. 发布命令族

推荐命令：

| 命令 | 目标 |
|---|---|
| `/release-propose <version>` | 创建或更新产品版本发布计划 |
| `/release-prepare <version>` | 执行发布前校验，生成或更新公告源文件 |
| `/release-publish <version>` | 记录发布确认结果和最终公告位置 |
