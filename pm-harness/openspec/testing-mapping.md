---
purpose: OpenSpec 测试映射
content: 需求、Bug、OpenSpec Change、验收项、测试用例、验证命令、测试证据和例外审批的追溯关系
source: Harness openspec/testing-mapping.md 抽象模板，初始化时基于用户输入、需求治理、Bug 治理、OpenSpec Change 和测试策略生成
update_method: 新增或调整需求、Bug、Change、验收标准、测试用例、测试命令、CI 门禁或例外审批时同步更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {QA_OWNER}
note: 适用于 {PRODUCT_NAME} 项目；本文档是测试追溯索引，不替代具体测试代码、验收文档或测试报告
---

# OpenSpec 测试映射

## 0. 文档定位 `[通用]`

本文档定义 `{PRODUCT_NAME}` 中需求、Bug、OpenSpec Change、验收项与测试资产之间的追溯关系。

目标：

- 确认每个需求或变更都有对应验证方式。
- 确认每个 Bug 修复都有复现与回归证据。
- 确认 OpenSpec Change 在实现、测试、验收和归档之间可追踪。
- 帮助 AI Agent 判断修改代码时应补充哪些测试与文档。

本文档只登记映射关系，不保存完整测试报告。测试报告、截图、trace、覆盖率产物应按 `rules/testing.md` 和 `docs/standards/testing-governance.md` 管理。

## 1. 生成参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_CODE}` | 项目代码 | 待确认 |
| `{QA_OWNER}` | 测试/质量负责人 | 待确认 |
| `{REQ_ROOT_DIR}` | 需求目录 | `issues/requirements` |
| `{BUG_ROOT_DIR}` | Bug 目录 | `issues/bugs` |
| `{CHANGE_ROOT_DIR}` | OpenSpec Change 目录 | `openspec/changes` |
| `{SPEC_ROOT_DIR}` | OpenSpec Spec 目录 | `openspec/specs` |
| `{TEST_ROOT_DIR}` | 测试目录 | `tests` |
| `{TEST_FRAMEWORKS}` | 测试框架清单 | 待确认 |
| `{TEST_COMMANDS}` | 测试命令清单 | 待确认 |
| `{CI_TEST_GATE}` | CI 测试门禁 | required / warning / disabled |
| `{COVERAGE_GATE}` | 覆盖率门禁 | enforced / warning / disabled |
| `{TRACE_ID_POLICY}` | Trace ID 规则 | 待确认 |
| `{EVIDENCE_STORAGE_POLICY}` | 测试证据保存策略 | 待确认 |

## 2. 追溯对象 `[通用]`

| 对象 | 来源 | 说明 |
|---|---|---|
| Requirement | `{REQ_ROOT_DIR}` | 需求、PRD、用户故事、验收标准 |
| Bug | `{BUG_ROOT_DIR}` | 缺陷记录、复现步骤、根因、修复验收 |
| OpenSpec Change | `{CHANGE_ROOT_DIR}` | 变更 proposal、design、tasks、spec delta |
| OpenSpec Spec | `{SPEC_ROOT_DIR}` | 已归档的正式能力规格 |
| Acceptance Criteria | 需求、Bug 或 Change | 可验证的验收项 |
| Test Case | `{TEST_ROOT_DIR}` 或源码就近测试 | 自动化测试、人工验收、脚本校验 |
| Evidence | CI、测试报告、截图、日志、trace | 验证证据，不一定提交仓库 |

## 3. 映射总原则 `[通用]`

- 每个进入实现的需求必须至少有一个验收项和一种验证方式。
- 每个 Bug 修复必须有复现路径、修复验证和回归测试或例外说明。
- 每个 OpenSpec Change 必须在归档前记录测试覆盖情况。
- 高风险变更必须覆盖单元、集成、API、E2E、安全或兼容性中的必要组合。
- 自动化测试优先；无法自动化时必须登记人工验收步骤和证据。
- 测试映射必须能从需求或 Change 反查到测试，也能从测试反查到业务原因。

## 4. 映射记录格式 `[通用 + 个性化]`

推荐使用以下结构登记映射：

