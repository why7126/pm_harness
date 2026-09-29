---
purpose: 生产镜像包构建与部署手册
content: 生产镜像构建、离线交付包、云服务器部署、校验、回滚和安全边界
source: Harness docs Token 优化模板，初始化时基于部署方式和发布策略生成
update_method: 镜像构建方式、交付包结构、生产部署流程、版本策略或回滚策略变化时更新
created_at: 2026-07-14 00:00:00
updated_at: 2026-07-31 17:10:00
owner: {DOCS_OWNER}
status: draft
note: 不得记录真实生产密钥、域名、客户数据或不可公开运维信息
---

# 生产镜像包构建与部署手册

本文记录 `{PRODUCT_NAME}` 的生产镜像包构建、离线交付和云服务器部署流程。具体镜像名、版本号、架构和部署命令必须在发布前由项目团队确认。

正式发布默认通过 `/release-propose`、`/release-prepare`、`/image-prepare`、`/image-build`、`/release-publish` 串联完成。手工 Docker 命令只作为排障参考，不得替代 `image-build-plan.json` 与 `image-manifest.json` 的发布证据。

## 1. 部署目标

推荐生产拓扑：

```text
Host Nginx / Load Balancer
  -> Web Container
  -> Backend Container
  -> Production Database
  -> Object Storage / External Services
```

目标架构：

```text
{TARGET_PLATFORM}
```

版本号：

```text
{RELEASE_VERSION}
```

## 2. 交付包结构

推荐结构：

```text
../releases/{RELEASE_VERSION}/
├── images/
│   ├── {PRODUCT_CODE}-{RELEASE_VERSION}-{TARGET_PLATFORM}.tar.gz
│   └── {PRODUCT_CODE}-{RELEASE_VERSION}-{TARGET_PLATFORM}.tar.gz.sha256
├── docker-compose.yml
├── .env.example
└── README-deploy.md
```

交付包不得包含真实 `.env`、真实客户数据、运行时数据库文件、对象存储数据卷或不可公开日志。

仓库内 `releases/{RELEASE_VERSION}/` 只保存 `release.json`、`announcement.mdx`、`image-build-plan.json`、`image-manifest.json` 等可审查发布事实；大体积镜像 tar 包和 `.sha256` 默认放在仓库外 `../releases/{RELEASE_VERSION}/images/`。

## 3. 构建前置条件

构建机需要：

```text
Docker / Docker Desktop / OrbStack
docker buildx
可访问基础镜像源与依赖包源
```

检查：

```bash
docker buildx version
docker buildx ls
```

## 4. 准备镜像构建计划

```bash
python scripts/validate-release.py --release-dir releases/{RELEASE_VERSION} --stage prepare
python scripts/validate-image-build.py prepare --release {RELEASE_VERSION}
```

`/image-prepare` 会生成或更新 `releases/{RELEASE_VERSION}/image-build-plan.json`。计划文件只允许记录构建 env 安全摘要、输入 hash、required commands、auto actions、warnings 与 blockers，不得记录真实 `.env`、密钥、数据库连接串、Authorization header、Cookie、本机绝对路径或真实客户数据。

如缺少 `scripts/build-images.env`，`/image-prepare` 可从 `scripts/build-images.env.example` 创建本地配置并仅自动写入安全白名单变量 `IMAGE_BUILD_TAG={RELEASE_VERSION}`。其他变量由发布负责人确认。

## 5. 构建镜像

推荐命令：

```bash
./scripts/build-images.sh scripts/build-images.env
python scripts/validate-image-build.py build --release {RELEASE_VERSION}
```

构建成功后必须生成 `releases/{RELEASE_VERSION}/image-manifest.json`，记录 version、image tag、platform、backend/web image、tarball path、sha256、input hashes、validation 和 source plan。若 plan blocked、版本/tag 不一致、input hash 漂移、Docker/buildx/网络/基础镜像源/验证/tar/sha256 失败，必须阻断发布。

后端镜像排障示例：

```bash
docker buildx build \
  --platform {TARGET_PLATFORM} \
  -t {PRODUCT_CODE}-backend:{RELEASE_VERSION} \
  -f src/backend/Dockerfile \
  --load \
  src/backend
```

Web 镜像排障示例：

```bash
docker buildx build \
  --platform {TARGET_PLATFORM} \
  -t {PRODUCT_CODE}-web:{RELEASE_VERSION} \
  -f src/web/Dockerfile \
  --load \
  .
```

如项目不包含后端或 Web 镜像，应删除不适用步骤并补充真实构建命令，同时更新 `scripts/build-images.sh` 和 `scripts/validate-image-build.py`。

## 6. 发布确认

```bash
python scripts/validate-release.py --release-dir releases/{RELEASE_VERSION} --stage publish
```

发布确认阶段必须重新校验 manifest 的版本、tag、source plan 和 input hashes。manifest 生成后 Dockerfile、构建脚本、schema、migration、Compose 或 release input 漂移时，镜像证据失效，必须重新执行 `/image-prepare` 与 `/image-build`，或记录经批准的外部构建证据。

## 7. 服务器部署

服务器前置条件：

```text
□ Docker / Compose 可用
□ 数据库已创建并可访问
□ 对象存储 bucket / 权限已准备（如启用）
□ 端口、防火墙、域名、HTTPS 已准备
□ .env 已在服务器本地创建，且不使用示例密钥
```

部署示例：

```bash
sha256sum -c images/*.sha256
docker load < images/{PRODUCT_CODE}-{RELEASE_VERSION}-{TARGET_PLATFORM}.tar.gz
docker compose config
docker compose up -d
```

## 8. 冒烟验证

```text
□ Web 可访问
□ Backend health 可访问
□ 登录 / 鉴权可用（如启用）
□ 核心读写 API 可用
□ 文件上传和读取可用（如启用）
□ 重启后数据仍可访问
□ 日志无密钥、连接串或客户数据泄露
```

## 9. 回滚

回滚前确认：

```text
□ 是否有数据库迁移，是否可逆
□ 是否有对象存储 Key 或数据格式变化
□ 是否需要恢复旧镜像 tag
□ 是否需要恢复旧 .env 或配置
□ 是否已记录回滚原因和影响范围
```

回滚命令应在实际发布前补充。
