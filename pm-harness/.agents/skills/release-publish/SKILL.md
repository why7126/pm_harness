---
name: "release-publish"
description: "记录产品版本发布确认结果和最终公告位置"
---

# release-publish

Use this skill when the user asks to run `/release-publish <version>` or record final release confirmation.

## Context Budget Guardrails（MUST）

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则用摘要承接，不重复全量读取。
- 从 `releases/<version>/release.json` 和 `announcement.mdx` 开始，按 validator/gate 报告定位问题。
- 不为发布确认全量展开关联 Sprint、Issue、Change；只有门禁证据缺失时读取对应片段。
- 输出聚焦发布结论、公告位置、门禁结果和回滚提醒。

## Input

- `<version>`：必填，例如 `v0.1.0`。
- Flags：`--announcement-url <url>`、`--published-at <YYYY-MM-DD HH:mm:ss>`、`--dry-run`、`--force`（仅用户明确确认时可用）。

## Must Read

```text
AGENTS.md
rules/document-governance.md
rules/directory-structure.md
rules/release.md
rules/security.md
rules/agent-context-budget.md
releases/<version>/release.json
releases/<version>/announcement.mdx
```

## Gates

Publish MUST be blocked unless:

- `python scripts/validate-release.py --release-dir releases/<version>` exits `0`.
- Every required gate is `pass` or correctly justified as `na`.
- Formal-scope Changes are archived, or non-archived items are explicitly outside formal scope.
- Public announcement is safe for external publication.
- Product version mismatch has explicit rationale, or the user-visible version equals `<version>`.
- User has supplied or confirmed the final announcement location if there is an external URL.

`--force` MUST NOT bypass public-safety failures or missing `release.json` / `announcement.mdx`.

## Steps

1. Validate release metadata and announcement safety.
2. Confirm publish-time fields:
   - `release_time` / published time in `YYYY-MM-DD HH:mm:ss`
   - final announcement path or URL
   - rollback and known issues are present
3. Update `releases/<version>/release.json` with publish confirmation fields if the existing schema already contains them, or append a conservative `publish_confirmation` object:

```json
{
  "published_at": "YYYY-MM-DD HH:mm:ss",
  "announcement_url": "https://example.com/releases/vX.Y.Z",
  "confirmed_by": "operator",
  "notes": "发布确认说明"
}
```

4. Re-run validation.

## Output

Report version, publish status, announcement file/URL, validation command result, gate summary, updated files, and rollback reminder.
