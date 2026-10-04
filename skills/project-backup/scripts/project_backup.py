#!/usr/bin/env python3
"""Local recovery packages. No provider calls, uploads, or source mutations."""

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import stat
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from verify_backup import checksum_failures, digest

PRUNE = {
    '.git',
    'node_modules',
    '.next',
    '.turbo',
    '.astro',
    'dist',
    'build',
    'coverage',
    '.venv',
    'venv',
    'vendor',
    'target',
    '.cache',
    'Pods',
    'DerivedData',
    '.gradle',
    '.expo',
    '__pycache__',
    '.worktrees',
    '.superpowers',
    '.playwright-mcp',
    '.orchid',
    '.wrangler',
}
MARKERS = {
    'package.json',
    'pyproject.toml',
    'Cargo.toml',
    'go.mod',
    'composer.json',
    'Gemfile',
    'Package.swift',
    'pom.xml',
    'pubspec.yaml',
    'deno.json',
    'deno.jsonc',
    'Dockerfile',
    'DockerFile',
}
# Data exports kept in a project's backups/ folder: what inventory lists and
# include_historical_exports takes.
EXPORT_SUFFIXES = {'.sql', '.sqlite', '.sqlite3', '.db', '.zip', '.tar', '.gz'}
PRIVATE_SUFFIXES = {'.p8', '.p12', '.jks', '.keystore', '.mobileprovision', '.pem', '.key'}
GENERATED = {'MANIFEST.json', 'SHA256SUMS.txt'}


def private_candidate(path):
    name = path.name.lower()
    if name.endswith(('.example', '.sample', '.template')) or name == 'debug.keystore':
        return False
    if name.startswith(('.env', '.dev.vars')) or path.suffix.lower() in PRIVATE_SUFFIXES:
        return True
    if name in {
        'google-services.json',
        'googleservice-info.plist',
        'key.properties',
        'account-details.json',
        'android-signing.json',
    }:
        return True
    return path.suffix.lower() in {'.json', '.yaml', '.yml', '.toml'} and any(
        label in name
        for label in ['service-account', 'service_account', 'firebase-adminsdk', 'credential', 'secret']
    )


def now():
    return datetime.now(timezone.utc).isoformat()


def expand(path):
    return Path(path).expanduser().absolute()


def safe_relative(value):
    p = Path(value)
    if not value or p.is_absolute() or '..' in p.parts or '\n' in value or '\r' in value:
        raise ValueError('Unsafe package-relative path')
    return p


def git(path, *args, check=True):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    r = subprocess.run(['git', '-C', str(path), *args], capture_output=True, env=env)
    if check and r.returncode:
        raise RuntimeError('Git operation failed: ' + ' '.join(args[:2]))
    return r.stdout


def walk_files(root, prune=PRUNE):
    for base, dirs, files in os.walk(root, followlinks=False):
        p = Path(base)
        dirs[:] = sorted(d for d in dirs if d not in prune and not (p / d).is_symlink())
        for name in sorted(files):
            q = p / name
            if name != '.DS_Store' and q.is_file() and not q.is_symlink():
                yield q


def worktrees(path):
    output = git(path, 'worktree', 'list', '--porcelain', '-z').decode('utf-8')
    records = []
    current = {}
    for item in output.split('\0'):
        if not item:
            if current:
                records.append(current)
                current = {}
        elif item.startswith('worktree '):
            current['path'] = item[9:]
        elif item.startswith('HEAD '):
            current['head'] = item[5:]
        elif item.startswith('branch '):
            current['branch'] = item[7:]
        elif item == 'detached':
            current['detached'] = True
        elif item == 'bare':
            current['bare'] = True
    if current:
        records.append(current)
    for row in records:
        p = Path(row['path'])
        row['available'] = p.is_dir()
        row['dirty'] = (
            bool(git(p, 'status', '--porcelain', '-z')) if p.is_dir() and not row.get('bare') else False
        )
    return records


