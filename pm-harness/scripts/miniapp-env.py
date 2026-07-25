#!/usr/bin/env python3
"""Manage a WeChat miniapp API environment strategy.

The script is intentionally project-neutral. Configure URLs through
`miniapp.env.json`, environment variables, or CLI flags instead of baking
production domains into the harness template.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MINIAPP = ROOT / "src" / "miniapp"
DEFAULT_ENV_TS = MINIAPP / "utils" / "env.ts"
DEFAULT_ENV_JS = MINIAPP / "utils" / "env.js"
PROJECT_PRIVATE_CONFIG = MINIAPP / "project.private.config.json"
CONFIG_FILE = ROOT / "miniapp.env.json"
DEFAULT_DEVELOPMENT_BASE_URL = "http://127.0.0.1:8010"
DEFAULT_DEVELOPMENT_FALLBACKS = ["http://localhost:8010", "http://localhost:8000"]
DEFAULT_STRATEGY = "auto"
VALID_STRATEGIES = {"dev", "prod", "auto"}


@dataclass(frozen=True)
class MiniappEnvConfig:
    production_base_url: str
    development_base_url: str
    development_fallbacks: list[str]
    env_ts: Path
    env_js: Path
    smoke_paths: list[str]
    static_test_command: list[str] | None


@dataclass(frozen=True)
class StrategyTemplate:
    ts_body: str
    js_body: str
    marker: str


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [item.strip() for item in value.split(",") if item.strip()]
    return []


def load_config(args: argparse.Namespace | None = None) -> MiniappEnvConfig:
    payload = _read_json(CONFIG_FILE)
    production_base_url = (
        getattr(args, "production_base_url", None)
        or os.environ.get("MINIAPP_PRODUCTION_BASE_URL")
        or payload.get("productionBaseUrl")
        or ""
    )
    development_base_url = (
        getattr(args, "development_base_url", None)
        or os.environ.get("MINIAPP_DEVELOPMENT_BASE_URL")
        or payload.get("developmentBaseUrl")
        or DEFAULT_DEVELOPMENT_BASE_URL
    )
    fallbacks = (
        _string_list(getattr(args, "development_fallbacks", None))
        or _string_list(os.environ.get("MINIAPP_DEVELOPMENT_FALLBACKS"))
        or _string_list(payload.get("developmentFallbackBaseUrls"))
        or DEFAULT_DEVELOPMENT_FALLBACKS
    )
    smoke_paths = (
        _string_list(getattr(args, "smoke_path", None))
        or _string_list(payload.get("smokePaths"))
    )
    static_test_command = _string_list(payload.get("staticTestCommand")) or None
    env_ts = Path(str(payload.get("envTsPath") or DEFAULT_ENV_TS)).expanduser()
    env_js = Path(str(payload.get("envJsPath") or DEFAULT_ENV_JS)).expanduser()
    if not env_ts.is_absolute():
        env_ts = ROOT / env_ts
    if not env_js.is_absolute():
        env_js = ROOT / env_js
    return MiniappEnvConfig(
        production_base_url=production_base_url.rstrip("/"),
        development_base_url=development_base_url.rstrip("/"),
        development_fallbacks=[item.rstrip("/") for item in fallbacks],
        env_ts=env_ts,
        env_js=env_js,
        smoke_paths=smoke_paths,
        static_test_command=static_test_command,
    )


def _strategy_template(strategy: str, config: MiniappEnvConfig) -> StrategyTemplate:
    if strategy not in VALID_STRATEGIES:
        raise ValueError(f"invalid strategy: {strategy}")

    if strategy == "dev":
        resolver = "return 'development';"
        marker = "return 'development'"
    elif strategy == "prod":
        resolver = "return 'production';"
        marker = "return 'production'"
    else:
        resolver = (
            "try {\n"
            "    const accountInfo = wx.getAccountInfoSync();\n"
            "    return accountInfo.miniProgram.envVersion === 'develop' ? 'development' : 'production';\n"
            "  } catch (error) {\n"
            "    return 'development';\n"
            "  }"
        )
        marker = "envVersion === 'develop' ? 'development' : 'production'"

    return StrategyTemplate(
        ts_body=_render_ts(resolver, config),
        js_body=_render_js(resolver, config),
        marker=marker,
    )


def _quoted(items: list[str]) -> str:
    return ", ".join(json.dumps(item, ensure_ascii=False) for item in items)


def _render_ts(resolver: str, config: MiniappEnvConfig) -> str:
    return f"""export type MiniappEnvironment = 'development' | 'production';

