# Wikis and knowledge bases

Confluence, Notion, GitLab or GitHub wikis, a handbook, or a docs folder used as a knowledge base. Read this when building or reviewing wiki pages or a space. Markdown syntax rules are in `markdown.md`. Sources are in the drawer's `research/docsmith.md`, section 6.

## Each page

* Title in the words a reader would search for, not internal jargon or a project code name alone.
* The first lines say what the page is for, who it is for, and the key answer or status.
* Owner and last reviewed date shown near the top (or in the tool's verified page feature). Flag a page with neither.
* Stale signs to flag: a review date older than the space's policy (often three to six months), references to past dates as future plans, dead links, mentions of people or systems that no longer exist. Do not decide a page is wrong; flag it for the owner.
* Descriptive headings, so a reader can link straight to a section. A contents list once the page passes a screen.
* One page, one job (see the four doc types in `markdown.md`). Split catch all pages.

## Across pages

* One source of truth. If the same fact or process lives on two pages, name the one that should win and flag the other to become a short summary with a link.
* Link, do not copy. A short summary plus a link is fine.
* Landing pages or hubs for each area, linking to the pages under them. Flag orphan pages nothing links to.
* Labels or tags used consistently, so search and filtered lists work.
* Avoid catch all pages (a giant FAQ, a page that is only a list of links, a glossary nobody maintains). Put each answer where a reader would look for it.

## Templates

If the space has templates, recurring pages follow them. If not, these shapes work:

* How-to: goal, prerequisites, numbered steps, result, related pages.
* Troubleshooting: the problem as the reader sees it, cause, numbered fix for the common case, related pages.
* Decision record: title, status (proposed, accepted, superseded), context, decision, options considered, consequences, date and people. Number them and never reuse a number. Keep superseded records and link them to their replacement.
* Meeting notes: date, attendees, decisions, actions with owners and dates. Decisions that matter beyond the meeting move to a decision record or the page they change.

## Changing a wiki

* Propose a change as an edit to the page, not as a separate note about the page.
* When moving content, replace the old copy with a link, never leave two versions.
* Keep page history; do not delete pages others may link to. Archive or mark them superseded, with a link to what replaced them.

## Common fixes and flags

Fix: missing summary lines you can write from the page itself, broken internal links, heading structure, a page not following the space's template when the content clearly fits it.

Flag: no owner, stale review date, duplicated content (name the page that should win), orphan pages, a title nobody would search for, a page mixing doc types.