def discover(roots):
    roots = [expand(p) for p in roots]
    repos = {}
    components = []
    loose = []
    for root in roots:
        if not root.is_dir() or root.is_symlink():
            raise ValueError('Workspace root missing or symlinked')
        for base, dirs, files in os.walk(root, followlinks=False):
            p = Path(base)
            dirs[:] = sorted(d for d in dirs if d not in PRUNE and not (p / d).is_symlink())
            if (p / '.git').exists():
                common = git(p, 'rev-parse', '--path-format=absolute', '--git-common-dir').decode().strip()
                if common not in repos:
                    repos[common] = {
                        'id': p.name,
                        'path': str(p),
                        'root': str(root),
                        'kind': 'git',
                        'common_directory': common,
                        'worktrees': worktrees(p),
                    }
                continue
            if (
                MARKERS.intersection(files)
                and not any(p.is_relative_to(Path(r['path'])) for r in repos.values())
                and not any(c['path'] == str(p) for c in components)
            ):
                components.append(
                    {'id': p.name, 'path': str(p), 'root': str(root), 'kind': 'files', 'worktrees': []}
                )
        covered = [Path(r['path']) for r in list(repos.values()) + components]
        loose.extend(uncovered(root, covered))
    projects = list(repos.values()) + components
    counts = {}
    for p in projects:
        counts[p['id']] = counts.get(p['id'], 0) + 1
    for p in projects:
        if counts[p['id']] > 1:
            p['id'] += '-' + hashlib.sha256(p['path'].encode()).hexdigest()[:8]
        p['local_recovery_candidates'] = [
            {'path': str(q.relative_to(Path(p['path']))), 'bytes': q.stat().st_size}
            for q in walk_files(p['path'])
            if private_candidate(q)
            or (
                'backups' in q.parts and q.suffix.lower() in EXPORT_SUFFIXES
            )
        ]
    return {
        'created_at_utc': now(),
        'roots': [str(p) for p in roots],
        'projects': sorted(projects, key=lambda r: r['id']),
        'unassigned_paths': sorted(set(loose)),
    }


def uncovered(folder, covered):
    """Paths under folder that belong to no project. A folder holding a project
    is opened, so what sits beside that project is listed too."""
    for p in sorted(folder.iterdir()):
        if p.name in PRUNE or p.name == '.DS_Store' or p.is_symlink() or p in covered:
            continue
        if any(p in q.parents for q in covered):
            yield from uncovered(p, covered)
        else:
            yield str(p)


def clean_remote(url):
    if '://' not in url:
        return url
    p = urlsplit(url)
    host = p.hostname or ''
    if ':' in host:
        host = '[' + host + ']'
    if p.port:
        host += ':' + str(p.port)
    return urlunsplit((p.scheme, host, p.path, '', ''))


