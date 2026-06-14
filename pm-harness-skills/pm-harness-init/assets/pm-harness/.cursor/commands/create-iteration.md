# Create Iteration

## 目标

根据当前项目中的需求（Requirement）、缺陷（Bug）和 OpenSpec Change，自动创建新的 Sprint（迭代）规划。

---

## 读取范围

必须读取：

```text
project.yaml

issues/requirements/**

issues/bugs/**

openspec/changes/**

iterations/**
```

同时读取：

```text
AGENTS.md

rules/requirement-management.md

rules/bug-management.md

rules/iteration-management.md

rules/openspec-workflow.md
```

---

## 创建前检查

### Requirement

仅纳入满足以下条件的需求：

```text
requirement.md 已存在

acceptance.md 已存在

trace.md 已存在

状态为：

Approved
Ready
```

---

### Bug

仅纳入满足以下条件的BUG：

```text
bug.md 已存在

root-cause.md 已存在

acceptance.md 已存在

状态为：

Open
Ready
```

---

### OpenSpec Change

仅纳入满足以下条件的 Change：

```text
proposal.md 已完成

design.md 已完成

tasks.md 已完成

test-plan.md 已完成
```

状态：

```text
Ready
```

---

## 容量规划

读取：

```text
project.yaml
```

获取：

```yaml
team:
  developers:
  testers:

iteration:
  duration:
```

如果不存在：

默认：

```yaml
developers: 2
testers: 1
duration: 2周
```

---

## 工作量估算

按以下标准估算：

```text
XS = 0.5人天

S  = 1人天

M  = 3人天

L  = 5人天

XL = 8人天

XXL = 13人天
```

估算：

```text
前端
后端
数据库
测试
```

总工作量。

---

## 迭代拆分原则

优先级：

```text
P0 BUG

P1 Requirement

P2 Requirement

P3 Requirement
```

优先处理：

```text
Blocker

Critical

High
```

---

## 功能归组原则

尽量把同一业务域放在同一Sprint。

例如：

```text
Tile Management

Tile Media

Tile Search
```

属于：

```text
产品管理域
```

应优先放在同一个Sprint。

---

## 创建迭代

创建：

```text
iterations/
└── sprint-XX/
```

---

生成：

```text
sprint.yaml

sprint.md

release-note.md

acceptance-report.md
```

---

## sprint.yaml

格式：

```yaml
sprint_id:

status: planning

start_date:
end_date:

capacity:
  developers:
  testers:

requirements:

bugs:

changes:

estimated_story_points:

estimated_person_days:
```

---

## sprint.md

生成：

### Sprint目标

### Scope

包含需求

包含BUG

包含Change

### 工作量估算

### 风险

### 依赖

### 发布计划

---

## release-note.md

生成初稿：

```text
新增功能

优化项

BUG修复

兼容性影响
```

---

## acceptance-report.md

生成模板：

```text
验收项

验收结果

问题清单

遗留风险
```

---

## 更新 Trace

自动更新：

```text
issues/requirements/*/trace.md

issues/bugs/*/trace.md

openspec/changes/*/trace.md
```

增加：

```yaml
iteration:
  sprint-XX
```

---

## 输出

输出：

### 本次Sprint包含

Requirements

Bugs

Changes

### 总工作量

### 风险列表

### 生成文件列表

### 后续建议
