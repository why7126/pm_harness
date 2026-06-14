---
name: pm-harness-init
description: 初始化 AI Coding 项目的 harness 工程结构。当用户需要为新项目生成标准化的 pm-harness 工程框架时使用本技能。触发场景包括：初始化新项目工程结构、生成 AI 编码脚手架、创建 pm-harness 工程、搭建 OpenSpec + AI Agent 规范编程项目结构。用户提供产品名称（必填）及可选配置后，本技能将生成完整的、经过参数化替换的 harness 工程 zip 包供用户下载。
---

# PM Harness 工程初始化技能

## 概述

本技能基于 `pm-harness` 模板工程，结合用户输入的产品信息，生成一个适用于 AI Coding（OpenSpec + AI Agent 规范编程）项目的标准化 harness 工程结构，最终输出 zip 包。

## 资产说明

本技能打包了以下资产，执行时必须以这些文件为基础，不得凭空生成：

| 资产路径 | 用途 |
|---------|------|
| `assets/pm-harness-template.zip` | 原始 pm-harness 模板工程，所有文件生成的事实源 |
| `assets/templates/requirements-template-README.md` | 需求模板目录说明 |
| `assets/templates/requirement-template.md` | requirement.md 文件模板 |
| `assets/templates/bugs-template-README.md` | Bug 模板目录说明 |
| `assets/templates/bug-template.md` | bug.md 文件模板 |

**重要**：执行 Step 3 构建工程目录时，必须先解压 `assets/pm-harness-template.zip` 作为基础，在此基础上做参数化替换和目录调整，而不是从零创建文件。

## 用户输入参数

### 必填

| 参数 | 说明 |
|------|------|
| 产品名称 | 用于替换文档标题、容器名、项目代码等 |
| 数据库 | 默认 `SQLite`；可选其他（PostgreSQL、MySQL 等）|
| 是否包括算法 | 默认 `否`；选 `是` 则创建 `src/algorithm/` 目录并更新相关文档 |

### 选填

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 产品定位 | 空 | 填充到产品总览文档 |
| 产品形态 | 多选，至少一项 | Web、微信小程序、Android、iOS、桌面端、H5 等 |
| 后端技术栈 | Python + FastAPI + Pydantic + uv + MinIO | 影响 AGENTS.md、rules、src/backend |
| 前端技术栈 | React + TypeScript + TailWind + Shadcn/ui + Axios + Orval + pnpm | 影响 rules、src/web |
| 信创数据库 | 空 | 如达梦、人大金仓等；更新 compatibility 和 rules/database.md |
| 信创操作系统 | 空 | 如麒麟、统信等；更新 compatibility/os/ |

## 执行步骤

### Step 1：收集用户输入

如果用户消息中未包含所有必填信息，逐步引导用户提供：
1. 产品名称（必填）
2. 产品形态（至少一项）
3. 数据库选型（默认 SQLite）
4. 是否包括算法（默认否）

选填项不阻塞流程，用默认值处理。

### Step 2：派生基础变量

根据用户输入派生以下变量（在后续文件生成中使用）：

```
PRODUCT_NAME        = 用户输入的产品名称（中文）
PRODUCT_CODE        = 产品名称的英文 slug，小写 kebab-case，如 "my-platform"
PRODUCT_DESCRIPTION = 产品定位（选填，默认为空字符串）
DB_PRIMARY          = 主数据库，默认 SQLite
DB_XINCHUAN         = 信创数据库（选填）
OS_XINCHUAN         = 信创操作系统（选填）
HAS_ALGORITHM       = 是否包括算法，true/false
BACKEND_STACK       = 后端技术栈描述
FRONTEND_STACK      = 前端技术栈描述
FORMS               = 产品形态列表（数组）
HAS_WEB             = FORMS 包含 Web
HAS_MINIAPP         = FORMS 包含 微信小程序
HAS_ANDROID         = FORMS 包含 Android
HAS_IOS             = FORMS 包含 iOS
```

### Step 3：构建工程目录

