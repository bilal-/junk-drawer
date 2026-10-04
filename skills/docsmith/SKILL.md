---
name: "docsmith"
description: "Review, improve, or build a slide deck, spreadsheet, formatted document, Markdown file (README, docs), or wiki page for structure, visual quality, layout, accessibility, and editability, including spreadsheet formulas, charts, and tables. Follows design instructions: a style or brand in the request, a DESIGN.md, design tokens, brand guide, or template in the project, then the file's own theme. Fixes small issues, flags big ones. Use on real files, or to build one to a brief. For the wording itself, use unslop."
---

# Docsmith

Review a real file and improve its structure, how it looks, how it is laid out, and how easy it is to read, reuse, and update. Or build a new file to a brief. Docsmith covers slide decks, spreadsheets, formatted documents (Word, Google Docs, PDF), Markdown (READMEs, docs), and wiki pages. Docsmith handles the file and its form. Unslop handles the words.

If the user only pastes plain text with no file and no format to build, there is nothing to format. Say so in one line and suggest unslop.

## Ground rules

* Work on a copy. Never overwrite the original. Save the result next to it with _polished added to the name. Exception: a text file under version control (Markdown, docs, a wiki kept in a repo) may be edited in place, since the history keeps the original. Say that you did.
* Use a pptx, docx, or xlsx skill or library if you have one to read and edit the file. For Markdown, edit the text directly. For a hosted wiki, work through its editor or API if you have access; otherwise return the revised page source and say where it goes.
* Look at the result. Render slides or pages to images (or a PDF), or preview Markdown as it will render, and view them before and after your changes.
* Keep all content and numbers exactly as they are. Never change a value to make something look better.
* Do not rewrite the writer's wording. If the text needs work, suggest unslop. Any text you add yourself (labels, alt text, notes, captions) uses simple words and no dashes.
* PDFs cannot be edited cleanly. For a PDF, review and flag only.
* Follow the design source (below). Never invent a brand.

## Review or build

* Review: the user gives a file. Run the design source lookup, the four checks, and the checks for its type. Fix or flag.
* Build: the user gives a brief and wants a new file. Find the design source first. Plan the structure before any styling: for a deck, write every slide title in order and check that they read as the argument; for a document, write the headings; for a workbook, list the input, calculation, and output sheets. Then build with real styles, layouts, and native charts, and finish by reviewing your own file with the same checks. Content you were not given is a placeholder, clearly marked, and listed in your summary. Never invent numbers.

## Design source

Find out what the file should look like before judging or changing it. Use the first source that covers a decision, in this order:

1. The request. A style, palette, font, template, or brand guide the user states or attaches.
2. A design file in the project. Look near the target file, then up to the project root, for `DESIGN.md`, a design tokens file (`*.tokens.json`, `*.tokens`), a brand or style guide, design sections in agent instruction files (`AGENTS.md`, `CLAUDE.md`, and similar), and templates (`.potx`, `.dotx`, `.xltx`, a reference deck). For Markdown, the repo's own lint and format config (`.markdownlint*`, `.prettierrc`, `.editorconfig`, `.vale.ini`) is the design source for syntax. The nearest file wins over one higher up.
3. The file's own theme: its master and layouts, styles, theme colours and fonts, cell styles, or, for Markdown and wikis, the conventions the other pages already follow.
4. Docsmith's defaults, only for what nothing above covers.

How to read and apply it:

* In a DESIGN.md, the tokens are the exact values, the prose covers what tokens do not, and the Do's and Don'ts are rules. It is written for screens: map its colours, type, and spacing onto the file and skip the rest. See `references/design-sources.md`.
* Apply a brand through the theme, not object by object (theme colours and fonts, master and layouts, styles, cell styles), then clear manual formatting so objects inherit it.
* If the request contradicts a project design file, say so in one line and follow the request.
* Reviewing an existing file: a few stray off brand colours or fonts are fixes. Restyling the whole file to a design source is a flag, unless the user asked for it.
* Say which design source you used in your summary. If you found none, say you used the file's own theme or the defaults.

