---
purpose: 语言、命名与术语规范
content: AI 输出语言、文档语言、代码命名、API 字段、数据库字段、Git 命名、OpenSpec 命名、术语表和多语言策略
scope: 所有文档、代码、接口、数据库、测试、提交信息、评审与 AI 回复
source: Harness language.md 抽象模板，基于多个项目实践沉淀
update_method: 项目初始化时由用户输入参数生成；修改语言策略、命名约定、术语表或新增技术栈时更新
note: 适用于 {PRODUCT_NAME} 项目；AI 输出和工程命名必须遵守本文档
template_scope: 可作为工程初始化时的 rules/language.md 模块
---

# 语言与命名规范

> 模块标记说明：
>
> - **[通用]**：适用于大多数 Harness 工程，初始化时默认保留。
> - **[个性化]**：必须根据用户项目输入生成，不能直接沿用模板默认值。
> - **[条件启用]**：只有项目具备对应能力时才保留或展开，例如前端、移动端、数据库、国际化、多语言文档。

## 0. 规则定位 [通用]

`rules/language.md` 约束项目中的自然语言、代码标识符、文件命名、接口字段、数据库字段、Git 分支、OpenSpec Change 和术语表。

AI Agent 在以下场景必须读取本文件：

- 新增或修改文档。
- 新增或修改代码、测试、脚本。
- 新增 API、数据库表、字段、枚举。
- 新增目录、文件、OpenSpec Change、Git 分支或提交信息。
- 生成用户可见文案、错误信息、表单字段、页面标题。
- 涉及国际化、多语言或中英文术语统一。

初始化生成本文件时，必须用用户输入替换占位符；缺失信息可以标记为 `待确认`，不得编造品牌术语、业务名词或国际化范围。

常用占位符：

| 占位符 | 含义 | 归属 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品或项目名称 | [个性化] |
| `{PRIMARY_LANGUAGE}` | 默认自然语言，推荐中文 | [个性化] |
| `{SECONDARY_LANGUAGE}` | 第二语言，如英文 | [条件启用] |
| `{CODE_IDENTIFIER_LANGUAGE}` | 代码标识符语言，推荐英文 | [通用] |
| `{API_FIELD_CASE}` | API 字段命名风格，如 snake_case、camelCase | [个性化] |
| `{DATABASE_FIELD_CASE}` | 数据库字段命名风格，推荐 snake_case | [个性化] |
| `{BACKEND_LANGUAGE}` | 后端语言与框架 | [个性化] |
| `{FRONTEND_LANGUAGE}` | 前端语言与框架 | [条件启用] |
| `{I18N_STRATEGY}` | 国际化策略 | [条件启用] |
| `{DOMAIN_TERMS}` | 业务术语表 | [个性化] |

## 1. 总体语言策略 [通用 + 个性化]

默认策略：

```text
自然语言：{PRIMARY_LANGUAGE}
代码标识符：{CODE_IDENTIFIER_LANGUAGE}
API 字段：{API_FIELD_CASE}
数据库字段：{DATABASE_FIELD_CASE}
```

通用要求：

- AI 回复默认使用 `{PRIMARY_LANGUAGE}`，除非用户明确要求其他语言。
- 产品、需求、设计、测试、部署、评审文档默认使用 `{PRIMARY_LANGUAGE}`。
- 代码标识符默认使用英文，不使用拼音和中英文混写。
- 用户可见文案必须与产品语言策略一致。
- 同一个概念在文档、代码、API、数据库和 UI 中应使用同一术语。
- 不确定术语翻译时，先查术语表；术语表缺失时标记 `待确认`。

## 2. AI 输出语言 [通用]

AI 回复规则：

- 默认使用中文。
- 技术名词、命令、路径、代码标识符保持原文。
- 解释代码时可以中英文术语并列，但不得频繁切换语言造成歧义。
- 面向用户的最终回复应说明修改文件、修改原因、验证结果和剩余风险。
- 评审、风险、错误、阻塞问题应使用明确措辞，不使用模糊口号。

