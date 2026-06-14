# Bug To Change

## 目标

将：

```text
issues/bugs/*
```

中的缺陷记录，

转换为：

```text
openspec/changes/fix-*
```

中的标准修复变更（Fix Change）。

确保：

```text
Bug
    ↓
Root Cause
    ↓
Impact Analysis
    ↓
Fix Change
    ↓
Regression Test
    ↓
Knowledge Base
```

形成完整闭环。

---

# 必须读取

执行前必须读取：

```text
AGENTS.md

project.yaml

rules/bug-management.md

rules/testing.md

rules/api.md

rules/database.md

rules/object-storage.md

rules/openspec-workflow.md

openspec/project.md
```

同时读取：

```text
issues/bugs/<BUG-ID>/**
```

包括：

```text
bug.md

root-cause.md

workaround.md

acceptance.md

trace.md

logs/**

screenshots/**
```

---

# 输入

输入：

```text
BUG-XXXX
```

例如：

```text
BUG-0001-minio-upload-timeout
```

---

# Step1 Bug完整性检查

检查：

```text
bug.md

root-cause.md

acceptance.md

trace.md
```

是否存在。

如果缺失：

自动生成模板。

---

检查：

```text
严重等级

状态

负责人

发现时间

环境
```

是否存在。

---

输出：

```text
Bug Readiness Report
```

状态：

```text
Ready

Partially Ready

Not Ready
```

---

# Step2 缺陷分析

分析：

## 现象

用户看到什么问题

---

## 复现路径

如何复现

---

## 影响范围

哪些功能受影响

---

## 业务影响

是否影响客户

是否影响收入

是否影响数据

---

输出：

```text
Bug Analysis Report
```

---

# Step3 Root Cause Review

读取：

```text
root-cause.md
```

分析根因是否充分。

如果缺失：

自动补充：

```text
直接原因

根本原因

触发条件

遗漏原因
```

---

根因分类：

```yaml
root_cause_type:
  code
  design
  database
  api
  ui
  infrastructure
  configuration
  dependency
  process
```

---

# Step4 Severity识别

自动归类：

```yaml
severity:
  blocker
  critical
  high
  medium
  low
```

规则：

```text
Blocker
系统不可用

Critical
核心功能不可用

High
主要功能异常

Medium
局部功能异常

Low
体验问题
```

---

# Step5 Impact Analysis

分析：

```text
Backend

Web

MiniApp

Admin

Database

Storage

API

Algorithm

Security

Performance
```

---

输出：

```yaml
impact:
  backend: true
  database: false
  storage: true
```

---

# Step6 Change分类

自动识别：

```yaml
change_type:
  bugfix
  hotfix
  refactor-fix
  migration-fix
```

---

规则：

```text
线上严重问题
→ hotfix

普通修复
→ bugfix

架构问题
→ refactor-fix
```

---

# Step7 创建 Fix Change

生成：

```text
openspec/changes/
└── fix-xxxx/
```

命名：

```text
fix-minio-upload-timeout

fix-tile-search-pagination

fix-admin-login-expired
```

---

# Step8 生成 proposal.md

内容：

## Bug来源

---

## 当前问题

---

## 影响范围

---

## 修复目标

---

## 风险

---

## 回滚方案

必须包含：

```text
Rollback Plan
```

---

# Step9 生成 design.md

内容：

## 根因

---

## 修复方案

---

## 数据影响

---

## API影响

---

## UI影响

---

## 测试方案

---

要求：

明确：

```text
为什么这样修
```

而不是：

```text
改代码即可
```

---

# Step10 生成 OpenSpec Spec

创建：

```text
openspec/changes/fix-xxx/specs/
```

---

格式：

```text
## MODIFIED Requirements

## FIXED Requirements
```

---

示例：

```text
System SHALL correctly paginate tile search results.
```

---

Scenario：

```text
Given page=2

When user searches

Then correct results SHALL be returned.
```

---

# Step11 生成 tasks.md

拆解：

```text
Root Cause Fix

API Fix

DB Fix

UI Fix

Regression Test

Documentation
```

---

示例：

```text
- [ ] 修复分页SQL

- [ ] 增加分页单元测试

- [ ] 增加分页集成测试

- [ ] 更新API文档

- [ ] 更新知识库
```

---

# Step12 生成 acceptance.md

来源：

```text
issues/bugs/*/acceptance.md
```

转换：

```text
AC-001

AC-002

AC-003
```

要求：

可验证

可自动化测试

---

# Step13 生成 Regression Plan

创建：

```text
regression-plan.md
```

内容：

## 直接验证

修复问题

---

## 邻域验证

相似功能

---

## 回归验证

受影响模块

---

例如：

```text
分页修复

↓

全部分页接口回归
```

---

# Step14 生成 test-plan.md

映射：

```text
Bug
 ↓
Fix
 ↓
Regression Test
```

---

输出：

```yaml
BUG-0001:
  unit:
  integration:
  e2e:
  regression:
```

---

# Step15 自动识别 Design System影响

如果：

```text
UI问题
```

则：

增加：

```text
UI Review

Design System Validation
```

---

要求：

验证：

```text
shared/ui

shared/business

templates
```

---

# Step16 自动识别 API影响

如果涉及：

```text
接口问题
```

自动加入：

```text
API Regression

OpenAPI Review

Orval Regeneration
```

---

# Step17 自动识别 Database影响

如果涉及：

```text
SQL

索引

分页

事务
```

自动加入：

```text
DB Regression

Migration Validation
```

---

# Step18 自动识别 Storage影响

如果涉及：

```text
MinIO

上传

视频

图片
```

自动加入：

```text
Storage Regression

Upload Test
```

---

# Step19 自动识别 Security影响

如果涉及：

```text
认证

权限

Token

登录
```

自动加入：

```text
Security Regression
```

验证：

```text
越权

权限绕过

Token失效
```

---

# Step20 更新 Traceability

更新：

```text
issues/bugs/<BUG>/trace.md
```

增加：

```yaml
change_id:
```

例如：

```yaml
change_id:
  - fix-minio-upload-timeout
```

---

生成：

```text
openspec/changes/fix-xxx/trace.md
```

内容：

```yaml
bug_id:

change_id:

severity:

iteration:

owner:
```

---

# Step21 更新知识库

如果：

```text
severity >= high
```

或者：

```text
重复出现问题
```

自动创建：

```text
docs/knowledge-base/incidents/
```

例如：

```text
minio-upload-timeout.md
```

内容：

```text
故障现象

根因

修复方案

预防措施
```

---

# Step22 自动推荐 Sprint

检查：

```text
iterations/*
```

如果：

```text
blocker
critical
```

建议：

```yaml
iteration:
  hotfix
```

否则：

```yaml
iteration:
  sprint-xx
```

---

# Step23 Change Metadata

生成：

```yaml
change_id:

bug_id:

severity:

change_type:

owner:

status:
```

---

# Step24 验收标准

完成后必须满足：

```text
□ proposal.md 已生成

□ design.md 已生成

□ tasks.md 已生成

□ acceptance.md 已生成

□ test-plan.md 已生成

□ regression-plan.md 已生成

□ spec.md 已生成

□ trace.md 已生成

□ bug trace 已更新

□ Root Cause 已验证

□ Regression Plan 已生成

□ 知识库已更新（如适用）

□ Change Metadata 已生成
```

---

# 输出

最终输出：

```text
1. Bug分析

2. Root Cause摘要

3. Impact分析

4. Fix Change信息

5. Regression Plan

6. 风险

7. 推荐Sprint

8. 知识库更新情况

9. 后续动作
```
