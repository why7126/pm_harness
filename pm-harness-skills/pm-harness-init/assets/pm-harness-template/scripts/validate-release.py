#!/usr/bin/env python3
"""Validate product release metadata and public announcement safety."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASES_DIR = ROOT / "releases"

REQUIRED_GATES = (
    "openspec_archive",
    "tests",
    "client_generation",
    "docker_compose",
    "database_migration",
    "env_example",
    "product_version",
    "announcement_preview",
)

IMPACT_KEYS = (
    "web_admin",
    "web_public",
    "miniapp",
    "backend",
    "database",
    "object_storage",
    "docker",
)

SENSITIVE_PATTERNS = (
    re.compile(r"\bAPP_SECRET_KEY\s*=", re.I),
    re.compile(r"\bDATABASE_URL\s*=", re.I),
    re.compile(r"\b[A-Za-z0-9_]+://[^/\s:]+:[^@\s]+@", re.I),
    re.compile(r"\bMINIO_SECRET_KEY\s*=", re.I),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.I),
    re.compile(r"\bpassword\s*=", re.I),
)

NO_IMPACT_VALUES = {"", "none", "na", "n/a", "not_applicable", "not applicable", "无", "不涉及"}
DATABASE_EVIDENCE_PATTERNS = (
    re.compile(r"schema\.[A-Za-z0-9_-]+\.sql", re.I),
    re.compile(r"\bmigration\b", re.I),
    re.compile(r"迁移"),
)
DATABASE_CHECK_PATTERNS = (
    re.compile(r"schema\s*drift", re.I),
    re.compile(r"information_schema", re.I),
    re.compile(r"\bsmoke\b", re.I),
    re.compile(r"目标数据库"),
    re.compile(r"生产数据库"),
)
DATABASE_ROLLBACK_PATTERNS = (
    re.compile(r"rollback", re.I),
    re.compile(r"backup", re.I),
    re.compile(r"回滚"),
    re.compile(r"备份"),
)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON {path}: {exc}") from None
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def extract_product_version(path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.search(r"PRODUCT_VERSION\s*=\s*['\"]([^'\"]+)['\"]", text)
    if not match:
        raise ValueError(f"PRODUCT_VERSION not found in {path}")
    return match.group(1)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def gate_is_passing(name: str, gate: Any, errors: list[str]) -> None:
    if not isinstance(gate, dict):
        errors.append(f"gate {name} must be an object")
        return
    status = str(gate.get("status", "")).lower()
    if status == "pass":
        require(bool(gate.get("evidence")), f"gate {name} status pass requires evidence", errors)
        return
    if status == "na":
        require(bool(gate.get("rationale")), f"gate {name} status na requires rationale", errors)
        return
    errors.append(f"gate {name} must be pass or na, got {status or '<missing>'}")


def impact_value_requires_gate(value: Any) -> bool:
    return str(value or "").strip().lower() not in NO_IMPACT_VALUES


def validate_database_impact_gate(data: dict[str, Any], errors: list[str]) -> None:
    impact = data.get("impact_scope")
    gates = data.get("gates")
    if not isinstance(impact, dict) or not isinstance(gates, dict):
        return
    if not impact_value_requires_gate(impact.get("database")):
        return

    gate = gates.get("database_migration")
    if not isinstance(gate, dict):
        return
    status = str(gate.get("status", "")).lower()
    if status != "pass":
        errors.append("database impact requires gate database_migration status pass")
        return

    evidence = str(gate.get("evidence", ""))
    require(
        any(pattern.search(evidence) for pattern in DATABASE_EVIDENCE_PATTERNS),
        "database impact requires database_migration evidence to mention migration or schema SQL",
        errors,
    )
    require(
        any(pattern.search(evidence) for pattern in DATABASE_CHECK_PATTERNS),
        "database impact requires schema drift, target database smoke, or information_schema evidence",
        errors,
    )
    require(
        any(pattern.search(evidence) for pattern in DATABASE_ROLLBACK_PATTERNS),
        "database impact requires database rollback or backup evidence",
        errors,
    )


def scan_public_safety(release_dir: Path, release_data: dict[str, Any], errors: list[str]) -> None:
    announcement_name = release_data.get("announcement", "announcement.mdx")
    announcement_path = release_dir / str(announcement_name)
    if not announcement_path.exists():
        errors.append(f"announcement file missing: {announcement_path}")
        return
    combined = json.dumps(release_data, ensure_ascii=False) + "\n" + announcement_path.read_text(encoding="utf-8")
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(combined):
            errors.append(f"public announcement or metadata contains sensitive pattern: {pattern.pattern}")


def validate_release(release_dir: Path, product_version_file: Path | None = None) -> list[str]:
    errors: list[str] = []
    data = load_json(release_dir / "release.json")

    version = str(data.get("version", ""))
    require(bool(re.fullmatch(r"v\d+\.\d+\.\d+(?:[-.][A-Za-z0-9.]+)?", version)), "version must be SemVer-like, e.g. v0.1.0", errors)
    require(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", str(data.get("release_time", "")))), "release_time must be YYYY-MM-DD HH:mm:ss", errors)
    require(bool(data.get("owner")), "owner is required", errors)
    require(data.get("formal_scope_only") is True, "formal_scope_only must be true", errors)

    sprints = data.get("sprints")
    require(isinstance(sprints, list), "sprints must be a list", errors)
    for key in ("requirements", "bugs", "changes", "known_issues", "upgrade_steps"):
        require(isinstance(data.get(key), list), f"{key} must be a list", errors)
    require(isinstance(data.get("rollback"), dict), "rollback must be an object", errors)

    impact = data.get("impact_scope")
    require(isinstance(impact, dict), "impact_scope must be an object", errors)
    if isinstance(impact, dict):
        for key in IMPACT_KEYS:
            require(key in impact, f"impact_scope.{key} is required", errors)

    gates = data.get("gates")
    require(isinstance(gates, dict), "gates must be an object", errors)
    if isinstance(gates, dict):
        for name in REQUIRED_GATES:
            require(name in gates, f"gate {name} is required", errors)
            if name in gates:
                gate_is_passing(name, gates[name], errors)
    validate_database_impact_gate(data, errors)

    product_version = extract_product_version(product_version_file)
    if product_version is not None and version != product_version:
        require(bool(data.get("version_change_rationale")), "version differs from PRODUCT_VERSION and version_change_rationale is empty", errors)

    require((release_dir.parent / "mint.json").exists(), f"release docs config missing: {release_dir.parent / 'mint.json'}", errors)
    scan_public_safety(release_dir, data, errors)
    return errors


def release_dirs_from_args(path: str | None) -> list[Path]:
    if path:
        return [Path(path).resolve()]
    if not RELEASES_DIR.exists():
        return []
    return sorted(p for p in RELEASES_DIR.iterdir() if p.is_dir() and re.fullmatch(r"v\d+\.\d+\.\d+(?:[-.][A-Za-z0-9.]+)?", p.name))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate product release metadata and announcement source.")
    parser.add_argument("--release-dir", help="Release directory such as releases/v0.1.0")
    parser.add_argument("--product-version-file", help="Optional source file containing PRODUCT_VERSION")
    args = parser.parse_args()

    release_dirs = release_dirs_from_args(args.release_dir)
    if not release_dirs:
        print("No versioned release directories found; templates only.")
        return 0

    all_errors: list[str] = []
    product_version_file = Path(args.product_version_file).resolve() if args.product_version_file else None
    for release_dir in release_dirs:
        errors = validate_release(release_dir, product_version_file)
        if errors:
            all_errors.append(f"{release_dir}:")
            all_errors.extend(f"  - {error}" for error in errors)

    if all_errors:
        print("Release validation failed:")
        for error in all_errors:
            print(error)
        return 1

    print(f"Release validation passed for {len(release_dirs)} release(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
