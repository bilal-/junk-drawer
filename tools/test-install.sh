#!/bin/sh
# Tests install.sh in a throwaway home whose path has a space in it.
#   tools/test-install.sh [shell]    (default: sh; try dash or "bash --posix")
# shellcheck disable=SC2016,SC2034 # check() evaluates its expressions, and $status, later
set -eu
cd "$(dirname "$0")/.."
shell=${1:-sh}
root=$(pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT INT TERM
export HOME="$work/a home"
unset CODEX_HOME
skills="$HOME/.claude/skills"
failures=0

# Runs install.sh and keeps its exit status in $status, so a failure is
# checked, not fatal.
install() {
  if $shell "$root/install.sh" "$@" >"$work/out" 2>&1; then status=0; else status=$?; fi
}
check() {
  if eval "$2"; then :; else
    echo "FAIL: $1"; sed 's/^/    /' "$work/out"; failures=$((failures + 1))
  fi
}
reset() { rm -rf "$HOME"; mkdir -p "$skills"; }

reset
install --link unslop
check "links into a harness that is present" '[ -L "$skills/unslop" ] && [ -f "$skills/unslop/SKILL.md" ]'
check "installs only the skill named" '[ ! -e "$skills/docsmith" ]'
check "leaves absent harnesses alone" '[ ! -e "$HOME/.codex" ]'
install --uninstall unslop
check "uninstall removes its own link" '[ ! -e "$skills/unslop" ] && [ ! -L "$skills/unslop" ]'

reset
install --copy unslop
check "copies with a marker" '[ -f "$skills/unslop/$(printf .junk-drawer)" ] && [ ! -L "$skills/unslop" ]'
install --copy unslop
check "reinstalls over its own unchanged copy without a backup" '[ -z "$(ls "$skills" | grep backup)" ]'
echo "mine" >"$skills/unslop/notes.txt"
install --uninstall unslop
check "uninstall keeps a copy the user changed, as a backup" '[ ! -e "$skills/unslop" ] && cat "$skills"/unslop.backup-*/notes.txt | grep -q mine'
rm -rf "$skills"/unslop.backup-*
install --copy unslop
ln -s /tmp "$skills/unslop/added-link"
install --uninstall unslop
check "uninstall keeps a copy the user added a link to" '[ -L "$skills"/unslop.backup-*/added-link ]'

reset
mkdir "$skills/unslop" && echo "theirs" >"$skills/unslop/SKILL.md"
install unslop
check "skips a skill it did not install" 'grep -q theirs "$skills/unslop/SKILL.md"'
install --uninstall unslop
check "uninstall leaves a skill it did not install" 'grep -q theirs "$skills/unslop/SKILL.md"'
install --force unslop
check "--force keeps the old skill as a backup" 'grep -q theirs "$skills"/unslop.backup-*/SKILL.md && [ -L "$skills/unslop" ]'
mkdir "$skills/docsmith"
install --force docsmith
install --uninstall docsmith
mkdir "$skills/docsmith"
install --force docsmith
check "a second backup in the same second gets its own name" '[ "$(ls -d "$skills"/docsmith.backup-* | wc -l | tr -d " ")" = 2 ]'

reset
mkdir -p "$work/elsewhere/skills/unslop" && touch "$work/elsewhere/skills/unslop/SKILL.md"
ln -s "$work/elsewhere/skills/unslop" "$skills/unslop"
install --uninstall unslop
check "uninstall leaves a link it did not make" '[ -L "$skills/unslop" ]'
install unslop
check "install skips a link it did not make" '[ "$(readlink "$skills/unslop")" = "$work/elsewhere/skills/unslop" ]'

reset
install --dir "$work/other place" --copy night-shift
check "--dir takes a path with a space" '[ -f "$work/other place/night-shift/SKILL.md" ]'
check "--dir alone installs nowhere else" '[ ! -e "$skills/night-shift" ]'
mkdir -p "$work/glob/a" "$work/glob/b"
install --dir "$work/glob/*" --copy night-shift
check "--dir takes a * literally" '[ -f "$work/glob/*/night-shift/SKILL.md" ] && [ ! -e "$work/glob/a/night-shift" ]'

install unslo.
check "rejects a skill that does not exist" '[ "$status" != 0 ]'
install --agent nope
check "rejects an unknown harness" '[ "$status" != 0 ]'
reset
install --dry-run --copy unslop
check "a dry run changes nothing" '[ -z "$(ls -A "$skills")" ]'
check "a dry run prints each command on one line" 'grep -q "would: cp -R .*unslop" "$work/out"'

if [ "$failures" = 0 ]; then echo "test-install ($shell): ok"; else exit 1; fi