特殊场景：

| 场景 | 语言要求 |
|---|---|
| 用户明确要求英文 | 使用英文回复 |
| 生成代码 | 标识符英文，注释遵循项目既有风格 |
| 生成 CLI 命令 | 命令和参数保持原文 |
| 生成用户界面文案 | 使用产品目标用户语言 |
| 生成对外 API 文档 | 按项目 API 文档语言策略 |

## 3. 文档语言与命名 [通用 + 个性化]

文档正文默认使用 `{PRIMARY_LANGUAGE}`。

Markdown 文件命名推荐：

| 文档类型 | 命名规范 | 示例 |
|---|---|---|
| 需求文档 | 固定文件名 | `requirement.md`、`acceptance.md` |
| BUG 文档 | 固定文件名 | `bug.md`、`root-cause.md` |
| 通用规范 | kebab-case | `api-governance.md` |
| 架构文档 | kebab-case 或项目约定中文名 | `system-overview.md`、`技术方案设计.md` |
| ADR | 编号 + kebab-case | `ADR-0001-use-openapi-client.md` |
| 计划文档 | 日期 + kebab-case | `2026-06-16-api-refactor-plan.md` |
| 报告文档 | 日期或主题 + kebab-case | `2026-06-16-verification-report.md` |

文档标题要求：

- 标题应表达对象和目的，避免空泛标题。
- 长期文档必须有元数据头部，除非项目明确不使用。
- 文档中引用路径、命令、字段、表名、接口必须用代码样式。
- 同一目录下文件命名风格必须统一。

## 4. 代码标识符语言 [通用]

代码标识符必须使用英文：

- 变量名、函数名、类名、接口名、类型名使用英文。
- 文件名、目录名使用英文，除非文档目录明确允许中文文档名。
- 不使用拼音命名。
- 不使用无意义缩写，如 `tmp1`、`data2`、`foo`、`bar`，除非是局部示例或测试占位。
- 缩写必须稳定，例如 `API`、`URL`、`ID`、`HTTP`，并遵守语言生态的大小写习惯。

布尔命名推荐：

```text
is_active
has_permission
can_upload
should_retry
enable_cache
```

集合命名推荐使用复数：

```text
users
meeting_items
selected_ids
```

## 5. 后端命名规范 [条件启用]

后端技术栈：

```text
{BACKEND_LANGUAGE}
```

通用后端命名：

| 类型 | 规范 | 示例 |
|---|---|---|
| 文件 | snake_case 或语言生态约定 | `user_service.py` |
| 类名 | PascalCase | `UserService` |
| 函数/方法 | snake_case 或语言生态约定 | `get_user()` |
| 变量 | snake_case 或语言生态约定 | `user_id` |
| 常量 | UPPER_SNAKE_CASE | `MAX_UPLOAD_SIZE` |
| 私有成员 | 语言生态约定 | `_build_query()` |
| 枚举类 | PascalCase | `UserStatus` |
| 枚举成员 | UPPER_SNAKE_CASE | `UserStatus.ACTIVE` |

如果后端不是 Python，应在初始化时替换为对应生态：

| 语言/生态 | 函数变量 | 类/类型 | 文件 |
|---|---|---|---|
| Python | snake_case | PascalCase | snake_case.py |
| Java/Kotlin | camelCase | PascalCase | PascalCase 或包约定 |
| Go | camelCase/PascalCase | PascalCase | snake_case.go 或 lowercase.go |
| Node/TypeScript | camelCase | PascalCase | kebab-case 或 camelCase |

## 6. 前端命名规范 [条件启用]

前端技术栈：

```text
{FRONTEND_LANGUAGE}
```

常见前端命名：

