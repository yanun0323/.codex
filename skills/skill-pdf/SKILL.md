---
name: skill-pdf
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Skill

Use PDF libraries/tools by task. For advanced operations see `REFERENCE.md`; for forms read `FORMS.md`.

## Tool Choice

- `pypdf`: read, merge, split, rotate, metadata, encrypt/decrypt, simple page ops.
- `pdfplumber`: text with layout and table extraction.
- `reportlab`: create PDFs.
- `pdftotext`: fast text extraction (`-layout`, `-f`, `-l`).
- `qpdf`: merge/split/rotate/decrypt from CLI.
- `pdftk`: use only if available.
- Scanned PDFs: OCR with `pytesseract` + `pdf2image`.

## ReportLab Rules

- Do not use Unicode subscript/superscript glyphs; built-in fonts may render boxes. Use Paragraph XML tags `<sub>`/`<super>` or manual canvas positioning.
- Prefer Platypus (`SimpleDocTemplate`, `Paragraph`, `Spacer`, `PageBreak`) for structured documents.
- Use professional fonts, margins, and page sizes appropriate to the deliverable.

## Common Workflows

- Merge: iterate readers with `PdfWriter.add_page`, or `qpdf --empty --pages ... -- output.pdf`.
- Split: create one `PdfWriter` per page/range.
- Rotate: use `page.rotate(90)` or `qpdf --rotate`.
- Watermark: load watermark page and merge onto each target page.
- Tables: extract with `pdfplumber`; convert to DataFrame/XLSX when requested.
- OCR: convert pages to images, run Tesseract, preserve page ordering.

## Verification

Confirm output exists, page count, key extracted text/table samples, rotation/order, form fields/watermark/OCR as applicable. Never expose protected content beyond the user’s requested transformation.