class Package:
    def __init__(self, destination, extend=False):
        self.root = expand(destination)
        self.sources = {}
        self.project_index = []
        self.missing = []
        self.previous = {}
        if self.root.exists():
            if not extend or self.root.is_symlink() or not (self.root / 'MANIFEST.json').is_file():
                raise ValueError('Existing destination requires a verified package and --extend')
            verify(self.root)
            self.previous = json.loads((self.root / 'MANIFEST.json').read_text())
            for row in self.previous.get('files', []):
                self.sources[row['path']] = {
                    k: v for k, v in row.items() if k not in {'path', 'bytes', 'sha256'}
                }
        else:
            self.root.mkdir(parents=True, mode=0o700)
        os.chmod(self.root, 0o700)

    def target(self, relative):
        p = self.root / safe_relative(str(relative))
        parent = p.parent
        while parent != self.root:
            if parent.is_symlink():
                raise ValueError('Symlink in destination')
            parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            os.chmod(parent, 0o700)
            parent = parent.parent
        if p.is_symlink():
            raise ValueError('Symlink destination')
        return p

    def write(self, relative, value, kind='documentation', replace=False):
        p = self.target(relative)
        if p.exists() and not replace:
            raise ValueError('Destination collision: ' + str(relative))
        data = value if isinstance(value, bytes) else value.encode('utf-8')
        flags = os.O_WRONLY | os.O_CREAT | (os.O_TRUNC if replace else os.O_EXCL)
        fd = os.open(p, flags, 0o600)
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
        os.chmod(p, 0o600)
        self.sources[str(relative)] = {'source': None, 'kind': kind}
        return p

    def write_json(self, relative, obj, **kw):
        return self.write(relative, json.dumps(obj, indent=2, ensure_ascii=False) + '\n', **kw)

    def copy(self, source, relative, description='', restore=''):
        source = expand(source)
        if not source.is_file():
            raise ValueError('Required source missing: ' + str(source))
        dest = self.target(relative)
        if dest.exists():
            raise ValueError('Destination collision: ' + str(relative))
        before = digest(source)
        with source.open('rb') as src, dest.open('xb') as dst:
            shutil.copyfileobj(src, dst, 1024 * 1024)
        os.chmod(dest, 0o600)
        if before != digest(source) or before != digest(dest):
            dest.unlink()
            raise RuntimeError('Source changed while copying: ' + str(source))
        self.sources[str(relative)] = {
            'source': str(source),
            'kind': 'verified-copy',
            'description': description,
            'restore': restore,
        }
        return dest

    def readme(self, relative, text):
        return self.write(str(Path(relative) / 'README.txt'), text.rstrip() + '\n')

    def tree(self, source, relative, description, restore=''):
        source = expand(source)
        if not source.is_dir():
            raise ValueError('Required directory missing')
        self.readme(relative, description + '\n\n' + restore)
        for p in walk_files(source):
            rel = Path(relative) / p.relative_to(source)
            if rel.name == 'README.txt':
                rel = rel.with_name('SOURCE-README.txt')
            self.copy(p, str(rel), description, restore)

    def explicit(self, entries, prefix=''):
        groups = {}
        for item in entries:
            if not item.get('description') or not item.get('restore'):
                raise ValueError('Each explicit file needs description and restore instructions')
            relative = str(Path(prefix) / safe_relative(item['destination']))
            self.copy(item['source'], relative, item['description'], item['restore'])
            groups.setdefault(str(Path(relative).parent), []).append(item)
        for folder, items in groups.items():
            path = self.target(str(Path(folder) / 'README.txt'))
            block = '\n'.join(
                '\n' + Path(i['destination']).name + '\n' + i['description'] + '\nRestore: ' + i['restore']
                for i in items
            )
            if path.exists():
                block = path.read_text() + '\nAdditional files\n' + block
            self.write(str(Path(folder) / 'README.txt'), block + '\n', replace=path.exists())

    def sqlite(self, source, relative):
        source = expand(source)
        dest = self.target(relative)
        if dest.exists():
            raise ValueError('Database destination collision')
        deadline = time.monotonic() + 20

        def progress(status, remaining, total):
            if time.monotonic() > deadline:
                raise RuntimeError('SQLite snapshot exceeded its bounded capture window')

        def capture(input_path, readonly):
            uri = input_path.as_uri() + '?mode=ro' if readonly else str(input_path)
            src = sqlite3.connect(uri, uri=readonly, timeout=5)
            dst = sqlite3.connect(dest)
            try:
                src.backup(dst, pages=256, progress=progress)
                if dst.execute('PRAGMA integrity_check').fetchone() != ('ok',):
                    raise RuntimeError('SQLite snapshot integrity check failed')
            finally:
                src.close()
                dst.close()

        kind = 'sqlite-online-backup'
        try:
            capture(source, True)
        except sqlite3.OperationalError as e:
            # A closed WAL-mode database can lack sidecars that a readonly opener
            # needs. Never open the original for writing or ignore an existing WAL.
            sidecars = [source.with_name(source.name + s) for s in ['-wal', '-shm', '-journal']]
            if str(e) != 'unable to open database file' or any(p.exists() for p in sidecars):
                raise RuntimeError('SQLite capture failed for ' + str(source) + ' (' + type(e).__name__ + ')')
            before = digest(source)
            with tempfile.TemporaryDirectory(prefix='project-backup-closed-sqlite-') as tmp:
                frozen = Path(tmp) / 'source.sqlite'
                shutil.copyfile(source, frozen)
                os.chmod(frozen, 0o600)
                if before != digest(frozen) or before != digest(source) or any(p.exists() for p in sidecars):
                    raise RuntimeError('Closed SQLite source changed while copying')
                if dest.exists():
                    dest.unlink()
                capture(frozen, False)
                if before != digest(source) or any(p.exists() for p in sidecars):
                    raise RuntimeError('Closed SQLite source changed during backup')
            kind = 'sqlite-online-backup-from-stable-closed-file-copy'
        os.chmod(dest, 0o600)
        self.sources[str(relative)] = {
            'source': str(source),
            'kind': kind,
            'integrity_check': 'ok',
            'environment': 'local development',
        }

    def project(self, project, override, account_notes):
        p = Path(project['path'])
        folder_name = override.get('folder_name', project['id'])
        if len(safe_relative(folder_name).parts) != 1:
            raise ValueError('Invalid project folder name')
        base = 'Projects/' + folder_name
        if (self.root / base).exists():
            raise ValueError('Project folder already exists: ' + project['id'])
        self.readme(
            base,
            'Project: ' + project['id'] + '\nSource repository location: ' + str(p) + '\n\n'
            'This folder contains private configuration, credentials, recovery records\n'
            'and selected persistent data. Repository source and tracked documentation\n'
            'remain in Git and are excluded by default.\n\n' + override.get('notes', '') + '\n\nRestore\n'
            '1. Verify this package with Tools/verify-backup.py. Obtain the project from Git.\n'
            '2. Restore private files to the paths listed in FILES.json, adjusting for\n'
            '   the new computer. Preserve key aliases, passwords, identities and counters.\n'
            '3. Restore hosted secret values from actual copied keys or the private vault.\n'
            '   A PROVIDER-RECORD lists names and settings; it cannot restore secret values.\n'
            '4. Test any data import in isolation before changing a running service.\n'
            '5. Reauthenticate provider accounts and recreate OS permissions normally.\n\n'
            'Source instructions remain in the repository. This is not a full production\n'
            'restore qualification.\n',
        )
        hosting = base + '/Hosting'
        self.readme(
            hosting,
            'Hosting recovery\n\n' + account_notes + '\n\n'
            'Hosting configuration and operating guides remain in Git.\n'
            'See provider records/exports when present. Secret-name records\n'
            'cannot restore secret values. Keep original encryption keys\n'
            'with encrypted data; replacing them loses access.\n',
        )
        config_files = [
            q.name for q in p.glob('wrangler*') if q.is_file() and q.suffix in {'.jsonc', '.json', '.toml'}
        ]
        env_names = set()
        private_files = []
        tracked = set(git(p, 'ls-files', '-z').split(b'\0')) if project['kind'] == 'git' else set()
        for q in walk_files(p):
            rel = q.relative_to(p)
            name = q.name
            is_private = private_candidate(q) and os.fsencode(str(rel)) not in tracked
            if is_private:
                target = (
                    base
                    + '/Private Configuration/'
                    + str(rel.with_name('dot-' + name[1:] if name.startswith('.') else name))
                )
                self.copy(
                    q,
                    target,
                    'Private local configuration/signing material',
                    'Restore to ' + str(rel) + ' within the project; keep it ignored by Git.',
                )
                private_files.append(str(rel))
            if q.suffix in {'.ts', '.tsx', '.js', '.mjs', '.cjs'} and q.stat().st_size < 2 * 1024 * 1024:
                env_names.update(
                    re.findall(r'\b(?:env|bindings)\.([A-Z][A-Z0-9_]+)', q.read_text(errors='replace'))
                )
        if private_files:
            self.readme(
                base + '/Private Configuration',
                'Private local files. FILES.json records original paths and usage.\n'
                'Names beginning dot- represent original dotfiles, which are renamed here for\n'
                'visibility during folder upload. Restore their exact original names.\n'
                'These files may contain development-only values; do not assume production parity.\n',
            )
        exports = p / 'backups'
        if override.get('include_historical_exports', False) and exports.is_dir():
            candidates = [
                q
                for q in walk_files(exports)
                if q.suffix.lower() in EXPORT_SUFFIXES
            ]
            if candidates:
                self.readme(
                    base + '/Recorded Data Exports',
                    'Previously saved data exports, copied byte-for-byte.\n'
                    'Inspect names, timestamps and the project runbooks for environment.\n'
                    'These historical files are separate from newly captured production exports.\n'
                    'Test an import in isolation before using an export for recovery.\n',
                )
                for q in candidates:
                    self.copy(
                        q,
                        base + '/Recorded Data Exports/' + str(q.relative_to(exports)),
                        'Previously saved project data export',
                        'Use the original project backup/restore runbook; verify date and environment first.',
                    )
        local = p / '.wrangler/state/v3'
        local_count = 0
        for area in ['d1', 'r2', 'kv']:
            source = local / area
            if not override.get('include_local_data', False) or not source.is_dir():
                continue
            for q in walk_files(source, prune={'.git', '__pycache__'}):
                if q.name.endswith(('-wal', '-shm', '-journal')):
                    continue
                target = (
                    base + '/Local Development Data/Cloudflare/' + area + '/' + str(q.relative_to(source))
                )
                if q.suffix in {'.sqlite', '.sqlite3', '.db'}:
                    self.sqlite(q, target)
                else:
                    self.copy(
                        q,
                        target,
                        'Local development object/storage bytes',
                        'Recreate local emulator storage only after reviewing paths and metadata.',
                    )
                local_count += 1
        if local_count:
            self.readme(
                base + '/Local Development Data',
                'Local Cloudflare emulator data, not production exports.\n'
                'SQLite snapshots include committed WAL contents via the online backup API.\n'
                'Other stored objects are verified file copies. This is a live development\n'
                'capture, not a coordinated cross-resource stopped-service snapshot.\n'
                'Restore in an isolated local environment; do not import these fixtures into production.\n',
            )
        self.explicit(override.get('files', []), base)
        remotes = []
        if project['kind'] == 'git':
            for line in git(p, 'remote', '-v').decode().splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    remotes.append({'name': parts[0], 'url': clean_remote(parts[1])})
        record = {
            'id': project['id'],
            'path': str(p),
            'kind': project['kind'],
            'captured_at_utc': now(),
            'hosting_config_files_in_git': config_files,
            'source_environment_names': sorted(env_names),
            'private_local_files': private_files,
            'local_storage_files': local_count,
            'remotes': remotes,
            'missing': override.get('missing', []),
            'production_restore_tested': False,
        }
        self.write_json(base + '/PROJECT-RECORD.json', record)
        files = {k[len(base) + 1 :]: v for k, v in self.sources.items() if k.startswith(base + '/')}
        self.write_json(base + '/FILES.json', files)
        self.missing.extend(project['id'] + ': ' + m for m in override.get('missing', []))
        self.project_index.append(
            {'id': project['id'], 'source': str(p), 'kind': project['kind'], 'folder': base}
        )
        print('Captured project: ' + project['id'], flush=True)

    def finish(self, profile, inventory):
        self.explicit(profile.get('shared_files', []) + profile.get('tool_files', []))
        for area in profile.get('loose_areas', []):
            self.tree(area['source'], area['destination'], area['description'], area.get('restore', ''))
        self.missing.extend(profile.get('missing', []))
        old_missing = self.previous.get('missing', [])
        self.missing.extend(m for m in old_missing if isinstance(m, str))
        self.write_json(
            'WORKSPACE-INVENTORY.json', inventory, replace=(self.root / 'WORKSPACE-INVENTORY.json').exists()
        )
        lines = [
            '# Projects in this recovery package',
            '',
            '| Project | Source | Folder |',
            '| --- | --- | --- |',
        ]
        known = {r['folder'] for r in self.project_index}
        projects_folder = self.root / 'Projects'
        for p in sorted(projects_folder.iterdir() if projects_folder.is_dir() else []):
            if p.is_dir() and str(p.relative_to(self.root)) not in known:
                prefix = str(p.relative_to(self.root)) + '/'
                source = next(
                    (
                        v.get('source')
                        for k, v in self.sources.items()
                        if k.startswith(prefix) and 'git-bundle' in v.get('kind', '') and v.get('source')
                    ),
                    'Existing package or reviewed archive',
                )
                self.project_index.append(
                    {'id': p.name, 'source': source, 'folder': str(p.relative_to(self.root))}
                )
        for r in sorted(self.project_index, key=lambda r: r['id']):
            lines.append('| %s | %s | %s |' % (r['id'], r['source'], r['folder']))
        self.write(
            'PROJECTS-INDEX.md', '\n'.join(lines) + '\n', replace=(self.root / 'PROJECTS-INDEX.md').exists()
        )
        self.write(
            'MISSING-ASSETS.md',
            '# Recovery gaps\n\n' + '\n'.join('- ' + m for m in sorted(set(self.missing))) + '\n\n'
            'A listed account/resource is not a backup of its data. Source and checksum\n'
            'verification do not establish store delivery or a full production restore.\n',
            replace=(self.root / 'MISSING-ASSETS.md').exists(),
        )
        self.write_json(
            'Tools/backup-profile.json', profile, replace=(self.root / 'Tools/backup-profile.json').exists()
        )
        verifier = Path(__file__).with_name('verify_backup.py')
        # An extended backup already has a verifier; replace it with this one.
        if (self.root / 'Tools/verify-backup.py').is_file():
            (self.root / 'Tools/verify-backup.py').unlink()
        self.copy(
            verifier,
            'Tools/verify-backup.py',
            'Standalone read-only checksum verifier',
            'Run python3 Tools/verify-backup.py from any working directory.',
        )
        tools_readme = self.root / 'Tools/README.txt'
        self.write(
            'Tools/README.txt',
            (tools_readme.read_text() if tools_readme.exists() else '') + '\nVerification and refresh\n'
            'Run python3 /path/to/package/Tools/verify-backup.py after copying or downloading.\n'
            'backup-profile.json records reviewed sources and instructions for a future\n'
            'refresh; update machine paths and pending items. It contains no key values.\n',
            replace=tools_readme.exists(),
        )
        root_readme = self.root / 'README.txt'
        root_note = '\nWorkspace backup update: ' + now() + '\n'
        root_note += (
            'Projects are indexed in PROJECTS-INDEX.md. Recovery gaps are listed in\n'
            'MISSING-ASSETS.md. Read each project README and original runbooks.\n'
            'This package contains plaintext private credentials and client data.\n'
            'Keep the destination restricted to its owner; never commit it to Git.\n'
            'Original files were copied and left in place. No upload was performed.\n'
            'After a manual upload, download the package and run Tools/verify-backup.py\n'
            'before deleting this local copy. Keep an independent recovery copy.\n'
            'Future refreshes should create a new dated destination.\n'
        )
        self.write(
            'README.txt',
            (root_readme.read_text() if root_readme.exists() else 'Private project recovery package\n')
            + root_note,
            replace=root_readme.exists(),
        )
        # Selected private folders also get concise recovery explanations.
        for p in sorted(self.root.rglob('*')):
            if p.is_dir() and not (p / 'README.txt').exists():
                folder = str(p.relative_to(self.root))
                self.readme(
                    folder,
                    'Folder: ' + folder + '\n'
                    'Read the nearest project README and FILES.json for original paths and\n'
                    'restore instructions. Files in this private package are independent\n'
                    'copies. Verify the top-level checksums before using them.\n',
                )
        rows = []
        for p in sorted(walk_files(self.root, prune=set())):
            rel = str(p.relative_to(self.root))
            if rel in GENERATED:
                continue
            rows.append(
                {
                    'path': rel,
                    'bytes': p.stat().st_size,
                    'sha256': digest(p),
                    **self.sources.get(rel, {'source': None, 'kind': 'existing-private-copy'}),
                }
            )
        previous_meta = {k: v for k, v in self.previous.items() if k != 'files'}
        manifest = {
            'schema_version': 2,
            'created_at_utc': now(),
            'files': rows,
            'projects': self.project_index,
            'missing': sorted(set(self.missing)),
            'previous_capture_metadata': previous_meta,
            'drive_upload_performed': False,
            'full_restore_rehearsal_performed': False,
        }
        self.write_json('MANIFEST.json', manifest, replace=(self.root / 'MANIFEST.json').exists())
        checks = [r['sha256'] + '  ' + r['path'] for r in rows]
        checks.append(digest(self.root / 'MANIFEST.json') + '  MANIFEST.json')
        self.write(
            'SHA256SUMS.txt',
            '\n'.join(sorted(checks)) + '\n',
            replace=(self.root / 'SHA256SUMS.txt').exists(),
        )
        verify(self.root)
        print(
            json.dumps(
                {
                    'destination': str(self.root),
                    'files': len(rows) + 2,
                    'bytes': sum(p.stat().st_size for p in walk_files(self.root, prune=set())),
                    'project_entries': len(self.project_index),
                    'missing_items': len(set(self.missing)),
                }
            ),
            flush=True,
        )


