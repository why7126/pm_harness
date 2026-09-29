---
purpose: 发布规范
content: 发布对象、公告、版本号、发布前门禁和回滚记录
source: Harness Token 优化模板
update_method: 发布流程、版本策略或发布命令族变化时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-31 17:10:00
note: 适用于启用 releases/ 的项目
---

# 发布规范

发布前必须完成测试、OpenSpec 校验、接口生成、变更归档、发布对象、公告源文件和发布说明。

## 1. 发版检查清单

对外发布产品版本时，若本次发版包含用户可见版本语义变更，MUST 人工更新项目内唯一的用户可见版本事实源，例如：

```text
src/shared/product-version.ts -> PRODUCT_VERSION
```

MUST NOT 依赖 `package.json`、后端应用版本、OpenAPI 版本、Git commit 或 CI 构建号作为用户可见产品版本。若项目尚未建立版本事实源，`release.json` 的 `gates.product_version` 可为 `na`，但必须写明原因。

## 2. 产品版本发布对象

产品版本发布对象用于表达一次对外产品发版，推荐放入：

```text
releases/vX.Y.Z/release.json
```

发布对象 MUST 支持：

- 一个产品版本关联一个或多个 Sprint。
- 追踪关联 REQ、BUG 和 OpenSpec Change。
- 区分 Sprint release note 与产品版本公告。
- 阻止未评审、未纳入交付或未归档闭环的内容进入正式发布范围。
- 记录影响范围、发布门禁证据、升级步骤、回滚策略和已知问题。

## 3. 公开发布公告

公开发布公告源文件推荐放入：

```text
releases/vX.Y.Z/announcement.mdx
```

公告 MUST 面向公开页面或客户交付展示，可使用 Mintlify 或等价静态文档预览校验。公告 MUST 包含版本号、发布时间、关联 Sprint、新增功能、修复 BUG、发布注意事项、已知问题、升级步骤、回滚说明和影响范围。

公告 MUST NOT 泄露密钥、真实客户数据、内部数据库连接串、对象存储凭据、不可公开域名或敏感运维信息。

## 4. 发布前门禁

| 门禁 | 要求 |
|---|---|
| OpenSpec | 关联 Change 已 archive，相关能力已合并到 `openspec/specs/`；未归档项不得进入正式发布范围 |
| 测试 | 按变更范围执行并记录结果 |
| API / 客户端 | 涉及 API 变更时，OpenAPI 与客户端生成物（如 Orval）已同步 |
| Docker Compose | 涉及部署变更时，Compose 配置与部署文档已同步 |
| 数据库 | 涉及数据库迁移或 schema 影响时，迁移脚本、数据库文档、目标 MySQL schema drift / smoke 或等价校验证据、回滚或备份说明已同步 |
| 环境变量 | 涉及环境变量时，`.env.example` 与注释已同步 |
| 产品版本 | 用户可见版本号与发布对象版本一致；如不更新，必须记录原因 |
| 公告预览 | 公告 build、preview 或等价静态文档校验通过 |
| 镜像准备 | 当 `image_required=true` 时，`releases/<version>/image-build-plan.json` 已生成、校验通过并被 `release.json` 引用 |
| 镜像构建 | 当 `image_required=true` 或包含离线镜像交付时，`releases/<version>/image-manifest.json` 已生成、未过期并被 `release.json` 引用；外部构建证据必须受控 |

任一必填门禁失败时，发布流程 MUST 阻断，并输出失败原因与修复建议。

当发布范围涉及后端运行代码、Web 构建产物、Dockerfile、Compose、`.env.example`、镜像构建脚本、构建 env 示例、数据库 schema / migration、API / 客户端生成物或离线镜像交付时，发布对象 MUST 将 `image_required` 设为 `true`，并按以下顺序执行：

```text
/release-propose <version>
  -> /release-prepare <version>
  -> /image-prepare <version>
  -> /image-build <version>
  -> /release-publish <version>
```

`/image-prepare` 只生成或更新 `releases/<version>/image-build-plan.json`，记录版本、image tag、source scope、release stable input hash、build env 安全摘要、Dockerfile、Compose、构建脚本、构建 env 示例、Nginx、schema、migration、数据库文档 input hash、required commands、auto actions、warnings 和 blockers。默认构建 env 缺失或 `IMAGE_BUILD_TAG` 与版本不一致时，命令 MAY 只自动创建/更新安全白名单变量并记录 auto action。Compose fallback image tag 与当前版本不同但实际发布 env 明确设置项目级 image tag 变量时 SHOULD 记录 warning，不得作为 blocker 要求每次 release 改 Compose 默认值。Docker 不可用、网络不可用、构建 env 示例异常、自动修正后仍版本不一致或真实构建前置条件不满足时可以写 blocked plan，但不得写 pass 证据。

`/image-build` MUST 读取有效且未过期的 image build plan 后再复用 `scripts/build-images.sh` 执行真实构建。构建成功后写入 `releases/<version>/image-manifest.json`，记录 version、image_tag、built_at、platform、backend_image、web_image、tarball、input_hashes、validation 和 source_plan。镜像 tar 包与 `.sha256` MUST 默认输出到仓库外 `../releases/<version>/images/`，不得提交到仓库内 `releases/`。缺少 plan、plan blocked、版本/tag 不一致、input hash 漂移、Docker/buildx/网络/基础镜像源/验证/tar/sha256 失败时 MUST 阻断，不得伪造成功 manifest。

发布确认阶段 MUST 重新校验 manifest 的版本、tag、source plan 和 input hashes。manifest 生成后 Dockerfile、构建脚本、schema、migration、Compose 或 release input 漂移时，镜像证据失效，必须重新执行 `/image-prepare` 与 `/image-build`，或记录经批准的外部构建证据。

外部构建证据只可作为受控替代证据，必须记录来源、版本、image tag、平台、镜像 digest 或 tarball sha256、校验方式、负责人确认和风险说明；不得绕过公开安全扫描、版本一致性校验或 input hash 漂移校验。

数据库影响不允许只记录 SQLite、本地测试或文档同步证据。`impact_scope.database` 非 `none` / `na` / `不涉及` 时，`database_migration` 门禁 MUST 为 `pass`，且 evidence MUST 明确包含：

- MySQL 或 `schema.mysql.sql` 目标路径证据。
- MySQL schema drift、目标 MySQL smoke、`information_schema` 校验或等价证据。
- 数据库回滚或备份证据。

发布对象和公告安全校验：

```bash
python scripts/validate-release.py --release-dir releases/vX.Y.Z --stage prepare
python scripts/validate-release.py --release-dir releases/vX.Y.Z --stage publish
```

## 5. 发布命令族

推荐命令：

| 命令 | 目标 |
|---|---|
| `/release-propose <version>` | 创建或更新产品版本发布计划 |
| `/release-prepare <version>` | 执行发布前校验，生成或更新公告源文件 |
| `/image-prepare <version>` | 生成镜像构建计划并校验 release、tag、Compose、Dockerfile、schema/migration 等输入 |
| `/image-build <version>` | 基于有效构建计划执行真实镜像构建、验证、离线包导出并生成 manifest |
| `/release-publish <version>` | 记录发布确认结果和最终公告位置 |
