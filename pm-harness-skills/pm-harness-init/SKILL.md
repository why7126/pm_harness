---
name: pm-harness-init
description: 初始化 AI Coding 项目的 harness 工程结构。当用户需要为新项目生成标准化的 pm-harness 工程框架时使用本技能。触发场景包括：初始化新项目工程结构、生成 AI 编码脚手架、创建 pm-harness 工程、搭建 OpenSpec + AI Agent 规范编程项目结构。技能会按预设顺序收集产品名称、产品编号、产品信息、能力、形态、存储、技术栈、数据库、编码 Agent 与必填 UI 设计；上传 ui-design.md 时严格遵循，手工描述时自动推导设计方案，再生成完整的参数化 harness 工程 zip 包。
---

# PM Harness 工程初始化技能

## 概述

本技能基于 `pm-harness` 模板工程，结合用户输入的产品信息，生成一个适用于 AI Coding（OpenSpec + AI Agent 规范编程）项目的标准化 harness 工程结构，最终输出 zip 包。

## 资产说明

本技能打包了以下资产，执行时必须以这些文件为基础，不得凭空生成：

| 资产路径 | 用途 |
|---------|------|
| `assets/pm-harness-template` | 轻量 pm-harness 模板工程，核心文档、规则、脚本和 `.claude/` 命令样本的事实源 |
| `assets/templates/requirements-template-README.md` | 需求模板目录说明 |
| `assets/templates/requirement-template.md` | requirement.md 文件模板 |
| `assets/templates/bugs-template-README.md` | Bug 模板目录说明 |
| `assets/templates/bug-template.md` | bug.md 文件模板 |

**重要**：执行 Step 3 构建工程目录时，必须先复制 `assets/pm-harness-template/` 作为基础，在此基础上做参数化替换、目录补齐和命令生成，而不是从零创建核心文档。为满足 Claude Skill 文件数量限制，模板工程不再预置所有 Agent 工具目录、OpenSpec 历史 Change、示例需求和示例迭代；嵌套 OpenSpec Skill 样本使用 `SKILL.template.md` 命名，初始化输出时再生成目标目录所需的 `SKILL.md`。

## 用户输入参数

收集用户输入前必须完整读取以下 reference：

| Reference | 读取时机 | 职责 |
|---|---|---|
| [user-input-schema.md](references/user-input-schema.md) | 收集输入、派生变量、处理缺省值时 | 顺序化必填输入、默认值、冲突处理、自动派生和推导配置摘要规则 |
| [agent-tool-mapping.md](references/agent-tool-mapping.md) | 解析 Agent 选择、生成工具目录时 | Agent 名称标准化、目录映射、命令和嵌套 Skill 渲染规则 |
| [default-command-catalog.md](references/default-command-catalog.md) | 生成 Agent 命令、启用或禁用治理流程时 | 默认命令族、命令语义和条件启用规则 |

输入收集原则：严格按 `user-input-schema.md` 的顺序提示全部必填用户决策；不得额外追问内部变量、固定目录或可自动派生的配置。默认项须展示并允许确认，冲突项须即时互斥处理；其余变量由 AI 自动派生并在推导配置摘要中展示，不得编造。

## 执行步骤

### Step 1：收集用户输入

1. 完整读取 [user-input-schema.md](references/user-input-schema.md)。
2. 严格按 schema 的 16 个输入步骤逐项收集或确认；用户一次性提供的有效字段可跳过重复提问，但不得改变剩余步骤顺序。
3. 对“其他”收集补充文本，并即时处理对象存储与信创数据库的互斥选项。
4. 在 UI 设计步骤中，要求用户二选一：上传 `ui-design.md` 或手工输入 UI 设计风格。上传文档时严格遵循其明确内容；手工输入时按 schema 引导收集风格信息，再由 AI 自动派生设计方案。
5. 自动派生内部变量、固定目录和默认配置，生成推导配置摘要供用户确认或修正。
6. 用户未回复摘要时，以已收集的必填项和自动派生值继续生成；不得追加推荐确认或条件追问。

### Step 2：派生基础变量

按 [user-input-schema.md](references/user-input-schema.md) 的字段定义、默认值和“变量派生”规则生成全部变量。变量必须在后续文档、目录、命令和配置中保持一致。

### Step 3：构建工程目录

1. 复制 `assets/pm-harness-template/` 到 `/home/claude/output/{PRODUCT_CODE}/`
2. 确认输出目录名为 `{PRODUCT_CODE}/`
3. 根据 `ENABLED_AGENT_TOOLS` 保留或生成 Agent 工具目录；基于 `.claude/` 命令样本和「Agent 工具目录」规则生成已启用工具目录；将 OpenSpec Skill 样本 `SKILL.template.md` 渲染为输出项目中的 `SKILL.md`；若 `Claude Code` 未启用，生成完成后从输出中删除 `.claude/`
4. 创建模板中未预置的空目录：`issues/`、`iterations/`、`openspec/specs/`、`openspec/changes/`、`openspec/archive/`、`docs/knowledge-base/`、`data/`
5. 在此基础上执行参数化替换和目录调整（见「文件生成规则」章节）

### Step 4：生成所有文件

按照「文件生成规则」章节逐一生成文件内容。

所有自动生成的 Markdown 文件必须包含 YAML Frontmatter 中的 `created_at` 和 `updated_at` 字段，格式统一为 `YYYY-MM-DD hh:mm:ss`。初始化生成时先计算一次当前本地时间作为 `{GENERATED_AT}`，新建文件的 `created_at` 与 `updated_at` 均写 `{GENERATED_AT}`；若基于模板文件生成，必须替换模板中的示例时间，不得原样保留模板资产的时间戳。

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
├── .claude/                    # Claude Code 启用时保留默认 commands + skills
├── .codex/                     # Codex 启用时基于 .claude 语义生成 prompts + skills
├── .cursor/                    # Cursor 启用时基于 .claude 语义生成 commands + skills
├── .kiro/                      # Kiro 启用时基于 .claude 语义生成 prompts + skills
├── .opencode/                  # OpenCode 启用时基于 .claude 语义生成 commands + skills
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
│   ├── README.md
│   ├── database/
│   │   ├── {db_primary}.md         # 以实际数据库命名
│   │   ├── postgresql.md           # 支持 PostgreSQL 时创建
│   │   ├── mysql.md                # 支持 MySQL 时创建
│   │   ├── dm.md                   # 信创数据库包含达梦时创建
│   │   ├── highgo.md               # 信创数据库包含海量时创建
│   │   ├── migration-rules.md
│   │   └── test-matrix.md
│   ├── devices/                    # 根据产品形态创建
│   │   ├── web.md                  # HAS_WEB=true 时创建
│   │   ├── wechat-miniapp.md       # HAS_WECHAT_MINIAPP=true 时创建
│   │   ├── h5.md                   # HAS_H5=true 时创建
│   │   ├── desktop.md              # HAS_DESKTOP=true 时创建
│   │   ├── android.md              # HAS_ANDROID=true 时创建
│   │   └── ios.md                  # HAS_IOS=true 时创建
│   └── object-storage/
│       ├── README.md
│       ├── minio.md
│       ├── s3.md
│       ├── cos.md
│       ├── oss.md
│       ├── obs.md
│       └── rustfs.md
├── data/                       # 初始化阶段仅保留 .gitkeep
├── docs/
│   ├── README.md
│   ├── 00-product-overview.md
│   ├── 01-architecture.md
│   ├── 02-deployment.md
│   ├── 03-api-index.md
│   ├── 04-database-design.md
│   ├── 05-compatibility-matrix.md
│   ├── 06-video-asset-management.md  # 如有媒体需求保留，否则标注为"待定"
│   ├── 07-object-storage-strategy.md
│   ├── standards/
│   │   ├── api-governance.md
│   │   ├── authentication.md
│   │   ├── error-codes.md
│   │   ├── file_upload.md
│   │   ├── frontend-test-standard.md
│   │   ├── openapi-rules.md
│   │   ├── test-coverage.md
│   │   ├── testing-governance.md
│   │   └── unit-test-standard.md
│   └── knowledge-base/         # 初始化阶段仅保留 .gitkeep 或按需创建 README
├── issues/
│   ├── requirements/
│   │   ├── plan/               # 规划中、评审未完成
│   │   ├── review/             # 已完成评审，尚未归档
│   │   └── archive/            # 已验收关闭并归档
│   └── bugs/
│       ├── plan/               # 规划中、评审未完成
│       ├── review/             # 已完成评审，尚未归档
│       └── archive/            # 已修复关闭并归档
├── iterations/                 # 初始化阶段仅保留 .gitkeep
├── openspec/
│   ├── project.md
│   ├── config.yaml
│   ├── specs/                  # 初始化阶段仅保留 .gitkeep
│   ├── changes/                # 初始化阶段仅保留 .gitkeep
│   └── archive/                # 初始化阶段仅保留 .gitkeep
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
│   ├── issues-lifecycle.md
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
│   ├── wechat-miniapp/                # HAS_WECHAT_MINIAPP=true 时创建
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

基于 `assets/pm-harness-template/AGENTS.md` 的模块化框架生成，不做简单全文替换后直接交付。

生成要求：
- 保留所有 `[通用]` 模块。
- 用用户输入替换所有 `[个性化]` 占位符；缺失信息标记为 `待确认`。
- 用用户输入替换 AGENTS.md 核心占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_DESCRIPTION}`、`{BUSINESS_DOMAIN}`、`{TARGET_USERS}`、`{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{ASYNC_TASK_STACK}`、`{ALGORITHM_STACK}`、`{DEPLOYMENT_STACK}`、`{ENABLED_AGENT_TOOLS}`、`{PRIMARY_AGENT_TOOL}`、`{PRIMARY_VERIFY_COMMAND}`。
- AGENTS.md 必须保留默认自定义命令基线：综合捕获 `/capture`、需求治理 `/req-*`、缺陷治理 `/bug-*`、Sprint 治理 `/sprint-*`、项目基线 `/initialize-project`、`/build-design-system`、`/build-api-standard`、`/build-test-framework`，以及 OpenSpec `/opsx-*` 命令族；仅允许按项目能力删除不适用的条件启用说明，不得改变同名命令的输入、输出、是否生成文档和是否生成代码边界。
- `ENABLED_AGENT_TOOLS` 中启用的 `.cursor/`、`.claude/`、`.codex/`、`.kiro/`、`.opencode/` 必须保留同一套默认命令语义；不同工具只允许按目录约定使用 commands、prompts 或分组路径。
- AGENTS.md 中项目验证、开发、部署类占位符必须按实际脚本或命令替换，例如 `{DIRECTORY_VALIDATE_COMMAND}`、`{OPENSPEC_VALIDATE_COMMAND}`、`{TEST_COMMAND}`、`{BUILD_COMMAND}`、`{DEV_COMMAND}`、`{DOCKER_UP_COMMAND}`、`{DOCKER_DOWN_COMMAND}`。
- AGENTS.md 中所有路径、URL 与策略占位符必须按实际工程替换或删除对应模块，例如 `{DESIGN_TOKEN_PATH}`、`{BASE_COMPONENT_PATH}`、`{COMPOSITE_COMPONENT_PATH}`、`{BUSINESS_COMPONENT_PATH}`、`{PAGE_TEMPLATE_PATH}`、`{DESIGN_SYSTEM_PREVIEW_URL}`、`{SERVICE_URLS}`、`{FORBIDDEN_DIRECTORIES}`、`{UI_TOKEN_POLICY}`、`{UI_COMPONENT_POLICY}`、`{UI_VISUAL_ACCEPTANCE_POLICY}`。
- 根据项目能力保留、删除或简化 `[条件启用]` 模块，例如 monorepo、前端 UI、算法、对象存储、部署、移动端、桌面端、多 Agent 工具、Sprint 治理、原型验收。
- 「项目定位」「系统包含」「必读文档」「rules 使用规则」「强制规则」「常用命令」「完成任务后检查清单」必须根据 FORMS、HAS_ALGORITHM、BACKEND_STACK、FRONTEND_STACK、DB_PRIMARY、OBJECT_STORAGE_ENABLED、MEDIA_ENABLED 和 DEPLOYMENT_STACK 生成。
- 如果启用需求、缺陷、Sprint 命令，必须生成 `req-*`、`bug-*`、`sprint-*`、`opsx-*` 的命令表；如果项目命令名不同，必须整体替换为项目命令，不得保留旧命令。
- 如果启用多个 Agent 工具，必须生成命令事实源、同步目标和同步命令；未启用时删除该条件模块。
- 如果存在 UI prototype、截图或设计稿，必须保留「原型与视觉验收优先级」模块；无 UI 时删除 UI 与 Design System 相关模块。
- 原型 PNG/视觉稿不属于初始化用户输入；它仅可在后续需求中作为可选附件使用，缺失时不得阻塞需求完善、实现或验收，改按 UI 规范、验收标准和浏览器验证执行。
- 如果启用数据、媒体、对象存储或模型能力，必须保留对应文件边界和检查项，并与 `rules/data-management.md`、`rules/media.md`、`rules/object-storage.md`、`rules/directory-structure.md` 保持一致。
- 不得保留指向不存在目录、命令、服务地址、子项目规则入口、Design System 预览页或客户端生成脚本的内容。
- 文档元数据 note 字段更新为 `适用于 {PRODUCT_NAME} 项目；AI 执行任何任务前必须优先阅读本文档`。
- 文档元数据必须包含 `created_at` 和 `updated_at`，二者在初始化生成时均使用 `{GENERATED_AT}`，格式为 `YYYY-MM-DD hh:mm:ss`。
- 保持 AGENTS.md 与 README.md、project.yaml、rules/global.md、rules/directory-structure.md、rules/document-governance.md、rules/issues-lifecycle.md、rules/requirement-management.md、rules/bug-management.md、rules/testing.md、rules/release.md 的流程、目录和命令命名一致。
- 生成后必须检查 AGENTS.md 是否能回答：
  - AI 任务开始前应该先读什么？
  - 这个项目的目录、模块和命令边界是什么？
  - 改完以后如何验证和汇报？

### rules/global.md

基于 `assets/pm-harness-template/rules/global.md` 的模块化框架生成，作为 AGENTS.md 之后的全局 guard 规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、执行前提、任务分级、禁止行为、OpenSpec 准入、状态源、验证准出、输出要求和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{MODULES}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{DEPLOYMENT_STACK}`、`{PRIMARY_VERIFY_COMMAND}`、`{TASK_TRACKING_SYSTEM}`。
- 根据实际目录和能力生成「模块归属与上下文路由」，不要保留不存在的模块入口。
- 如项目没有前端、算法、对象存储、模型文件、私有化部署等能力，应删除或简化对应 `[条件启用]` 路由与验证项。
- 从实际脚本生成统一验证命令；命令未知时写 `待确认`，不得编造。
- 保持 global.md 与 AGENTS.md、rules/directory-structure.md、project.yaml 的模块和技术栈描述一致。

### rules/api.md

基于 `assets/pm-harness-template/rules/api.md` 的模块化框架生成，作为接口设计、接口调用和接口变更的强制规则。

生成要求：
- 保留所有 `[通用]` 模块，包括 API 设计原则、路径规范、请求规范、响应结构、错误码、兼容性、变更流程、测试要求和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{API_PREFIX}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{API_DOC_PATH}`、`{OPENAPI_SOURCE}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如鉴权、OpenAPI 客户端生成、前端 API 调用、文件上传、异步任务、Webhook、外部服务、SDK。
- 如前端技术栈支持 OpenAPI 客户端生成，生成 `{API_CLIENT_GENERATOR}`、`{API_CLIENT_GENERATE_COMMAND}`、`{API_GENERATED_DIR}`；否则删除客户端生成的硬性命令，保留契约同步要求。
- 根据业务领域生成 `{API_RESOURCE_EXAMPLES}`，不得保留模板中的具体业务资源。
- API 前缀未知时默认 `/api/v1`，但需在项目初始化输出中提示可确认。
- 保持 api.md 与 `docs/03-api-index.md`、`docs/standards/openapi-rules.md`、`docs/standards/api-governance.md`、前端生成配置和后端框架描述一致。

### rules/language.md

基于 `assets/pm-harness-template/rules/language.md` 的模块化框架生成，作为语言、命名和术语治理规则。

生成要求：
- 保留所有 `[通用]` 模块，包括总体语言策略、AI 输出语言、文档语言、代码标识符、测试命名、Git 命名、OpenSpec 命名、禁止事项和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRIMARY_LANGUAGE}`、`{CODE_IDENTIFIER_LANGUAGE}`、`{API_FIELD_CASE}`、`{DATABASE_FIELD_CASE}`、`{BACKEND_LANGUAGE}`、`{DOMAIN_TERMS}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如前端命名、移动端命名、国际化、多语言文档。
- 根据 BACKEND_STACK 和 FRONTEND_STACK 生成对应生态的命名规范，不得只保留 Python/React 示例。
- 根据 DB_PRIMARY 和 API 约定生成数据库字段、API 字段命名风格；未知时默认数据库 `snake_case`，API 字段标记 `待确认`。
- 根据产品名称、产品定位、业务领域生成初始术语表；不确定的术语必须标记 `待确认`。
- 所有文档时间记录必须统一为 `YYYY-MM-DD hh:mm:ss`；仅文件名、目录名和归档分组可使用 `YYYY-MM-DD` 或 `YYYY-MM`。
- 保持 language.md 与 api.md、database.md、coding.md、directory-structure.md 中的命名约定一致。

