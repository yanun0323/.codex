---
name: agents-solid-shard
description: Enforce shard-solid conventions for SolidJS components. Use for any SolidJS UI/component work to ensure strict compliance with shard-solid.md.
---

# agents-solid-shard

## When to Use
- Any request that adds/edits/refactors SolidJS components or UI.
- Any work that touches SolidJS UI patterns, component structure, or styling.

If any rule conflicts with explicit user instructions, follow the user instructions.
If any rule conflicts with agents-global, follow the higher-priority rule defined there.

---

## Required References (MANDATORY)
You MUST read the shard-solid references before making any SolidJS UI/component change.

- Primary index: `references/shard-solid/00-index.md`
- Section files: `references/shard-solid/*.md`
- Writing standard: `references/standards/solid-component-writing.md`

If you cannot find a relevant rule after searching the references, STOP and ask the user for clarification.

---

## How to Use the References (STRICT)
1) Open `references/shard-solid/00-index.md`.
2) Find the matching section title for the task.
3) Read the corresponding section file(s).
4) Read `references/standards/solid-component-writing.md` and apply all rules.
4) Implement exactly as described; do not invent patterns.
5) Self-check against the section(s) before responding.

---

## Enforcement Rules (HARD)
- Do not create SolidJS components that violate shard-solid structure, naming, or styling rules.
- Do not introduce alternative UI patterns when shard-solid provides guidance.
- Do not bypass shard-solid requirements by “custom fixes”.
- When uncertain, STOP and ASK.
### When shard-solid is about CLI/dependencies only
If a shard-solid section is purely about CLI/setup/dependencies, follow it as a setup step only. Use the writing standard for component structure and behavior.

---

## Conflict Resolution With Other Skills
If a rule in agents-solid/agents-ui conflicts with shard-solid guidance:
- Prefer shard-solid for component structure, styling, and composition rules.
- Prefer agents-ui for layering/a11y rules unless shard-solid explicitly overrides them.
- Prefer agents-solid for data fetching, error states, i18n, and validation rules.
If shard-solid only provides installation/CLI guidance, defer to the writing standard for component structure.

When a conflict is detected, state it briefly and proceed with the higher-priority rule.

---

## Minimal Self-Check (MANDATORY)
- The implementation matches the exact shard-solid section(s) used.
- No user-facing strings are inline (use shared copy as required by agents-solid).
- UI states include loading/empty/error/success where data-driven.
- Tiering (primitives/components/features) is respected.
