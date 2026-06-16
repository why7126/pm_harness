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
│   ├── bug-management.md
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
│   ├── requirement-management.md
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

基于 `assets/pm-harness/AGENTS.md` 的模块化框架生成，不做简单全文替换后直接交付。

生成要求：
- 保留所有 `[通用]` 模块。
- 用用户输入替换所有 `[个性化]` 占位符；缺失信息标记为 `待确认`。
- 用用户输入替换 AGENTS.md 核心占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_DESCRIPTION}`、`{BUSINESS_DOMAIN}`、`{TARGET_USERS}`、`{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{ASYNC_TASK_STACK}`、`{ALGORITHM_STACK}`、`{DEPLOYMENT_STACK}`、`{ENABLED_AGENT_TOOLS}`、`{PRIMARY_VERIFY_COMMAND}`。
- AGENTS.md 中所有命令占位符必须按实际脚本或 slash command 替换，例如 `{REQ_CAPTURE_COMMAND}`、`{REQ_COMPLETE_COMMAND}`、`{REQ_TO_CHANGE_COMMAND}`、`{BUG_CAPTURE_COMMAND}`、`{BUG_COMPLETE_COMMAND}`、`{BUG_TO_CHANGE_COMMAND}`、`{OPSX_APPLY_COMMAND}`、`{OPSX_ARCHIVE_COMMAND}`、`{SPRINT_PROPOSE_COMMAND}`、`{SPRINT_APPLY_COMMAND}`、`{DIRECTORY_VALIDATE_COMMAND}`、`{OPENSPEC_VALIDATE_COMMAND}`、`{TEST_COMMAND}`、`{BUILD_COMMAND}`、`{DEV_COMMAND}`、`{DOCKER_UP_COMMAND}`、`{DOCKER_DOWN_COMMAND}`。
- AGENTS.md 中所有路径、URL 与策略占位符必须按实际工程替换或删除对应模块，例如 `{DESIGN_TOKEN_PATH}`、`{BASE_COMPONENT_PATH}`、`{COMPOSITE_COMPONENT_PATH}`、`{BUSINESS_COMPONENT_PATH}`、`{PAGE_TEMPLATE_PATH}`、`{DESIGN_SYSTEM_PREVIEW_URL}`、`{SERVICE_URLS}`、`{FORBIDDEN_DIRECTORIES}`、`{UI_TOKEN_POLICY}`、`{UI_COMPONENT_POLICY}`、`{UI_VISUAL_ACCEPTANCE_POLICY}`。
- 根据项目能力保留、删除或简化 `[条件启用]` 模块，例如 monorepo、前端 UI、算法、对象存储、部署、移动端、桌面端、多 Agent 工具、Sprint 治理、原型验收。
- 「项目定位」「系统包含」「必读文档」「rules 使用规则」「强制规则」「常用命令」「完成任务后检查清单」必须根据 FORMS、HAS_ALGORITHM、BACKEND_STACK、FRONTEND_STACK、DB_PRIMARY、OBJECT_STORAGE_ENABLED、MEDIA_ENABLED 和 DEPLOYMENT_STACK 生成。
- 如果启用需求、缺陷、Sprint 命令，必须生成 `req-*`、`bug-*`、`sprint-*`、`opsx-*` 的命令表；如果项目命令名不同，必须整体替换为项目命令，不得保留旧命令。
- 如果启用多个 Agent 工具，必须生成命令事实源、同步目标和同步命令；未启用时删除该条件模块。
- 如果存在 UI prototype、截图或设计稿，必须保留「原型与视觉验收优先级」模块；无 UI 时删除 UI 与 Design System 相关模块。
- 如果启用数据、媒体、对象存储或模型能力，必须保留对应文件边界和检查项，并与 `rules/data-management.md`、`rules/media.md`、`rules/object-storage.md`、`rules/directory-structure.md` 保持一致。
- 不得保留指向不存在目录、命令、服务地址、子项目规则入口、Design System 预览页或客户端生成脚本的内容。
- 文档元数据 note 字段更新为 `适用于 {PRODUCT_NAME} 项目；AI 执行任何任务前必须优先阅读本文档`。
- 保持 AGENTS.md 与 README.md、project.yaml、rules/global.md、rules/directory-structure.md、rules/document-governance.md、rules/requirement-management.md、rules/bug-management.md、rules/testing.md、rules/release.md 的流程、目录和命令命名一致。
- 生成后必须检查 AGENTS.md 是否能回答：
  - AI 任务开始前应该先读什么？
  - 这个项目的目录、模块和命令边界是什么？
  - 改完以后如何验证和汇报？

### rules/global.md

基于 `assets/pm-harness/rules/global.md` 的模块化框架生成，作为 AGENTS.md 之后的全局 guard 规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、执行前提、任务分级、禁止行为、OpenSpec 准入、状态源、验证准出、输出要求和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{MODULES}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{DEPLOYMENT_STACK}`、`{PRIMARY_VERIFY_COMMAND}`、`{TASK_TRACKING_SYSTEM}`。
- 根据实际目录和能力生成「模块归属与上下文路由」，不要保留不存在的模块入口。
- 如项目没有前端、算法、对象存储、模型文件、私有化部署等能力，应删除或简化对应 `[条件启用]` 路由与验证项。
- 从实际脚本生成统一验证命令；命令未知时写 `待确认`，不得编造。
- 保持 global.md 与 AGENTS.md、rules/directory-structure.md、project.yaml 的模块和技术栈描述一致。

### rules/api.md

基于 `assets/pm-harness/rules/api.md` 的模块化框架生成，作为接口设计、接口调用和接口变更的强制规则。

生成要求：
- 保留所有 `[通用]` 模块，包括 API 设计原则、路径规范、请求规范、响应结构、错误码、兼容性、变更流程、测试要求和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{API_PREFIX}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{API_DOC_PATH}`、`{OPENAPI_SOURCE}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如鉴权、OpenAPI 客户端生成、前端 API 调用、文件上传、异步任务、Webhook、外部服务、SDK。
- 如前端技术栈支持 OpenAPI 客户端生成，生成 `{API_CLIENT_GENERATOR}`、`{API_CLIENT_GENERATE_COMMAND}`、`{API_GENERATED_DIR}`；否则删除客户端生成的硬性命令，保留契约同步要求。
- 根据业务领域生成 `{API_RESOURCE_EXAMPLES}`，不得保留模板中的具体业务资源。
- API 前缀未知时默认 `/api/v1`，但需在项目初始化输出中提示可确认。
- 保持 api.md 与 `docs/03-api-index.md`、`docs/openapi-rules.md`、`docs/api-governance.md`、前端生成配置和后端框架描述一致。

### rules/language.md

基于 `assets/pm-harness/rules/language.md` 的模块化框架生成，作为语言、命名和术语治理规则。

生成要求：
- 保留所有 `[通用]` 模块，包括总体语言策略、AI 输出语言、文档语言、代码标识符、测试命名、Git 命名、OpenSpec 命名、禁止事项和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRIMARY_LANGUAGE}`、`{CODE_IDENTIFIER_LANGUAGE}`、`{API_FIELD_CASE}`、`{DATABASE_FIELD_CASE}`、`{BACKEND_LANGUAGE}`、`{DOMAIN_TERMS}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如前端命名、移动端命名、国际化、多语言文档。
- 根据 BACKEND_STACK 和 FRONTEND_STACK 生成对应生态的命名规范，不得只保留 Python/React 示例。
- 根据 DB_PRIMARY 和 API 约定生成数据库字段、API 字段命名风格；未知时默认数据库 `snake_case`，API 字段标记 `待确认`。
- 根据产品名称、产品定位、业务领域生成初始术语表；不确定的术语必须标记 `待确认`。
- 保持 language.md 与 api.md、database.md、coding.md、directory-structure.md 中的命名约定一致。

