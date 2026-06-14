---
title: 系统架构
purpose: 描述系统模块、前后端分层、对象存储、数据流和AI开发边界
content: 项目模板文档
source: AI自动生成，人工确认
update_method: 相关流程或内容变化时更新
owner: 项目文档负责人
status: draft
note: 企业初始化模板
---

# 系统架构

## 1. 总体架构

```text
Web端 / 微信小程序 / 管理端
        ↓
FastAPI Backend
        ↓
SQLite + MinIO
```

## 2. 后端分层

```text
api → schemas → services → repositories → models
```

## 3. 媒体资源链路

```text
上传文件
  ↓
后端校验
  ↓
MinIO单桶存储
  ↓
SQLite保存元数据
  ↓
前端展示
```

## 4. AI边界

AI必须基于 `issues/` 与 `openspec/` 开发，不允许直接凭空修改 `src/`。