Never override, whatever the design source says:

* Content, numbers, formulas, units, dates, names, quotations, and citations.
* Logos and marks: their artwork, colours, proportions, clear space, and minimum size. Third party marks follow their owner's rules. A brand file that describes another company is a style reference only; never use its marks.
* Legal text: copyright and trademark notices, disclaimers, confidentiality labels, required wording.
* Accessibility minimums: text contrast at least 4.5:1 (3:1 for large text, 18 pt or 14 pt bold), chart marks and meaningful graphics at least 3:1, colour never the only carrier of meaning, real headings, reading order, alt text, table header rows. If a brand colour fails, keep the hue and use a passing tint or shade, or the brand's dark or light neutral, and report the swap with both ratios. Never recolour a logo to fix contrast.
* Semantic structure: placeholders stay placeholders, styles keep their meaning (Heading stays Heading, Input stays Input).
* Artwork and photos keep their own colours.
* Locked or protected areas, tracked changes, and comments.

## Fix or flag

* Fix directly: small, safe changes that do not alter content. Examples: inconsistent font sizes, slightly misaligned objects, uneven spacing, inconsistent number formats, a hardcoded number that should point to a cell holding the same value, a missing alt text you can write from what the image plainly shows, a heading level that skips, a stray off theme colour, a missing language on a code fence.
* Flag: anything structural or anything that needs a decision. Examples: a full redesign or restyle, a slide order or storyline that needs rethinking, a calculation that needs reorganizing, a number with no traceable source, a chart whose title the data does not support, a page that mixes doc types, a wiki page with no owner.
* Never guess. If you are not sure what the author intended, flag it.

## Check 1: Aesthetics

Guiding question: if you could not read the language in this file, would its visual quality still look strong, judging by palette, styling, and other visual elements?

* Palette: a small set of colours from the design source, used consistently, with contrast that meets the minimums above, and colour that means the same thing everywhere.
* Type: one or two fonts, a clear size scale, consistent use of bold and italics. No underlining except links, no long runs of capitals.
* Visual elements: charts, images, and icons share one style. Nothing looks like a leftover default or a clutter of decoration. No 3D effects.
* Consistency: every page or slide feels like part of the same piece.

## Check 2: Layout

Guiding question: does the physical placement of objects make the file easy to follow for someone with limited context?

* Spacing: even margins and gaps, room to breathe, nothing crammed.
* Alignment: objects line up on a shared grid. Nothing overlaps or runs off the page.
* Hierarchy: the main point is the first thing the eye lands on, then the support.
* Grouping: related items sit together, labels sit next to what they label, unrelated items are clearly apart.
* Reading order: the eye moves through the page in the order the ideas build, and the file's reading order (for screen readers) matches.

## Check 3: Editability

Guiding question: if the underlying data changed overnight, how easy would it be to update and reuse this file?

* Decks: charts and tables are native and editable, not pasted pictures. Text sits in the layout's placeholders. Slides use layouts and shared styles. A number that appears in several places is easy to change in all of them.
* Documents: headings, lists, captions, and tables use real styles, not manual formatting. Spacing comes from styles, not blank lines, tabs, or spaces. The contents list and cross references are generated, not typed.
* Markdown and wikis: one source of truth; link to a fact rather than copy it. Diagrams kept as text (such as Mermaid) where the renderer supports it.
* All files: remove leftovers nobody needs, such as objects parked off the page, empty slides, and stray blank pages. Do not delete hidden sheets or layouts in a branded template; unhide or keep them and flag. If something might be intended, keep it and flag it.

## Check 4: Spreadsheet formulas (spreadsheets only)

Guiding question: could someone open this workbook and audit exactly how each number was calculated? A strong workbook has formulas that fit their purpose, are easy to read, and are easy to tweak.

