---
name: skill-xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path - even casually (like \"the xlsx in my downloads\") - and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
license: Proprietary. LICENSE.txt has complete terms
---

# XLSX Skill

Use when the deliverable is a spreadsheet (`.xlsx`, `.xlsm`, `.csv`, `.tsv`).

## Requirements

- Use professional, consistent fonts.
- Preserve existing templates exactly; template conventions override all defaults.
- Deliver zero formula errors: `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`.
- Use formulas for calculations, not Python-hardcoded results, so workbooks remain dynamic.
- Recalculate formula workbooks with LibreOffice:

```bash
python scripts/recalc.py output.xlsx [timeout_seconds]
```

Fix reported errors and rerun until clean.

## Tool Choice

- `pandas`: data analysis, cleanup, bulk tabular transforms/export.
- `openpyxl`: formulas, formatting, workbook/sheet edits, preserving Excel features.
- `load_workbook(..., data_only=True)` reads calculated values but saving destroys formulas; do not save those workbooks.

## Financial Models

Unless template/user overrides:

- Blue text: hardcoded inputs/scenario values.
- Black: formulas.
- Green: same-workbook links.
- Red: external links.
- Yellow fill: key assumptions/update cells.
- Years as text; currency headers include units; zeros display as `-`; percentages `0.0%`; multiples `0.0x`; negatives in parentheses.
- Put assumptions in separate cells and reference them in formulas.
- Document hardcoded sources beside cells: source, date, reference, URL if applicable.

## Formula Checks

Verify sample references, column mapping, 1-indexed Excel row offsets, null handling, far-right columns, multiple matches, denominator zeros, cross-sheet refs, dependencies, and edge cases. Start formulas on a few cells before applying broadly.

## Code Style

Write concise Python with minimal comments/prints. In spreadsheets, comment complex formulas/assumptions and document data sources.

## Finish

Save, recalc if formulas exist, scan for errors, confirm expected sheets/ranges/formats, and report final spreadsheet path plus verification result.