```yaml
{TRACE_ID}:
  type: requirement | bug | change | sprint | manual
  source: "{SOURCE_PATH_OR_URL}"
  change: "{CHANGE_ID_OR_NOT_APPLICABLE}"
  specs:
    - "{SPEC_MODULE}"
  acceptance:
    - id: "{AC_ID}"
      description: "{AC_DESCRIPTION}"
      verify_by:
        - unit
        - integration
        - api
        - frontend
        - e2e
        - compatibility
        - security
        - manual
  tests:
    - id: "{TEST_ID}"
      type: unit | integration | api | frontend | e2e | compatibility | security | script | manual
      path: "{TEST_PATH_OR_COMMAND}"
      command: "{TEST_COMMAND}"
      owner: "{TEST_OWNER}"
      status: planned | active | passing | failing | skipped | deprecated
  evidence:
    - "{EVIDENCE_PATH_OR_CI_URL}"
  exceptions:
    - "{EXCEPTION_ID_OR_REASON}"
```

初始化时必须按项目实际测试框架、目录和命令改写字段。

## 5. Requirement 映射 `[通用 + 个性化]`

```yaml
{REQ_ID}:
  type: requirement
  source: "{REQ_ROOT_DIR}/{REQ_ID}/requirement.md"
  acceptance_source: "{REQ_ROOT_DIR}/{REQ_ID}/acceptance.md"
  change: "{CHANGE_ID_OR_PENDING}"
  acceptance:
    - id: "{AC_ID}"
      description: "{AC_DESCRIPTION}"
      verify_by:
        - "{TEST_TYPE}"
  tests:
    - id: "{TEST_ID}"
      type: "{TEST_TYPE}"
      path: "{TEST_PATH}"
      command: "{TEST_COMMAND}"
      status: planned
  evidence:
    - "待执行"
```

要求：

- `REQ_ID` 必须与需求目录一致。
- 验收项必须来自 acceptance 文档或需求评审结论。
- 尚未实现的测试标记为 `planned`，不得伪造成 `passing`。

## 6. Bug 映射 `[通用 + 个性化]`

```yaml
{BUG_ID}:
  type: bug
  source: "{BUG_ROOT_DIR}/{BUG_ID}/bug.md"
  reproduction_source: "{BUG_ROOT_DIR}/{BUG_ID}/reproduction.md"
  change: "{FIX_CHANGE_ID_OR_PENDING}"
  regression:
    required: true
    reason: "{REGRESSION_REASON}"
  tests:
    - id: "{REGRESSION_TEST_ID}"
      type: "{TEST_TYPE}"
      path: "{TEST_PATH}"
      command: "{TEST_COMMAND}"
      status: planned
  evidence:
    - "待执行"
```

要求：

- Bug 修复必须优先登记复现测试。
- 无法自动化复现时，必须登记人工验收步骤、环境、数据和证据。
- 严重缺陷、权限缺陷、数据缺陷、安全缺陷不得只登记 smoke 测试。

## 7. OpenSpec Change 映射 `[通用 + 个性化]`

```yaml
{CHANGE_ID}:
  type: change
  source: "{CHANGE_ROOT_DIR}/{CHANGE_ID}"
  specs:
    - "{SPEC_MODULE}"
  tasks:
    source: "{CHANGE_ROOT_DIR}/{CHANGE_ID}/tasks.md"
  acceptance:
    - id: "{CHANGE_AC_ID}"
      description: "{CHANGE_ACCEPTANCE_DESCRIPTION}"
      verify_by:
        - "{TEST_TYPE}"
  tests:
    - id: "{TEST_ID}"
      type: "{TEST_TYPE}"
      path: "{TEST_PATH}"
      command: "{TEST_COMMAND}"
      status: planned
  archive_gate:
    tests_recorded: false
    docs_synced: false
    specs_updated: false
```

归档前必须满足：

- 相关测试已执行或有例外审批。
- 文档同步已完成。
- Spec delta 已归档到正式 spec。
- 失败或跳过测试已有原因和后续计划。

## 8. 测试类型矩阵 `[通用 + 个性化]`

