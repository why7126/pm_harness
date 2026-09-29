---
created_at: 2026-08-27 00:26:26
updated_at: 2026-08-27 00:26:26
---

# TilesFST 数据采集治理学习应用

## 输入

- 命令：`/spec-study apply TilesFST product-data-collection-observability-standard product-data-observability-hard-gate workflow-skill-data-collection-gate`
- 学习对象：`ProjectTilesFST`
- 应用 Change：`add-tilesfst-data-observability-governance`
- Sprint：`sprint-001`

## 学习结论

TilesFST 在产品数据采集治理上提供了三类可迁移能力：

- 建立产品数据采集、请求日志、Task Trace 和端请求封装的统一标准。
- 使用脚本校验标准完整性和 REQ/BUG/Change/Sprint 的触达面声明。
- 在 REQ、OpenSpec、Sprint 工作流 Skill 中前置数据采集声明门禁。

本项目采纳治理结构与门禁思想，不复制 TilesFST 业务实现、表结构、接口路径、运行日志或端侧实现细节。

## 应用结果

- 新增 `docs/standards/product-data-collection-observability.md`。
- 新增 `scripts/validate-product-data-observability-standard.py`。
- 新增 `scripts/validate-product-data-observability-gates.py`。
- 更新 `AGENTS.md`、`docs/README.md`、`docs/08-command-execution-order.md`、`rules/document-governance.md`。
- 更新 REQ、OpenSpec、Sprint 工作流 Skill 的产品数据采集与链路观测门禁。
- 同步 `pm-harness/` 和 `pm-harness-skills/pm-harness-init/assets/pm-harness-template/`。
- 新建并纳入 `openspec/changes/add-tilesfst-data-observability-governance/`。

## product_data_collection_observability

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - workflow_governance
  reason: 本次应用建立工作流治理层的数据采集观测标准和硬门禁；不触达业务 API、DB、端请求封装或运行时日志数据。
  validation: 运行标准校验、Change 门禁、OpenSpec、目录、模板同步、Workflow Sync、AI Usage 和只读保护复核。
```

## 只读保护

学习阶段只读参考 TilesFST 治理资产。应用阶段仅修改 ProjectPmHarness 当前仓库治理资产、模板资产和 active Change/Sprint 事实源。

## 验证

计划执行以下最小相关验证：

- `python scripts/validate-product-data-observability-standard.py`
- `python scripts/validate-product-data-observability-gates.py --change add-tilesfst-data-observability-governance`
- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate add-tilesfst-data-observability-governance`
- `python pm-harness/scripts/validate-template-sync.py`
- `python pm-harness/scripts/validate-directory-structure.py`
- `python pm-harness/scripts/validate-skill-package.py`
- `python pm-harness/scripts/validate-agent-context-budget.py`
- `python pm-harness/scripts/validate-product-data-observability-standard.py`
- `python pm-harness/scripts/validate-product-data-observability-gates.py`
