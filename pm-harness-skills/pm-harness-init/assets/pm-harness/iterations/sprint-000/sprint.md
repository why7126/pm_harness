---
title: Sprint 000 迭代说明
purpose: 项目基础设施 Sprint — Design System、API 标准、测试框架
content: initialize-project 交付物登记与验收
source: initialize-project / project.yaml
update_method: 基础设施变更时更新
owner: 项目负责人
status: completed
---

# Sprint 000

## Sprint 目标

完成瓷砖信息管理平台**基础设施建设**，为 Sprint-001 业务功能（REQ-0001 用户登录）提供可复用基线：

1. Design System（Token、组件、模板、校验）
2. API 治理（统一返回、错误码、OpenAPI/Orval）
3. 测试框架（Pytest、治理文档、CI）
4. Docker Compose 基线（已在项目模板中存在）

## Scope

| 编号 | 名称 | 状态 |
|------|------|------|
| REQ-0000-build-design-system | 建设 Design System | completed |
| REQ-0000-build-api-standard | 建设 API 标准 | completed |
| REQ-0000-build-test-standard | 建设测试标准 | completed |

## Change 列表

| Change ID | 说明 | 状态 |
|-----------|------|------|
| `build-design-system` | DS 治理与校验补全 | completed |
| `build-api-standard` | API 治理文档与 error_codes | completed |
| `build-test-framework` | 根 tests/ 与 CI | completed |

**说明：** 部分实现已通过 `add-design-system`、`add-user-login` 提前交付；本 Sprint 补全治理层与 Sprint-000 登记。

## 工作量

| 工作包 | 人天 |
|--------|------|
| Design System | 5 |
| API 标准 | 4 |
| 测试框架 | 3 |
| Docker 基线（已有） | 1 |
| 文档与校验脚本 | 2 |
| **合计** | **15** |

## 风险

- 根 `tests/` 与 `src/backend/tests/` 并存，需逐步收敛
- API 路由 OpenAPI 元数据需随业务接口持续补齐

## 后续

Sprint-001 聚焦 REQ-0001 用户登录与登录页视觉对齐。
