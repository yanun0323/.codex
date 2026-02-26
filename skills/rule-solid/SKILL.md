---
name: rule-solid
description: Rules for SolidJS frontend work - boundaries, data fetching, UI states, error mapping, i18n copy rules, validation, security, and testing.
---

# SolidJS Frontend Rules


## 1) Stack and Constraints

- SolidJS + TypeScript
- Tailwind CSS for styling (must use existing project Tailwind setup; do not add alternate styling systems unless explicitly approved).
- Build tooling: follow the existing repo (often Vite).
- Prefer local, bundled references over external links.
  - Use `references/` in this skill for component patterns and example usage.
- Do not introduce new libraries (router/query/validation/UI) unless explicitly approved.
  - If the repo already uses a standard library (e.g., TanStack Router/Query, Zod), use it consistently.
- UI components MUST use shadcn-solid as the source of reusable components.
  - Follow the shadcn-solid copy/paste approach (components live in the repo; not a runtime dependency).
  - The CLI may be used for scaffolding, but do not add alternative UI component libraries unless explicitly approved.
  - Usage syntax and examples should come from this skill’s `references/` and from the repo’s existing `src/components/ui/` implementations.

### shadcn-solid UI Rules (Merged)

Real goal: produce SolidJS UI code **only** using the shadcn-solid component set and its composition patterns.

This is intentionally strict: if a shadcn-solid component exists for the job, use it.

Non-negotiable rules (text-only enforcement for now):
1. Do not hand-roll UI primitives when a shadcn-solid component exists.
   - Examples: dialogs, popovers, menus, selects, radios, checkboxes, toggles, tabs, pagination, toasts, text fields.
2. No raw `<button>`, `<input>`, `<select>`, `<textarea>` in product UI.
   - Exception: inside shadcn-solid components themselves, or when implementing a missing shadcn-solid component in `src/components/ui/`.