1. 解压 `assets/pm-harness-template.zip` 到 `/home/claude/output/`
2. 将解压出的 `pm-harness/` 目录重命名为 `{PRODUCT_CODE}/`
3. 在此基础上执行参数化替换和目录调整（见「文件生成规则」章节）

### Step 4：生成所有文件

按照「文件生成规则」章节逐一生成文件内容。

### Step 5：打包输出

```bash
cd /home/claude/output
zip -r {PRODUCT_CODE}-harness.zip {PRODUCT_CODE}/ \
  --exclude "*/.DS_Store" \
  --exclude "*/__pycache__/*" \
  --exclude "*/.pytest_cache/*"
cp {PRODUCT_CODE}-harness.zip /mnt/user-data/outputs/
```

然后调用 `present_files` 工具向用户展示 zip 文件。

---

## 目录结构规则

```
{PRODUCT_CODE}/
├── .claude/                    # 保留原模板内容（commands + skills）
├── .codex/                     # 保留原模板内容
├── .cursor/                    # 保留原模板内容，commands 中的产品引用更新
├── .kiro/                      # 保留原模板内容
├── .opencode/                  # 保留原模板内容
├── AGENTS.md                   # 必须更新
├── README.md                   # 必须更新
├── project.yaml                # 必须更新
├── docker-compose.yml          # 必须更新
├── DOCUMENT_METADATA_INDEX.md  # 必须更新
├── .dockerignore               # 必须更新
├── .env.example                # 必须更新
├── .gitignore                  # 保留（通用内容已足够）
├── pytest.ini                  # 保留
├── compatibility/
│   ├── database/
│   │   ├── {db_primary}.md         # 以实际数据库命名
│   │   ├── migration-rules.md
│   │   └── test-matrix.md
│   ├── devices/                    # 根据产品形态创建
│   │   ├── web.md                  # HAS_WEB=true 时创建
│   │   ├── wechat-miniapp.md       # HAS_MINIAPP=true 时创建
│   │   ├── android.md              # HAS_ANDROID=true 时创建
│   │   └── ios.md                  # HAS_IOS=true 时创建
│   └── object-storage/
│       └── minio.md
├── data/                       # 置空（仅保留 .gitkeep）
├── docs/
│   ├── 00-product-overview.md
│   ├── 01-architecture.md
│   ├── 02-deployment.md
│   ├── 03-api-index.md
│   ├── 04-database-design.md
│   ├── 05-compatibility-matrix.md
│   ├── 06-video-asset-management.md  # 如有媒体需求保留，否则标注为"待定"
│   ├── 07-object-storage-strategy.md
│   ├── api-governance.md
│   ├── authentication.md
│   ├── error-codes.md
│   ├── file-upload.md
│   ├── frontend-test-standard.md
│   ├── openapi-rules.md
│   ├── test-coverage.md
│   ├── testing-governance.md
│   ├── unit-test-standard.md
│   └── knowledge-base/         # 置空目录（仅 .gitkeep）
├── issues/
│   ├── requirements/
│   │   └── template/           # 需求模板目录（详见文件规则）
│   └── bugs/
│       └── template/           # Bug模板目录（详见文件规则）
├── iterations/                 # 置空（仅 .gitkeep）
├── openspec/
│   ├── project.md
│   ├── config.yaml
│   ├── specs/                  # 置空（仅 .gitkeep）
│   ├── changes/                # 置空（仅 .gitkeep）
│   └── archive/                # 置空（仅 .gitkeep）
├── rules/
│   ├── global.md
│   ├── language.md
│   ├── coding.md
│   ├── api.md
│   ├── compatibility.md
│   ├── data-management.md
│   ├── database.md
│   ├── directory-structure.md
│   ├── document-governance.md
│   ├── environment.md
│   ├── media.md
│   ├── object-storage.md
│   ├── port-management.md
│   ├── release.md
│   ├── security.md
│   ├── testing.md
│   └── ui-design.md
├── scripts/                    # 保留原模板脚本，更新产品引用
├── src/
│   ├── backend/                # 必有
│   ├── web/                    # HAS_WEB=true 时创建
│   ├── miniapp/                # HAS_MINIAPP=true 时创建
│   ├── android/                # HAS_ANDROID=true 时创建
│   ├── ios/                    # HAS_IOS=true 时创建
│   ├── algorithm/              # HAS_ALGORITHM=true 时创建
│   ├── shared/                 # 共享代码目录
│   ├── sdk/                    # SDK目录
│   └── infrastructure/         # 基础设施目录
└── tests/
    ├── compatibility/          # 各端兼容性测试占位
    ├── e2e/
    ├── fixtures/
    ├── integration/
    └── unit/
```

