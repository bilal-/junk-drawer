# Spreadsheets

Read this when building a workbook, or reviewing a model, a data table, or anything people make decisions from. It adds to Check 4 in SKILL.md. Sources are in the drawer's `research/docsmith.md`, section 4 (FAST Standard, ICAEW Financial Modelling Code, EuSpRIG and Panko's error research, Broman and Woo).

Most real workbooks contain errors, and the people who built them rarely see them. Check cell by cell where it matters, and do not trust a workbook because it looks tidy.

## Two kinds of sheet

* A model (inputs, calculations, outputs): apply the model rules.
* A data table (records, logs, exports): apply the data table rules.

Many workbooks have both. Keep them on separate sheets.

## Model layout

* Inputs, calculations, and outputs are separate, ideally on separate sheets. A dashboard that takes a few inputs and shows results is the allowed exception.
* A cover or About sheet: purpose, owner, version or date, contents, the colour key, and known limits.
* Each input is entered once; each calculation is done once. Everything else links to it.
* Calculations flow top to bottom and left to right. Sheets are ordered the same way (inputs, then calculations, then outputs).
* Columns line up across sheets: the label, units, constants, and first period sit in the same columns everywhere.
* One timeline driven by one start date input. Each column is one period.
* Avoid links to other workbooks. If needed, bring data in through one import sheet.

## Formulas

* One formula per row, the same across the row. Any cell that breaks the pattern is a finding.
* Short formulas. If a formula is longer than your thumb on screen or takes more than about half a minute to explain, split it into steps. Flag deeply nested IFs, and volatile or opaque functions such as OFFSET and INDIRECT.
* No changeable numbers inside formulas (rates, prices, thresholds). Fixed constants such as 12, 24, 100, or 1000 are fine.
* Never type a value over a formula in a calculated row.
* Link to the original calculation, not to a cell that only links to it.
* Ranges cover the whole data. Check range ends against the last row (a short range silently drops data).
* No circular references. Round only for display, not in calculations.

## Labels, units, signs

* Every row has a unique label with its unit: "Revenue ($000)", "Headcount (FTE)". No mixed scales in a row.
* One sign convention, stated on the cover sheet, used everywhere.
* Sheet names mean something. "Sheet1" is a finding.

## Colour key and styles

* Inputs look different from formulas, under one key for the whole workbook, explained on the cover sheet. Do not impose a palette: banks use blue font for inputs, black for formulas, and green for links to other sheets; ICAEW prefers a fill or border for inputs, not font colour alone. Check that the workbook follows its own key, and if it has none, add one only in build mode or flag it.
* Use cell styles (Excel's built in Input, Calculation, Output, Check Cell, and Linked Cell, or the workbook's own) rather than one off formatting.
* Keep conditional formatting light.
* No merged cells. Use center across selection for headings.

## Number formats

* Numbers right aligned. The same decimals within a column, and no more precision than the data has.
* Thousands separators. One style for negatives (minus sign or parentheses), used throughout.
* Percentages formatted as percentages, dates as dates.
* Units in the header, not repeated in every cell.

## Navigation and print

* Freeze panes so labels and the timeline stay visible.
* Print areas, titles, and fit to width set on input and output sheets only.

## Hidden things and names

* Nothing hidden without a reason: rows, columns, sheets, white text, number formats that show nothing. Hiding unused columns past the timeline is fine. Hidden content has caused real data breaches; flag it.
* Before removing a hidden sheet, check whether any formula refers to it. Prefer unhide and flag.
* Named ranges: the standards disagree, so do not flag names as such. Flag names that are vague, broken, or say something different from the row label.

## Checks

* A checks area or sheet: balance sheet balances, totals reconcile, required inputs are filled. Each check has a small tolerance.
* One master check that rolls them all up, shown where every sheet can see it.
* In build mode, add checks for every total that should tie out.

## Data tables

* One rectangle: one header row, one variable per column, one record per row, one value per cell.
* No blank rows or columns inside the table, no subtotals mixed in with records, no calculations in raw data.
* Dates in ISO form (YYYY-MM-DD). Watch for text that the app turned into dates (gene names, part codes, IDs with leading zeros).
* No colour or highlighting as data; add a column instead.
* One consistent code for missing values. Flag mixed codes and blanks that mean "same as above".
* A data dictionary or notes sheet explaining each column.
* Data validation on columns people type into.
* Check the format's limits (an old .xls file stops at 65,536 rows).

## Common fixes and flags

Fix: a hardcoded total replaced by a formula giving the same value, an inconsistent formula in a row repaired when the intent is obvious, units added to labels, number formats made consistent, freeze panes set, a missing input style applied under the workbook's existing key.

Flag: mixed inputs and calculations that need reorganizing, a missing checks sheet in a model, hidden content, a formula whose intent is unclear, a short range, a number with no source, a data table that is not rectangular.
