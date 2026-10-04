---
name: "docsmith"
description: "Review and improve a deck, spreadsheet, or formatted document for visual quality, layout, and editability, including spreadsheet formulas. Fixes small issues, flags big ones. Use on real files."
---

# Docsmith

Review a real file (slide deck, spreadsheet, or formatted document) and improve how it looks, how it is laid out, and how easy it is to update. Docsmith handles the file. Unslop handles the words.

If the user only pastes plain text, there is nothing to format. Say so in one line and suggest unslop.

## Ground rules

* Work on a copy. Never overwrite the original. Save the result next to it with _polished added to the name.
* Use the matching file skill (pptx, docx, or xlsx) to read and edit the file.
* Look at the result. Render slides or pages to images (or a PDF) and view them before and after your changes.
* Keep all content and numbers exactly as they are. Never change a value to make something look better.
* Do not rewrite the writer's wording. If the text needs work, suggest unslop. Any text you add yourself (labels, notes) uses simple words and no dashes.
* PDFs cannot be edited cleanly. For a PDF, review and flag only.

## Fix or flag

* Fix directly: small, safe changes that do not alter content. Examples: inconsistent font sizes, slightly misaligned objects, uneven spacing, inconsistent number formats, a hardcoded number that should point to a cell.
* Flag: anything structural or anything that needs a decision. Examples: a full redesign, a slide order that needs rethinking, a calculation that needs reorganizing, a number with no traceable source.
* Never guess. If you are not sure what the author intended, flag it.

## Check 1: Aesthetics

Guiding question: if you could not read the language in this file, would its visual quality still look strong, judging by palette, styling, and other visual elements?

* Palette: a small set of colors used consistently, enough contrast to read, and color that means the same thing everywhere.
* Type: one or two fonts, a clear size scale, consistent use of bold and italics.
* Visual elements: charts, images, and icons share one style. Nothing looks like a leftover default or a clutter of decoration.
* Consistency: every page or slide feels like part of the same piece.

## Check 2: Layout

Guiding question: does the physical placement of objects make the file easy to follow for someone with limited context?

* Spacing: even margins and gaps, room to breathe, nothing crammed.
* Alignment: objects line up on a shared grid. Nothing overlaps or runs off the page.
* Hierarchy: the main point is the first thing the eye lands on, then the support.
* Grouping: related items sit together, unrelated items are clearly apart.
* Reading order: the eye moves through the page in the order the ideas build.

## Check 3: Editability

Guiding question: if the underlying data changed overnight, how easy would it be to update and reuse this file?

* Decks: charts and tables are native and editable, not pasted pictures. Text sits in real text boxes. Slides use layouts and shared styles. A number that appears in several places is easy to change in all of them.
* Documents: headings, lists, and tables use real styles, not manual formatting. Spacing comes from styles, not blank lines.
* All files: remove leftovers nobody needs, such as hidden sheets, objects parked off the page, empty slides, and unused layouts. If something might be intended, keep it and flag it.

## Check 4: Spreadsheet formulas (spreadsheets only)

Guiding question: could someone open this workbook and audit exactly how each number was calculated? A strong workbook has formulas that fit their purpose, are easy to read, and are easy to tweak.

* No hardcoded numbers where a formula belongs, such as totals, percentages, or anything derived.
* Inputs and assumptions sit in labeled cells, not buried inside formulas.
* The same formula pattern runs down a column or across a row. Flag any cell that breaks the pattern.
* Formulas are simple enough to read. Split long nested formulas into steps.
* References are clear and use absolute references where they should.
* Headers have labels and units.
* A short notes area explains the key calculations and assumptions.
* No errors, broken references, or circular references. Totals tie out.

Fix directly: replace a hardcoded number with a reference or formula, repair an inconsistent formula in a column, label an input, add a missing unit, make number formats consistent.

Flag: calculation logic that needs reorganizing, a sheet that needs rebuilding, a number that cannot be traced to a source, or a formula that looks wrong when the intent is unclear.

## Delivering

Send the polished file. Then give a short summary: what you fixed (a few plain lines) and what you flagged (one line each, with where it is and what is needed). Do not recap every step.