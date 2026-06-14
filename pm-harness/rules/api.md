---
purpose: API设计规范
content: FastAPI接口路径、响应结构、错误码、OpenAPI、Orval生成规则
source: AI自动生成初稿，项目团队确认
update_method: 新增接口、修改接口、调整错误码或前端生成方式时更新
note: API变更必须同步docs/03-api-index.md和Orval客户端
---

# API设计规范

## 1. 路径规范

接口统一使用 `/api/v1` 前缀。

推荐资源：

```text
/api/v1/tiles
/api/v1/tile-categories
/api/v1/tile-series
/api/v1/media/images
/api/v1/media/videos
/api/v1/admin/tiles
```

## 2. 响应结构

统一响应结构：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

分页响应：

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 20
}
```

## 3. OpenAPI与Orval

- FastAPI必须正确暴露OpenAPI。
- 前端接口类型必须通过Orval生成。
- API变更后必须运行：

```bash
./scripts/generate-openapi-client.sh
```

## 4. 媒体API

媒体上传接口必须返回：

- media_id
- object_key
- url或preview_url
- mime_type
- size
- width/height，若适用
- duration，若为视频且可获取
- cover_url，若为视频且有封面

## 5. AI更新规则

AI新增或修改API时，必须同步：

```text
docs/03-api-index.md
openspec/changes/<change-id>/specs/*/spec.md
src/web/orval.config.ts
src/web/src/api/generated/
tests/integration/
```
