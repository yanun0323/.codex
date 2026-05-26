---
name: skill-docx
description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of \"Word doc\", \"word document\", \".docx\", or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a \"report\", \"memo\", \"letter\", \"template\", or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation."
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX Skill

`.docx` is a ZIP of XML. Use structured tools, then validate.

## Read / Convert

- Legacy `.doc`: convert first with `python scripts/office/soffice.py --headless --convert-to docx document.doc`.
- Extract text, including tracked changes: `pandoc --track-changes=all document.docx -o output.md`.
- Raw XML: `python scripts/office/unpack.py document.docx unpacked/`.
- Images/pages: convert to PDF with `soffice.py`, then `pdftoppm`.
- Accept tracked changes: `python scripts/accept_changes.py input.docx output.docx`.

## Create New DOCX

Use `docx-js` (`npm install -g docx`) and validate with:

```bash
python scripts/office/validate.py doc.docx
```

Hard rules:

- Set page size explicitly; docx-js defaults to A4. US Letter is `12240 x 15840` DXA.
- Landscape: pass portrait dimensions and `PageOrientation.LANDSCAPE`.
- Use Arial/default professional fonts unless instructed.
- Override built-in heading IDs exactly (`Heading1`, `Heading2`) and include `outlineLevel` for TOC.
- Use numbering config for bullets/numbers; never manual Unicode bullets.
- Never use `\n`; create separate `Paragraph`s.
- Page breaks must be inside `Paragraph`.
- `ImageRun` requires `type` and complete `altText`.
- Tables need `WidthType.DXA`, table `width`, `columnWidths`, matching cell widths, cell margins, and `ShadingType.CLEAR`.
- TOC headings must use `HeadingLevel`.

## Edit Existing DOCX

1. Unpack:

```bash
python scripts/office/unpack.py document.docx unpacked/
```

2. Edit XML in `unpacked/word/` with direct string replacement, not scripts, unless using provided helpers. Use `Claude` as tracked-change/comment author unless user specifies otherwise.
3. Pack:

```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

Packing validates and auto-repairs invalid `durableId` values and missing `xml:space="preserve"` on whitespace text.

## XML Rules

- Preserve XML validity, element order, RSIDs, relationships, and formatting runs.
- Use smart quote entities in new professional text: `&#x2018;`, `&#x2019;`, `&#x201C;`, `&#x201D;`.
- Add `xml:space="preserve"` to `<w:t>` with leading/trailing spaces.
- For tracked changes, replace whole `<w:r>` elements with sibling `<w:del>`/`<w:ins>`; do not inject change tags inside runs. Preserve `<w:rPr>`.
- Use `scripts/comment.py` for comments, then add markers in document XML.

## Finish

Validate, reopen/extract key text if possible, and report the final `.docx` path plus any unsupported features or manual checks.
