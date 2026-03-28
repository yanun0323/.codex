---
name: skill-vercel-design-guidelines
description: Use this skill to apply Vercel Web Interface Guidelines during UI design review, implementation, and copywriting in web apps (for web frontend usage, 網頁前端使用).
---

# Skill Vercel Design Guidelines

## Scope
Use this skill when a task asks for UI/UX direction, component behavior review, form/interaction behavior, layout polish, accessible content structure, copy tone, or performance-minded frontend decisions.

The source content is Vercel's Web Interface Guidelines: https://vercel.com/design/guidelines

## Core use case
1. Identify the area being changed (for example: interactions, animations, layout, content, forms, performance, design, or copywriting).
2. Evaluate against the corresponding rules.
3. Return concrete, actionable recommendations with file or selector-level specifics when possible.

## Interactions
- Keyboard works everywhere. All flows are keyboard-operable and should follow WAI-ARIA Authoring Patterns.
- Clear focus. Every focusable control must show visible focus. Prefer `:focus-visible` over `:focus` and use `:focus-within` for grouped controls.
- Manage focus. Use focus traps and move/return focus according to ARIA interaction patterns.
- Match visual and hit targets. If the visual target is smaller than 24px, expand hit area to at least 24px; on mobile, use minimum 44px.
- Mobile input size. Set input font size to at least 16px on mobile or set viewport with `maximum-scale=1`.
- Respect zoom. Never disable browser zoom.
- Hydration-safe inputs. Inputs should not lose focus or value after hydration.
- Don\'t block paste. Never disable paste in `<input>` or `<textarea>`.
- Loading buttons. Show a loading indicator and keep the original label visible.
- Minimum loading-state duration. If loading UI is shown, add a short show delay (~150 to 300 ms) and minimum visible time (~300 to 500 ms).
- URL as state. Persist UI state in URL so share, refresh, and back/forward behavior works.
- Optimistic updates. Update UI immediately, then reconcile on server response and rollback/undo on failure.
- Ellipsis for follow-up and processing states, such as Rename…, Loading…, Saving…, Generating…
- Confirm destructive actions, or provide undo with a safe window.
- Prevent double-tap zoom on controls by using `touch-action: manipulation`.
- Tap highlight follows design using `webkit-tap-highlight-color`.
- Design forgiving interactions with large targets, clear affordances, and predictable behavior.
- Tooltip timing: delay the first tooltip in a group; no delay for subsequent peers.
- Overscroll behavior: use `overscroll-behavior: contain` where appropriate.
- Persist scroll positions across back/forward navigation.
- Autofocus for speed on desktop only when there is a single primary input; avoid default autofocus on mobile.
- No dead zones: any visual affordance should be interactive.
- Deep-link everything, including tabs, filters, pagination, expanded panels, and stateful views.
- Clean drag interactions: disable text selection and apply `inert` while dragging.
- Links are links: use `<a>` or `<Link>` for navigation, not `<button>` or `<div>`.
- Announce async updates using polite `aria-live`.
- Locale-aware keyboard shortcuts with platform-specific symbols.

## Animations
- Honor `prefers-reduced-motion` and provide a reduced-motion variant.
- Prefer CSS first, then Web Animations API; avoid main-thread JS-driven animations when possible.
- Prefer compositor-friendly properties (`transform`, `opacity`) and avoid layout properties (`width`, `height`, `top`, `left`) that trigger reflow/repaint.
- Animate only when it clarifies cause and effect or adds deliberate delight.
- Match easing to what changes (size, distance, trigger).
- Keep animations interruptible.
- Animate in response to input; avoid autoplay.
- Set meaningful transform origin for where motion starts.
- Avoid `transition: all`; explicitly list intended properties.
- For SVG, animate `<g>` wrappers and set `transform-box: fill-box; transform-origin: center`.

## Layout
- Optical alignment: adjust by 1px when visual perception beats geometry.
- Deliberate alignment to grid, baseline, edge, or optical center; avoid accidental placement.
- Balance lockups by adjusting icon/text weight, size, and spacing.
- Validate responsive behavior on mobile, laptop, and ultra-wide (simulate ultra-wide at 50% zoom).
- Respect safe areas using safe-area variables.
- Avoid excessive scrollbars; fix overflow issues that create unwanted scrolling.
- Let browser layout handle flow, wrapping, and alignment with flex/grid/intrinsic sizing instead of JS measurements.

