---
purpose: API 索引
content: API 分组、契约来源、接口清单、错误码、客户端生成和同步规则
source: Harness docs Token 优化模板，初始化时基于 API 契约生成
update_method: 新增、删除或修改 API、错误码、权限、OpenAPI 或客户端生成方式时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-07-14 00:00:00
owner: {DOCS_OWNER}
note: 本文档是 API 导航，不复制完整 OpenAPI JSON
---

# API 索引

## 1. 契约来源

| 项 | 位置 |
|---|---|
| API 前缀 | `{API_BASE_PATH}` |
| OpenAPI 来源 | `{OPENAPI_SOURCE}` |
| 客户端生成配置 | `{API_CLIENT_CONFIG}` |
| 生成命令 | `{API_CLIENT_GENERATE_COMMAND}` |
| 错误码规则 | [standards/error-codes.md](standards/error-codes.md) |
| API 治理规则 | [standards/api-governance.md](standards/api-governance.md) |

## 2. API 分组

| 分组 | 路径前缀 | 权限 | 说明 |
|---|---|---|---|
| Public | `{PUBLIC_API_PREFIX}` | `{PUBLIC_AUTH}` | 面向公开端或匿名访问 |
| User | `{USER_API_PREFIX}` | `{USER_AUTH}` | 面向登录用户 |
| Admin | `{ADMIN_API_PREFIX}` | `{ADMIN_AUTH}` | 面向管理端 |
| Internal | `{INTERNAL_API_PREFIX}` | `{INTERNAL_AUTH}` | 内部服务调用 |

## 3. 接口清单

初始化或 API 变更后，用真实接口替换下表。

| Method | Path | 分组 | 说明 | 权限 | Spec / 测试 |
|---|---|---|---|---|---|
| GET | `{API_PATH}` | `{GROUP}` | `{DESCRIPTION}` | `{AUTH}` | `{SPEC_OR_TEST}` |

只记录接口索引和关键约束；请求/响应 schema 以 OpenAPI 和对应测试为准。

## 4. 响应与错误

统一响应结构、分页结构和错误码策略见：

- [rules/api.md](../rules/api.md)
- [standards/api-governance.md](standards/api-governance.md)
- [standards/error-codes.md](standards/error-codes.md)

## 5. 变更同步清单

API 变更必须同步：

```text
□ openspec/changes/<change-id>/specs/
□ docs/03-api-index.md
□ docs/standards/api-governance.md（如规则变化）
□ OpenAPI 来源
□ 客户端生成物
□ 后端 API / Service / Schema 测试
□ 前端调用和错误处理测试
```

复核生成物时遵守 `rules/agent-context-budget.md`：默认看 diff stat、接口片段和 schema 片段，不输出完整 generated 文件。
