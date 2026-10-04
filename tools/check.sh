#!/bin/sh
# Every check the drawer has. Runs before each commit (tools/setup.sh).
set -eu
cd "$(dirname "$0")/.."
python3 tools/build.py --check
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck -s sh install.sh tools/check.sh tools/setup.sh
else
  echo "shellcheck not installed: install.sh not linted" >&2
fi
sh -n install.sh
./install.sh --list >/dev/null
echo "check: ok"
