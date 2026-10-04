#!/bin/sh
# Installs skills from the junk drawer into every agent harness on this machine.
#
#   curl -fsSL https://raw.githubusercontent.com/bilal-/junk-drawer/main/install.sh | sh
#   curl -fsSL .../install.sh | sh -s -- unslop night-shift
#   ./install.sh --agent claude --link unslop     (from a checkout)
#
# Run with --help for every option. Read it before you pipe it to sh: it is
# short on purpose.

set -eu

REPO="bilal-/junk-drawer"
REF="${JUNK_DRAWER_REF:-main}"
MARK=".junk-drawer"

usage() {
  cat <<'EOF'
Usage: install.sh [options] [skill ...]

Installs the named skills (all of them if none are named) into the skills
folder of every agent harness found on this machine.

Options:
  --agent NAME   Install for this harness only; repeat for more. One of:
                 claude codex agents gemini antigravity qwen opencode copilot cursor
  --dir PATH     Also install into PATH (any harness not listed above).
  --link         Link to this checkout instead of copying (edits show at once).
  --copy         Copy, even from a checkout.
  --force        Replace a skill of the same name that this script did not
                 install. The old one is kept as NAME.backup-<time>.
  --uninstall    Remove skills this script installed, instead of installing.
  --dry-run      Say what would happen; change nothing.
  --list         List the skills in the drawer and exit.
  -h, --help     This help.

Environment: JUNK_DRAWER_REF picks a branch or tag (default: main).
EOF
}

say() { printf '%s\n' "$*"; }
fail() { printf 'install.sh: %s\n' "$*" >&2; exit 1; }

# Every harness this script knows: a name, its skills folder, and the folder
# whose presence means the harness is installed.
harnesses() {
  home="$HOME"
  codex_home="${CODEX_HOME:-$home/.codex}"
  cat <<EOF
claude $home/.claude/skills $home/.claude
codex $codex_home/skills $codex_home
agents $home/.agents/skills $home/.agents
gemini $home/.gemini/skills $home/.gemini
antigravity $home/.gemini/antigravity-cli/skills $home/.gemini/antigravity-cli
qwen $home/.qwen/skills $home/.qwen
opencode $home/.config/opencode/skills $home/.config/opencode
copilot $home/.copilot/skills $home/.copilot
cursor $home/.cursor/skills $home/.cursor
EOF
}

agents=""
dirs=""
skills=""
mode=""
force=0
uninstall=0
dry=0
list=0

while [ $# -gt 0 ]; do
  case "$1" in
    --agent) [ $# -ge 2 ] || fail "--agent needs a name"; agents="$agents $2"; shift 2 ;;
    --dir) [ $# -ge 2 ] || fail "--dir needs a path"; dirs="$dirs $2"; shift 2 ;;
    --link) mode='link'; shift ;;
    --copy) mode='copy'; shift ;;
    --force) force=1; shift ;;
    --uninstall) uninstall=1; shift ;;
    --dry-run) dry=1; shift ;;
    --list) list=1; shift ;;
    -h|--help) usage; exit 0 ;;
    -*) fail "unknown option $1 (see --help)" ;;
    *) skills="$skills $1"; shift ;;
  esac
done

# Where the skills come from: this checkout if the script is in one,
# otherwise a fresh download of the repository.
here=""
case "$0" in
  */install.sh) here=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd) ;;
esac
if [ -n "$here" ] && [ -d "$here/skills" ]; then
  source_dir="$here/skills"
  [ -n "$mode" ] || mode='link'
else
  [ "$mode" != link ] || fail "--link needs a checkout; run ./install.sh from one"
  mode='copy'
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT INT TERM
  command -v curl >/dev/null 2>&1 || fail "curl is needed to download the skills"
  curl -fsSL "https://codeload.github.com/$REPO/tar.gz/$REF" | tar -xz -C "$tmp" ||
    fail "could not download $REPO@$REF"
  source_dir=$(find "$tmp" -mindepth 2 -maxdepth 2 -type d -name skills | head -n 1)
  [ -n "$source_dir" ] || fail "the download has no skills folder"
fi

available=$(cd "$source_dir" && for d in */; do [ -f "$d/SKILL.md" ] && printf '%s\n' "${d%/}"; done)

if [ "$list" = 1 ]; then
  printf '%s\n' "$available"
  exit 0
fi

if [ -z "$skills" ]; then
  skills=$available
else
  for s in $skills; do
    printf '%s\n' "$available" | grep -qx "$s" || fail "no skill named $s (see --list)"
  done
fi

# The folders to install into: the named harnesses, or every one present.
targets=""
known=$(harnesses)
if [ -n "$agents" ]; then
  for a in $agents; do
    line=$(printf '%s\n' "$known" | awk -v a="$a" '$1 == a')
    [ -n "$line" ] || fail "unknown harness $a (see --help)"
    targets="$targets $(printf '%s' "$line" | awk '{print $2}')"
  done
else
  targets=$(printf '%s\n' "$known" | while read -r _ folder marker; do
    if [ -d "$marker" ]; then printf '%s ' "$folder"; fi
  done)
fi
targets="$targets $dirs"
[ -n "$(printf '%s' "$targets" | tr -d ' ')" ] ||
  fail "no agent harness found; name one with --agent or a folder with --dir"

run() {
  if [ "$dry" = 1 ]; then say "  would: $*"; else "$@"; fi
}

# Whether $1 is a skill this script installed: a link into a junk drawer, or
# a copy carrying the marker file.
ours() {
  if [ -L "$1" ]; then
    case "$(readlink "$1")" in */skills/*) [ -f "$1/$MARK" ] || [ -f "$(readlink "$1")/SKILL.md" ] ;; *) false ;; esac
  else
    [ -f "$1/$MARK" ]
  fi
}

for target in $targets; do
  for s in $skills; do
    dest="$target/$s"
    if [ "$uninstall" = 1 ]; then
      if [ -e "$dest" ] || [ -L "$dest" ]; then
        if ours "$dest"; then
          say "remove $dest"; run rm -rf "$dest"
        else
          say "skip $dest: not installed by the junk drawer"
        fi
      fi
      continue
    fi
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      if ours "$dest"; then
        run rm -rf "$dest"
      elif [ "$force" = 1 ]; then
        backup="$dest.backup-$(date +%Y%m%d%H%M%S)"
        say "keep the old $s as $backup"; run mv "$dest" "$backup"
      else
        say "skip $dest: a skill of that name is already there (use --force to replace it)"
        continue
      fi
    fi
    run mkdir -p "$target"
    if [ "$mode" = link ]; then
      say "link $dest"; run ln -s "$source_dir/$s" "$dest"
    else
      say "copy $dest"; run cp -R "$source_dir/$s" "$dest"
      if [ "$dry" = 0 ]; then printf '%s@%s\n' "$REPO" "$REF" >"$dest/$MARK"; fi
    fi
  done
done

if [ "$dry" = 1 ]; then say "dry run: nothing changed"; else say "done"; fi
