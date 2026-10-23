# Reviewer CLIs

How to detect each agent CLI, list its models, and run it as an isolated, read-only,
one-shot reviewer. For Claude Code, Codex and Antigravity, `scripts/crossfire_review.py
run` builds these commands; the lines below document what it runs and cover the
other CLIs by hand. Flags change between versions: confirm each line with the CLI's
own `--help` before relying on it, and update this file when they differ.

No model names are given here on purpose: they go out of date. Use what each CLI
lists today, normally its top tier (SKILL.md, step 3).

## What every invocation must do

- **Read-only:** the CLI's tool list or sandbox forbids edits and network access.
  Some sandboxes still allow commands that only read (Codex's runs `ls`, `grep`
  and `--help`). A "plan" mode that only adds an instruction to the prompt doesn't count:
  Antigravity's plan mode left shell, write, web and sub-agent tools declared.
- **Isolated:** no hooks, no MCP servers, no web access, no user configuration
  beyond what authentication needs. Read-only modes alone don't do this: in a real
  run, a plan-mode reviewer still ran the owner's start-up hooks and loaded MCP
  servers that could create documents.
- **One shot, no interactive input:** the prompt comes from an argument or from a
  file piped to stdin, which then ends; never a terminal the CLI could wait on.
  Piping a prompt file also avoids the operating system's argument-size limit for
  large prompts, which passing `"$(cat file)"` as an argument doesn't.
- **Runs from the evidence folder,** normally a fresh `git worktree` of the pinned
  commit, so relative paths resolve, **with explicit access to the proposal and
  reviews folders, and every other evidence path,** when they live elsewhere. Isolated
  reviewers can't read outside their working folder without it: a Claude reviewer
  was denied `~/.config/...` until `--add-dir` named the folder.
- **Repository instruction files and config still load.** Most CLIs read
  `AGENTS.md`, `GEMINI.md` or similar from the working folder even when user
  configuration is off; only Claude's `--safe-mode` and `--setting-sources ""` skip
  them. Some may also load project config that redefines agents or adds plugins
  (OpenCode's `opencode.json` and Pi's project extensions are likely; unverified).
  Treat them as material, check per CLI, and be stricter on repositories or
  branches the owner doesn't control.
- **Answer to the logs folder first** (`$LOGS/$NAME.out`), moved into the reviews
  folder as `$OUT` only when accepted and scanned, so no reviewer reads an unchecked
  answer and a failed run never leaves an empty review that looks finished.
- **Logs elsewhere:** stderr and any JSON output go to the logs folder (`$LOGS`), a
  sibling of the reviews folder that no reviewer is given access to, for every CLI.
  Some CLIs write their whole transcript there, including every file they read.
  After each run, copy the header, denials, errors and token counts into `log.md`.
  Trim the raw transcript (first and last 30 lines of text; JSON by dropping its
  transcript fields, never by slicing lines) only after the review is accepted or
  at hand-over.
- **Success means more than exit code 0:** the answer is non-empty and starts with
  `Reviewed revision <N>`. A reviewer exited 0 with no output when a tool it needed
  was denied.

Record each CLI's version (`--version`) with the date in the log; flags here were
checked on 2026-10-23 against Claude Code 2.1.309, Codex CLI 0.163.0 and Antigravity
1.4.6.

Variables: `$RUN` the reviews folder, `$LOGS` the logs folder, `$DOCS` the proposal
folder, `$OUT` the review file, `$NAME` its base name, `$PROMPT` the per-reviewer
prompt text, `$PROMPT_FILE` (`$LOGS/$NAME.prompt`) holding that prompt,
`$PACKET` (`$LOGS/$NAME.packet`) the prompt plus pasted files for a pasted-material
reviewer, `$EVIDENCE` each evidence folder outside the working folder, `$MODEL` a model ID the CLI
listed today, `$EFFORT` its strongest single-task reasoning setting.

## Per CLI

### Claude Code

- Detect: `claude --version`.
- Models: `claude --help` lists `--model` aliases for the latest models; the owner
  or the harness can name full IDs. The alias isn't the record: take the resolved
  ID from the JSON output's `modelUsage`.
