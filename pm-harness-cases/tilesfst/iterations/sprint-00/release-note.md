# Sprint 00 发布说明

## 新增能力

### Design System

- TS Token 层、`globals.css`、Tailwind 语义 class
- shadcn/ui 基础 + 复合 UI + 业务组件 + 页面模板
- `/design-system` 预览页
- `scripts/validate-design-system.py`

### API 标准

- 治理文档：`api-governance`、`error-codes`、`openapi-rules`、`authentication`、`file-upload`
- `error_codes.py`、统一 `ApiResponse`
- Orval 客户端生成链路

### 测试框架

- 根目录 `pytest.ini`、`tests/conftest.py`
- 治理文档与 `openspec/testing-mapping.md`
- GitHub Actions `test.yml`
- `scripts/validate-test-framework.py`

### Docker

- `docker-compose.yml`（backend、web、minio）
- `.env.example`、`scripts/docker-up.sh`

## 兼容性

- 无破坏性 API 变更
- Sprint-01 业务功能在此基础上继续迭代
