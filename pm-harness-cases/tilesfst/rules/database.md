---
purpose: 数据库规范
content: SQLite表设计、迁移、索引、媒体元数据、软删除、审计字段规则
source: AI自动生成初稿，项目团队确认
update_method: 新增表、字段、索引、迁移或媒体元数据存储规则时更新
note: 当前项目默认使用SQLite，后续如升级数据库必须创建OpenSpec Change
---

# 数据库规范

## 1. 数据库定位

当前项目使用 SQLite，适合单体部署、演示环境、小规模门店信息管理场景。

## 2. 表设计要求

核心表建议包括：

- tiles：瓷砖主表
- tile_categories：分类
- tile_series：系列
- tile_media：图片/视频/文档媒体资产
- admin_users：企业内部员工
- audit_logs：操作日志

## 3. 通用字段

业务表建议包含：

```text
id
created_at
updated_at
deleted_at
created_by
updated_by
```

## 4. 媒体元数据

媒体表必须记录：

```text
media_type
object_key
bucket_name
mime_type
file_size
width
height
duration
cover_object_key
sort_order
```

## 5. SQLite规则

- 必须使用参数化查询。
- 需要为常用筛选条件建立索引。
- 不允许在业务代码中拼接SQL字符串。
- 迁移脚本必须可重复执行或有版本记录。

## 6. AI更新规则

AI修改数据库结构时必须同步：

```text
docs/04-database-design.md
openspec/changes/<change-id>/implementation/db.md
tests/integration/
data/README.md
```
