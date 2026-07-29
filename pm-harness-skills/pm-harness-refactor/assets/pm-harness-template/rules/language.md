---
purpose: 全局规则
content: 团队研发规范和AI约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-03 23:29:19
note: 适用于{PRODUCT_NAME}项目模板
---

# 语言规范

产品、需求、设计、测试、OpenSpec 规范正文和长期治理文档 MUST 使用中文优先编写；代码标识符使用英文；API 字段使用英文 snake_case 或 camelCase，按接口约定统一。

## OpenSpec 语言规则

- `openspec/specs/**/spec.md` 与 `openspec/changes/**/specs/**/spec.md` 中的业务能力标题、需求说明、场景名称和验收描述 MUST 使用中文。
- OpenSpec 解析关键字 MAY 保留英文，例如 `Requirement`、`Scenario`、`MUST`、`SHALL`、`WHEN`、`THEN`、`AND`，以保证 CLI 校验稳定。
- API 路径、HTTP 方法、数据库表名、字段名、枚举值、代码类名、文件路径、命令、产品英文专名（如 客户端生成、Mintlify、Docker、Swagger）MAY 保留英文。
- 归档后生成的 `Purpose` 不得保留 `TBD - created by archiving...` 等脚手架占位文案；应改为中文能力说明。
