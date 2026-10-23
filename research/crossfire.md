# Research: crossfire

Background for `skills/crossfire/SKILL.md`. The skill comes from a real run on
2026-10-23: a phone app's conversation view, pairing scanner, third-party
credits, app size and a new agents list, reviewed in two rounds by Claude Opus
5.5, Claude Fable 5.1, Codex gpt-6.1-sol and Codex gpt-6-astra (both Codex at
`xhigh`). Earlier, a streaming redesign went through the same loop with the same
four reviewers. Evidence below is from those runs unless noted.

## Why several reviewers, in sequence

**Later reviewers still find blocking issues.** In round 1, each of the four
reviewers found between five and six blocking issues the previous ones had missed:
the first separated bugs from design, the second showed a planned fix couldn't
work because the code evicted what it widened to find, the third showed a
"waiting for input" detector would lock ordinary conversations, the fourth showed
a "phone-only" release contained a wire change that would break older servers.
Round 2 still found blocking issues, mostly introduced by round-1 fixes.
Evidence: two runs, one project. Weak in general, but consistent.

**Different families catch different things.** The Claude reviewers were
strongest on user experience, missing states and plan order; the Codex reviewers
on protocol compatibility, races and budget arithmetic. Order mattered less than
covering both. Evidence: two runs; anecdotal.

**Sequence helped; parallel wasn't tried.** Each reviewer read a revision with
earlier findings already fixed, so later reviews went deeper instead of repeating.
No parallel run was compared, so this isn't a measured advantage. The one review
that ran against a stale revision (below) repeated the previous review's findings
almost exactly.

## Failures the rules prevent

- **Stale draft after a failed save.** The disk filled while revision 8 was being
  written; the save failed silently and the next reviewer reviewed revision 7.
  Rule: save each revision to a temporary file, read it back before renaming, hash
  the saved files, and have each reviewer report the revision it read.
- **Reviewers can't write in read-only mode.** Claude Code in plan mode reported it
  couldn't save its review into the reviews folder; the review was only in its
  output. Rule: capture the CLI's answer (stdout, JSON `result`, or Codex's `-o`
  file). (Plan mode itself was later dropped; see the second review below.)
- **Stdin wait.** Without `< /dev/null`, Claude Code waited and warned about
  missing stdin data. Rule: no interactive input; a prompt piped from a file is
  fine, and avoids the argument-size limit.
- **Silent substitution.** The owner named "Codex sol 5.5", which didn't exist; the
  owner chose `gpt-6.1-sol` when asked. Rule: list real model IDs, never
  substitute silently.
- **Fixes that contradict other sections.** Several round-2 findings were a fix in
  one part contradicting another (an "only optional field" claim in the order of
  work after the design required paged snapshots; mockups promising a stage-2
  feature in stage 1). Rule: fix every place a change touches.
- **Reviewers wrong in detail.** Reviewers cited wrong line numbers, overstated
  size savings that didn't apply to store downloads, and guessed at formats.
  Rule: verify each claim before adopting it.
- **Privacy.** A past reviewer's whole-home search triggered an operating-system
  permission prompt attributed to the product. Rule: the brief limits reviewers to
  named paths and excludes private data.

## Read-only modes

From each CLI's `--help` on 2026-10-23 (superseded for Claude Code and Antigravity by
the findings below; plan modes aren't treated as read-only any more): Claude Code `--permission-mode plan`,
Codex `exec -s read-only`, Gemini CLI and Qwen Code `--approval-mode plan`,
Antigravity `--mode plan`, OpenCode `run --agent plan` (agent-configurable),
Pi `--tools` allow-list or `--no-tools`. Evidence: tool documentation; flags
change between versions, so the skill says to confirm with `--help`.

## Smoke tests, 2026-10-23

Run on one Mac with seven agent CLIs installed: Claude Code and Codex reviewed
fine; OpenCode answered in `--agent plan`; Antigravity worked once the prompt was
put after `-p` (it treats the next argument as the prompt) and, in plan mode,
wrote a plan file and asked for approval; Gemini CLI first overrode `plan` to
`default` because the folder wasn't trusted, then failed on account eligibility;
Qwen Code had no auth type; Pi had no API key. Rules from this: smoke-test in the
read-only mode itself, read stderr for silent mode changes, and treat "installed"
and "available" as different.


## Isolation, from the skill's own first review (2026-10-23)

- **Read-only isn't isolated.** A Claude Code reviewer in `--permission-mode plan`
  ran the owner's SessionStart hook, loaded MCP servers that can create documents,
  and had web fetching available; Codex in `-s read-only` also ran the owner's
  hooks. Tested replacements: Claude Code with `--setting-sources "" --tools
  "Read,Grep,Glob" --strict-mcp-config --output-format json` answered and reported
  the resolved model; `--bare` failed for a subscription login ("Not logged in").
  Codex with `--ephemeral --ignore-user-config -s read-only -o FILE` answered, and
  its stderr header showed `sandbox: read-only` and the reasoning effort.
