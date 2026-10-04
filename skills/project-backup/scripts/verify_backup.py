#!/usr/bin/env python3
"""Verify package bytes without opening credentials as text or changing data."""
import hashlib
import re
import sys
from pathlib import Path


def verify(root):
    expected_paths = set(); failures = []
    for line in (root / 'SHA256SUMS.txt').read_text().splitlines():
        expected, relative = line.split('  ', 1); rel = Path(relative)
        if rel.is_absolute() or '..' in rel.parts or not re.fullmatch('[0-9a-f]{64}', expected):
            raise ValueError('Invalid checksum record')
        if relative in expected_paths: raise ValueError('Duplicate checksum record')
        expected_paths.add(relative); target = root / rel
        if target.is_symlink() or not target.is_file(): failures.append(relative); continue
        h = hashlib.sha256()
        with target.open('rb') as f:
            for data in iter(lambda: f.read(1024 * 1024), b''): h.update(data)
        if h.hexdigest() != expected: failures.append(relative)
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name != '.DS_Store'}
    if actual != expected_paths | {'SHA256SUMS.txt'}: failures.append('unlisted or missing files')
    if any(p.is_symlink() for p in root.rglob('*')): failures.append('symlink in package')
    if failures:
        print('Integrity check failed:', *failures, sep='\n  '); return 1
    print('Verified %d files. No data changed.' % len(expected_paths)); return 0


if __name__ == '__main__':
    # Installed helper accepts a path; the packaged Tools/verify-backup.py locates its own root.
    root = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) == 2 else Path(__file__).resolve().parents[1]
    try: sys.exit(verify(root))
    except (ValueError, OSError) as e: raise SystemExit('Verification stopped: ' + str(e))