def verify(destination):
    """Checks the package against its checksums, as the standalone verifier
    does, and that it is still private: owner-only, a README in every folder."""
    root = expand(destination)
    if root.is_symlink():
        raise RuntimeError('Package contains a symlink')
    failures, count = checksum_failures(root)
    if failures:
        raise RuntimeError('Backup integrity failure: ' + ', '.join(failures))
    for p in [root] + list(root.rglob('*')):
        if p.is_dir() and not (p / 'README.txt').is_file():
            raise RuntimeError('Folder lacks README: ' + str(p))
        if stat.S_IMODE(p.stat().st_mode) & 0o077:
            raise RuntimeError('Non-private package permissions')
    print('Verified %d checksummed files; no source data changed.' % count, flush=True)


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    inv = sub.add_parser('inventory')
    inv.add_argument('--root', action='append', required=True)
    inv.add_argument('--output', required=True)
    build = sub.add_parser('build')
    build.add_argument('--profile', required=True)
    build.add_argument('--destination', required=True)
    build.add_argument('--extend', action='store_true')
    check = sub.add_parser('verify')
    check.add_argument('--destination', required=True)
    args = parser.parse_args()
    if args.command == 'inventory':
        data = discover(args.root)
        target = expand(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink():
            raise ValueError('Symlink inventory output')
        target.write_text(json.dumps(data, indent=2) + '\n')
        os.chmod(target, 0o600)
        print(
            json.dumps(
                {
                    'projects': len(data['projects']),
                    'unassigned_paths': len(data['unassigned_paths']),
                    'output': str(target),
                }
            )
        )
        return
    if args.command == 'verify':
        verify(args.destination)
        return
    profile = json.loads(expand(args.profile).read_text())
    if profile.get('schema_version') != 1:
        raise ValueError('Unsupported profile schema')
    dest = expand(args.destination)
    # The backup must not land inside anything it copies, or it copies itself.
    # Compare real paths: a link (macOS's /tmp, say) can name the same folder twice.
    real_dest = dest.resolve()
    for source in profile['roots'] + [area['source'] for area in profile.get('loose_areas', [])]:
        real_source = expand(source).resolve()
        if real_dest.is_relative_to(real_source) or real_source.is_relative_to(real_dest):
            raise ValueError('Source and destination must be separate trees')
    inventory = discover(profile['roots'])
    package = Package(dest, args.extend)
    for project in inventory['projects']:
        override = profile.get('projects', {}).get(project['id'], {})
        if not override.get('exclude', False):
            package.project(
                project,
                override,
                profile.get('account_notes', 'Follow the account rules in the project instructions.'),
            )
    package.finish(profile, inventory)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, sqlite3.Error) as e:
        raise SystemExit('Backup stopped: ' + str(e))