### rules/coding.md

基于 `assets/pm-harness/rules/coding.md` 的模块化框架生成，作为架构分层、模块边界和代码质量规则。

生成要求：
- 保留所有 `[通用]` 模块，包括总体编码原则、架构分层、模块边界、代码风格、错误处理、依赖管理、AI 修改代码规则和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{BACKEND_STACK}`、`{BACKEND_MODULE_STRUCTURE}`、`{FORMAT_COMMAND}`、`{LINT_COMMAND}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如后端、前端、移动端/小程序、数据库、对象存储、算法/模型、异步任务、共享类型与代码生成。
- 根据 BACKEND_STACK 生成后端分层和模块结构；非 Python/FastAPI 项目不得保留 Python 专属硬性要求。
- 根据 FRONTEND_STACK 生成前端组件、状态、服务和生成客户端规则；无前端时删除前端章节。
- 根据 FORMS 生成移动端、小程序或桌面端规则；未启用的端不得保留强制规则。
- 根据 DB_PRIMARY、对象存储、算法和异步任务配置，生成对应代码边界和 adapter/client/service 规则。
- 从实际脚本生成 `{FORMAT_COMMAND}`、`{LINT_COMMAND}`、`{TYPECHECK_COMMAND}`；未知时写 `待确认`，不得编造。
- 保持 coding.md 与 language.md、api.md、database.md、testing.md、directory-structure.md 的命名、目录和质量门禁一致。

### rules/compatibility.md

基于 `assets/pm-harness/rules/compatibility.md` 的模块化框架生成，作为端、平台、数据库、部署和第三方服务兼容性规则。

生成要求：
- 保留所有 `[通用]` 模块，包括总体兼容原则、API 与协议兼容、兼容性测试要求、AI 修改规则和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_FORMS}`、`{RUNTIME_VERSION_MATRIX}`、`{OS_SUPPORT_MATRIX}`、`{DEPLOYMENT_MODES}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如 Web 浏览器、移动端/小程序、数据库、对象存储、CPU 架构、信创、第三方服务、算法服务、Webhook。
- 根据 FORMS 生成产品形态兼容范围；未启用的端不得保留强制兼容要求。
- 根据 FRONTEND_STACK 生成 `{BROWSER_SUPPORT_MATRIX}`；无 Web 前端时删除 Web 浏览器兼容章节。
- 根据 DB_PRIMARY 和信创数据库生成 `{DATABASE_SUPPORT_MATRIX}`；单数据库项目应明确只支持该数据库。
- 根据对象存储配置生成 `{OBJECT_STORAGE_SUPPORT_MATRIX}`；没有文件/媒体/模型需求时可简化对象存储章节。
- 根据 DEPLOYMENT_STACK、信创 OS、CPU 架构要求生成部署、OS、CPU 和信创兼容规则。
- 未知版本、平台或厂商支持范围标记为 `待确认`，不得编造。
- 保持 compatibility.md 与 api.md、database.md、environment.md、object-storage.md、port-management.md、directory-structure.md 一致。

### rules/data-management.md

基于 `assets/pm-harness/rules/data-management.md` 的模块化框架生成，作为数据目录、数据资产、提交边界和脱敏规则。

