---
description: Audit UI code against the local design system and report concrete spacing, depth, color, and pattern drift.
---

Audit the current interface implementation against the project's design system.

Workflow:
1. Check whether `.vscode/interface-design/system.md` exists.
2. If it exists, extract the project's spacing, depth, color, and component rules.
3. Inspect relevant UI files and compare them against those rules.
4. Report only concrete violations with file locations and actionable fixes.
5. If no system file exists, say so clearly and recommend either extracting a system or establishing one first.

Focus areas:
- Spacing scale violations
- Radius and border inconsistencies
- Depth model drift such as unexpected shadows
- Color palette drift
- Repeated component pattern mismatches

Keep the output concise and oriented toward fixes, not theory.