## Content
- Inline help before tooltips.
- Stable skeletons that mirror final content to avoid layout shift.
- Accurate page titles by context.
- No dead ends: every screen has a next step or recovery path.
- Design all states including empty, sparse, dense, and error.
- Prefer curly quotes (“ ”) over straight quotes.
- Avoid widows and orphans.
- Use tabular numbers (`font-variant-numeric: tabular-nums`) for comparisons.
- Never rely on color alone; include text labels.
- Keep icon and control meaning clear to non-sighted users.
- Keep accessible names/labels even if visual labels are omitted.
- Use the ellipsis character `…` rather than three periods.
- Set `scroll-margin-top` for heading anchors.
- Keep layouts resilient to short, average, and long user-generated content.
- Format dates, times, numbers, and currencies for user locale.
- Use language settings (`Accept-Language` and `navigator.languages`) instead of IP/GPS location.
- Set accurate accessible names (`aria-label`) and hide decorative elements with `aria-hidden`.
- Icon-only controls must have descriptive `aria-label`.
- Prefer native semantics (`button`, `a`, `label`, `table`) before ARIA attributes.
- Use hierarchical headings and provide a skip link.
- Use non-breaking spaces to prevent glued terms from breaking:
  - `10 MB` to `10&nbsp;MB`
  - `⌘ + K` to `⌘&nbsp;+&nbsp;K`
  - `Vercel SDK` to `Vercel&nbsp;SDK`
- Use `&#x2060;` when no space is desired.

## Forms
- Enter submits when a focused text input is the only control; if multiple controls exist, submit from the last control.
- In `<textarea>`, ⌘/⌃+Enter submits; Enter inserts newline.
- Every control has a `<label>` or explicit label association.
- Clicking labels focuses the associated control.
- Keep submit enabled until request starts; then disable during in-flight requests, show spinner, and include an idempotency key.
- Don\'t block typing. Allow input and provide validation feedback.
- Don\'t pre-disable submit; allow incomplete submits to surface validation.
- Radios/checkboxes should avoid dead zones; label and control should share one hit target.
- Place errors next to fields; on submit, focus first error.
- Set `autocomplete` and meaningful `name` values for autofill.
- Disable spellcheck selectively for emails, codes, usernames, etc.
- Use correct `type` and `inputmode` for each field.
- Placeholders should signal emptiness and end with an ellipsis.
- Placeholder value should be an example or pattern, e.g. `+1 (123) 456-7890` and `sk-012345679…`.
- Warn before navigation when unsaved changes exist.
- Ensure password managers and 2FA workflows work, and allow pasting one-time codes.
- Don\'t trigger password-manager fields on non-auth inputs.
- Trim trailing whitespace for fields affected by text replacement/expansion.
- Set explicit `background-color` and `color` on native `<select>` for Windows dark-mode contrast.

## Performance
- Test across device/browser matrices, including iOS Low Power Mode and macOS Safari.
- Measure reliably and disable extensions that alter runtime behavior.
- Minimize and speed up re-renders using React DevTools or React Scan.
- Profile with CPU and network throttling.
- Minimize layout work by batching reads/writes and avoiding unnecessary reflows/repaints.
- Keep POST/PATCH/DELETE latency below 500ms as a practical target.
- Prefer uncontrolled inputs when possible; make controlled loops cheap.
- Virtualize large lists (for example with `virtua` or `content-visibility: auto`).
- Preload only above-the-fold images; lazy-load the rest.
- Prevent image CLS with explicit dimensions and reserved space.
- Use `preconnect` for key origins with `crossorigin` where needed.
- Preload critical fonts to reduce first paint text jump.
- Subset fonts with `unicode-range` and limit variable axes.
- Move expensive long tasks off main thread, often into Web Workers.

## Design
- Use layered shadows with at least two layers for ambient + direct light.
- Use crisp borders and semi-transparent borders where helpful.
- Keep nested radii concentric with child radius <= parent radius.
- Keep hue consistency on non-neutral backgrounds.
- Use color-blind-friendly chart palettes.
- Prefer APCA contrast guidance over WCAG 2 for perceptual contrast.
- Raise contrast in hover, active, and focus states.
- Keep browser UI consistent with page background via `<meta name="theme-color">`.
- Set `color-scheme: dark` on `<html>` in dark themes for UI elements like scrollbars.
- For text scaling artifacts, animate wrappers or use `translateZ(0)` / `will-change`.
- Avoid gradient banding; use background images for dark fades when needed.

## Vercel-specific copywriting
- Use active voice and keep copy concise.
- Headings and buttons use Title Case (Chicago), while marketing pages can use sentence case.
- Prefer `&` where stylistically appropriate.
- Use action-oriented language and second-person framing.
- Use consistent terms and placeholders (for example, `YOUR_API_TOKEN_HERE`, `0123456789`).
- Use numerals for counts.
- Keep currency formatting consistent within a given context (either all zero-decimal or two-decimal).
- Separate number and unit with a space, use non-breaking spaces for glued units.
- Use positive, solution-oriented language in success and error states.
- Error copy should explain what to do next.
- Use specific labels (e.g., avoid generic labels like Continue).
- Example replacements:
  - "The CLI will be installed" -> "Install the CLI"
  - "You will need the CLI…" -> "Install the CLI…"
  - "Your deployment failed" -> "Something went wrong; try again or contact support"
  - "Invalid API key" -> "Your API key is incorrect or expired. Generate a new key in your account settings"
  - "Continue" -> "Save API Key"

## AGENTS integration
- If using Vercel agent review workflows, use:
  - `curl -fsSL https://vercel.com/design/guidelines/install | bash`
- Add AGENTS.md in projects where these rules should be auto-applied.