生成要求：
- 保留所有 `[通用]` 模块，包括数据资产目录矩阵、可提交内容、禁止提交内容、data 目录规则、样例数据、测试 fixtures、日志缓存、脱敏规则、.gitignore 边界、AI 更新规则和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{DATA_ASSET_MATRIX}`、`{SENSITIVE_DATA_TYPES}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如数据库 schema/seed、对象存储、文件上传、媒体处理、导入导出、备份恢复、模型文件、训练数据。
- 根据 DB_PRIMARY、HAS_ALGORITHM、对象存储、产品形态和导入导出需求生成 `{DATA_ASSET_MATRIX}`。
- 根据业务领域生成 `{SENSITIVE_DATA_TYPES}`，例如用户身份、联系方式、交易数据、媒体数据、声纹/人脸/定位等；未知时标记 `待确认`。
- 根据数据库能力生成 `{DATABASE_STACK}` 及 schema/seed 策略；无数据库时删除数据库章节。
- 根据对象存储和媒体能力生成 `{OBJECT_STORAGE_STACK}`；无上传/媒体/对象存储时简化该章节。
- 根据算法或模型能力生成 `{MODEL_ASSET_POLICY}`；无算法时删除模型章节或仅保留 `models/` 占位说明。
- 保持 data-management.md 与 security.md、media.md、object-storage.md、database.md、testing.md、directory-structure.md、.gitignore 一致。

### rules/database.md

基于 `assets/pm-harness/rules/database.md` 的模块化框架生成，作为数据库选型、Schema、迁移、Repository 和查询规则。

生成要求：
- 保留所有 `[通用]` 模块，包括数据库定位、Schema 与迁移、表设计、主键/时间/软删除/审计、索引与约束、Repository/DAO、查询事务、Seed/Fixtures、数据库变更文档、AI 更新规则和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{DATABASE_STACK}`、`{MIGRATION_STRATEGY}`、`{SCHEMA_FILES}`、`{REPOSITORY_PATTERN}`、`{CORE_TABLES}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如多数据库兼容、ORM/Model、租户隔离、审计、媒体/文件元数据、SQLite、PostgreSQL、MySQL、信创数据库。
- 单数据库项目只生成该数据库专项规则；多数据库项目必须生成 `{DATABASE_SUPPORT_MATRIX}` 并说明差异封装方式。
- 根据 BACKEND_STACK 生成 ORM、Repository、DAO 或手写 SQL 规则；不得保留不适用的框架或迁移工具。
- 根据 DB_PRIMARY 和信创数据库生成 schema、migration、DDL 文件路径；未知时标记 `待确认`。
- 根据产品定位和初始需求生成 `{CORE_TABLES}`；不确定的业务表写 `待确认`，不得保留模板业务表。
- 涉及文件、媒体、对象存储时生成元数据字段规则；没有此能力时删除或简化该章节。
- 保持 database.md 与 api.md、coding.md、data-management.md、compatibility.md、testing.md、environment.md 一致。

### rules/directory-structure.md

