# Docsmith research

Notes and sources behind docsmith's rules. Gathered 2026-10-04 by web search and page fetches. Grouped by file type and theme. Each finding has a source and an evidence note.

Evidence key:

* **Std**: a standard, specification, regulation, or vendor rule (WCAG, ISO, ECMA, FAST, ICAEW, CommonMark, Microsoft checker).
* **Emp**: a controlled or field study.
* **Prac**: widely adopted practitioner guidance (consulting practice, Datawrapper, Google style guides, Write the Docs).
* **Op**: one author's view or an untested rule of thumb.

Most numeric thresholds in this field (3 seconds, 24 pt, 6x6, 250 words, 45 to 90 characters) are practitioner numbers that nobody has tested. The skill treats them as review triggers, not laws.

## 1. Verdict on the current skill

### Supported

| Current rule | Support |
| --- | --- |
| Look at the rendered result before and after | Kosslyn et al. 2012 found viewers often cannot spot broken design principles, so check against a list on the real render (Emp). PowerPoint's checker does not test text against the slide background, so contrast must be checked by eye or by computing it (Std). |
| Keep content and numbers exactly | Every standard below; integrity is the floor (Std). |
| A small palette used consistently, colour that means one thing | Few, "Practical Rules for Using Color in Charts" (Prac); Datawrapper on fewer colours (Prac). |
| One or two fonts, a clear size scale | Butterick, "Mixing fonts": few documents tolerate a third font (Prac). |
| Hierarchy, grouping, reading order | Mayer's signalling principle, 24 of 28 tests (Emp); spatial contiguity, 22 of 22 (Emp). |
| Native, editable charts and real text boxes; slides use layouts | Microsoft: text outside placeholders is missing from Outline View and read in creation order (Std). |
| Documents use real styles, spacing from styles not blank lines | Microsoft and WebAIM Word guidance; state accessibility checklists map this to WCAG 1.3.1 (Std). |
| No hardcoded numbers where a formula belongs; inputs in labelled cells | FAST 3.04-01, ICAEW Twenty Principles #14, ICAEW Code "Avoid hardcoding" (Std). |
| The same formula pattern across a row or column | FAST 3.02-01 calls it "one of only a few universally accepted principles" (Std). |
| Split long formulas | FAST 3.03-01 "longer than your thumb"; Panko: logic errors in long formulas are found far less often in review (Std, Emp). |
| Labels and units on headers | FAST 3.05, ICAEW Code "Use clear units" (Std). |
| A notes area | ICAEW Twenty #7 and #17, FAST 2.05 and 2.06: a cover or About sheet (Std). |
| No errors or circular references, totals tie out | ICAEW Code "Avoid circular references", "Include checks" (Std). |
| Fix small, flag big; never guess | Consistent with every review standard found; Panko shows reviewers are overconfident, so flag when unsure (Emp). |

### Needs a refinement

* "Remove unused layouts": unsafe in a branded template. Layouts belong to the master and the brand (Microsoft template docs, Std). Keep layouts in a corporate template; only remove those that are clearly leftovers in a one-off deck, and flag otherwise.
* "Remove hidden sheets": FAST 2.01-08 and the ICAEW Code say nothing should be hidden, but a hidden sheet may feed formulas. Check for references first; unhide and flag rather than delete. Hidden content is a real risk (the 2022 UK Ministry of Defence Afghan data breach came from hidden data in a spreadsheet; widely reported).
* "No hardcoded numbers": allow universal constants (12 months, 24 hours, 1000) as FAST and ICAEW both do.
* "Enough contrast to read": make it a number. WCAG 2.2: 4.5:1 for text, 3:1 for large text and for chart marks (Std).
* "Absolute references where they should be": practitioner advice only; keep but it carries less weight than row consistency.
* Colour coding of inputs: the current skill says nothing, but standards disagree on colours (see 4.3), so the rule must be "one key, used consistently", not a palette.

### Contradicted

Nothing in the current skill is contradicted outright. Two implicit assumptions are risky:

* A single idea of "good slide" (sparse) would be wrong for read decks. Duarte's Slidedocs and consulting practice allow dense decks meant to be read (Prac). The skill must first decide whether a deck is presented or read.
* Treating any truncated axis or any pie chart as a defect would be wrong. Correll et al. 2020 and Skau and Kosara 2016 (Emp) show both are conditional.

### Missing

* Design source: no way to receive a style, brand, DESIGN.md, tokens, or template.
* Build mode: the skill only reviews.
* Markdown, READMEs, and wikis: not covered.
* Accessibility: alt text, reading order, slide titles, table headers, colour alone, tagged PDFs.
* Deck structure: title read-through, assertion titles, presented vs read decks.
* Document structure: main point first, informative headings, heading levels.
* Charts and tables: chart choice, baselines, finding titles, direct labels, table alignment.
* Spreadsheet: checks sheet and master check, cover sheet, colour key, one timeline, tidy raw data, merged cells, error-prone cases (range ends, date auto-conversion, row limits).

## 2. Slides

### Argument

