# Requirement To Change

## 目标

将：

```text
issues/requirements/*
```

中的业务需求，

转换为：

```text
openspec/changes/*
```

中的标准 OpenSpec Change。

确保：

```text
Requirement
    ↓
OpenSpec
    ↓
Implementation
    ↓
Test
```

形成可追踪闭环。

---

# 必须读取

执行前必须读取：

```text
AGENTS.md

project.yaml

rules/requirement-management.md

rules/openspec-workflow.md

rules/api.md

rules/database.md

rules/testing.md

rules/ui-design.md

openspec/project.md
```

同时读取：

```text
issues/requirements/<REQ-ID>/**
```

包括：

```text
requirement.md

user-stories.md

business-flow.md

acceptance.md

trace.md

prototype/**
```

---

# 输入

输入：

```text
REQ-XXXX
```

例如：

```text
REQ-0001-tile-info-management
```

---

# Step1 Requirement完整性检查

检查：

```text
requirement.md

user-stories.md

business-flow.md

acceptance.md

trace.md
```

是否存在。

如果缺失：

生成缺失文档模板。

---

检查：

```text
状态
优先级
负责人
来源
```

是否存在。

---

输出：

```text
Requirement Readiness Report
```

包括：

```text
Ready

Partially Ready

Not Ready
```

---

# Step2 需求理解

分析：

## 业务目标

为什么做

---

## 用户

谁使用

---

## 业务流程

用户如何使用

---

## 核心能力

新增什么能力

---

## 非功能需求

性能

安全

兼容性

可维护性

---

输出：

```text
Requirement Analysis
```

---

# Step3 影响分析

分析影响范围：

```text
Backend

Web

MiniApp

Admin

Database

Storage

API

Algorithm

Test
```

---

输出：

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  database: true
  storage: true
```

---

# Step4 Change分类

自动识别：

```text
Feature

Enhancement

Refactor

Migration
```

---

生成：

```yaml
change_type: Feature
```

---

# Step5 创建 Change ID

规则：

```text
add-xxx

update-xxx

remove-xxx
```

例如：

```text
add-tile-info-management
```

---

创建：

```text
openspec/changes/add-tile-info-management/
```

---

# Step6 生成 proposal.md

内容：

## 背景

需求来源

---

## 问题

当前缺少什么能力

---

## 目标

希望实现什么

---

## 范围

包含：

```text
In Scope
```

不包含：

```text
Out Of Scope
```

---

## 风险

潜在风险

---

## 收益

业务收益

---

# Step7 生成 design.md

设计内容：

## 架构设计

---

## API设计

---

## 数据模型设计

---

## UI设计

---

## 存储设计

---

## 测试设计

---

要求：

引用：

```text
rules/*
```

中的规范。

---

# Step8 生成 OpenSpec Spec

创建：

```text
openspec/changes/<change>/specs/
```

---

使用 OpenSpec 格式：

```text
## ADDED Requirements

### Requirement:
```

示例：

```text
System SHALL allow store owners to view tile information.
```

---

必须包含：

```text
Requirement

Scenario
```

---

# Step9 生成 tasks.md

自动拆解任务。

维度：

```text
Backend

Database

API

Web

MiniApp

Admin

Storage

Test

Docs
```

---

示例：

```text
- [ ] 创建 tiles 表

- [ ] 创建 Tile API

- [ ] 创建 Tile List Page

- [ ] 创建 Tile Detail Page

- [ ] 创建 Integration Test

- [ ] 更新 API 文档
```

---

# Step10 生成 acceptance.md

根据：

```text
issues/requirements/*/acceptance.md
```

自动转换。

格式：

```text
AC-001

AC-002

AC-003
```

要求：

可测试

可验证

不可模糊

---

# Step11 生成 test-plan.md

自动映射：

```text
Requirement
    ↓
Acceptance
    ↓
Test Case
```

输出：

```yaml
AC-001:
  unit:
  integration:
  e2e:
```

---

# Step12 建立 Traceability

更新：

```text
issues/requirements/<REQ>/trace.md
```

增加：

```yaml
change_id:
```

例如：

```yaml
change_id:
  - add-tile-info-management
```

---

生成：

```text
openspec/changes/<change>/trace.md
```

内容：

```yaml
requirement_id:

change_id:

iteration:

owner:
```

---

# Step13 自动识别 Design System 影响

检查：

```text
prototype/**
```

是否新增页面。

如果新增：

自动加入：

```text
UI Task

Design System Review
```

---

要求：

新页面必须：

```text
复用 shared/ui

复用 shared/business

复用 templates
```

---

# Step14 自动识别 API 影响

如果需求涉及：

```text
新增接口
```

自动加入：

```text
API Task

OpenAPI Task

Orval Task
```

---

# Step15 自动识别 Database 影响

如果需求涉及：

```text
新增字段

新增表

修改表
```

自动加入：

```text
Migration Task

Database Test
```

---

# Step16 自动识别 Storage 影响

如果需求涉及：

```text
图片

视频

附件
```

自动加入：

```text
MinIO Task

Upload Test

Storage Test
```

---

# Step17 自动识别 Iteration

检查：

```text
iterations/*
```

寻找：

```text
status=planning
```

的 Sprint。

如果容量允许：

自动建议：

```yaml
iteration:
  sprint-01
```

否则：

```yaml
iteration:
  backlog
```

---

# Step18 更新 OpenSpec Registry

更新：

```text
openspec/project.md
```

中的能力清单。

---

# Step19 创建 Change Metadata

生成：

```yaml
change_id:

requirement_id:

change_type:

priority:

owner:

created_at:

status:
```

---

# Step20 验收标准

完成后必须满足：

```text
□ proposal.md 已生成

□ design.md 已生成

□ tasks.md 已生成

□ acceptance.md 已生成

□ test-plan.md 已生成

□ spec.md 已生成

□ trace.md 已生成

□ requirement trace 已更新

□ Change Metadata 已生成

□ Design System影响已识别

□ API影响已识别

□ Database影响已识别

□ Storage影响已识别
```

---

# 输出

最终输出：

```text
1. Requirement分析

2. Impact分析

3. Change信息

4. OpenSpec文件列表

5. 工作量预估

6. 建议Sprint

7. 风险

8. 后续动作
```
