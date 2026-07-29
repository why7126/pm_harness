from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MARKER_PREFIX = "workflow-sync"

SCOPE_MARKERS = {
    "requirements": f"{MARKER_PREFIX}:scope-requirements",
    "bugs": f"{MARKER_PREFIX}:scope-bugs",
    "changes": f"{MARKER_PREFIX}:scope-changes",
    "release_status": f"{MARKER_PREFIX}:release-status",
}

ISSUE_DONE_STATUSES = frozenset({"done", "archived", "resolved", "closed"})
ISSUE_ACTIVE_SPRINT_STATUSES = frozenset({"approved", "in_sprint", "applied"})

CHANGE_TO_ISSUE_STATUS = {
    "archived": "done",
    "applied": "in_sprint",
    "in_progress": "in_sprint",
    "proposed": "in_sprint",
    "not_started": "approved",
}

# Issue lifecycle events: sprint sync only when the target REQ/BUG is in sprint scope.
ISSUE_SCOPED_EVENTS = frozenset(
    {
        "req.capture",
        "req.generate",
        "req.complete",
        "req.review",
        "req.opsx",
        "bug.capture",
        "bug.generate",
        "bug.complete",
        "bug.review",
        "bug.opsx",
    }
)

# Change lifecycle events: sprint sync only when the target change is in sprint scope.
CHANGE_SCOPED_EVENTS = frozenset(
    {
        "opsx.propose",
        "opsx.apply",
        "opsx.archive",
    }
)
