---
purpose: 命令执行顺序速查
content: ProjectPmHarness REQ/BUG、Sprint、OpenSpec、发布、镜像、产品手册与治理命令的推荐顺序
created_at: 2026-08-10 23:19:03
updated_at: 2026-08-27 01:02:22
---

# 命令执行顺序速查

## 标准链路

```text
/capture
-> /req-* 或 /bug-*
-> /sprint-propose
-> /req-opsx 或 /bug-opsx
-> /opsx-apply
-> /opsx-modify（可选）
-> /opsx-archive
-> /sprint-archive
-> /sprint-exps
-> /release-propose
-> /release-prepare
-> /usage-docs-generate|update|validate
-> /image-prepare
-> /image-build
-> /upgrade-plan（按需）
-> /upgrade-validate（按需）
-> /release-publish
```

纯治理学习或规范优化可使用：

```text
/spec-study <project>
-> /spec-study apply <confirmed-items>
```

```text
/spec-opt <governance-goal>
```

## REQ / BUG 到 OpenSpec

- 未评审的 REQ/BUG 不得进入 Sprint、不得转 OpenSpec、不得执行开发。
- 已评审 REQ/BUG MUST 先纳入 Sprint，再创建 Change。
- 来源于 REQ/BUG 的下一步命令 SHOULD 保留完整 `REQ-xxxx-slug` 或 `BUG-xxxx-slug`，避免中途改用裸 Change ID 造成链路断裂。
- 无 REQ/BUG 来源的纯治理 Change 才直接使用 `<change-id>`。

## 串行写入边界

会写同一事实源的命令必须串行执行，包括 Sprint scope 更新、Workflow Sync、Issue promote、AI Usage snapshot 和归档证据生成。

## 最小相关验证矩阵

选择验证前 SHOULD 先看本次 diff scope 和触达面。已通过且未被后续改动影响的检查，不需要因为最终汇报而机械重复；CI 负责全量矩阵，本地命令负责提供与本次变更相匹配的最小相关证据。

| 触达范围 | 最小相关校验 |
|---|---|
| `.agents/skills/`、`rules/agent-context-budget.md` | `python scripts/validate-agent-context-budget.py` |
| OpenSpec Change 文档或 delta spec | `python scripts/validate-openspec-language.py`、`openspec validate <change-id>` |
| 目录边界、docs、issues、iterations、releases、mintlify、deploy | `python scripts/validate-directory-structure.py` |
| 长期文档、规则、技能说明、知识库 | `python scripts/validate-doc-prose-hygiene.py <focused-paths>` |
| 产品数据采集、链路观测、日志审计、Task Trace 或端请求封装 | `python scripts/validate-product-data-observability-standard.py`、`python scripts/validate-product-data-observability-gates.py --change <change-id>` |
| BUG review approve | `python scripts/validate-root-cause-evidence.py --bug <BUG-id> --require-confirmed` |
| BUG 根因、返修根因或问题排查证据 | `python scripts/validate-root-cause-evidence.py --bug <BUG-id>` 或 `--change <change-id>` |
| Sprint 选择、创建或追加范围 | `python scripts/validate-sprint-selection.py [--sprint <sprint-id>]`、`python scripts/validate-sprint-scope.py <sprint-id> [--item <REQ|BUG|change-id>]` |
| Sprint 归档、`sprint.md` 收口或复盘输入 | `python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id>`、`python scripts/check-sprint-close-stale-scan.py --sprint <sprint-id>`、`python scripts/generate-sprint-fact-sheet.py --sprint <sprint-id> --summary` |
| 发布对象、公告、usage docs、Mintlify | release、usage-docs、Mintlify 和公开安全校验 |
| 镜像构建或离线交付 | `python scripts/validate-image-build.py` 对应 plan/manifest 校验 |
| 版本升级路径 | `python scripts/validate-release-upgrade.py validate-plan --plan <path>` |
| 安全 / env / 本地数据 | `python scripts/git-check.py` 或聚焦安全脚本 |

## 输出边界

「下一步」只放可直接执行的命令；「待用户决策/处理」只放缺失输入、范围选择、证据补充、验收或发布确认、阻塞项。

## 命令执行复盘 Hook

所有 workflow 命令完成后 MUST 输出：

```text
执行链路复盘：
- 链路状态：正常 / warning / blocked
- 问题证据：无 / <脚本输出、文件路径、校验报告、日志摘要或用户证据>
- 规范优化建议：无明显优化点 / <建议命令或标准 capture 文案>
- follow-up 状态：未自动创建 Issue/Change
```

`正常` 只能用于必需校验、Workflow Sync 与 AI Usage hook 通过，或该命令明确不适用对应 hook 的情况。`warning` 用于非阻塞问题、可选 hook 跳过、局部校验未覆盖或发现可优化规范点。`blocked` 用于必需门禁失败、缺少补证导致无法定根因或验收、或脚本显示事实源不一致。

默认不自动创建 follow-up Issue/Change；如需沉淀新问题，只输出建议命令或 capture 文案，等待用户明确授权。
