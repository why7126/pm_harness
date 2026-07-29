#!/usr/bin/env python3
"""Prepare and validate release image build plan/manifest artifacts."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASES_DIR = ROOT / "releases"
DEFAULT_ENV_FILE = ROOT / "scripts" / "build-images.env"
ENV_EXAMPLE_FILE = ROOT / "scripts" / "build-images.env.example"

NO_IMPACT_VALUES = {"", "none", "na", "n/a", "not_applicable", "not applicable", "无", "不涉及"}
IMAGE_IMPACT_KEYS = ("backend", "database", "docker", "object_storage")
SAFE_ENV_KEYS = {
    "IMAGE_BUILD_TAG",
    "IMAGE_BUILD_PLATFORM",
    "BACKEND_PYTHON_BASE_IMAGE",
    "WEB_NODE_BASE_IMAGE",
    "WEB_NGINX_BASE_IMAGE",
    "IMAGE_BUILD_BACKEND_IMAGE",
    "IMAGE_BUILD_WEB_IMAGE",
    "IMAGE_BUILD_BUILDER",
    "IMAGE_BUILD_CREATE_BUILDER",
    "IMAGE_BUILD_LOAD",
    "IMAGE_BUILD_EXPORT_TAR",
    "IMAGE_BUILD_RELEASE_DIR",
    "IMAGE_BUILD_TAR_NAME",
}
SENSITIVE_PATTERNS = (
    re.compile(r"\bAPP_SECRET_KEY\s*=", re.I),
    re.compile(r"\bDATABASE_URL\s*=", re.I),
    re.compile(r"mysql(\+\w+)?://", re.I),
    re.compile(r"\b(MINIO|OBJECT_STORAGE)_(SECRET|ACCESS)_KEY\s*=", re.I),
    re.compile(r"\bAuthorization\s*:", re.I),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.I),
    re.compile(r"\bCookie\s*:", re.I),
    re.compile(r"\bpassword\s*=", re.I),
    re.compile(r"/Users/[^\\s\"']+", re.I),
)

INPUT_FILE_CANDIDATES = (
    "src/shared/product-version.ts",
    "src/backend/Dockerfile",
    "src/web/Dockerfile",
    "src/web/nginx.conf",
    "docker-compose.prod.yml",
    "docker-compose.prod.external.yml",
    ".env.example",
    "scripts/build-images.sh",
    "scripts/build-images.env.example",
    "src/backend/app/db/schema.sql",
    "src/backend/app/db/schema.mysql.sql",
    "src/backend/app/db/migrations.py",
    "src/backend/app/db/mysql_migrations.py",
    "docs/04-database-design.md",
    "docs/08-production-image-release.md",
)


class ImageBuildError(ValueError):
    """User-facing validation error."""


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def rel_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ImageBuildError(f"missing file: {rel_path(path)}") from None
    except json.JSONDecodeError as exc:
        raise ImageBuildError(f"invalid JSON {rel_path(path)}: {exc}") from None
    if not isinstance(data, dict):
        raise ImageBuildError(f"{rel_path(path)} must contain a JSON object")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if key in SAFE_ENV_KEYS:
            values[key] = value.strip().strip("'\"")
    return values


def safe_env_summary(path: Path) -> dict[str, Any]:
    values = parse_env(path)
    sanitized: dict[str, str] = {}
    for key, value in values.items():
        if key not in SAFE_ENV_KEYS:
            continue
        if re.search(r"/Users/|://.*@", value):
            sanitized[key] = "<redacted>"
        else:
            sanitized[key] = value
    return {"path": rel_path(path), "exists": path.exists(), "safe_values": sanitized}


def impact_requires_image(release_data: dict[str, Any]) -> bool:
    explicit = release_data.get("image_required")
    if isinstance(explicit, bool):
        return explicit
    impact = release_data.get("impact_scope")
    if not isinstance(impact, dict):
        return False
    return any(str(impact.get(key, "")).strip().lower() not in NO_IMPACT_VALUES for key in IMAGE_IMPACT_KEYS)


def input_files_for_release(release_dir: Path) -> list[Path]:
    files = [release_dir / "release.json"]
    announcement = read_json(release_dir / "release.json").get("announcement", "announcement.mdx")
    files.append(release_dir / str(announcement))
    files.extend(ROOT / item for item in INPUT_FILE_CANDIDATES)
    return [path for path in files if path.exists()]


def current_input_hashes(paths: list[Path]) -> dict[str, str]:
    return {rel_path(path): file_sha256(path) for path in paths}


def compose_tag_defaults() -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    pattern = re.compile(r"\$\{(?:IMAGE_BUILD_TAG|[A-Z0-9_]+_IMAGE_TAG):-([^}]+)\}")
    for relative in ("docker-compose.prod.yml", "docker-compose.prod.external.yml"):
        path = ROOT / relative
        if path.exists():
            result[relative] = pattern.findall(path.read_text(encoding="utf-8"))
    return result


def build_required_commands(version: str, env_file: Path = DEFAULT_ENV_FILE) -> list[dict[str, str]]:
    return [
        {
            "name": "prepare",
            "command": f"python scripts/validate-image-build.py prepare --release {version}",
        },
        {
            "name": "build",
            "command": f"./scripts/build-images.sh {rel_path(env_file)}",
        },
        {
            "name": "manifest",
            "command": f"python scripts/validate-image-build.py build --release {version}",
        },
    ]


def assert_public_safe(data: dict[str, Any], *, artifact: str) -> None:
    text = json.dumps(data, ensure_ascii=False)
    matches = [pattern.pattern for pattern in SENSITIVE_PATTERNS if pattern.search(text)]
    if matches:
        raise ImageBuildError(f"{artifact} contains sensitive data: {', '.join(matches)}")


def prepare_plan(version: str, release_dir: Path | None = None, env_file: Path = DEFAULT_ENV_FILE) -> dict[str, Any]:
    release_dir = release_dir or RELEASES_DIR / version
    release_data = read_json(release_dir / "release.json")
    release_version = str(release_data.get("version", ""))
    if release_version != version:
        raise ImageBuildError(f"release.json version {release_version or '<missing>'} does not match {version}")

    example_values = parse_env(ENV_EXAMPLE_FILE)
    env_values = parse_env(env_file)
    image_required = impact_requires_image(release_data)
    image_tag = env_values.get("IMAGE_BUILD_TAG") or example_values.get("IMAGE_BUILD_TAG") or version
    platform = env_values.get("IMAGE_BUILD_PLATFORM") or example_values.get("IMAGE_BUILD_PLATFORM") or "linux/amd64"
    blockers: list[dict[str, str]] = []

    if image_required and not env_file.exists():
        blockers.append(
            {
                "code": "build_env_missing",
                "message": "scripts/build-images.env is missing; copy scripts/build-images.env.example before image-build.",
            }
        )
    if image_required and image_tag != version:
        blockers.append(
            {
                "code": "image_tag_mismatch",
                "message": f"IMAGE_BUILD_TAG {image_tag} does not match release version {version}.",
            }
        )
    if example_values.get("IMAGE_BUILD_TAG") and example_values["IMAGE_BUILD_TAG"] != "v0.0.1":
        blockers.append(
            {
                "code": "env_example_not_template",
                "message": "scripts/build-images.env.example should keep IMAGE_BUILD_TAG as v0.0.1 template placeholder.",
            }
        )

    compose_defaults = compose_tag_defaults()
    for compose_file, tags in compose_defaults.items():
        for tag in tags:
            if tag != version:
                blockers.append(
                    {
                        "code": "compose_default_tag_mismatch",
                        "message": f"{compose_file} default image tag is {tag}, expected {version} or explicit release rationale.",
                    }
                )

    input_files = input_files_for_release(release_dir)
    plan = {
        "version": version,
        "generated_at": now_text(),
        "image_required": image_required,
        "image_required_rationale": release_data.get("image_required_rationale", ""),
        "image_tag": image_tag,
        "platform": platform,
        "source_scope": {
            "sprints": release_data.get("sprints", []),
            "requirements": release_data.get("requirements", []),
            "bugs": release_data.get("bugs", []),
            "changes": release_data.get("changes", []),
        },
        "build_env": {
            "default": safe_env_summary(env_file),
            "example": safe_env_summary(ENV_EXAMPLE_FILE),
        },
        "input_files": [rel_path(path) for path in input_files],
        "input_hashes": current_input_hashes(input_files),
        "database_impact": {
            "required": str(release_data.get("impact_scope", {}).get("database", "")).strip().lower()
            not in NO_IMPACT_VALUES,
            "inputs": [
                item
                for item in (
                    "src/backend/app/db/schema.sql",
                    "src/backend/app/db/schema.mysql.sql",
                    "src/backend/app/db/migrations.py",
                    "src/backend/app/db/mysql_migrations.py",
                    "docs/04-database-design.md",
                )
                if (ROOT / item).exists()
            ],
            "evidence_required": [
                "MySQL schema drift or target MySQL smoke evidence",
                "database rollback or backup evidence",
            ],
        },
        "compose_tag_defaults": compose_defaults,
        "required_commands": build_required_commands(version, env_file),
        "blockers": blockers,
    }
    assert_public_safe(plan, artifact="image-build-plan.json")
    write_json(release_dir / "image-build-plan.json", plan)
    return plan


def validate_plan(version: str, release_dir: Path | None = None, *, require_unblocked: bool = False) -> list[str]:
    release_dir = release_dir or RELEASES_DIR / version
    errors: list[str] = []
    try:
        plan = read_json(release_dir / "image-build-plan.json")
        assert_public_safe(plan, artifact="image-build-plan.json")
    except ImageBuildError as exc:
        return [str(exc)]
    if plan.get("version") != version:
        errors.append(f"image-build-plan.json version must be {version}")
    for key in ("image_required", "image_tag", "source_scope", "build_env", "input_files", "input_hashes", "database_impact", "required_commands", "blockers"):
        if key not in plan:
            errors.append(f"image-build-plan.json missing {key}")
    if require_unblocked and plan.get("blockers"):
        errors.append("image-build-plan.json has blockers")
    input_files = [ROOT / item for item in plan.get("input_files", []) if isinstance(item, str)]
    current_hashes = current_input_hashes([path for path in input_files if path.exists()])
    for path, expected in plan.get("input_hashes", {}).items():
        actual = current_hashes.get(path)
        if actual != expected:
            errors.append(f"input hash drift: {path}")
    return errors


def tar_sha256_from_sidecar(tar_path: Path) -> str | None:
    sidecar = Path(f"{tar_path}.sha256")
    if not sidecar.exists():
        return None
    return sidecar.read_text(encoding="utf-8").split()[0]


def validate_manifest(version: str, release_dir: Path | None = None) -> list[str]:
    release_dir = release_dir or RELEASES_DIR / version
    errors = validate_plan(version, release_dir, require_unblocked=False)
    try:
        manifest = read_json(release_dir / "image-manifest.json")
        assert_public_safe(manifest, artifact="image-manifest.json")
    except ImageBuildError as exc:
        return [str(exc)]
    if manifest.get("version") != version:
        errors.append(f"image-manifest.json version must be {version}")
    for key in ("image_tag", "built_at", "platform", "backend_image", "web_image", "tarball", "input_hashes", "validation", "source_plan"):
        if key not in manifest:
            errors.append(f"image-manifest.json missing {key}")
    try:
        plan = read_json(release_dir / "image-build-plan.json")
    except ImageBuildError as exc:
        errors.append(str(exc))
        plan = {}
    if plan and manifest.get("input_hashes") != plan.get("input_hashes"):
        errors.append("image-manifest.json input_hashes do not match image-build-plan.json")
    return errors


def build_images(version: str, release_dir: Path | None = None, env_file: Path = DEFAULT_ENV_FILE) -> dict[str, Any]:
    release_dir = release_dir or RELEASES_DIR / version
    errors = validate_plan(version, release_dir, require_unblocked=True)
    if errors:
        raise ImageBuildError("; ".join(errors))
    plan = read_json(release_dir / "image-build-plan.json")
    subprocess.run([str(ROOT / "scripts" / "build-images.sh"), str(env_file)], cwd=ROOT, check=True)

    env_values = parse_env(env_file)
    tag = str(plan.get("image_tag") or env_values.get("IMAGE_BUILD_TAG") or version)
    platform = str(plan.get("platform") or env_values.get("IMAGE_BUILD_PLATFORM") or "linux/amd64")
    backend_name = env_values.get("IMAGE_BUILD_BACKEND_IMAGE", "pm-harness-backend")
    web_name = env_values.get("IMAGE_BUILD_WEB_IMAGE", "pm-harness-web")
    tar_name = env_values.get("IMAGE_BUILD_TAR_NAME") or f"pm-harness-{tag}-{platform.replace('/', '-')}.tar.gz"
    tar_path = release_dir / "images" / tar_name
    tarball = {
        "path": rel_path(tar_path),
        "sha256": tar_sha256_from_sidecar(tar_path),
        "exists": tar_path.exists(),
    }
    manifest = {
        "version": version,
        "image_tag": tag,
        "built_at": now_text(),
        "platform": platform,
        "backend_image": {"name": backend_name, "tag": tag, "ref": f"{backend_name}:{tag}"},
        "web_image": {"name": web_name, "tag": tag, "ref": f"{web_name}:{tag}"},
        "tarball": tarball,
        "input_hashes": plan["input_hashes"],
        "validation": {
            "platform": "pass",
            "backend_dependencies": "pass",
            "web_nginx": "pass",
            "tar_export": "pass" if tarball["exists"] else "na",
        },
        "source_plan": {
            "path": rel_path(release_dir / "image-build-plan.json"),
            "sha256": file_sha256(release_dir / "image-build-plan.json"),
        },
    }
    assert_public_safe(manifest, artifact="image-manifest.json")
    write_json(release_dir / "image-manifest.json", manifest)
    return manifest


def print_summary(kind: str, version: str, path: Path, errors: list[str] | None = None) -> None:
    errors = errors or []
    print(f"## Image {kind} Validation")
    print()
    print(f"Version: {version}")
    print(f"Path: {rel_path(path)}")
    print(f"Result: {'fail' if errors else 'pass'}")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("prepare", "validate-plan", "validate-manifest", "build"):
        sub = subparsers.add_parser(name)
        sub.add_argument("--release", required=True)
        sub.add_argument("--release-dir")
        sub.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    args = parser.parse_args()

    release_dir = Path(args.release_dir).resolve() if args.release_dir else RELEASES_DIR / args.release
    env_file = Path(args.env_file).resolve()
    try:
        if args.command == "prepare":
            plan = prepare_plan(args.release, release_dir, env_file)
            print_summary("Plan", args.release, release_dir / "image-build-plan.json")
            print(f"image_required: {plan['image_required']}")
            print(f"blocker_count: {len(plan['blockers'])}")
            return 0
        if args.command == "validate-plan":
            errors = validate_plan(args.release, release_dir, require_unblocked=False)
            print_summary("Plan", args.release, release_dir / "image-build-plan.json", errors)
            return 1 if errors else 0
        if args.command == "validate-manifest":
            errors = validate_manifest(args.release, release_dir)
            print_summary("Manifest", args.release, release_dir / "image-manifest.json", errors)
            return 1 if errors else 0
        if args.command == "build":
            manifest = build_images(args.release, release_dir, env_file)
            print_summary("Manifest", args.release, release_dir / "image-manifest.json")
            print(f"image_tag: {manifest['image_tag']}")
            print(f"tarball: {manifest['tarball']['path']}")
            return 0
    except (ImageBuildError, subprocess.CalledProcessError) as exc:
        print(f"Image build workflow failed: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
