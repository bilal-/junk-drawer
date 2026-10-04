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
BACKUPS="${JUNK_DRAWER_BACKUPS:-$HOME/.junk-drawer-backups}"

usage() {
  cat <<'EOF'
Usage: install.sh [options] [skill ...]

Installs the named skills (all of them if none are named) into the skills
folder of every agent harness found on this machine.

Options:
  --agent NAME   Install for this harness only; repeat for more. One of:
                 claude codex agents gemini antigravity qwen opencode copilot cursor
  --dir PATH     Install into PATH instead (any harness not listed above).
  --link         Link to this checkout instead of copying (edits show at once).
  --copy         Copy, even from a checkout.
  --force        Replace a skill of the same name that this script did not
                 install. The old one is moved to the backups folder.
  --uninstall    Remove skills this script installed, instead of installing.
                 A copy you have changed since is moved to the backups folder.
  --dry-run      Say what would happen; change nothing.
  --list         List the skills in the drawer and exit.
  -h, --help     This help.

Backups go to ~/.junk-drawer-backups, outside every skills folder, so no
harness loads an old copy as a skill.

Environment: JUNK_DRAWER_REF picks a branch or tag (default: main);
JUNK_DRAWER_BACKUPS picks the backups folder.
EOF
}

say() { printf '%s\n' "$*"; }
fail() { printf 'install.sh: %s\n' "$*" >&2; exit 1; }

# Lists below hold one item per line, so paths may contain spaces.
nl='
'

# Every harness this script knows: a name, its skills folder, and the folder
# whose presence means the harness is installed, separated by "|".
harnesses() {
  codex_home="${CODEX_HOME:-$HOME/.codex}"
  cat <<EOF
claude|$HOME/.claude/skills|$HOME/.claude
codex|$codex_home/skills|$codex_home
agents|$HOME/.agents/skills|$HOME/.agents
gemini|$HOME/.gemini/skills|$HOME/.gemini
antigravity|$HOME/.gemini/antigravity-cli/skills|$HOME/.gemini/antigravity-cli
qwen|$HOME/.qwen/skills|$HOME/.qwen
opencode|$HOME/.config/opencode/skills|$HOME/.config/opencode
copilot|$HOME/.copilot/skills|$HOME/.copilot
cursor|$HOME/.cursor/skills|$HOME/.cursor
EOF
}

agents=""
targets=""
skills=""
mode=""
force=0
uninstall=0
dry=0
list=0

while [ $# -gt 0 ]; do
  case "$1" in
    --agent) [ $# -ge 2 ] || fail "--agent needs a name"; agents="$agents$2$nl"; shift 2 ;;
    --dir) [ $# -ge 2 ] || fail "--dir needs a path"; targets="$targets$2$nl"; shift 2 ;;
    --link) mode='link'; shift ;;
    --copy) mode='copy'; shift ;;
    --force) force=1; shift ;;
    --uninstall) uninstall=1; shift ;;
    --dry-run) dry=1; shift ;;
    --list) list=1; shift ;;
    -h|--help) usage; exit 0 ;;
    -*) fail "unknown option $1 (see --help)" ;;
    *) skills="$skills$1$nl"; shift ;;
  esac
done

# Where the skills come from: this checkout if the script is in one,
# otherwise a fresh download of the repository.
here=""
case "$0" in
  */install.sh) here=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd) ;;
esac
if [ -n "$here" ] && [ -f "$here/drawer.json" ] && [ -d "$here/skills" ]; then
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

available=$(cd "$source_dir" && for d in */; do
  if [ -f "$d/SKILL.md" ]; then printf '%s\n' "${d%/}"; fi
done)

if [ "$list" = 1 ]; then
  printf '%s\n' "$available"
  exit 0
fi

# From here on, loops split lists on newlines only, and never expand a * or ?
# in a name or path.
IFS=$nl
set -f

if [ -z "$skills" ]; then
  skills=$available
