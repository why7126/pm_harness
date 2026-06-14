---
purpose: 数据目录与数据资产管理规范
content: data目录用途、提交边界、样例数据、运行时数据、数据脱敏、AI更新规则
source: AI自动生成初稿，项目团队确认
update_method: 新增数据类型、导入导出流程、上传存储策略、测试数据策略时更新
note: AI必须遵守本规范，禁止提交真实客户数据和运行时数据库文件
---

# 数据管理规范

## 1. data目录定位

`data/` 仅用于本地开发、演示、测试样例和运行时数据承载，不作为业务源码目录。

## 2. 可提交内容

- `.gitkeep`
- `data/README.md`
- 脱敏样例图片
- 脱敏样例视频
- 用于测试的公开样例数据
- 数据说明文档

## 3. 禁止提交内容

- 真实门店数据
- 真实客户图片或视频
- SQLite运行时数据库文件
- MinIO运行时数据
- 日志文件
- 临时转码文件
- 包含手机号、姓名、地址、价格协议等敏感信息的数据

## 4. AI生成/更新规则

AI如果新增以下能力：

- 文件上传
- 图片管理
- 视频管理
- Excel导入导出
- 数据备份恢复
- 样例数据生成
- SQLite初始化脚本

必须同步更新：

```text
data/README.md
.gitignore
.env.example
docs/04-database-design.md
rules/data-management.md
tests/fixtures/
```

## 5. 样例数据规则

样例数据必须满足：

- 可公开
- 已脱敏
- 不包含真实客户信息
- 文件大小适合Git管理
- 有明确用途说明

## 6. 运行时数据规则

运行时数据必须放入：

```text
data/runtime/
data/uploads/
data/processed/
data/tmp/
```

上述目录默认不提交Git。
