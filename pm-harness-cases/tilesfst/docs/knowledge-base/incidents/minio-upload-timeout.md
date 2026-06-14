---
title: MinIO上传超时复盘示例
purpose: 提供故障复盘示例
content: 项目模板文档
source: AI自动生成，人工确认
update_method: 相关流程或内容变化时更新
owner: 项目文档负责人
status: draft
note: 企业初始化模板
---

# MinIO上传超时复盘

## 现象

上传大视频时接口超时。

## 可能原因

- 后端请求超时
- Nginx上传限制
- 临时目录空间不足
- MinIO连接异常

## 经验沉淀

大文件上传能力必须同时更新：

- `.env.example`
- Docker Compose
- 后端上传限制
- OpenSpec验收标准