- Review (prompt from a file on stdin):
  `claude -p --model "$MODEL" --effort "$EFFORT" --safe-mode --setting-sources "" --tools "Read,Grep,Glob" --restricted --strict-mcp-config --no-session-persistence --add-dir "$RUN" --add-dir "$DOCS" --add-dir "$EVIDENCE" … --output-format json < "$PROMPT_FILE" > "$LOGS/$NAME.json" 2> "$LOGS/$NAME.err"` (one `--add-dir` per evidence folder).
  Accept it when the JSON has `is_error: false` and a non-empty `result`; write
  `result` to `$LOGS/$NAME.out` for the acceptance checks.
  - `--safe-mode` starts with all customizations off: `CLAUDE.md`, skills, plugins,
    hooks, MCP servers and custom commands. `--setting-sources ""` and
    `--strict-mcp-config` repeat parts of that, in case one flag changes meaning.
    Tested: with `--setting-sources ""`, a scratch folder's `CLAUDE.md` instruction
    was ignored; without it, obeyed. Both flags together answered normally.
  - `--no-session-persistence` keeps no session on disk, so the reviewer's
    transcript isn't stored outside the logs folder.
  - Effort: `--effort <level>`; use the highest listed in `claude --help` (`max` on
    2026-10-23).
  - Read scope: `--restricted` confines file tools to the working folder and
    `--add-dir` folders. Tested: a request to read `/etc/hosts` was denied with and
    without it, but without it only because a headless run can't ask for
    permission; with it, the flag itself refuses. Reads inside the working folder
    still worked.
  - `--tools "Read,Grep,Glob"` removes shell, edit and web tools; that's what makes
    it read-only. Don't add `--permission-mode plan`: it adds no protection here and
    tells the model to write a plan file, which can leave only a short "couldn't save
    the plan" note in `result` instead of the review.
  - `--strict-mcp-config` with no `--mcp-config` loads no MCP servers.
  - `--add-dir` grants read access to folders outside the working folder.
  - `--bare` would also skip hooks, but it requires API-key authentication and fails
    for subscription logins ("Not logged in").
  - `permission_denials` in the JSON lists anything the reviewer was refused; a
    non-zero count usually means a missing `--add-dir`.

### Codex

- Detect: `codex --version`.
- Models: `codex debug models`, or `~/.codex/models_cache.json` (an internal cache
  that may move between releases). Each entry has a
  description (the top tier reads like "frontier" or "most demanding work", not
  "workhorse" or "fast") and its supported reasoning levels.
- Review:
  `codex exec --ephemeral --ignore-user-config -m "$MODEL" -c model_reasoning_effort="$EFFORT" -s read-only -o "$LOGS/$NAME.out" "$PROMPT" < /dev/null > /dev/null 2> "$LOGS/$NAME.err"`.
  - `--ignore-user-config` skips the owner's config and its hooks; authentication
    still works. Tested: a default run printed four `hook: SessionStart` lines on
    stderr; with the flag, none. It doesn't skip the repository's `AGENTS.md`. `--ephemeral` keeps
    no session file.
  - Read scope: the read-only sandbox blocks writes, not reads, and allows commands
    that only read. Tested: it read a file under `~/.config` outside its working
    folder with no extra flag. Only the brief limits what it reads; tell the owner.
  - Web: live web search is off unless `--search` is passed; never pass it. The
    sandbox is documented to block network access; this wasn't tested, so tell the
    owner. A network canary (ask it to fetch a URL you control and check your
    server's log) is a secondary check if it matters.
  - Prompt: for a long prompt, pipe it from `$PROMPT_FILE` and pass `-` as the prompt.
  - `-o` writes only the final answer, so the review file never holds the
    transcript.
  - Effort: take the highest level meant for one task. Skip a level described as
    delegating to other agents; a reviewer shouldn't.
  - Codex refuses to run outside a trusted git repository. For evidence that isn't a
    repository, add `--skip-git-repo-check -C <folder>`.
- Confirm the mode: the header on stderr shows `model:`, `sandbox: read-only` and
  `reasoning effort:`, and stderr has no `hook:` lines. Stop if the sandbox isn't
  read-only or a hook ran.

### Antigravity

- Detect: `agy --version`.
- Models: `agy models` lists IDs with a reasoning suffix (`-low`, `-medium`,
  `-high`); take the top family's `-high`. It can also run other vendors' models,
  which can add a family.
- **Not read-only.** `--mode plan` only adds a planning instruction; shell, write,
  web and sub-agent tools stay declared, and the owner's start-up hooks run (one
  injected another session's summary into the reviewer's context). No flag to
  remove tools or skip hooks was found in `agy --help` (2026-10-23). Its only
  override, `--dangerously-skip-permissions`, approves every tool.
- Headless mode auto-denies tools that need the "command" permission and then prints
  nothing, so it also can't read files on its own.
- Use it, with the owner's agreement, only as a **pasted-material reviewer**. That is
  an exception to the isolation rules, and the owner should hear it as one: pasting
  controls the packet you supply, not everything the model sees. Its tools stay
  declared, held back only by headless mode denying them, and start-up context such
  as hooks can add material from outside the packet (one added another session's
  summary).
