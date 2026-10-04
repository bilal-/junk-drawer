# junk-drawer

Every house has one drawer where the useful things end up: the tape, the
batteries, the key nobody can place but nobody throws out. This is that
drawer, for agent skills.

Each skill is a plain `SKILL.md` in the open [Agent Skills](https://agentskills.io)
format, so it works in Claude Code, Codex, Gemini CLI, and most other agent
harnesses. Install one, or the whole drawer.

## What's in the drawer

<!-- skills: written by tools/build.py from drawer.json -->
| Skill | What it does |
| --- | --- |
| [`docsmith`](skills/docsmith/SKILL.md) | Reviews or builds decks, spreadsheets, documents, Markdown, and wiki pages: structure, layout, accessibility, editability, formulas, and charts. Follows your DESIGN.md, brand, or template. Fixes the small things, flags the big ones. |
| [`night-shift`](skills/night-shift/SKILL.md) | Reviews, fixes, and refactors a codebase in rounds, with a second model as reviewer, until a round comes back clean. Built to run while you sleep. |
| [`unslop`](skills/unslop/SKILL.md) | Makes a draft read like a person wrote it: strips chat residue, checks facts and story, cuts the patterns that mark text as machine-written, keeps the writer's voice. |
<!-- /skills -->

## Install

Pick whichever suits you. Each way works for one skill or for all of them.

### With `npx skills` (recommended)

[`skills`](https://github.com/vercel-labs/skills) is an open installer that
knows where some sixty agent harnesses keep their skills, and installs into
every one it finds.

```sh
npx skills add bilal-/junk-drawer --skill unslop -g    # one skill, every harness, for your user
npx skills add bilal-/junk-drawer --all                 # everything, no questions
npx skills add bilal-/junk-drawer --list                # see what's here first
```

Add `-a <harness>` to install for one harness only, for example
`-a claude-code`, `-a codex`, `-a qwen-code`, `-a kimi-code-cli`, or
`-a antigravity-cli`. It needs Node.js, and it sends anonymous install counts;
see its README to turn that off.

### With `curl`, no Node needed

```sh
curl -fsSL https://raw.githubusercontent.com/bilal-/junk-drawer/main/install.sh | sh                  # everything
curl -fsSL https://raw.githubusercontent.com/bilal-/junk-drawer/main/install.sh | sh -s -- unslop     # one skill
```

It downloads the drawer and copies the skills into every harness it finds:
Claude Code, Codex, Gemini CLI, Antigravity CLI, Qwen Code, OpenCode, GitHub
Copilot, Cursor, and the shared `~/.agents/skills` folder. It never replaces a
skill of the same name that it did not install, unless you pass `--force`, and
then it keeps the old one as a backup. Pass `--dry-run` to see what it would
do, `--agent <name>` to pick a harness, and `--dir <path>` for any other.

Read [`install.sh`](install.sh) before you pipe it to `sh`; it is short on
purpose.

### By hand

A skill is one folder. Copy it into your harness's skills folder:

| Harness | Skills folder |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| Antigravity CLI (`agy`) | `~/.gemini/antigravity-cli/skills/` |
| Qwen Code | `~/.qwen/skills/` |
| Kimi Code CLI, and others that share it | `~/.agents/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| GitHub Copilot | `~/.copilot/skills/` |
| Cursor | `~/.cursor/skills/` |

Each skill here is a single file today, so this is enough:

```sh
mkdir -p ~/.claude/skills/unslop
curl -fsSL https://raw.githubusercontent.com/bilal-/junk-drawer/main/skills/unslop/SKILL.md \
  -o ~/.claude/skills/unslop/SKILL.md
```

For a project instead of your user, use the same folder names inside the
project (for example `.claude/skills/`).

### From a marketplace

| Harness | Add the drawer | Install a skill |
| --- | --- | --- |
| Claude Code | `/plugin marketplace add bilal-/junk-drawer` | `/plugin install unslop@junk-drawer` |
| Codex | `codex plugin marketplace add bilal-/junk-drawer` | `codex plugin add unslop@junk-drawer` |
| Gemini CLI | `gemini extensions install https://github.com/bilal-/junk-drawer` | (installs every skill) |

Each skill is its own plugin, and `the-whole-drawer` installs them all.

## Updating and removing

| How you installed | Update | Remove |
| --- | --- | --- |
| `npx skills` | `npx skills update` | `npx skills remove unslop` |
| `curl` | run the same command again | add `--uninstall` |
| From a checkout (`./install.sh --link`) | `git pull` | `./install.sh --uninstall` |
| Claude Code | `/plugin marketplace update junk-drawer` | `/plugin uninstall unslop@junk-drawer` |
| Codex | `codex plugin marketplace upgrade junk-drawer` | `codex plugin remove unslop@junk-drawer` |
| Gemini CLI | `gemini extensions update junk-drawer` | `gemini extensions uninstall junk-drawer` |

## Adding a skill

1. Make `skills/<name>/SKILL.md`, with `name` and `description` frontmatter.
2. Add it to [`drawer.json`](drawer.json).
3. Run `tools/build.py` to write every harness's manifest, and commit them.

`tools/check.sh` checks all of this, and runs before every commit once you run
`tools/setup.sh`. See [`AGENTS.md`](AGENTS.md) for the rules.

## License

[MIT](LICENSE).
