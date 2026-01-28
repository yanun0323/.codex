# Solid Component Writing Standard (Shard Solid)

This file defines the REQUIRED component writing rules for SolidJS UI work in this repo.
If shard-solid references do not cover a topic, follow this standard.

## 1) File Placement & Naming
- **Components** go under `shared/ui/components/*`.
- **Primitives** go under `shared/ui/primitives/*`.
- **Feature UI** goes under `features/*/ui/*` (or existing repo convention).
- File names: `kebab-case.tsx`.
- Component names: `PascalCase` matching file name.

## 2) Component Structure (Required Order)
1. Imports
2. Types
3. Constants (static data only)
4. Component definition
5. Helpers (pure functions only)

## 3) Props & Types
- Props types must be explicit: `type XxxProps = { ... }`.
- Props should be minimal; prefer composition over configuration overload.
- No `any` in UI components.

## 4) State & Effects
- Use `createSignal`/`createMemo` for local UI state.
- Avoid derived state in signals when `createMemo` is sufficient.
- Use `createEffect` only for side effects, never for derivations.

## 5) Rendering & Slots
- Use `props.children` for slot-like composition.
- Avoid implicit DOM structure changes; keep DOM structure stable.
- Keep JSX shallow; extract subcomponents when depth > 3 levels.

## 6) Styling
- Use Tailwind classes only (no inline styles unless required by spec).
- Prefer tokens from Tailwind config (avoid magic numbers).
- Keep variant classes in a single `cn(...)` block.

## 7) Accessibility
- Use semantic elements (button, nav, header, section).
- Always provide accessible labels for inputs.
- Interactive components must be keyboard accessible.

## 8) Copy & i18n
- No inline user-facing strings.
- Use shared copy (zh-TW) as required by agents-solid.

## 9) Error/Empty/Loading States
- Data-driven UI must implement loading/empty/error/success states.

## 10) Do Not
- Do not fetch data in shared UI components.
- Do not import primitives directly in feature UI.
- Do not bypass shard-solid patterns with custom styling or behaviors.