3. Prefer composition APIs (Trigger/Content/Portal/etc.) exactly as shown in references.
4. Imports must come from the local shadcn-solid UI layer (your repo), not from random third-party packages.
   - Typical: `@/components/ui/<component>` (or your repo's equivalent alias).
5. If a component is missing, add it to your repo (copy from upstream shadcn-solid / your registry) and then use it.
   - Do not re-implement a one-off variant inline.

Import path policy (avoid drift):
- Upstream docs show multiple import aliases (e.g. `@/components/ui/*`, `@components/ui/*`, sometimes `@/registry/ui/*`). Your repo must pick one convention.
- Do this once per task:
  - Search the codebase for existing imports from the UI layer and follow that alias consistently.
  - If no convention exists, default to `@/components/ui/<component>`.
- Never mix aliases within the same PR.

How to use this rule set while coding:
1. Identify what UI primitives you need (form inputs, overlay, menu, etc.).
2. Open the corresponding reference file under `references/` and follow the minimal usage example.
3. Compose the UI with shadcn-solid components; only use raw HTML for layout/typography wrappers (`div`, `section`, `header`, etc.).
4. Keep accessibility semantics intact: don't remove labels/triggers/portals just to \"simplify\".

References index (in `references/`):
- Get started: [Introduction](references/get-started-introduction.md), [Installation](references/get-started-installation.md), [Theming](references/get-started-theming.md), [Dark mode](references/get-started-dark-mode.md)
- Forms: [TanStack Form + Valibot](references/forms-tanstack-form.md)
- Components: [Accordion](references/component-accordion.md), [Alert](references/component-alert.md), [Alert Dialog](references/component-alert-dialog.md), [Badge](references/component-badge.md), [Breadcrumbs](references/component-breadcrumbs.md), [Button](references/component-button.md), [Button Group](references/component-button-group.md), [Calendar](references/component-calendar.md), [Card](references/component-card.md), [Carousel](references/component-carousel.md), [Chart](references/component-chart.md), [Checkbox](references/component-checkbox.md), [Collapsible](references/component-collapsible.md), [Combobox](references/component-combobox.md), [Command](references/component-command.md), [Context Menu](references/component-context-menu.md), [Data Table](references/component-data-table.md), [Date Picker](references/component-date-picker.md), [Dialog](references/component-dialog.md), [Drawer](references/component-drawer.md), [Dropdown Menu](references/component-dropdown-menu.md), [File Field](references/component-file-field.md), [Hover Card](references/component-hover-card.md), [Kbd](references/component-kbd.md), [Menubar](references/component-menubar.md), [Navigation Menu](references/component-navigation-menu.md), [Number Field](references/component-number-field.md), [OTP Field](references/component-otp-field.md), [Pagination](references/component-pagination.md), [Popover](references/component-popover.md), [Progress](references/component-progress.md), [Radio Group](references/component-radio-group.md), [Resizable](references/component-resizable.md), [Search](references/component-search.md), [Segmented Control](references/component-segmented-control.md), [Select](references/component-select.md), [Separator](references/component-separator.md), [Sidebar](references/component-sidebar.md), [Skeleton](references/component-skeleton.md), [Slider](references/component-slider.md), [Sonner](references/component-sonner.md), [Switch](references/component-switch.md), [Table](references/component-table.md), [Tabs](references/component-tabs.md), [Text Field](references/component-text-field.md), [Toggle Button](references/component-toggle-button.md), [Toggle Group](references/component-toggle-group.md), [Tooltip](references/component-tooltip.md)

---

## 2) Folder Ownership and Boundaries (Prefer / Enforce Where Applicable)

Typical structure (names may vary):
- app/: bootstrap, providers, global layout
- pages/: route composition only
- features/: feature logic + feature UI composition
- entities/: domain types/schemas only
- shared/: cross-cutting infra (api client, auth, ui, utils)

Hard rules:
- pages must not contain business logic or direct data fetching (unless repo does so already).
- shared must not depend on features/pages.
- entities must not depend on features.

If the repo has a different structure, follow the repo and keep boundaries consistent.

---

## 3) Data Fetching and Server State

- Prefer a single API client module (e.g., `shared/api/client.ts`) rather than scattered `fetch`.
- Handle non-2xx responses explicitly.
- Use TanStack Query for API interactions.
  - Follow existing repo patterns first (search for `createQuery`, `createMutation`, or the repo’s query wrapper).
  - Do not cache server state in ad-hoc signals.

---

## 4) UI State Requirements (MANDATORY)

All data-driven UI MUST implement:
- loading
- empty
- error
- success

Make state transitions explicit and consistent.

---

## 5) Error Mapping (Frontend)

- Backend error.code values are machine-stable; frontend maps codes to user-facing zh-TW messages.
- Always surface request_id when helpful (e.g., in error UI or toast) without exposing internal details.
- Do not show raw server error strings to users.

---

## 6) Copy and i18n Rules (STRICT)

- All user-facing UI copy MUST be Traditional Chinese (zh-TW).
- Copy MUST NOT be hardcoded inline inside components.
- Centralize copy in a shared module (choose existing location; examples):
  - `src/shared/i18n/zh-TW.ts`
  - `src/shared/copy.ts`

Rules:
- Keys: English
- Values: zh-TW
- Components import keys/values; no duplicated inline copy.

Non-copy strings (keep English):
- variable/function/type names
- API field names
- error codes / analytics keys
- CSS classes / test IDs

---

## 7) Validation

- Validate critical API responses at runtime when the repo has an existing pattern:
  - Use Zod if present.
  - Otherwise, implement minimal runtime guards for critical fields.
- Do not add a new validation library unless approved.

---

## 8) Security Baseline (Frontend)

- Frontend must never store or handle secrets.
- Permission checks in frontend are UX-only; backend is authoritative.
- Avoid leaking internal details in UI errors.

---

## 9) Testing (Aligned with Global Risk-Based Policy)

- If a frontend test harness exists:
  - Add minimal tests for medium/high-risk changes.
- If not:
  - Provide manual verification steps and recommend where a test should be added later.

---

## 10) When Uncertain

STOP and ASK if unclear about:
- authentication/authorization UX flows
- money/balance/order correctness
- destructive actions or irreversible UI flows
