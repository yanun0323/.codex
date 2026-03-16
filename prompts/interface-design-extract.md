---
description: Extract reusable UI patterns from existing code and codify them into a local interface design system document.
---

Extract a design system from the current UI codebase.

Workflow:
1. Scan common UI files for repeated spacing, radius, color, typography, shadow, and layout values.
2. Infer the dominant patterns rather than listing every value.
3. Identify reusable component patterns such as buttons, inputs, cards, tables, and panels.
4. Summarize the inferred system in a concrete, reusable format.
5. Create or update `.vscode/interface-design/system.md` if the task implies saving the extracted system.

Output expectations:
- Show the proposed scales and patterns.
- Call out ambiguity when the codebase contains conflicting patterns.
- Favor frequency-based decisions over one-off outliers.