| 测试类型 | 适用变更 | 典型命令/位置 | 是否必需 |
|---|---|---|---|
| unit | 业务规则、工具函数、权限判断、错误码 | `{UNIT_TEST_COMMAND}` | 条件 |
| integration | API、数据库、对象存储、队列、外部服务 | `{INTEGRATION_TEST_COMMAND}` | 条件 |
| api | API 契约、响应结构、错误码、认证授权 | `{API_TEST_COMMAND}` | 条件 |
| frontend | 组件、页面、表单、状态、API Mock | `{FRONTEND_TEST_COMMAND}` | 条件 |
| e2e | 核心用户路径、跨模块流程 | `{E2E_TEST_COMMAND}` | 条件 |
| compatibility | 浏览器、设备、数据库、部署矩阵 | `{COMPATIBILITY_TEST_COMMAND}` | 条件 |
| security | 登录、权限、越权、输入校验、敏感数据 | `{SECURITY_TEST_COMMAND}` | 条件 |
| script | 目录、文档、API、测试框架校验脚本 | `{SCRIPT_VALIDATE_COMMAND}` | 条件 |
| manual | 无法稳定自动化的验收 | `{MANUAL_EVIDENCE_POLICY}` | 条件 |

未启用的测试类型不得作为强制项保留。

## 9. 测试证据 `[通用 + 个性化]`

测试证据保存策略：

```text
{EVIDENCE_STORAGE_POLICY}
```

允许证据：

- CI Job URL。
- 测试报告摘要。
- 覆盖率报告路径。
- Playwright/Cypress trace、截图、视频。
- 人工验收记录。
- 发布验收报告。

禁止：

- 提交包含敏感信息的日志。
- 把临时二进制报告长期提交到仓库，除非项目明确要求。
- 用无法复现的口头描述代替关键验收证据。

## 10. 例外审批 `[通用]`

当某个验收项暂时无法自动化测试时，必须登记例外：

```yaml
exceptions:
  - id: "{EXCEPTION_ID}"
    reason: "{REASON}"
    risk: "{RISK}"
    alternative_verification: "{MANUAL_OR_OTHER_CHECK}"
    owner: "{OWNER}"
    expires_at: "{DATE_OR_MILESTONE}"
```

例外不得永久存在。到期必须补测、延期评审或删除对应承诺。

## 11. AI 修改规则 `[通用]`

AI 新增、修改或归档需求、Bug、Change、测试时必须：

- 同步更新本文档的映射记录。
- 不得把未实现测试标记为 passing。
- 不得删除失败测试对应的映射来规避质量门禁。
- 不得保留来源项目需求 ID、Bug ID、Change ID、测试路径、业务场景或技术栈假设。
- 修改 API、数据库、权限、上传、对象存储、部署或兼容性时，必须评估测试类型矩阵。
- 无法验证时必须登记例外、原因和替代验证。

## 12. 初始化生成建议 `[通用]`

初始化生成本文档时应执行：

1. 根据用户输入替换 `{PRODUCT_NAME}`、`{PRODUCT_CODE}`、`{QA_OWNER}`、`{REQ_ROOT_DIR}`、`{BUG_ROOT_DIR}`、`{CHANGE_ROOT_DIR}`、`{SPEC_ROOT_DIR}`、`{TEST_ROOT_DIR}`。
2. 根据 TEST_FRAMEWORKS、TEST_COMMANDS、CI_TEST_GATE、COVERAGE_GATE 生成测试类型矩阵。
3. 根据已有需求、Bug、OpenSpec Change 生成初始映射；没有实际记录时保留格式模板，不生成虚假需求。
4. 根据项目能力保留或删除 `[条件启用]` 测试类型。
5. 未确认测试路径、命令、证据和 owner 标记为 `待确认` 或 `planned`。
6. 不得保留来源项目 Sprint、需求、登录、测试文件、脚本、框架或路径示例。
7. 保持本文档与 `openspec/project.md`、`openspec/config.yaml`、`rules/testing.md`、`docs/standards/testing-governance.md` 一致。

## 13. 更新触发条件 `[通用]`

以下变化必须更新本文档：

- 新增、拆分、取消或归档 Requirement。
- 新增、修复、关闭或重新打开 Bug。
- 新增、实现、归档或回滚 OpenSpec Change。
- 验收标准、测试用例、测试命令、测试路径或 CI 门禁变化。
- 覆盖率目标、测试证据保存策略或例外审批变化。
- API、数据库、权限、安全、对象存储、上传、部署、兼容性等高风险能力变化。
