---
purpose: OpenSpec项目上下文
content: 项目背景、技术栈、AI约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# 项目上下文


## 项目背景

瓷砖信息管理平台服务于瓷砖企业和零售店主，提供产品资料展示、查询和维护能力。

## 技术栈

- 后端：Python3.12、FastAPI、Pydantic、uv、SQLite、MinIO
- 前端：React19、TypeScript、Tailwind、shadcn/ui、Axios、Orval、pnpm
- 小程序：微信小程序

## 研发规则

- 需求来源：`issues/requirements`
- BUG来源：`issues/bugs`
- 研发变更：`openspec/changes`
- 正式能力：`openspec/specs`


## AI执行约束

AI必须先阅读本文件和对应 OpenSpec Change，再进行代码修改。
