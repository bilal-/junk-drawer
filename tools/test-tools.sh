#!/bin/sh
# Tests that the tools scripts work on this checkout and nowhere else, run
# from a copy of it in a throwaway folder.
set -eu
unset CDPATH
cd "$(dirname "$0")/.."
# shellcheck source=tools/test-lib.sh
. tools/test-lib.sh
scratch tools
isolate_git
failures=0
fail() { echo "FAIL: $1"; failures=$((failures + 1)); }

mkdir "$work/drawer" "$work/decoy" "$work/decoy/tools"
cp -R tools "$work/drawer/"
git init -q "$work/drawer"
(cd "$work/drawer" && CDPATH="$work/decoy" sh tools/setup.sh) >/dev/null 2>&1 || true
[ ! -e "$work/decoy/.githooks" ] || fail "setup.sh followed CDPATH into another folder"
[ "$(git -C "$work/drawer" config core.hooksPath)" = .githooks ] || fail "setup.sh did not set up its own checkout"

if [ "$failures" = 0 ]; then echo "test-tools: ok"; else exit 1; fi
