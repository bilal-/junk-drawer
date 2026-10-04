#!/bin/sh
# Every check the drawer has. Runs before each commit (tools/setup.sh).
set -eu
unset CDPATH
cd "$(dirname "$0")/.."
python3 tools/build.py --check
python3 tools/test-build.py
tools/test-tools.sh
python3 tools/test-backup.py
tools/test-bump.sh
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck -s sh install.sh tools/*.sh
else
  echo "shellcheck not installed: install.sh not linted" >&2
fi
tools/test-install.sh
if command -v dash >/dev/null 2>&1; then tools/test-install.sh dash; fi
echo "check: ok"
