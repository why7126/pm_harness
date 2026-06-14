# Build API Standard

## 目标

建立企业级 API Governance（API治理体系）。

将：

```text
rules/api.md
```

转换为：

```text
可执行API规范
OpenAPI规范
FastAPI代码模板
Orval客户端生成规范
自动校验脚本
```

确保：

```text
后端
OpenAPI
前端
测试
```

全部遵循统一标准。

---

# 必须读取

执行前必须读取：

```text
AGENTS.md

project.yaml

rules/api.md

rules/security.md

rules/testing.md

rules/coding.md

openspec/project.md
```

如果存在：

```text
src/backend/*
src/web/*
```

也必须读取。

---

# Step1 建立 API Governance

生成：

```text
docs/api-governance.md
```

内容必须包含：

## API设计原则

REST First

统一资源命名

幂等性

向后兼容

OpenAPI First

---

## URL规范

例如：

```text
/api/v1/tiles

/api/v1/tiles/{id}

/api/v1/media
```

禁止：

```text
/getTiles

/queryTileList

/deleteById
```

---

## HTTP Method规范

GET

POST

PUT

PATCH

DELETE

对应使用场景。

---

## API版本规范

统一：

```text
/api/v1/*
```

未来：

```text
/api/v2/*
```

---

# Step2 建立统一返回结构

生成：

```text
src/backend/app/schemas/common/
```

包含：

```text
response.py

pagination.py

error.py
```

---

统一返回：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

---

分页返回：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [],
    "page": 1,
    "page_size": 20,
    "total": 100
  }
}
```

---

错误返回：

```json
{
  "code": 40001,
  "message": "invalid parameter"
}
```

---

# Step3 建立错误码体系

生成：

```text
docs/error-codes.md

src/backend/app/core/error_codes.py
```

规则：

```text
0 成功

1xxxx 系统错误

2xxxx 认证授权

3xxxx 业务错误

4xxxx 参数错误

5xxxx 外部依赖错误
```

示例：

```python
INVALID_PARAMETER = 40001
UNAUTHORIZED = 20001
TILE_NOT_FOUND = 30001
```

---

# Step4 建立 FastAPI代码结构

生成：

```text
src/backend/app/
```

结构：

```text
api/
core/
models/
schemas/
services/
repositories/
```

每个模块：

```text
modules/
└── tiles/
    ├── router.py
    ├── service.py
    ├── repository.py
    ├── schema.py
    └── model.py
```

禁止：

```text
全部写在router
```

---

# Step5 建立 OpenAPI First

生成：

```text
docs/openapi-rules.md
```

要求：

所有接口必须：

```python
response_model=
summary=
description=
tags=
```

必须完整。

---

生成：

```text
/openapi.json
```

作为：

```text
唯一API契约
```

---

# Step6 建立前端 Orval 规范

生成：

```text
src/web/orval.config.ts
```

规则：

```text
OpenAPI
    ↓
Orval
    ↓
生成TypeScript类型
    ↓
生成Axios客户端
```

目录：

```text
src/web/src/generated/
```

禁止：

```text
手写接口类型
```

---

# Step7 建立分页规范

统一：

```text
page
page_size
```

返回：

```text
items
total
```

禁止：

```text
rows
list
records
```

混用。

---

# Step8 建立查询规范

支持：

```text
keyword

sort_by

sort_order

page

page_size
```

统一格式。

---

# Step9 建立鉴权规范

生成：

```text
docs/authentication.md
```

统一：

```text
JWT
```

Header：

```text
Authorization: Bearer xxx
```

禁止：

```text
token=
sessionId=
```

混用。

---

# Step10 建立文件上传规范

生成：

```text
docs/file-upload.md
```

统一：

```text
multipart/form-data
```

返回：

```json
{
  "file_id": "",
  "url": ""
}
```

---

适用于：

```text
图片

视频

附件
```

---

# Step11 建立测试规范

生成：

```text
tests/api/
```

要求：

每个接口必须：

```text
成功测试

失败测试

权限测试

边界测试
```

---

# Step12 建立自动校验

生成：

```text
scripts/validate-api-standard.py
```

检查：

```text
response_model

tags

summary

description

错误码

分页结构

返回结构
```

输出违规报告。

---

# Step13 建立 OpenSpec Change

不存在则创建：

```text
openspec/changes/build-api-standard/
```

生成：

```text
proposal.md
design.md
tasks.md
acceptance.md
test-plan.md
trace.md
specs/api-governance/spec.md
```

---

# Step14 更新文档

更新：

```text
AGENTS.md

rules/api.md

docs/api-governance.md

docs/error-codes.md

docs/openapi-rules.md

docs/authentication.md

docs/file-upload.md
```

---

# 验收标准

完成后必须满足：

```text
□ API Governance文档已生成

□ 统一返回结构已生成

□ 错误码体系已生成

□ FastAPI模板已生成

□ OpenAPI规范已生成

□ Orval配置已生成

□ 分页规范已生成

□ JWT规范已生成

□ 文件上传规范已生成

□ API测试框架已生成

□ validate-api-standard.py可运行

□ OpenSpec Change已创建
```

---

# 最终输出

输出：

```text
1. API治理摘要

2. API目录结构

3. 错误码体系

4. OpenAPI规范

5. Orval规范

6. 测试规范

7. 自动校验规则

8. 尚需人工确认的问题
```
