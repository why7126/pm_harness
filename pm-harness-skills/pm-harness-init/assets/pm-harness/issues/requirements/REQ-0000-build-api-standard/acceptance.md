# 验收标准

## 治理文档

- [x] `docs/standards/api-governance.md`
- [x] `docs/standards/error-codes.md`
- [x] `docs/standards/openapi-rules.md`
- [x] `docs/standards/authentication.md`
- [x] `docs/standards/file_upload.md`
- [x] `docs/03-api-index.md`

## 代码

- [x] `src/backend/app/schemas/common.py` 统一响应
- [x] `src/backend/app/core/error_codes.py`
- [x] `src/backend/app/api/v1/` 路由模块
- [x] `src/web/orval.config.ts` + 生成客户端
- [x] `src/sdk/README.md`

## 校验与测试

- [x] `scripts/validate-api-standard.py`
- [x] `tests/integration/api/test_api_baseline.py`
- [x] `src/backend/tests/test_auth.py`
