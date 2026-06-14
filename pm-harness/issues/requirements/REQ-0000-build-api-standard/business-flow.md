# 业务流程

```text
rules/api.md
        ↓
FastAPI Router + Pydantic Schema
        ↓
OpenAPI (/openapi.json)
        ↓
Orval → src/web/src/shared/api/generated.ts
        ↓
集成测试 + validate-api-standard.py
```
