---
purpose: 环境变量与运行环境规范
content: 规范 .env.example、服务环境变量、运行时配置、密钥边界、Docker Compose 与部署环境同步规则
source: Harness environment.md 抽象模板，基于多项目环境治理规则沉淀
update_method: 项目初始化时按用户输入生成；新增服务、端口、密钥、数据库、对象存储、第三方服务、部署方式或运行参数时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
note: 适用于 {PRODUCT_NAME} 项目；.env.example 可提交，真实 .env 和生产密钥禁止提交
template_scope: 可作为工程初始化的 environment.md 模块
---

# 环境变量与运行环境规范

## 0. 规则定位 [通用]

本文档用于约束 `{PRODUCT_NAME}` 项目的环境变量、运行时配置、密钥、端口、部署环境和配置同步规则，确保：

- 所有环境相关配置都有统一来源和说明。
- `.env.example` 与代码、Docker Compose、部署文档保持一致。
- 真实密钥、生产配置、客户私有化配置不会进入 Git。
- 前端构建时变量、运行时配置、后端服务配置边界清晰。
- AI 新增配置时知道必须同步哪些文件。

### 0.1 初始化占位符 [通用]

| 占位符 | 含义 | 生成要求 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品中文名 | 来自用户输入 |
| `{PRODUCT_CODE}` | 项目代码名 | kebab-case |
| `{PRODUCT_FORMS}` | 产品形态 | Web、微信小程序、移动端、桌面端、H5 等 |
| `{BACKEND_STACK}` | 后端技术栈 | 决定配置加载方式 |
| `{FRONTEND_STACK}` | 前端技术栈 | 决定前端环境变量前缀与构建方式 |
| `{DATABASE_STACK}` | 数据库选型 | 决定 DB_* 或连接串变量 |
| `{OBJECT_STORAGE_STACK}` | 对象存储 | MinIO、S3、OSS、COS、无 |
| `{DEPLOYMENT_STACK}` | 部署方式 | Docker Compose、Kubernetes、私有化、SaaS |
| `{CONFIG_LOADER}` | 配置加载库 | pydantic-settings、Spring Config、dotenv 等 |
| `{ENVIRONMENTS}` | 环境列表 | development、test、staging、production、private 等 |
| `{PUBLIC_ENV_PREFIX}` | 前端可公开变量前缀 | 如 `VITE_`、`NEXT_PUBLIC_` |

生成初始化工程时，必须替换全部占位符；无法确认的信息写 `待确认`，不得保留样例项目的业务变量名。

## 1. 文档模块分类 [通用]

本文档中的章节按以下标签标识：

- `[通用]`：所有 Harness 工程都应保留。
- `[个性化]`：必须根据用户输入、技术栈、部署模式生成。
- `[条件启用]`：仅在对应能力启用时保留，例如前端、对象存储、Redis、异步任务、算法服务、信创环境。

初始化生成时，不得把未启用的服务变量写成强制必填。

## 2. 基本原则 [通用]

- 根目录必须提供 `.env.example`，或在项目初始化时明确说明根环境文件不启用并列出替代位置。
- 真实 `.env`、`.env.local`、`.env.production`、客户私有配置、密钥文件禁止提交 Git。
- 新增任何环境变量时，必须同步更新对应 `.env.example`、部署文档、Docker Compose/Kubernetes 配置和配置加载代码。
- Docker Compose、启动脚本、CI/CD、部署脚本使用的变量必须在示例文件或部署文档中有说明。
- 不允许在代码、测试、文档示例、截图、日志中写入真实密钥。
- 敏感变量不得设置生产可用的非空默认值。
- 不确定的变量默认值必须写 `待确认` 或使用明显不可用于生产的示例值。

## 3. 环境文件归属 [通用 + 个性化]

