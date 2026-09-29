---
created_at: 2026-08-21 13:16:11
updated_at: 2026-08-21 13:16:11
---

# Proposal

## Why

`/req-review` and `/bug-review` are high-frequency governance commands whose happy path is review approval. Requiring `--approve` on every approved review adds friction, while the negative outcomes still need explicit intent.

The current command guidance is also inconsistent: `/req-review` says no flag asks the user, while `/bug-review` does not define no-flag behavior. Downstream examples still recommend `--approve`, even though lifecycle rules only require the resulting `approved` state before Sprint and OpenSpec gates.

## What Changes

- Make no-flag `/req-review <REQ-id>` default to approved.
- Make no-flag `/bug-review <BUG-id>` default to approved.
- Keep `--approve` as a supported compatibility alias.
- Keep non-approval outcomes explicit via `--reject`, `--defer`, and `--wont-fix` for BUG.
- Update command examples and template assets so future projects inherit the same behavior.

## Impact

- Affects governance command skills and command examples only.
- Does not change business runtime code, API, DB schema, Web, miniapp, admin, Orval, or Docker behavior.