- **Stderr holds whole transcripts.** Codex wrote 460–580 KB of stderr per review,
  including file contents, into the reviews folder that later reviewers were told to
  read. Rule: logs go to `logs/`, excluded by the brief; `-o` captures only the
  answer.
- **Empty review files.** Redirecting stdout creates the review file before the run;
  a failed run left an empty file that looked finished. Rule: temporary file, renamed
  on success.
- **A stale review was never re-run.** The review of the stale revision became the
  run's final verdict. Rule: reviewers state the revision they read; a mismatch is
  re-run and doesn't count.
- **Editing during a review.** The author's investigation notes were kept in a
  separate file during reviews in the real run, which avoided a reviewer reading a
  half-edited design. Rule: notes file during reviews, fold in at the next revision.
- **Time and cost.** Eight reviews took about two hours; one Codex review used
  142,345 tokens; one ran 57 minutes.

Judgement calls without measurement, stated as such in the skill: a different model
family last in each round; ordering decisions by when they're needed; top-tier models
with the strongest reasoning setting for design review.

## From the skill's second review (Antigravity, 2026-10-23)

- **Plan mode isn't read-only in Antigravity.** The reviewer reported that
  `--mode plan` only prepended a planning instruction; shell, write, web and
  sub-agent tools remained declared, and the owner's start-up hook ran and injected
  another session's summary. A canary asking it to create a file created none, which
  shows the model declined, not that it couldn't. Rule: read-only must come from the
  tool list or sandbox; canaries are secondary.
- **Headless denial looks like success.** Its first run exited 0 with no output: a
  tool needing the "command" permission was auto-denied in headless mode. Rule:
  success requires a non-empty answer with the right revision line. It then reviewed
  successfully from about 45 KB of pasted material with tools forbidden.
- **Isolated reads stop at the working folder.** A Claude reviewer with
  `--setting-sources "" --tools Read,Grep,Glob` was denied a file in `~/.config`;
  with `--add-dir` for that folder it read it.
- **Plan mode and JSON output.** Reported, not reproduced: with Claude's plan mode,
  `result` can hold only a final "couldn't save the plan" note. The tool list already
  makes it read-only, so plan mode was dropped.
- **Stating the revision in the prompt defeats the stale-revision check.** A
  reviewer can echo it without reading the file. Rule: the prompt never states it.

The early-stop rules (same blocker in two consecutive rounds, judgement
disagreements, scope growth) are judgement calls from the Shellbell runs, where
repeated findings on the same subject needed owner decisions rather than more
revisions.


## From the skill's third review (Claude Fable, 2026-10-23)

- **Codex logs in the evidence repository.** The Codex command used a relative
  `logs/` path while every CLI runs from the evidence folder, so its transcript
  would have landed in the repository. Rule: logs use an absolute path in a sibling
  folder no reviewer can read.
- **Instruction files, tested.** In a scratch repository with a `CLAUDE.md` saying
  to start every reply with a code word, Claude Code with `--setting-sources ""`
  replied plainly; without it, it used the code word.
- **Codex reads the whole disk.** In `-s read-only`, Codex printed a line from a
  file under `~/.config` outside its working folder with no extra flag. Only the
  brief limits its reads.
- **Claude Code exposes `--effort`** (low to max on 2026-10-23); this run's own
  Claude reviews used the default, which the skill now corrects.
- **Stale files in multi-file subjects.** A revision number kept only in `log.md`
  can't show that one file of several failed to save; line counts per file can.
- **Time limits.** The longest real review took 57 minutes, so a 60-minute limit
  would kill comparable reviews and the rerun rule would repeat them unchanged.

## From the skill's fourth review (Codex gpt-6-astra, max, 2026-10-23)

- **Line counts don't identify content.** The reviewer showed a one-line change to a
  command that kept the file's line count. Rule: content hashes identify a
  revision; the reviewer's revision line is only a cheap check.
- **Accepted isn't folded.** A review accepted just before a session ended would have
  been skipped on resume. Rule: received, accepted and folded states in the log.
- **Unbounded retries.** The retry rule had no ceiling. Rule: a run ceiling and one
  retry per reviewer by default, as night-shift bounds its recovery.
- **Claude flags, tested.** `--safe-mode` (all customizations off) with
  `--effort max` and `--no-session-persistence` answered normally; a prompt piped on
  stdin worked, which avoids the argument-size limit of `"$(cat file)"`.

## From the skill's fifth review (Claude Opus, max effort, round 2, 2026-10-23)

- **The author is the only judge of findings.** r1-4 proposed `--restricted` and
  frozen snapshots; neither appeared in revision 5 and the log gave no reason. Rule:
  every rejection is logged with its reason, judgement-based rejections of blockers
  go to the owner, and the hand-over lists them.
