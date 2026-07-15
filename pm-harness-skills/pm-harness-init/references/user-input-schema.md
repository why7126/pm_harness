# 用户输入 Schema

## 使用规则

- 按下表的序号逐项提示用户输入或选择；不得跳过、合并或改变顺序。
- 下表全部为必填项。默认选项可直接采用，但仍要在该步骤明确展示并让用户确认；“其他”被选中时，必须要求填写具体内容。
- 用户可以一次性提供多个字段。已提供且有效的字段无需重复询问，继续提示下一个未完成步骤。
- `暂无` 是产品竞品与核心竞争力的合法占位值，不得把它当作缺失信息追问。
- 多选冲突项须在选择当下处理：选中冲突项会取消另一组中的已有选择；不得让冲突组合进入推导配置。
- 除本表列出的用户决策外，其余变量均由 AI 基于用户输入自动派生；不再询问项目代码、部署方式、认证、缓存、异步任务或测试命令等扩展字段。
- 生成最终工程时，`待确认` 只能作为集中待决策事项出现，不得散落在 README、AGENTS、配置文件或大段文档表格中。

## 顺序化输入清单

| 序号 | 输入项 | 变量 | 输入方式与引导 | 默认值 / 校验 |
|---:|---|---|---|---|
| 1 | 产品名称 | `PRODUCT_NAME` | 文本。提示：`请输入产品名称。` | 必填，非空。
| 2 | 产品编号 | `PRODUCT_CODE` | 文本。提示：`请输入产品编号，仅允许使用英文字母、下划线 _ 或连字符 -。` | 必填；必须匹配 `^[A-Za-z_-]+$`，不得包含中文、数字、空格或其他特殊字符。
| 3 | 产品描述 | `PRODUCT_DESCRIPTION`、`TARGET_USERS`、`PROBLEM_STATEMENT` | 文本。提示：`请说明面向哪些用户群体，以及产品为该用户群体解决什么问题。` | 必填；内容必须同时覆盖用户群体和待解决问题。
| 4 | 核心能力 | `CORE_CAPABILITIES` | 文本或分条。提示：`请填写产品的核心能力。` | 必填，至少一项明确能力。
| 5 | 产品竞品 | `COMPETITORS` | 文本或分条。提示：`请填写竞品名称及其官网地址；如暂无竞品，可填写“暂无”。` | 必填；每个非“暂无”竞品须含名称和官网地址。
| 6 | 核心竞争力 | `CORE_COMPETENCIES` | 文本或分条。提示：`请填写产品相对竞品的核心竞争力；如暂无，可填写“暂无”。` | 必填。
| 7 | 产品形态 | `PRODUCT_FORMS` | 多选：`Web端`、`微信小程序`、`桌面端`、`移动端（H5）`、`移动端（iOS）`、`移动端（Android）`、`其他`。选中“其他”时追加文本输入。 | 必填，至少一项；默认选中 `Web端`。
| 8 | 管理后台 | `ADMIN_CONSOLE_INCLUDED` | 单选：`包含`、`不包含`。 | 必填；默认 `包含`。
| 9 | 对象存储 | `OBJECT_STORAGE_TYPES` | 多选：`无`、`文档`、`图片`、`音频`、`视频`、`其他`。选中“其他”时追加文本输入。 | 必填，至少一项；`无` 与 `文档/图片/音频/视频` 互斥。
| 10 | 本地模型 | `LOCAL_MODEL_INCLUDED` | 单选：`包含`、`不包含`。 | 必填；默认 `不包含`。
| 11 | 后端技术栈 | `BACKEND_STACK` | 单选：`Python + FastAPI + Pydantic + uv`、`其他`。选中“其他”时追加文本输入。 | 必填；默认 `Python + FastAPI + Pydantic + uv`。
| 12 | 前端技术栈 | `FRONTEND_STACK` | 单选：`React + TypeScript + TailWind + Shadcn/UI + Axios + Orval + pnpm`、`其他`。选中“其他”时追加文本输入。 | 必填；默认 `React + TypeScript + TailWind + Shadcn/UI + Axios + Orval + pnpm`。
| 13 | 主关系型数据库 | `DB_PRIMARY`、`DATABASE_STACK` | 单选：`SQLite`、`MySQL`、`Postgresql`、`其他`。选中“其他”时追加文本输入。 | 必填；默认 `SQLite`。
| 14 | 信创数据库 | `XINCHUANG_DATABASES` | 多选：`无`、`达梦`、`海量`、`Postgresql`、`其他`。选中“其他”时追加文本输入。 | 必填，至少一项；`无` 与 `达梦/海量/Postgresql` 互斥。
| 15 | 编码 Agent 工具 | `ENABLED_AGENT_TOOLS`、`PRIMARY_AGENT_TOOL` | 多选：`Codex`、`Claude Code`、`Cursor`、`OpenCode`、`Kiro`、`其他`。选中“其他”时追加文本输入。 | 必填，至少一项；默认选中 `Codex`。`PRIMARY_AGENT_TOOL` 默认取第一个已选标准工具；仅选择“其他”时取其填写值。
| 16 | UI 设计 | `UI_DESIGN_INPUT_MODE`、`UI_DESIGN_SOURCE_PATH`、`UI_DESIGN_SOURCE_CONTENT`、`UI_STYLE_BRIEF` | 二选一：`上传 ui-design.md` 或 `手工输入 UI 设计风格`。上传时读取完整文档；手工输入时显示下方的填写引导。 | 必填；两种方式必须且只能选择一种。

