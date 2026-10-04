# Markdown, READMEs, and docs

Read this when building or reviewing a README, a docs page, or any Markdown file. Sources are in the drawer's `research/docsmith.md`, section 5.

## Follow the repo first

The repo's own config is the design source for syntax: `.markdownlint*`, `.prettierrc*` (especially `proseWrap`), `.editorconfig`, `.vale.ini`. If a linter is configured, run it and fix what it reports. Match the conventions the other files already use. Only fall back to the defaults below when the repo says nothing.

Never reflow paragraphs you did not otherwise change. It hides the real edit in the diff.

## Syntax defaults

* Write CommonMark. Use GitHub extras (tables, task lists, alerts, Mermaid) only where the file is rendered on GitHub or a renderer that supports them.
* One H1, on the first line (or a front matter title). Its text matches or nearly matches the file name.
* Heading levels step by one. Headings are unique within the file (duplicates make ambiguous anchors). Use `#` style headings.
* One bullet marker per file. Blank lines around headings, lists, and code fences. No trailing spaces, no runs of blank lines.
* Every code fence names a language; use `text` or `console` when nothing fits. Fenced blocks, not indented ones.
* Every image has alt text that says what it shows.
* No bare URLs, and no "here" or "this link" as link text.
* Links inside the repo are relative, not absolute URLs to the hosting site. Every `#anchor` resolves to a real heading; after renaming a heading, find and fix links to it.
* Reference style links only where inline URLs hurt reading, such as in tables.
* Inline HTML only when Markdown cannot do it (for example `<details>`), and only what the renderer allows.
* Tables only for data that varies in two dimensions. If cells hold paragraphs or most are empty, use a list. Right align numeric columns with `---:`.
* GitHub alerts (`> [!NOTE]`, `> [!WARNING]`, and others) at most one or two per page, never back to back or nested.
* Diagrams as Mermaid or other text sources where they render, not exported images.
* Front matter only where a site generator reads it.

Line length is a team choice: hard wrap at 80, one sentence or clause per line, or no wrap. Follow the repo. Do not flag it otherwise.

## READMEs

Order:

1. Name, matching the repo or package.
2. One line on what it is, under about 120 characters, with no heading above it.
3. Optional: a few badges that a typical reader would actually use (build status, version). Flag walls of badges.
4. Install.
5. Usage, with a short example that runs as written after a clone, and its expected output where useful.
6. Links out to fuller docs, then contributing, then license last.

Also:

* Say why someone would use it and where to get help.
* If the project is no longer maintained, say so at the top.
* Add a contents list once it passes about 100 lines.
* Keep it short and link out. Move overflow into docs; never delete it.
* No broken links.

## One page, one job

Docs pages are one of four types. Keep them apart.

* Tutorial: a guided lesson for a beginner, with a result at the end.
* How-to guide: steps to reach a goal for someone who knows the basics. Step headings may be imperatives.
* Reference: dry, complete, structured like the thing it describes.
* Explanation: background, reasons, trade offs.

Flag a page that mixes them (a tutorial that turns into a reference table, a reference page full of opinion) and say how to split it. Do not create empty sections or folders for types nobody has written yet.

## Docs as code

* Docs change in the same commit as the code they describe.
* Delete docs that are wrong or dead; wrong docs are worse than none. Flag rather than delete if unsure.
* Suggest a linter (markdownlint), a link checker (such as lychee), and a prose linter (such as Vale) in CI if the repo has none. Do not add them unasked.

## Common fixes and flags

Fix: heading levels, missing code fence languages, missing alt text you can write from what the image shows, bare URLs, absolute links that should be relative, broken anchors, trailing spaces and extra blank lines, misaligned numeric table columns.

Flag: a README that does not say what the project is in its first lines, examples that do not run, a page mixing doc types, duplicate content that should link to one source, a broken external link.
