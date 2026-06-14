---
purpose: Requirement 与测试用例映射
content: 验收项到自动化测试的追溯
source: build-test-framework
update_method: 新增 Requirement 或测试时更新
---

# OpenSpec 测试映射

## 格式

```yaml
REQ-xxxx:
  acceptance:
    - AC-001
  tests:
    - tests/integration/api/test_xxx.py::test_name
```

## Sprint-00 基础设施

```yaml
REQ-0000-build-design-system:
  acceptance:
    - DS-AC-001 Token 与组件可预览
  tests:
    - src/web/src/components/ui/design-system.test.tsx
    - scripts/validate-design-system.py

REQ-0000-build-api-standard:
  acceptance:
    - API-AC-001 统一返回与 OpenAPI
  tests:
    - tests/integration/api/test_api_baseline.py
    - src/backend/tests/test_auth.py
    - scripts/validate-api-standard.py

REQ-0000-build-test-standard:
  acceptance:
    - TEST-AC-001 Pytest 与治理文档就绪
  tests:
    - tests/unit/test_error_codes.py
    - scripts/validate-test-framework.py
```

## Sprint-01

```yaml
REQ-0001-user-login:
  acceptance:
    - 见 issues/requirements/REQ-0001-user-login/acceptance.md
  tests:
    - src/backend/tests/test_auth.py
    - src/web/src/features/auth/**/*.test.tsx
```