> 用户原始编号中“核心能力”和“产品竞品”均标为 3。为保证问询顺序和变量可追踪性，schema 内连续编号；加上新增产品编号与 UI 设计，共 16 个输入步骤。

### UI 设计输入分支

#### 上传 `ui-design.md`

- 要求用户上传名为 `ui-design.md` 的文档；读取完整内容并写入 `UI_DESIGN_SOURCE_CONTENT`。
- 此模式下，生成的设计方案、Token、页面/组件规范、交互和视觉验收规则必须严格遵循该文档。不得以 AI 偏好替换、扩写或重设计其中的明确内容。
- 文档未覆盖的项目仅标记为 `待确认` 或 `不适用`；不得用 AI 自动补齐为与文档冲突的方案。
- 用户在此前步骤中的显式产品输入与文档存在矛盾时，暂停生成并要求用户明确以哪项为准；不得静默覆盖任一来源。

#### 手工输入 UI 设计风格

要求用户填写 `UI_STYLE_BRIEF`。输入框应给出以下引导，用户可自由文字描述或分条填写：

1. **整体风格与品牌气质**：例如专业、简约、科技感、温暖、轻奢、数据密集等。
2. **色彩偏好**：主色、辅助色、背景色，以及是否有必须避免的颜色或品牌色。
3. **字体与排版**：中文/英文风格、字号层级、阅读密度、圆角与阴影偏好。
4. **布局与导航**：例如侧边栏、顶部导航、卡片/Bento、表格优先、仪表盘或内容流。
5. **组件与交互**：按钮、表单、数据展示、反馈动效的气质；是否偏好 Shadcn/UI 的默认风格或需要强定制。
6. **图标、插画与图片**：使用偏好、禁用元素，以及是否需要深色模式、响应式与无障碍支持。
7. **核心页面或关键场景**：希望优先设计的页面、流程或用户任务。

- 手工输入模式下，AI 基于 `UI_STYLE_BRIEF`、产品描述、核心能力、产品形态和前端技术栈，自动生成完整且一致的设计方案，并写入 `rules/ui-design.md` 及其关联文档。
- 未填写的视觉细节由 AI 合理推导，不再逐项追问；生成方案须与用户明确的偏好一致。

## 标准化与冲突处理

### 产品形态标准化