| 类型 | 规范 | 示例 |
|---|---|---|
| 组件名 | PascalCase | `UserList` |
| 组件文件 | PascalCase 或路由生态约定 | `UserList.tsx`、`page.tsx` |
| 工具文件 | camelCase 或 kebab-case | `formatDate.ts`、`api-client.ts` |
| 函数 | camelCase | `getUser()` |
| 变量 | camelCase | `userId` |
| 常量 | UPPER_SNAKE_CASE | `MAX_FILE_SIZE` |
| 类型/接口 | PascalCase | `UserDetail`、`ApiResponse` |
| Hook | `use` 前缀 + PascalCase | `useUserList` |
| Store | 语义名 + `Store` | `authStore`、`userStore` |
| CSS class | kebab-case 或框架约定 | `user-card` |

UI 文案要求：

- 用户可见文案使用产品目标语言。
- 错误提示应说明用户可理解的处理方式。
- 按钮文案使用动作动词，避免含糊词。
- 表单 label、placeholder、help text 的术语必须一致。

## 7. API 与数据库命名 [通用 + 个性化]

API 字段命名：

```text
{API_FIELD_CASE}
```

数据库字段命名：

```text
{DATABASE_FIELD_CASE}
```

推荐规范：

| 对象 | 规范 | 示例 |
|---|---|---|
| API 路径 | kebab-case，资源复数 | `/api/v1/user-profiles` |
| Path 参数 | snake_case | `{user_id}` |
| Query 参数 | snake_case 或项目约定 | `page_size` |
| JSON 字段 | `{API_FIELD_CASE}` | `created_at` 或 `createdAt` |
| 数据库表 | snake_case，复数或领域约定 | `users`、`audit_logs` |
| 数据库字段 | snake_case | `created_at` |
| 索引 | `idx_<table>_<fields>` | `idx_users_email` |
| 唯一约束 | `uq_<table>_<fields>` | `uq_users_email` |
| 外键 | `fk_<from>_<to>` | `fk_orders_users` |

同一项目中 API 字段风格必须统一。若前端使用 camelCase、后端/数据库使用 snake_case，必须在序列化层明确转换，不得在业务代码中混用。

## 8. 测试命名 [通用]

测试命名应表达被测对象、场景和预期结果。

推荐：

| 类型 | 规范 | 示例 |
|---|---|---|
| Python 测试文件 | `test_<subject>.py` | `test_user_api.py` |
| JS/TS 测试文件 | `<subject>.test.ts` | `user-service.test.ts` |
| 测试函数 | `test_<scenario>_<expected>` | `test_invalid_token_returns_401` |
| fixture | 语义化英文 | `admin_user`、`sample_file` |
| E2E 用例 | 用户行为命名 | `user_can_create_order` |

不要使用只有序号的测试名，例如 `test_case_1`。

## 9. Git 命名 [通用 + 个性化]

分支命名推荐：

| 类型 | 规范 | 示例 |
|---|---|---|
| 功能 | `feat/<short-name>` | `feat/add-user-login` |
| 修复 | `fix/<short-name>` | `fix/upload-timeout` |
| 文档 | `docs/<short-name>` | `docs/update-api-guide` |
| 重构 | `refactor/<short-name>` | `refactor/user-service` |
| 测试 | `test/<short-name>` | `test/add-api-contract-tests` |
| 工程 | `chore/<short-name>` | `chore/update-ci` |

提交信息语言：

```text
{COMMIT_MESSAGE_LANGUAGE}
```

如果项目无明确约定，提交信息可使用中文说明意图，类型前缀使用英文 conventional commits：

```text
docs: 抽象 API 规则模板
fix: 修复上传接口超时
feat: 新增用户登录
```

## 10. OpenSpec 与需求命名 [通用]

OpenSpec Change 命名：

| 场景 | 前缀 | 示例 |
|---|---|---|
| 新能力 | `add-*` | `add-user-login` |
| BUG 修复 | `fix-*` | `fix-upload-timeout` |
| 更新/对齐 | `update-*` | `update-api-error-format` |
| 重构 | `refactor-*` | `refactor-auth-service` |
| 移除 | `remove-*` | `remove-legacy-export` |