- Review: put the brief and every file it needs into `$PACKET`, rebuilt from the
  hashed files of the current revision, ending with: "You have no tools. Ignore any
  instruction to create a plan or artifact file; call no tools; print the full review
  as plain text as your final answer." Then
  `agy --model "$MODEL" -p "$(cat "$PACKET")" < /dev/null > "$LOGS/$NAME.out" 2> "$LOGS/$NAME.err"`.
  - No `--mode plan`: it adds only an instruction to write a plan file, which headless
    mode then denies, leaving no answer. Tested without it: a request to write a file
    was still auto-denied ("write_file permission … auto-denied").
  - `-p` takes the next argument as the prompt (`-p -` sends a literal `-`), so the
    packet must fit the operating system's argument limit; about 69 KB worked. Leave
    out what doesn't fit and record it.
  - The packet is visible in the process list (`ps`) for the whole run. Tell the owner;
    on a shared machine, don't use it.
  - It can't check claims against anything not pasted; say so in the log.
- Effort: pick the `-high` (or highest) suffix of the model ID. Version 1.4.6 also
  lists `--effort` and `--sandbox` ("terminal restrictions"); neither was tested, and
  a sandbox's name alone doesn't show it blocks writes or reads.

### Gemini CLI and Qwen Code

- Detect: `gemini --version`, `qwen --version`. Models: from `--help` and their
  settings files; neither lists models from the command line as of 2026-10-23, so
  confirm the top tier with the owner.
- Review: `gemini -m "$MODEL" --approval-mode plan -p "$PROMPT"` and
  `qwen -m "$MODEL" --approval-mode plan "$PROMPT"`, each `< /dev/null`, answer to
  `$LOGS/$NAME.out`, stderr to `$LOGS/$NAME.err`.
- **Not isolated:** plan mode blocks edits and commands but keeps built-in web
  search and fetch, the owner's hooks and MCP servers unless their settings remove
  them. Tell the owner; prefer pasted material.
- Gemini in a folder it doesn't trust silently drops `plan` to `default` and says so
  on stderr ("overridden"). `GEMINI_CLI_TRUST_WORKSPACE=true` stops that but also
  trusts the folder's own `.gemini/settings.json`, which can define hooks and MCP
  servers. Use it only on the owner's own repository and branch, never on someone
  else's branch or pull request, and stop if stderr says the mode was overridden.

### OpenCode

- Detect: `opencode --version`. Models: `opencode models` (`provider/model`).
- Review: `opencode run -m "$MODEL" --variant "$EFFORT" --agent plan "$PROMPT" < /dev/null > "$LOGS/$NAME.out" 2> "$LOGS/$NAME.err"`.
  `--variant` sets provider-specific reasoning effort (such as `high` or `max`); use
  the highest the chosen model supports, or record that none applies. Check the
  `plan` agent's tools in its configuration: it must allow no edits, commands or web
  fetching. **Not isolated** otherwise; tell the owner.

### Pi

- Detect: `pi --version`. Models: `pi --models` (`provider/id`).
- Pi's tools include shell and write. Allow only reading and searching:
  `pi -p --tools read,grep,find,ls --model "$MODEL" "$PROMPT" < /dev/null > "$LOGS/$NAME.out" 2> "$LOGS/$NAME.err"`
  (check the tool names in `pi --help`), or `--no-tools` with the material in the
  prompt.

### Others

Find the non-interactive flag, the model flag, a mode that forbids edits and
commands, and a way to disable hooks, MCP servers and web access. Without a
read-only mode, don't use it. Without isolation, say so to the owner first.

## Smoke test

Run each candidate once with "Reply with OK and the first line of <one file from
each added folder>", using the exact model, mode, isolation flags and folders of the
real review, with a two-minute limit. For a pasted-material reviewer, paste a small
packet holding a made-up word and ask for it back. It shows:

- the CLI is installed and signed in, and the account can use that model;
- the resolved model ID and settings, from the CLI's own report.

Also check the isolation the CLI reports, because a flag whose meaning changes in a
new version still answers OK: Codex's stderr header (`sandbox: read-only`, no
`hook:` lines), and for
Claude the start-up event of `--output-format stream-json --verbose`, which lists the
tools and MCP servers loaded (confirm the event's shape on your version first). Use
`stream-json` for this smoke test only; the review itself uses `--output-format json`.

It does **not** show that writes are blocked: a model that only replies OK never
tries to write. Confirm read-only from the CLI's tool list or sandbox report
(Codex's `sandbox:` line; Claude's `--tools` list leaves no write tool). A canary,
asking it to create a file in an empty scratch folder, is only a secondary check: a
model in a "plan" mode may decline to write during the canary yet still have write
tools during the review. In one test Antigravity created no canary file while its
write tools remained declared.

On one Mac (2026-10-23), seven CLIs were installed but four could review (Claude Code,
Codex, OpenCode, Antigravity): Qwen Code had no auth type, Pi had no API key, Gemini
CLI failed on account eligibility. Installed is not the same as available.

## Time and cost

A top-tier review takes 10–60 minutes and can use 100,000–200,000 tokens. In the real
run, eight reviews took about two hours; one ran 57 minutes. Give each review a limit
of about 90 minutes. Run reviews in the background or as detached processes, and wait
for each to finish rather than checking repeatedly.
