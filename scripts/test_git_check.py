#!/usr/bin/env python3
"""Regression suite using synthetic content and disposable Git repositories."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent

def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

scan = load('git_check_tested', 'git-check.py')
env = load('env_policy_tested', 'validate-env-ignore-policy.py')
IGNORE = '.env\n.env.*\n*.env\n!.env.example\n!.env.*.example\n!*.env.example\n'

class GitSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.test')
        self.write('.gitignore', IGNORE)
        self.git('add', '.gitignore')
        self.git('commit', '-qm', 'baseline')
        self.base = self.git('rev-parse', 'HEAD').decode().strip()

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, stderr=subprocess.DEVNULL)

    def write(self, path, content):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)

    def secret(self, value=None):
        return 'password' + ' = "' + (value or 'synthetic-' + 'credential-987654') + '"\n'

    def findings(self, **kwargs):
        return scan.scan_repository(self.root, **kwargs)[0]

    def test_index_secret_survives_clean_worktree_and_does_not_write(self):
        self.write('a.txt', self.secret()); self.git('add', 'a.txt')
        before = self.git('ls-files', '--stage', '-z')
        self.write('a.txt', 'clean\n')
        self.assertTrue(any(f.source == 'index' and f.rule == 'assigned-secret' for f in self.findings()))
        self.assertEqual(before, self.git('ls-files', '--stage', '-z'))

    def test_worktree_secret_separate_from_index(self):
        self.write('a.txt', 'clean'); self.git('add', 'a.txt')
        self.write('a.txt', self.secret())
        f = self.findings()
        self.assertTrue(any(x.source == 'worktree' and x.rule == 'assigned-secret' for x in f))
        self.assertFalse(any(x.source == 'index' for x in f))

    def test_history_detects_removed_intermediate_secret_and_commit_message(self):
        self.write('old.txt', self.secret()); self.git('add', 'old.txt'); self.git('commit', '-qm', 'temporary')
        self.git('rm', '-q', 'old.txt'); self.git('commit', '-qm', self.secret())
        f = self.findings(base=self.base)
        self.assertTrue(any(x.path == 'old.txt' and x.source.startswith('history:') for x in f))
        self.assertTrue(any(x.path == 'COMMIT_MESSAGE' for x in f))
        self.assertTrue(self.findings(history=True))
        with self.assertRaises(scan.ScanError):
            self.findings(base='missing-ref')

    def test_all_excludes_ignored_env_but_scans_untracked(self):
        self.write('.env', self.secret()); self.write('new.txt', self.secret())
        f = self.findings(scan_all=True)
        self.assertFalse(any(x.path == '.env' for x in f))
        self.assertTrue(any(x.path == 'new.txt' for x in f))
        self.git('add', '-f', '.env')
        self.assertTrue(any(x.path == '.env' and x.source == 'index' for x in self.findings()))
        self.assertIn(('real-env-tracked', '.env'), env.validate(self.root))

    def test_exact_placeholders_not_substrings_or_url_queries(self):
        for value in ['example-secret-123', 'localhost-secret-123', 'change-me-secret-123', 'secret?1234567']:
            self.assertTrue(scan.scan_text('a', self.secret(value), 'test'))
        for value in ['<password>', '${PASSWORD}', 'change-me']:
            self.assertFalse(scan.scan_text('a', self.secret(value), 'test'))
        url = 'mysql' + '://real:secret-value@example.com/db?safe=1'
        self.assertTrue(scan.scan_text('a', url, 'test'))
        safe = 'mysql' + '://example:change-me@localhost/db'
        self.assertFalse(scan.scan_text('a', safe, 'test'))

    def test_template_placeholders_are_exact_and_unquoted(self):
        for value in ['${PASSWORD}', '{PASSWORD}', '${PASSWORD:-{PASSWORD}}', 'CHANGE_ME', 'replace-with-secret-key']:
            self.assertFalse(scan.scan_text('a', 'password' + '=' + value, 'test'), value)
        for value in ['${PASSWORD}-real', '${PASSWORD:-real-secret}', '{PASSWORD}-real', 'CHANGE_ME-real', 'replace-with-secret-key-real']:
            self.assertTrue(scan.scan_text('a', 'password' + '=' + value, 'test'), value)
        self.assertFalse(scan.scan_text('a', 'Authorization' + ': Bearer <token>`', 'test'))
        self.assertFalse(scan.scan_text('compose.yml', 'MINIO_ROOT_PASSWORD' + ': ${OBJECT_STORAGE_SECRET_KEY:-{OBJECT_STORAGE_SECRET_KEY}}', 'test'))
        self.assertTrue(scan.scan_text('compose.yml', 'MINIO_ROOT_PASSWORD' + ': ${OBJECT_STORAGE_SECRET_KEY:-real-value}', 'test'))
        self.assertFalse(scan.scan_text('compose.yml', 'MINIO_ROOT_USER' + ': ${OBJECT_STORAGE_ACCESS_KEY:-{OBJECT_STORAGE_ACCESS_KEY}}', 'test'))

    def test_path_regex_has_no_whole_line_or_test_exemptions(self):
        prefixes = '/' + 'Users/|/' + 'home/'
        self.assertFalse(scan.scan_text('src/filter.py', prefixes, 'test'))
        for p in ['/' + 'Users/alice/project', '/' + 'home/alice/project', 'C:' + '\\Users\\alice\\project']:
            self.assertTrue(scan.scan_text('tests/fixture.py', 're.compile(r"' + p + '")', 'test'))
        self.assertTrue(scan.scan_text('src/filter.py', prefixes + ' ' + self.secret(), 'test'))

    def test_no_sensitive_excerpts_even_with_multiple_values(self):
        one, two = 'synthetic-one-987654', 'synthetic-two-987654'
        text = self.secret(one).strip() + '; ' + self.secret(two)
        self.write('a.txt', text); self.git('add', 'a.txt')
        # Invoke the real CLI in a fixture so reporting and integration are covered.
        for file in ['git-check.py', 'validate-env-ignore-policy.py']:
            self.write('scripts/' + file, (HERE / file).read_text())
        result = subprocess.run([sys.executable, str(self.root / 'scripts/git-check.py')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(one, result.stdout + result.stderr)
        self.assertNotIn(two, result.stdout + result.stderr)
        self.assertIn('assigned-secret', result.stdout)

    def test_env_policy_checks_both_sides(self):
        self.assertEqual(env.validate(self.root), [])
        self.write('.gitignore', '*.env*\n')
        self.assertTrue(any(code == 'env-example-ignored' for code, _ in env.validate(self.root)))
        self.write('.gitignore', '')
        self.assertTrue(any(code == 'env-ignore-missing' for code, _ in env.validate(self.root)))

    def test_special_filenames_and_links(self):
        self.write('a space\nname.txt', self.secret()); self.git('add', 'a space\nname.txt')
        f = self.findings()
        self.assertTrue(any(x.source == 'index' for x in f))
        self.assertTrue(scan.display_path('a space\nname.txt').startswith('path-sha256:'))
        (self.root / 'link').symlink_to('a space\nname.txt'); self.git('add', 'link')
        self.assertTrue(any(x.rule == 'link-or-submodule-unscanned' for x in self.findings()))

    def test_limits_nested_runtime_and_invalid_encoding(self):
        self.write('big.txt', 'a' * (scan.TEXT_LIMIT + 1)); self.git('add', 'big.txt')
        self.assertTrue(any('incomplete' in x.rule or 'unscanned' in x.rule for x in self.findings()))
        self.assertTrue(scan.forbidden('src/web/node_modules/pkg/index.js'))
        self.assertTrue(scan.scan_bytes('odd.txt', b'\xff', 'index', 10))

    def test_shallow_history_fails_closed(self):
        (self.root / '.git/shallow').write_text(self.base + '\n')
        with self.assertRaises(scan.ScanError):
            self.findings(history=True)

    def test_unmerged_index_blocks(self):
        self.write('conflict.txt', 'base\n'); self.git('add', 'conflict.txt'); self.git('commit', '-qm', 'base file')
        branch = self.git('branch', '--show-current').decode().strip()
        self.git('checkout', '-qb', 'other')
        self.write('conflict.txt', 'other\n'); self.git('commit', '-qam', 'other')
        self.git('checkout', '-q', branch)
        self.write('conflict.txt', 'main\n'); self.git('commit', '-qam', 'main')
        subprocess.run(['git', 'merge', 'other'], cwd=self.root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.assertTrue(any(x.rule == 'unmerged-index' for x in self.findings()))

    def test_large_untracked_binary_uses_actual_size(self):
        with (self.root / 'large.png').open('wb') as stream:
            stream.truncate(11 * 1024 * 1024)
        self.assertTrue(any(x.rule == 'large-file' for x in self.findings(scan_all=True)))

    def test_clean_cli_and_warning_semantics(self):
        for file in ['git-check.py', 'validate-env-ignore-policy.py']:
            self.write('scripts/' + file, (HERE / file).read_text())
        result = subprocess.run([sys.executable, str(self.root / 'scripts/git-check.py')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        f = scan.scan_text('sample.txt', 'person' + '@private.test', 'test')
        self.assertEqual(f[0].severity, 'warning')
        self.assertEqual(scan.display_path('person' + '@private.test'), 'path-sha256:' + __import__('hashlib').sha256(('person' + '@private.test').encode()).hexdigest()[:16])

if __name__ == '__main__':
    unittest.main()
