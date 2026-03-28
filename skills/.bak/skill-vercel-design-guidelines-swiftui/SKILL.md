---
name: skill-vercel-design-guidelines-swiftui
description: Use this skill to apply Vercel Web Interface Guidelines when building SwiftUI interfaces and interactions (for SwiftUI usage, SwiftUI 使用).
---

# Skill Vercel Design Guidelines for SwiftUI

## Scope
Use this skill when a task asks for SwiftUI UI/UX direction, component behavior review, form/interaction behavior, layout polish, accessibility, content structure, copy tone, or performance-minded frontend decisions.

The source content is Vercel's Web Interface Guidelines: https://vercel.com/design/guidelines

This adaptation translates the web principles to SwiftUI contexts across iOS, iPadOS, macOS, watchOS, and tvOS.

## Core use case
1. Identify which area is changing (interactions, animations, layout, content, forms, performance, design, or copy).
2. Apply the relevant rules in the equivalent SwiftUI implementation layer.
3. Return concrete, actionable recommendations with SwiftUI APIs and modifier names.

## Interactions
- Keyboard and focus work for every task flow.
  - iOS: support keyboard shortcuts and Return key behavior in iPad text fields.
  - macOS: ensure tab focus order follows a logical reading order.
  - tvOS: verify focus updates and focus restoration.
- Visible focus and selection.
  - Use clear focus states, `focusable`, and visible focus highlights where applicable.
  - Use `FocusState` for deterministic focus movement.
- Manage focus and focus return after modals, sheets, and popovers.
- Match visual affordance and hit target size.
  - Use minimum 44pt touch targets on mobile; keep clear margins between interactive controls.
- Provide resilient input targets for trackpad, pointer, and touch.
- Avoid disabling paste in text inputs.
- For long operations, keep button label and action feedback visible together (label + spinner).
- Use progressive loading indicators with minimal perceived flicker.
- Keep async button states disabled only while request is in flight.
- Show copy-friendly, action-oriented labels in button states, such as "Saving…" and "Retrying…".
- Use stable URLs and deep links when possible, or equivalent deep navigation state for app flows.
- Optimistic UI when safe; always reconcile with server state and support cancel/undo semantics.
- Persist list/grid/state position across transitions when possible.
- Guard destructive actions with explicit confirmation or undo.
- Avoid accidental gesture dead zones; controls should have generous `contentShape`.
- For drag interactions, disable unintended text selection and keep source state consistent during drag.
- Use semantic navigation controls (`NavigationLink`, `navigationDestination`) instead of non-semantic tap containers.
- Use polite announcements for async updates with `AccessibilityNotification`
  - e.g., `UIAccessibility.post(notification: .announcement, argument: "Saved")`.
- Locale-aware commands and shortcuts where keyboard interaction is supported.

## Animations
- Respect reduced motion: use `@Environment(\.accessibilityReduceMotion)` and provide non-animated alternatives.
- Prefer declarative animations (`withAnimation`, `animation`, `matchedGeometryEffect`) over manual timers.
- Keep animations performant by avoiding layout-affecting changes on frequently updated views.
- Use animatable properties that are cheap to animate (`opacity`, `scale`, `offset`, `transform`) before changing layout.
- Make animations interruptible and cancellation-safe.
- Keep animations tied to explicit intent (state change, user action), avoid autoplay or constant movement.
- Use meaningful timing and easing (`easeInOut`, spring settings) that fit the interaction.
- Avoid animating complex lists and geometry in one large transaction.
- For heavy transitions, set explicit `animation` and avoid `withAnimation` around large closures.
- For SVG-equivalent vector work, keep container transforms stable and avoid repaint churn.

## Layout
- Use consistent spacing tokens instead of hard-coded values.
- Validate alignment with grid and baseline; adjust optical alignment by one point when needed.
- Prefer `Layout`, `Grid`, and stack primitives over manual frame math.
- Let SwiftUI layout handle wrapping and adaptive behavior; avoid brittle `GeometryReader` unless necessary.
- Use `safeAreaInset`, `ignoresSafeArea`, and adaptive layout spacing for notched devices.
- Test on compact and regular size classes.
- Avoid unexpected scroll jitter by controlling `List`/`ScrollView` insets.
- Set predictable anchor and layout behavior to reduce jumps during async content updates.
- Predefine sizes and placeholders to reduce jump on image/content load.
- For wide-screen screens, avoid over-stretching by using centered containers and column width limits.