| 用户选择 | 标准值 | 派生变量 |
|---|---|---|
| Web端 | `Web` | `HAS_WEB=true`、`HAS_FRONTEND=true` |
| 微信小程序 | `微信小程序` | `HAS_WECHAT_MINIAPP=true`、`HAS_FRONTEND=true` |
| 桌面端 | `桌面端` | `HAS_DESKTOP=true` |
| 移动端（H5） | `H5` | `HAS_MOBILE=true`、`HAS_H5=true`、`HAS_FRONTEND=true` |
| 移动端（iOS） | `iOS` | `HAS_MOBILE=true`、`HAS_IOS=true` |
| 移动端（Android） | `Android` | `HAS_MOBILE=true`、`HAS_ANDROID=true` |
| 其他 | 用户填写值 | 记录为 `PRODUCT_FORMS_OTHER`，相关能力标记 `待确认` |

`ADMIN_CONSOLE_INCLUDED=包含` 时，派生 `HAS_WEB_ADMIN=true`、`HAS_FRONTEND=true`，并把“管理后台”写入产品能力摘要；它不替代用户在产品形态中对 Web 端的选择。

### 对象存储与媒体派生

- `OBJECT_STORAGE_TYPES=[无]`：`OBJECT_STORAGE_ENABLED=false`、`UPLOAD_ENABLED=false`、`MEDIA_ENABLED=false`、`OBJECT_STORAGE_STACK=不适用`。
- 选中任一 `文档/图片/音频/视频/其他`：`OBJECT_STORAGE_ENABLED=true`、`UPLOAD_ENABLED=true`；图片、音频或视频会使 `MEDIA_ENABLED=true`。
- 对象存储供应商、Bucket、Key 规则和上传限制由 AI 作为初始建议派生，明确标注 `待确认`，不单独向用户提问。

### 技术栈与数据库派生

- 默认后端栈派生：`BACKEND_LANGUAGE=Python`、`BACKEND_FRAMEWORK=FastAPI`、`BACKEND_DATA_VALIDATION=Pydantic`、`BACKEND_PACKAGE_MANAGER=uv`、`API_STYLE=REST`。
- 默认前端栈派生：`FRONTEND_FRAMEWORK=React`、`FRONTEND_LANGUAGE=TypeScript`、`STYLE_SYSTEM=TailWind`、`COMPONENT_LIBRARY=Shadcn/UI`、`HTTP_CLIENT=Axios`、`API_CLIENT_GENERATOR=Orval`、`FRONTEND_PACKAGE_MANAGER=pnpm`。
- `DATABASE_STACK` 由 `DB_PRIMARY` 与 `XINCHUANG_DATABASES` 组合生成；若信创数据库包含主库同名项，保留一次并在兼容矩阵中标注“主库兼容目标”。
- `LOCAL_MODEL_INCLUDED=包含` 时：`HAS_ALGORITHM=true`、`AI_OR_ALGORITHM_ENABLED=true`、`MODEL_ASSET_POLICY=models/ 本地模型资产，具体模型待确认`；否则均为 `false` 或 `不适用`。

### Agent 标准化

依照 [agent-tool-mapping.md](agent-tool-mapping.md) 标准化已选工具。`MULTI_AGENT_ENABLED` 在已选标准工具超过一个时为 `true`；`PRIMARY_AGENT_TOOL` 是输出项目的主要入口，命令模板仍以 `agent-tool-mapping.md` 规定的事实源渲染，再同步到其它已选工具目录。

### UI 设计派生

- `UI_DESIGN_INPUT_MODE=上传` 时：`UI_DESIGN_SOURCE_ENABLED=true`，以 `UI_DESIGN_SOURCE_CONTENT` 为唯一设计事实源。
- `UI_DESIGN_INPUT_MODE=手工输入` 时：`UI_DESIGN_SOURCE_ENABLED=false`，由 AI 生成 `UI_STACK`、`DESIGN_SYSTEM_ENABLED`、Token、组件体系、页面结构、响应式、可访问性和视觉验收策略。
- 两种模式都应与 `PRODUCT_FORMS`、`ADMIN_CONSOLE_INCLUDED` 和 `FRONTEND_STACK` 保持一致；无 UI 产品形态但包含管理后台时，仍生成管理后台的 UI 方案。

