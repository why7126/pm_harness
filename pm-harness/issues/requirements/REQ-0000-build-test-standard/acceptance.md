# 验收标准

## 目录与配置

- [x] `tests/unit/`、`tests/integration/`、`tests/e2e/`、`tests/fixtures/`
- [x] `pytest.ini`（含 `src/backend/tests`）
- [x] `tests/conftest.py`（TestClient + SQLite fixture）
- [x] `.coveragerc`

## 文档

- [x] `docs/testing-governance.md`
- [x] `docs/unit-test-standard.md`
- [x] `docs/frontend-test-standard.md`
- [x] `docs/test-coverage.md`
- [x] `openspec/testing-mapping.md`

## 基线测试

- [x] `tests/unit/test_error_codes.py`
- [x] `tests/integration/api/test_api_baseline.py`

## 工具与 CI

- [x] `scripts/validate-test-framework.py`
- [x] `.github/workflows/test.yml`