### rules/coding.md

基于 `assets/pm-harness-template/rules/coding.md` 的模块化框架生成，作为架构分层、模块边界和代码质量规则。

生成要求：
- 保留所有 `[通用]` 模块，包括总体编码原则、架构分层、模块边界、代码风格、错误处理、依赖管理、AI 修改代码规则和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{BACKEND_STACK}`、`{BACKEND_MODULE_STRUCTURE}`、`{FORMAT_COMMAND}`、`{LINT_COMMAND}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如后端、前端、移动端/微信小程序、数据库、对象存储、算法/模型、异步任务、共享类型与代码生成。
- 根据 BACKEND_STACK 生成后端分层和模块结构；非 Python/FastAPI 项目不得保留 Python 专属硬性要求。
- 根据 FRONTEND_STACK 生成前端组件、状态、服务和生成客户端规则；无前端时删除前端章节。
- 根据 FORMS 生成移动端、微信小程序或桌面端规则；未启用的端不得保留强制规则。
- 根据 DB_PRIMARY、对象存储、算法和异步任务配置，生成对应代码边界和 adapter/client/service 规则。
- 从实际脚本生成 `{FORMAT_COMMAND}`、`{LINT_COMMAND}`、`{TYPECHECK_COMMAND}`；未知时写 `待确认`，不得编造。
- 保持 coding.md 与 language.md、api.md、database.md、testing.md、directory-structure.md 的命名、目录和质量门禁一致。

### rules/compatibility.md

基于 `assets/pm-harness-template/rules/compatibility.md` 的模块化框架生成，作为端、平台、数据库、部署和第三方服务兼容性规则。

生成要求：
- 保留所有 `[通用]` 模块，包括总体兼容原则、API 与协议兼容、兼容性测试要求、AI 修改规则和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_FORMS}`、`{RUNTIME_VERSION_MATRIX}`、`{OS_SUPPORT_MATRIX}`、`{DEPLOYMENT_MODES}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如 Web 浏览器、移动端/微信小程序、数据库、对象存储、CPU 架构、信创、第三方服务、算法服务、Webhook。
- 根据 FORMS 生成产品形态兼容范围；未启用的端不得保留强制兼容要求。
- 根据 FRONTEND_STACK 生成 `{BROWSER_SUPPORT_MATRIX}`；无 Web 前端时删除 Web 浏览器兼容章节。
- 根据 DB_PRIMARY 和信创数据库生成 `{DATABASE_SUPPORT_MATRIX}`；单数据库项目应明确只支持该数据库。
- 根据对象存储配置生成 `{OBJECT_STORAGE_SUPPORT_MATRIX}`；没有文件/媒体/模型需求时可简化对象存储章节。
- 根据 DEPLOYMENT_STACK、信创 OS、CPU 架构要求生成部署、OS、CPU 和信创兼容规则。
- 未知版本、平台或厂商支持范围标记为 `待确认`，不得编造。
- 保持 compatibility.md 与 api.md、database.md、environment.md、object-storage.md、port-management.md、directory-structure.md 一致。

### rules/data-management.md

基于 `assets/pm-harness-template/rules/data-management.md` 的模块化框架生成，作为数据目录、数据资产、提交边界和脱敏规则。

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

基于 `assets/pm-harness-template/rules/database.md` 的模块化框架生成，作为数据库选型、Schema、迁移、Repository 和查询规则。

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

