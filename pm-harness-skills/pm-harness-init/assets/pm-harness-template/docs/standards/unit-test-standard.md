---
purpose: 单元测试标准
content: 单元测试范围、目录命名、断言质量、Mock 边界、测试数据、覆盖要求、AI 补测规则与维护规范
source: Harness docs/standards/unit-test-standard.md 抽象模板，初始化时基于用户输入生成
update_method: 单元测试框架、代码分层、测试目录、覆盖率目标或质量门禁变化时同步更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {QA_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；本文档聚焦单元测试，测试治理总纲见 testing-governance
---

# 单元测试标准

## 0. 文档定位 `[通用]`

本文档定义项目单元测试标准，覆盖测试范围、目录命名、断言质量、Mock 边界、测试数据、覆盖要求、AI 补测规则、CI 门禁和维护规则。

本文档是 `docs/standards/testing-governance.md` 的专项细则，应与 `docs/standards/test-coverage.md`、`docs/standards/frontend-test-standard.md`、`rules/testing.md` 和 CI 配置保持一致。

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{QA_OWNER}` | 测试/质量负责人 | 待确认 |
| `{BACKEND_STACK}` | 后端技术栈 | 待确认 |
| `{FRONTEND_STACK}` | 前端技术栈 | 待确认 |
| `{UNIT_TEST_FRAMEWORK}` | 单元测试框架 | pytest / unittest / vitest / jest / go test / junit |
| `{UNIT_TEST_COMMAND}` | 单元测试命令 | 待确认 |
| `{UNIT_TEST_PATHS}` | 单元测试目录 | 待确认 |
| `{UNIT_TEST_FILE_PATTERN}` | 测试文件命名模式 | 待确认 |
| `{SOURCE_LAYERING}` | 代码分层 | API / Service / Repository / Domain / UI / Shared |
| `{MOCK_STRATEGY}` | Mock 策略 | 待确认 |
| `{FIXTURE_STRATEGY}` | Fixture/Factory 策略 | 待确认 |
| `{UNIT_COVERAGE_TARGET}` | 单元测试覆盖率目标 | 待确认 |
| `{CI_UNIT_TEST_GATE}` | CI 单元测试门禁 | required / warning / disabled |

## 2. 启用条件 `[通用]`

满足以下任一条件时，应启用本文档：

- 项目包含可独立验证的函数、类、组件、Service、Domain、Repository、工具函数、SDK 或脚本。
- 项目需要在 PR 或 OpenSpec Change 中快速验证行为变化。
- 项目存在权限、安全、数据处理、计算逻辑、错误码、外部服务适配或状态转换。
- 项目需要覆盖率统计、质量门禁或回归测试。

当项目暂未具备自动化单元测试条件时，应保留本文档并标记 `{UNIT_TEST_FRAMEWORK}=待确认`，同时记录未来启用条件。

## 3. 单元测试原则 `[通用]`

| 原则 | 说明 |
|---|---|
| 测行为 | 测试公开行为和业务结果，不测试无意义实现细节 |
| 小范围 | 单个测试聚焦一个行为或规则 |
| 可重复 | 测试不依赖执行顺序、系统时间、外部服务或脏数据 |
| 有断言 | 每个测试必须有明确断言，不保留空 smoke |
| 可读性 | 测试名表达场景、条件和期望结果 |
| 快速反馈 | 单元测试应适合本地和 PR 高频运行 |
| 隔离依赖 | 网络、文件系统、数据库、时间、随机数、第三方服务需可控 |

## 4. 必须覆盖的对象 `[通用 + 个性化]`

根据 `{SOURCE_LAYERING}` 生成具体覆盖对象：

| 对象 | 必须测试 | 条件 |
|---|---|---|
| Domain / 业务规则 | 状态流转、边界、非法输入、权限规则 | 有业务规则时启用 |
| Service / Use Case | 编排逻辑、失败分支、事务边界、外部依赖异常 | 有服务层时启用 |
| Repository / DAO | 查询条件、分页排序、数据映射、空结果、异常 | 有数据访问层时启用 |
| API Adapter / Controller | 参数解析、调用边界、错误映射 | 条件启用，核心逻辑仍应下沉测试 |
| Utility / Helper | 格式化、转换、校验、计算、解析 | 有工具函数时启用 |
| Error Codes / Constants | 错误码映射、枚举兼容、用户提示 | 有统一错误码时启用 |
| SDK / Client | 请求构造、响应解析、重试、错误转换 | 有 SDK 或客户端时启用 |
| CLI / Scripts | 参数校验、幂等性、失败路径、输出结果 | 有脚本工具时启用 |
| UI 纯逻辑 | 状态 reducer、表单校验、数据转换 | 有前端业务逻辑时启用 |

禁止只测试薄 Router/Controller 而不测试实际业务逻辑。

## 5. 测试场景要求 `[通用]`

每个重要函数、方法、组件逻辑或业务规则至少考虑：

- 正常路径：输入合法，返回符合预期。
- 异常路径：输入非法、依赖失败、权限不足、资源不存在。
- 边界条件：空值、零值、最大/最小值、重复数据、临界状态。
- 幂等场景：重复调用、重复提交、重试后结果一致。
- 兼容场景：旧字段、默认值、缺失字段、版本差异。
- 安全场景：越权、敏感字段、危险操作、输入污染。

不是每个函数都必须机械补齐所有场景，但高风险逻辑必须说明未覆盖原因。

## 6. 目录与命名 `[通用 + 个性化]`

单元测试目录：

```text
{UNIT_TEST_PATHS}
```

测试文件模式：

```text
{UNIT_TEST_FILE_PATTERN}
```

推荐规则：

| 维度 | 规则 |
|---|---|
| 文件位置 | 可采用集中式 `tests/unit/` 或源码就近测试，必须与项目框架一致 |
| 文件命名 | 测试文件名应能映射被测模块 |
| 测试命名 | 名称应表达“场景 + 条件 + 期望” |
| 分组 | 同一模块测试可按行为、方法或业务场景分组 |
| Fixture | 共享 Fixture 放在明确目录或框架约定位置 |
| 报告产物 | 临时报告、快照、覆盖率产物不得提交 Git |

示例命名风格：

```text
test_<module>_<behavior>_<expected_result>
should_<expected_result>_when_<condition>
<module>.spec.<framework-extension>
```

初始化时必须按实际语言和测试框架改写示例。

## 7. 断言质量 `[通用]`

有效断言必须验证业务结果，而不是只验证代码被执行。

推荐断言：

- 返回值、状态、错误码、异常类型、消息结构。
- 数据库写入、更新、删除、事务回滚或查询条件。
- 调用外部依赖时的参数、次数、错误处理和回退结果。
- 权限判断、资源归属、租户边界和敏感字段过滤。
- 输出结构、序列化结果、兼容字段和默认值。

禁止：

- 无断言测试。
- 只断言对象不为空，但不验证关键字段。
- 只追求覆盖率的空调用。
- 大量快照替代业务断言。
- 测试私有实现导致重构困难。

## 8. Mock 与依赖边界 `[通用 + 个性化]`

Mock 策略：

```text
{MOCK_STRATEGY}
```

规则：

- 外部网络、第三方 API、邮件/短信、支付、对象存储、系统时间、随机数必须可控。
- Mock 应验证关键调用参数和失败分支，不只返回固定成功值。
- 不应 Mock 被测对象本身。
- Repository 测试可使用轻量测试数据库、内存替代或隔离容器，但必须说明与生产数据库差异。
- Service 测试可 Mock Repository 或外部 Gateway，但必须覆盖依赖失败、空结果和权限异常。
- 前端纯逻辑测试可 Mock API Client、Router、Storage、Feature Flag。

## 9. Fixture、Factory 与测试数据 `[通用 + 个性化]`

Fixture 策略：

```text
{FIXTURE_STRATEGY}
```

要求：

- 测试数据应最小化，只包含验证行为所需字段。
- 推荐使用 Factory/Builder 生成默认有效对象，再覆盖场景字段。
- 不得使用生产数据、真实用户信息、密钥或 Token。
- 时间、ID、随机数应可注入或固定。
- 测试数据应能自动清理或隔离，避免影响后续测试。
- 大型 Fixture 必须说明用途，避免变成不可读的隐式依赖。

## 10. 示例模板 `[通用]`

初始化时应按实际语言、框架和业务对象生成示例。以下仅为结构示意：

```text
test: 当 <场景/条件> 时，应 <期望结果>
arrange: 构造最小输入、依赖、权限和初始状态
act: 调用被测公开行为
assert: 验证返回值、状态变化、依赖调用和错误结构
```

示例不应保留来源项目业务对象、类名、表名、路径或命令。

## 11. 覆盖率要求 `[通用 + 个性化]`

单元测试覆盖率目标：

```text
{UNIT_COVERAGE_TARGET}
```

要求：

- 覆盖率目标由 `docs/standards/test-coverage.md` 统一定义。
- 核心业务、权限、安全、数据处理、错误码和 Bug 修复路径应优先补测。
- 覆盖率不足时，应补充有意义断言，而不是写空测试。
- 允许对生成代码、纯类型声明、框架入口等进行合理排除，但必须在覆盖率标准中登记。

## 12. CI 与运行命令 `[通用 + 个性化]`

单元测试命令：

```bash
{UNIT_TEST_COMMAND}
```

CI 单元测试门禁：

```text
{CI_UNIT_TEST_GATE}
```

要求：

- 单元测试应在 PR 或等价合并流程中运行。
- 单元测试失败时不得合并，除非有明确例外审批。
- 命令必须来自实际脚本、测试框架或 CI 配置；未知时标记 `待确认`。
- 单元测试应尽量快速，慢测试、外部依赖测试应归入集成测试或单独标记。

## 13. AI 修改规则 `[通用]`

AI 新增或修改业务代码时必须：

- 为新增行为补充单元测试，或说明为什么不适合单元测试。
- 为 Bug 修复添加复现测试。
- 修改错误码、权限、校验、边界条件时同步补测。
- 修改测试框架、目录、命令或覆盖率目标时同步更新本文档。
- 不得删除失败测试、降低断言质量、扩大跳过范围或保留无意义 smoke。
- 不得保留来源项目业务名、类名、目录、命令、数据库或测试框架假设。

## 14. 与其他测试的边界 `[通用]`

| 测试类型 | 单元测试边界 |
|---|---|
| 集成测试 | 验证多个模块、数据库、对象存储、队列或外部服务真实协作 |
| API 测试 | 验证请求响应、认证授权、错误码、协议兼容 |
| 前端组件测试 | 验证 UI 渲染、交互、状态和可访问性 |
| E2E 测试 | 验证完整用户路径和跨模块流程 |
| 兼容性测试 | 验证浏览器、设备、运行时、部署和数据库矩阵 |

单元测试应尽量将失败定位到小范围逻辑，避免承担完整链路验收职责。

## 15. 初始化生成建议 `[通用]`

初始化生成本文档时应执行：

1. 根据用户输入替换 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{QA_OWNER}`、`{BACKEND_STACK}`、`{FRONTEND_STACK}`、`{UNIT_TEST_FRAMEWORK}`、`{UNIT_TEST_COMMAND}`、`{UNIT_TEST_PATHS}`、`{UNIT_TEST_FILE_PATTERN}`、`{MOCK_STRATEGY}`、`{FIXTURE_STRATEGY}`、`{UNIT_COVERAGE_TARGET}`、`{CI_UNIT_TEST_GATE}`。
2. 根据 SOURCE_LAYERING、BACKEND_STACK、FRONTEND_STACK、HAS_SDK、HAS_ALGORITHM、HAS_SCRIPTS 生成必须覆盖对象。
3. 根据实际语言和测试框架改写目录、命名、示例和命令。
4. 根据项目能力保留或删除 `[条件启用]` 内容，例如 Repository、SDK、CLI、前端纯逻辑、算法、对象存储、数据库。
5. 未确认的信息标记为 `待确认`，不得编造测试框架、命令、目录、覆盖率目标或 CI 门禁。
6. 不得保留来源项目业务类名、测试函数、数据库、目录或技术栈假设。
7. 保持本文档与 `docs/standards/testing-governance.md`、`docs/standards/test-coverage.md`、`rules/testing.md` 一致。

## 16. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- 单元测试框架、命令、目录、命名规则或 CI 门禁变化。
- 后端、前端、SDK、CLI、脚本、算法或共享库分层变化。
- Mock、Fixture、Factory、测试数据库或外部依赖策略变化。
- 覆盖率目标、排除规则或质量门禁变化。
- 新增权限、安全、计费、数据处理、上传、导入导出、外部服务等高风险模块。
