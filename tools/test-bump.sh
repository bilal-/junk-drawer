#!/bin/sh
# Tests build.py's version-bump check against real git histories, in a
# throwaway folder: each case is a published repository and a clone of it.
set -eu
cd "$(dirname "$0")/.."
root=$(pwd)
work=$(mktemp -d /tmp/junk-drawer-bump.XXXXXX)
trap 'rm -rf "$work"' EXIT INT TERM
failures=0
# Run from the pre-commit hook, git points these at the commit in progress;
# the throwaway repositories must not touch it.
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_COMMON_DIR \
  GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_PREFIX GIT_NAMESPACE
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=test@example.com
export GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=test@example.com

g() { git -c core.hooksPath=/dev/null -c init.defaultBranch=main "$@"; }

# A published repository holding the working tree's drawer, every skill at
# 1.0.0 whatever the real versions are, and a clone of it in $work/clone.
fresh() {
  rm -rf "$work/pub.git" "$work/clone"
  g init -q "$work/seed"
  cp -R "$root/skills" "$root/drawer.json" "$root/README.md" "$work/seed/"
  mkdir -p "$work/seed/tools" && cp "$root/tools/build.py" "$work/seed/tools/"
  (cd "$work/seed" && python3 -c "
import json, pathlib
p = pathlib.Path('drawer.json'); d = json.loads(p.read_text())
for s in d['skills']: s['version'] = '1.0.0'
p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')")
  g -C "$work/seed" add -A && g -C "$work/seed" commit -qm seed
  g clone -q --bare "$work/seed" "$work/pub.git" && rm -rf "$work/seed"
  g clone -q "$work/pub.git" "$work/clone"
}
in_clone() { (cd "$work/clone" && "$@"); }
set_version() {
  in_clone python3 -c "
import json, pathlib
p = pathlib.Path('drawer.json'); d = json.loads(p.read_text())
next(s for s in d['skills'] if s['name'] == '$1')['version'] = '$2'
p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')"
}
edit() { echo "edit" >>"$work/clone/skills/$1/SKILL.md"; }
commit() { in_clone g commit -qam "$1"; }
flagged() { in_clone python3 tools/build.py --check 2>&1 | grep -o "skills/[a-z-]* changed" | sed 's/ changed//' | tr '\n' ' '; }
expect() {
  got=$(flagged)
  if [ "$got" != "$2" ]; then echo "FAIL: $1: flagged '$got', expected '$2'"; failures=$((failures + 1)); fi
}

fresh
expect "a clean clone" ""
edit unslop
expect "an edit without a raise" "skills/unslop "
set_version unslop 1.0.1
expect "an edit with a raise" ""
commit "raise"; edit unslop
expect "a second edit before the push" ""

fresh
in_clone g switch -q -c feature
edit unslop
expect "a branch with no upstream" "skills/unslop "

fresh
in_clone g remote rename origin upstream
in_clone g switch -q -c feature
edit unslop
expect "a remote not named origin" "skills/unslop "

fresh
set_version unslop 1.1.0; edit unslop; commit "unslop 1.1.0"
in_clone g push -q origin HEAD:master
in_clone g remote set-head origin -d
in_clone g switch -q -c feature origin/master
in_clone g branch -q --unset-upstream
edit unslop
expect "main and master both published, made from master" "skills/unslop "

fresh
in_clone g switch -q -c topic
edit night-shift; commit "topic one"; edit night-shift; commit "topic two"
in_clone g push -q origin topic
in_clone g switch -q main
set_version night-shift 1.0.1; edit night-shift; commit "night-shift 1.0.1"
in_clone g push -q origin main
in_clone g switch -q -c feature
in_clone g merge -q -X theirs --no-edit origin/topic >/dev/null
set_version night-shift 1.0.1
expect "a branch that merged a longer topic, against main" "skills/night-shift "

fresh
in_clone g switch -q -c feature
set_version docsmith 1.0.1; commit "raise only"
expect "a raise with no edit" ""

if [ "$failures" = 0 ]; then echo "test-bump: ok"; else exit 1; fi
