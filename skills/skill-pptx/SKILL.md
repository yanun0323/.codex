---
name: skill-pptx
description: "Use this skill any time a .pptx file is involved in any way - as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill."
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX Skill

## Quick Reference

- Read/analyze: `python -m markitdown presentation.pptx`
- Visual overview: `python scripts/thumbnail.py presentation.pptx`
- Raw XML: `python scripts/office/unpack.py presentation.pptx unpacked/`
- Edit/template workflow: read `editing.md`
- Create from scratch: read `pptxgenjs.md`

## Design Rules

- Avoid plain title + bullets. Every slide needs a visual element: image, chart, icon, shape, timeline, comparison, or stat callout.
- Pick a content-specific palette with one dominant color, 1-2 supports, and one accent. Do not default to generic blue.
- Use a repeated motif; vary layouts across slides.
- Prefer strong contrast, 0.5" margins, 0.3-0.5" gaps, left-aligned body text, and title/body size contrast.
- Choose a deliberate font pairing; default only when matching a template.
- Never use low-contrast text/icons, random spacing, text-only slides, leftover placeholders, or accent lines under titles.
- Preserve and match existing templates when editing.

## QA Required

Assume the first render has issues.

1. Extract text:

```bash
python -m markitdown output.pptx
```

2. Check missing text, typos, order, and placeholders:

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

3. Render images:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

4. Visually inspect for overlap, overflow, cutoff, collisions, bad margins, uneven alignment, weak contrast, excessive wrapping, and placeholders.
5. Fix issues and re-render affected slides. Do not declare success until at least one fix-and-verify cycle is complete.

## Dependencies

`markitdown[pptx]`, Pillow, `pptxgenjs`, LibreOffice via `scripts/office/soffice.py`, and Poppler `pdftoppm`.