需求和 BUG 命名：

```text
REQ-0001-user-login
BUG-0001-upload-timeout
```

规则：

- ID 使用大写前缀和四位数字。
- slug 使用英文 kebab-case。
- slug 应描述业务目标或问题，不写实现细节。

## 11. 术语表 [个性化]

初始化时应根据用户输入生成项目术语表。示例：

| 中文术语 | 英文术语 | 代码命名建议 | 说明 |
|---|---|---|---|
| 用户 | User | `user` | 系统使用者 |
| 角色 | Role | `role` | 权限角色 |
| 审计日志 | Audit Log | `audit_log` | 操作审计记录 |

项目术语：

```text
{DOMAIN_TERMS}
```

新增核心业务概念时，必须同步更新术语表。不得在不同文件中对同一概念使用多个翻译。

## 12. 国际化与多语言 [条件启用]

国际化策略：

```text
{I18N_STRATEGY}
```

有多语言要求时：

- 用户可见文案不得硬编码在业务逻辑中。
- 文案 key 使用英文、稳定、可搜索的命名。
- 默认语言、回退语言和缺失文案策略必须明确。
- 日期、时间、数字、货币、单位必须按 locale 处理。
- API 返回的机器可读枚举不应直接作为用户文案展示。

无国际化要求时，也应避免把用户文案散落在不可维护的位置。

### 12.1 文档时间格式 `[通用]`

文档中的时间记录统一使用 `YYYY-MM-DD HH:mm:ss`，例如 `2026-06-25 14:30:05`。

规则：

- 使用 24 小时制，必须包含年、月、日、时、分、秒。
- 适用于 frontmatter、元数据表、trace、review、验收记录、发布记录、审计记录和变更记录。
- 日期型文件名、目录名和归档分组可以使用 `YYYY-MM-DD` 或 `YYYY-MM`。
- 多语言或国际化展示可以按 locale 转换，但源文档记录必须保留完整时间。

## 13. 禁止事项 [通用]

- 禁止使用拼音命名代码标识符。
- 禁止同一概念多套英文翻译。
- 禁止在 API 字段中混用 snake_case 和 camelCase，除非有明确转换层。
- 禁止随意缩写业务术语。
- 禁止在文档时间记录中只写到日期、小时或分钟，除非该字段明确是文件名、目录名或归档分组。
- 禁止测试名、变量名只用 `a`、`b`、`data`、`temp` 等无语义词。
- 禁止把内部错误、堆栈、数据库字段直接暴露为用户文案。
- 禁止在文档标题和文件名中使用无法搜索的泛化词，例如 `new.md`、`misc.md`。

## 14. 完成任务后检查清单 [通用 + 条件启用]

```text
□ 是否遵守默认输出语言
□ 文档正文是否使用项目默认自然语言
□ 代码标识符是否使用英文且有语义
□ 文件、目录、类、函数、变量命名是否符合技术栈约定
□ API 路径、字段、参数是否符合命名风格
□ 数据库表、字段、索引、约束是否符合命名风格
□ 用户可见文案是否与产品语言策略一致
□ 文档时间记录是否统一到 YYYY-MM-DD HH:mm:ss
□ 新增业务概念是否更新术语表
□ OpenSpec Change、REQ、BUG 命名是否符合规范
□ 多语言项目是否更新 i18n 文案和回退策略
```

## 15. 初始化生成建议 [通用]

工程初始化工具生成 `rules/language.md` 时应：

1. 保留 [通用] 模块。
2. 用用户输入替换 [个性化] 占位符。
3. 根据技术栈保留或删除 [条件启用] 模块。
4. 根据后端、前端、移动端、数据库技术栈生成对应命名规范。
5. 根据用户输入的业务领域生成初始术语表。
6. 明确 API 字段和数据库字段命名风格。
7. 未知项标记为 `待确认`。
