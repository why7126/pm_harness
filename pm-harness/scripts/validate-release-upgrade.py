#!/usr/bin/env python3
"""Generate and validate release deployment upgrade plans."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NO_IMPACT_VALUES = {"", "none", "na", "n/a", "not_applicable", "not applicable", "无", "不涉及"}
SUPPORT_LEVELS = {
    "fresh-install-supported",
    "adjacent-upgrade-supported",
    "cross-version-upgrade-supported",
    "cross-version-upgrade-requires-manual-review",
    "unsupported",
}
ENV_EXAMPLE_PATTERNS = (
    ".env.example",
    "src/backend/.env.example",
    "src/backend/.env.docker",
    "deploy/**/*.env.example",
    "scripts/build-images.env.example",
)
PRODUCTION_REQUIRED_KEY_HINTS = (
    "SECRET",
    "PASSWORD",
    "DATABASE_URL",
    "ACCESS_KEY",
    "TOKEN",
    "IMAGE_TAG",
)
UNSAFE_EXAMPLE_TOKENS = ("change-me", "replace-with", "example.com", "localhost", "sqlite:")
SENSITIVE_PATTERNS = (
    re.compile(r"\bDATABASE_URL\s*=\s*(?!<)", re.I),
    re.compile(r"\bAuthorization\s*:", re.I),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.I),
    re.compile(r"\bCookie\s*:", re.I),
    re.compile(r"/Users/[^\\s\"']+", re.I),
)


class UpgradePlanError(ValueError):
    """User-facing validation error."""


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def rel_path(path: Path, *, root: Path) -> str:
    return os.path.relpath(path.resolve(), root.resolve())


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise UpgradePlanError(f"missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise UpgradePlanError(f"invalid JSON {path}: {exc}") from None
    if not isinstance(data, dict):
        raise UpgradePlanError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def semver_key(version: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise UpgradePlanError(f"unsupported version format: {version}")
    return tuple(int(part) for part in match.groups())


def release_dir(root: Path, version: str) -> Path:
    return root / "releases" / version


def release_versions(root: Path) -> list[str]:
    base = root / "releases"
    if not base.is_dir():
        return []
    versions = [path.name for path in base.iterdir() if path.is_dir() and re.fullmatch(r"v\d+\.\d+\.\d+", path.name)]
    return sorted(versions, key=semver_key)


def previous_version(root: Path, to_version: str) -> str | None:
    versions = [version for version in release_versions(root) if semver_key(version) < semver_key(to_version)]
    return versions[-1] if versions else None


def versions_between(root: Path, from_version: str, to_version: str) -> list[str]:
    start = semver_key(from_version)
    end = semver_key(to_version)
    return [version for version in release_versions(root) if start < semver_key(version) <= end]


def release_fact(root: Path, version: str) -> dict[str, Any] | None:
    path = release_dir(root, version) / "release.json"
    return read_json(path) if path.exists() else None


def manifest_exists(root: Path, version: str) -> bool:
    data = release_fact(root, version)
    manifest_name = str(data.get("image_manifest", "image-manifest.json")) if data else "image-manifest.json"
    return (release_dir(root, version) / manifest_name).exists()


def source_confidence(root: Path, version: str) -> str:
    if version == "fresh":
        return "fresh"
    data = release_fact(root, version)
    if not data:
        return "partial"
    has_release_version = data.get("version") == version
    has_announcement = (release_dir(root, version) / str(data.get("announcement", "announcement.mdx"))).exists()
    return "verified" if has_release_version and has_announcement else "reconstructed"


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_env_text(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def env_example_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in ENV_EXAMPLE_PATTERNS:
        files.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(set(files), key=lambda path: rel_path(path, root=root))


def env_snapshot(root: Path) -> dict[str, dict[str, str]]:
    return {rel_path(path, root=root): parse_env_text(path.read_text(encoding="utf-8")) for path in env_example_files(root)}


def env_summary(snapshot: dict[str, dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {
        "required_in_production": [],
        "unsafe_example_value": [],
        "manual_review": [],
    }
    for path, values in sorted(snapshot.items()):
        for key, value in sorted(values.items()):
            key_upper = key.upper()
            if any(hint in key_upper for hint in PRODUCTION_REQUIRED_KEY_HINTS):
                result["required_in_production"].append(
                    {"path": path, "key": key, "recommendation": "生产环境必须显式配置，不得依赖示例值"}
                )
            if any(token in value.lower() for token in UNSAFE_EXAMPLE_TOKENS):
                result["unsafe_example_value"].append(
                    {"path": path, "key": key, "recommendation": "生产环境不得使用该示例值"}
                )
    if not snapshot:
        result["manual_review"].append({"path": "env examples", "key": "<none>", "recommendation": "缺少 env 示例，需人工复核部署配置"})
    return result


def impact_requires_database(release_data: dict[str, Any] | None) -> bool:
    if not isinstance(release_data, dict):
        return False
    impact = release_data.get("impact_scope")
    if not isinstance(impact, dict):
        return False
    return str(impact.get("database", "")).strip().lower() not in NO_IMPACT_VALUES


def classify_support(root: Path, from_version: str, to_version: str, blockers: list[str], warnings: list[str]) -> str:
    if blockers:
        return "unsupported"
    if from_version == "fresh":
        return "fresh-install-supported"
    if from_version == previous_version(root, to_version):
        return "adjacent-upgrade-supported"
    between = versions_between(root, from_version, to_version)
    if not between:
        return "unsupported"
    missing_release = [version for version in between if release_fact(root, version) is None]
    missing_manifest = [version for version in between if not manifest_exists(root, version)]
    if missing_release or missing_manifest:
        warnings.append(
            "跨版本路径缺少完整 release 或 image manifest 证据，需人工复核："
            f"missing_release={missing_release}, missing_manifest={missing_manifest}"
        )
        return "cross-version-upgrade-requires-manual-review"
    warnings.append("跨版本路径具备基础版本事实，仍需补充演练、DB/env/object storage 和回滚证据后才能标记 supported。")
    return "cross-version-upgrade-requires-manual-review"


def assert_public_safe(data: Any, *, artifact: str) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) if not isinstance(data, str) else data
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(text):
            raise UpgradePlanError(f"{artifact} contains unsafe content matching {pattern.pattern}")


def build_plan(root: Path, from_version: str, to_version: str) -> dict[str, Any]:
    target_release = release_fact(root, to_version)
    source_release = None if from_version == "fresh" else release_fact(root, from_version)
    blockers: list[str] = []
    warnings: list[str] = []
    if target_release is None:
        blockers.append(f"missing target release.json for {to_version}")
    if from_version != "fresh" and source_release is None:
        warnings.append(f"missing source release.json for {from_version}; source facts require manual reconstruction")
    if target_release and target_release.get("version") not in {None, to_version}:
        blockers.append("target release.json version does not match to_version")
    if target_release and impact_requires_database(target_release):
        warnings.append("目标版本存在数据库影响，需补充迁移、smoke、备份或回滚证据")

    support_level = classify_support(root, from_version, to_version, blockers, warnings)
    target_dir = release_dir(root, to_version)
    image_manifest_name = str(target_release.get("image_manifest", "image-manifest.json")) if target_release else "image-manifest.json"
    manifest_path = target_dir / image_manifest_name
    env = env_snapshot(root)
    plan = {
        "schema_version": 1,
        "generated_at": now_text(),
        "from_version": from_version,
        "to_version": to_version,
        "support_level": support_level,
        "source_confidence": {
            "from_version": source_confidence(root, from_version),
            "to_version": source_confidence(root, to_version),
        },
        "version_facts": {
            "target_release": {"path": f"releases/{to_version}/release.json", "exists": target_release is not None},
            "target_image_manifest": {"path": f"releases/{to_version}/{image_manifest_name}", "exists": manifest_path.exists()},
            "target_image_manifest_sha256": sha256_file(manifest_path),
            "source_release": None if from_version == "fresh" else {"path": f"releases/{from_version}/release.json", "exists": source_release is not None},
        },
        "impact_summary": {
            "database": "manual_review" if target_release and impact_requires_database(target_release) else "none",
            "env": "manual_review",
            "docker": "manual_review" if manifest_path.exists() else "missing_manifest_or_not_required",
            "api": "manual_review",
            "object_storage": "manual_review",
            "maintenance_tasks": "manual_review",
        },
        "env_diff": {
            "status": "manual_review",
            "summary": env_summary(env),
            "notes": [
                "当前计划只基于仓库 env 示例生成变量名级摘要；跨版本差异需结合 Git tag、release 归档或人工快照复核。",
                "不得在升级计划中写入真实 env 值、密钥、连接串、Cookie、Authorization header、本机绝对路径或客户数据。",
            ],
        },
        "required_checks": [
            "validate release.json and announcement public safety",
            "validate image manifest when image_required=true",
            "review env diff and production overrides",
            "run DB drift/smoke and backup evidence when database impact exists",
            "review object storage migration and rollback impact",
            "record rollback verification or manual fallback",
        ],
        "steps": [
            {"order": 1, "action": "确认目标 release 与镜像 manifest 事实源", "automation": "manual_review"},
            {"order": 2, "action": "复核 env diff 并准备生产覆盖值", "automation": "manual_review"},
            {"order": 3, "action": "按部署文档执行升级前备份、部署和 smoke", "automation": "manual_execution"},
            {"order": 4, "action": "记录升级结果、回滚窗口和证据位置", "automation": "manual_record"},
        ],
        "rollback": {
            "strategy": "manual_restore_or_previous_image",
            "requires": ["previous image or deployment package", "database backup or forward fix", "object storage impact review"],
            "verified": False,
        },
        "blockers": blockers,
        "warnings": warnings,
        "evidence": [],
    }
    assert_public_safe(plan, artifact="upgrade plan")
    return plan


def validate_plan(root: Path, path: Path) -> dict[str, Any]:
    plan = read_json(path)
    errors: list[str] = []
    warnings: list[str] = []
    for key in ("from_version", "to_version", "support_level", "source_confidence", "version_facts", "impact_summary", "env_diff", "steps", "rollback"):
        if key not in plan:
            errors.append(f"missing required field: {key}")
    if plan.get("support_level") not in SUPPORT_LEVELS:
        errors.append("support_level is invalid")
    if plan.get("from_version") != "fresh":
        try:
            semver_key(str(plan.get("from_version")))
        except UpgradePlanError as exc:
            errors.append(str(exc))
    try:
        semver_key(str(plan.get("to_version")))
    except UpgradePlanError as exc:
        errors.append(str(exc))
    target_release = release_fact(root, str(plan.get("to_version")))
    if target_release is None:
        errors.append("target release.json is missing")
    if plan.get("support_level") == "cross-version-upgrade-supported":
        evidence = plan.get("evidence")
        if not isinstance(evidence, list) or len(evidence) < 3:
            errors.append("cross-version-upgrade-supported requires explicit rehearsal, DB/env/object storage, and rollback evidence")
    if plan.get("blockers"):
        warnings.append("plan contains blockers; implementation must not proceed until resolved")
    assert_public_safe(plan, artifact=str(path))
    return {"path": rel_path(path, root=root), "errors": errors, "warnings": warnings, "status": "pass" if not errors else "fail"}


def cmd_plan(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    plan = build_plan(root, args.from_version, args.to_version)
    output = release_dir(root, args.to_version) / "upgrade-plans" / f"{args.from_version}-to-{args.to_version}.json"
    write_json(output, plan)
    result = validate_plan(root, output)
    print(json.dumps({"plan": rel_path(output, root=root), "validation": result}, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


def cmd_validate_plan(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    result = validate_plan(root, Path(args.plan).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


def cmd_env_diff(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    payload = {"status": "manual_review", "summary": env_summary(env_snapshot(root))}
    assert_public_safe(payload, artifact="env-diff")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(ROOT))
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="Generate an upgrade plan")
    plan.add_argument("--from", dest="from_version", required=True)
    plan.add_argument("--to", dest="to_version", required=True)
    plan.set_defaults(func=cmd_plan)
    validate = sub.add_parser("validate-plan", help="Validate an upgrade plan")
    validate.add_argument("--plan", required=True)
    validate.set_defaults(func=cmd_validate_plan)
    env_diff = sub.add_parser("env-diff", help="Summarize env example review points")
    env_diff.set_defaults(func=cmd_env_diff)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except UpgradePlanError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