* No hardcoded numbers where a formula belongs, such as totals, percentages, or anything derived. Fixed constants like 12 months or 1000 are fine.
* Inputs and assumptions sit in labeled cells, not buried inside formulas, and look different from formulas under one colour key used across the workbook.
* The same formula pattern runs down a column or across a row. Flag any cell that breaks the pattern.
* Formulas are simple enough to read. Split long nested formulas into steps.
* References are clear, point to the source and not to another link, and use absolute references where they should.
* Headers have labels and units.
* A short notes or cover area explains the purpose, the key calculations, and the assumptions.
* No errors, broken references, or circular references. Totals tie out, ideally through a checks area.

Fix directly: replace a hardcoded number with a reference or formula that gives the same value, repair an inconsistent formula in a column, label an input, add a missing unit, make number formats consistent.

Flag: calculation logic that needs reorganizing, a sheet that needs rebuilding, a number that cannot be traced to a source, or a formula that looks wrong when the intent is unclear.

## Checks by file type

Run the short list for the file's type. Read the matching reference file (in `references/` beside this file) when you build that type, when the file is long or high stakes, or when a check below needs more detail. Read `references/charts-and-tables.md` whenever the file has a chart or a data table, and `references/design-sources.md` when a design source is unclear or conflicts with another.

### Slides (`references/slides.md`)

* Decide first: presented (someone speaks over it) or read (sent to be read alone). Presented slides carry one idea and little text, with detail in the speaker notes. Read decks may be dense but still one idea per slide, in full sentences.
* Read only the titles in order. They should tell the argument and reach the conclusion. Flag topic titles ("Market overview") where a statement of the point belongs; the wording goes to unslop.
* Every slide has a unique title (it may sit off the slide if hidden), and the body supports that title.
* Projected body text at least 24 pt. Alt text on meaningful images, decorative ones marked decorative. Reading order set.

### Documents (`references/documents.md`)

* The main point or request comes first: in the first paragraph, or in an executive summary that stands alone.
* Headings are real heading styles, informative, with no skipped levels and one title. At most three levels in most documents.
* Body 10 to 12 pt in print, line spacing about 120 to 145 percent, lines about 45 to 90 characters.
* Tables have a marked header row that repeats across pages and no merged cells. Images have alt text. Document title and language are set. A PDF export is tagged.

### Spreadsheets (`references/spreadsheets.md`)

* Inputs, calculations, and outputs are separated, with a cover sheet that says what the workbook is for and explains the colour key.
* Nothing is hidden without a reason. No merged cells in data. Sheet names mean something.
* Freeze panes on headers. Numbers right aligned with consistent decimals and one style for negatives.
* Raw data tables are one rectangle with one header row, one value per cell, ISO dates, and no colour used as data.

### Markdown and READMEs (`references/markdown.md`)

* Follow the repo's lint and format config. Otherwise: one H1 on the first line, heading levels step by one, unique headings, a language on every code fence, alt text on every image, no bare URLs, relative links inside the repo.
* A README opens with the name and one line on what it is, then install and usage, then links out for depth. Code in it runs as written.
* One page, one job: a tutorial, a how-to guide, reference, or explanation. Flag a page that mixes them.
* Never reflow untouched paragraphs; it buries the real change in the diff.

### Wikis and knowledge bases (`references/wikis.md`)

* The title uses the words a reader would search for. The first lines say what the page is for and who it is for.
* The page shows an owner and a last reviewed date. Flag pages with neither, or that look stale.
* Link to the single source of truth instead of copying it. Flag duplicates and name the page that should win.
* Recurring page types (how-to, troubleshooting, decision, meeting notes) follow the space's template if it has one.

## Delivering

Send the polished or new file. Then give a short summary: which design source you used, what you fixed (a few plain lines), and what you flagged (one line each, with where it is and what is needed). In build mode, also list every placeholder. Do not recap every step.
