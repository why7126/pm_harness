---
purpose: 产品版本发布目录
content: 发布对象、公开公告源文件、模板和发布校验边界
source: PM Harness 通用发布治理模块
update_method: 发布流程、公告格式或发布门禁变化时更新
created_at: 2026-07-23 00:00:00
updated_at: 2026-07-23 00:00:00
note: releases/ 不替代 iterations、issues 或 openspec；仅记录对外产品版本发布事实
---

# 产品版本发布目录

`releases/` 用于承载对外产品版本发布对象、公开公告源文件、发布校验材料和静态文档配置。

## 目录结构

```text
releases/
├── README.md
├── mint.json
├── templates/
│   ├── release.json
│   └── announcement.mdx
└── v0.1.0/
    ├── release.json
    └── announcement.mdx
```

## 文件职责

| 文件 | 职责 |
|---|---|
| `vX.Y.Z/release.json` | 机器可读发布事实源，关联 Sprint、REQ、BUG、OpenSpec Change、影响范围和门禁证据 |
| `vX.Y.Z/announcement.mdx` | 面向公开页面或客户交付的发布公告源文件 |
| `templates/release.json` | 发布对象模板 |
| `templates/announcement.mdx` | 公告模板 |
| `mint.json` | Mintlify 或等价静态文档预览配置；未使用 Mintlify 时保留为公告站点配置示例 |

## 边界

- MUST 只存放产品版本发布对象、公开公告源文件、发布校验记录和静态公告站点配置。
- MUST NOT 替代 `iterations/` 四件套、`issues/` 需求/BUG 文档、`openspec/changes/` 变更事实源或 `docs/` 长期技术文档。
- MUST NOT 存放构建产物、真实客户数据、密钥、数据库连接串、对象存储凭据或不可公开运维信息。
- 版本目录 SHOULD 使用 SemVer 风格，例如 `v0.1.0/`。
- 公告发布时间字段 MUST 使用 `YYYY-MM-DD HH:mm:ss`。

## 校验

发布前运行：

```bash
python scripts/validate-release.py --release-dir releases/v0.1.0
```

没有任何版本目录时，校验脚本只确认模板目录存在并返回通过。
