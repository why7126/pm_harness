---
purpose: 前端测试标准
content: 前端测试栈、测试分层、组件测试、页面测试、交互测试、API Mock、可访问性、视觉回归、E2E 分工、运行命令与维护规则
source: Harness docs/standards/frontend-test-standard.md 抽象模板，初始化时基于用户输入生成
update_method: 前端技术栈、测试框架、目录结构、组件体系、关键流程或质量门禁变化时同步更新
owner: {FRONTEND_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；无前端项目可保留为未来启用规范并标记不适用
---

# 前端测试标准

## 0. 文档定位 `[通用]`

本文档定义项目的前端测试标准，覆盖测试栈、测试分层、组件测试、页面测试、表单与交互、状态管理、API Mock、可访问性、视觉回归、E2E 分工、运行命令、CI 门禁和 AI 修改规则。

本文档是 `rules/testing.md` 中前端测试章节的落地细则，应与 `docs/standards/testing-governance.md`、`docs/standards/unit-test-standard.md`、`docs/standards/test-coverage.md`、`rules/ui-design.md` 保持一致。

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{FRONTEND_OWNER}` | 前端负责人 | 待确认 |
| `{FRONTEND_ENABLED}` | 是否启用前端 | true / false |
| `{FRONTEND_STACK}` | 前端技术栈 | React / Vue / Svelte / Angular / WeChat Miniapp / Flutter Web / none |
| `{FRONTEND_TEST_STACK}` | 前端测试工具 | Vitest / Jest / Testing Library / Cypress CT / Playwright CT / none |
| `{E2E_TEST_STACK}` | E2E 测试工具 | Playwright / Cypress / WebdriverIO / none |
| `{FRONTEND_SOURCE_DIR}` | 前端源码目录 | `src/web` / 待确认 |
| `{FRONTEND_TEST_FILE_PATTERN}` | 测试文件匹配 | 待确认 |
| `{FRONTEND_TEST_COMMAND}` | 前端测试命令 | 待确认 |
| `{FRONTEND_CHECK_COMMAND}` | 类型检查/Lint/格式命令 | 待确认 |
| `{FRONTEND_COVERAGE_COMMAND}` | 前端覆盖率命令 | 待确认 |
| `{FRONTEND_COVERAGE_TARGET}` | 前端覆盖率目标 | 待确认 |
| `{DESIGN_SYSTEM_ENABLED}` | 是否启用 Design System | true / false |
| `{DESIGN_SYSTEM_COMPONENT_PATH}` | 组件库路径 | 待确认 |
| `{API_MOCK_STRATEGY}` | API Mock 策略 | MSW / mock adapter / fake client / none |
| `{VISUAL_TEST_STRATEGY}` | 视觉测试策略 | screenshot / storybook / manual / none |
| `{A11Y_TEST_STRATEGY}` | 可访问性测试策略 | automated / checklist / none |

## 2. 启用条件 `[通用]`

满足以下任一条件时，应完整启用本文档：

- 项目包含 Web、管理后台、H5、桌面端、微信小程序、移动 Web 或可视化界面。
- 项目存在可复用组件、页面、表单、交互流程、状态管理或前端 API Client。
- 项目需要 Design System、视觉验收、可访问性、响应式或浏览器兼容测试。
- 项目存在登录、权限、上传、媒体播放、导入导出、复杂表单或关键业务流程。

当 `{FRONTEND_ENABLED}=false` 且项目无前端界面时，可保留本文档为未来启用规范，并删除强制测试命令、目录、组件测试和 E2E 要求。

## 3. 测试总原则 `[通用]`

| 原则 | 说明 |
|---|---|
| 用户行为优先 | 测试应验证用户可观察行为，而不是组件内部实现细节 |
| 分层清晰 | 组件测试验证局部交互，页面测试验证状态组合，E2E 验证关键流程 |
| Mock 边界明确 | 单元/组件测试 Mock 网络层，E2E 使用真实或受控后端 |
| 状态覆盖完整 | 加载、空态、错误、权限不足、禁用、成功反馈必须按场景覆盖 |
| 可维护 | 测试选择器、Fixture、Mock 数据和断言应稳定、可读 |
| 不掩盖缺陷 | 不得用跳过测试、降低断言、隐藏错误日志替代修复 |
| 与设计一致 | 组件 variant、响应式、可访问性和视觉状态必须与 UI 规范一致 |

## 4. 测试栈 `[通用 + 个性化]`

当前前端技术栈：

```text
{FRONTEND_STACK}
```

当前前端测试栈：

```text
{FRONTEND_TEST_STACK}
```

当前 E2E 测试栈：

```text
{E2E_TEST_STACK}
```

生成规则：

- React 项目可使用 Vitest/Jest + Testing Library，也可使用 Playwright/Cypress 组件测试。
- Vue 项目可使用 Vitest/Jest + Vue Test Utils，也可使用 Playwright/Cypress 组件测试。
- Svelte、Angular、微信小程序、桌面端或移动 Web 应使用对应生态测试工具。
- 当前项目未配置前端测试框架时，应标记为 `待确认`，不得编造命令。
- 不存在前端时，应删除强制前端测试要求，仅保留未来启用说明。

## 5. 目录与命名 `[通用 + 个性化]`

前端源码目录：

```text
{FRONTEND_SOURCE_DIR}
```

测试文件匹配：

```text
{FRONTEND_TEST_FILE_PATTERN}
```

推荐约定：

| 类型 | 推荐位置 | 说明 |
|---|---|---|
| 组件测试 | 与组件就近或 `tests/unit/frontend/` | 验证组件渲染、交互和状态 |
| 页面测试 | 页面目录就近或 `tests/integration/frontend/` | 验证页面组合、路由、数据状态 |
| Hook/Store 测试 | 逻辑模块就近 | 验证状态管理和副作用 |
| API Client 测试 | services/api 目录就近 | 验证请求构造、错误处理、类型转换 |
| E2E 测试 | `tests/e2e/` | 验证跨页面关键流程 |
| Fixture/Mock | `tests/fixtures/` 或前端测试目录 | 存放稳定测试数据 |

要求：

- 测试文件命名必须与项目测试框架匹配。
- 测试目录不得混入生产构建产物、大体积截图或真实用户数据。
- 共享 Fixture 应表达业务语义，不得复制来源项目业务对象。

## 6. 必须覆盖的前端场景 `[通用]`

前端新增或修改功能时，至少评估以下测试：

- 渲染：正常渲染、空态、加载态、错误态。
- 交互：点击、输入、选择、拖拽、上传、键盘操作。
- 表单：必填、格式、边界值、禁用状态、提交成功、提交失败。
- 状态：本地状态、全局状态、缓存、URL query、路由参数。
- 权限：未登录、权限不足、角色差异、只读状态。
- API：成功响应、业务错误、参数错误、401、403、超时、重试。
- 可访问性：label、焦点、键盘导航、语义角色、错误提示关联。
- 响应式：移动端、桌面端、窄屏、长文本、溢出。
- 视觉：Design Token、组件 variant、主题、暗色模式、截图基线。

## 7. 组件测试 `[通用 + 条件启用]`

当项目存在可复用组件、业务组件或 Design System 时启用。

组件测试必须覆盖：

- 基础渲染不抛错。
- 关键 props、variant、size、disabled、loading、error 等状态。
- 用户事件触发回调、状态变化和可见反馈。
- 表单组件的 label、value、error、helper text、aria 属性。
- 组件组合时的插槽、children、受控/非受控行为。

禁止：

- 仅写无断言的 smoke 测试长期保留。
- 断言组件内部私有状态、私有 DOM 结构或框架实现细节。
- 为了测试方便修改生产组件可访问性或业务行为。

## 8. 页面与流程测试 `[通用 + 条件启用]`

当项目存在页面、路由、导航、登录态或复杂业务流程时启用。

页面测试应覆盖：

- 路由参数、URL query、默认状态和返回路径。
- 数据加载成功、加载中、失败、空结果。
- 用户提交、保存、删除、取消、确认等关键操作。
- 401、403、业务错误、网络错误的展示与恢复。
- 权限差异导致的按钮、菜单、字段可见性或禁用状态。

页面级测试不应完全替代 E2E。跨页面、真实浏览器、真实登录和关键业务闭环应交给 E2E。

## 9. API Mock 与数据策略 `[通用 + 个性化]`

API Mock 策略：

```text
{API_MOCK_STRATEGY}
```

要求：

- 组件和页面测试默认 Mock 网络层，不依赖真实后端服务。
- Mock 响应必须匹配真实 API 契约、字段命名、错误码和分页结构。
- 错误场景 Mock 必须覆盖 401、403、参数错误、业务错误和外部依赖失败。
- 前端 API Client 变更时必须同步测试 Mock、OpenAPI 生成类型和错误处理。
- 禁止在前端测试中使用真实生产账号、真实 Token、真实接口地址或生产数据。

## 10. Design System 测试 `[条件启用 + 个性化]`

当 `{DESIGN_SYSTEM_ENABLED}=true` 时启用。

组件库路径：

```text
{DESIGN_SYSTEM_COMPONENT_PATH}
```

必须覆盖：

- 基础组件的 smoke、variant、size、状态、可访问性。
- 组合组件的交互、焦点、键盘行为、错误展示。
- Design Token 变化对组件样式和主题的影响。
- 重要组件的视觉基线或人工验收清单。

要求：

- Design System 测试必须与 `rules/ui-design.md` 保持一致。
- 新增组件必须同步添加测试、示例和视觉验收方式。
- 仅覆盖按钮/输入框 smoke 不足以支撑完整组件体系，应随组件增长补齐交互和状态测试。

## 11. 可访问性测试 `[条件启用 + 个性化]`

可访问性策略：

```text
{A11Y_TEST_STRATEGY}
```

建议覆盖：

- 表单控件有 label 或可访问名称。
- 错误提示与输入控件关联。
- 弹窗、下拉、菜单、抽屉有焦点管理和键盘关闭。
- 重要操作可键盘访问。
- 颜色、禁用、错误、成功状态不只依赖颜色表达。

自动化工具无法覆盖所有体验问题，关键页面仍应保留人工检查清单。

## 12. 视觉回归与响应式 `[条件启用 + 个性化]`

视觉测试策略：

```text
{VISUAL_TEST_STRATEGY}
```

启用条件：

- 项目有 Design System、主题、暗色模式、复杂布局、图表、媒体展示或高视觉一致性要求。
- UI 变更容易造成回归，且截图基线维护成本可接受。

要求：

- 截图基线必须稳定，避免依赖当前时间、随机数据、动画、网络图片。
- 响应式测试至少覆盖项目支持的主要断点。
- 视觉变化必须与设计变更、需求或验收记录关联。
- 不启用自动截图时，应生成手工视觉验收清单。

## 13. 与 E2E 的分工 `[通用 + 个性化]`

E2E 测试栈：

```text
{E2E_TEST_STACK}
```

分工原则：

| 层级 | 负责内容 | 不负责内容 |
|---|---|---|
| 组件测试 | 单组件渲染、状态、交互、可访问性 | 跨页面真实流程 |
| 页面测试 | 页面组合、路由参数、Mock API 状态 | 多服务真实联调 |
| E2E | 登录、关键业务闭环、真实浏览器兼容 | 所有边界条件穷举 |
| 手工验收 | 主观视觉、复杂设备、低频兼容 | 可稳定自动化的回归 |

要求：

- 关键用户路径必须有 E2E 或人工验收步骤。
- E2E 不应覆盖所有组件分支，组件级边界应留给组件测试。
- E2E 失败若暴露组件缺陷，应补充组件或页面测试防回归。

## 14. 运行命令与 CI `[通用 + 个性化]`

前端测试命令：

```bash
{FRONTEND_TEST_COMMAND}
```

前端检查命令：

```bash
{FRONTEND_CHECK_COMMAND}
```

覆盖率命令：

```bash
{FRONTEND_COVERAGE_COMMAND}
```

覆盖率目标：

```text
{FRONTEND_COVERAGE_TARGET}
```

要求：

- 命令必须来自实际 `package.json`、脚本或 CI 配置；未知时标记 `待确认`。
- CI 至少应运行类型检查、Lint、单元/组件测试或项目明确的等价检查。
- 覆盖率下降、测试跳过、截图基线大面积更新必须人工确认。
- 前端测试命令应与 `rules/testing.md`、`docs/standards/test-coverage.md` 保持一致。

## 15. AI 修改规则 `[通用]`

AI 修改前端代码、组件、页面或交互时必须同步检查：

```text
rules/testing.md
rules/ui-design.md
docs/standards/frontend-test-standard.md
docs/standards/testing-governance.md
docs/standards/test-coverage.md
docs/standards/unit-test-standard.md
tests/e2e/
```

要求：

- 不得只改 UI 或交互而不评估测试。
- 不得删除断言、跳过测试或降低覆盖率来通过 CI。
- 不得保留来源项目测试框架、路径、组件名、命令或 Design System 假设。
- 不得让组件测试依赖真实后端、真实账号、真实对象存储或生产数据。
- 新增 Design System 组件、表单、权限状态、上传、媒体、登录态必须补充测试或验收说明。

## 16. 初始化生成建议 `[通用]`

初始化生成本文档时应执行：

1. 根据用户输入替换 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{FRONTEND_ENABLED}`、`{FRONTEND_STACK}`、`{FRONTEND_TEST_STACK}`、`{E2E_TEST_STACK}`、`{FRONTEND_SOURCE_DIR}`、`{FRONTEND_TEST_COMMAND}`。
2. 保留所有 `[通用]` 模块。
3. 根据项目能力保留或删除 `[条件启用]` 模块，例如 Design System、可访问性、视觉回归、E2E、上传、媒体、登录态、移动端/微信小程序。
4. 用真实测试框架、目录、命令、组件路径、Mock 策略和覆盖率目标替换占位；未知信息标记为 `待确认`。
5. 不得编造测试命令、测试框架、组件路径或覆盖率目标。
6. 保持本文档与 `rules/testing.md`、`rules/ui-design.md`、`docs/standards/testing-governance.md`、`docs/standards/test-coverage.md` 一致。

## 17. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- 前端框架、测试框架、构建工具、目录结构或运行命令变化。
- 新增 Design System、组件库、主题、视觉回归或可访问性策略。
- 新增登录态、权限、上传、媒体、复杂表单、图表或关键用户流程。
- E2E 分工、CI 门禁、覆盖率目标或测试数据策略变化。