基于 `assets/pm-harness-template/rules/directory-structure.md` 的模块化框架生成，作为目录边界、文件归属、生成代码边界、文档归属、新增目录流程和目录同步规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、顶层目录职责、AI 工具目录、rules/docs/issues/iterations/openspec/compatibility/scripts/deploy/data/models/src/tests 目录边界、生成代码目录、文件归属决策表、禁止事项、新增目录流程和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{DEPLOYMENT_STACK}`、`{ENABLED_AGENT_TOOLS}`、`{PRIMARY_AGENT_TOOL}`、`{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{ITERATION_PATTERN}`、`{CHANGE_ID_PATTERN}`、`{DOCS_STRUCTURE}`、`{GENERATED_CODE_DIRS}`、`{HAS_WEB}`、`{HAS_WECHAT_MINIAPP}`、`{HAS_MOBILE}`、`{HAS_DESKTOP}`、`{HAS_ALGORITHM}`、`{HAS_OBJECT_STORAGE}`、`{HAS_MEDIA}`。
- 根据项目能力保留或删除 `[条件启用]` 模块，例如 Web、微信小程序、Android、iOS、桌面端、H5、算法、对象存储、媒体、模型文件、Kubernetes、Helm、私有化部署、AI 工具目录。
- 根据 PRODUCT_FORMS、HAS_WEB、HAS_WECHAT_MINIAPP、HAS_MOBILE、HAS_DESKTOP 生成 `src/` 子目录和 `compatibility/devices/` 文档；未启用的端不得保留强制目录要求。
- 根据 BACKEND_STACK 生成 `src/backend/` 入口文件、依赖文件、分层目录；非 Python/FastAPI 项目不得保留 Python 专属硬性描述。
- 根据 FRONTEND_STACK 生成 `src/web/` 结构和生成代码目录；无 Web 前端时删除 Web 前端强制规则。
- 根据 DATABASE_STACK 和兼容性要求生成数据库迁移、schema、compatibility/database 目录描述；无数据库时简化数据库相关描述。
- 根据 REQ_ROOT_DIR、BUG_ROOT_DIR、ITERATION_PATTERN、CHANGE_ID_PATTERN 生成 issues、iterations、openspec 的目录归属；必须与 issues-lifecycle.md、requirement-management.md、bug-management.md、document-governance.md 一致。
- 根据 DOCS_STRUCTURE 生成 docs 分层；未知时默认使用主文档、standards、guides、knowledge-base、README 分层。
- 根据 GENERATED_CODE_DIRS 生成生成代码目录边界；未知时标记 `待确认`，不得编造生成工具。
- 根据 HAS_ALGORITHM 决定是否生成 `src/algorithm/` 和根 `models/` 目录规则；没有算法/模型需求时 `models/` 只保留占位说明或删除强制规则。
- 根据 HAS_OBJECT_STORAGE、HAS_MEDIA 生成 object-storage、media、data、tests fixtures 和 compatibility 相关目录规则；未启用能力删除强制要求。
- 根据 DEPLOYMENT_STACK 生成 `deploy/` 子目录规则；未启用 Kubernetes 时不得生成强制 `k8s/` 规则。
- 根据 ENABLED_AGENT_TOOLS 保留 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/`；未启用工具不得保留强制规则。
- 保持 directory-structure.md 与 AGENTS.md、README.md、project.yaml、global.md、document-governance.md、issues-lifecycle.md、requirement-management.md、bug-management.md、coding.md、testing.md、data-management.md、database.md 一致。

### rules/document-governance.md

基于 `assets/pm-harness-template/rules/document-governance.md` 的模块化框架生成，作为 docs、issues、requirements、bugs、iterations、openspec、compatibility、rules 的文档生命周期、研发追溯、同步和归档规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、研发文档链路、docs 分层、文档分类、Markdown 元数据、docs 更新触发矩阵、issues/iterations/openspec 治理、自动同步矩阵、命名规范、质量要求、AI 执行顺序、轻量修订、评审确认、归档策略、禁止事项和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{DEPLOYMENT_STACK}`、`{PROJECT_GOVERNANCE_LEVEL}`、`{DOCS_STRUCTURE}`、`{ISSUE_WORKFLOW}`、`{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{ITERATION_PATTERN}`、`{SPRINT_FACT_SOURCE}`、`{CHANGE_ID_PATTERN}`、`{TASK_TRACKING_SYSTEM}`、`{DOC_REVIEW_POLICY}`、`{ARCHIVE_POLICY}`。
- 根据 PROJECT_GOVERNANCE_LEVEL 生成研发文档链路；未知时默认使用 `issues -> iterations -> openspec/changes -> src/tests -> docs/compatibility/rules -> openspec/specs -> openspec/archive`。
- 根据 DOCS_STRUCTURE 生成 docs 分层；未知时默认使用主文档、standards、guides、knowledge-base、README 分层。
- 根据 REQ_ROOT_DIR、BUG_ROOT_DIR、ISSUE_WORKFLOW 与 issues-lifecycle.md、requirement-management.md、bug-management.md 生成 issues 治理；不得把需求、Bug、迭代放入 docs 根目录。
- 根据 ITERATION_PATTERN 与 SPRINT_FACT_SOURCE 生成迭代目录、四件套和事实源规则；未知时默认 `iterations/sprint-xxx/` 与 `sprint.yaml`。
- 根据是否启用 OpenSpec 生成 changes/specs/archive 章节；未启用时替换为项目等价变更系统，不得保留不可执行的 OpenSpec 强制要求。
- 根据 PRODUCT_FORMS 保留或删除 Web、微信小程序、移动端、桌面端、H5 相关 docs 和兼容性同步规则。
- 根据 BACKEND_STACK、FRONTEND_STACK、DATABASE_STACK、DEPLOYMENT_STACK、对象存储和算法能力生成自动同步矩阵；未启用能力不得保留强制同步要求。
- 根据 TASK_TRACKING_SYSTEM 保留 Jira、Linear、飞书、多维表格、GitHub Issues 或本地 backlog 章节；未启用时删除或标记为 `未启用`。
- 根据 DOC_REVIEW_POLICY 与 ARCHIVE_POLICY 生成人工确认和归档策略；未知时标记 `待确认`。
- 所有文档中的发生时间、创建时间、更新时间、评审时间、验证时间、发布时间、归档时间必须生成到秒级，格式为 `YYYY-MM-DD hh:mm:ss`；无法确认时写 `待确认`。
- 保持 document-governance.md 与 AGENTS.md、global.md、directory-structure.md、issues-lifecycle.md、requirement-management.md、bug-management.md、api.md、database.md、testing.md、release.md、README.md 一致。

### rules/issues-lifecycle.md

基于 `assets/pm-harness-template/rules/issues-lifecycle.md` 的模块化框架生成，作为需求与 BUG 共用的 plan、review、archive 三阶段物理目录生命周期规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、总原则、目录结构、阶段准入、迁移时机、trace 字段、registry 规则、与需求/BUG/Sprint/OpenSpec 的关系、自动化要求、初始化生成建议和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{REQ_ID_PATTERN}`、`{BUG_ID_PATTERN}`、`{REQ_REGISTRY_FILE}`、`{BUG_REGISTRY_FILE}`、`{ISSUE_LIFECYCLE_STAGES}`、`{REQ_STATUS_TO_STAGE}`、`{BUG_STATUS_TO_STAGE}`、`{ISSUE_REVIEW_POLICY}`、`{ISSUE_ARCHIVE_POLICY}`、`{ISSUE_PATH_COMPAT_POLICY}`、`{WORKFLOW_SYNC_COMMAND}`、`{TASK_TRACKING_SYSTEM}`。
- 默认生成 `plan`、`review`、`archive` 三阶段；如用户明确改名，必须同步 directory-structure、document-governance、requirement-management、bug-management、AGENTS、命令说明和校验脚本。
- 默认要求新建 REQ/BUG 落入 `plan/`，评审通过后进入 `review/`，拒绝/延期/不修/关闭或归档后进入 `archive/`。
- 根据是否启用 OpenSpec、Sprint、外部看板、遗留扁平路径和自动化同步脚本保留或删除 `[条件启用]` 模块；未启用能力不得保留不可执行的强制命令。
- `trace.md` 字段必须至少能表达 `status` 与 `lifecycle_stage`；如启用 `current_path`、外部看板字段或 owner 字段，必须说明同步策略。
- `_registry.yaml` 必须保留在 `issues/requirements/` 与 `issues/bugs/` 根目录；不得生成到阶段目录内。
- 保持 issues-lifecycle.md 与 AGENTS.md、directory-structure.md、document-governance.md、requirement-management.md、bug-management.md、sprint 命令、capture/review/opsx 命令和 sync-workflow-status.py 一致。

### rules/requirement-management.md

基于 `assets/pm-harness-template/rules/requirement-management.md` 的模块化框架生成，作为需求捕获、澄清、目录结构、状态机、命令阶段、评审门禁、Readiness、原型、验收标准、OpenSpec 转换、迭代流转、变更控制和 AI 处理边界规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、需求治理总原则、目录结构、状态机、需求类型与优先级、捕获与澄清、需求包六件套、验收标准、Readiness 门禁、评审门禁、trace 最小字段、变更控制、AI 处理规则、同步关系、初始化生成建议和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{REQ_ROOT_DIR}`、`{REQ_ID_PATTERN}`、`{REQ_REGISTRY_FILE}`、`{REQ_STATUS_MACHINE}`、`{REQ_PRIORITY_LEVELS}`、`{REQ_TYPE_TAXONOMY}`、`{REQ_REVIEW_POLICY}`、`{REQ_READINESS_POLICY}`、`{REQ_SPRINT_POLICY}`、`{REQ_TO_CHANGE_POLICY}`、`{REQ_PROTOTYPE_POLICY}`、`{REQ_ACCEPTANCE_POLICY}`、`{REQ_TRACE_POLICY}`、`{REQ_CHANGE_CONTROL_POLICY}`、`{TASK_TRACKING_SYSTEM}`。
- 根据 ISSUE_WORKFLOW、ITERATION_PATTERN、CHANGE_ID_PATTERN、TASK_TRACKING_SYSTEM 生成需求目录、状态流转、进入迭代和转研发变更规则；未知时标记 `待确认`。
- 保留默认综合捕获命令 `/capture` 和需求命令族 `/req-capture`、`/req-explore`、`/req-generate`、`/req-complete`、`/req-review`、`/req-opsx`，并确保已启用 Agent 工具目录语义一致。
- 根据团队产品治理策略生成 REQ_TYPE_TAXONOMY、REQ_PRIORITY_LEVELS、REQ_REVIEW_POLICY 和 REQ_READINESS_POLICY；未知时保留模板默认值并标记需要人工确认。
- 根据是否启用 OpenSpec、Sprint、外部看板、CI/CD、发布流程生成 REQ_TO_CHANGE_POLICY、REQ_SPRINT_POLICY 和 trace 规则；未启用能力删除对应强制章节。
- 需求 `trace.md` 必须包含「关联缺陷」章节，字段为 `BUG`、`严重等级`、`状态`、`关联 Change`、`说明`；该章节只保存索引级关联，不重复 BUG 全文、复现步骤、根因分析、日志、截图或回归记录。
- 根据 HAS_WEB、HAS_WECHAT_MINIAPP、HAS_MOBILE、HAS_DESKTOP、UI_STACK 生成原型目录与设计评审规则；无 UI 或原型流程时删除或标记为“不适用”。
- 根据 api、database、security、media、object-storage、compatibility、ui-design、testing 能力生成验收标准同步矩阵；未启用能力不得保留强制验收项。
- 根据是否存在客户需求、合规需求或外部看板生成客户/合规/外部看板章节；未启用时删除或标记为“不适用”。
- 保持 requirement-management.md 与 issues-lifecycle.md、document-governance.md、directory-structure.md、testing.md、bug-management.md、release.md、api.md、database.md、security.md、ui-design.md 一致。

### rules/bug-management.md

基于 `assets/pm-harness-template/rules/bug-management.md` 的模块化框架生成，作为 Bug 捕获、分级、复现、根因分析、状态机、目录结构、评审门禁、OpenSpec 转换、回归测试、知识沉淀和 AI 处理边界规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、缺陷治理总原则、目录结构、状态机、严重等级与优先级、捕获与复现、根因分析、评审门禁、迭代与修复流转、验收与回归测试、AI 处理规则、同步关系、初始化生成建议和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{BUG_ROOT_DIR}`、`{BUG_ID_PATTERN}`、`{BUG_REGISTRY_FILE}`、`{BUG_STATUS_MACHINE}`、`{BUG_SEVERITY_LEVELS}`、`{BUG_PRIORITY_LEVELS}`、`{BUG_REVIEW_POLICY}`、`{BUG_SPRINT_POLICY}`、`{BUG_TO_CHANGE_POLICY}`、`{BUG_EVIDENCE_POLICY}`、`{BUG_TEST_POLICY}`、`{BUG_KB_POLICY}`、`{BUG_SLA_POLICY}`。
- 根据 ISSUE_WORKFLOW、ITERATION_PATTERN、CHANGE_ID_PATTERN、TASK_TRACKING_SYSTEM 生成 Bug 目录、状态流转、进入迭代和转修复变更规则；未知时标记 `待确认`。
- 保留默认综合捕获命令 `/capture` 和缺陷命令族 `/bug-capture`、`/bug-explore`、`/bug-generate`、`/bug-complete`、`/bug-review`、`/bug-opsx`，并确保已启用 Agent 工具目录语义一致。
- 根据团队质量策略生成 BUG_SEVERITY_LEVELS、BUG_PRIORITY_LEVELS 和 BUG_REVIEW_POLICY；未知时保留模板默认等级并标记需要人工确认。
- 根据是否启用 OpenSpec、Sprint、外部看板、CI/CD、发布流程生成 BUG_TO_CHANGE_POLICY、BUG_SPRINT_POLICY 和 trace 规则；未启用能力删除对应强制章节。
- Bug 关联需求时，必须反向更新对应需求 `trace.md` 的「关联缺陷」索引；不得把 BUG 全文复制到需求文档。
- 根据 security、database、media、object-storage、compatibility、ui-design、testing 能力保留或删除安全缺陷、数据缺陷、上传/媒体缺陷、兼容缺陷、UI 缺陷和回归测试同步规则。
- 根据是否存在线上 SLA、值班、客户工单或事故响应生成 BUG_SLA_POLICY；未启用时删除或标记为“不适用”。
- 保持 bug-management.md 与 issues-lifecycle.md、document-governance.md、directory-structure.md、testing.md、security.md、release.md、api.md、database.md、media.md、object-storage.md、compatibility.md、ui-design.md 一致。

### rules/environment.md

基于 `assets/pm-harness-template/rules/environment.md` 的模块化框架生成，作为 .env.example、运行环境、密钥边界、服务配置和部署环境同步规则。

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

基于 `assets/pm-harness-template/rules/media.md` 的模块化框架生成，作为图片、音频、视频、文档、导入导出、转码产物、对象存储和上传安全规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、媒体能力总览、存储原则、上传入口、安全规则、访问控制、本地开发与测试数据边界、环境变量、AI 更新规则、禁止事项和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{MEDIA_ENABLED}`、`{MEDIA_TYPES}`、`{OBJECT_STORAGE_STACK}`、`{MEDIA_BUCKET_POLICY}`、`{MEDIA_KEY_PATTERN}`、`{MAX_UPLOAD_POLICY}`、`{MEDIA_PROCESSING_PIPELINE}`、`{FRONTEND_MEDIA_STACK}`。
- 根据 MEDIA_ENABLED 决定是否生成完整媒体规范；未启用媒体/文件上传能力时，仅保留占位说明、安全边界和禁止事项。
- 根据 MEDIA_TYPES 保留或删除图片、音频、视频、文档、导入导出、处理产物章节；未启用类型不得保留强制格式、变量、API、测试要求。
- 根据 OBJECT_STORAGE_STACK 生成对象存储、Bucket、对象 Key、签名 URL 和访问控制规则；无对象存储时改为文件系统策略。
- 根据 FORMS 生成 Web、微信小程序、移动端、桌面端的上传、预览、播放、录音录像限制。
- 根据 MEDIA_PROCESSING_PIPELINE 生成缩略图、封面、转码、ASR、OCR、异步任务和处理状态规则；无处理流程时删除强制处理要求。
- 根据 MAX_UPLOAD_POLICY 生成大小、格式、MIME、文件头、时长、分辨率限制；未知时标记 `待确认`，不得编造生产限制。
- 根据 FRONTEND_MEDIA_STACK 生成前端上传组件、播放器、录音、波形、预览能力；无前端时删除前端媒体章节。
- 保持 media.md 与 object-storage.md、data-management.md、environment.md、api.md、database.md、security.md、testing.md、docs/06-video-asset-management.md 一致。

### rules/object-storage.md

基于 `assets/pm-harness-template/rules/object-storage.md` 的模块化框架生成，作为对象存储启用条件、供应商适配、Bucket、对象 Key、权限、签名 URL、生命周期和兼容性规则。

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

基于 `assets/pm-harness-template/rules/port-management.md` 的模块化框架生成，作为开发端口、Docker 端口、宿主机映射、冲突处理和服务拓扑端口规则。

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

基于 `assets/pm-harness-template/rules/release.md` 的模块化框架生成，作为版本发布、准入检查、构建打包、部署验证、发布说明、回滚和归档规则。

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

基于 `assets/pm-harness-template/rules/security.md` 的模块化框架生成，作为敏感信息、认证授权、输入校验、上传与对象存储、外部服务、日志脱敏、部署安全、License、Guard 和 AI 安全边界规则。

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

基于 `assets/pm-harness-template/rules/testing.md` 的模块化框架生成，作为测试分层、覆盖率目标、TDD、Mock、Fixture、接口测试、前端测试、E2E、外部服务、数据隔离、运行命令和 AI 测试行为规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、测试总原则、测试用例结构、必须覆盖场景、TDD 与需求追踪、AI 修改测试规则、同步关系、初始化生成建议和检查清单。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{TEST_STRATEGY}`、`{BACKEND_TEST_STACK}`、`{FRONTEND_TEST_STACK}`、`{MOBILE_TEST_STACK}`、`{E2E_TEST_STACK}`、`{COVERAGE_TARGET}`、`{COVERAGE_BY_LAYER}`、`{TEST_COMMANDS}`、`{CI_TEST_COMMAND}`、`{UNIT_TEST_COMMAND}`、`{INTEGRATION_TEST_COMMAND}`、`{COVERAGE_COMMAND}`、`{FRONTEND_CHECK_COMMAND}`、`{E2E_TEST_COMMAND}`、`{TEST_DATABASE_STRATEGY}`、`{FIXTURE_STRATEGY}`、`{MOCK_STRATEGY}`、`{API_TEST_STRATEGY}`、`{SECURITY_TEST_STRATEGY}`、`{PERFORMANCE_TEST_STRATEGY}`。
- 根据 BACKEND_STACK、FRONTEND_STACK、MOBILE_STACK、HAS_WEB、HAS_WECHAT_MINIAPP、HAS_DESKTOP、HAS_SDK、HAS_ALGORITHM 生成测试分层和测试栈；未启用端或模块不得保留强制测试要求。
- 根据实际 `package.json`、Makefile、脚本目录、CI 配置和测试框架生成 TEST_COMMANDS；命令未知时标记 `待确认`，不得编造。
- 根据 DB_PRIMARY、DATABASE_STACK、COMPATIBILITY_TARGETS 生成测试数据库、事务回滚、迁移测试、多数据库兼容测试规则；无数据库时删除对应强制章节。
- 根据 API_PREFIX、OPENAPI_SOURCE、HAS_WEBHOOK、HAS_SDK 生成 API 与契约测试规则；无 API 时删除对应强制章节。
- 根据 HAS_UPLOAD、HAS_MEDIA、OBJECT_STORAGE_STACK、DATA_MANAGEMENT_SCOPE 生成上传、媒体、下载、预览和对象存储测试规则；未启用能力删除对应章节。
- 根据 AUTH_STRATEGY、PERMISSION_MODEL、SENSITIVE_DATA_TYPES 生成安全测试规则；权限、安全或敏感数据策略未知时标记 `待确认`。
- 根据 DEPLOYMENT_STACK、RELEASE_CHANNELS、CI_PROVIDER 生成 CI、发布门禁、E2E、性能和稳定性测试规则；未启用 CI/CD 时标记为“本地手动执行”或 `待确认`。
- 保持 testing.md 与 global.md、coding.md、api.md、database.md、data-management.md、security.md、media.md、object-storage.md、compatibility.md、release.md 一致。

### rules/ui-design.md

基于 `assets/pm-harness-template/rules/ui-design.md` 的模块化框架生成，作为产品设计定位、Design Token、组件体系、页面结构、交互状态、响应式、可访问性、内容呈现、视觉验收和 AI UI 修改边界规则。

生成要求：
- 保留所有 `[通用]` 模块，包括规则定位、文档模块分类、设计定位、UI 技术栈、色彩系统、字体/间距/布局密度、组件使用优先级、核心组件规范、页面结构、交互反馈、可访问性、视觉验收、AI UI 修改规则、同步关系、初始化生成建议和检查清单。
- 用第 16 步 UI 设计输入的结果替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_POSITIONING}`、`{TARGET_USERS}`、`{SUPPORTED_CLIENTS}`、`{UI_STACK}`、`{FRONTEND_FRAMEWORK}`、`{STYLE_SYSTEM}`、`{COMPONENT_LIBRARY}`、`{ICON_LIBRARY}`、`{STATE_MANAGEMENT}`、`{FORM_STACK}`、`{CHART_STACK}`、`{MOTION_STACK}`、`{DESIGN_STYLE}`、`{DESIGN_PRINCIPLES}`、`{DESIGN_TOKEN_SOURCE}`、`{TOKEN_SYNC_COMMAND}`、`{ROUTE_LAYOUTS}`、`{CORE_PAGES}`、`{CORE_COMPONENTS}`、`{RESPONSIVE_POLICY}`、`{ACCESSIBILITY_TARGET}`、`{I18N_POLICY}`、`{THEMING_POLICY}`、`{UI_VERIFY_COMMANDS}`、`{VISUAL_ACCEPTANCE_SOURCE}`。
- `UI_DESIGN_INPUT_MODE=上传` 时，必须将上传的 `ui-design.md` 作为 UI 设计的唯一事实源，严格提取并遵循其设计定位、支持端、设计风格、Design Token、组件库、图标库、页面结构、核心页面、核心组件、响应式、可访问性、主题/国际化、视觉验收来源和 UI 验证命令。文档未覆盖内容仅标记为 `待确认` 或 `不适用`，不得自行重设计。
- `UI_DESIGN_INPUT_MODE=手工输入` 时，必须基于 `UI_STYLE_BRIEF`、产品描述、核心能力、产品形态与前端技术栈，自动生成完整一致的 UI 设计方案，并填充上述个性化变量；不得额外要求用户提供 `ui-design.md`。
- `ui-design.md` 的解析结果必须同步写入或影响：`rules/ui-design.md`、`AGENTS.md` 中 UI 相关路径与验收策略、`README.md` 技术栈/核心能力说明、`project.yaml` 的 frontend/ui/design_system 字段、`docs/00-product-overview.md` 的产品形态与核心场景、`docs/01-architecture.md` 的前端/UI 模块、`docs/05-compatibility-matrix.md` 的端与浏览器矩阵、`docs/standards/frontend-test-standard.md` 的前端测试策略、`docs/standards/test-coverage.md` 的前端覆盖率目标、`DOCUMENT_METADATA_INDEX.md` 的来源登记。
- 上传 `ui-design.md` 与既有产品输入发生冲突时，必须暂停生成并要求用户明确裁决；不得以任一来源覆盖另一来源，也不得静默降级为 `待确认` 后继续生成。
- 根据 FRONTEND_STACK、HAS_WEB、HAS_WECHAT_MINIAPP、HAS_MOBILE、HAS_DESKTOP、SUPPORTED_CLIENTS 生成 UI 适用范围；无 UI 项目应删除强制前端规范或标记为“不适用”。
- 根据 UI_STACK、COMPONENT_LIBRARY、ICON_LIBRARY、STYLE_SYSTEM 生成组件复用优先级和技术栈表；不得保留 React/Tailwind/shadcn 等未启用技术的强制规则。
- 手工输入模式下，根据 DESIGN_STYLE、PRODUCT_POSITIONING、TARGET_USERS 生成设计定位、色彩、字体、间距、布局密度和交互原则；上传模式下严格使用 `ui-design.md` 中的对应规范。不得保留来源项目品牌名、颜色、页面名、业务模块或客户名，除非它们就是用户上传文档中明确要求保留的内容。
- 根据 DESIGN_TOKEN_SOURCE 和 TOKEN_SYNC_COMMAND 生成 Design Token 章节；未建立 Token 系统时标记 `待完善`，并保留最小颜色/字体/间距/圆角约束。
- 根据 CORE_PAGES、ROUTE_LAYOUTS、CORE_COMPONENTS 生成页面结构和核心组件规范；未启用页面类型不得保留强制实现要求。
- 根据 HAS_MEDIA、HAS_UPLOAD、HAS_CHARTS、HAS_3D、HAS_MAP、OBJECT_STORAGE_STACK 生成媒体、图片和可视化章节；未启用能力删除对应章节。
- 根据 RESPONSIVE_POLICY、ACCESSIBILITY_TARGET、I18N_POLICY、THEMING_POLICY 生成响应式、可访问性、国际化、主题和白标规则；未知时标记 `待确认`。
- 根据 package.json、脚本目录、测试配置、设计稿或原型来源生成 UI_VERIFY_COMMANDS 和 VISUAL_ACCEPTANCE_SOURCE；命令未知时标记 `待确认`，不得编造。
- 不得把用户提供的 `ui-design.md` 原文整段复制到 `rules/ui-design.md`；必须抽象为 Harness 规则结构，并区分 `[通用]`、`[个性化]`、`[条件启用]`。
- 保持 ui-design.md 与 directory-structure.md、coding.md、api.md、language.md、media.md、object-storage.md、security.md、testing.md、compatibility.md、environment.md、release.md 一致。

### README.md

基于 `assets/pm-harness-template/README.md` 的模块化框架生成，作为工程根入口，覆盖产品简介、用户角色、核心能力、技术栈、快速启动、部署入口、目录导航、AI 约束、文档索引和初始化建议。

生成要求：
- 保留所有 `[通用]` 模块，包括文档定位、AI 协作约束、文档导航、项目治理命令、初始化建议和更新触发条件。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_DESCRIPTION}`、`{BUSINESS_DOMAIN}`、`{TARGET_USERS}`、`{PRODUCT_FORMS}`、`{CORE_CAPABILITIES}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{ASYNC_TASK_STACK}`、`{ALGORITHM_STACK}`、`{DEPLOYMENT_STACK}`、`{LOCAL_SETUP_COMMANDS}`、`{DEV_COMMANDS}`、`{TEST_COMMANDS}`、`{DOCKER_UP_COMMAND}`、`{DOCKER_DOWN_COMMAND}`、`{SERVICE_URLS}`、`{DIRECTORY_VALIDATE_COMMAND}`、`{PRIMARY_VERIFY_COMMAND}`、`{PROJECT_OWNER}`。
- 根据 PRODUCT_FORMS、BACKEND_STACK、FRONTEND_STACK、DATABASE_STACK、OBJECT_STORAGE_STACK、ASYNC_TASK_STACK、ALGORITHM_STACK、DEPLOYMENT_STACK 生成技术栈表、快速启动、目录说明和部署入口；未启用能力不得保留强制说明。
- 根据用户角色和核心能力生成用户角色表与核心能力表；无多角色项目可合并为单一“用户/操作者/系统调用方”。
- 根据实际脚本、包管理器、Makefile、Docker Compose、CI 或项目文档生成启动、开发、测试、验证、部署和目录校验命令；未知时标记 `待确认`，不得编造。
- 服务名、端口、URL、环境变量和默认账号策略必须来自真实配置或用户输入；不得在 README 中写入真实密码、Token、Access Key 或生产凭据。
- 根据是否启用 Docker、Kubernetes、对象存储、媒体、算法/模型、移动端、微信小程序、桌面端、OpenSpec、Sprint 治理保留或删除 `[条件启用]` 内容。
- 保留默认自定义命令族说明：`/capture`、`/req-*`、`/bug-*`、`/sprint-*`、`/initialize-project`、`/build-design-system`、`/build-api-standard`、`/build-test-framework`、`/opsx-*`；不得改变默认命令的阶段、输入、输出和是否生成代码边界。
- 不得保留来源项目产品名、用户角色、业务能力、技术栈、端口、服务地址、默认账号密码、bucket、表名、路径或测试示例。
- 保持 README 与 `AGENTS.md`、`project.yaml`、`docs/README.md`、`docs/00-product-overview.md`、`docs/01-architecture.md`、`docs/02-deployment.md`、`rules/directory-structure.md`、`rules/environment.md`、`rules/port-management.md`、`rules/document-governance.md` 一致。

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
  wechat_miniapp: {HAS_WECHAT_MINIAPP}
  android: {HAS_ANDROID}
  ios: {HAS_IOS}

algorithm:
  enabled: {HAS_ALGORITHM}
```

### docker-compose.yml

基于 `assets/pm-harness-template/docker-compose.yml` 的模块化框架生成，作为本地开发、演示部署和服务拓扑的 Compose 入口。

生成要求：
- 保留顶部注释元数据，包括 purpose、content、source、update_method、owner、note；不得给 YAML 文件插入 Markdown frontmatter。
- 用用户输入替换占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{DEPLOYMENT_OWNER}`、`{DEPLOYMENT_STACK}`、`{BACKEND_CONTAINER_PORT}`、`{HOST_PORT_BACKEND}`、`{WEB_DOCKERFILE}`、`{WEB_CONTAINER_PORT}`、`{HOST_PORT_WEB}`、`{DATABASE_IMAGE}`、`{DATABASE_NAME}`、`{DATABASE_USER}`、`{DATABASE_PASSWORD}`、`{DATABASE_CONTAINER_PORT}`、`{HOST_PORT_DATABASE}`、`{OBJECT_STORAGE_IMAGE}`、`{OBJECT_STORAGE_COMMAND}`、`{OBJECT_STORAGE_ACCESS_KEY}`、`{OBJECT_STORAGE_SECRET_KEY}`、`{OBJECT_STORAGE_API_PORT}`、`{HOST_PORT_OBJECT_STORAGE_API}`、`{OBJECT_STORAGE_CONSOLE_PORT}`、`{HOST_PORT_OBJECT_STORAGE_CONSOLE}`、`{WORKER_COMMAND}`、`{ALGORITHM_CONTAINER_PORT}`、`{HOST_PORT_ALGORITHM}`。
- 根据 BACKEND_STACK、FRONTEND_STACK、DATABASE_STACK、OBJECT_STORAGE_STACK、ASYNC_TASK_STACK、ALGORITHM_STACK 生成服务清单；未启用服务必须删除对应 service、profile、volume、端口和依赖。
- backend 服务为默认服务；web、database、object-storage、worker、algorithm 等必须按项目能力使用 profile 或直接删除。
- 根据实际 Dockerfile、源码目录和构建方式生成 build.context、dockerfile、image 和 command；未知时标记 `待确认` 或删除无法运行的服务，不得编造。
- 根据 `rules/port-management.md` 生成宿主机端口变量和容器内端口；默认采用“容器内固定，宿主机可变”的映射策略。
- 根据 `rules/environment.md` 和 `.env.example` 生成 env_file、environment 和变量名；不得在 compose 中写入真实密码、Token、Access Key 或生产凭据。
- 根据 `rules/data-management.md`、`rules/database.md`、`rules/object-storage.md` 生成 volume；未启用数据库或对象存储时删除对应 named volume。
- 根据服务真实健康检查能力生成 healthcheck；未知时使用 `待确认` 注释或删除健康检查，不得保留无意义命令。
- 对象存储初始化服务仅在 OBJECT_STORAGE_STACK 启用且存在明确 bucket/container 初始化需求时保留；不得保留来源项目 bucket、默认账号或供应商假设。
- 保持 `docker-compose.yml` 与 `.env.example`、`README.md`、`docs/02-deployment.md`、`docs/01-architecture.md`、`rules/environment.md`、`rules/port-management.md`、`rules/security.md`、`rules/object-storage.md` 一致。

### .env.example

- `APP_NAME` 改为 `{PRODUCT_CODE}`
- SQLite 数据库路径中的项目名替换
- MinIO bucket 默认值替换为 `{PRODUCT_CODE}`
- 如 DB_PRIMARY 非 SQLite，移除 SQLite 相关变量，增加对应数据库连接变量

### DOCUMENT_METADATA_INDEX.md

基于 `assets/pm-harness-template/DOCUMENT_METADATA_INDEX.md` 的模块化框架生成，作为文档资产、配置资产和脚本资产的元数据登记入口。

生成要求：
- 保留所有 `[通用]` 模块，包括文档定位、元数据字段规范、配置与脚本元数据规则、文档模块分类、规则文档清单、AI 修改规则、初始化生成建议和更新触发条件。
- 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{DOCS_OWNER}`、`{DOCUMENT_SOURCE_POLICY}`、`{DOCUMENT_REVIEW_POLICY}`、`{DOCUMENT_UPDATE_POLICY}`、`{ENABLED_DOC_MODULES}`、`{ENABLED_PRODUCT_FORMS}`、`{ENABLED_TECH_STACKS}`、`{ENABLED_GOVERNANCE_FLOWS}`、`{DOCUMENT_METADATA_SCHEMA_VERSION}`。
- 根据实际生成文件更新核心文档资产清单、专项标准文档清单、配置与脚本资产清单；不存在的文件不得登记为已存在资产，可标记为 `计划创建` 或删除。
- 根据 PRODUCT_FORMS、BACKEND_STACK、FRONTEND_STACK、DATABASE_STACK、OBJECT_STORAGE_STACK、MEDIA_ENABLED、API_ENABLED、AUTH_ENABLED、TESTING_ENABLED、DEPLOYMENT_STACK、OPENSPEC_ENABLED、ITERATION_ENABLED 保留或删除 `[条件启用]` 模块。
- 为每个 Markdown 文档生成或校验 frontmatter：`purpose`、`content`、`source`、`update_method`、`owner`、`note`。
- 文档元数据和正文表格中的时间记录必须使用 `YYYY-MM-DD hh:mm:ss`，例如 `created_at`、`updated_at`、`reviewed_at`、`verified_at`、`archived_at`、`published_at` 等；无法确认时写 `待确认`。
- 配置和脚本文件不得强制插入 YAML Frontmatter；应使用注释元数据或在本文档中登记，避免破坏语法。
- 删除来源项目历史版本编号、阶段说明和迁移记录；不得保留来源项目业务名、技术栈、服务名、端口、bucket、表名、路径或默认账号。
- 未确认的 owner、source、update_method、启用条件或脚本来源标记 `待确认`，不得编造。
- 保持 `DOCUMENT_METADATA_INDEX.md` 与 `README.md`、`AGENTS.md`、`project.yaml`、`docs/README.md`、`rules/document-governance.md`、`rules/directory-structure.md` 一致。

### rules/ 目录下所有文件

统一替换：
- 所有来源项目产品名 → `{PRODUCT_NAME}`
- 所有来源项目代码名 → `{PRODUCT_CODE}`
- `rules/database.md`：将核心表示例替换为通用占位表（`users`、`audit_logs` 等通用表保留，业务表替换为 `{PRODUCT_CODE}_items` 等占位）
- `rules/coding.md`：前端框架描述根据 FRONTEND_STACK 调整；后端描述根据 BACKEND_STACK 调整
- `rules/ui-design.md`：如前端非 React/Tailwind/shadcn，移除具体 Design System 章节，替换为通用 UI 规范占位
- `rules/directory-structure.md`：src 子目录列表根据 FORMS 和 HAS_ALGORITHM 调整

### docs/ 目录下文件

- 所有产品名、项目代码替换
- `README.md`：基于 `assets/pm-harness-template/docs/README.md` 的模块化框架生成，作为 `docs/` 目录总入口、主文档阅读顺序、专项治理文档、知识库和文档边界说明。
  - 保留所有 `[通用]` 模块，包括文档定位、文档分层、知识库、不属于 docs 根目录的内容、文档维护规则、AI Agent 使用规则、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{DOCS_OWNER}`、`{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_ENABLED}`、`{MEDIA_ENABLED}`、`{DEPLOYMENT_STACK}`、`{DOCUMENT_GOVERNANCE_POLICY}`。
  - 根据项目能力保留或删除 `[条件启用]` 文档条目，例如 API、OpenAPI、认证、文件上传、前端测试、数据库、视频/媒体、对象存储。
  - 文档清单必须与实际生成的 `docs/` 文件一致；不存在的文件不得作为已存在链接出现，可标记为 `计划创建`。
  - 不得保留来源项目产品名、业务说明、技术栈、数据库、bucket、端名称或旧路径假设；专项治理文档必须统一生成到 `docs/standards/`。
  - 明确 `issues/requirements/{plan,review,archive}/`、`issues/bugs/{plan,review,archive}/`、`iterations/`、`openspec/changes/` 与 `docs/` 的职责边界，禁止恢复旧式 `docs/prd/`、`docs/bugs/`、`docs/iterations/`。
  - 保持 `docs/README.md` 与 `rules/document-governance.md`、`DOCUMENT_METADATA_INDEX.md`、`AGENTS.md`、主 `README.md`、`docs/00-product-overview.md` 一致。
- `docs/standards/api-governance.md`：基于 `assets/pm-harness-template/docs/standards/api-governance.md` 的模块化框架生成，作为 API 设计原则、资源命名、URL/Method/版本、请求响应、错误码、认证授权、分页排序、幂等、OpenAPI、客户端生成、测试和维护规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、启用条件、设计原则、HTTP Method、分页排序过滤、AI 修改规则、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{API_OWNER}`、`{API_ENABLED}`、`{API_STYLE}`、`{API_PREFIX}`、`{API_VERSION_STRATEGY}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{RESPONSE_ENVELOPE}`、`{ERROR_CODE_DOC_PATH}`、`{AUTH_STRATEGY}`、`{PERMISSION_MODEL}`、`{OPENAPI_SOURCE}`、`{API_CLIENT_GENERATOR}`、`{API_CLIENT_GENERATE_COMMAND}`、`{API_VERIFY_COMMAND}`。
  - 当 API_ENABLED=false 且项目无 API/RPC/GraphQL/Webhook/SDK 时，只保留启用条件和未来启用说明，删除强制接口、OpenAPI、客户端生成和测试要求。
  - 根据 API_STYLE 保留或改写 REST、GraphQL、RPC、Webhook、SDK 章节；未启用风格不得出现在强制规范中。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如认证授权、文件上传、媒体接口、OpenAPI、客户端生成、Webhook、SDK、异步任务。
  - API 路径、资源名、分组、认证策略、响应结构、错误码文档、OpenAPI 来源和客户端生成命令必须来自用户输入或对应文档；不得保留来源项目资源名、路径、后端框架、客户端生成器、对象存储或认证方式。
  - 保持 `docs/standards/api-governance.md` 与 `rules/api.md`、`rules/security.md`、`rules/language.md`、`docs/03-api-index.md`、`docs/standards/openapi-rules.md`、`docs/standards/error-codes.md`、`docs/standards/authentication.md`、`docs/standards/file_upload.md`、`rules/testing.md` 一致。
- `docs/standards/openapi-rules.md`：基于 `assets/pm-harness-template/docs/standards/openapi-rules.md` 的模块化框架生成，作为 OpenAPI 契约来源、路由元数据、Schema、响应、错误码、安全声明、Tags、客户端生成、校验和兼容规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、启用条件、契约总原则、路由元数据、Tags 与分组、Schema 规范、响应与错误码、契约校验、兼容性与版本、测试验收、AI 修改规则、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{API_OWNER}`、`{OPENAPI_ENABLED}`、`{OPENAPI_VERSION}`、`{OPENAPI_SOURCE}`、`{OPENAPI_RUNTIME_URL}`、`{OPENAPI_OUTPUT_PATH}`、`{API_PREFIX}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{RESPONSE_ENVELOPE}`、`{AUTH_STRATEGY}`、`{ERROR_CODE_DOC_PATH}`、`{API_TAGS}`、`{API_CLIENT_GENERATOR}`、`{API_CLIENT_GENERATE_COMMAND}`、`{API_GENERATED_DIR}`、`{OPENAPI_VALIDATE_COMMAND}`。
  - 当 OPENAPI_ENABLED=false 且项目无 API 契约、客户端生成或接口文档需求时，只保留启用条件和未来启用说明，删除强制导出、生成和校验要求。
  - 根据 OPENAPI_SOURCE 生成运行时导出、静态 YAML/JSON、代码生成、API 网关或聚合契约规则；未启用来源不得出现在强制规范中。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如安全声明、客户端生成、Webhook、SDK、上传、异步任务、开放 API。
  - 契约来源、运行时地址、导出路径、API tags、客户端生成器、生成命令、生成目录和校验命令必须来自用户输入、实际脚本、框架配置或对应文档；未知时标记 `待确认`，不得编造。
  - 不得保留来源项目路径、资源名、后端框架注解、运行时地址、生成器、输出目录或命令。
  - 保持 `docs/standards/openapi-rules.md` 与 `rules/api.md`、`rules/security.md`、`rules/language.md`、`docs/03-api-index.md`、`docs/standards/api-governance.md`、`docs/standards/error-codes.md`、`docs/standards/authentication.md`、前端 API Client、SDK 和测试一致。
- `docs/standards/authentication.md`：基于 `assets/pm-harness-template/docs/standards/authentication.md` 的模块化框架生成，作为认证方式、登录登出、Token/Session、权限模型、受保护接口、前端登录态、错误码、安全测试和维护规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、启用条件、认证总原则、凭证传递、受保护接口与公开端点、错误码与响应、测试验收、AI 修改规则、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{SECURITY_OWNER}`、`{AUTH_ENABLED}`、`{AUTH_STRATEGY}`、`{AUTH_PROVIDER}`、`{AUTH_HEADER}`、`{TOKEN_TYPE}`、`{TOKEN_EXPIRE_POLICY}`、`{TOKEN_REFRESH_POLICY}`、`{TOKEN_STORAGE_POLICY}`、`{PASSWORD_POLICY}`、`{MFA_POLICY}`、`{PERMISSION_MODEL}`、`{ROLE_MATRIX}`、`{PUBLIC_ENDPOINTS}`、`{AUTH_ERROR_CODE_RANGE}`、`{AUTH_TEST_COMMAND}`。
  - 当 AUTH_ENABLED=false 且项目无登录态、用户身份、服务间凭证或访问控制需求时，只保留启用条件和未来启用说明，删除强制登录、Token、权限、前端守卫和测试要求。
  - 根据 AUTH_STRATEGY 保留或改写 Token、Session、OAuth2、OIDC、SSO、API Key、服务间认证章节；未启用策略不得出现在强制规范中。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如密码登录、MFA、前端登录态、服务间认证、Webhook、开放 API、SDK、管理端。
  - 登录接口、公开端点、角色矩阵、权限模型、Token 生命周期、前端登录态、错误码和测试命令必须来自用户输入或对应文档；不得保留来源项目角色、路径、函数名、前端目录、框架依赖或认证实现细节。
  - 保持 `docs/standards/authentication.md` 与 `rules/security.md`、`rules/api.md`、`docs/03-api-index.md`、`docs/standards/api-governance.md`、`docs/standards/error-codes.md`、`docs/standards/openapi-rules.md`、`rules/testing.md` 一致。
- `docs/standards/error-codes.md`：基于 `assets/pm-harness-template/docs/standards/error-codes.md` 的模块化框架生成，作为错误码分段、HTTP 映射、响应结构、登记流程、实现同步、前端处理、测试和维护规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、启用条件、设计原则、错误响应结构、HTTP 状态映射、命名与消息规范、新增与变更流程、测试验收、AI 修改规则、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{API_OWNER}`、`{ERROR_CODE_STYLE}`、`{SUCCESS_CODE}`、`{RESPONSE_ENVELOPE}`、`{ERROR_CODE_RANGES}`、`{AUTH_ERROR_CODE_RANGE}`、`{BUSINESS_ERROR_CODE_RANGE}`、`{PARAMETER_ERROR_CODE_RANGE}`、`{DEPENDENCY_ERROR_CODE_RANGE}`、`{ERROR_CODE_IMPL_PATH}`、`{EXCEPTION_IMPL_PATH}`、`{FRONTEND_ERROR_HANDLER_PATH}`、`{ERROR_CODE_TEST_COMMAND}`。
  - 根据 ERROR_CODE_STYLE 生成 numeric、string 或 mixed 风格；未启用风格不得混入强制规范。
  - 根据项目能力保留或删除 `[条件启用]` 错误码，例如认证授权、外部依赖、上传、对象存储、异步任务、支付、短信、LLM、Webhook、SDK。
  - 错误码分段、业务错误码、HTTP 映射、用户提示、开发说明、前端处理、实现路径和测试命令必须来自用户输入、需求、API 设计或对应文档；不得保留来源项目业务错误、依赖名称、实现路径或技术栈。
  - 未确认的业务错误码必须标记为 `待确认` 或 `reserved`，不得伪造已实现状态。
  - 保持 `docs/standards/error-codes.md` 与 `rules/api.md`、`rules/security.md`、`docs/03-api-index.md`、`docs/standards/api-governance.md`、`docs/standards/authentication.md`、`docs/standards/openapi-rules.md`、前端错误处理和测试一致。
- `docs/standards/file_upload.md`：基于 `assets/pm-harness-template/docs/standards/file_upload.md` 的模块化框架生成，作为文件上传入口、认证授权、格式大小限制、安全校验、对象存储、元数据、响应结构、错误码、测试和维护规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、启用条件、上传总原则、上传方式、上传接口、认证授权、安全校验、响应结构、错误码、测试验收、AI 修改规则、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{MEDIA_OWNER}`、`{UPLOAD_ENABLED}`、`{UPLOAD_SCENARIOS}`、`{UPLOAD_METHOD}`、`{API_PREFIX}`、`{UPLOAD_ENDPOINTS}`、`{AUTH_STRATEGY}`、`{OBJECT_STORAGE_ENABLED}`、`{OBJECT_STORAGE_STACK}`、`{BUCKET_POLICY}`、`{OBJECT_KEY_PATTERN}`、`{UPLOAD_ALLOWED_TYPES}`、`{UPLOAD_MAX_SIZE_POLICY}`、`{UPLOAD_SECURITY_POLICY}`、`{UPLOAD_RESPONSE_SCHEMA}`、`{UPLOAD_ERROR_CODES}`、`{UPLOAD_TEST_COMMAND}`。
  - 当 UPLOAD_ENABLED=false 且项目无上传、导入、附件、媒体或对象存储写入能力时，只保留启用条件和未来启用说明，删除强制接口、环境变量、存储、前端和测试要求。
  - 根据 UPLOAD_METHOD 保留或改写 multipart、预签名 URL、分片上传、后端流式上传、异步处理章节；未启用方式不得出现在强制规范中。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如图片、音频、视频、文档、导入文件、压缩包、对象存储、元数据、前端上传体验、扫描、转码、分片上传。
  - 上传接口、文件类型、大小限制、对象存储、bucket、对象 Key、元数据字段、错误码、前端处理和测试命令必须来自用户输入、需求、API 设计或对应文档；不得保留来源项目 bucket、路径、业务资源、对象 Key、错误码或存储供应商假设。
  - 保持 `docs/standards/file_upload.md` 与 `rules/media.md`、`rules/object-storage.md`、`rules/security.md`、`rules/api.md`、`docs/03-api-index.md`、`docs/04-database-design.md`、`docs/standards/error-codes.md`、`docs/06-video-asset-management.md`、`docs/07-object-storage-strategy.md`、`rules/testing.md` 一致。
- `docs/standards/testing-governance.md`：基于 `assets/pm-harness-template/docs/standards/testing-governance.md` 的模块化框架生成，作为测试目标、测试分层、目录职责、测试类型策略、AI 补测要求、CI 门禁、覆盖率治理、测试数据和例外审批的测试体系总纲。
  - 保留所有 `[通用]` 模块，包括文档定位、测试治理目标、OpenSpec 与需求变更测试要求、AI 开发要求、覆盖率治理、测试数据与环境、例外审批、相关文档、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{QA_OWNER}`、`{TEST_STRATEGY}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{TEST_FRAMEWORKS}`、`{UNIT_TEST_COMMAND}`、`{INTEGRATION_TEST_COMMAND}`、`{E2E_TEST_COMMAND}`、`{FULL_TEST_COMMAND}`、`{COVERAGE_COMMAND}`、`{CI_TEST_GATE}`、`{COVERAGE_GATE}`、`{TEST_REPORT_PATH}`、`{TEST_DIRECTORY_LAYOUT}`。
  - 根据 BACKEND_STACK、FRONTEND_STACK、DATABASE_STACK、OBJECT_STORAGE_STACK、PRODUCT_FORMS、HAS_WEB、HAS_WECHAT_MINIAPP、HAS_MOBILE、HAS_SDK、HAS_ALGORITHM 生成测试类型、目录职责和分层策略；未启用能力不得保留强制测试要求。
  - 测试框架、测试命令、测试目录、报告路径、CI 门禁和覆盖率门禁必须来自用户输入、实际脚本、测试框架或 CI 配置；未知时标记 `待确认`，不得编造。
  - 当项目暂未启用自动化测试时，保留测试治理目标、最低质量门禁、未来启用计划和例外审批，删除强制运行命令。
  - 不得保留来源项目测试目录、命令、对象存储服务、前端框架、数据库、CI 文件或业务场景假设。
  - 保持 `docs/standards/testing-governance.md` 与 `rules/testing.md`、`docs/standards/unit-test-standard.md`、`docs/standards/frontend-test-standard.md`、`docs/standards/test-coverage.md`、`openspec/testing-mapping.md`、CI 配置和测试脚本一致。
- `docs/standards/unit-test-standard.md`：基于 `assets/pm-harness-template/docs/standards/unit-test-standard.md` 的模块化框架生成，作为单元测试范围、目录命名、断言质量、Mock 边界、测试数据、覆盖要求、AI 补测规则和维护规范入口。
  - 保留所有 `[通用]` 模块，包括文档定位、启用条件、单元测试原则、测试场景要求、断言质量、示例模板、AI 修改规则、与其他测试的边界、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{QA_OWNER}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{UNIT_TEST_FRAMEWORK}`、`{UNIT_TEST_COMMAND}`、`{UNIT_TEST_PATHS}`、`{UNIT_TEST_FILE_PATTERN}`、`{SOURCE_LAYERING}`、`{MOCK_STRATEGY}`、`{FIXTURE_STRATEGY}`、`{UNIT_COVERAGE_TARGET}`、`{CI_UNIT_TEST_GATE}`。
  - 根据 SOURCE_LAYERING、BACKEND_STACK、FRONTEND_STACK、HAS_SDK、HAS_ALGORITHM、HAS_SCRIPTS 生成必须覆盖对象；未启用的层、端或模块不得保留强制单元测试要求。
  - 单元测试框架、测试命令、目录、命名规则、Mock 策略、Fixture 策略、覆盖率目标和 CI 门禁必须来自用户输入、实际测试框架、脚本或 CI 配置；未知时标记 `待确认`，不得编造。
  - 当项目暂未启用单元测试时，保留启用条件、单元测试原则、最低质量要求和未来启用说明，删除强制运行命令。
  - 示例必须按用户项目语言、框架和业务对象生成；不得保留来源项目业务类名、测试函数、数据库、目录、命令或技术栈假设。
  - 保持 `docs/standards/unit-test-standard.md` 与 `docs/standards/testing-governance.md`、`docs/standards/test-coverage.md`、`rules/testing.md`、CI 配置和测试脚本一致。
- `docs/standards/frontend-test-standard.md`：基于 `assets/pm-harness-template/docs/standards/frontend-test-standard.md` 的模块化框架生成，作为前端测试栈、组件测试、页面测试、API Mock、可访问性、视觉回归、E2E 分工、运行命令和 CI 门禁规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、启用条件、测试总原则、必须覆盖的前端场景、与 E2E 的分工、AI 修改规则、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{FRONTEND_OWNER}`、`{FRONTEND_ENABLED}`、`{FRONTEND_STACK}`、`{FRONTEND_TEST_STACK}`、`{E2E_TEST_STACK}`、`{FRONTEND_SOURCE_DIR}`、`{FRONTEND_TEST_FILE_PATTERN}`、`{FRONTEND_TEST_COMMAND}`、`{FRONTEND_CHECK_COMMAND}`、`{FRONTEND_COVERAGE_COMMAND}`、`{FRONTEND_COVERAGE_TARGET}`、`{DESIGN_SYSTEM_ENABLED}`、`{DESIGN_SYSTEM_COMPONENT_PATH}`、`{API_MOCK_STRATEGY}`、`{VISUAL_TEST_STRATEGY}`、`{A11Y_TEST_STRATEGY}`。
  - 当用户提供 `ui-design.md` 时，必须从中提取 Design System 组件、核心页面、交互状态、响应式规则、可访问性目标、视觉验收来源和验证命令，用于生成 DESIGN_SYSTEM_COMPONENT_PATH、VISUAL_TEST_STRATEGY、A11Y_TEST_STRATEGY、核心组件测试范围和页面测试范围；未知项标记 `待确认`。
  - 当 FRONTEND_ENABLED=false 且项目无 Web、管理后台、H5、桌面端、微信小程序、移动 Web 或可视化界面时，只保留启用条件和未来启用说明，删除强制测试栈、目录、组件测试和 E2E 要求。
  - 根据 FRONTEND_STACK 和 FRONTEND_TEST_STACK 生成 React、Vue、Svelte、Angular、微信小程序、桌面端或其他前端栈的测试工具和目录约定；不得保留未启用框架的强制测试工具。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如 Design System、页面测试、API Mock、可访问性、视觉回归、E2E、上传、媒体、登录态、权限状态。
  - 测试目录、测试命令、组件路径、Mock 策略、覆盖率目标和 CI 门禁必须来自用户输入、实际 `package.json`、脚本或 CI 配置；未知时标记 `待确认`，不得编造。
  - 不得保留来源项目测试框架、路径、组件名、测试文件名、命令或 Design System 假设。
  - 保持 `docs/standards/frontend-test-standard.md` 与 `rules/testing.md`、`rules/ui-design.md`、`docs/standards/testing-governance.md`、`docs/standards/unit-test-standard.md`、`docs/standards/test-coverage.md`、`tests/e2e/` 一致。
- `docs/standards/test-coverage.md`：基于 `assets/pm-harness-template/docs/standards/test-coverage.md` 的模块化框架生成，作为覆盖率目标、分层门槛、统计范围、排除规则、测量命令、CI 门禁、例外审批和趋势治理规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、启用条件、覆盖率总原则、必须重点覆盖的代码、例外与审批、趋势治理、与测试标准的关系、AI 修改规则、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{QA_OWNER}`、`{COVERAGE_ENABLED}`、`{COVERAGE_TARGET}`、`{COVERAGE_BY_LAYER}`、`{BACKEND_COVERAGE_TARGET}`、`{FRONTEND_COVERAGE_TARGET}`、`{CORE_MODULE_COVERAGE_TARGET}`、`{COVERAGE_TOOLING}`、`{COVERAGE_CONFIG_PATH}`、`{COVERAGE_COMMAND}`、`{COVERAGE_REPORT_FORMATS}`、`{COVERAGE_EXCLUDE_RULES}`、`{CI_COVERAGE_GATE}`、`{COVERAGE_ARTIFACT_PATH}`。
  - 当 COVERAGE_ENABLED=false 或项目暂未配置覆盖率统计时，只保留启用条件、质量替代门禁和未来启用说明，删除强制覆盖率命令、阈值和 CI 阻断要求。
  - 根据 BACKEND_STACK、FRONTEND_STACK、MOBILE_STACK、HAS_WEB、HAS_WECHAT_MINIAPP、HAS_SDK、HAS_ALGORITHM、HAS_SCRIPTS 生成分层覆盖率目标；未启用端或模块不得保留强制覆盖率门槛。
  - 覆盖率工具、配置路径、测量命令、报告格式、产物路径和 CI 门禁必须来自用户输入、实际测试框架、脚本或 CI 配置；未知时标记 `待确认`，不得编造。
  - 覆盖率排除规则必须显式登记；不得保留来源项目目录、命令、配置路径、CI 文件或技术栈假设。
  - 保持 `docs/standards/test-coverage.md` 与 `rules/testing.md`、`docs/standards/testing-governance.md`、`docs/standards/unit-test-standard.md`、`docs/standards/frontend-test-standard.md`、CI 配置和测试框架配置一致。
- `00-product-overview.md`：基于 `assets/pm-harness-template/docs/00-product-overview.md` 的模块化框架生成，作为产品定位、目标用户、用户痛点、产品形态、核心场景、核心能力、范围边界、数据对象、成功指标和文档导航入口。
  - 保留所有 `[通用]` 模块，包括文档定位、文档导航、更新触发条件和初始化生成建议。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{BUSINESS_DOMAIN}`、`{PRODUCT_DESCRIPTION}`、`{TARGET_USERS}`、`{USER_PAIN_POINTS}`、`{PRODUCT_FORMS}`、`{CORE_SCENARIOS}`、`{CORE_CAPABILITIES}`、`{OUT_OF_SCOPE}`、`{SUCCESS_METRICS}`、`{STAKEHOLDERS}`。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如 Web、管理后台、微信小程序、移动端、桌面端、API/SDK、媒体、对象存储、算法/模型服务。
  - 核心场景必须按“角色 + 触发条件 + 用户目标 + 关键步骤 + 成功结果”生成，不得只罗列功能名。
  - 核心能力必须能映射到后续 `issues/requirements/`、`openspec/changes/`、`docs/` 或 `rules/`。
  - 未确认的信息标记为 `待确认`；不得保留来源项目业务名、用户角色、能力名称或服务地址。
  - 保持 `00-product-overview.md` 与 `README.md`、`project.yaml`、`AGENTS.md`、`docs/01-architecture.md`、`docs/04-database-design.md`、`rules/global.md`、`rules/document-governance.md` 一致。
- `01-architecture.md`：基于 `assets/pm-harness-template/docs/01-architecture.md` 的模块化框架生成，作为系统上下文、模块职责、源码分层、运行时拓扑、关键数据流、存储架构、API/集成、安全权限、非功能要求、AI 开发边界和架构决策入口。
  - 保留所有 `[通用]` 模块，包括文档定位、架构原则、AI 开发边界、测试验证边界、更新触发条件和初始化生成建议。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{ASYNC_TASK_STACK}`、`{ALGORITHM_STACK}`、`{DEPLOYMENT_STACK}`、`{EXTERNAL_INTEGRATIONS}`、`{ARCHITECTURE_OWNER}`、`{PRIMARY_VERIFY_COMMAND}`。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如后端、Web、微信小程序、移动端、共享层、SDK、对象存储、媒体、异步任务、算法/模型、外部集成、缓存/搜索、Kubernetes/私有化部署。
  - 总体架构图必须根据 FORMS 和技术栈生成真实模块，不得保留未启用端或不存在服务。
  - 模块职责必须能映射到 `src/`、`deploy/`、`data/`、`models/`、`tests/` 等实际目录。
  - 数据流必须按“触发角色 + 入口端 + API/服务 + 数据对象 + 失败策略 + 验证方式”生成；涉及文件、媒体、对象存储、异步任务、算法模型时必须保留对应链路。
  - 运行时拓扑必须与 `docs/02-deployment.md`、`.env.example`、`docker-compose.yml` 或 `deploy/` 一致。
  - 存储架构必须与 `docs/04-database-design.md`、`rules/database.md`、`rules/data-management.md`、`rules/object-storage.md` 一致。
  - 不得保留来源项目业务名、服务名、端口、技术栈或存储方案；未知信息标记为 `待确认`。
  - 保持 `01-architecture.md` 与 `00-product-overview.md`、`README.md`、`project.yaml`、`AGENTS.md`、`docs/02-deployment.md`、`docs/03-api-index.md`、`docs/04-database-design.md`、`docs/05-compatibility-matrix.md`、`rules/directory-structure.md` 一致。
- `02-deployment.md`：基于 `assets/pm-harness-template/docs/02-deployment.md` 的模块化框架生成，作为部署目标、服务组成、环境变量、端口策略、运行方式、数据持久化、安全要求、验证与回滚入口。
  - 保留所有 `[通用]` 模块，包括文档定位、部署目标、环境配置、端口策略、数据持久化、部署安全、部署验证、回滚与故障处理、AI 修改规则、更新触发条件和初始化生成建议。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{DEPLOYMENT_STACK}`、`{DEPLOYMENT_ENVIRONMENTS}`、`{SERVICE_MATRIX}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{ASYNC_TASK_STACK}`、`{ALGORITHM_STACK}`、`{DEPLOYMENT_OWNER}`、`{PRIMARY_DEPLOY_COMMAND}`、`{PRIMARY_VERIFY_COMMAND}`。
  - 根据 DEPLOYMENT_STACK 保留或删除 `[条件启用]` 模块，例如 Docker Compose、Kubernetes/Helm、SaaS、PaaS、私有化、离线交付。
  - 根据 SERVICE_MATRIX 生成真实服务、镜像/构建来源、内部端口、宿主/入口端口、依赖、volume 和健康检查；未启用服务不得出现在部署组件中。
  - 根据数据库、对象存储、媒体、异步任务、算法/模型能力保留或删除对应部署章节。
  - 环境变量矩阵必须与 `.env.example`、`rules/environment.md` 一致；敏感变量不得生成真实默认值。
  - 端口策略必须与 `rules/port-management.md` 一致；不得为了本机冲突修改应用内部端口。
  - Docker Compose 服务必须与 `docker-compose.yml`、Dockerfile、服务级 env 文件一致；Kubernetes/Helm 必须与 `deploy/` 一致。
  - 数据持久化必须与 `rules/data-management.md`、`rules/database.md`、`rules/object-storage.md` 一致。
  - 不得保留来源项目容器名、bucket、端口、账号、密码、服务名或部署命令；未知信息标记为 `待确认`。
  - 保持 `02-deployment.md` 与 `01-architecture.md`、`README.md`、`AGENTS.md`、`.env.example`、`docker-compose.yml`、`deploy/`、`rules/environment.md`、`rules/port-management.md`、`rules/security.md`、`rules/release.md` 一致。
- `03-api-index.md`：基于 `assets/pm-harness-template/docs/03-api-index.md` 的模块化框架生成，作为 API 分组、基础约定、认证授权、响应结构、错误码、OpenAPI、客户端生成、接口维护规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、基础约定、OpenAPI 与契约来源、API 分组、接口清单模板、错误码速查、版本兼容、API 测试要求、维护规则和初始化生成建议。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{API_PREFIX}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{AUTH_STRATEGY}`、`{PERMISSION_MODEL}`、`{RESPONSE_ENVELOPE}`、`{ERROR_CODE_DOC_PATH}`、`{OPENAPI_SOURCE}`、`{API_DOC_PATH}`、`{API_CLIENT_GENERATOR}`、`{API_CLIENT_GENERATE_COMMAND}`、`{API_GENERATED_DIR}`、`{API_GROUPS}`、`{API_OWNER}`。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如认证、权限、OpenAPI 客户端生成、文件上传、媒体、Webhook、异步任务、外部集成、SDK。
  - 根据 API_GROUPS 生成真实 API 分组、路径前缀、认证要求、状态和契约来源；不得保留来源项目业务资源。
  - API 前缀未知时默认建议 `/api/v1`，但必须标记 `待确认`。
  - 如果启用 OpenAPI 客户端生成，必须生成 API_CLIENT_GENERATOR、API_CLIENT_GENERATE_COMMAND、API_GENERATED_DIR；未启用时删除硬性生成命令。
  - 错误码、响应 envelope、认证头、字段命名、分页、幂等和版本策略必须与 `rules/api.md`、`rules/security.md`、`rules/language.md` 一致。
  - 文件上传、媒体、对象存储接口必须与 `rules/media.md`、`rules/object-storage.md`、`docs/04-database-design.md` 一致。
  - 不得保留来源项目接口路径、资源名、角色名、错误 message、脚本路径或生成目录；未知信息标记为 `待确认`。
  - 保持 `03-api-index.md` 与 `rules/api.md`、`docs/01-architecture.md`、`docs/04-database-design.md`、`rules/testing.md`、`rules/security.md`、前端生成配置和后端框架描述一致。
- `04-database-design.md`：基于 `assets/pm-harness-template/docs/04-database-design.md` 的模块化框架生成，作为数据库选型、Schema 来源、表清单、字段规范、关系约束、索引、迁移、种子数据、数据安全和维护规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、数据库概述、数据对象与 ER 关系、表清单、通用字段规范、表结构模板、迁移策略、数据安全、与 API 对应、测试要求、维护规则和初始化生成建议。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{DATABASE_STACK}`、`{MIGRATION_STRATEGY}`、`{SCHEMA_SOURCE}`、`{ORM_STACK}`、`{REPOSITORY_PATTERN}`、`{CORE_DATA_OBJECTS}`、`{AUTH_STRATEGY}`、`{AUDIT_POLICY}`、`{OBJECT_STORAGE_STACK}`、`{MEDIA_ENABLED}`、`{TENANCY_MODEL}`、`{DATABASE_OWNER}`。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如认证用户、审计日志、媒体/文件元数据、对象存储、租户隔离、多数据库兼容、Seed、Fixtures。
  - 根据 CORE_DATA_OBJECTS 生成真实业务表；未知时写 `业务表待需求明确后填充`，不得保留来源项目业务表。
  - Schema 来源、ORM/Model 路径、Repository/DAO 路径、迁移路径必须与实际技术栈和目录结构一致。
  - 认证、角色、用户状态、权限表必须与 `rules/security.md`、`docs/03-api-index.md` 一致。
  - 媒体、文件、对象存储元数据必须与 `rules/media.md`、`rules/object-storage.md`、`docs/07-object-storage-strategy.md` 一致。
  - Seed、Fixtures、运行时数据库、本地 demo 数据必须与 `rules/data-management.md`、`.gitignore` 一致。
  - 不得保留来源项目业务表、字段、角色、bucket、运行时路径或 API 路径；未知信息标记为 `待确认`。
  - 保持 `04-database-design.md` 与 `rules/database.md`、`docs/01-architecture.md`、`docs/02-deployment.md`、`docs/03-api-index.md`、`rules/data-management.md`、`rules/testing.md` 一致。
- `05-compatibility-matrix.md`：基于 `assets/pm-harness-template/docs/05-compatibility-matrix.md` 的模块化框架生成，作为产品形态兼容、能力覆盖、浏览器与设备、运行时、数据库、对象存储、部署环境、操作系统、CPU 架构、API 兼容和验证规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、兼容性等级、产品形态与能力矩阵、API 与协议兼容、后端运行时兼容、操作系统与 CPU 架构兼容、部署方式兼容、兼容性测试矩阵、AI 修改兼容性规则、更新触发条件和初始化生成建议。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_FORMS}`、`{SUPPORTED_CLIENTS}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{DEPLOYMENT_STACK}`、`{OS_SUPPORT_MATRIX}`、`{CPU_ARCH_MATRIX}`、`{RUNTIME_VERSION_MATRIX}`、`{COMPATIBILITY_OWNER}`、`{COMPATIBILITY_TEST_COMMAND}`。
  - 根据 PRODUCT_FORMS 保留或删除 Web、管理后台、微信小程序、移动端、桌面端、API/SDK 等端能力列；未启用端不得出现在强制矩阵中。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如浏览器兼容、移动端/微信小程序/桌面端、数据库、对象存储、外部服务、信创、私有化部署、OS/CPU。
  - 能力名称必须来自 `00-product-overview.md` 或需求文档；不得保留来源项目业务能力。
  - 数据库、对象存储、部署、运行时和 API 兼容要求必须分别与 `04-database-design.md`、`07-object-storage-strategy.md`、`02-deployment.md`、`01-architecture.md`、`03-api-index.md` 一致。
  - 兼容性测试矩阵必须与 `rules/testing.md`、`rules/compatibility.md`、`rules/release.md` 一致；无法自动化验证时必须生成人工验证步骤。
  - 不得保留来源项目端名称、业务能力、数据库、对象存储、浏览器版本或部署环境；未知信息标记为 `待确认`。
  - 保持 `05-compatibility-matrix.md` 与 `rules/compatibility.md`、`docs/00-product-overview.md`、`docs/01-architecture.md`、`docs/02-deployment.md`、`docs/03-api-index.md`、`docs/04-database-design.md`、`rules/testing.md`、`rules/release.md` 一致。
- `06-video-asset-management.md`：基于 `assets/pm-harness-template/docs/06-video-asset-management.md` 的模块化框架生成，作为视频与富媒体资产场景、端能力、上传、对象存储、封面、转码、播放、元数据、安全、测试和验收规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、启用条件、视频资产生命周期、上传策略、安全与合规、测试与验收、初始化阶段建议、AI 修改要求和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{VIDEO_ENABLED}`、`{MEDIA_ASSET_OWNER}`、`{PRODUCT_FORMS}`、`{VIDEO_BUSINESS_SCENARIOS}`、`{OBJECT_STORAGE_STACK}`、`{VIDEO_BUCKET}`、`{VIDEO_KEY_PATTERN}`、`{COVER_KEY_PATTERN}`、`{TRANSCODING_ENABLED}`、`{TRANSCODING_PROVIDER}`、`{CDN_ENABLED}`、`{MEDIA_TABLE}`、`{UPLOAD_MAX_SIZE}`、`{VIDEO_FORMATS}`、`{VIDEO_TEST_COMMAND}`。
  - 当 VIDEO_ENABLED=false 且需求中没有视频/富媒体能力时，只保留启用条件、未来启用建议和文档治理说明，删除强制 API、数据库、转码、前端和测试实现要求。
  - 根据 PRODUCT_FORMS 保留或删除 Web、管理后台、移动端、微信小程序、桌面端、API/SDK 的端能力矩阵；未启用端不得出现在强制能力中。
  - 根据项目能力保留或删除 `[条件启用]` 模块，例如对象存储、封面、转码、CDN、API、前端体验、移动端/微信小程序适配、内容审核。
  - 业务场景、业务对象、媒体表、bucket、object key、API 路径和测试命令必须来自用户输入或对应文档；不得保留来源项目业务场景、表名、bucket 或 key。
  - 对象存储、媒体类型、数据库元数据、API、权限和兼容性要求必须分别与 `rules/object-storage.md`、`rules/media.md`、`docs/04-database-design.md`、`docs/03-api-index.md`、`rules/security.md`、`docs/05-compatibility-matrix.md` 一致。
  - 兼容性测试和验收标准必须与 `rules/testing.md`、`rules/compatibility.md`、`rules/release.md` 一致；无法自动化验证时必须生成人工验证步骤。
  - 未知信息标记为 `待确认`，不得编造转码服务、CDN、文件大小、格式白名单或权限模型。
  - 保持 `06-video-asset-management.md` 与 `rules/media.md`、`rules/object-storage.md`、`rules/security.md`、`rules/api.md`、`rules/testing.md`、`docs/03-api-index.md`、`docs/04-database-design.md`、`docs/05-compatibility-matrix.md` 一致。
