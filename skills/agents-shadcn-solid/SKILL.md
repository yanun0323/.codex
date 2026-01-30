---
name: agents-shadcn-solid
description: Build SolidJS frontends using shadcn-solid UI components only. Provides references for each component and setup guides; use this skill when writing or refactoring SolidJS UI so you do not hand-roll primitives.
license: Proprietary. See LICENSE.txt
compatibility: Designed for an agent that can edit a SolidJS codebase (e.g., Codex CLI). Assumes TailwindCSS (or UnoCSS) + shadcn-solid components installed in the repo.
---

# shadcn-solid-ui

## Real goal

Produce SolidJS UI code **only** using the shadcn-solid component set and its composition patterns.

This skill is intentionally **strict**: if a shadcn-solid component exists for the job, use it.

## Non‑negotiable rules (text-only enforcement for now)

1. **Do not hand-roll UI primitives** when a shadcn-solid component exists.
   - Examples: dialogs, popovers, menus, selects, radios, checkboxes, toggles, tabs, pagination, toasts, text fields.
2. **No raw `<button>`, `<input>`, `<select>`, `<textarea>`** in product UI.
   - Exception: inside shadcn-solid components themselves, or when you are implementing a missing shadcn-solid component in `src/components/ui/`.
3. **Prefer composition APIs** (Trigger/Content/Portal/etc.) exactly as shown in references.
4. **Imports must come from the local shadcn-solid UI layer** (your repo), not from random third-party packages.
   - Typical: `@/components/ui/<component>` (or your repo’s equivalent alias).
5. If a component is missing, **add it to your repo** (copy from upstream shadcn-solid / your registry) and then use it. Do not re-implement a one-off variant inline.

## Import path policy (avoid drift)

Upstream docs show multiple import aliases (e.g. `@/components/ui/*`, `@components/ui/*`, sometimes `@/registry/ui/*`).
Your repo must pick one convention.

**Do this once per task:**
- Search the codebase for existing imports from the UI layer and follow that alias consistently.
- If no convention exists, default to `@/components/ui/<component>`.

Never mix aliases within the same PR.

## How to use this skill while coding

1. Identify what UI primitives you need (form inputs, overlay, menu, etc.).
2. Open the corresponding reference file under `references/` and follow the minimal usage example.
3. Compose the UI with shadcn-solid components; only use raw HTML for layout/typography wrappers (`div`, `section`, `header`, etc.).
4. Keep accessibility semantics intact: don’t remove labels/triggers/portals just to “simplify”.

## References index

### Get started
- [Introduction](references/get-started-introduction.md)
- [Installation](references/get-started-installation.md)
- [Theming](references/get-started-theming.md)
- [Dark mode](references/get-started-dark-mode.md)

### Forms
- [TanStack Form + Valibot](references/forms-tanstack-form.md)

### Components
- [Accordion](references/component-accordion.md)
- [Alert](references/component-alert.md)
- [Alert Dialog](references/component-alert-dialog.md)
- [Badge](references/component-badge.md)
- [Breadcrumbs](references/component-breadcrumbs.md)
- [Button](references/component-button.md)
- [Button Group](references/component-button-group.md)
- [Calendar](references/component-calendar.md)
- [Card](references/component-card.md)
- [Carousel](references/component-carousel.md)
- [Chart](references/component-chart.md)
- [Checkbox](references/component-checkbox.md)
- [Collapsible](references/component-collapsible.md)
- [Combobox](references/component-combobox.md)
- [Command](references/component-command.md)
- [Context Menu](references/component-context-menu.md)
- [Data Table](references/component-data-table.md)
- [Date Picker](references/component-date-picker.md)
- [Dialog](references/component-dialog.md)
- [Drawer](references/component-drawer.md)
- [Dropdown Menu](references/component-dropdown-menu.md)
- [File Field](references/component-file-field.md)
- [Hover Card](references/component-hover-card.md)
- [Kbd](references/component-kbd.md)
- [Menubar](references/component-menubar.md)
- [Navigation Menu](references/component-navigation-menu.md)
- [Number Field](references/component-number-field.md)
- [OTP Field](references/component-otp-field.md)
- [Pagination](references/component-pagination.md)
- [Popover](references/component-popover.md)
- [Progress](references/component-progress.md)
- [Radio Group](references/component-radio-group.md)
- [Resizable](references/component-resizable.md)
- [Search](references/component-search.md)
- [Segmented Control](references/component-segmented-control.md)
- [Select](references/component-select.md)
- [Separator](references/component-separator.md)
- [Sidebar](references/component-sidebar.md)
- [Skeleton](references/component-skeleton.md)
- [Slider](references/component-slider.md)
- [Sonner](references/component-sonner.md)
- [Switch](references/component-switch.md)
- [Table](references/component-table.md)
- [Tabs](references/component-tabs.md)
- [Text Field](references/component-text-field.md)
- [Toggle Button](references/component-toggle-button.md)
- [Toggle Group](references/component-toggle-group.md)
- [Tooltip](references/component-tooltip.md)

## Notes

- This skill folder follows the Agent Skills format: `SKILL.md` with YAML frontmatter + optional `references/` directory for progressive disclosure.
