---
purpose: 兼容性矩阵
content: 产品形态、浏览器/端、数据库、对象存储、部署和能力兼容性
source: Harness docs Token 优化模板，初始化时基于产品形态和兼容目标生成
update_method: 支持端、运行时、数据库、对象存储、部署环境或兼容承诺变化时更新
created_at: 2026-06-27 08:44:18
updated_at: 2026-07-14 00:00:00
owner: {DOCS_OWNER}
note: 详细适配说明放在 compatibility/ 目录
---

# 兼容性矩阵

## 1. 产品形态

| 能力 | Web | Admin | H5 | 小程序 | Android | iOS | Desktop |
|---|---|---|---|---|---|---|---|
| `{CAPABILITY}` | 待确认 | 待确认 | 待确认 | 待确认 | 待确认 | 待确认 | 待确认 |

## 2. 运行环境

| 类型 | 支持范围 | 说明 |
|---|---|---|
| 浏览器 | `{BROWSER_SUPPORT}` | 见 `compatibility/devices/web.md` |
| 移动端 | `{MOBILE_SUPPORT}` | 见对应端文档 |
| 数据库 | `{DATABASE_SUPPORT}` | 见 `compatibility/database/` |
| 对象存储 | `{OBJECT_STORAGE_SUPPORT}` | 见 `compatibility/object-storage/` |
| 部署 | `{DEPLOYMENT_SUPPORT}` | 见 `docs/02-deployment.md` |

## 3. 更新规则

- 新增或取消支持端时，同步本文件、`compatibility/devices/` 和 `rules/compatibility.md`。
- 新增数据库或对象存储适配时，同步 `compatibility/`、部署文档和测试矩阵。
- 兼容性声明必须有测试、手工验收或明确的“待确认”标记。
