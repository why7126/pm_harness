---
purpose: 兼容性目录入口
content: 说明 compatibility 目录下数据库、设备端、对象存储等独立兼容模块的职责、生成规则和同步要求
source: Harness compatibility/README.md 抽象模板
update_method: 新增端形态、数据库、对象存储、运行环境或兼容目标时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-06-27 08:44:18
owner: {COMPATIBILITY_OWNER}
status: draft
note: 适用于 {PRODUCT_NAME} 项目
template_scope: 可作为工程初始化时的 compatibility/README.md 模块
---

# 兼容性模块索引

## 0. 目录定位 `[通用]`

`compatibility/` 用于沉淀项目级兼容性事实源，覆盖端设备、数据库、对象存储、运行环境和部署差异。

兼容性规则总入口见 `rules/compatibility.md`；本目录保存可独立维护、可独立测试的专项适配说明。

## 1. 初始化参数 `[个性化]`

| 参数 | 说明 | 示例 |
|---|---|---|
| `{PRODUCT_NAME}` | 产品名称 | 待确认 |
| `{PRODUCT_FORMS}` | 产品形态 | Web、微信小程序、H5、桌面端 |
| `{DATABASE_STACK}` | 数据库栈 | SQLite / PostgreSQL / MySQL |
| `{XINCHUANG_DATABASES}` | 信创数据库 | 达梦 / 海量 / 无 |
| `{OBJECT_STORAGE_STACK}` | 对象存储 | MinIO / S3 / COS / OSS / OBS |
| `{COMPATIBILITY_OWNER}` | 兼容性负责人 | 待确认 |

## 2. 模块清单 `[通用 + 条件启用]`

| 模块 | 文件 | 启用条件 |
|---|---|---|
| 数据库迁移规则 | `database/migration-rules.md` | 使用数据库时 |
| 数据库测试矩阵 | `database/test-matrix.md` | 使用数据库时 |
| SQLite | `database/sqlite.md` | 主库或测试库使用 SQLite |
| PostgreSQL | `database/postgresql.md` | 声明支持 PostgreSQL |
| MySQL | `database/mysql.md` | 声明支持 MySQL |
| 达梦 DM | `database/dm.md` | 信创数据库包含达梦 |
| 海量 HighGo | `database/highgo.md` | 信创数据库包含海量 |
| Web | `devices/web.md` | 产品形态包含 Web 或管理后台 |
| 微信小程序 | `devices/wechat-miniapp.md` | 产品形态包含微信小程序 |
| H5 | `devices/h5.md` | 产品形态包含移动端 H5 |
| 桌面端 | `devices/desktop.md` | 产品形态包含桌面端 |
| Android | `devices/android.md` | 产品形态包含 Android |
| iOS | `devices/ios.md` | 产品形态包含 iOS |
| MinIO | `object-storage/minio.md` | 对象存储包含 MinIO |
| S3 | `object-storage/s3.md` | 对象存储包含 S3 或 S3 Compatible |
| COS | `object-storage/cos.md` | 对象存储包含腾讯 COS |
| OSS | `object-storage/oss.md` | 对象存储包含阿里云 OSS |
| OBS | `object-storage/obs.md` | 对象存储包含华为 OBS |
| RustFS | `object-storage/rustfs.md` | 对象存储包含 RustFS |

## 3. 生成规则 `[通用]`

- 未启用的端、数据库、对象存储文档不得作为强制兼容要求保留。
- 启用但信息未知的模块必须写 `待确认`，不得编造版本、厂商、测试结果或客户环境。
- 兼容范围必须可验证，不能只写“主流浏览器”“常见数据库”。
- 兼容性变更必须同步 `docs/05-compatibility-matrix.md`、`rules/compatibility.md`、测试和发布说明。

## 4. AI 更新规则 `[通用]`

AI Agent 修改端能力、数据库、对象存储、部署方式或兼容范围时，必须先读取本目录对应模块，并同步更新测试矩阵。不得伪造兼容测试通过结果。