- **Secrets were only excluded by wording.** Ignored `.env` files and keys can sit in
  the evidence working tree, and listing them in the brief tells every reviewer
  where they are. Rule: review from a fresh worktree of the pinned commit, exclude
  by pattern, cite secrets by path only, scan answers before passing them on.
- **Codex's read-only sandbox runs commands.** Real Codex reviews logged dozens of
  shell executions under `sandbox: read-only`. Rule: read-only means no writes and
  no network, not no commands. Codex web search is off unless `--search` is passed.
- **Antigravity stdin, tested.** `agy -p -` sent a literal "-" as the prompt, so a
  pasted packet must fit in an argument.
- **Owner-chosen alternatives go unreviewed.** The Shellbell run ended with 22
  decisions, some forking contracts; reviewers mostly tested the recommended
  options. Rule: note which options were reviewed, ask contract-forking decisions
  between reviews, offer a targeted review of an unreviewed choice.
- **Prior art.** In the Shellbell run the owner had to ask for it, and it changed the
  internal model (ACP-shaped types). Rule: look for prior art before the first
  draft.
- **Hand-typed commands broke four times** in the skill's own run: Codex's
  repository check, Antigravity's `-p` ordering, Antigravity's silent empty answer,
  and the relative log path.
- **Unsourced judgement calls**, stated as such: pinning the evidence commit,
  mockup screenshots for reviewers, coverage notes and the author-side injection
  rule come from these reviews' reasoning, not from an observed failure.

## From the skill's sixth review (Antigravity, round 2, 2026-10-23)

- **Worktree gaps.** Revision 6 put reviewers in a pinned worktree but didn't copy
  later revisions or uncommitted evidence into it, and the brief still named the
  live working tree, which isolated reviewers could only reach by re-exposing ignored
  secrets. Rule: the brief names worktree paths; copy each revision in.
- **A design can't hold its own hashes.** Rule: `log.md` is mandatory and holds the
  operational record; this run's own revision-5 and revision-6 entries also omitted
  the brief's hash, which revision 7 adds.
- **Antigravity plan mode, tested again.** Without `--mode plan`, a request to write
  a file in an empty repository was still auto-denied ("write_file permission … auto-
  denied") and no file appeared. Plan mode only adds an instruction to write a plan
  file, so it was dropped. A pasted packet sits in the process list for the whole run.
- **Unchecked answers.** Answers renamed into the reviews folder before the checks
  could be read by a parallel reviewer. Rule: answers stay in the logs folder until
  accepted and scanned.

## From the skill's seventh review (Claude Fable, max effort, round 2, 2026-10-23)

- **Half-applied fix.** Revision 7 moved answers to the logs folder for Claude, Codex
  and Antigravity but left `$OUT.tmp` in the reviews folder for OpenCode, Pi, Gemini
  and Qwen. The same class of failure the skill warns about: a fix in one place,
  not every place it touches.
- **Codex hooks, tested.** A default `codex exec` printed four `hook: SessionStart`
  lines on stderr; with `--ignore-user-config`, none. Rule: check for `hook:` lines
  as part of the isolation check.
- **This run skipped its own worktree rule.** The brief named the live repository,
  and the acceptance checks couldn't notice. Rule: creating the worktree is a
  numbered setup action, acceptance checks every brief path, and reviewing an
  uncommitted subject in place is a logged owner decision.
- **History is reachable.** A worktree's `.git` file points at the main repository's
  objects, stashes and config, and Codex can run read-only git commands. Rule: scan
  history and config, and forbid them in the brief.

## From the skill's eighth review (Codex gpt-6-astra, max, round 2, 2026-10-23)

- **The acceptance check's own false positive.** The run's ad hoc check counted 11
  `hook:` matches in Codex's stderr and rejected the review; none were hooks. Codex's
  stderr holds the text of every file read, and the skill's own files quote
  `hook: SessionStart`. Anchored to the start of a line, the count was 0. Rule: count
  only whole lines shaped like the hook notice. The helper script does this, with a
  test.
- **`--restricted`, tested.** Without it, a read of `/etc/hosts` was refused only
  because a headless run couldn't ask permission; with it, the flag itself confined
  file tools to the working folders, and reads inside still worked. The earlier
  rejection reason (the tool list already removes command tools) answered a
  different question; the finding was reopened on a flaw in that reason, as the
  brief allows, and adopted.
- **Path checks, packet order, dirty evidence.** The brief must name the logs folder
  to forbid it, so "every path in the brief" was the wrong test; packet building
  before the log update froze the old revision number; commit plus `git status`
  can't show an already-modified file changing again. Rules: input paths only,
  checked before launch; one ordered save sequence; snapshots hash copied and
  external evidence.

## Owner decisions, 2026-10-23

- Ship the helper script with the skill, tested in `tools/test-crossfire.py`.
- The secret scan includes local git history and config.
- This run reviewed uncommitted files in place in the owner's own repository, as a
  logged exception.