基于 `assets/pm-harness/rules/directory-structure.md` 的模块化框架生成，作为目录边界、文件归属、生成代码边界、文档归属、新增目录流程和目录同步规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、顶层目录职责、AI 工具目录、rules/docs/issues/iterations/openspec/compatibility/scripts/deploy/data/models/src/tests 目录边界、生成代码目录、文件归属决策表、禁止事项、新增目录流程和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{DEPLOYMENT_STACK}`、`{ENABLED_AGENT_TOOLS}`、`{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{ITERATION_PATTERN}`、`{CHANGE_ID_PATTERN}`、`{DOCS_STRUCTURE}`、`{GENERATED_CODE_DIRS}`、`{HAS_WEB}`、`{HAS_MINIAPP}`、`{HAS_MOBILE}`、`{HAS_DESKTOP}`、`{HAS_ALGORITHM}`、`{HAS_OBJECT_STORAGE}`、`{HAS_MEDIA}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如 Web、小程序、Android、iOS、桌面端、H5、算法、对象存储、媒体、模型文件、Kubernetes、Helm、私有化部署、AI 工具目录。
- 根据 PRODUCT_FORMS、HAS_WEB、HAS_MINIAPP、HAS_MOBILE、HAS_DESKTOP 生成 `src/` 子目录和 `compatibility/devices/` 文档；未启用的端不得保留强制目录要求。
- 根据 BACKEND_STACK 生成 `src/backend/` 入口文件、依赖文件、分层目录；非 Python/FastAPI 项目不得保留 Python 专属硬性描述。
- 根据 FRONTEND_STACK 生成 `src/web/` 结构和生成代码目录；无 Web 前端时删除 Web 前端强制规则。
- 根据 DATABASE_STACK 和兼容性要求生成数据库迁移、schema、compatibility/database 目录描述；无数据库时简化数据库相关描述。
- 根据 REQ_ROOT_DIR、BUG_ROOT_DIR、ITERATION_PATTERN、CHANGE_ID_PATTERN 生成 issues、iterations、openspec 的目录归属；必须与 requirement-management.md、bug-management.md、document-governance.md 一致。
- 根据 DOCS_STRUCTURE 生成 docs 分层；未知时默认使用主文档、standards、guides、knowledge-base、README 分层。
- 根据 GENERATED_CODE_DIRS 生成生成代码目录边界；未知时标记 `待确认`，不得编造生成工具。
- 根据 HAS_ALGORITHM 决定是否生成 `src/algorithm/` 和根 `models/` 目录规则；没有算法/模型需求时 `models/` 只保留占位说明或删除强制规则。
- 根据 HAS_OBJECT_STORAGE、HAS_MEDIA 生成 object-storage、media、data、tests fixtures 和 compatibility 相关目录规则；未启用能力删除强制要求。
- 根据 DEPLOYMENT_STACK 生成 `deploy/` 子目录规则；未启用 Kubernetes 时不得生成强制 `k8s/` 规则。
- 根据 ENABLED_AGENT_TOOLS 保留 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/`；未启用工具不得保留强制规则。
- 保持 directory-structure.md 与 AGENTS.md、README.md、project.yaml、global.md、document-governance.md、requirement-management.md、bug-management.md、coding.md、testing.md、data-management.md、database.md 一致。

### rules/document-governance.md

基于 `assets/pm-harness/rules/document-governance.md` 的模块化框架生成，作为 docs、issues、requirements、bugs、iterations、openspec、compatibility、rules 的文档生命周期、研发追溯、同步和归档规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、研发文档链路、docs 分层、文档分类、Markdown 元数据、docs 更新触发矩阵、issues/iterations/openspec 治理、自动同步矩阵、命名规范、质量要求、AI 执行顺序、轻量修订、评审确认、归档策略、禁止事项和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{DEPLOYMENT_STACK}`、`{PROJECT_GOVERNANCE_LEVEL}`、`{DOCS_STRUCTURE}`、`{ISSUE_WORKFLOW}`、`{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{ITERATION_PATTERN}`、`{SPRINT_FACT_SOURCE}`、`{CHANGE_ID_PATTERN}`、`{TASK_TRACKING_SYSTEM}`、`{DOC_REVIEW_POLICY}`、`{ARCHIVE_POLICY}`。
- 根据 PROJECT_GOVERNANCE_LEVEL 生成研发文档链路；未知时默认使用 `issues -> iterations -> openspec/changes -> src/tests -> docs/compatibility/rules -> openspec/specs -> openspec/archive`。
- 根据 DOCS_STRUCTURE 生成 docs 分层；未知时默认使用主文档、standards、guides、knowledge-base、README 分层。
- 根据 REQ_ROOT_DIR、BUG_ROOT_DIR、ISSUE_WORKFLOW 与 requirement-management.md、bug-management.md 生成 issues 治理；不得把需求、Bug、迭代放入 docs 根目录。
- 根据 ITERATION_PATTERN 与 SPRINT_FACT_SOURCE 生成迭代目录、四件套和事实源规则；未知时默认 `iterations/sprint-xxx/` 与 `sprint.yaml`。
- 根据是否启用 OpenSpec 生成 changes/specs/archive 章节；未启用时替换为项目等价变更系统，不得保留不可执行的 OpenSpec 强制要求。
- 根据 PRODUCT_FORMS 保留或删除 Web、小程序、移动端、桌面端、H5 相关 docs 和兼容性同步规则。
- 根据 BACKEND_STACK、FRONTEND_STACK、DATABASE_STACK、DEPLOYMENT_STACK、对象存储和算法能力生成自动同步矩阵；未启用能力不得保留强制同步要求。
- 根据 TASK_TRACKING_SYSTEM 保留 Jira、Linear、飞书、多维表格、GitHub Issues 或本地 backlog 章节；未启用时删除或标记为 `未启用`。
- 根据 DOC_REVIEW_POLICY 与 ARCHIVE_POLICY 生成人工确认和归档策略；未知时标记 `待确认`。
- 保持 document-governance.md 与 AGENTS.md、global.md、directory-structure.md、requirement-management.md、bug-management.md、api.md、database.md、testing.md、release.md、README.md 一致。

### rules/requirement-management.md

基于 `assets/pm-harness/rules/requirement-management.md` 的模块化框架生成，作为需求捕获、澄清、目录结构、状态机、命令阶段、评审门禁、Readiness、原型、验收标准、OpenSpec 转换、迭代流转、变更控制和 AI 处理边界规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、需求治理总原则、目录结构、状态机、需求类型与优先级、捕获与澄清、需求包六件套、验收标准、Readiness 门禁、评审门禁、trace 最小字段、变更控制、AI 处理规则、同步关系、初始化生成建议和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{REQ_ROOT_DIR}`、`{REQ_ID_PATTERN}`、`{REQ_REGISTRY_FILE}`、`{REQ_COMMANDS}`、`{REQ_STATUS_MACHINE}`、`{REQ_PRIORITY_LEVELS}`、`{REQ_TYPE_TAXONOMY}`、`{REQ_REVIEW_POLICY}`、`{REQ_READINESS_POLICY}`、`{REQ_SPRINT_POLICY}`、`{REQ_TO_CHANGE_POLICY}`、`{REQ_PROTOTYPE_POLICY}`、`{REQ_ACCEPTANCE_POLICY}`、`{REQ_TRACE_POLICY}`、`{REQ_CHANGE_CONTROL_POLICY}`、`{TASK_TRACKING_SYSTEM}`。
- 根据 ISSUE_WORKFLOW、ITERATION_PATTERN、CHANGE_ID_PATTERN、TASK_TRACKING_SYSTEM 生成需求目录、状态流转、进入迭代和转研发变更规则；未知时标记 `待确认`。
- 根据实际命令目录生成 REQ_COMMANDS；不得保留不存在的 `/req-*`、`requirement-to-opsx` 或其他来源项目命令名。
- 根据团队产品治理策略生成 REQ_TYPE_TAXONOMY、REQ_PRIORITY_LEVELS、REQ_REVIEW_POLICY 和 REQ_READINESS_POLICY；未知时保留模板默认值并标记需要人工确认。
- 根据是否启用 OpenSpec、Sprint、外部看板、CI/CD、发布流程生成 REQ_TO_CHANGE_POLICY、REQ_SPRINT_POLICY 和 trace 规则；未启用能力删除对应强制章节。
- 根据 HAS_WEB、HAS_MINIAPP、HAS_MOBILE、HAS_DESKTOP、UI_STACK 生成原型目录与设计评审规则；无 UI 或原型流程时删除或标记为“不适用”。
- 根据 api、database、security、media、object-storage、compatibility、ui-design、testing 能力生成验收标准同步矩阵；未启用能力不得保留强制验收项。
- 根据是否存在客户需求、合规需求或外部看板生成客户/合规/外部看板章节；未启用时删除或标记为“不适用”。
- 保持 requirement-management.md 与 document-governance.md、directory-structure.md、testing.md、bug-management.md、release.md、api.md、database.md、security.md、ui-design.md 一致。

### rules/bug-management.md

基于 `assets/pm-harness/rules/bug-management.md` 的模块化框架生成，作为 Bug 捕获、分级、复现、根因分析、状态机、目录结构、评审门禁、OpenSpec 转换、回归测试、知识沉淀和 AI 处理边界规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、缺陷治理总原则、目录结构、状态机、严重等级与优先级、捕获与复现、根因分析、评审门禁、迭代与修复流转、验收与回归测试、AI 处理规则、同步关系、初始化生成建议和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{BUG_ROOT_DIR}`、`{BUG_ID_PATTERN}`、`{BUG_REGISTRY_FILE}`、`{BUG_COMMANDS}`、`{BUG_STATUS_MACHINE}`、`{BUG_SEVERITY_LEVELS}`、`{BUG_PRIORITY_LEVELS}`、`{BUG_REVIEW_POLICY}`、`{BUG_SPRINT_POLICY}`、`{BUG_TO_CHANGE_POLICY}`、`{BUG_EVIDENCE_POLICY}`、`{BUG_TEST_POLICY}`、`{BUG_KB_POLICY}`、`{BUG_SLA_POLICY}`。
- 根据 ISSUE_WORKFLOW、ITERATION_PATTERN、CHANGE_ID_PATTERN、TASK_TRACKING_SYSTEM 生成 Bug 目录、状态流转、进入迭代和转修复变更规则；未知时标记 `待确认`。
- 根据实际命令目录生成 BUG_COMMANDS；不得保留不存在的 `/bug-*`、`bug-to-change` 或其他来源项目命令名。
- 根据团队质量策略生成 BUG_SEVERITY_LEVELS、BUG_PRIORITY_LEVELS 和 BUG_REVIEW_POLICY；未知时保留模板默认等级并标记需要人工确认。
- 根据是否启用 OpenSpec、Sprint、外部看板、CI/CD、发布流程生成 BUG_TO_CHANGE_POLICY、BUG_SPRINT_POLICY 和 trace 规则；未启用能力删除对应强制章节。
- 根据 security、database、media、object-storage、compatibility、ui-design、testing 能力保留或删除安全缺陷、数据缺陷、上传/媒体缺陷、兼容缺陷、UI 缺陷和回归测试同步规则。
- 根据是否存在线上 SLA、值班、客户工单或事故响应生成 BUG_SLA_POLICY；未启用时删除或标记为“不适用”。
- 保持 bug-management.md 与 document-governance.md、directory-structure.md、testing.md、security.md、release.md、api.md、database.md、media.md、object-storage.md、compatibility.md、ui-design.md 一致。

### rules/environment.md

基于 `assets/pm-harness/rules/environment.md` 的模块化框架生成，作为 .env.example、运行环境、密钥边界、服务配置和部署环境同步规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、基本原则、环境文件归属、命名规范、环境分类、安全要求、AI 更新规则、校验与启动前检查、禁止事项和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{DEPLOYMENT_STACK}`、`{CONFIG_LOADER}`、`{ENVIRONMENTS}`、`{PUBLIC_ENV_PREFIX}`。
- 根据 BACKEND_STACK 生成配置加载方式，例如 Python/FastAPI 使用 pydantic-settings，Spring Boot 使用 application.yml + env override，Node/NestJS 使用 ConfigModule；未知时标记 `待确认`。
- 根据 FRONTEND_STACK 生成前端公开变量前缀；无 Web/H5/移动端前端时删除前端构建时变量和运行时配置章节。
- 根据 DB_PRIMARY 生成数据库环境变量；单数据库优先 `DATABASE_URL`，多数据库或信创适配可使用 `DB_TYPE/DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME`。
- 根据对象存储、文件上传、媒体、模型能力保留或删除对象存储与文件配置章节；未启用时不得保留 MinIO/S3 强制变量。
- 根据 DEPLOYMENT_STACK 保留 Docker Compose、Kubernetes、SaaS、私有化部署章节；未启用 Kubernetes 时不得生成 Secret/ConfigMap 硬性要求。
- 根据是否启用 Redis、异步任务、第三方服务、License、算法服务生成对应变量分类；未启用能力不得保留强制必填变量。
- 所有示例密钥必须使用明显不可用于生产的占位值，不得生成真实 Token、真实 IP、客户名、生产域名。
- 保持 environment.md 与 `.env.example`、`src/backend/.env.example`、`docker-compose.yml`、README.md、docs/02-deployment.md、port-management.md、security.md、compatibility.md 一致。

### rules/media.md

基于 `assets/pm-harness/rules/media.md` 的模块化框架生成，作为图片、音频、视频、文档、导入导出、转码产物、对象存储和上传安全规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、媒体能力总览、存储原则、上传入口、安全规则、访问控制、本地开发与测试数据边界、环境变量、AI 更新规则、禁止事项和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{MEDIA_ENABLED}`、`{MEDIA_TYPES}`、`{OBJECT_STORAGE_STACK}`、`{MEDIA_BUCKET_POLICY}`、`{MEDIA_KEY_PATTERN}`、`{MAX_UPLOAD_POLICY}`、`{MEDIA_PROCESSING_PIPELINE}`、`{FRONTEND_MEDIA_STACK}`。
- 根据 MEDIA_ENABLED 决定是否生成完整媒体规范；未启用媒体/文件上传能力时，仅保留占位说明、安全边界和禁止事项。
- 根据 MEDIA_TYPES 保留或删除图片、音频、视频、文档、导入导出、处理产物章节；未启用类型不得保留强制格式、变量、API、测试要求。
- 根据 OBJECT_STORAGE_STACK 生成对象存储、Bucket、对象 Key、签名 URL 和访问控制规则；无对象存储时改为文件系统策略。
- 根据 FORMS 生成 Web、小程序、移动端、桌面端的上传、预览、播放、录音录像限制。
- 根据 MEDIA_PROCESSING_PIPELINE 生成缩略图、封面、转码、ASR、OCR、异步任务和处理状态规则；无处理流程时删除强制处理要求。
- 根据 MAX_UPLOAD_POLICY 生成大小、格式、MIME、文件头、时长、分辨率限制；未知时标记 `待确认`，不得编造生产限制。
- 根据 FRONTEND_MEDIA_STACK 生成前端上传组件、播放器、录音、波形、预览能力；无前端时删除前端媒体章节。
- 保持 media.md 与 object-storage.md、data-management.md、environment.md、api.md、database.md、security.md、testing.md、docs/06-video-asset-management.md 一致。

### rules/object-storage.md

基于 `assets/pm-harness/rules/object-storage.md` 的模块化框架生成，作为对象存储启用条件、供应商适配、Bucket、对象 Key、权限、签名 URL、生命周期和兼容性规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、总原则、启用条件、Bucket 策略、对象 Key 规范、存储客户端接口、上传下载访问控制、安全要求、AI 更新规则、禁止事项和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{OBJECT_STORAGE_ENABLED}`、`{OBJECT_STORAGE_STACK}`、`{OBJECT_STORAGE_PROVIDER_MATRIX}`、`{BUCKET_NAME}`、`{BUCKET_POLICY}`、`{OBJECT_KEY_PREFIXES}`、`{STORAGE_CLIENT_INTERFACE}`、`{SIGNED_URL_POLICY}`、`{LIFECYCLE_POLICY}`。
- 根据 OBJECT_STORAGE_ENABLED 决定生成完整对象存储规范或未启用占位说明；未启用时不得保留 MinIO/S3/COS/OBS/RustFS 强制变量和测试要求。
- 根据 OBJECT_STORAGE_STACK 生成供应商兼容矩阵和适配层描述；单供应商项目只保留该供应商，多供应商项目必须保留工厂/adapter 规则。
- 根据 BUCKET_POLICY 生成单 Bucket、多 Bucket、租户隔离或文件系统策略；默认推荐一个项目一个 Bucket，桶内按前缀区分资源。
- 根据 OBJECT_KEY_PREFIXES 生成项目专属对象前缀，不得保留样例业务前缀。
- 根据 BACKEND_STACK 生成 STORAGE_CLIENT_INTERFACE；业务层不得直接依赖具体供应商 SDK。
- 根据 SIGNED_URL_POLICY 生成上传/下载签名 URL 有效期、用途和权限约束；无签名 URL 能力时删除该强制规则。
- 根据 LIFECYCLE_POLICY 生成 tmp、imports、exports、processed、models 等对象清理策略；未知时标记 `待确认`。
- 保持 object-storage.md 与 media.md、data-management.md、environment.md、security.md、compatibility.md、port-management.md、docs/07-object-storage-strategy.md 一致。

### rules/port-management.md

基于 `assets/pm-harness/rules/port-management.md` 的模块化框架生成，作为开发端口、Docker 端口、宿主机映射、冲突处理和服务拓扑端口规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、总体策略、端口分层、环境变量映射、端口冲突处理、端口校验、安全边界、AI 更新规则、禁止事项和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{SERVICE_PORT_MATRIX}`、`{BACKEND_PORT}`、`{WEB_PORT}`、`{GATEWAY_PORT}`、`{DATABASE_PORT}`、`{OBJECT_STORAGE_PORTS}`、`{ALGORITHM_PORT}`、`{DEPLOYMENT_PORT_MATRIX}`、`{PORT_ENV_VARS}`、`{PORT_CHECK_COMMAND}`。
- 根据 FORMS、BACKEND_STACK、FRONTEND_STACK、DB_PRIMARY、OBJECT_STORAGE_STACK、HAS_ALGORITHM 和 DEPLOYMENT_STACK 生成 SERVICE_PORT_MATRIX；未启用服务不得出现在强制端口矩阵中。
- 默认采用“容器内固定，宿主机可变”策略；端口冲突优先调整 `HOST_PORT_*` 宿主机映射变量，不得随意修改应用内部监听端口。
- 根据 Docker Compose、Kubernetes、SaaS、私有化等部署方式生成 DEPLOYMENT_PORT_MATRIX；未启用部署模式删除对应强制规则。
- 根据实际 `.env.example` 和 `docker-compose.yml` 生成 PORT_ENV_VARS；不得编造不存在的环境变量。
- 根据实际脚本生成 PORT_CHECK_COMMAND；未知时标记 `待确认`。
- 保持 port-management.md 与 environment.md、object-storage.md、compatibility.md、security.md、docs/02-deployment.md、README.md、docker-compose.yml 一致。

### rules/release.md

基于 `assets/pm-harness/rules/release.md` 的模块化框架生成，作为版本发布、准入检查、构建打包、部署验证、发布说明、回滚和归档规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、发布原则、发布准入、版本策略、构建目标、镜像/制品管理、部署验证、配置发布、发布说明、回滚策略、归档同步、AI 更新规则、禁止事项和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{RELEASE_CHANNELS}`、`{VERSION_STRATEGY}`、`{BUILD_TARGETS}`、`{VERIFY_COMMANDS}`、`{BUILD_COMMANDS}`、`{DEPLOYMENT_STACK}`、`{DEPLOYMENT_VERIFY_CHECKLIST}`、`{ROLLBACK_STRATEGY}`、`{RELEASE_NOTE_TEMPLATE}`。
- 根据 FORMS、BACKEND_STACK、FRONTEND_STACK、HAS_ALGORITHM、DB_PRIMARY、OBJECT_STORAGE_STACK 和 DEPLOYMENT_STACK 生成 BUILD_TARGETS；未启用服务/端不得出现在强制构建目标中。
- 根据实际脚本生成 VERIFY_COMMANDS 和 BUILD_COMMANDS；未知时标记 `待确认`，不得编造命令。
- 根据 DEPLOYMENT_STACK 生成 Docker Compose、Kubernetes、SaaS、私有化、离线交付或 CI/CD 章节；未启用方式删除强制规则。
- 根据数据库、环境变量、对象存储、媒体、算法、移动端能力保留或删除对应 `[条件启用]` 发布规则。
- 根据 VERSION_STRATEGY 生成版本号、镜像 tag、制品命名和可追溯规则；未知时标记 `待确认`。
- 根据 ROLLBACK_STRATEGY 生成镜像、配置、数据库、前端、移动端、算法模型等回滚规则；无明确方案时写 `待确认`。
- 保持 release.md 与 testing.md、environment.md、database.md、api.md、compatibility.md、document-governance.md、README.md、docs/02-deployment.md 一致。

### rules/security.md

基于 `assets/pm-harness/rules/security.md` 的模块化框架生成，作为敏感信息、认证授权、输入校验、上传与对象存储、外部服务、日志脱敏、部署安全、License、Guard 和 AI 安全边界规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、安全总原则、敏感信息管理、输入校验、日志审计、AI 安全行为、安全变更同步矩阵、初始化生成建议和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{AUTH_STRATEGY}`、`{AUTH_PROVIDER}`、`{PERMISSION_MODEL}`、`{TOKEN_STORAGE_POLICY}`、`{SENSITIVE_SECRET_TYPES}`、`{SENSITIVE_DATA_TYPES}`、`{UPLOAD_SECURITY_POLICY}`、`{OBJECT_STORAGE_SECURITY}`、`{EXTERNAL_SERVICE_SECURITY}`、`{DEPLOYMENT_SECURITY_BASELINE}`、`{LICENSE_SECURITY_POLICY}`、`{GUARD_POLICY}`。
- 根据 AUTH_STRATEGY 和 AUTH_PROVIDER 生成认证要求；未明确公开的业务 API 默认必须鉴权，公开端点必须与 api.md 保持一致。
- 根据 PERMISSION_MODEL 生成角色、租户、资源、数据范围、管理端、用户端、内部接口和开放接口的权限边界；未知时标记 `待确认`。
- 根据 FRONTEND_STACK、HAS_WEB、TOKEN_STORAGE_POLICY 生成前端安全规则；无前端登录态时删除或标记前端章节为“不适用”。
- 根据 HAS_MEDIA、HAS_UPLOAD、OBJECT_STORAGE_STACK、DATA_MANAGEMENT_SCOPE 生成上传、媒体、下载、预览、对象存储、导入导出安全规则；未启用能力不得保留强制实现要求。
- 根据 EXTERNAL_SERVICES、HAS_LLM、HAS_OAUTH、HAS_WEBHOOK、HAS_PAYMENT、HAS_SMS_EMAIL 生成外部服务安全规则；未知超时、脱敏、签名策略时标记 `待确认`。
- 根据 DEPLOYMENT_STACK 生成 HTTPS、网关、CORS、安全 Header、非 root 容器、端口暴露、Kubernetes Secret、私有化部署等规则；未启用部署模式删除对应强制规则。
- 根据 HAS_LICENSE、HAS_PRIVATE_DEPLOYMENT、COMPATIBILITY_TARGETS 生成 License、私有化、信创和合规适配规则；未启用时删除或标记为“不适用”。
- 根据 GUARD_POLICY 生成审批、命令执行、高风险变更和仓库外写入规则；未启用 Guard 时保留 AI 安全底线并删除审批落盘要求。
- 保持 security.md 与 global.md、api.md、environment.md、data-management.md、database.md、media.md、object-storage.md、release.md、port-management.md、compatibility.md 一致。

### rules/testing.md

基于 `assets/pm-harness/rules/testing.md` 的模块化框架生成，作为测试分层、覆盖率目标、TDD、Mock、Fixture、接口测试、前端测试、E2E、外部服务、数据隔离、运行命令和 AI 测试行为规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、测试总原则、测试用例结构、必须覆盖场景、TDD 与需求追踪、AI 修改测试规则、同步关系、初始化生成建议和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{TEST_STRATEGY}`、`{BACKEND_TEST_STACK}`、`{FRONTEND_TEST_STACK}`、`{MOBILE_TEST_STACK}`、`{E2E_TEST_STACK}`、`{COVERAGE_TARGET}`、`{COVERAGE_BY_LAYER}`、`{TEST_COMMANDS}`、`{CI_TEST_COMMAND}`、`{UNIT_TEST_COMMAND}`、`{INTEGRATION_TEST_COMMAND}`、`{COVERAGE_COMMAND}`、`{FRONTEND_CHECK_COMMAND}`、`{E2E_TEST_COMMAND}`、`{TEST_DATABASE_STRATEGY}`、`{FIXTURE_STRATEGY}`、`{MOCK_STRATEGY}`、`{API_TEST_STRATEGY}`、`{SECURITY_TEST_STRATEGY}`、`{PERFORMANCE_TEST_STRATEGY}`。
- 根据 BACKEND_STACK、FRONTEND_STACK、MOBILE_STACK、HAS_WEB、HAS_MINIAPP、HAS_DESKTOP、HAS_SDK、HAS_ALGORITHM 生成测试分层和测试栈；未启用端或模块不得保留强制测试要求。
- 根据实际 `package.json`、Makefile、脚本目录、CI 配置和测试框架生成 TEST_COMMANDS；命令未知时标记 `待确认`，不得编造。
- 根据 DB_PRIMARY、DATABASE_STACK、COMPATIBILITY_TARGETS 生成测试数据库、事务回滚、迁移测试、多数据库兼容测试规则；无数据库时删除对应强制章节。
- 根据 API_PREFIX、OPENAPI_SOURCE、HAS_WEBHOOK、HAS_SDK 生成 API 与契约测试规则；无 API 时删除对应强制章节。
- 根据 HAS_UPLOAD、HAS_MEDIA、OBJECT_STORAGE_STACK、DATA_MANAGEMENT_SCOPE 生成上传、媒体、下载、预览和对象存储测试规则；未启用能力删除对应章节。
- 根据 AUTH_STRATEGY、PERMISSION_MODEL、SENSITIVE_DATA_TYPES 生成安全测试规则；权限、安全或敏感数据策略未知时标记 `待确认`。
- 根据 DEPLOYMENT_STACK、RELEASE_CHANNELS、CI_PROVIDER 生成 CI、发布门禁、E2E、性能和稳定性测试规则；未启用 CI/CD 时标记为“本地手动执行”或 `待确认`。
- 保持 testing.md 与 global.md、coding.md、api.md、database.md、data-management.md、security.md、media.md、object-storage.md、compatibility.md、release.md 一致。

### rules/ui-design.md

基于 `assets/pm-harness/rules/ui-design.md` 的模块化框架生成，作为产品设计定位、Design Token、组件体系、页面结构、交互状态、响应式、可访问性、内容呈现、视觉验收和 AI UI 修改边界规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、设计定位、UI 技术栈、色彩系统、字体/间距/布局密度、组件使用优先级、核心组件规范、页面结构、交互反馈、可访问性、视觉验收、AI UI 修改规则、同步关系、初始化生成建议和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_POSITIONING}`、`{TARGET_USERS}`、`{SUPPORTED_CLIENTS}`、`{UI_STACK}`、`{FRONTEND_FRAMEWORK}`、`{STYLE_SYSTEM}`、`{COMPONENT_LIBRARY}`、`{ICON_LIBRARY}`、`{STATE_MANAGEMENT}`、`{FORM_STACK}`、`{CHART_STACK}`、`{MOTION_STACK}`、`{DESIGN_STYLE}`、`{DESIGN_PRINCIPLES}`、`{DESIGN_TOKEN_SOURCE}`、`{TOKEN_SYNC_COMMAND}`、`{ROUTE_LAYOUTS}`、`{CORE_PAGES}`、`{CORE_COMPONENTS}`、`{RESPONSIVE_POLICY}`、`{ACCESSIBILITY_TARGET}`、`{I18N_POLICY}`、`{THEMING_POLICY}`、`{UI_VERIFY_COMMANDS}`、`{VISUAL_ACCEPTANCE_SOURCE}`。
- 根据 FRONTEND_STACK、HAS_WEB、HAS_MINIAPP、HAS_MOBILE、HAS_DESKTOP、SUPPORTED_CLIENTS 生成 UI 适用范围；无 UI 项目应删除强制前端规范或标记为“不适用”。
- 根据 UI_STACK、COMPONENT_LIBRARY、ICON_LIBRARY、STYLE_SYSTEM 生成组件复用优先级和技术栈表；不得保留 React/Tailwind/shadcn 等未启用技术的强制规则。
- 根据 DESIGN_STYLE、PRODUCT_POSITIONING、TARGET_USERS 生成设计定位、色彩、字体、间距、布局密度和交互原则；不得保留来源项目品牌名、颜色、页面名、业务模块或客户名。
- 根据 DESIGN_TOKEN_SOURCE 和 TOKEN_SYNC_COMMAND 生成 Design Token 章节；未建立 Token 系统时标记 `待完善`，并保留最小颜色/字体/间距/圆角约束。
- 根据 CORE_PAGES、ROUTE_LAYOUTS、CORE_COMPONENTS 生成页面结构和核心组件规范；未启用页面类型不得保留强制实现要求。
- 根据 HAS_MEDIA、HAS_UPLOAD、HAS_CHARTS、HAS_3D、HAS_MAP、OBJECT_STORAGE_STACK 生成媒体、图片和可视化章节；未启用能力删除对应章节。
- 根据 RESPONSIVE_POLICY、ACCESSIBILITY_TARGET、I18N_POLICY、THEMING_POLICY 生成响应式、可访问性、国际化、主题和白标规则；未知时标记 `待确认`。
- 根据 package.json、脚本目录、测试配置、设计稿或原型来源生成 UI_VERIFY_COMMANDS 和 VISUAL_ACCEPTANCE_SOURCE；命令未知时标记 `待确认`，不得编造。
- 保持 ui-design.md 与 directory-structure.md、coding.md、api.md、language.md、media.md、object-storage.md、security.md、testing.md、compatibility.md、environment.md、release.md 一致。

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
