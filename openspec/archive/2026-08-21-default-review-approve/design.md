---
created_at: 2026-08-21 13:16:11
updated_at: 2026-08-21 13:16:11
---

# Design

## Command Semantics

The review commands use an explicit negative-outcome model:

- No flag means `approve`.
- `--approve` remains accepted and maps to the same path as no flag.
- `--reject`, `--defer`, and BUG-only `--wont-fix` must be explicit.

This preserves the lifecycle gate because downstream commands still check for `approved` or `in_sprint`. The change only removes redundant syntax for the normal review path.

## Audit Text

Promotion reasons should describe the effective command behavior, not force the old spelling. Review skills should use a reason such as:

```bash
/req-review (default approve)
/bug-review (default approve)
```

When the user explicitly supplies `--approve`, the command may still record the explicit command form.

## Synchronization

Because this behavior is part of reusable Harness command ergonomics, the same updates must be applied to:

- Root project `.agents/skills/`.
- `pm-harness/.agents/skills/`.
- `pm-harness-skills/pm-harness-init/assets/pm-harness-template/.agents/skills/`.
- Template lifecycle rule examples where they still instruct users to add `--approve`.