- `07-object-storage-strategy.md`：基于 `assets/pm-harness-template/docs/07-object-storage-strategy.md` 的模块化框架生成，作为对象存储选型、桶/容器策略、资源前缀、对象 key、访问控制、上传下载、元数据、生命周期、备份迁移、成本治理和测试验收规则入口。
  - 保留所有 `[通用]` 模块，包括文档定位、启用条件、当前策略概览、桶/容器划分策略、资源前缀与类型、对象 Key 命名规范、访问控制、上传与下载策略、元数据与数据库关联、生命周期与清理、备份迁移恢复、本地开发与测试替代方案、测试与验收、何时调整桶策略、AI 修改要求和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{OBJECT_STORAGE_ENABLED}`、`{OBJECT_STORAGE_OWNER}`、`{OBJECT_STORAGE_PROVIDER}`、`{OBJECT_STORAGE_MODE}`、`{DEFAULT_BUCKET}`、`{BUCKET_NAMING_RULE}`、`{OBJECT_KEY_PATTERN}`、`{PUBLIC_ACCESS_POLICY}`、`{SIGNED_URL_TTL}`、`{CDN_ENABLED}`、`{MEDIA_TYPES}`、`{BACKUP_POLICY}`、`{LIFECYCLE_POLICY}`、`{OBJECT_STORAGE_TEST_COMMAND}`。
  - 当 OBJECT_STORAGE_ENABLED=false 且需求中没有文件/媒体/导入导出能力时，只保留启用条件、替代方案和未来迁移触发条件，删除强制 bucket、环境变量、集成测试和部署要求。
  - 根据 OBJECT_STORAGE_MODE 选择单桶 + 前缀、多桶、按环境隔离、按租户隔离等策略；未选择的策略应保留为参考或删除强制配置。
  - 根据 MEDIA_TYPES 保留或删除图片、视频、文档、导入导出、临时文件、处理产物、归档等资源前缀；未启用类型不得出现在强制清单中。
  - bucket、container、前缀、object key、访问策略、生命周期和测试命令必须来自用户输入或对应文档；不得保留来源项目 bucket、前缀、服务提供方或业务资源说明。
  - 对象存储策略必须与 `rules/object-storage.md`、`rules/media.md`、`rules/security.md`、`rules/api.md`、`rules/data-management.md`、`docs/03-api-index.md`、`docs/04-database-design.md`、`docs/06-video-asset-management.md` 一致。
  - 备份、迁移、生命周期、成本治理和兼容性要求必须与 `docs/02-deployment.md`、`docs/05-compatibility-matrix.md`、`rules/compatibility.md`、`rules/release.md` 一致。
  - 未知信息标记为 `待确认`，不得编造云厂商、bucket 名称、公开策略、签名 URL TTL、CDN 或清理周期。
  - 保持 `07-object-storage-strategy.md` 与 `rules/object-storage.md`、`rules/media.md`、`rules/security.md`、`rules/data-management.md`、`docs/02-deployment.md`、`docs/03-api-index.md`、`docs/04-database-design.md`、`docs/05-compatibility-matrix.md`、`docs/06-video-asset-management.md` 一致。

### openspec/project.md 和 config.yaml

- `openspec/project.md`：基于 `assets/pm-harness-template/openspec/project.md` 的模块化框架生成，作为 OpenSpec 项目上下文，覆盖项目背景、产品范围、技术栈、目录职责、研发事实源、Change ID、规格模块、执行流程、AI 约束、测试映射和文档同步关系。
  - 保留所有 `[通用]` 模块，包括文档定位、OpenSpec 目录职责、研发事实源、OpenSpec 执行流程、AI 执行约束、与项目文档同步关系、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_OWNER}`、`{PRODUCT_DESCRIPTION}`、`{BUSINESS_DOMAIN}`、`{TARGET_USERS}`、`{PRODUCT_FORMS}`、`{CORE_CAPABILITIES}`、`{OUT_OF_SCOPE}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{DATABASE_STACK}`、`{OBJECT_STORAGE_STACK}`、`{ASYNC_TASK_STACK}`、`{ALGORITHM_STACK}`、`{DEPLOYMENT_STACK}`、`{OPENSPEC_ENABLED}`、`{CHANGE_ID_PATTERN}`、`{SPEC_MODULES}`、`{PRIMARY_VERIFY_COMMAND}`。
  - 根据 OPENSPEC_ENABLED 决定保留完整 OpenSpec 流程或标记为“不适用”；未启用 OpenSpec 时必须指向项目等价变更系统，不得保留不可执行的强制流程。
  - 根据 PRODUCT_FORMS、CORE_CAPABILITIES、BACKEND_STACK、FRONTEND_STACK、DATABASE_STACK、OBJECT_STORAGE_STACK、ASYNC_TASK_STACK、ALGORITHM_STACK、DEPLOYMENT_STACK 生成产品范围、技术栈上下文、规格模块和同步关系；未启用能力不得保留正式规格要求。
  - Change ID、规格模块、验证命令和事实源必须来自用户输入、项目治理流程或实际目录；未知时标记 `待确认`，不得编造。
  - 不得保留来源项目业务名、用户角色、技术栈、路径、端口、对象存储、数据库、规格模块或示例。
  - 保持 `openspec/project.md` 与 `AGENTS.md`、`project.yaml`、`README.md`、`docs/00-product-overview.md`、`docs/01-architecture.md`、`rules/document-governance.md`、`openspec/testing-mapping.md` 一致。