| 文件 | 职责 | 是否可提交 | 生成策略 |
|---|---|---:|---|
| `.env.example` | 根环境变量示例与统一索引 | 是 | 必须保留或说明替代方案 |
| `.env` | 本地真实环境变量 | 否 | 禁止提交 |
| `.env.local` | 本地覆盖配置 | 否 | 按需启用 |
| `.env.test` | 测试环境变量示例或真实测试配置 | 视内容而定 | 示例可提交，真实凭据禁止 |
| `.env.production` | 生产环境配置 | 否 | 不提交，仅文档说明 |
| `src/backend/.env.example` | 后端服务变量示例 | 是 | 有后端时保留 |
| `src/backend/.env.docker` | Docker 本地后端变量 | 是，仅示例值 | 启用 Docker Compose 时保留 |
| `src/web/.env.example` | Web 前端构建变量示例 | 是 | 有 Web 时保留 |
| `src/web/public/config/runtime-env.json` | Web 运行时配置 | 视内容而定 | 私有化或运行时注入时启用 |
| `deploy/*/*.env.example` | 部署场景变量示例 | 是 | 按部署方式生成 |
| `secrets/*` | 密钥文件或证书 | 否 | 默认不进入 Git |

`.gitignore` 必须覆盖真实环境文件、密钥、证书、客户配置和部署私有配置。

## 4. 命名规范 [通用 + 个性化]

### 4.1 通用命名 [通用]

环境变量使用大写蛇形命名：

```text
DOMAIN_COMPONENT_SETTING
```

示例：

```text
APP_ENV
LOG_LEVEL
BACKEND_PORT
DATABASE_URL
MINIO_BUCKET
MAX_UPLOAD_SIZE_MB
```

要求：

- 变量名必须表达所属域和用途。
- 布尔值使用 `true/false` 或项目统一格式。
- 时长变量必须带单位，例如 `_SECONDS`、`_MINUTES`、`_DAYS`。
- 大小变量必须带单位，例如 `_BYTES`、`_MB`、`_GB`。
- URL 使用 `_URL`，Host/Port 拆分时使用 `_HOST`、`_PORT`。
- 不得使用含糊变量名，例如 `KEY`、`TOKEN`、`URL1`、`TEMP`。

### 4.2 前端公开变量前缀 [条件启用]

前端构建时公开变量必须使用框架规定前缀：

| 前端技术栈 | 公开变量前缀 |
|---|---|
| Vite | `VITE_` |
| Next.js | `NEXT_PUBLIC_` |
| Nuxt | `NUXT_PUBLIC_` |
| Vue CLI | `VUE_APP_` |
| 未确认 | `{PUBLIC_ENV_PREFIX}` |

任何使用公开前缀的变量都视为可被浏览器看到，禁止放置密钥、Token、数据库地址或内部凭据。

## 5. 环境分类 [通用 + 个性化]

默认环境：

| 环境 | 标识 | 用途 | 配置来源 |
|---|---|---|---|
| 本地开发 | `development` | 开发调试 | `.env`、`.env.local` |
| 自动化测试 | `test` | 单元/集成/e2e | 测试专用 env 或 CI 注入 |
| 预发/验收 | `staging` | 上线前验证 | 部署平台或安全配置中心 |
| 生产 | `production` | 线上运行 | 密钥管理系统或部署平台 |
| 私有化 | `private` | 客户环境 | 客户侧配置，不提交 |

初始化时根据 `{ENVIRONMENTS}` 生成实际环境列表。无预发或私有化时，不得保留强制部署规则。

## 6. 配置加载方式 [个性化]

根据 `{BACKEND_STACK}` 生成配置加载规范：

| 技术栈 | 推荐方式 | 说明 |
|---|---|---|
| Python / FastAPI | `pydantic-settings` | 统一 Settings 类，支持 `.env` |
| Python / Django | Django settings + env | 不同环境拆分 settings |
| Java / Spring Boot | `application.yml` + env override | 密钥通过环境变量注入 |
| Node.js / NestJS | `@nestjs/config` + dotenv | 使用 ConfigModule |
| Node.js / Express | dotenv + schema validation | 必须做变量校验 |
| Go | envconfig/viper | 启动时校验必填变量 |
| 未确认 | `{CONFIG_LOADER}` | 初始化时标记待确认 |