else
  for s in $skills; do
    printf '%s\n' "$available" | grep -Fqx -- "$s" || fail "no skill named $s (see --list)"
  done
fi

# The folders to install into: the named harnesses and folders, or every
# harness present.
known=$(harnesses)
for a in $agents; do
  line=$(printf '%s\n' "$known" | awk -F'|' -v a="$a" '$1 == a')
  [ -n "$line" ] || fail "unknown harness $a (see --help)"
  targets="$targets$(printf '%s' "$line" | cut -d'|' -f2)$nl"
done
if [ -z "$targets" ]; then
  for line in $known; do
    if [ -d "$(printf '%s' "$line" | cut -d'|' -f3)" ]; then
      targets="$targets$(printf '%s' "$line" | cut -d'|' -f2)$nl"
    fi
  done
fi
[ -n "$targets" ] || fail "no agent harness found; name one with --agent or a folder with --dir"

run() {
  if [ "$dry" = 1 ]; then (IFS=' '; say "  would: $*"); else "$@"; fi
}

# Everything in a copied skill, as its marker records it: each file with its
# checksum, each link with its target, each folder by name, anything else
# (a pipe, say) by name without opening it.
contents() {
  (cd "$1" && find . ! -name . ! -name "$MARK" | LC_ALL=C sort | while IFS= read -r f; do
    if [ -L "$f" ]; then printf 'link %s -> %s\n' "$f" "$(readlink "$f")"
    elif [ -d "$f" ]; then printf 'dir %s\n' "$f"
    elif [ -f "$f" ]; then printf 'file %s %s\n' "$(cksum <"$f" | awk '{print $1, $2}')" "$f"
    else printf 'other %s\n' "$f"
    fi
  done)
}

# Whether $1 is a skill this script installed and nobody has changed since: a
# link to a skill in a junk-drawer checkout, or a copy whose files all match
# its marker.
ours() {
  if [ -L "$1" ]; then
    to=$(readlink "$1")
    [ "$(basename -- "$(dirname -- "$to")")" = skills ] &&
      grep -q '"name": "junk-drawer"' "$(dirname -- "$(dirname -- "$to")")/drawer.json" 2>/dev/null
  else
    [ -f "$1/$MARK" ] && [ "$(sed 1d "$1/$MARK")" = "$(contents "$1")" ]
  fi
}

# Moves $1 into the backups folder, under a name nothing else has, and says
# where. The backups sit outside every skills folder, so no harness loads them.
back_up() {
  backup="$BACKUPS/$(basename -- "$1")-$(date +%Y%m%d%H%M%S)"
  n=1
  while [ -e "$backup" ] || [ -L "$backup" ]; do
    n=$((n + 1))
    backup="$BACKUPS/$(basename -- "$1")-$(date +%Y%m%d%H%M%S)-$n"
  done
  say "keep $1 as $backup"; run mkdir -p "$BACKUPS"; run mv "$1" "$backup"
}

for target in $targets; do
  target=${target%/}
  for s in $skills; do
    dest="$target/$s"
    if [ "$uninstall" = 1 ]; then
      if ours "$dest"; then
        say "remove $dest"; run rm -rf "$dest"
      elif [ -f "$dest/$MARK" ]; then
        say "$dest has changed since it was installed"; back_up "$dest"
      elif [ -e "$dest" ] || [ -L "$dest" ]; then
        say "skip $dest: not installed by the junk drawer"
      fi
      continue
    fi
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      if ours "$dest"; then
        run rm -rf "$dest"
      elif [ "$force" = 1 ] || [ -f "$dest/$MARK" ]; then
        back_up "$dest"
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
      if [ "$dry" = 0 ]; then
        { printf '%s@%s\n' "$REPO" "$REF"; contents "$dest"; } >"$dest/$MARK"
      fi
    fi
  done
done

if [ "$dry" = 1 ]; then say "dry run: nothing changed"; else say "done"; fi
