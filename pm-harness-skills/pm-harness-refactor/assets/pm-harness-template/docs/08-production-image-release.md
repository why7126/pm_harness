---
purpose: 生产镜像包构建与部署手册
content: 生产镜像构建、离线交付包、云服务器部署、校验、回滚和安全边界
source: Harness docs Token 优化模板，初始化时基于部署方式和发布策略生成
update_method: 镜像构建方式、交付包结构、生产部署流程、版本策略或回滚策略变化时更新
created_at: 2026-07-14 00:00:00
updated_at: 2026-07-14 00:00:00
owner: {DOCS_OWNER}
status: draft
note: 不得记录真实生产密钥、域名、客户数据或不可公开运维信息
---

# 生产镜像包构建与部署手册

本文记录 `{PRODUCT_NAME}` 的生产镜像包构建、离线交付和云服务器部署流程。具体镜像名、版本号、架构和部署命令必须在发布前由项目团队确认。

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
{PRODUCT_CODE}-release-{RELEASE_VERSION}/
├── images/
│   ├── {PRODUCT_CODE}-{RELEASE_VERSION}-{TARGET_PLATFORM}.tar.gz
│   └── {PRODUCT_CODE}-{RELEASE_VERSION}-{TARGET_PLATFORM}.tar.gz.sha256
├── docker-compose.yml
├── .env.example
└── README-deploy.md
```

交付包不得包含真实 `.env`、真实客户数据、运行时数据库文件、对象存储数据卷或不可公开日志。

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

## 4. 构建镜像

后端镜像示例：

```bash
docker buildx build \
  --platform {TARGET_PLATFORM} \
  -t {PRODUCT_CODE}-backend:{RELEASE_VERSION} \
  -f src/backend/Dockerfile \
  --load \
  src/backend
```

Web 镜像示例：

```bash
docker buildx build \
  --platform {TARGET_PLATFORM} \
  -t {PRODUCT_CODE}-web:{RELEASE_VERSION} \
  -f src/web/Dockerfile \
  --load \
  .
```

如项目不包含后端或 Web 镜像，应删除不适用步骤并补充真实构建命令。

## 5. 导出离线镜像包

```bash
mkdir -p releases/{RELEASE_VERSION}/images
docker save \
  {PRODUCT_CODE}-backend:{RELEASE_VERSION} \
  {PRODUCT_CODE}-web:{RELEASE_VERSION} \
  | gzip > releases/{RELEASE_VERSION}/images/{PRODUCT_CODE}-{RELEASE_VERSION}-{TARGET_PLATFORM}.tar.gz

shasum -a 256 \
  releases/{RELEASE_VERSION}/images/{PRODUCT_CODE}-{RELEASE_VERSION}-{TARGET_PLATFORM}.tar.gz \
  > releases/{RELEASE_VERSION}/images/{PRODUCT_CODE}-{RELEASE_VERSION}-{TARGET_PLATFORM}.tar.gz.sha256
```

## 6. 服务器部署

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

## 7. 冒烟验证

```text
□ Web 可访问
□ Backend health 可访问
□ 登录 / 鉴权可用（如启用）
□ 核心读写 API 可用
□ 文件上传和读取可用（如启用）
□ 重启后数据仍可访问
□ 日志无密钥、连接串或客户数据泄露
```

## 8. 回滚

回滚前确认：

```text
□ 是否有数据库迁移，是否可逆
□ 是否有对象存储 Key 或数据格式变化
□ 是否需要恢复旧镜像 tag
□ 是否需要恢复旧 .env 或配置
□ 是否已记录回滚原因和影响范围
```

回滚命令应在实际发布前补充。