要求：

- 配置读取必须集中在 `core/config`、`settings`、`config` 等约定模块。
- 应在启动时校验必填变量，不得等到运行中才失败。
- 敏感变量不得打印到日志。
- 配置默认值只能用于本地开发，生产相关变量必须显式注入。

## 7. 后端环境变量 [通用 + 个性化]

有后端服务时，至少按以下分类生成：

| 类别 | 示例变量 | 说明 |
|---|---|---|
| 应用 | `APP_ENV`, `APP_NAME`, `LOG_LEVEL`, `APP_SECRET_KEY` | 环境、日志、应用密钥 |
| 服务绑定 | `BACKEND_HOST`, `BACKEND_PORT`, `API_PREFIX` | 监听地址与 API 前缀 |
| CORS | `BACKEND_CORS_ORIGINS` | 允许前端来源 |
| 数据库 | `DATABASE_URL` 或 `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | 按 `{DATABASE_STACK}` 生成 |
| 认证 | `JWT_SECRET_KEY`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | 有登录/权限时启用 |
| Redis/缓存 | `REDIS_URL`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` | 有缓存/队列时启用 |
| 异步任务 | `CELERY_BROKER_URL`, `TASK_QUEUE_URL`, `ENABLE_WORKER` | 有任务队列时启用 |
| 对象存储 | `STORAGE_TYPE`, `MINIO_ENDPOINT`, `S3_BUCKET` 等 | 按 `{OBJECT_STORAGE_STACK}` 生成 |
| 文件限制 | `MAX_UPLOAD_SIZE_MB`, `ALLOWED_FILE_TYPES` | 有上传/导入时启用 |
| 外部服务 | `{SERVICE_NAME}_URL`, `{SERVICE_NAME}_TIMEOUT_SECONDS` | 第三方或内部服务 |
| License | `LICENSE_PUBLIC_KEY_PATH`, `LICENSE_SERVER_URL` | 私有化/授权时启用 |

### 7.1 数据库变量 [条件启用]

单数据库项目优先使用统一连接串：

```ini
DATABASE_URL=postgresql://example_user:example_password@localhost:5432/example_db
```

多数据库或信创适配项目可使用拆分变量：

```ini
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=example_user
DB_PASSWORD=example_password
DB_NAME=example_db
```

SQLite 项目可使用：

```ini
SQLITE_DATABASE_URL=sqlite:///./data/sqlite/{PRODUCT_CODE}.db
```

不得在示例中写入生产地址、生产账号或真实密码。

### 7.2 外部服务超时 [条件启用]

所有外部服务必须配置超时：

```ini
{SERVICE_NAME}_URL=http://localhost:9000
{SERVICE_NAME}_TIMEOUT_SECONDS=60
{SERVICE_NAME}_RETRY_COUNT=3
```

超时、重试、熔断默认值必须与 `rules/compatibility.md`、`rules/api.md` 保持一致。

## 8. 前端环境变量 [条件启用]

启用 Web/H5/移动端前端时，必须区分构建时变量与运行时配置。

### 8.1 构建时变量 [条件启用]

示例：

```ini
{PUBLIC_ENV_PREFIX}APP_ENV=development
{PUBLIC_ENV_PREFIX}API_BASE_URL=http://localhost:8000
{PUBLIC_ENV_PREFIX}APP_NAME={PRODUCT_NAME}
```

要求：

- 公开前缀变量会进入浏览器包，禁止存放密钥。
- API Base URL、版本号、环境标识可公开。
- 客户私有化地址如需运行时替换，不应固化在构建产物中。

### 8.2 运行时配置 [条件启用]

私有化部署、同一镜像多环境部署或客户侧部署可启用运行时配置：

```text
src/web/public/config/runtime-env.json
```

要求：

- 运行时配置只能包含可公开信息。
- 不得包含服务端密钥、数据库连接串、对象存储 Secret。
- 修改运行时配置不应要求重新构建前端镜像。

