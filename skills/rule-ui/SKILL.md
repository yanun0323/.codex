---
name: rule-ui
description: UI layering and component rules for SolidJS UI work, including tier boundaries, styling, accessibility, and review checklist.
---

# UI Layering and Component Rules (SolidJS)


## 1) UI Layering Model (MANDATORY)

All UI MUST follow a 3-tier model:

Tier 1: Primitives  -> interaction behavior + accessibility only
Tier 2: Components  -> styling + structure + reusable visual patterns
Tier 3: Features    -> composition + data binding + feature state

No layer skipping.

---

## 2) Tier 1 - Primitives (Behavior + A11y Only)

- Use existing primitive libraries in the repo.
  - If the repo uses Kobalte: prefer Kobalte primitives.
  - If the repo uses corvu: use it only for gaps/approved patterns.
- Primitives MUST:
  - be unstyled or minimally styled
  - contain no business logic
  - contain no user-facing copy
- Primitives should live in a stable location (example):
  - `shared/ui/primitives/*`

Do not introduce a new primitive library without approval.

---

## 3) Tier 2 - Shared Components (Reusable Visual Patterns)

- Shared components wrap Tier 1 primitives and own styling.
- Components MUST:
  - use centralized copy (no inline user-facing strings)
  - standardize spacing/typography via Tailwind tokens or design tokens
  - avoid data fetching and business logic
- Suggested location:
  - `shared/ui/components/*`

Copy-paste component sources (only if already part of repo conventions):
- Solid UI / shadcn-solid style patterns:
  - MUST be copied into the codebase (no opaque runtime dependency)
  - MUST be adapted to project folder boundaries and copy rules

---

## 4) Tier 3 - Feature UI (Composition Only)

- Feature UI composes Tier 2 components and binds server state.
- Feature UI MUST NOT:
  - import Tier 1 primitives directly
  - implement custom accessibility behaviors
  - reimplement generic UI patterns (dialogs, menus, toasts)

---

## 5) Tailwind and Styling Rules

- Prefer design tokens from Tailwind config.
- Avoid arbitrary magic numbers.
  - Arbitrary values allowed only when no token exists and must be justified.
- Keep styling decisions out of primitives (Tier 1).
- Consistent spacing and typography across features.

---

## 6) Accessibility (Non-Negotiable)

- Interactive elements must be keyboard accessible.
- Inputs must have associated labels.
- Dialogs/menus/popovers must manage focus correctly (via primitives).
- Use semantic HTML where possible.

---

## 7) Common Anti-Patterns (HARD ERRORS)

- Feature imports primitives directly (skips Tier 2)
- Inline user-facing strings in JSX/TSX
- Data fetching inside shared UI components
- Multiple inconsistent dialogs for the same pattern
- Reimplementing dialog/menu behavior in feature code
- Showing raw server error messages to users

---

## 8) UI Review Checklist (Use in Critic Mode)

- Does the UI implement loading/empty/error/success?
- Is copy centralized and zh-TW?
- Are error states user-safe and actionable?
- Are interactions accessible (keyboard/focus)?
- Are reusable patterns extracted into Tier 2 instead of duplicated?
- Are styles consistent with existing design tokens?