---

## 文件生成规则

### AGENTS.md

完整保留原模板结构，进行以下替换：
- 产品名称全部替换（如「瓷砖信息管理平台」→ `{PRODUCT_NAME}`）
- 「系统包含」章节根据 FORMS 和 HAS_ALGORITHM 更新
- 后端强制规则中的技术栈更新为用户输入的 BACKEND_STACK
- 前端强制规则中的技术栈更新为用户输入的 FRONTEND_STACK
- 数据库规则替换为用户选择的数据库
- Docker Compose 服务地址根据实际配置更新
- 如有信创数据库，增加信创数据库兼容性章节
- Design System 章节根据实际前端框架调整（若非 React/Shadcn，简化或移除）
- 文档元数据 note 字段更新为 `{PRODUCT_NAME}项目模板`

### README.md

- 标题更新为 `{PRODUCT_NAME}`
- 产品简介更新为 `{PRODUCT_DESCRIPTION}`（若空则用默认占位文字）
- 技术栈章节根据用户输入更新
- 目录说明根据 FORMS 更新（只列出实际存在的目录）
- Docker Compose 服务地址中容器名替换为 `{PRODUCT_CODE}`

### project.yaml

```yaml
project:
  name: {PRODUCT_NAME}
  code: {PRODUCT_CODE}
  description: {PRODUCT_DESCRIPTION}

backend:
  # 根据 BACKEND_STACK 填充
  database: {DB_PRIMARY}
  object_storage: MinIO  # 如 BACKEND_STACK 不含 MinIO 则调整

frontend:
  # 根据 FRONTEND_STACK 填充

channels:
  # 根据 FORMS 动态生成，如：
  web_public: {HAS_WEB}
  wechat_miniapp: {HAS_MINIAPP}
  android: {HAS_ANDROID}
  ios: {HAS_IOS}

algorithm:
  enabled: {HAS_ALGORITHM}
```

### docker-compose.yml

- 容器名从 `tile-info-platform-*` 改为 `{PRODUCT_CODE}-*`
- 网络名从 `tile-info-platform` 改为 `{PRODUCT_CODE}`
- 数据库 volume 路径根据 DB_PRIMARY 调整（SQLite 使用 volume，PostgreSQL/MySQL 增加对应服务）
- 如 DB_PRIMARY 非 SQLite，增加对应数据库 service
- MinIO bucket 环境变量默认值改为 `{PRODUCT_CODE}`

### .env.example

- `APP_NAME` 改为 `{PRODUCT_CODE}`
- SQLite 数据库路径中的项目名替换
- MinIO bucket 默认值替换为 `{PRODUCT_CODE}`
- 如 DB_PRIMARY 非 SQLite，移除 SQLite 相关变量，增加对应数据库连接变量

### DOCUMENT_METADATA_INDEX.md

- 文档 note 字段统一改为 `{PRODUCT_NAME}项目模板`
- 版本说明更新（移除「V2～V5」历史版本描述，统一为「初始化版本」）

### rules/ 目录下所有文件