## 9. 对象存储与文件配置 [条件启用]

启用对象存储、文件上传、媒体处理、模型文件时，必须生成对应变量：

```ini
STORAGE_TYPE=minio
MINIO_ENDPOINT=localhost:9000
MINIO_PUBLIC_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=example_access_key
MINIO_SECRET_KEY=example_secret_key
MINIO_BUCKET={PRODUCT_CODE}
MINIO_SECURE=false
MAX_UPLOAD_SIZE_MB=100
ALLOWED_FILE_TYPES=image/jpeg,image/png,application/pdf
```

规则：

- Access Key / Secret Key 示例值必须明显不可用于生产。
- Bucket 命名必须与 `{PRODUCT_CODE}` 或业务域一致。
- 文件大小限制、类型白名单必须同步 `rules/data-management.md`、`rules/media.md`、`docs/standards/file_upload.md`。
- 模型文件下载地址、校验值、存储位置不得写入真实私有凭据。

## 10. Docker Compose 环境 [条件启用]

启用 Docker Compose 时：

- `docker-compose.yml` 使用的变量必须在 `.env.example` 或部署 env 示例中说明。
- `env_file` 不得指向不存在的文件。
- 本地开发可以使用示例值，生产部署不得复用开发默认密码。
- 容器内地址与宿主机地址必须区分，例如 `minio:9000` 与 `localhost:9000`。
- 暴露端口必须与 `rules/port-management.md` 一致。

示例：

```yaml
services:
  backend:
    env_file:
      - .env
    ports:
      - "${HOST_PORT_BACKEND:-8000}:8000"
```

新增 Compose 变量时，必须同步：

- `.env.example`
- `src/backend/.env.example` 或对应服务 env 示例
- `docs/02-deployment.md`
- `rules/port-management.md`
- `README.md`

## 11. Kubernetes / 云部署 / 私有化 [条件启用]

按 `{DEPLOYMENT_STACK}` 保留对应规则。

### 11.1 Kubernetes [条件启用]

- ConfigMap 只放非敏感配置。
- Secret 存放敏感配置，禁止把 Secret 明文提交 Git。
- Helm values 示例只能使用占位值。
- 生产密钥必须由密钥管理系统或部署平台注入。

### 11.2 SaaS / 云部署 [条件启用]

- 生产配置由云平台、CI/CD 或密钥管理系统注入。
- 不得在仓库中保存生产 `.env`。
- 环境差异必须写入 `docs/02-deployment.md`。

### 11.3 私有化部署 [条件启用]

- 客户侧配置必须单独保存，不提交仓库。
- 可提供 `deploy/private/*.env.example` 作为模板。
- License、证书、公钥路径等必须使用环境变量或挂载文件。
- 客户标识、部署模式、运行时配置必须与兼容性文档一致。

## 12. 信创与多平台环境 [条件启用]

如项目要求适配信创数据库、信创 OS、ARM64、国产中间件，应生成：

| 类型 | 配置要求 |
|---|---|
| 信创数据库 | `DB_TYPE`、驱动、端口、连接参数、兼容模式 |
| 信创 OS | 文件路径、编码、权限、系统依赖 |
| ARM64 | 镜像架构、依赖包、二进制路径 |
| 国产中间件 | 服务地址、认证方式、超时 |

相关变量必须同步 `rules/compatibility.md`、`compatibility/database/*`、`docs/05-compatibility-matrix.md`。

## 13. 安全要求 [通用]

- `.env.example` 只能包含示例值。
- 密码、Token、Secret 必须使用明显示例值，例如 `example_secret_change_me`。
- 不得使用看似真实的长 Token、真实 IP、真实域名、客户名、生产账号。
- 生产密钥应通过部署平台、Secret Manager、KMS、Kubernetes Secret 或客户侧配置注入。
- 日志中不得打印敏感环境变量。
- 错误提示不得回显完整连接串或密钥。
- 文档示例不得包含真实 `.env` 内容。

## 14. AI 更新规则 [通用]