export type MiniappApiConfig = {{
  environment: MiniappEnvironment;
  apiBaseUrl: string;
  apiFallbackBaseUrls: string[];
}};

export const MINIAPP_API_CONFIGS: Record<MiniappEnvironment, MiniappApiConfig> = {{
  development: {{
    environment: 'development',
    apiBaseUrl: {json.dumps(config.development_base_url, ensure_ascii=False)},
    apiFallbackBaseUrls: [{_quoted(config.development_fallbacks)}],
  }},
  production: {{
    environment: 'production',
    apiBaseUrl: {json.dumps(config.production_base_url, ensure_ascii=False)},
    apiFallbackBaseUrls: [],
  }},
}};

export function resolveMiniappEnvironment(): MiniappEnvironment {{
  {resolver}
}}

export function resolveMiniappApiConfig(environment = resolveMiniappEnvironment()): MiniappApiConfig {{
  return MINIAPP_API_CONFIGS[environment];
}}

export const miniappApiConfig = resolveMiniappApiConfig();
"""


def _render_js(resolver: str, config: MiniappEnvConfig) -> str:
    return f"""const MINIAPP_API_CONFIGS = {{
  development: {{
    environment: 'development',
    apiBaseUrl: {json.dumps(config.development_base_url, ensure_ascii=False)},
    apiFallbackBaseUrls: [{_quoted(config.development_fallbacks)}],
  }},
  production: {{
    environment: 'production',
    apiBaseUrl: {json.dumps(config.production_base_url, ensure_ascii=False)},
    apiFallbackBaseUrls: [],
  }},
}};

function resolveMiniappEnvironment() {{
  {resolver}
}}

function resolveMiniappApiConfig(environment = resolveMiniappEnvironment()) {{
  return MINIAPP_API_CONFIGS[environment];
}}

const miniappApiConfig = resolveMiniappApiConfig();

