---
purpose: 数据库文档
content: SQLite表结构设计
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# 数据库设计


## 核心表

- `tiles`：瓷砖主表
- `tile_categories`：分类表
- `tile_specs`：规格表
- `tile_images`：图片表
- `users`：用户表（认证与角色）
- `login_logs`：登录日志表（预留）

### users 表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | TEXT PK | 用户 UUID |
| username | TEXT UNIQUE | 登录用户名 |
| phone | TEXT | 手机号（预留） |
| email | TEXT | 邮箱（预留） |
| password_hash | TEXT | bcrypt 哈希 |
| display_name | TEXT | 显示名称 |
| role | TEXT | `admin` / `employee` / `store_owner` |
| status | TEXT | `active` / `disabled` |
| last_login_at | TEXT | 最近登录时间 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### login_logs 表（预留）

| 字段 | 说明 |
|---|---|
| id | 日志 ID |
| user_id | 用户 ID |
| login_identifier | 脱敏登录标识 |
| result | `success` / `failed` |
| failure_reason | 失败原因 |
| ip | 登录 IP |
| user_agent | 客户端信息 |
| created_at | 创建时间 |

## 设计原则

SQLite 存储结构化数据，MinIO 存储图片文件。


## 媒体资产表建议

建议新增 `tile_media` 表统一管理图片、视频和文档：

| 字段 | 说明 |
|---|---|
| id | 媒体ID |
| tile_id | 瓷砖ID |
| media_type | image/video/document |
| bucket_name | MinIO存储桶 |
| object_key | 对象Key |
| mime_type | MIME类型 |
| file_size | 文件大小 |
| width | 图片/视频宽度 |
| height | 图片/视频高度 |
| duration | 视频时长 |
| cover_object_key | 视频封面对象Key |
| sort_order | 排序 |
| created_at | 创建时间 |