## Content
- Place helper text close to controls so users understand context before tooltips or secondary help.
- Use stable placeholder and loading shells to reduce layout changes.
- Make headings and section hierarchy clear (dynamic type compatible).
- Never leave dead-end states: include recovery actions or clear next steps.
- Design all states: empty, partial, loading, error, and empty-search.
- Use proper typographic hierarchy with platform-appropriate fonts and Dynamic Type scaling.
- Avoid relying on color alone; include symbols or text for state/intent.
- Prefer readable quotes and punctuation in localized strings.
- Keep numerals legible and stable (`UIFontMetrics` / Dynamic Type friendly styles).
- Use tabular numbers when comparing lists or tables.
- Ensure accessibility text for icons and decorative elements have `accessibilityHidden(true)` if purely visual.
- For headings and anchors, preserve readable jump behavior with `.scrollTargetLayout()` and clear ids.
- Support short, normal, and very long copy without clipping.
- Use locale-aware formatting for dates, numbers, and currency.
- Keep labels specific and unambiguous.
- Use `Text("...")` with proper localized ellipsis `"…"` when truncating.

## Forms
- Enter/submit behaviors should be explicit.
  - `SubmitLabel(.done)` and `.onSubmit` should reflect intended action.
- Label all controls clearly.
  - Include helper text and validation copy close to the field.
- Keep submit button enabled during input, then disable while request is in flight.
- Don\'t block typing with aggressive inline validation.
- Validate progressively and show errors near the control.
- For grouped controls, set intuitive `SubmitLabel` and keyboard return behavior.
- Keep `TextField` and `SecureField` keyboard types set correctly (`.emailAddress`, `.numberPad`, etc.).
- Use `textContentType`, `autocorrectionDisabled`, `autocapitalization` intentionally.
- Preserve pasted values when users paste tokens, codes, or secrets.
- Avoid exposing sensitive data in accessibility labels unless user chooses to reveal.
- Keep picker styles accessible and predictable across platforms.
- For OTP/code inputs, support one-time-code entry and paste behavior.
- Handle unsaved changes with confirmation on navigation pop / dismissal.
- Choose clear placeholder examples and show required/optional status.
- Ensure form controls retain state during async re-renders.

## Performance
- Test on low-memory and older devices before finalizing interaction-heavy views.
- Profile with Instruments, time profiler, and memory graph.
- Reduce body recomposition by separating stateful/cheap view components.
- Use `@StateObject` for long-lived owners, `@ObservedObject` for references, and avoid unnecessary `@Published` churn.
- Avoid expensive image decoding on main thread.
- Use image caching and downsampled assets in lists.
- Prefer lazy containers for large collections.
- Keep updates minimal by diffing data and using stable IDs.
- Batch state updates to avoid thrash on high-frequency events.
- Avoid unnecessary transitions in deeply nested views when no state changed.
- Preload critical assets; lazy load non-critical ones.
- Keep gesture recognizers and heavy computations outside view body when possible.
- Keep haptic and animation side effects on main thread-safe lifecycle events.

## Design
- Use layered visual hierarchy: elevation and border separation should be intentional.
- Keep border radii, shadows, and overlays consistent across reusable components.
- Use nested radii consistently; child corners should not exceed parent radii.
- Use color sets that remain readable in both light/dark and high-contrast modes.
- Ensure contrast and focus states are sufficient in all Dynamic Type sizes.
- Use APCA-minded contrast decisions for fine-grained readability tuning.
- Avoid hardcoded white/black text; use semantic colors where possible.
- Tune background/text contrast for buttons and controls in all states.
- Keep shadows lightweight and readable on OLED and dark-mode environments.
- Avoid banding-like transitions in dark gradients by adjusting assets or subtle texture.

## Copywriting for SwiftUI interfaces
- Use concise, action-first copy.
- Use second-person language for user-facing instructions.
- Prefer consistent terminology across screens and repeated workflows.
- Use clear state copy:
  - "Save" vs "Continue" (if ambiguous)
  - "Try again" vs generic "Error"
- Keep numbers readable (`8 deployments`, not `eight deployments`).
- Use consistent currency formatting within each screen.
- Leave spacing between number and unit (`10 MB` and non-breaking spacing for narrow UI contexts).
- Write failure copy with next-step guidance:
  - Instead of "Invalid key", say "Your key is invalid. Open Settings and generate a new one."
  - Instead of "Failed", say "Retry or contact support if the issue continues."
- Use placeholders consistently (`YOUR_API_TOKEN_HERE`, `123456`).

## SwiftUI adoption notes
- This skill is intended for SwiftUI implementation and review, not HTML/CSS-specific recommendations.
- Use this in code review, design implementation, and test planning for SwiftUI screens, forms, and motion.