module.exports = {{
  MINIAPP_API_CONFIGS,
  resolveMiniappEnvironment,
  resolveMiniappApiConfig,
  miniappApiConfig,
}};
"""


def detect_strategy(config: MiniappEnvConfig) -> str:
    if not config.env_ts.exists() or not config.env_js.exists():
        return "missing"
    ts = config.env_ts.read_text(encoding="utf-8")
    js = config.env_js.read_text(encoding="utf-8")
    for strategy in ["auto", "prod", "dev"]:
        marker = _strategy_template(strategy, config).marker
        if marker in ts and marker in js:
            return strategy
    return "unknown"


def _read_project_private_config() -> dict[str, Any]:
    return _read_json(PROJECT_PRIVATE_CONFIG)


def _set_devtools_url_check(enabled: bool) -> None:
    payload = _read_project_private_config()
    payload.setdefault("setting", {})
    if not isinstance(payload["setting"], dict):
        payload["setting"] = {}
    payload["setting"]["urlCheck"] = enabled
    PROJECT_PRIVATE_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    PROJECT_PRIVATE_CONFIG.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _smoke_url(url: str) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            body = response.read().decode("utf-8")
            status = response.status
    except urllib.error.HTTPError as error:
        return {"url": url, "ok": False, "status": error.code, "error": str(error)}
    except urllib.error.URLError as error:
        return {"url": url, "ok": False, "status": None, "error": str(error)}

    code_ok: bool | None = None
    try:
        payload = json.loads(body)
        code_ok = payload.get("code") in (0, "0", None)
    except json.JSONDecodeError:
        code_ok = None
    return {"url": url, "ok": status == 200 and code_ok is not False, "status": status, "code_ok": code_ok}


def check_state(config: MiniappEnvConfig, *, smoke: bool = False) -> dict[str, Any]:
    ts = config.env_ts.read_text(encoding="utf-8") if config.env_ts.exists() else ""
    js = config.env_js.read_text(encoding="utf-8") if config.env_js.exists() else ""
    strategy = detect_strategy(config)
    private_config = _read_project_private_config()
    expected_url_check = True if strategy == "prod" else False
    smoke_results = []
    if smoke and config.production_base_url:
        smoke_results = [_smoke_url(f"{config.production_base_url}{path}") for path in config.smoke_paths]
    result: dict[str, Any] = {
        "strategy": strategy,
        "files": {
            "ts": str(config.env_ts.relative_to(ROOT)) if config.env_ts.is_relative_to(ROOT) else str(config.env_ts),
            "js": str(config.env_js.relative_to(ROOT)) if config.env_js.is_relative_to(ROOT) else str(config.env_js),
            "ts_exists": config.env_ts.exists(),
            "js_exists": config.env_js.exists(),
            "ts_js_strategy_match": strategy in VALID_STRATEGIES,
        },
        "devtools": {
            "private_config_exists": PROJECT_PRIVATE_CONFIG.exists(),
            "urlCheck": private_config.get("setting", {}).get("urlCheck"),
            "expected_urlCheck": expected_url_check,
            "urlCheck_matches_strategy": private_config.get("setting", {}).get("urlCheck") is expected_url_check,
        },
        "development": {
            "apiBaseUrl": config.development_base_url,
            "apiFallbackBaseUrls": config.development_fallbacks,
            "present_in_ts": config.development_base_url in ts,
            "present_in_js": config.development_base_url in js,
        },
        "production": {
            "apiBaseUrl": config.production_base_url,
            "configured": bool(config.production_base_url),
            "present_in_ts": bool(config.production_base_url and config.production_base_url in ts),
            "present_in_js": bool(config.production_base_url and config.production_base_url in js),
        },
        "smoke": smoke_results,
        "ok": strategy in VALID_STRATEGIES
        and bool(config.production_base_url)
        and config.production_base_url in ts
        and config.production_base_url in js
        and private_config.get("setting", {}).get("urlCheck") is expected_url_check,
    }
    if smoke_results:
        result["ok"] = bool(result["ok"] and all(item["ok"] for item in smoke_results))
    return result


def set_strategy(strategy: str, config: MiniappEnvConfig) -> dict[str, Any]:
    if not config.production_base_url:
        raise ValueError("production base URL is required; set miniapp.env.json or MINIAPP_PRODUCTION_BASE_URL")
    template = _strategy_template(strategy, config)
    config.env_ts.parent.mkdir(parents=True, exist_ok=True)
    config.env_js.parent.mkdir(parents=True, exist_ok=True)
    config.env_ts.write_text(template.ts_body, encoding="utf-8")
    config.env_js.write_text(template.js_body, encoding="utf-8")
    _set_devtools_url_check(strategy == "prod")
    return check_state(config, smoke=False)


def run_static_tests(config: MiniappEnvConfig) -> dict[str, Any] | None:
    if not config.static_test_command:
        return None
    completed = subprocess.run(config.static_test_command, cwd=ROOT, text=True, capture_output=True, check=False)
    return {
        "command": " ".join(config.static_test_command),
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout_tail": "\n".join(completed.stdout.splitlines()[-8:]),
        "stderr_tail": "\n".join(completed.stderr.splitlines()[-8:]),
    }


def checklist(config: MiniappEnvConfig) -> list[str]:
    domain = config.production_base_url or "<productionBaseUrl>"
    return [
        f"微信公众平台 request 合法域名包含 {domain}",
        "微信开发者工具重新上传开发版本",
        "微信公众平台版本管理中将最新开发版本设为体验版",
        "手机删除旧体验版入口后重新扫码最新体验版二维码",
        "体验版关键路径完成冒烟验证，并记录到 release 或 Sprint 验收材料",
    ]


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_set(args: argparse.Namespace) -> int:
    config = load_config(args)
    try:
        result = set_strategy(args.strategy, config)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    _print_json({"action": "set", **result})
    return 0 if result["ok"] else 1


def command_check(args: argparse.Namespace) -> int:
    config = load_config(args)
    result = check_state(config, smoke=args.smoke)
    _print_json({"action": "check", **result})
    return 0 if result["ok"] else 1


def command_prepare(args: argparse.Namespace) -> int:
    config = load_config(args)
    try:
        state = set_strategy("prod", config)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    tests = None if args.skip_tests else run_static_tests(config)
    smoke = check_state(config, smoke=True)
    ok = bool(state["ok"] and smoke["ok"] and (tests is None or tests["ok"]))
    _print_json(
        {
            "action": "prepare",
            "ok": ok,
            "strategy": "prod",
            "state": state,
            "tests": tests,
            "smoke": smoke["smoke"],
            "checklist": checklist(config),
            "next": "/miniapp-confirm 或 /miniapp-restore",
        }
    )
    return 0 if ok else 1


def command_confirm(args: argparse.Namespace) -> int:
    _print_json(
        {
            "action": "confirm",
            "ok": True,
            "channel": args.channel,
            "version": args.version,
            "result": args.result,
            "notes": args.notes,
            "safe_record": "请将此摘要复制到 release 或 Sprint 验收记录；不要记录微信会话密钥、Cookie、Authorization header 或 .env 内容。",
            "next": "/miniapp-restore",
        }
    )
    return 0


def command_restore(args: argparse.Namespace) -> int:
    config = load_config(args)
    try:
        result = set_strategy(args.strategy, config)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    _print_json({"action": "restore", **result})
    return 0 if result["ok"] else 1


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--production-base-url", help="Production API base URL")
    parser.add_argument("--development-base-url", help="Development API base URL")
    parser.add_argument("--development-fallbacks", help="Comma-separated fallback development base URLs")
    parser.add_argument("--smoke-path", action="append", help="Production smoke path, e.g. /api/v1/health")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage miniapp API environment strategy.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    set_parser = subparsers.add_parser("set")
    add_common_args(set_parser)
    set_parser.add_argument("strategy", choices=sorted(VALID_STRATEGIES))
    set_parser.set_defaults(func=command_set)

    check_parser = subparsers.add_parser("check")
    add_common_args(check_parser)
    check_parser.add_argument("--smoke", action="store_true")
    check_parser.set_defaults(func=command_check)

    prepare_parser = subparsers.add_parser("prepare")
    add_common_args(prepare_parser)
    prepare_parser.add_argument("--skip-tests", action="store_true")
    prepare_parser.set_defaults(func=command_prepare)

    confirm_parser = subparsers.add_parser("confirm")
    confirm_parser.add_argument("--channel", choices=["trial", "release"], required=True)
    confirm_parser.add_argument("--version", required=True)
    confirm_parser.add_argument("--result", choices=["passed", "blocked", "follow_up"], default="passed")
    confirm_parser.add_argument("--notes", default="")
    confirm_parser.set_defaults(func=command_confirm)

    restore_parser = subparsers.add_parser("restore")
    add_common_args(restore_parser)
    restore_parser.add_argument("--strategy", choices=sorted(VALID_STRATEGIES), default=DEFAULT_STRATEGY)
    restore_parser.set_defaults(func=command_restore)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