- `openspec/config.yaml`：基于 `assets/pm-harness-template/openspec/config.yaml` 的模块化 YAML 配置生成，作为 OpenSpec 项目标识、目录路径、语言策略、Change 命名、规格策略、校验命令、归档策略和 AI guardrails 配置入口。
  - 保留顶部注释元数据，包括 purpose、content、source、update_method、owner、note；不得给 YAML 文件插入 Markdown frontmatter。
  - 用用户输入替换占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{PRODUCT_OWNER}`、`{OPENSPEC_ENABLED}`、`{OPENSPEC_SPEC_DIR}`、`{OPENSPEC_CHANGE_DIR}`、`{OPENSPEC_ARCHIVE_DIR}`、`{OPENSPEC_PROJECT_DOC}`、`{OPENSPEC_TESTING_MAPPING}`、`{OPENSPEC_LANGUAGE}`、`{DEFAULT_LOCALE}`、`{DOCUMENTATION_LANGUAGE}`、`{CHANGE_ID_PATTERN}`、`{SPEC_MODULES}`、`{OPENSPEC_VALIDATE_COMMAND}`、`{OPSX_PROPOSE_COMMAND}`、`{OPSX_APPLY_COMMAND}`、`{OPSX_ARCHIVE_COMMAND}`、`{OPENSPEC_TESTING_MAPPING_VALIDATE_COMMAND}`、`{TARGET_CHANGE_PATH}`、`{EXTERNAL_TRACKING_ENABLED}`、`{TASK_TRACKING_SYSTEM}`、`{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{SPRINT_ROOT_DIR}`。
  - 根据 OPENSPEC_ENABLED 决定是否保留完整 changes/specs/archive/testing-mapping 配置；未启用 OpenSpec 时保留最小配置并标记 `enabled: false`，不得保留强制执行命令。
  - Change allowed_prefixes、required_files、status_flow 必须与 `openspec/project.md`、`rules/document-governance.md`、`rules/requirement-management.md`、`rules/bug-management.md` 一致。
  - commands 字段必须来自实际命令、脚本或 Agent 命令定义；未知时标记 `待确认` 或删除对应命令，不得编造。
  - external_tracking 仅在启用外部需求/Bug/Sprint 系统时保留；未启用时设置 enabled=false 或删除 system 字段。
  - 配置必须保持 YAML 可解析；占位符需要加引号时必须加引号，布尔值占位符必须初始化为 true/false。
  - 不得保留来源项目 project 值、业务名、路径、技术栈、命令或规格模块。
  - 保持 `openspec/config.yaml` 与 `openspec/project.md`、`AGENTS.md`、`project.yaml`、`rules/document-governance.md`、`openspec/testing-mapping.md` 一致。
- `openspec/testing-mapping.md`：基于 `assets/pm-harness-template/openspec/testing-mapping.md` 的模块化框架生成，作为 Requirement、Bug、OpenSpec Change、验收项、测试用例、验证命令、测试证据和例外审批的追溯索引。
  - 保留所有 `[通用]` 模块，包括文档定位、追溯对象、映射总原则、例外审批、AI 修改规则、初始化生成建议和更新触发条件。
  - 用用户输入替换 `[个性化]` 占位符：`{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{QA_OWNER}`、`{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{CHANGE_ROOT_DIR}`、`{SPEC_ROOT_DIR}`、`{TEST_ROOT_DIR}`、`{TEST_FRAMEWORKS}`、`{TEST_COMMANDS}`、`{CI_TEST_GATE}`、`{COVERAGE_GATE}`、`{TRACE_ID_POLICY}`、`{EVIDENCE_STORAGE_POLICY}`。
  - 根据 TEST_FRAMEWORKS、TEST_COMMANDS、CI_TEST_GATE、COVERAGE_GATE、HAS_WEB、HAS_API、HAS_DATABASE、HAS_OBJECT_STORAGE、HAS_AUTH、HAS_E2E、HAS_COMPATIBILITY 生成测试类型矩阵；未启用测试类型不得保留强制映射。
  - 根据实际需求、Bug 和 OpenSpec Change 生成初始映射；没有实际记录时保留格式模板，不得生成虚假的 REQ、BUG、Change 或 passing 测试。
  - 测试路径、命令、证据、owner 和状态必须来自实际测试框架、脚本、CI 或人工验收记录；未知时标记 `待确认`、`planned` 或 `待执行`，不得编造。
  - Bug 修复映射必须包含复现或回归测试要求；无法自动化时必须登记例外审批和替代验证。
  - 不得保留来源项目 Sprint、需求 ID、登录场景、测试文件、脚本、框架、路径或业务能力示例。
  - 保持 `openspec/testing-mapping.md` 与 `openspec/project.md`、`openspec/config.yaml`、`rules/testing.md`、`docs/standards/testing-governance.md`、`docs/standards/test-coverage.md`、CI 配置一致。

### issues/requirements/template/

基于 `assets/templates/requirements-template-README.md`、`assets/templates/requirement-template.md` 和 `assets/templates/requirement-trace-template.md` 创建如下结构（帮助用户了解如何创建需求）：

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

每个文件包含结构占位和说明注释（中文），不得恢复来源项目的示例需求。

### issues/bugs/template/

基于 `assets/templates/bugs-template-README.md` 和 `assets/templates/bug-template.md` 创建如下结构（帮助用户了解如何记录 Bug）：

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

每个文件包含结构占位和说明注释（中文），不得恢复来源项目的示例缺陷。

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

**src/wechat-miniapp/**（HAS_WECHAT_MINIAPP=true 时创建）

```
src/wechat-miniapp/
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

### Agent 工具目录

构建 Agent 目录时必须完整读取 [agent-tool-mapping.md](references/agent-tool-mapping.md) 和 [default-command-catalog.md](references/default-command-catalog.md)。

- 只生成 `ENABLED_AGENT_TOOLS` 中启用的目录；用户未选择时按输入 schema 默认值生成。
- 使用 `.claude/` 作为唯一命令与嵌套 Skill 事实源，按 Agent 映射渲染其它工具目录。
- 各工具的同名命令必须遵守默认命令目录中的阶段、输入、输出、文档/代码边界。

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

如新增 `created_at`、`updated_at`、`reviewed_at`、`verified_at`、`archived_at`、`published_at` 等时间字段，必须使用 `YYYY-MM-DD hh:mm:ss`；无法确认完整时间时写 `待确认`。

---

## 置空目录规则

以下目录不在轻量模板中预置完整文件，初始化时需创建目录结构并保持内容为空。若目标仓库需要追踪空目录，可创建 `.gitkeep`；否则可以只创建空目录。

- `data/`（所有子目录）
- `docs/knowledge-base/`
- `openspec/specs/`
- `openspec/changes/`
- `openspec/archive/`
- `iterations/`

---

## 质量要求

1. **无业务硬编码**：生成的工程不得包含任何来源项目业务词汇（产品名替换除外）
2. **中文优先**：所有文档使用中文，代码标识符使用英文
3. **结构完整性**：每个 src 子目录必须有 `README.md` 说明目录职责
4. **规则一致性**：AGENTS.md、rules/、project.yaml 中的技术栈描述必须一致
5. **模板可用性**：issues/template 中的模板文件必须包含真实可用的结构示例

---

## 常见产品形态与目录对照

| 产品形态 | src 子目录 | compatibility/devices/ |
|---------|-----------|----------------------|
| Web | `src/web/` | `web.md` |
| 微信小程序 | `src/wechat-miniapp/` | `wechat-miniapp.md` |
| Android | `src/android/` | `android.md` |
| iOS | `src/ios/` | `ios.md` |
| 桌面端 | `src/desktop/` | `desktop.md` |
| H5 | `src/h5/` | `h5.md` |

---

## 输出检查清单

生成完成后，在向用户展示前，确认以下项目：

```
□ 所有文件中来源项目产品名已替换为 {PRODUCT_NAME}
□ 所有文件中来源项目代码名已替换为 {PRODUCT_CODE}
□ src/ 目录根据 FORMS 正确创建/省略
□ src/algorithm/ 根据 HAS_ALGORITHM 正确处理
□ docker-compose.yml 服务与实际选型一致
□ .env.example 变量与 docker-compose.yml 一致
□ issues/requirements/ 包含 plan、review、archive 三个状态目录
□ issues/bugs/ 包含 plan、review、archive 三个状态目录
□ rules/issues-lifecycle.md 已生成，并与需求/BUG/目录/文档治理规则一致
□ openspec/specs、changes、archive 仅保留 .gitkeep
□ iterations/ 仅保留 .gitkeep
□ data/ 仅保留 .gitkeep 或必要 README
□ docs/knowledge-base/ 仅保留 .gitkeep 或必要 README
□ ENABLED_AGENT_TOOLS 已根据用户选择或默认值写入 README、AGENTS、project.yaml 和 rules
□ 启用的 Agent 工具目录已生成，未启用的 Agent 工具目录未保留
□ 非 Claude Code 工具目录已基于 .claude 命令语义生成
□ 信创数据库（如有）相关文件已创建
□ 信创操作系统（如有）相关文件已创建
□ 所有 Markdown 文件包含正确元数据头部
```
