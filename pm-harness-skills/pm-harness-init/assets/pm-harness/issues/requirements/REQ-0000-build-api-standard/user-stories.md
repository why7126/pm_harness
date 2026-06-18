# 用户故事

## US-API-001 统一响应

作为前端开发者，我希望所有接口返回 `{ code, message, data }`，以便 Axios 拦截器统一处理。

## US-API-002 类型生成

作为开发者，我希望通过 Orval 从 OpenAPI 生成 TS 客户端，避免手写类型。

## US-API-003 错误码可查

作为排障人员，我希望在 `docs/standards/error-codes.md` 查阅错误码含义。
