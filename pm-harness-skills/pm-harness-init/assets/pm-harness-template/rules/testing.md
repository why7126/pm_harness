---
purpose: 全局规则
content: 团队研发规范和AI约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于{PRODUCT_NAME}项目模板
---

# 测试规范

后端使用 pytest；前端使用 Vitest/Testing Library；接口变更必须补充集成测试。

涉及 API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装、App 请求封装或工作流治理的变更，测试计划 MUST 读取 `docs/standards/product-data-collection-observability.md`，覆盖 `product_data_collection_observability` 声明、`affected_layers` 适用层级、`reason` 原因和 `validation` 结果；不适用时写明 N/A 或 `not_applicable` 原因。
