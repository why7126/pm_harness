---
purpose: API 治理体系
content: REST 设计原则、URL/Method/版本、统一返回与 OpenAPI First
source: rules/api.md / build-api-standard
update_method: API 规范变更时同步更新
---

# API 治理体系

## 设计原则

| 原则 | 说明 |
|------|------|
| REST First | 资源导向 URL，禁止动词式路径 |
| 统一资源命名 | 复数名词、kebab-case 段 |
| 幂等性 | PUT/DELETE 幂等；POST 创建非幂等 |
| 向后兼容 | 破坏性变更走 `/api/v2` |
| OpenAPI First | FastAPI 注解完整，契约即 `openapi.json` |

## URL 规范

```text
/api/v1/tiles
/api/v1/tiles/{id}
/api/v1/auth/login
/api/v1/admin/tiles
/api/v1/uploads/images
```

禁止：`/getTiles`、`/queryTileList`、`/deleteById`

## HTTP Method

| Method | 场景 |
|--------|------|
| GET | 查询、列表、详情 |
| POST | 创建、登录、上传 |
| PUT | 全量更新 |
| PATCH | 部分更新 |
| DELETE | 删除 |

## 版本

当前统一前缀：`/api/v1/*`

## 统一返回结构

成功：

```json
{ "code": 0, "message": "success", "data": {} }
```

分页 `data`：

```json
{ "items": [], "page": 1, "page_size": 20, "total": 100 }
```

错误：

```json
{ "code": 40001, "message": "invalid parameter", "data": null }
```

实现见 `src/backend/app/schemas/common.py`、`app/core/exceptions.py`。

## 错误码

见 `docs/error-codes.md`、`src/backend/app/core/error_codes.py`。

## OpenAPI 与 Orval

1. 后端路由 MUST 设置 `response_model`、`summary`、`description`、`tags`
2. 导出 OpenAPI：`src/web/openapi.json`
3. 生成客户端：`./scripts/generate-openapi-client.sh`
4. 前端禁止手写接口类型

## 鉴权

见 `docs/authentication.md` — JWT，`Authorization: Bearer <token>`

## 文件上传

见 `docs/file-upload.md` — `multipart/form-data`，后端授权 + MinIO

## 校验

```bash
python scripts/validate-api-standard.py
```

## 相关文档

- `rules/api.md`
- `docs/03-api-index.md`
- `docs/openapi-rules.md`
- `docs/error-codes.md`
