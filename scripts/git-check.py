#!/usr/bin/env python3
"""Read-only Git safety checks: index blobs, tracked worktree and optional history."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from dataclasses import dataclass
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
TEXT_LIMIT = 1024 * 1024
BINARY = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.pdf', '.zip', '.gz', '.tar', '.tgz', '.db', '.sqlite', '.sqlite3'}
RUNTIME = {'node_modules', '.venv', '__pycache__', '.pytest_cache', '.vite', 'dist', 'build', 'coverage'}
DATA_RUNTIME = {'runtime', 'sqlite', 'uploads', 'processed', 'tmp', 'minio', 's3', 'mysql'}
PLACEHOLDERS = {'change-me', 'change-me-in-local-env', 'example', 'example.com', 'localhost', '127.0.0.1', 'CHANGE_ME', 'replace-with-access-key', 'replace-with-secret-key'}
# Match actual usernames, not regex syntax or a whole source line exemption.
HOME_PATH = re.compile(r'(?<![\w.-])(?:/' + r'Users/|/' + r'home/|[A-Za-z]:\\+Users\\+)([\w.-]+)(?=[/\\\s\"\x27`]|$)')
SECRET_PATTERNS = [
    ('authorization', re.compile(r'\bAuthorization\s*:\s*Bearer\s+([^\s\"\x27`]+)', re.I), 'error'),
    ('cookie', re.compile(r'\bCookie\s*:\s*([^\r\n]+)', re.I), 'error'),
    ('assigned-secret', re.compile(r'''(?<!\$\{)\b(?:api[_-]?key|access[_-]?key|secret[_-]?key|secret|token|password|(?:MINIO|S3|OBJECT_STORAGE)_[A-Z0-9_]*(?:KEY|SECRET|TOKEN|PASSWORD))\b\s*[:=]\s*(?:"([^"\r\n]+)"|'([^'\r\n]+)'|([^\s,;`]+))''', re.I), 'error'),
    ('database-url', re.compile(r'\b(?:mysql|postgresql|postgres)://[^\s\"\x27`]+', re.I), 'error'),
    ('private-key', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'), 'error'),
    ('local-absolute-path', HOME_PATH, 'error'),
    ('privacy-email', re.compile(r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b'), 'warning'),
    ('privacy-phone', re.compile(r'(?<![A-Za-z0-9])1[3-9]\d{9}(?![A-Za-z0-9])'), 'warning'),
]

@dataclass(frozen=True)
class Finding:
    severity: str
    rule: str
    path: str
    source: str
    line: int | None = None

class ScanError(Exception):
    """Only fixed diagnostic codes may be exposed."""


def git(root: Path, *args: str) -> bytes:
    proc = subprocess.run(['git', '--no-optional-locks', *args], cwd=root,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise ScanError('git-read-failed')
    return proc.stdout


def placeholder(value: str) -> bool:
    value = value.strip()
    fallback = re.fullmatch(r'\$\{[A-Z_][A-Z0-9_]*:-([^$]+)\}', value)
    if fallback:
        return placeholder(fallback.group(1))
    return (value in PLACEHOLDERS
            or bool(re.fullmatch(r'<[a-z][a-z0-9_-]*>', value))
            or bool(re.fullmatch(r'\{[A-Z_][A-Z0-9_]*\}', value))
            or bool(re.fullmatch(r'\$\{[A-Z_][A-Z0-9_]*\}', value)))


def safe_match(rule: str, match: re.Match) -> bool:
    value = next((v for v in reversed(match.groups()) if v is not None), match.group())
    if rule == 'database-url':
        try:
            parsed = urlsplit(match.group())
            # Hostnames and query strings never exempt actual credentials.
            return (parsed.username is not None and parsed.password is not None
                    and placeholder(unquote(parsed.username)) and placeholder(unquote(parsed.password))
                    and not parsed.query and not parsed.fragment)
        except ValueError:
            return False
    if rule == 'privacy-email':
        return value.lower() in {'example.com', 'example.org', 'example.test'}
    if rule == 'local-absolute-path':
        return value == 'example'
    if rule in {'cookie', 'private-key'}:
        return placeholder(match.group(1)) if rule == 'cookie' else False
    return placeholder(value)


def scan_text(path: str, text: str, source: str) -> list[Finding]:
    result = []
    for number, line in enumerate(text.splitlines(), 1):
        for rule, pattern, severity in SECRET_PATTERNS:
            if any(not safe_match(rule, m) for m in pattern.finditer(line)):
                result.append(Finding(severity, rule, path, source, number))
    return result


def real_env(path: str) -> bool:
    name = Path(path).name
    return not name.endswith('.example') and (name == '.env' or name.startswith('.env.') or name.endswith('.env'))


def forbidden(path: str) -> bool:
    parts = Path(path).parts
    return (real_env(path) or bool(set(parts) & RUNTIME)
            or Path(path).suffix in {'.db', '.sqlite', '.sqlite3', '.pyc', '.zip'}
            or Path(path).name == '.DS_Store'
            or any(parts[i] == 'data' and parts[i+1] in DATA_RUNTIME for i in range(len(parts)-1)))


def scan_bytes(path: str, data: bytes, source: str, max_mb: int, *, size: int | None = None) -> list[Finding]:
    findings = [Finding('error', 'forbidden-path', path, source)] if forbidden(path) else []
    if (len(data) if size is None else size) > max_mb * 1024 * 1024:
        findings.append(Finding('error', 'large-file', path, source))
    if Path(path).suffix.lower() in BINARY or b'\0' in data[:8192]:
        return findings  # Content of binary formats is explicitly outside coverage.
    if len(data) > TEXT_LIMIT:
        return findings + [Finding('error', 'text-limit-unscanned', path, source)]
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return findings + [Finding('error', 'encoding-unscanned', path, source)]
    return findings + scan_text(path, text, source)


def blob(root: Path, oid: str) -> bytes:
    size = int(git(root, 'cat-file', '-s', oid))
    if size > TEXT_LIMIT:
        # Caller records an explicit incomplete scan; avoid loading unbounded objects.
        raise ScanError('object-limit-unscanned')
    return git(root, 'cat-file', 'blob', oid)


def safe_worktree_bytes(root: Path, path: str) -> tuple[bytes, int] | None:
    # Open each component without following symlinks, including directory links.
    parts = Path(path).parts
    if not parts or any(p in {'..', '/'} for p in parts):
        raise ScanError('unsafe-path')
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in parts[:-1]:
            new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = new
        leaf = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        with os.fdopen(leaf, 'rb') as stream:
            metadata = os.fstat(stream.fileno())
            if not stat.S_ISREG(metadata.st_mode):
                raise ScanError('special-file-unscanned')
            return stream.read(TEXT_LIMIT + 1), metadata.st_size
    except FileNotFoundError:
        return None  # Deleted worktree file; index object is still inspected.
    finally:
        os.close(fd)


def scan_repository(root: Path, *, scan_all=False, base=None, history=False, max_mb=10):
    findings: list[Finding] = []
    seen = set()
    count = 0

    def inspect_object(path, oid, mode, source):
        nonlocal count
        key = (path, oid, mode, source.split(':')[0])
        if key in seen:
            return
        seen.add(key)
        count += 1
        if mode not in {'100644', '100755'}:
            findings.append(Finding('error', 'link-or-submodule-unscanned', path, source))
            return
        try:
            findings.extend(scan_bytes(path, blob(root, oid), source, max_mb))
        except (ScanError, ValueError):
            findings.append(Finding('error', 'object-read-incomplete', path, source))

    paths = set()
    index_before = git(root, 'ls-files', '--stage', '-z')
    for record in index_before.split(b'\0'):
        if not record:
            continue
        meta, raw_path = record.split(b'\t', 1)
        mode, oid, stage = meta.decode('ascii').split()
        path = os.fsdecode(raw_path)
        paths.add(path)
        if stage != '0':
            findings.append(Finding('error', 'unmerged-index', path, 'index'))
        inspect_object(path, oid, mode, 'index')
    if scan_all:
        paths.update(os.fsdecode(p) for p in git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0') if p)
    for path in sorted(paths):
        count += 1
        try:
            data = safe_worktree_bytes(root, path)
            if data is not None:
                findings.extend(scan_bytes(path, data[0], 'worktree', max_mb, size=data[1]))
        except (OSError, ScanError):
            findings.append(Finding('error', 'worktree-read-incomplete', path, 'worktree'))
    if base is not None or history:
        if git(root, 'rev-parse', '--is-shallow-repository').strip() == b'true':
            raise ScanError('shallow-history-incomplete')
        head = git(root, 'rev-parse', '--verify', 'HEAD^{commit}').decode().strip()
        if base is not None:
            base_oid = git(root, 'rev-parse', '--verify', '--end-of-options', base + '^{commit}').decode().strip()
            commits = git(root, 'rev-list', f'{base_oid}..{head}').decode().splitlines()
        else:
            commits = git(root, 'rev-list', head).decode().splitlines()
        for commit in commits:
            source = 'history:' + commit[:12]
            message = git(root, 'show', '-s', '--format=%B', commit).decode('utf-8', errors='replace')
            findings.extend(scan_text('COMMIT_MESSAGE', message, source))
            for rec in git(root, 'ls-tree', '-r', '-z', commit).split(b'\0'):
                if not rec:
                    continue
                meta, raw_path = rec.split(b'\t', 1)
                mode, kind, oid = meta.decode('ascii').split()
                inspect_object(os.fsdecode(raw_path), oid, mode, source)
        if git(root, 'rev-parse', '--verify', 'HEAD^{commit}').decode().strip() != head:
            findings.append(Finding('error', 'head-changed-during-scan', 'HEAD', 'history'))
    if git(root, 'ls-files', '--stage', '-z') != index_before:
        findings.append(Finding('error', 'index-changed-during-scan', 'INDEX', 'index'))
    return findings, count


def display_path(path: str) -> str:
    # No content excerpts. Suspicious filenames are identified by a stable digest.
    if (any(ord(c) < 32 or ord(c) > 126 for c in path)
            or scan_text('', path, '') or re.search(r'[:=@?\\]', path)):
        return 'path-sha256:' + hashlib.sha256(os.fsencode(path)).hexdigest()[:16]
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all', action='store_true', help='also scan non-ignored untracked files; never Git history')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--base', help='also inspect every commit tree and message in BASE..HEAD')
    group.add_argument('--history', action='store_true', help='also inspect all history reachable from HEAD (first push)')
    parser.add_argument('--max-file-size-mb', type=int, default=10)
    args = parser.parse_args(argv)
    if args.max_file_size_mb < 1:
        parser.error('--max-file-size-mb must be positive')
    try:
        findings, count = scan_repository(ROOT, scan_all=args.all, base=args.base, history=args.history, max_mb=args.max_file_size_mb)
        spec = importlib.util.spec_from_file_location('env_ignore_policy', ROOT / 'scripts/validate-env-ignore-policy.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        findings.extend(Finding('error', code, path, 'env-policy') for code, path in module.validate(ROOT))
    except ScanError as exc:
        print('Git safety check blocked: ' + str(exc))
        return 2
    except (OSError, ValueError, ImportError):
        print('Git safety check blocked: repository or policy read failed; no raw diagnostic emitted.')
        return 2
    print(f'Git safety check: index + worktree; inspected {count} entries')
    print('History: ' + ('selected' if args.base is not None or args.history else 'not scanned'))
    print('Coverage: heuristic UTF-8 text <= 1 MiB; binary content excluded; ignored untracked files excluded.')
    for f in findings:
        print(f'[{f.severity}] {f.source} {display_path(f.path)}:{f.line or 0} {f.rule}')
    errors = sum(f.severity == 'error' for f in findings)
    print(f'Errors: {errors}; warnings: {len(findings)-errors}. Review warnings individually; no automatic cleanup.')
    return int(errors > 0)

if __name__ == '__main__':
    sys.exit(main())
