---
purpose: OpenAPI 注解规范
content: FastAPI 路由 OpenAPI 元数据要求
source: build-api-standard
update_method: API 规范变更时同步更新
---

# OpenAPI 规范

## 要求

每个对外路由 MUST 声明：

```python
@router.get(
    "/tiles",
    response_model=ApiResponse[PaginatedTiles],
    summary="获取瓷砖列表",
    description="分页查询瓷砖目录，支持 keyword 筛选。",
    tags=["tiles"],
)
```

## 契约来源

- 运行时：`GET /openapi.json`（FastAPI 默认）
- 前端生成输入：`src/web/openapi.json`（由脚本导出）

## 生成流程

```bash
./scripts/generate-openapi-client.sh
```

输出：`src/web/src/shared/api/generated.ts`（Orval）

## 禁止

- 手写与 OpenAPI 不一致的 TS 类型
- 缺少 `response_model` 的公开接口
- 未登记 tags 的模块混杂

## 校验

```bash
python scripts/validate-api-standard.py
```