AI 修改以下内容时，必须检查环境变量同步：

| 修改内容 | 必须检查 |
|---|---|
| `docker-compose.yml` | `.env.example`、部署文档、端口规则 |
| 后端配置加载代码 | 后端 `.env.example`、测试、README |
| 前端 API 地址或构建配置 | 前端 env 示例、运行时配置、部署文档 |
| 数据库连接方式 | `.env.example`、`rules/database.md`、迁移说明 |
| 对象存储配置 | `.env.example`、`rules/object-storage.md`、部署文档 |
| 上传/媒体/模型参数 | `.env.example`、`rules/media.md`、`rules/data-management.md` |
| 第三方服务客户端 | 服务 URL、超时、重试、密钥说明 |
| 端口 | `.env.example`、`rules/port-management.md`、README |
| CI/CD 或部署脚本 | 部署 env 示例、密钥注入说明 |

AI 不得在回复中打印真实 `.env` 内容；如需要说明变量，只列变量名、用途和示例格式。

## 15. 校验与启动前检查 [通用]

项目应提供环境校验方式，例如：

```bash
python scripts/check-env.py
```

或对应技术栈命令。校验应覆盖：

- 必填变量是否存在。
- 端口是否为合法数字。
- URL 是否格式正确。
- 布尔值、数字、时长、大小单位是否合法。
- 敏感变量是否仍使用默认示例值。
- Docker Compose 引用的变量是否有示例说明。

未知校验命令时，初始化文档写 `待确认`，不得编造。

## 16. 禁止事项 [通用]

- 禁止提交真实 `.env`、生产配置、客户配置、证书、私钥。
- 禁止在代码中硬编码默认密码、Token、Secret、生产地址。
- 禁止在 `.env.example` 中使用真实密钥或可登录账号。
- 禁止前端公开变量包含后端密钥、数据库地址、对象存储 Secret。
- 禁止 Docker Compose、脚本、测试引用未说明的环境变量。
- 禁止新增变量只改代码不改文档和示例。
- 禁止把环境变量散落在多个文档中且无索引说明。

## 17. 初始化生成建议 [通用]

将本文档作为工程初始化模块时，生成器应按以下步骤处理：

1. 根据 `{PRODUCT_NAME}`、`{PRODUCT_CODE}` 替换文档元数据与示例变量。
2. 根据 `{BACKEND_STACK}` 生成配置加载方式和后端变量分类。
3. 根据 `{FRONTEND_STACK}` 生成前端公开变量前缀和构建/运行时配置规则。
4. 根据 `{DATABASE_STACK}` 生成数据库变量，单数据库优先 `DATABASE_URL`，需要兼容时生成拆分变量。
5. 根据 `{OBJECT_STORAGE_STACK}` 决定是否保留对象存储变量。
6. 根据 `{DEPLOYMENT_STACK}` 决定 Docker Compose、Kubernetes、SaaS、私有化章节。
7. 根据 `{PRODUCT_FORMS}` 删除不适用的前端、微信小程序、移动端配置要求。
8. 根据是否启用 Redis、异步任务、算法、License、第三方服务保留对应 `[条件启用]` 模块。
9. 检查本文档与 `.env.example`、`docker-compose.yml`、`README.md`、`docs/02-deployment.md`、`rules/port-management.md`、`rules/security.md` 一致。

## 18. 完成任务后检查清单 [通用]

```text
□ 环境文件归属清晰，真实 .env 禁止提交
□ [通用]、[个性化]、[条件启用] 模块标识完整
□ 环境变量命名、单位、公开前缀规则明确
□ 后端、前端、数据库、对象存储、部署变量按能力生成
□ Docker Compose / Kubernetes / 私有化规则与实际部署方式一致
□ 安全要求覆盖密钥、Token、生产地址、日志回显
□ AI 更新规则覆盖代码、部署、端口、数据库、对象存储、第三方服务
□ 初始化生成建议可被工程生成器直接使用
□ 未保留样例项目业务变量名或不适用技术栈硬性要求
```
