---
purpose: 数据目录与数据资产管理规范
content: data 目录用途、提交边界、样例数据、运行时数据、数据脱敏、AI 更新规则
source: Harness Token 优化模板
update_method: 新增数据类型、导入导出流程、上传存储策略、测试数据策略时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-14 00:00:00
note: AI 必须遵守本规范，禁止提交真实客户数据和运行时数据库文件
---

# 数据管理规范

## 1. data 目录定位

`data/` 仅用于本地开发、演示、测试样例和运行时数据承载，不作为业务源码目录。

## 2. 可提交内容

- `.gitkeep`
- `data/README.md`
- 脱敏样例文件
- 用于测试的公开样例数据
- 数据说明文档

## 3. 禁止提交内容

- 真实客户、用户、门店、订单、合同、价格协议等敏感数据
- 运行时数据库文件
- 对象存储运行时数据
- 日志文件
- 临时处理文件
- 包含手机号、姓名、地址、身份证、邮箱、密钥等敏感信息的数据

## 4. AI 更新规则

AI 如果新增以下能力，必须同步检查：

```text
□ data/README.md
□ .gitignore
□ .env.example
□ docs/04-database-design.md
□ rules/data-management.md
□ tests/fixtures/
```

适用能力包括文件上传、导入导出、备份恢复、样例数据生成、测试 fixture、数据库初始化脚本、数据清理任务等。

## 5. 运行时数据

运行时数据 SHOULD 放入：

```text
data/runtime/
data/processed/
data/tmp/
data/object-storage/
```

若项目采用其他运行时数据卷路径，必须在 `data/README.md`、`.gitignore`、部署文档中明确提交边界。
