---
created_at: 2026-08-21 22:28:02
updated_at: 2026-08-21 22:28:02
---

# Design

## 1. 升级路径对象

发布版本事实源继续由 `releases/vX.Y.Z/release.json`、`image-build-plan.json` 与 `image-manifest.json` 承载。升级治理新增按来源版本区分的路径对象：

```text
releases/<to-version>/upgrade-plans/<from-version>-to-<to-version>.json
```

`from-version=fresh` 表示首次部署。计划只记录安全摘要、影响分类、检查清单、步骤、回滚和证据，不记录真实 env 值、密钥、连接串、本机绝对路径或客户数据。

## 2. 命令技能

新增两个技能：

- `/upgrade-plan --from <fresh|version> --to <version>`：生成并立即校验升级计划。
- `/upgrade-validate --plan <path>`：校验指定升级计划。

两个命令只做计划与校验，不执行生产升级、不写真实 env、不执行写入型 DB 或对象存储维护任务。

## 3. 通用脚本

新增 `scripts/validate-release-upgrade.py`，保留 TilesFST 中可迁移的治理形态，但改写为模板通用版本：

- 支持 `plan`、`validate-plan`、`env-diff` 子命令。
- 使用通用 `APP_IMAGE_TAG` / `IMAGE_TAG` 摘要，不绑定 `TILESFST_*`。
- 输出 env diff 仅包含变量名、分类和建议。
- 缺少跨版本完整事实或演练证据时，不得标记为 `cross-version-upgrade-supported`。

## 4. 文档卫生与验证矩阵

新增 `docs/standards/document-prose-hygiene.md` 与 `scripts/validate-doc-prose-hygiene.py`，用于启发式发现长期文档中的会话推理、临时草稿、review 对话、不可解析路径和敏感片段。

更新命令执行顺序文档，加入按 diff scope 选择最小相关校验的矩阵。矩阵只帮助选择验证范围，不替代各 Skill 的 MUST 门禁。

## 5. 模板同步

本次能力会影响未来生成的新项目，必须同步：

- `pm-harness/`
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/`

根目录 `docs/spec-logs/` 的实际学习报告不得同步进模板。
