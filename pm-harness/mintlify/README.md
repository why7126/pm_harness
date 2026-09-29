---
created_at: 2026-08-04 00:00:00
updated_at: 2026-08-04 00:00:00
purpose: Mintlify 公开产品文档站源目录说明
---

# Mintlify 文档站源目录

`mintlify/` 承载公开产品文档站源文件、Mintlify 配置、公告投影和可公开截图资产。

- `releases/vX.Y.Z/usage-docs/` 是版本产品使用文档事实源和发布快照。
- `mintlify/docs/vX.Y.Z/` 由 release 快照同步或投影生成。
- `mintlify/docs/latest/` 指向最新已生成并校验通过的版本。
- `mintlify/assets/screenshots/` 集中存放可公开截图资产。

本目录不得存放构建产物、真实客户数据、密钥、数据库连接串、真实 `.env`、Authorization header、Cookie、运行时数据库或不可公开运维信息。