统一替换：
- 所有「瓷砖信息管理平台」→ `{PRODUCT_NAME}`
- 所有 `tile-info-platform` → `{PRODUCT_CODE}`
- `rules/database.md`：将核心表示例替换为通用占位表（`users`、`audit_logs` 等通用表保留，业务表替换为 `{PRODUCT_CODE}_items` 等占位）
- `rules/coding.md`：前端框架描述根据 FRONTEND_STACK 调整；后端描述根据 BACKEND_STACK 调整
- `rules/ui-design.md`：如前端非 React/Tailwind/shadcn，移除具体 Design System 章节，替换为通用 UI 规范占位
- `rules/directory-structure.md`：src 子目录列表根据 FORMS 和 HAS_ALGORITHM 调整

### docs/ 目录下文件

- 所有产品名、项目代码替换
- `00-product-overview.md`：核心场景、用户角色根据 FORMS 和 PRODUCT_DESCRIPTION 调整，业务特定场景改为通用占位
- `01-architecture.md`：系统架构图根据 FORMS 和技术栈更新
- `02-deployment.md`：部署服务组成根据 docker-compose 实际服务更新
- `04-database-design.md`：移除瓷砖相关业务表，保留通用表（users、audit_logs），并注明「业务表待需求明确后填充」
- `05-compatibility-matrix.md`：矩阵行根据 FORMS 调整

### openspec/project.md 和 config.yaml

- 产品名称、项目代码替换
- `config.yaml` 中 `project` 字段替换为 `{PRODUCT_CODE}`

### issues/requirements/template/

创建如下结构（帮助用户了解如何创建需求）：

```
issues/requirements/template/
├── README.md                  # 说明模板使用方式
├── requirement.md             # 需求文档模板
├── acceptance.md              # 验收标准模板
├── user-stories.md            # 用户故事模板
├── business-flow.md           # 业务流程模板
├── trace.md                   # 需求追溯模板
└── prototype/
    └── README.md              # 说明原型文件放置规范
```

每个文件包含结构占位和说明注释（中文）。

### issues/bugs/template/

创建如下结构（帮助用户了解如何记录 Bug）：

```
issues/bugs/template/
├── README.md                  # 说明模板使用方式
├── bug.md                     # Bug 描述模板
├── root-cause.md              # 根因分析模板
├── workaround.md              # 临时解决方案模板
├── acceptance.md              # 修复验收标准模板
├── trace.md                   # Bug 追溯模板
├── logs/                      # 日志目录占位（.gitkeep）
└── screenshots/               # 截图目录占位（.gitkeep）
```

### src/ 目录

