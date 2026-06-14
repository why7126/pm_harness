# Build Test Framework

## 目标

建立企业级 Testing Governance（测试治理体系）。

将：

```text
rules/testing.md
```

转化为：

```text
测试规范
测试目录
测试模板
测试基线
自动校验
CI检查
```

确保：

```text
Requirement
    ↓
OpenSpec
    ↓
Implementation
    ↓
Test
    ↓
Release
```

形成完整闭环。

---

# 必须读取

执行前必须读取：

```text
AGENTS.md

project.yaml

rules/testing.md

rules/coding.md

rules/api.md

rules/database.md

openspec/project.md
```

如果存在：

```text
src/**
tests/**
```

也必须读取。

---

# Step1 建立 Testing Governance

生成：

```text
docs/testing-governance.md
```

内容包括：

## 测试目标

验证：

```text
正确性

稳定性

兼容性

安全性

回归能力
```

---

## 测试金字塔

统一：

```text
            E2E
         Integration
            Unit
```

比例：

```text
Unit        70%

Integration 20%

E2E         10%
```

---

## AI开发要求

任何 Change：

```text
新增代码
必须新增测试
```

禁止：

```text
修改代码
不修改测试
```

---

# Step2 建立测试目录

生成：

```text
tests/
├── unit/
├── integration/
├── e2e/
├── compatibility/
├── performance/
├── security/
├── fixtures/
└── reports/
```

---

职责：

### unit

单元测试

---

### integration

接口测试

数据库测试

MinIO测试

---

### e2e

完整业务流程

---

### compatibility

浏览器

小程序

SQLite

未来PG

---

### performance

性能测试

---

### security

安全测试

---

# Step3 建立 Pytest 基线

生成：

```text
pytest.ini
```

统一：

```ini
[pytest]

testpaths = tests

python_files = test_*.py

addopts =
    -v
    --tb=short
```

---

生成：

```text
tests/conftest.py
```

统一：

```text
TestClient

SQLite Fixture

MinIO Fixture
```

---

# Step4 建立 Unit Test 标准

生成：

```text
docs/unit-test-standard.md
```

要求：

必须测试：

```text
Service

Repository

Utility

Algorithm
```

禁止：

```text
只测 Router
```

---

示例：

```python
def test_create_tile():
    ...
```

---

覆盖：

```text
正常路径

异常路径

边界条件
```

---

# Step5 建立 API Test 标准

生成：

```text
tests/integration/api/
```

规则：

每个接口必须：

```text
成功测试

失败测试

权限测试

参数校验测试
```

例如：

```python
test_create_tile_success

test_create_tile_invalid_parameter

test_create_tile_unauthorized
```

---

# Step6 建立 Database Test 标准

生成：

```text
tests/integration/database/
```

验证：

```text
CRUD

事务

分页

唯一索引

外键约束
```

---

SQLite：

```text
内存数据库
```

运行。

---

# Step7 建立 MinIO Test 标准

生成：

```text
tests/integration/storage/
```

验证：

```text
上传

下载

删除

不存在对象
```

---

视频：

```text
视频上传

封面生成

路径生成
```

---

# Step8 建立 Frontend Test 标准

生成：

```text
src/web/tests/
```

使用：

```text
Vitest

React Testing Library
```

验证：

```text
组件渲染

事件响应

状态变化
```

---

生成：

```text
docs/frontend-test-standard.md
```

---

# Step9 建立 E2E 标准

生成：

```text
tests/e2e/
```

使用：

```text
Playwright
```

---

场景：

```text
登录

查看瓷砖

搜索瓷砖

上传图片

上传视频
```

---

要求：

每个核心 Requirement：

至少一个 E2E。

---

# Step10 建立 Compatibility Test

生成：

```text
tests/compatibility/
```

包括：

```text
web

miniapp

sqlite

docker

minio
```

---

未来扩展：

```text
postgresql

dameng
```

---

# Step11 建立 Performance Test

生成：

```text
tests/performance/
```

使用：

```text
Locust
```

测试：

```text
列表查询

搜索

上传
```

指标：

```text
P95

TPS

错误率
```

---

# Step12 建立 Security Test

生成：

```text
tests/security/
```

检查：

```text
鉴权

越权

SQL注入

XSS

文件上传
```

---

# Step13 建立 Coverage 规范

生成：

```text
.coveragerc
```

要求：

```text
Backend >= 80%

Core Module >= 90%
```

---

生成：

```text
docs/test-coverage.md
```

---

# Step14 建立 AI 测试生成规范

生成：

```text
.claude/skills/test-generation.md
```

规则：

当：

```text
新增 Service
```

自动生成：

```text
test_service_xxx.py
```

---

当：

```text
新增 Router
```

自动生成：

```text
integration test
```

---

当：

```text
新增 Requirement
```

自动生成：

```text
E2E Test
```

---

# Step15 建立 OpenSpec Test Mapping

生成：

```text
openspec/testing-mapping.md
```

要求：

每个 Requirement：

```text
Requirement
    ↓
Acceptance
    ↓
Test Case
```

形成映射。

---

示例：

```yaml
REQ-0001:
  acceptance:
    - AC-001
    - AC-002

  tests:
    - test_create_tile
    - test_query_tile
```

---

# Step16 建立自动校验

生成：

```text
scripts/validate-test-framework.py
```

检查：

```text
Change 是否存在测试

Service 是否存在测试

Router 是否存在测试

Requirement 是否存在E2E
```

输出违规报告。

---

# Step17 建立 CI 规则

生成：

```text
.github/workflows/test.yml
```

执行：

```text
unit

integration

e2e
```

失败禁止合并。

---

# Step18 创建 OpenSpec Change

如果不存在：

```text
openspec/changes/build-test-framework/
```

生成：

```text
proposal.md
design.md
tasks.md
acceptance.md
test-plan.md
trace.md
specs/testing/spec.md
```

---

# Step19 更新文档

更新：

```text
AGENTS.md

rules/testing.md

docs/testing-governance.md

docs/unit-test-standard.md

docs/frontend-test-standard.md

docs/test-coverage.md
```

---

# 验收标准

完成后必须满足：

```text
□ Pytest基线已建立

□ Frontend Test基线已建立

□ E2E基线已建立

□ MinIO测试已建立

□ SQLite测试已建立

□ Compatibility测试已建立

□ Performance测试已建立

□ Security测试已建立

□ Coverage规则已建立

□ AI自动补测试规则已建立

□ validate-test-framework.py可运行

□ CI测试流程已建立

□ OpenSpec Change已创建
```

---

# 最终输出

输出：

```text
1. 测试治理摘要

2. 测试目录结构

3. 覆盖率标准

4. E2E覆盖情况

5. CI检查规则

6. 自动校验规则

7. 尚需人工确认的问题
```
