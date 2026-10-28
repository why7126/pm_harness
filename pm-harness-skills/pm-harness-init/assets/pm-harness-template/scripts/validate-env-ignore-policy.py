#!/usr/bin/env python3
"""Read-only env ignore policy: examples trackable, real env ignored and untracked."""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REAL = ('.env', '.env.local', '.env.production', 'deploy/local/runtime.env', 'deploy/prod/runtime.env', 'scripts/build-images.env')
EXAMPLES = tuple(p + '.example' for p in REAL)


def ignored(root, path):
    result = subprocess.run(['git', '--no-optional-locks', 'check-ignore', '--no-index', '-q', '--', path], cwd=root,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode not in (0, 1):
        raise OSError('ignore-check-failed')
    return result.returncode == 0


def validate(root=ROOT):
    issues = []
    for path in REAL:
        if not ignored(root, path):
            issues.append(('env-ignore-missing', path))
    for path in EXAMPLES:
        if ignored(root, path):
            issues.append(('env-example-ignored', path))
    proc = subprocess.run(['git', '--no-optional-locks', 'ls-files', '-z'], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise OSError('index-read-failed')
    for raw in proc.stdout.split(b'\0'):
        path = os.fsdecode(raw)
        name = Path(path).name
        if path and not name.endswith('.example') and (name == '.env' or name.startswith('.env.') or name.endswith('.env')):
            issues.append(('real-env-tracked', path))
    return issues


if __name__ == '__main__':
    try:
        issues = validate()
        # Paths from user files may themselves be sensitive; never echo them here.
        for code, _ in issues:
            print('[error] ' + code)
        print(f'Env policy errors: {len(issues)}')
        sys.exit(bool(issues))
    except OSError:
        print('Env policy unavailable; Git read failed.')
        sys.exit(2)