1. Read only the titles in order; they should tell the whole argument and end at the recommendation. Topic titles ("Market overview") fail. Minto, The Pyramid Principle, as used in consulting: Deckary, https://deckary.com/blog/pyramid-principle-consulting ; StrategyPunk, https://www.strategypunk.com/the-minto-pyramid-principle-how-to-communicate-like-a-mckinsey-consultant-pdf/ . Prac.
2. Vertical logic: the body proves the title, the title sums up the body. If the chart does not support the title, fix the title, never the chart. Same sources. Prac.
3. Horizontal logic: sibling slides make one kind of point in a stated order, no overlaps and no gaps (MECE). Same sources. Prac.
4. Ghost deck: write every title and sketch every exhibit before building. Working With McKinsey, http://workingwithmckinsey.blogspot.com/2013/07/McKinsey-presentations-ghost-decks.html . Prac. Useful for build mode.
5. Lead with the answer (situation, complication, resolution). Minto via Deckary. Prac.

### One slide

6. Assertion-evidence: a full sentence claim as the headline (at most two lines, sentence case), visual evidence below, not bullets. Alley, https://www.assertion-evidence.com/ . Prac; format details are Alley's own (Op).
7. Garner and Alley 2013, 110 engineering students: assertion-evidence slides gave better comprehension, fewer misconceptions, better recall, lower cognitive load. "How the Design of Presentation Slides Affects Audience Comprehension", Int. J. Eng. Educ. 29(6), https://writing.engr.psu.edu/ae_comprehension.pdf . Emp, one group, one topic. Alley et al. 2006 found sentence headlines improved retention (https://www.assertion-evidence.com/references.html). Emp.
8. Glance test: the point should land in about three seconds. Duarte, https://www.duarte.com/resources/guides-tools/the-glance-test/ . Prac; the number is untested.
9. One idea per slide; remove anything whose removal does not change the meaning (repeated logos, 3D, decoration). Reynolds, Presentation Zen, https://www.garrreynolds.com/design-tips . Prac.
10. Coherence: cut interesting but unneeded material (23 of 23 tests, median d = 0.86). Mayer and Fiorella 2014, Cambridge Handbook of Multimedia Learning ch. 12, https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/CD5B7AE1279A9AB81F8EEBB53DBEC86E . Emp, strong.
11. Signalling: make structure visible and point at the key element (24 of 28, d = 0.41). Same chapter. Emp, moderate.
12. Redundancy: do not put the narrated words on screen as well (16 of 16, d = 0.86). Same chapter; Mayer 2017, https://onlinelibrary.wiley.com/doi/abs/10.1111/jcal.12197 . Emp.
13. Spatial contiguity: labels on or next to what they describe (22 of 22, d = 1.10). Same chapter. Emp. Caveat for 10 to 13: lab effects shrink and sometimes reverse in real classrooms (arXiv 2409.09145, https://arxiv.org/pdf/2409.09145). Emp.
14. Kosslyn et al. 2012: eight perceptual principles routinely broken in real decks, often invisible to viewers. Frontiers in Psychology, https://doi.org/10.3389/fpsyg.2012.00230 . Emp. Supports checking against an explicit list.

### Density and size

15. The 6x6 rule has no traceable origin and leans on a misreading of Miller's "7 plus or minus 2". Tufte, https://www.edwardtufte.com/notebook/the-magical-number-seven-plus-or-minus-two-not-relevant-for-design/ ; Forbes, https://www.forbes.com/sites/propointgraphics/2017/07/05/debunking-the-presentation-6x6-rule/ . Prac. Do not enforce it; instead flag bullet lists on presented slides where a claim plus a visual would do.
16. Projected type: body at least 24 pt, titles about 32 to 44 pt; Kawasaki's 30 pt is stricter. ARL, https://www.arl.org/accessibility-guidelines-for-powerpoint-presentations/ ; Six Minutes, https://sixminutes.dlugan.com/10-20-30-rule-guy-kawasaki-powerpoint/ . Prac; no slide study exists.
17. Read decks (Slidedocs) are a legitimate format: up to about 250 words, one concept per page, real sentences. Duarte, https://www.duarte.com/resources/guides-tools/slidedocs-ebook/ . Op.

### Disagreement: presented vs read

Reynolds and Duarte (slide:ology) want sparse projected slides. Tufte, "The Cognitive Style of PowerPoint" (https://www.edwardtufte.com/notebook/new-edition-of-the-cognitive-style-of-powerpoint/), rejects slides for serious analysis and wants dense printed handouts; Amazon's narrative memos take the same side. Consulting firms send dense read decks with action titles. Reconcile by medium: presented decks follow 6 to 16; read decks follow 1 to 5 and 17 and may be dense. Every slide still gets a title (accessibility), and full sentence titles help in both.

### Charts on slides

18. Write the message first, then choose the comparison: part of a whole, ranking, time series, distribution, correlation. Zelazny, Say It with Charts, https://www.informit.com/articles/article.aspx?p=170392&seqNum=30 . Prac.
19. Declutter, then highlight one series; context in grey; label directly. Knaflic, Storytelling with Data. Prac.

### Notes, masters, accessibility

20. Detail goes in speaker notes or a handout, not on a projected slide. Reynolds. Op/Prac.
21. Build from layouts and placeholders. Text outside placeholders is missing from Outline View and read in creation order. Microsoft, https://support.microsoft.com/en-us/powerpoint/add-edit-or-remove-a-placeholder-on-a-slide-layout . Std.
22. Every slide has a unique title (it may be placed off slide if hidden); alt text on meaningful visuals; decorative ones marked decorative; reading order set; tables have header rows; video captioned. Microsoft, "Make your PowerPoint presentations accessible", https://support.microsoft.com/en-us/office/make-your-powerpoint-presentations-accessible-to-people-with-disabilities-6f7772b2-2f33-4bd2-8ca7-dae3b2b3ef25 ; "Rules for the Accessibility Checker", https://support.microsoft.com/en-us/office/rules-for-the-accessibility-checker-651e08f2-0fc3-4e10-aaca-74b4a67101c1 . Std.
23. The checker does not test text against the slide background; compute contrast yourself. Same Microsoft rules page. Std.

## 3. Documents (reports, memos, proposals)

### Structure

1. Main point first (BLUF). Army Regulation 25-50, para 1-36b, names it one of two essential requirements. https://corpslakes.erdc.dren.mil/employees/pdfs/AR25-50.pdf (mirror). Std.
2. Subject line states purpose and the action needed. Sehgal, "How to Write Email with Military Precision", HBR 2016, https://hbr.org/2016/11/how-to-write-email-with-military-precision . Prac.
3. Decision documents in full sentences, not bullets. Bezos 2017 shareholder letter on six page narratives read in silence, https://www.aboutamazon.com/news/company-news/2017-letter-to-shareholders ; the 2004 "no PowerPoint" email is second hand (https://slab.com/blog/jeff-bezos-writing-management-strategy/). Prac.
4. Pyramid order: one governing thought, grouped support. Barbara Minto, https://www.barbaraminto.com/ . Prac.
5. Executive summary stands alone, leads with the recommendation, about 5 to 15 percent of length. Walton College, https://walton.uark.edu/business-communication-lab/resources/downloads/business-forms/Executive_Summary.pdf . Prac.
6. Many informative headings; questions, then statements, then topics. Federal Plain Language Guidelines 2011, https://wid.org/wp-content/uploads/2022/03/FederalPLGuidelines.pdf (plainlanguage.gov now redirects to https://digital.gov/guides/plain-language). Std/Prac.
7. Front load headings; descriptive, sentence case, no block capitals. GOV.UK, https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/ . Prac. Disagreement: GOV.UK says headings should not be questions; the Federal guidelines rank them best. Rule: question headings for FAQ or reference where the reader's questions are known, statements elsewhere.

### Typography

8. Body 10 to 12 pt in print, 15 to 25 px on screen. Butterick, https://practicaltypography.com/typography-in-ten-minutes.html . Prac.
9. Line spacing 120 to 145 percent. Same. Prac. WCAG 1.4.12 is a robustness test (content survives 1.5 line height set by the user), not an authoring minimum.
10. Line length 45 to 90 characters (Butterick, https://practicaltypography.com/line-length.html); 45 to 75, 66 ideal (Bringhurst via https://webtypography.net/2.1.2). Prac.
11. Line length research is mixed: Dyson and Haselgrove 2001 found 55 characters best for comprehension; other screen studies found long lines read faster. https://stu.westga.edu/~ssynan1/literacy/Dyson.pdf . Emp, mixed. Rule: flag only outside about 40 to 100.
12. Margins usually 1.5 to 2 inches at 12 pt; one inch margins at 12 pt usually mean lines are too long. https://practicaltypography.com/page-margins.html . Prac.
13. One font, two at most. https://practicaltypography.com/mixing-fonts.html . Prac.
14. Mechanics to flag: double spaces, underlining that is not a link, all caps longer than a line, bold plus italic, straight quotes, double hyphens as dashes, first line indents together with paragraph space. https://practicaltypography.com/summary-of-key-rules.html . Prac.
15. Hierarchy with the fewest cues; at most three heading levels; space first, then size, then bold; keep with next. https://practicaltypography.com/headings.html . Prac.
16. Font choice is contested: Butterick dislikes Arial and Times; Microsoft's accessibility guidance recommends Arial or Calibri. Rule: do not flag a font as wrong; flag only display, novelty, or monospaced faces in body text.

### Headings, navigation, styles

17. Real heading styles in order, one title, no skipped levels. WebAIM, https://webaim.org/techniques/word/ ; WCAG 1.3.1, 2.4.6. Std.
18. Long reports: numbered headings (1, 1.1, 1.1.1) applied through styles. https://practicaltypography.com/hierarchical-headings.html . Prac.
19. Generated table of contents; page numbers; no essential content only in headers or footers. Microsoft, https://support.microsoft.com/en-us/office/add-a-heading-in-a-word-document-3eb8b917-56dc-4a17-891a-a026b2c790f2 . Std.
20. Format through styles; flag bold Normal text posing as headings. Microsoft, "Make your Word documents accessible", https://support.microsoft.com/en-us/office/make-your-word-documents-accessible-to-people-with-disabilities-d9bf3683-87ac-47ea-b91a-78dcacb3c66d . Std.
21. No blank paragraphs for spacing, no tabs or spaces for alignment. Illinois DoIT, https://doit.illinois.gov/initiatives/accessibility/guides/word.html . Std derived.
22. Real list styles. WebAIM. Std derived.
23. Table header row marked and repeated across pages. Microsoft, https://support.microsoft.com/en-us/word/repeat-table-header-on-subsequent-pages . Std.
24. Captions through the caption feature; cross references as fields, never typed numbers. Microsoft Q&A, https://learn.microsoft.com/en-us/answers/questions/5343052/how-to-insert-a-cross-reference-to-a-figure-captio . Prac.

### Accessibility

25. Text contrast 4.5:1, large text 3:1 (18 pt, or 14 pt bold). Logos exempt; brand colours are not. WCAG 2.2 SC 1.4.3, https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html . Std.
26. Meaningful graphics 3:1 against neighbours. SC 1.4.11, https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html . Std.
27. Colour never the only carrier of meaning (SC 1.4.1). Checkers cannot detect this; a reviewer must. Std.
28. Alt text: meaning for informative images, action for functional ones, data or table for complex charts, empty or decorative flag for decoration; no "image of", no file names. W3C alt decision tree, https://www.w3.org/WAI/tutorials/images/decision-tree/ . Std.
29. Data tables are simple rectangles with a header row; no merged or split cells. Microsoft checker rules page. Std.
30. Link text says where it goes (2.4.4); document language set (3.1.1); images inline so reading order holds (1.3.2). Std.
31. PDFs tagged, titled, title displayed. W3C PDF18, https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF18 ; PDF/UA-1 (ISO 14289-1:2014) and PDF/UA-2 (ISO 14289-2:2024), https://pdfa.org/announcing-no-cost-access-to-pdfs-accessibility-standards/ . Std.
32. Legal floor: Section 508 pins WCAG 2.0 AA (https://www.access-board.gov/ict/); the European Accessibility Act applies from 28 June 2025 via EN 301 549 (WCAG 2.1 AA) (https://universaldesign.ie/communications-digital/european-accessibility-act). Building to WCAG 2.2 AA meets both. Std.

## 4. Spreadsheets

### Structure

1. Separate inputs, calculations, and outputs; a dashboard that takes inputs and shows results is the allowed exception. ICAEW Twenty Principles #10 (2018, mirror http://a1financialmodelling.co.uk/Images/Twenty.pdf); ICAEW Financial Modelling Code, https://www.icaew.com/-/media/corporate/files/technical/technology/excel/financial-modelling-code.ashx ; FAST Standard 02c, 1.01-01, https://fast-standard.org/wp-content/uploads/2019/10/FAST-Standard-02c-July-2019.pdf . Std.
2. Each input once, each calculation once; everything else links to it. FAST 1.01-07; ICAEW #15. Std.
3. Flow top to bottom, left to right; sheets in the same order. FAST 1.02-01, 2.01-04. Std.
4. Consistent columns on every sheet: label, constants, units, first period in the same place. FAST 2.01-01; Grossman and Ozluk 2010, https://arxiv.org/pdf/1008.4174 . Std.
5. One timeline from one start date input. FAST 1.01-03, 2.01-02. Std.
6. Avoid links between workbooks; if needed, pass through import and export sheets. FAST 1.03. Std.
7. A cover or About sheet: purpose, contents, colour key, version log, limitations. ICAEW #7, #17; FAST 2.05, 2.06. Std.

### Formulas

8. One formula per row, consistent across the row. FAST 3.02-01. Std.
9. Short formulas: "longer than your thumb" or more than 24 seconds to explain means split it; avoid nested IFs, OFFSET, INDIRECT. FAST 3.03-01, 3.03-02, 3.03-07, 4.01-03; SMART, https://spreadsheetstandards.wordpress.com/2013/02/12/smart-financial-modelling-corality/ . Std; exact thresholds Op.
10. No changeable numbers inside formulas; universal constants allowed. FAST 3.04-01; ICAEW #14. Std.
11. Never type a value over a formula in a calculated row. FAST 3.01-01. Std.
12. No circular references; round only for display. ICAEW Code. Std.
13. No links to links (daisy chains); no partial range references. FAST 3.06-02, 3.02-03. Std.

### Labels and signs

14. Unique row labels with units ("Revenue ($000)"). FAST 3.05; ICAEW Code. Std.
15. One stated sign convention. FAST wants positive on workings with direction in the label; ICAEW accepts any labelled convention. Std, disagreement on which.
16. Meaningful sheet names; "Sheet1" is a finding. ICAEW Code. Std.

### Colour and formatting

17. Inputs look different from formulas, under one key for the whole workbook. Banking: blue font inputs, black formulas, green links to other sheets (https://www.fe.training/free-resources/financial-modeling/financial-model-formatting-numbers/ , Prac). ICAEW: a fill or border, not font colour alone (Std). FAST 1.01-06 uses red and blue for exports and imports (Std). BPM: distinct styles are a standard, the colour is a convention. Rule: check the workbook follows its own key; do not impose a palette.
18. Cell styles rather than one off formatting (FAST 4.02-01). Excel's built in Input, Calculation, Output, Check Cell, and Linked Cell styles exist for this (ECMA-376 cellStyle builtinId 20 to 24, https://webapp.docx4java.org/OnlineDemo/ecma376/SpreadsheetML/cellStyle.html ). Std.
19. No merged cells; use Center Across Selection. FAST 4.02-02. Std/Prac.
20. Number formats: right aligned, same decimals in a column, thousands separators, one negative style, no false precision. ICAEW Code "Use clear formatting"; Few via https://www.csescienceeditor.org/article/best-practices-in-table-design/ . Std/Prac.
21. Freeze panes so labels and timeline stay visible; show the master check in the frozen area. ICAEW Code; FAST 2.03. Std.
22. Print setup only on input and presentation sheets. FAST 1.02-02. Std/Prac.

### Hiding and names

23. Nothing hidden: rows, columns, sheets, white text, formats that show nothing. Hiding unused columns past the timeline is allowed. ICAEW allows grouping; FAST mostly does not. FAST 2.01-08; ICAEW Code "Don't hide things". Std. The 2022 UK Ministry of Defence breach of about 18,700 Afghan applicants' data came from hidden spreadsheet content (widely reported).
24. Named ranges: FAST says do not use them (3.03-08); ICAEW is neutral; BPM and Operis favour them with naming rules. Rule: do not flag names as such; flag vague, broken, or misleading ones. Std, disagreement.

### Checks and review

25. A checks sheet with tolerances, rolled into one master check shown on every sheet. ICAEW Code "Include checks" and "Include a master check"; ICAEW #19; FAST 2.03-05. Std.
26. Errors are near certain: 88 percent of 113 audited spreadsheets had at least one error; cell error rates about 1 to 5 percent. Panko, "What We Know About Spreadsheet Errors", https://www.researchgate.net/publication/228662532_What_We_Know_About_Spreadsheet_Errors . Emp.
27. Builders are overconfident; inspection is the method shown to work. Panko 2000, https://arxiv.org/abs/0802.3457 ; Panko 2015, https://arxiv.org/abs/1602.02601 . Emp.
28. Teams of three found 83 percent of seeded errors against 63 percent for individuals; logic errors and omissions were found far less often. Panko 1999, JMIS 16(2). Emp.
29. Documented failures to check for: wrong range ends (Reinhart and Rogoff, Herndon, Ash and Pollin 2014, https://blog.oup.com/2014/01/public-debt-gdp-growth-austerity-why-reinhart-and-rogoff-are-wrong/); dividing by a sum instead of an average (JPMorgan London Whale, https://www.accountingweb.co.uk/tech/excel/excel-errors-jp-morgans-whale-sized-classic); gene names converted to dates (Ziemann et al. 2016, https://doi.org/10.1186/s13059-016-1044-7 ; Abeysooriya et al. 2021, https://doi.org/10.1371/journal.pcbi.1008984); the .xls row limit losing 15,841 COVID cases (https://www.theregister.com/2020/10/05/excel_england_coronavirus_contact_error/). Catalogue: EuSpRIG Horror Stories, https://eusprig.org/research-info/horror-stories/ . Emp (case reports).

### Data tables

30. Raw data is one rectangle: one header row, one variable per column, one observation per row, one thing per cell; ISO dates; no colour as data; no calculations in raw data; a data dictionary; validation. Wickham, "Tidy Data", JSS 59(10) 2014, https://doi.org/10.18637/jss.v059.i10 ; Broman and Woo, "Data Organization in Spreadsheets", The American Statistician 72(1) 2018, https://doi.org/10.1080/00031305.2017.1375989 . Prac, peer reviewed. Disagreement: Broman fills every cell with one missing value code; White et al. 2013 prefer blanks. Rule: flag mixed codes and "same as above" blanks.

## 5. Markdown and READMEs

### Syntax and lint

1. Write CommonMark; use GFM extensions only where GitHub renders the file. CommonMark 0.31.2, https://spec.commonmark.org/ ; GFM, https://github.github.com/gfm/ . Std.
2. GitHub alerts (`> [!NOTE]` and others) sparingly, one or two per page, never stacked or nested; other renderers show a plain blockquote. GitHub Docs, https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax . Std (vendor).
3. markdownlint rules worth enforcing: MD001 heading levels step by one; MD003 and MD004 one heading and bullet style; MD009 and MD012 no trailing spaces, no double blanks; MD022, MD031, MD032 blank lines around headings, fences, lists; MD024 unique headings; MD025 and MD041 one H1 on the first line; MD033 inline HTML only from an allow list; MD034 no bare URLs; MD040 every fence has a language; MD045 images have alt text; MD051 anchors resolve. https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md . Std (tool).
4. Google Markdown style: ATX headings, H1 matches the file name, unique descriptive headings, no "here" link text, declare the code language, tables only for uniform two dimensional data. https://google.github.io/styleguide/docguide/style.html . Prac.
5. Line wrapping is disputed: Google hard wraps at 80; semantic line breaks put one clause per line (https://sembr.org/); many repos turn MD013 off; Prettier's proseWrap offers always, never, preserve (https://prettier.io/docs/options). Rule: follow the repo's configuration and never reflow untouched paragraphs. Op/Prac.
6. Relative links inside a repo; absolute blob URLs break on branches and clones. GitHub Docs, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes . Std (vendor).
7. Reference links only where inline URLs hurt reading (tables, repeated URLs). Google style guide. Prac.
8. Diagrams as Mermaid text, not exported images. GitHub Docs, https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams . Std (vendor).
9. Front matter only where a site generator reads it; GitHub renders it as a table. Community observation only (https://github.com/orgs/community/discussions/178337). Op.

### READMEs

10. Name, one line description, install, usage, then links out; what it does, why, how to start, where to get help, who maintains it. GitHub truncates past 500 KiB. GitHub Docs (above). Std (vendor).
11. standard-readme order: title, badges, short description (under 120 characters, no heading), contents (required at 100 lines), install, usage, contributing, license last; no broken links. https://github.com/RichardLitt/standard-readme/blob/main/spec.md . Op formalised as spec.
12. Broadest first, specialist detail deeper. Art of README (archived), https://web.archive.org/web/20231231175007/https://github.com/hackergrrl/art-of-readme . Op. Disagrees on usage before install.
13. Badges only if they give the typical reader real value. Art of README. Op.
14. Length: makeareadme says "too long is better than too short" (https://www.makeareadme.com/); GitHub favours short with links out. Rule: short README, nothing lost; move overflow to docs. Prac.
15. Code in a README runs as written after a clone. Art of README; makeareadme. Prac.

### Doc types and docs as code

16. Diátaxis: tutorial, how-to guide, reference, explanation; one type per page; mixing blurs both. https://diataxis.fr/ , https://diataxis.fr/compass/ . Prac (widely adopted). Counterpoint: GitLab mixes formats when useful.
17. Do not build empty Diátaxis scaffolding; improve one page at a time. https://diataxis.fr/how-to-use-diataxis/ . Prac.
18. Docs change in the same commit as the code. Google, https://google.github.io/styleguide/docguide/best_practices.html ; Write the Docs, https://www.writethedocs.org/guide/docs-as-code/ . Prac.
19. Minimum viable documentation; delete dead docs; incorrect docs are worse than missing ones. Google best practices; Write the Docs principles, https://www.writethedocs.org/guide/writing/docs-principles/ . Prac.
20. Check in CI: markdownlint-cli2 (https://github.com/DavidAnson/markdownlint-cli2), lychee for links (https://lychee.cli.rs/), Vale for prose (https://docs.vale.sh/). Std (tools).

## 6. Wikis and knowledge bases

1. One source of truth: link, do not repeat; if you copy, remove the origin and link. GitLab Handbook usage, https://handbook.gitlab.com/handbook/about/handbook-usage/ . Prac.
2. When pages conflict, name the canonical one and deprecate the rest. Software Engineering at Google, ch. 10, https://abseil.io/resources/swe-book/html/ch10.html . Prac.
3. Some repetition is acceptable as a short summary plus a link (Write the Docs "ARID"). Prac. Disagreement in emphasis with GitLab.
4. Changes proposed as edits to the page, then announced by linking the change. GitLab handbook first. Prac (one large org).
5. Every page has an owner and a last reviewed date; stale pages trigger review. Google freshness dates (SWE at Google ch. 10); Notion verified pages with expiry, https://www.notion.com/help/wikis-and-verified-pages ; Confluence verified status (no native expiry), https://community.atlassian.com/forums/Confluence-articles/Verified-Pages-Now-Available-in-Confluence/ba-p/2664827 . Prac and vendor features.
6. Findable: titles in the reader's own search words, labels, descriptive headings, linkable sections, a contents list once a page passes a screen; avoid catch all FAQ and link list pages. Atlassian, https://support.atlassian.com/jira-service-management-cloud/docs/write-and-share-knowledge-base-articles/ ; GitLab; Write the Docs principles. Prac.
7. Templates for repeating page types. Troubleshooting: problem, numbered fix, related pages (https://www.atlassian.com/software/confluence/templates/troubleshooting-article). Decision: status, stakeholders, background, options, outcome (https://www.atlassian.com/software/confluence/templates/decision). Std (vendor).
8. Decisions as ADRs: title, context, decision, status, consequences; numbered, never reused; superseded ones kept and linked. Nygard 2011, https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions ; https://adr.github.io/ . Prac.

Not found: a primary source for "docs or it didn't happen", a Write the Docs page specific to wikis, and a canonical "Diátaxis for wikis".

## 7. Charts and tables (all file types)

### Choice and encoding

1. Put the key comparison on a common scale (position); angle, area, and colour are read less precisely. Cleveland and McGill 1984, JASA 79(387), https://doi.org/10.1080/01621459.1984.10478080 . Emp.
2. Replicated by crowdsourcing; area is worse still. Heer and Bostock, CHI 2010, http://vis.stanford.edu/papers/crowdsourcing-graphical-perception . Emp.
3. Choose by relationship (deviation, correlation, ranking, distribution, change over time, magnitude, part to whole). FT Visual Vocabulary, https://github.com/ft-interactive/visual-vocabulary . Prac.
4. Lines for time, bars for categories; no lines across unordered categories. Datawrapper, https://www.datawrapper.de/blog/line-charts . Prac.
5. Tables for lookups and exact values, charts for shape. Few, Show Me the Numbers. Prac.
6. Small multiples with shared scales instead of one crowded chart. Tufte, Envisioning Information. Prac.
7. Bullet graphs instead of gauges. Few, https://www.perceptualedge.com/articles/misc/Bullet_Graph_Design_Spec.pdf . Prac.

### Integrity

8. Bars start at zero. Datawrapper Academy, https://www.datawrapper.de/academy/why-our-column-and-bar-charts-start-at-zero . Prac.
9. Truncated axes inflate perceived effects even with break marks; lines may be truncated when the range fits a meaningful effect. Correll, Bertini, Franconeri, CHI 2020, https://dl.acm.org/doi/10.1145/3313831.3376222 . Emp.
10. Drawn effect proportional to data effect (lie factor); icons scaled by height square the effect. Tufte, The Visual Display of Quantitative Information, https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/ . Prac.
11. No decorative 3D; it hurts pies and never helps. Schonlau and Peters, https://www.researchgate.net/publication/228314076 . Emp.
12. Dual axes are usually misleading; prefer two aligned charts or an index. Few, https://www.perceptualedge.com/articles/visual_business_intelligence/dual-scaled_axes.pdf ; Datawrapper, https://www.datawrapper.de/blog/dualaxis . Prac. Defended for correlation analysis (https://link.springer.com/chapter/10.1007/978-3-030-93119-3_22); a warning, not an error.

### Pies and decoration (contested)

13. Pies only for parts of a whole summing to 100 percent, about five slices at most. Datawrapper, https://www.datawrapper.de/blog/pie-charts . Prac.
14. Few against pies, https://www.perceptualedge.com/articles/visual_business_intelligence/save_the_pies_for_dessert.pdf (Prac); Skau and Kosara 2016 show pies and donuts read by area and arc, similar accuracy, https://kosara.net/publications/Skau-EuroVis-2016 (Emp). Rule: allow within limits.
15. Remove non data ink that carries nothing. Tufte. Prac.
16. Relevant embellishment did not hurt accuracy and helped recall. Bateman et al. CHI 2010, https://doi.org/10.1145/1753326.1753716 ; Borkin et al. 2013, http://web.mit.edu/zoya/www/docs/InfoVis_borkin-128.pdf . Emp. Few's rebuttal, https://www.perceptualedge.com/articles/visual_business_intelligence/the_chartjunk_debate.pdf . Rule: flag decoration that distorts or is irrelevant; allow relevant decoration.

### Titles and labels

17. Title states the finding; definitions go in the subtitle or notes. Datawrapper, https://www.datawrapper.de/blog/text-in-data-visualizations . Prac.
18. Titles drive what readers recall. Borkin et al. 2016, http://olivalab.mit.edu/Papers/07192646.pdf . Emp.
19. A slanted title changes what readers take away, and they still judge the chart impartial; so a finding title must be true to the data. Kong, Liu, Karahalios CHI 2018, https://doi.org/10.1145/3173574.3174012 ; CHI 2019, https://dl.acm.org/doi/10.1145/3290605.3300576 . Emp.
20. Label series directly rather than with a legend. Datawrapper, https://www.datawrapper.de/blog/color-keys-for-data-visualizations . Prac.
21. Sort unordered categories by value, "Other" last; keep natural order for time and ordinal. ONS, https://service-manual.ons.gov.uk/data-visualisation/guidance/ordering-in-charts . Prac.

### Colour

22. Colour only when it means something; soft colours for most data, one strong for the highlight. Few, https://www.perceptualedge.com/articles/visual_business_intelligence/rules_for_using_color.pdf . Prac.
23. Highlight one series, grey the rest. Datawrapper, https://www.datawrapper.de/blog/emphasize-with-color-in-data-visualizations . Prac.
24. More than about seven categorical colours is a defect. Datawrapper, https://www.datawrapper.de/blog/colors . Prac.
25. Sequential, diverging, categorical scales matched to the data; vary lightness; no rainbow scales on ordered data. Harrower and Brewer 2003, https://doi.org/10.1179/000870403235002042 ; viridis, https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html . Prac.
26. Avoid red and green pairs; about 8 percent of men of Northern European descent have red green colour vision deficiency; use Okabe-Ito or blue and orange; check in greyscale. Wong 2011, Nature Methods, https://www.nature.com/articles/nmeth.1618 ; Datawrapper, https://www.datawrapper.de/blog/colorblindness-part1 . Prac grounded in vision science.

### Accessibility

27. Colour not the only cue; chart marks 3:1; chart text 4.5:1. WCAG 1.4.1, 1.4.11, 1.4.3. Std.
28. Alt text: chart type, data, takeaway; long description or data table for complex charts. Cesal, https://medium.com/nightingale/writing-alt-text-for-data-visualization-2a218ef43f81 ; W3C complex images, https://www.w3.org/WAI/tutorials/images/complex/ . Std/Prac.

### Tables

29. Right align numbers, left align text, headers aligned with their column; never centre numbers (in Markdown, `---:`); tabular figures; same decimals in a column; units in the header; light rules or white space rather than a full grid; header set apart. Schwabish, "Ten Guidelines for Better Tables", J. Benefit-Cost Analysis 11(2) 2020, https://doi.org/10.1017/bca.2020.11 ; Datawrapper fonts, https://www.datawrapper.de/blog/fonts-for-data-visualization . Prac.

## 8. Design instructions

### DESIGN.md (Google)

1. `DESIGN.md`, by convention at the project root. Optional YAML front matter (`version`, `name`, `description`, `colors`, `typography`, `rounded`, `spacing`, `components`; `primary` colour required; references like `{colors.primary}`) and a Markdown body with sections in a fixed order: Overview, Colors, Typography, Layout, Elevation and Depth, Shapes, Components, Do's and Don'ts. "The tokens are the normative values; the prose provides context for how to apply them." The Overview guides choices no token covers; Do's and Don'ts are guardrails. A linter (`npx @google/design.md lint`) warns on contrast below 4.5:1. Alpha, Apache 2.0. https://github.com/google-labs-code/design.md ; spec, https://github.com/google-labs-code/design.md/blob/main/docs/spec.md ; https://github.com/google-labs-code/design.md/blob/main/PHILOSOPHY.md . Std (vendor, alpha).
2. Community DESIGN.md files describing real brands, extending the sections with responsive behaviour and an agent prompt guide. VoltAgent awesome-design-md, https://github.com/VoltAgent/awesome-design-md . Prac. These describe other companies' brands: style reference only, never their marks.
3. DESIGN.md is web and UI oriented (components, rounded corners, elevation). For decks and documents, map its colours, type scale, and spacing; ignore component tokens that have no match. (Inference.)

### Agent instruction files (precedence pattern)

4. AGENTS.md: nearest file to the edited file wins; explicit chat prompts override everything. https://agents.md/ . Prac (cross vendor).
5. Claude Code memory files concatenate from root down; context, not enforced config. https://code.claude.com/docs/en/memory . Std (vendor).
6. Kiro steering (`.kiro/steering/*.md`), workspace wins over global. https://kiro.dev/docs/steering/ . Cursor rules (`.cursor/rules/*.mdc`). https://cursor.com/docs/context/rules . Std (vendor).
7. Pattern across tools: explicit request, then team or org policy, then the nearest project file, then parent or global files.

### Design tokens

8. W3C DTCG Format Module 2025.10, first stable version (Community Group report, not a W3C Recommendation). `$value` required; `$type`, `$description`, `$extensions`, `$deprecated`; types include color, dimension, fontFamily, fontWeight, typography, shadow; aliases `{group.token}`; files `.tokens` or `.tokens.json`. https://w3c.github.io/cg-reports/design-tokens/CG-FINAL-format-20251028/ ; https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/ . Std (community group).
9. Style Dictionary supports DTCG since v4. https://styledictionary.com/info/dtcg/ . Std (tool docs).

### Brand guides

10. Typical contents: logo variants, clear space, minimum size, misuse examples, palette with usage rules, type hierarchy, voice. BrandyHQ, https://brandyhq.com/blog/logo-usage-guidelines/ ; Bynder, https://www.bynder.com/en/glossary/brand-guidelines-definition/ . Prac.
11. Third party marks follow their owner's rules: no altering, recolouring, or distorting. Microsoft Trademark and Brand Guidelines, https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks . Std (legal terms).

### Office themes and templates

12. One theme shared by PowerPoint, Word, and Excel: 12 colour slots (dk1, lt1, dk2, lt2, accent1 to accent6, hlink, folHlink) and a major (headings) and minor (body) font. ISO/IEC 29500; https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.colorscheme?view=openxml-3.0.1 . Std.
13. PowerPoint: master, layouts, placeholders; .potx. Changing theme fonts updates all title and body text. https://support.microsoft.com/en-us/powerpoint/create-and-save-a-powerpoint-template . Std (vendor).
14. Word: styles take theme fonts and colours; a theme does not override manual formatting; .dotx. https://support.microsoft.com/en-us/word/create-a-template . Std (vendor).
15. Excel: cell styles follow the theme; built in Input, Output, Calculation, Check Cell, Linked Cell styles; .xltx. https://support.microsoft.com/en-us/office/apply-create-or-remove-a-cell-style-472213bf-66bd-40c8-815c-594f0f90cd22 . Std.
16. Google Slides themes via Edit theme; Docs has paragraph styles but no theme builder. https://support.google.com/docs/answer/1705254 . Std (vendor).
17. To apply a brand: write it into the theme, masters, and styles, then clear direct formatting so objects inherit. Per object colours drift. (Inference from 12 to 15.)

### Accessibility under a design input

18. Brand colours are not exempt from contrast; only logotypes are. WCAG 2.2 Understanding 1.4.3. Std.
19. When a brand colour fails: use a passing tint or shade from the same family, or the brand's dark or light neutral for text; move the weak colour to large text or decoration; add a non colour cue; never alter the logo; report each substitution with both ratios. (Synthesis; Std basis.)

### Proposed precedence

1. Hard limits: content and numbers, logos and legal text, accessibility minimums. Nothing outranks these.
2. Explicit instructions in the request (or an attached brand guide or template). If they contradict a project design file, say so once and follow the request.
3. A design file in the project: the DESIGN.md, tokens file, or brand guide nearest to the target file; then design sections in AGENTS.md or CLAUDE.md. Tokens are values; prose decides what tokens do not cover. Tokens files win on values where both exist.
4. The file's own template, theme, master, and styles.
5. Docsmith's defaults.

When reviewing an existing file against a higher source, small deviations (an off palette colour on one chart) are fixes; restyling the whole file is a flag unless the user asked for it.