**src/backend/**（必有）

```
src/backend/
├── .env.example            # 后端专用环境变量模板
├── .env.docker             # Docker 环境变量模板
├── Dockerfile              # 后端镜像，根据 BACKEND_STACK 调整
└── app/
    ├── main.py             # FastAPI 入口（或对应框架入口）
    ├── api/                # 路由层占位
    ├── core/               # 核心配置占位
    ├── db/                 # 数据库层占位
    ├── models/             # 模型层占位
    ├── repositories/       # 数据访问层占位
    ├── schemas/            # 数据 Schema 占位
    └── services/           # 服务层占位
```

各文件包含基础骨架代码和注释，不包含任何业务逻辑。

**src/web/**（HAS_WEB=true 时创建）

```
src/web/
├── .dockerignore
├── Dockerfile
├── nginx.conf
├── package.json            # 基础依赖，根据 FRONTEND_STACK 调整
└── src/
    ├── app/
    ├── components/
    ├── features/
    ├── pages/
    ├── services/
    └── styles/
```

**src/miniapp/**（HAS_MINIAPP=true 时创建）

```
src/miniapp/
├── pages/
├── components/
├── services/
└── utils/
```

**src/android/**（HAS_ANDROID=true 时创建）

```
src/android/
└── README.md    # 说明 Android 项目结构规范
```

**src/ios/**（HAS_IOS=true 时创建）

```
src/ios/
└── README.md    # 说明 iOS 项目结构规范
```

**src/algorithm/**（HAS_ALGORITHM=true 时创建）

```
src/algorithm/
├── README.md        # 说明算法模块职责与开发规范
├── models/          # 模型文件存放
├── inference/       # 推理服务
├── training/        # 训练脚本（可选）
└── requirements.txt # 算法依赖
```

### .cursor/ 目录

保留原模板所有内容（commands 和 skills），并对 commands 中的产品引用（瓷砖相关）进行通用化替换。

---

## 信创适配规则

### 信创数据库

如用户指定信创数据库（如达梦 DM、人大金仓 KingbaseES 等）：

1. 在 `compatibility/database/` 下新增 `{xinchuan_db}.md`
2. 在 `rules/database.md` 末尾增加「信创数据库适配」章节，说明差异和注意事项
3. 在 `docs/05-compatibility-matrix.md` 中增加信创数据库兼容性矩阵行
4. 在 `AGENTS.md` 约束中注明信创数据库要求

### 信创操作系统

如用户指定信创操作系统（如麒麟、统信 UOS 等）：

1. 在 `compatibility/` 下新增 `os/` 目录，创建 `{xinchuan_os}.md`
2. 在 `docs/05-compatibility-matrix.md` 增加操作系统兼容行
3. 在 `rules/environment.md` 增加信创 OS 适配注意事项

---

## 算法模块规则

HAS_ALGORITHM=true 时，额外执行：

1. 创建 `src/algorithm/` 目录结构（见上）
2. 在 `AGENTS.md` 「系统包含」增加「算法服务」
3. 在 `rules/directory-structure.md` 增加 `src/algorithm/` 说明
4. 在 `docs/01-architecture.md` 架构图中增加 Algorithm 模块
5. 在 `docker-compose.yml` 中增加 algorithm 服务占位（注释掉，待需求明确）
6. 在 `project.yaml` 中 `algorithm.enabled: true`

---

## 文档元数据模板

所有 Markdown 文件头部必须包含：

```yaml
---
purpose: {文档用途}
content: {文档内容简述}
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于{PRODUCT_NAME}项目模板
---
```

---

## 置空目录规则

以下目录需保留目录结构但内容为空（只放 `.gitkeep`）：

- `data/`（所有子目录）
- `docs/knowledge-base/`
- `openspec/specs/`
- `openspec/changes/`
- `openspec/archive/`
- `iterations/`

---

## 质量要求

1. **无业务硬编码**：生成的工程不得包含任何「瓷砖」「tile」相关业务词汇（产品名替换除外）
2. **中文优先**：所有文档使用中文，代码标识符使用英文
3. **结构完整性**：每个 src 子目录必须有 `README.md` 说明目录职责
4. **规则一致性**：AGENTS.md、rules/、project.yaml 中的技术栈描述必须一致
5. **模板可用性**：issues/template 中的模板文件必须包含真实可用的结构示例

---

## 常见产品形态与目录对照

| 产品形态 | src 子目录 | compatibility/devices/ |
|---------|-----------|----------------------|
| Web | `src/web/` | `web.md` |
| 微信小程序 | `src/miniapp/` | `wechat-miniapp.md` |
| Android | `src/android/` | `android.md` |
| iOS | `src/ios/` | `ios.md` |
| 桌面端 | `src/desktop/` | `desktop.md` |
| H5 | `src/h5/` | `h5.md` |

---

## 输出检查清单

生成完成后，在向用户展示前，确认以下项目：

```
□ 所有文件中「瓷砖信息管理平台」已替换为 {PRODUCT_NAME}
□ 所有文件中「tile-info-platform」已替换为 {PRODUCT_CODE}
□ src/ 目录根据 FORMS 正确创建/省略
□ src/algorithm/ 根据 HAS_ALGORITHM 正确处理
□ docker-compose.yml 服务与实际选型一致
□ .env.example 变量与 docker-compose.yml 一致
□ issues/requirements/template/ 包含完整模板结构
□ issues/bugs/template/ 包含完整模板结构
□ openspec/specs、changes、archive 已置空
□ iterations/ 已置空
□ data/ 已置空
□ docs/knowledge-base/ 已置空
□ .cursor/ 目录完整保留
□ 信创数据库（如有）相关文件已创建
□ 信创操作系统（如有）相关文件已创建
□ 所有 Markdown 文件包含正确元数据头部
```
