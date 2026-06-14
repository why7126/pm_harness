# REQ-0000 建设 API 标准

## 1. 背景

多端（Web、小程序、管理端）与 AI 协作开发需要统一的 API 契约、错误码、鉴权与 OpenAPI/Orval 生成链路。

## 2. 目标

- REST `/api/v1` 资源命名与统一返回结构
- 错误码分段治理（`error_codes.py`、`docs/error-codes.md`）
- FastAPI 分层：api / schemas / services / repositories
- OpenAPI First + Orval 客户端

## 3. 范围

| 包含 | 不包含 |
|------|--------|
| 治理文档、校验脚本 | 全部业务模块 CRUD |
| 认证 API 基线 | 小程序 SDK 生成 |
| `src/sdk` 说明 | GraphQL |

## 4. 状态

`completed` — 认证与瓷砖/upload 路由已存在；Sprint-00 补全治理层。