## 自动派生与固定默认

以下内容不得作为独立问题询问，应从前述输入自动派生，并在“推导配置摘要”中展示：

| 类型 | 变量/配置 | 派生规则 |
|---|---|---|
| 业务定位 | `BUSINESS_DOMAIN`、`OUT_OF_SCOPE`、`DOMAIN_TERMS` | 由产品描述、核心能力、竞品与核心竞争力推导；不确定部分标记 `待确认`。 |
| 基础架构 | `HAS_BACKEND`、`HAS_API_SERVICE`、`API_ENABLED` | 默认启用后端与 REST API，以匹配默认后端栈；选择其它栈时仍保持 API 需求，框架细节待确认。 |
| 前端能力与 UI | `HAS_FRONTEND`、`HAS_WEB`、`HAS_WECHAT_MINIAPP`、`HAS_MOBILE`、`HAS_DESKTOP`、`UI_STACK`、`DESIGN_SYSTEM_ENABLED` | 由产品形态、管理后台与 UI 设计输入分支派生。 |
| Agent | `MULTI_AGENT_ENABLED`、`AGENT_COMMAND_SYNC_POLICY` | 由已选工具派生；以主 Agent 的命令语义为事实源，向其它已选工具同步。 |
| 固定目录 | `REQ_ROOT_DIR`、`BUG_ROOT_DIR`、`SPRINT_ROOT_DIR`、`CHANGE_ROOT_DIR`、`SPEC_ROOT_DIR`、`TEST_ROOT_DIR` | 固定为 `issues/requirements`、`issues/bugs`、`iterations`、`openspec/changes`、`openspec/specs`、`tests`。 |
| 治理与验证 | OpenSpec、需求、Bug、Sprint、项目基线、文档和测试治理 | 默认启用；验证命令由已选技术栈生成。 |
| 部署 | `DEPLOYMENT_STACK`、`DOCKER_COMPOSE_ENABLED` | 默认 `docker-compose` 与本地开发；生产配置标记 `待确认`。 |

## 推导配置摘要

完成第 16 步后，先输出以下摘要供用户确认或修正，再生成工程：

1. 产品定位：产品名称、产品编号、用户群体、解决问题、核心能力、竞品、核心竞争力。
2. 产品范围：产品形态、管理后台、对象存储类型、本地模型。
3. 技术方案：后端、前端、主关系型数据库、信创数据库及其自动派生配置。
4. Agent：已启用工具、主 Agent、命令同步策略。
5. UI 设计：输入方式；上传模式展示严格遵循的文档来源，手工模式展示 AI 推导的设计方案摘要。
6. AI 推导项与所有 `待确认` 项。

用户未回复摘要时，按已收集的 16 项与摘要中的自动派生值继续生成；不得凭空新增业务需求。

## 未决策项处理

生成工程时按交付价值处理未知信息：

| 类型 | 处理方式 |
|---|---|
| 阻塞运行或治理 | 写入 `docs/pending-decisions.md`，说明影响、建议默认值、决策时机 |
| 后续需求细节 | 不在长期文档中铺占位，后续通过 `issues/requirements/` 补充 |
| 未启用能力 | 删除对应章节、文档、目录、配置或强制规则 |
| 配置值、路径、命令、布尔值 | 不允许写 `待确认`；应给出安全默认、删除字段或集中到 pending decisions |

最终交付文档不得保留 `[通用]`、`[个性化]`、`[条件启用]`、生成参数、初始化生成建议、模块标记说明或模板元信息。打包前必须运行 `python scripts/validate-generated-docs.py --strict`。
