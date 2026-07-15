---
purpose: API 设计规范
content: 接口路径、响应结构、错误码、OpenAPI、客户端生成规则
source: Harness Token 优化模板
update_method: 新增接口、修改接口、调整错误码或前端生成方式时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-14 00:00:00
note: API 变更必须同步 docs/03-api-index.md、OpenAPI 来源、客户端生成物和测试
---

# API 设计规范

## 1. 路径与版本

- 接口 SHOULD 使用统一版本前缀，例如 `/api/v1`。
- 路径使用资源名词，避免动词堆叠；批量、导入导出、上传下载等动作可作为子资源或 action。
- 管理端、公开端、移动端或内部接口必须有清晰权限边界。

## 2. 响应结构

统一响应结构由项目初始化后确认；推荐包含：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

分页响应至少说明 `items`、`total`、`page`、`page_size` 或等价字段。错误响应必须能被前端和测试稳定断言。

## 3. OpenAPI 与客户端生成

- 后端必须正确暴露 OpenAPI 或等价接口契约。
- 前端接口类型 SHOULD 通过 OpenAPI 生成，避免手写重复类型。
- API 变更后必须同步 `docs/03-api-index.md`、生成配置、生成物和相关测试。
- 复核生成物时遵守 `rules/agent-context-budget.md`，只读取目标接口或 schema 片段。

## 4. 上传与媒体接口

涉及文件、图片、视频、附件上传时，响应至少说明：

```text
media_id / file_id
object_key
url 或 preview_url
mime_type
size
width / height（如适用）
duration / cover_url（视频如适用）
```

上传必须经过后端鉴权与校验，不得让前端直连未授权对象存储。

## 5. AI 更新清单

AI 新增或修改 API 时必须检查：

```text
□ OpenSpec Change / spec 是否同步
□ docs/03-api-index.md 是否同步
□ OpenAPI / 客户端生成物是否同步
□ 错误码与权限边界是否同步
□ 单元 / 集成 / 前端调用测试是否同步
```
